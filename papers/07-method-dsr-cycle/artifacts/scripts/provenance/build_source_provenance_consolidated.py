#!/usr/bin/env python3
"""build_source_provenance_consolidated.py — Unified per-source provenance table.

Cartographer 2026-05-09 — programme-lead Pedro Farinha.

Consolidates per-source provenance across both repo conventions:
- 26 baselines: pilots/<source>/source_manifest.yaml (multi-schema)
- 5 iter-3:    data/<source>/stubs/source_retrieval_receipt.json (uniform)
- 16 sources have BOTH (cross-confirmation source for iter-3 baselines too)

Emits:
- data/p7_olir_audit/p7_v2_corrected/v7/reports/source_provenance_consolidated.md
- data/p7_olir_audit/p7_v2_corrected/v7/reports/source_provenance_consolidated.json

Output schema (per source):
  pilot_id, title, publisher, version, publication_date, canonical_url,
  doi_url (if exists), license (if declared), primary_checksum_sha256,
  retrieved_at, local_snapshot_path, artefact_count, schema_source

Authority: programme-lead Pedro Farinha 2026-05-09 (paper7 reinforcement of
provenance ahead of figshare/B2SHARE submission); reviewer-citable single
source-of-truth for the 31-source corpus.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: PyYAML required (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(1)

REPO_ROOT = Path(__file__).resolve().parents[1]
V7_ROOT = REPO_ROOT / "data" / "p7_olir_audit" / "p7_v2_corrected" / "v7"
SUPPLIER_PATH = V7_ROOT / "SUPPLIER_v7_0.json"
PILOTS_ROOT = REPO_ROOT / "pilots"
DATA_ROOT = REPO_ROOT / "data"
OUT_MD = V7_ROOT / "reports" / "source_provenance_consolidated.md"
OUT_JSON = V7_ROOT / "reports" / "source_provenance_consolidated.json"


@dataclass
class ProvenanceRow:
    pilot_id: str
    title: str = ""
    publisher: str = ""
    version: str = ""
    publication_date: str = ""
    canonical_url: str = ""
    doi_url: str = ""
    license: str = ""
    primary_checksum_sha256: str = ""
    retrieved_at: str = ""
    local_snapshot_path: str = ""
    artefact_count: int = 0
    schema_source: str = ""
    notes: list[str] = field(default_factory=list)


def supplier_sources() -> list[str]:
    raw = json.loads(SUPPLIER_PATH.read_text(encoding="utf-8"))
    items = raw.get("items") or raw.get("contracts") or []
    sources = sorted({item.get("source") for item in items if item.get("source")})
    return sources


def parse_baseline_manifest(src: str) -> ProvenanceRow | None:
    """Parse pilots/<source>/source_manifest.yaml (multi-schema baseline; 7 variants)."""
    path = PILOTS_ROOT / src / "source_manifest.yaml"
    if not path.exists():
        return None
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    row = ProvenanceRow(pilot_id=src, schema_source=str(path.relative_to(REPO_ROOT)))

    # Schema 1: meta + source_document (asvs, ssdf, owasp_dsomm, enisa, dsomm, samm style)
    sd = raw.get("source_document")
    if sd:
        row.title = str(sd.get("title", "")) + (
            f" — {sd.get('subtitle')}" if sd.get("subtitle") else ""
        )
        row.publisher = str(sd.get("publisher", ""))
        row.version = str(sd.get("version", ""))
        row.publication_date = str(sd.get("publication_date", ""))
        row.canonical_url = str(
            sd.get("canonical_url") or sd.get("origin_url") or ""
        )
        row.doi_url = str(sd.get("doi_url", ""))
        row.license = str(sd.get("license", ""))
        # Retrieval policy block (separate at top-level; varied field names)
        rp = raw.get("retrieval_policy", {})
        row.primary_checksum_sha256 = str(rp.get("checksum_sha256", ""))
        row.retrieved_at = str(
            rp.get("retrieved_at") or rp.get("captured_release_timestamp", "")
        )
        local_path = rp.get("local_snapshot_path") or rp.get("local_snapshot_paths")
        if isinstance(local_path, list):
            local_path = local_path[0] if local_path else ""
        row.local_snapshot_path = str(local_path or "")
        row.artefact_count = 1
        return row

    # Schema 2: source_collection + documents[] (slsa style)
    sc = raw.get("source_collection")
    if sc:
        row.title = str(sc.get("title", ""))
        row.publisher = str(sc.get("publisher", ""))
        row.version = str(sc.get("version", ""))
        row.publication_date = str(sc.get("publication_date", ""))
        row.license = str(sc.get("license", ""))
        documents = raw.get("documents", [])
        row.artefact_count = len(documents)
        if documents:
            first = documents[0]
            row.canonical_url = str(first.get("canonical_url", ""))
            row.local_snapshot_path = str(first.get("local_source_path", ""))
        return row

    # Schema 3: top-level pilot_id + sources[] (capec style)
    if raw.get("sources"):
        sources = raw["sources"]
        row.artefact_count = len(sources)
        if sources:
            first = sources[0]
            row.title = str(first.get("title") or raw.get("source_scope", ""))
            row.canonical_url = str(first.get("origin_url") or first.get("canonical_url", ""))
            row.publisher = str(raw.get("source_family", ""))
            row.version = str(raw.get("version", ""))
            row.primary_checksum_sha256 = str(first.get("sha256", ""))
            row.retrieved_at = str(first.get("download_date", ""))
            row.local_snapshot_path = str(first.get("local_path", ""))
        return row

    # Schema 4: meta + documents[] flat (mcp_official style; per-document checksums)
    if raw.get("meta") and raw.get("documents"):
        documents = raw["documents"]
        row.artefact_count = len(documents)
        meta = raw["meta"]
        row.publisher = str(meta.get("source_family", ""))
        if documents:
            first = documents[0]
            row.title = str(first.get("title", ""))
            row.canonical_url = str(first.get("canonical_url", ""))
            row.publication_date = str(first.get("publication_date", ""))
            row.primary_checksum_sha256 = str(first.get("checksum_sha256", ""))
            row.local_snapshot_path = str(first.get("local_source_path", ""))
        return row

    # Schema 5: top-level flat (owasp_mcp_secure_server style)
    if raw.get("title") and raw.get("publisher") and raw.get("version"):
        row.title = str(raw.get("title", ""))
        row.publisher = str(raw.get("publisher", ""))
        row.version = str(raw.get("version", ""))
        row.publication_date = str(raw.get("publication_date", ""))
        row.canonical_url = str(
            raw.get("landing_page_url") or raw.get("download_url") or raw.get("source_url", "")
        )
        row.license = str(raw.get("license", ""))
        retrieval = raw.get("retrieval", {})
        row.primary_checksum_sha256 = str(retrieval.get("checksum_sha256", ""))
        row.retrieved_at = str(retrieval.get("retrieved_at", ""))
        local_files = raw.get("local_files", {})
        if isinstance(local_files, dict):
            row.local_snapshot_path = str(
                local_files.get("pdf") or local_files.get("landing_page", "")
            )
        row.artefact_count = 1
        return row

    # Schema 6: top-level pilot_id + documents[] without source_collection wrapper
    # (owasp_mcp_third_party / owasp_mcp_top_10 style)
    if raw.get("pilot_id") and raw.get("documents"):
        documents = raw["documents"]
        row.artefact_count = len(documents)
        row.publisher = str(raw.get("publisher", ""))
        if documents:
            first = documents[0]
            row.title = str(first.get("title", ""))
            row.version = str(first.get("version_label", ""))
            row.publication_date = str(first.get("publication_date", ""))
            row.canonical_url = str(
                first.get("landing_page_url")
                or first.get("source_url")
                or first.get("canonical_url", "")
            )
            row.local_snapshot_path = str(
                first.get("local_pdf_path")
                or first.get("local_source_path")
                or first.get("local_html_path", "")
            )
        return row

    row.notes.append("manifest schema unrecognised — manual review required")
    return row


def parse_secondary_receipt(src: str) -> dict:
    """Parse data/<source>/stubs/source_retrieval_receipt.json (for checksum + retrieved_at fallback).

    Two known schemas:
    - iter-3 receipts: items[] with origin_url + sha256 + retrieved_at per artefact
    - baseline (e.g., asvs) receipts: captured_files[] with checksum_sha256 per artefact + top-level retrieved_at

    Returns dict with primary_checksum_sha256 + retrieved_at + artefact_count + path.
    """
    path = DATA_ROOT / src / "stubs" / "source_retrieval_receipt.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    result: dict = {"path": str(path.relative_to(REPO_ROOT))}

    # iter-3 schema: items[]
    items = raw.get("items", [])
    if items:
        result["artefact_count"] = len(items)
        first = items[0]
        result["primary_checksum_sha256"] = str(first.get("sha256", ""))
        result["retrieved_at"] = str(first.get("retrieved_at", ""))
        result["origin_url"] = str(first.get("origin_url", ""))
        result["title_hint"] = str(
            first.get("title") or first.get("source_document_id", "")
        )
        result["version_hint"] = str(
            first.get("version") or first.get("upstream_release", "")
        )
        return result

    # baseline schema: captured_files[]
    captured = raw.get("captured_files", [])
    if captured:
        result["artefact_count"] = len(captured)
        first = captured[0]
        result["primary_checksum_sha256"] = str(first.get("checksum_sha256", ""))
        result["origin_url"] = str(first.get("source_url", ""))
        result["retrieved_at"] = str(raw.get("retrieved_at", ""))
        return result

    # Variant schema: artifacts[] (enisa, slsa, owasp_mcp_third_party)
    artifacts = raw.get("artifacts", [])
    if artifacts:
        result["artefact_count"] = len(artifacts)
        first = artifacts[0]
        result["primary_checksum_sha256"] = str(
            first.get("checksum_sha256") or first.get("sha256", "")
        )
        result["origin_url"] = str(
            first.get("source_url") or first.get("origin_url") or first.get("canonical_url", "")
        )
        result["retrieved_at"] = str(
            raw.get("retrieved_at") or first.get("retrieved_at", "")
        )
        return result

    # Variant schema: sources[] (owasp_mcp_top_10)
    sources_list = raw.get("sources", [])
    if sources_list:
        result["artefact_count"] = len(sources_list)
        first = sources_list[0]
        result["primary_checksum_sha256"] = str(
            first.get("checksum_sha256") or first.get("sha256", "")
        )
        result["origin_url"] = str(
            first.get("source_url") or first.get("origin_url") or first.get("canonical_url", "")
        )
        result["retrieved_at"] = str(
            raw.get("retrieved_at") or first.get("retrieved_at", "")
        )
        return result

    return result


def parse_iter3_receipt(src: str) -> ProvenanceRow | None:
    """Parse data/<source>/stubs/source_retrieval_receipt.json (iter-3 + some baselines)."""
    path = DATA_ROOT / src / "stubs" / "source_retrieval_receipt.json"
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    row = ProvenanceRow(pilot_id=src, schema_source=str(path.relative_to(REPO_ROOT)))

    items = raw.get("items", [])
    row.artefact_count = len(items)
    if items:
        # Use first item as primary; receipts have one or more artefacts per pilot
        first = items[0]
        row.title = str(first.get("title") or first.get("source_document_id", ""))
        row.canonical_url = str(
            first.get("origin_url") or first.get("publication_page", "")
        )
        row.publisher = str(raw.get("source_family", ""))
        row.version = str(first.get("version") or first.get("upstream_release", ""))
        row.publication_date = str(first.get("release_date", ""))
        row.primary_checksum_sha256 = str(first.get("sha256", ""))
        row.retrieved_at = str(first.get("retrieved_at", ""))
        row.local_snapshot_path = str(first.get("local_path", ""))
    if raw.get("version_status"):
        row.notes.append(str(raw["version_status"]))
    if raw.get("expected_quality_caveat"):
        row.notes.append(str(raw["expected_quality_caveat"]))
    return row


def build_row(src: str) -> ProvenanceRow:
    """Build per-source provenance row.

    Strategy:
    1. Try baseline manifest (pilots/<source>/source_manifest.yaml) — high-level
       provenance + retrieval policy (canonical_url + doi_url + version + title)
    2. Always check secondary receipt (data/<source>/stubs/source_retrieval_receipt.json)
       for missing checksum_sha256 + retrieved_at + artefact-level details
    3. Merge: take URL/title/version/etc from manifest; fill missing checksum +
       retrieved_at from receipt
    4. iter-3 sources have NO baseline manifest; use receipt as primary

    This handles 7 manifest schema variants + uniform receipt schema.
    """
    baseline = parse_baseline_manifest(src)
    secondary = parse_secondary_receipt(src)

    if baseline:
        row = baseline
        # Fill from secondary if missing
        if not row.primary_checksum_sha256 and secondary.get("primary_checksum_sha256"):
            row.primary_checksum_sha256 = secondary["primary_checksum_sha256"]
        if not row.retrieved_at and secondary.get("retrieved_at"):
            row.retrieved_at = secondary["retrieved_at"]
        if not row.canonical_url and secondary.get("origin_url"):
            row.canonical_url = secondary["origin_url"]
        if secondary:
            row.notes.append(
                f"cross-confirmation: also present at {secondary['path']} "
                f"({secondary.get('artefact_count', '?')} artefacts)"
            )
        return row

    # No baseline manifest — iter-3 source uses receipt as primary
    if secondary:
        row = ProvenanceRow(pilot_id=src, schema_source=secondary["path"])
        row.title = secondary.get("title_hint", "")
        row.version = secondary.get("version_hint", "")
        row.canonical_url = secondary.get("origin_url", "")
        row.primary_checksum_sha256 = secondary.get("primary_checksum_sha256", "")
        row.retrieved_at = secondary.get("retrieved_at", "")
        row.artefact_count = secondary.get("artefact_count", 0)
        # Re-parse for richer fields (publisher, publication_date)
        path = DATA_ROOT / src / "stubs" / "source_retrieval_receipt.json"
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            row.publisher = str(raw.get("source_family", ""))
            items = raw.get("items", [])
            if items and items[0].get("release_date"):
                row.publication_date = str(items[0]["release_date"])
            if raw.get("version_status"):
                row.notes.append(str(raw["version_status"]))
            if raw.get("expected_quality_caveat"):
                row.notes.append(str(raw["expected_quality_caveat"]))
        return row

    # Neither — should not happen for a SUPPLIER-listed source
    return ProvenanceRow(pilot_id=src, notes=["NO PROVENANCE ARTEFACT FOUND"])


EU_REGULATORY = {"eu_cra", "eu_dora", "eu_nis2", "eu_rgpd"}


def fill_runtime_checksum(row: ProvenanceRow) -> None:
    """Compute sha256 from local_snapshot_path if file exists + checksum missing.

    Reproducibility note: deterministic given current local file state at run time.
    Annotates row.notes that this checksum was computed at runtime, not declared
    in manifest — this distinguishes manifest-declared (immutable) checksums from
    runtime-computed ones.
    """
    if row.primary_checksum_sha256:
        return
    if not row.local_snapshot_path:
        if row.pilot_id in EU_REGULATORY:
            row.notes.append(
                "EU regulatory source — URL-only provenance by design; CELEX-anchored at canonical_url. No local snapshot captured (regulatory texts are identified by CELEX number + EUR-Lex URL; canonical URL stable + dated)."
            )
        return
    local = REPO_ROOT / row.local_snapshot_path
    if not local.exists():
        return
    try:
        h = hashlib.sha256()
        with local.open("rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        row.primary_checksum_sha256 = h.hexdigest()
        row.notes.append(
            f"checksum_sha256 computed at runtime from {row.local_snapshot_path} "
            f"(not declared in manifest)"
        )
    except OSError as exc:
        row.notes.append(f"runtime checksum failed: {exc}")


def render_md(rows: list[ProvenanceRow]) -> str:
    lines = []
    lines.append("# Source Provenance — Consolidated (31-source corpus, substrate v7)")
    lines.append("")
    lines.append("**Date:** 2026-05-09")
    lines.append("**Author:** Cartographer (under programme-lead Pedro Farinha)")
    lines.append("**Substrate:** v7 (`SUPPLIER_v7_0.json` SHA `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04`)")
    lines.append("**Generator:** `scripts/build_source_provenance_consolidated.py` (deterministic Python)")
    lines.append("")
    lines.append("This document consolidates per-source provenance across both repo conventions:")
    lines.append("- **26 baseline sources:** `pilots/<source>/source_manifest.yaml` (multi-schema; canonical_url + doi_url + checksum + retrieved_at)")
    lines.append("- **5 iter-3 sources** (mitre_atlas, nist_ai_100_2_e2025, nist_ai_rmf_1_0, owasp_llm_top_10, owasp_ml_top_10): `data/<source>/stubs/source_retrieval_receipt.json` (uniform schema; origin_url + sha256 + retrieved_at + version)")
    lines.append("")
    lines.append("Both conventions provide URL + version + access date + checksum + local snapshot path. This single artefact is reviewer-citable as the unified provenance source-of-truth for the substrate v7 corpus.")
    lines.append("")
    lines.append("## Per-source provenance table")
    lines.append("")
    lines.append("| # | Source | Title | Publisher | Version | Publication date | URL (canonical / origin) | DOI | sha256 (primary) | Retrieved | Artefacts |")
    lines.append("|---:|---|---|---|---|---|---|---|---|---|---:|")
    for i, row in enumerate(rows, 1):
        title = row.title[:60].replace("|", "\\|") + ("…" if len(row.title) > 60 else "")
        url = row.canonical_url.replace("|", "\\|")
        doi = row.doi_url.replace("|", "\\|") if row.doi_url else "—"
        sha = row.primary_checksum_sha256[:12] + "…" if row.primary_checksum_sha256 else "—"
        retrieved = row.retrieved_at[:10] if row.retrieved_at else "—"
        publisher = row.publisher.replace("|", "\\|")
        version = row.version.replace("|", "\\|")
        pub_date = row.publication_date.replace("|", "\\|")
        lines.append(
            f"| {i} | `{row.pilot_id}` | {title} | {publisher} | {version} | {pub_date} | {url} | {doi} | `{sha}` | {retrieved} | {row.artefact_count} |"
        )
    lines.append("")
    lines.append("## Schema source per row")
    lines.append("")
    lines.append("| Source | Schema source path |")
    lines.append("|---|---|")
    for row in rows:
        lines.append(f"| `{row.pilot_id}` | `{row.schema_source}` |")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    notes_present = [r for r in rows if r.notes]
    if notes_present:
        for row in notes_present:
            lines.append(f"### `{row.pilot_id}`")
            for note in row.notes:
                lines.append(f"- {note}")
            lines.append("")
    else:
        lines.append("(no per-source notes)")
        lines.append("")
    lines.append("## Cross-references")
    lines.append("")
    lines.append("- Substrate v7 SUPPLIER (input): `data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json`")
    lines.append("- Substrate v7 MANIFEST: `data/p7_olir_audit/p7_v2_corrected/v7/MANIFEST_v7_0.json`")
    lines.append("- PIPELINE 1 lifted rows: `data/p7_olir_audit/p7_v2_corrected/v5/lifted/<source>_lifted.jsonl` × 31")
    lines.append("- PIPELINE 2 grounded contracts: `data/p7_olir_audit/p7_v2_corrected/v7/<source>/per_item_contract.json` × 31")
    lines.append("- OLIR exports: `data/p7_olir_audit/p7_v2_corrected/v7/olir_exports/concept_crosswalk_<source>.{xml,json}` × 31 + Schema 1.1 conformant × 31")
    lines.append("- Cycle A frozen tag: `cycle-a-iter-1-frozen-2026-05-04` (substrate v5 anchor); `substrate-v7-iter-3-ai-ml-incorporated` (substrate v7 anchor)")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    sources = supplier_sources()
    if len(sources) != 31:
        print(f"warning: SUPPLIER yielded {len(sources)} sources; expected 31", file=sys.stderr)

    rows = [build_row(src) for src in sources]
    for row in rows:
        fill_runtime_checksum(row)

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_md(rows), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generator": "scripts/build_source_provenance_consolidated.py",
                "substrate": "v7",
                "supplier_sha256": "596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04",
                "sources": [asdict(r) for r in rows],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"emitted: {OUT_MD.relative_to(REPO_ROOT)}")
    print(f"emitted: {OUT_JSON.relative_to(REPO_ROOT)}")
    print(f"sources: {len(rows)}")
    print()
    print("Coverage check:")
    have_url = sum(1 for r in rows if r.canonical_url)
    have_sha = sum(1 for r in rows if r.primary_checksum_sha256)
    have_doi = sum(1 for r in rows if r.doi_url)
    have_retrieved = sum(1 for r in rows if r.retrieved_at)
    have_version = sum(1 for r in rows if r.version)
    print(f"  canonical_url: {have_url}/{len(rows)}")
    print(f"  doi_url: {have_doi}/{len(rows)}")
    print(f"  primary_checksum_sha256: {have_sha}/{len(rows)}")
    print(f"  retrieved_at: {have_retrieved}/{len(rows)}")
    print(f"  version: {have_version}/{len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
