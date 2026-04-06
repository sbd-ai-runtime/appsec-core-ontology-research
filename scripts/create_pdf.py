#!/usr/bin/env python3
"""Generate release PDFs from publish_docs.json or publish_docs.yaml."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PublishDefaults:
    input_format: str
    standalone: bool
    pdf_engine: str | None
    pandoc_args: tuple[str, ...]


@dataclass(frozen=True)
class PublishEntry:
    doc_id: str
    title: str
    sources: tuple[Path, ...]
    output: Path
    metadata: dict[str, Any]
    pdf_engine: str | None
    pandoc_args: tuple[str, ...]


def load_config(config_path: Path) -> dict[str, Any]:
    suffix = config_path.suffix.lower()
    raw_text = config_path.read_text(encoding="utf-8")
    if suffix == ".json":
        return json.loads(raw_text)
    if suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "YAML config requested but PyYAML is not installed. "
                "Use JSON or install PyYAML."
            ) from exc
        loaded = yaml.safe_load(raw_text)
        if not isinstance(loaded, dict):
            raise ValueError("YAML config must contain a top-level object")
        return loaded
    raise ValueError(f"Unsupported config format: {config_path.suffix}")


def parse_defaults(raw_defaults: dict[str, Any] | None) -> PublishDefaults:
    raw_defaults = raw_defaults or {}
    pandoc_args = raw_defaults.get("pandoc_args", [])
    if not isinstance(pandoc_args, list) or not all(isinstance(item, str) for item in pandoc_args):
        raise ValueError("'defaults.pandoc_args' must be a list of strings")

    return PublishDefaults(
        input_format=str(raw_defaults.get("from", "gfm+smart")),
        standalone=bool(raw_defaults.get("standalone", True)),
        pdf_engine=raw_defaults.get("pdf_engine"),
        pandoc_args=tuple(pandoc_args),
    )


def _ensure_output_in_repo(output_path: Path, repo_root: Path) -> Path:
    resolved = output_path.resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"Output path must stay inside the repo root: {resolved}") from exc
    return resolved


def parse_publish_docs(config_path: Path, repo_root: Path) -> tuple[PublishDefaults, list[PublishEntry]]:
    payload = load_config(config_path)
    defaults = parse_defaults(payload.get("defaults"))

    raw_documents = payload.get("documents")
    if not isinstance(raw_documents, list) or not raw_documents:
        raise ValueError("Config must contain a non-empty 'documents' list")

    entries: list[PublishEntry] = []
    for index, raw_doc in enumerate(raw_documents, start=1):
        if not isinstance(raw_doc, dict):
            raise ValueError("Each document entry must be an object")

        doc_id = str(raw_doc.get("id", f"doc{index}"))
        title = str(raw_doc.get("title", doc_id))
        sources = raw_doc.get("sources")
        if not isinstance(sources, list) or not sources or not all(isinstance(item, str) for item in sources):
            raise ValueError(f"Document '{doc_id}' must define a non-empty 'sources' list")

        output_value = raw_doc.get("output")
        if not isinstance(output_value, str) or not output_value.strip():
            raise ValueError(f"Document '{doc_id}' must define an 'output' path")

        metadata = raw_doc.get("metadata", {})
        if not isinstance(metadata, dict):
            raise ValueError(f"Document '{doc_id}' has invalid 'metadata'; expected an object")

        pandoc_args = raw_doc.get("pandoc_args", [])
        if not isinstance(pandoc_args, list) or not all(isinstance(item, str) for item in pandoc_args):
            raise ValueError(f"Document '{doc_id}' has invalid 'pandoc_args'; expected a list of strings")

        source_paths = tuple((repo_root / source).resolve() for source in sources)
        output_path = _ensure_output_in_repo(repo_root / output_value, repo_root)

        entries.append(
            PublishEntry(
                doc_id=doc_id,
                title=title,
                sources=source_paths,
                output=output_path,
                metadata=metadata,
                pdf_engine=raw_doc.get("pdf_engine"),
                pandoc_args=tuple(pandoc_args),
            )
        )

    return defaults, entries


def metadata_args(metadata: dict[str, Any]) -> list[str]:
    args: list[str] = []
    for key, value in metadata.items():
        if isinstance(value, bool):
            serialized = "true" if value else "false"
        elif isinstance(value, (int, float, str)):
            serialized = str(value)
        else:
            raise ValueError(
                f"Unsupported metadata value for '{key}'. "
                "Use scalar values only or pass custom flags via 'pandoc_args'."
            )
        args.extend(["--metadata", f"{key}={serialized}"])
    return args


def resolve_pdf_engine(explicit_engine: str | None, defaults: PublishDefaults) -> list[str]:
    engine = explicit_engine if explicit_engine is not None else defaults.pdf_engine
    if not engine:
        return []
    return ["--pdf-engine", engine]


def build_pdf(
    entry: PublishEntry,
    defaults: PublishDefaults,
    pandoc_bin: str,
    repo_root: Path,
    dry_run: bool,
) -> None:
    missing_sources = [str(path) for path in entry.sources if not path.exists()]
    if missing_sources:
        raise FileNotFoundError(f"Missing source files for {entry.output.name}: {', '.join(missing_sources)}")

    entry.output.parent.mkdir(parents=True, exist_ok=True)

    cmd = [pandoc_bin]
    if defaults.standalone:
        cmd.append("--standalone")
    cmd.extend(["--from", defaults.input_format])
    cmd.extend(resolve_pdf_engine(entry.pdf_engine, defaults))
    cmd.extend(defaults.pandoc_args)
    cmd.extend(entry.pandoc_args)
    cmd.extend(metadata_args(entry.metadata))
    cmd.extend(["-o", str(entry.output)])
    cmd.extend(str(path) for path in entry.sources)

    print("$ " + " ".join(cmd))
    if dry_run:
        return

    subprocess.run(cmd, check=True, cwd=repo_root)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=str(repo_root / "publish_docs.json"),
        help="Path to publish_docs.json or publish_docs.yaml. Defaults to publish_docs.json in the repo root.",
    )
    parser.add_argument("--pandoc", default="pandoc", help="Pandoc executable to use.")
    parser.add_argument("--list", action="store_true", help="List the resolved publish mappings and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Print pandoc commands without executing them.")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    try:
        defaults, entries = parse_publish_docs(config_path=config_path, repo_root=repo_root)
    except Exception as exc:  # pragma: no cover - CLI path
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.list:
        for entry in entries:
            sources = "; ".join(str(path) for path in entry.sources)
            print(f"{entry.doc_id}: {sources} -> {entry.output}")
        return 0

    if not shutil.which(args.pandoc):
        print(
            f"error: pandoc executable '{args.pandoc}' was not found. "
            "Install pandoc or use --pandoc to point to it.",
            file=sys.stderr,
        )
        return 1

    try:
        for entry in entries:
            build_pdf(
                entry=entry,
                defaults=defaults,
                pandoc_bin=args.pandoc,
                repo_root=repo_root,
                dry_run=args.dry_run,
            )
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
