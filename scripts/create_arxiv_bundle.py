#!/usr/bin/env python3
"""Generate arXiv-ready TeX bundles from the paper Markdown sources."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


UNICODE_SANITIZE_REPLACEMENTS = (
    ("└──→", "+-->"),
    ("├──→", "+-->"),
    ("│", "|"),
    ("─", "-"),
)


@dataclass(frozen=True)
class ExportDefaults:
    input_format: str
    tex_engine: str
    verify_passes: int
    pandoc_args: tuple[str, ...]


@dataclass(frozen=True)
class ExportEntry:
    doc_id: str
    title: str
    source: Path
    output_dir: Path | None
    archive_name: str


def load_config(config_path: Path) -> dict[str, Any]:
    return json.loads(config_path.read_text(encoding="utf-8"))


def parse_defaults(payload: dict[str, Any]) -> ExportDefaults:
    raw_defaults = payload.get("defaults", {})
    if not isinstance(raw_defaults, dict):
        raise ValueError("'defaults' must be an object")

    pandoc_args = raw_defaults.get("pandoc_args", [])
    if not isinstance(pandoc_args, list) or not all(isinstance(item, str) for item in pandoc_args):
        raise ValueError("'defaults.pandoc_args' must be a list of strings")

    verify_passes = raw_defaults.get("verify_passes", 2)
    if not isinstance(verify_passes, int) or verify_passes < 1:
        raise ValueError("'defaults.verify_passes' must be an integer >= 1")

    tex_engine = raw_defaults.get("tex_engine", "xelatex")
    if not isinstance(tex_engine, str) or not tex_engine:
        raise ValueError("'defaults.tex_engine' must be a non-empty string")

    return ExportDefaults(
        input_format=str(raw_defaults.get("from", "markdown+smart+raw_attribute")),
        tex_engine=tex_engine,
        verify_passes=verify_passes,
        pandoc_args=tuple(pandoc_args),
    )


def parse_entries(payload: dict[str, Any], repo_root: Path) -> list[ExportEntry]:
    raw_documents = payload.get("documents")
    if not isinstance(raw_documents, list) or not raw_documents:
        raise ValueError("Config must contain a non-empty 'documents' list")

    entries: list[ExportEntry] = []
    for index, raw_document in enumerate(raw_documents, start=1):
        if not isinstance(raw_document, dict):
            raise ValueError("Each document must be an object")

        doc_id = str(raw_document.get("id", f"doc{index}"))
        title = str(raw_document.get("title", doc_id))
        source_value = raw_document.get("source")
        output_dir_value = raw_document.get("output_dir")
        archive_name = raw_document.get("archive_name")

        if not isinstance(source_value, str) or not source_value.strip():
            raise ValueError(f"Document '{doc_id}' must define a non-empty 'source'")
        if output_dir_value is not None and (
            not isinstance(output_dir_value, str) or not output_dir_value.strip()
        ):
            raise ValueError(f"Document '{doc_id}' has invalid 'output_dir'")
        if not isinstance(archive_name, str) or not archive_name.strip():
            raise ValueError(f"Document '{doc_id}' must define a non-empty 'archive_name'")

        entries.append(
            ExportEntry(
                doc_id=doc_id,
                title=title,
                source=(repo_root / source_value).resolve(),
                output_dir=(repo_root / output_dir_value).resolve() if output_dir_value else None,
                archive_name=archive_name,
            )
        )

    return entries


def select_entries(entries: list[ExportEntry], requested_ids: list[str]) -> list[ExportEntry]:
    if not requested_ids:
        return entries

    requested = set(requested_ids)
    selected = [entry for entry in entries if entry.doc_id in requested]
    missing = sorted(requested - {entry.doc_id for entry in selected})
    if missing:
        raise ValueError(f"Unknown document ids: {', '.join(missing)}")
    return selected


def sanitize_markdown(text: str) -> str:
    sanitized = text
    for needle, replacement in UNICODE_SANITIZE_REPLACEMENTS:
        sanitized = sanitized.replace(needle, replacement)
    return sanitized


def generate_tex(
    entry: ExportEntry,
    defaults: ExportDefaults,
    repo_root: Path,
    output_root: Path,
) -> Path:
    if not entry.source.exists():
        raise FileNotFoundError(f"Missing source file: {entry.source}")

    bundle_dir = entry.output_dir if entry.output_dir is not None else output_root / entry.doc_id
    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    bundle_dir.mkdir(parents=True, exist_ok=True)

    main_tex = bundle_dir / "main.tex"
    source_text = sanitize_markdown(entry.source.read_text(encoding="utf-8"))

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".md",
        encoding="utf-8",
        delete=False,
    ) as handle:
        handle.write(source_text)
        temp_source = Path(handle.name)

    try:
        cmd = [
            "pandoc",
            "--standalone",
            "--from",
            defaults.input_format,
            "-t",
            "latex",
            *defaults.pandoc_args,
            "-o",
            str(main_tex),
            str(temp_source),
        ]
        subprocess.run(cmd, check=True, cwd=repo_root)
    finally:
        temp_source.unlink(missing_ok=True)

    return main_tex


def copy_source_assets(entry: ExportEntry, bundle_dir: Path) -> None:
    """Copy figure/image asset directories from source into the bundle (preserving subdir structure) so TeX compilation resolves \\includegraphics{images/...} and \\includegraphics{figures/...} references."""
    source_root = entry.source.parent
    for asset_dir_name in ("figures", "images"):
        asset_dir = source_root / asset_dir_name
        if asset_dir.is_dir():
            dest_dir = bundle_dir / asset_dir_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            for asset in asset_dir.iterdir():
                if asset.is_file() and not asset.name.startswith("."):
                    shutil.copy2(asset, dest_dir / asset.name)


def replace_svg_with_pdf(main_tex: Path) -> None:
    """Replace \\includesvg{...svg} with \\includegraphics{...pdf} since inkscape is not assumed available at TeX compile time; PDF counterparts of figures are provided in the bundle by copy_source_assets."""
    text = main_tex.read_text(encoding="utf-8")
    import re
    text = re.sub(
        r"\\includesvg(\[[^\]]*\])?\{([^}]+)\.svg\}",
        r"\\includegraphics\1{\2.pdf}",
        text,
    )
    main_tex.write_text(text, encoding="utf-8")


def verify_tex(bundle_dir: Path, defaults: ExportDefaults) -> None:
    if not shutil.which(defaults.tex_engine):
        raise RuntimeError(
            f"TeX engine '{defaults.tex_engine}' was not found. "
            "Install it or use a different engine in publish_arxiv.json."
        )

    cmd = [
        defaults.tex_engine,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "main.tex",
    ]
    for _ in range(defaults.verify_passes):
        result = subprocess.run(
            cmd,
            check=False,
            cwd=bundle_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            output = "\n".join(
                part for part in (result.stdout.strip(), result.stderr.strip()) if part
            )
            raise RuntimeError(
                f"TeX verification failed in {bundle_dir} with engine '{defaults.tex_engine}'.\n{output}"
            )


def write_archive(bundle_dir: Path, archive_path: Path) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "w:gz") as archive:
        for path in sorted(bundle_dir.iterdir()):
            if path.name.startswith("."):
                continue
            if path.resolve() == archive_path.resolve():
                continue
            if path.suffix in {".aux", ".log", ".out", ".toc"}:
                continue
            if path.suffix == ".pdf":
                continue
            archive.add(path, arcname=path.name)


def write_preview(bundle_dir: Path, preview_path: Path) -> None:
    compiled_pdf = bundle_dir / "main.pdf"
    if not compiled_pdf.exists():
        raise FileNotFoundError(
            f"Compiled PDF not found at {compiled_pdf}. Run without --skip-verify to produce it."
        )
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(compiled_pdf, preview_path)


def cleanup_bundle(bundle_dir: Path) -> None:
    for path in bundle_dir.iterdir():
        if path.suffix in {".aux", ".log", ".out", ".pdf", ".toc", ".xdv"}:
            path.unlink(missing_ok=True)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=str(repo_root / "publish_arxiv.json"),
        help="Path to publish_arxiv.json. Defaults to the repository root file.",
    )
    parser.add_argument(
        "--document",
        action="append",
        default=[],
        help="Document id to export. Repeat to select multiple documents. Defaults to all documents.",
    )
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "arxiv"),
        help="Directory where per-paper arXiv folders will be written.",
    )
    parser.add_argument(
        "--write-archive",
        action="store_true",
        help="Also write a .tar.gz upload bundle inside each paper folder.",
    )
    parser.add_argument(
        "--write-preview",
        action="store_true",
        help="Copy the compiled PDF to arxiv_preview/ alongside the arxiv/ folder.",
    )
    parser.add_argument("--list", action="store_true", help="List the configured document ids and exit.")
    parser.add_argument("--skip-verify", action="store_true", help="Generate bundles without TeX compilation checks.")
    args = parser.parse_args()

    try:
        payload = load_config(Path(args.config).resolve())
        defaults = parse_defaults(payload)
        entries = parse_entries(payload, repo_root)
        selected_entries = select_entries(entries, args.document)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.list:
        for entry in entries:
            print(f"{entry.doc_id}: {entry.title}")
        return 0

    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    try:
        for entry in selected_entries:
            main_tex = generate_tex(
                entry=entry,
                defaults=defaults,
                repo_root=repo_root,
                output_root=output_root,
            )
            copy_source_assets(entry, main_tex.parent)
            replace_svg_with_pdf(main_tex)
            if not args.skip_verify:
                verify_tex(main_tex.parent, defaults)
            if args.write_preview:
                preview_name = entry.archive_name.replace("-arxiv.tar.gz", "-arxiv-preview.pdf")
                preview_path = main_tex.parent.parent / "arxiv_preview" / preview_name
                write_preview(main_tex.parent, preview_path)
            if args.write_archive:
                archive_path = main_tex.parent / entry.archive_name
                write_archive(main_tex.parent, archive_path)
                cleanup_bundle(main_tex.parent)
                print(f"ready {entry.doc_id}: {main_tex.parent} ({archive_path.name})")
            else:
                cleanup_bundle(main_tex.parent)
                print(f"ready {entry.doc_id}: {main_tex.parent}")
    except (FileNotFoundError, RuntimeError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
