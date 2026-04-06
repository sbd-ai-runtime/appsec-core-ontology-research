#!/usr/bin/env python3
"""Sync curated V1 artifact files into the public release repository."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArtifactFile:
    source_repo: str
    source: str
    dest: str


@dataclass(frozen=True)
class ArtifactBundle:
    bundle_id: str
    description: str
    files: tuple[ArtifactFile, ...]


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_manifest(path: Path) -> tuple[dict[str, str], list[ArtifactBundle]]:
    raw = load_manifest(path)
    source_roots = raw.get("source_roots")
    bundles = raw.get("bundles")

    if not isinstance(source_roots, dict) or not source_roots:
        raise ValueError("Manifest must define a non-empty 'source_roots' object")
    if not isinstance(bundles, list) or not bundles:
        raise ValueError("Manifest must define a non-empty 'bundles' array")

    parsed_bundles: list[ArtifactBundle] = []
    for raw_bundle in bundles:
        if not isinstance(raw_bundle, dict):
            raise ValueError("Each bundle must be an object")
        bundle_id = raw_bundle.get("id")
        description = raw_bundle.get("description", "")
        raw_files = raw_bundle.get("files")
        if not isinstance(bundle_id, str) or not bundle_id:
            raise ValueError("Each bundle must define a non-empty string 'id'")
        if not isinstance(raw_files, list) or not raw_files:
            raise ValueError(f"Bundle '{bundle_id}' must define a non-empty 'files' array")

        files: list[ArtifactFile] = []
        for raw_file in raw_files:
            if not isinstance(raw_file, dict):
                raise ValueError(f"Bundle '{bundle_id}' contains a non-object file entry")
            try:
                source_repo = raw_file["source_repo"]
                source = raw_file["source"]
                dest = raw_file["dest"]
            except KeyError as exc:
                raise ValueError(f"Bundle '{bundle_id}' has a file entry missing {exc}") from exc
            if not all(isinstance(value, str) and value for value in (source_repo, source, dest)):
                raise ValueError(f"Bundle '{bundle_id}' contains an invalid file entry")
            files.append(ArtifactFile(source_repo=source_repo, source=source, dest=dest))

        parsed_bundles.append(
            ArtifactBundle(
                bundle_id=bundle_id,
                description=str(description),
                files=tuple(files),
            )
        )

    return {str(key): str(value) for key, value in source_roots.items()}, parsed_bundles


def parse_source_root_overrides(values: list[str]) -> dict[str, str]:
    overrides: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"Invalid --source-root override '{value}'. Expected repo_id=path.")
        repo_id, path = value.split("=", 1)
        repo_id = repo_id.strip()
        path = path.strip()
        if not repo_id or not path:
            raise ValueError(f"Invalid --source-root override '{value}'. Expected repo_id=path.")
        overrides[repo_id] = path
    return overrides


def resolve_source_roots(repo_root: Path, defaults: dict[str, str], overrides: dict[str, str]) -> dict[str, Path]:
    resolved: dict[str, Path] = {}
    for repo_id, path_value in defaults.items():
        path = overrides.get(repo_id, path_value)
        resolved[repo_id] = (repo_root / path).resolve()
    return resolved


def selected_bundles(all_bundles: list[ArtifactBundle], requested: list[str]) -> list[ArtifactBundle]:
    if not requested:
        return all_bundles
    requested_set = set(requested)
    bundles = [bundle for bundle in all_bundles if bundle.bundle_id in requested_set]
    missing = sorted(requested_set - {bundle.bundle_id for bundle in bundles})
    if missing:
        raise ValueError(f"Unknown bundle ids: {', '.join(missing)}")
    return bundles


def ensure_dest_in_repo(dest: Path, repo_root: Path) -> Path:
    resolved = dest.resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"Destination must remain inside repo root: {resolved}") from exc
    return resolved


def sync_bundle(
    bundle: ArtifactBundle,
    source_roots: dict[str, Path],
    repo_root: Path,
    dry_run: bool,
) -> tuple[int, int]:
    copied = 0
    skipped = 0
    for artifact in bundle.files:
        if artifact.source_repo not in source_roots:
            raise ValueError(f"Unknown source repo '{artifact.source_repo}' in bundle '{bundle.bundle_id}'")

        source_path = (source_roots[artifact.source_repo] / artifact.source).resolve()
        dest_path = ensure_dest_in_repo(repo_root / artifact.dest, repo_root)

        if not source_path.exists():
            raise FileNotFoundError(f"Missing source file: {source_path}")

        if dest_path.exists() and source_path.read_bytes() == dest_path.read_bytes():
            print(f"skip {bundle.bundle_id}: {artifact.dest}")
            skipped += 1
            continue

        print(f"copy {bundle.bundle_id}: {source_path} -> {dest_path}")
        if not dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dest_path)
        copied += 1

    return copied, skipped


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=str(repo_root / "publish_artifacts.json"),
        help="Path to publish_artifacts.json. Defaults to the repository root file.",
    )
    parser.add_argument(
        "--bundle",
        action="append",
        default=[],
        help="Bundle id to sync. Repeat to select multiple bundles. Defaults to all bundles.",
    )
    parser.add_argument(
        "--source-root",
        action="append",
        default=[],
        help="Override a source root as repo_id=path.",
    )
    parser.add_argument("--list", action="store_true", help="List bundle ids and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Print copy operations without executing them.")
    args = parser.parse_args()

    try:
        default_source_roots, bundles = parse_manifest(Path(args.config).resolve())
        overrides = parse_source_root_overrides(args.source_root)
        bundle_selection = selected_bundles(bundles, args.bundle)
        source_roots = resolve_source_roots(repo_root, default_source_roots, overrides)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.list:
        for bundle in bundles:
            print(f"{bundle.bundle_id}: {bundle.description}")
        return 0

    try:
        copied = 0
        skipped = 0
        for bundle in bundle_selection:
            bundle_copied, bundle_skipped = sync_bundle(
                bundle=bundle,
                source_roots=source_roots,
                repo_root=repo_root,
                dry_run=args.dry_run,
            )
            copied += bundle_copied
            skipped += bundle_skipped
        print(f"done: copied={copied} skipped={skipped}")
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
