#!/usr/bin/env python3
"""build_sources_original_archive.py — Bundle original source files into a single zip.

Cartographer 2026-05-09 — programme-lead Pedro Farinha ratified inclusion of
original source files as a single zip artefact for paper7 figshare deposit.

For each of the 31 substrate-v7 sources, locates the original downloaded
artefact(s) at one of:
- Worktree sources/<source>/  (5 iter-3 + 4 EU regs captured 2026-05-07/2026-05-09)
- Parent ESI sources/<source>/ (22 baseline sources captured 2026-04-03..15)

Builds deterministic zip archive at:
- data/p7_publish_bundle/sources_original.zip
- data/p7_publish_bundle/sources_original_manifest.json

Determinism: fixed timestamp (substrate-v7 anchor 2026-05-08) + sorted file
order + ZIP_DEFLATED compression → reproducible sha256 across re-runs given
identical input file set.

License notice: original source files retain their upstream licenses
(varies per source; see data/<source>/stubs/source_retrieval_receipt.json
and pilots/<source>/source_manifest.yaml for per-source license details).
This zip is research-dataset distribution under fair use / EU public sector
reuse / OWASP CC-BY-SA / NIST public domain / etc. — not commercial reuse.

Authority: programme-lead Pedro Farinha 2026-05-09; figshare deposit
self-contained archive convention.
"""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PARENT_ESI = Path("/Volumes/G-DRIVE/Shared/SecurityByDesign-TheoryOfEverything/ExternalSourcesInventory")
WORKTREE_SOURCES = REPO_ROOT / "sources"
PARENT_SOURCES = PARENT_ESI / "sources"
SUPPLIER_PATH = REPO_ROOT / "data" / "p7_olir_audit" / "p7_v2_corrected" / "v7" / "SUPPLIER_v7_0.json"
OUT_DIR = REPO_ROOT / "data" / "p7_publish_bundle"
OUT_ZIP = OUT_DIR / "sources_original.zip"
OUT_MANIFEST = OUT_DIR / "sources_original_manifest.json"

# Fixed timestamp (substrate-v7 emission anchor: 2026-05-07; ZIP needs UTC tuple)
ZIP_DATE = (2026, 5, 7, 12, 0, 0)


@dataclass
class FileEntry:
    pilot_id: str
    relative_path: str   # within zip: <pilot_id>/<filename>
    source_path: str      # absolute path on disk
    size_bytes: int
    sha256: str


def supplier_sources() -> list[str]:
    raw = json.loads(SUPPLIER_PATH.read_text(encoding="utf-8"))
    items = raw.get("items") or raw.get("contracts") or []
    return sorted({item.get("source") for item in items if item.get("source")})


def find_source_dir(src: str) -> Path | None:
    """Locate source dir at worktree first; fallback to parent ESI checkout."""
    worktree_dir = WORKTREE_SOURCES / src
    if worktree_dir.is_dir() and any(worktree_dir.iterdir()):
        return worktree_dir
    parent_dir = PARENT_SOURCES / src
    if parent_dir.is_dir() and any(parent_dir.iterdir()):
        return parent_dir
    return None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    sources = supplier_sources()
    if len(sources) != 31:
        print(f"warning: {len(sources)} sources from SUPPLIER (expected 31)", file=sys.stderr)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    entries: list[FileEntry] = []
    missing_sources: list[str] = []

    # Sort sources alphabetically for deterministic order
    for src in sources:
        src_dir = find_source_dir(src)
        if src_dir is None:
            missing_sources.append(src)
            continue

        # Sort files alphabetically for deterministic order
        for path in sorted(src_dir.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(src_dir)
            archive_name = f"{src}/{rel.as_posix()}"
            entries.append(FileEntry(
                pilot_id=src,
                relative_path=archive_name,
                source_path=str(path),
                size_bytes=path.stat().st_size,
                sha256=sha256_file(path),
            ))

    print(f"Building zip with {len(entries)} files across {len(sources) - len(missing_sources)} sources...")
    if missing_sources:
        print(f"  WARNING: {len(missing_sources)} sources have no local files: {missing_sources}", file=sys.stderr)

    with zipfile.ZipFile(OUT_ZIP, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for entry in entries:
            info = zipfile.ZipInfo(filename=entry.relative_path, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(entry.source_path, "rb") as fh:
                zf.writestr(info, fh.read())

    zip_size = OUT_ZIP.stat().st_size
    zip_sha = sha256_file(OUT_ZIP)

    sources_present = sorted(set(e.pilot_id for e in entries))
    by_source = {src: [] for src in sources_present}
    for e in entries:
        by_source[e.pilot_id].append({
            "relative_path": e.relative_path,
            "size_bytes": e.size_bytes,
            "sha256": e.sha256,
        })

    manifest = {
        "schema_version": "1.0",
        "archive_path": "data/p7_publish_bundle/sources_original.zip",
        "archive_size_bytes": zip_size,
        "archive_sha256": zip_sha,
        "build_timestamp_anchor": "2026-05-07T12:00:00Z (deterministic; substrate-v7 anchor)",
        "supplier_sha256": "596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04",
        "total_files": len(entries),
        "total_sources": len(sources_present),
        "missing_sources": missing_sources,
        "sources_present": sources_present,
        "files_by_source": by_source,
        "license_notice": (
            "Original source files retain their upstream licenses. See "
            "data/<source>/stubs/source_retrieval_receipt.json or "
            "pilots/<source>/source_manifest.yaml for per-source license. "
            "Research-dataset distribution under fair use / public-sector "
            "reuse / OWASP CC-BY-SA / NIST public-domain / EU public-sector "
            "reuse policy (Commission Decision 2011/833/EU). Not commercial reuse."
        ),
    }

    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print()
    print(f"emitted: {OUT_ZIP.relative_to(REPO_ROOT)}")
    print(f"  size: {zip_size:,} bytes ({zip_size / (1024*1024):.2f} MB)")
    print(f"  sha256: {zip_sha}")
    print(f"emitted: {OUT_MANIFEST.relative_to(REPO_ROOT)}")
    print(f"  files: {len(entries)}")
    print(f"  sources present: {len(sources_present)} / {len(sources)}")
    if missing_sources:
        print(f"  sources missing: {missing_sources}")
    return 0 if not missing_sources else 1


if __name__ == "__main__":
    raise SystemExit(main())
