#!/usr/bin/env python3
"""build_paper7_bundle.py — Generate paper7 bundle JSON for publish_artifacts.json.

Cartographer 2026-05-09 — programme-lead Pedro Farinha.

CLEAN PARALLEL STRUCTURE (ratified 2026-05-09):

  papers/07-method-dsr-cycle/artifacts/
  ├── sources/                          # per-source clean dirs × 31
  │   └── <source>/
  │       ├── manifest.yaml             # canonical provenance (where exists)
  │       ├── brief.md                  # narrative context (where exists)
  │       ├── indexing_contract.yaml    # indexing spec (where exists)
  │       ├── retrieval_receipt.json    # capture state (where exists)
  │       ├── quality_dossier.json      # iter-3 streamlined dossier (where exists)
  │       ├── source_object_inventory.json   # extraction state (where exists)
  │       ├── source_unit_inventory.json     # extraction state (where exists)
  │       ├── lifted.jsonl              # PIPELINE 1 output (uniform 31/31)
  │       ├── per_item_contract.json    # PIPELINE 2 grounded (uniform 31/31)
  │       ├── olir_crosswalk.xml        # OLIR XML (uniform 31/31)
  │       ├── olir_crosswalk.json       # OLIR JSON (uniform 31/31)
  │       └── olir_schema_1_1.json      # NIST OLIR Schema 1.1 conformant (uniform 31/31)
  ├── sources_archive/
  │   ├── sources_original.zip          # 76 raw source files; 29.93 MB; sha256 e222f066...
  │   └── sources_original_manifest.json
  ├── substrate/                        # corpus aggregates
  │   ├── SUPPLIER_v7_0.json
  │   ├── MANIFEST_v7_0.json
  │   ├── claims.ttl
  │   ├── shacl_report.{md,json}
  │   ├── source_provenance_consolidated.{md,json}
  │   └── ontology_side_index.json
  ├── cross_validation/                 # validation evidence
  │   ├── ssdf_crossval.json + ssdf_crossval_filtered.json
  │   ├── scf_crossval.json
  │   ├── frontier_match_and_per_task_audit.json
  │   ├── per_pair_audit.xlsx
  │   ├── ldp_cluster_analysis.json
  │   ├── calibration_distribution.json
  │   ├── per_source_metadata_table.json
  │   ├── reports/
  │   │   ├── LABDEPTHPENDING_ACR_ANALYSIS.md
  │   │   ├── H2_INVERTED_MAPPING_DECISION.md
  │   │   └── PROCESS_INTEGRITY_REPORT.md
  │   └── k_way_analysis/               # Phase A.5 dispatcher (k-way + null-model)
  │       ├── per_entity_k_way.json
  │       ├── k_way_summary.json
  │       ├── null_model_baseline.json
  │       ├── k_way_brief.md
  │       └── v5_baseline_recall.json
  ├── method/                           # methodology + decisions
  │   ├── decision_0003_main.md + decision_0003_amendment_1.md + appendix
  │   ├── dsr_history/{iter_2.md, iter_3.md, README.md}
  │   ├── llm_assist_provenance.md
  │   ├── iteration_3_evidence_package.md
  │   ├── olir_conversion_methodology.md
  │   └── figshare_substrate_inventory.md
  ├── figures/                          # paper figures (3 × 4 formats + prompts)
  │   ├── figure-1-pw8-sa11-multi-claim-alignment.{svg,dot,pdf,png}
  │   ├── figure-2-po1-sa1-strict-match-baseline.{svg,dot,pdf,png}
  │   ├── figure-3-po2-ops15-genuine-divergence.{svg,dot,pdf,png}
  │   └── prompt_specs.md
  ├── olir/                             # OLIR shared assets
  │   ├── reference_document.{xml,json}
  │   ├── self_structural_validator_report.{md,json}
  │   ├── jarsigner_verdict.md
  │   └── schema_1_1/
  │       ├── OLIR_Schema.json
  │       └── validator_report.{md,json}
  └── scripts/                          # reproducibility
      ├── grounding/{run_pipeline_v7, emit_substrate_v7_ttl, ldp_cluster_analysis_v7,
      │              encode, score, calibrate_thresholds, pydantic_schemas}.py
      ├── cross_validation/{cross_validate_ssdf_references_v7,
      │                     cross_validate_ssdf_references_v7_filtered,
      │                     cross_validate_scf_strm_v7,
      │                     frontier_match_and_audit_v7}.py
      ├── figures/generate_p7_section_8_2_figures.py
      ├── olir/{generate_olir_exports, validate_olir_jsonschema}.py
      ├── provenance/build_source_provenance_consolidated.py
      ├── sources_archive/build_sources_original_archive.py
      └── build_paper7_bundle.py

Authority: programme-lead Pedro Farinha 2026-05-09 ratified clean parallel
layout (replaces convoluted ESI mirror; consolidates per-source files).
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_REPO = "external_sources_inventory"
DEST_PREFIX = "papers/07-method-dsr-cycle/artifacts"

V7_ROOT = REPO_ROOT / "data" / "p7_olir_audit" / "p7_v2_corrected" / "v7"
V5_LIFTED = REPO_ROOT / "data" / "p7_olir_audit" / "p7_v2_corrected" / "v5" / "lifted"
SUPPLIER_PATH = V7_ROOT / "SUPPLIER_v7_0.json"
PILOTS_ROOT = REPO_ROOT / "pilots"
DATA_ROOT = REPO_ROOT / "data"
DOCS_DSR = REPO_ROOT / "docs" / "DSR-HISTORY"
BRIEFS = REPO_ROOT / "agentic" / "briefs"
DECISIONS = REPO_ROOT / "agentic" / "decisions"
REPORTS = V7_ROOT / "reports"
FIGURES = REPORTS / "figures"
OLIR_EXPORTS = V7_ROOT / "olir_exports"
OLIR_SCHEMA_V1_1 = OLIR_EXPORTS / "olir_schema_v1_1"
K_WAY_ANALYSIS = V7_ROOT / "k_way_analysis"
SOURCES_ARCHIVE_DIR = REPO_ROOT / "data" / "p7_publish_bundle"

OUTPUT_PATH = REPO_ROOT / "data" / "p7_publish_bundle" / "paper7_bundle.json"


@dataclass(frozen=True)
class Entry:
    source_repo: str
    source: str
    dest: str


def supplier_sources() -> list[str]:
    raw = json.loads(SUPPLIER_PATH.read_text(encoding="utf-8"))
    items = raw.get("items") or raw.get("contracts") or []
    sources = sorted({item.get("source") for item in items if item.get("source")})
    if not sources:
        raise ValueError("SUPPLIER yielded zero sources")
    return sources


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def add_entry(entries: list[Entry], source: Path, dest: str) -> bool:
    """Append entry if source file exists; return True if added."""
    if source.exists() and source.is_file():
        entries.append(Entry(
            source_repo=SOURCE_REPO,
            source=repo_relative(source),
            dest=f"{DEST_PREFIX}/{dest}",
        ))
        return True
    return False


def add_per_source(entries: list[Entry], sources: list[str], absences: dict) -> None:
    """sources/<source>/ — per-source consolidated dir.

    Per source, attempts to add (presence varies):
    - manifest.yaml         from pilots/<source>/source_manifest.yaml
    - brief.md              from pilots/<source>/brief.md
    - indexing_contract.yaml from pilots/<source>/indexing_contract.yaml
    - retrieval_receipt.json from data/<source>/stubs/source_retrieval_receipt.json
    - quality_dossier.json   from data/<source>/stubs/quality_dossier.json
    - source_object_inventory.json from data/<source>/stubs/source_object_inventory.json
    - source_unit_inventory.json   from data/<source>/stubs/source_unit_inventory.json
    - lifted.jsonl          from data/.../v5/lifted/<source>_lifted.jsonl  (uniform)
    - per_item_contract.json from data/.../v7/<source>/per_item_contract.json (uniform)
    - olir_crosswalk.xml     from olir_exports/concept_crosswalk_<source>.xml (uniform)
    - olir_crosswalk.json    from olir_exports/concept_crosswalk_<source>.json (uniform)
    - olir_schema_1_1.json   from olir_exports/olir_schema_v1_1/<source>_olir_v1_1.json (uniform)
    """
    for src in sources:
        per_src_dest = f"sources/{src}"

        # Manifest + narrative + indexing (legacy P2-era pilots/<source>/)
        if not add_entry(entries, PILOTS_ROOT / src / "source_manifest.yaml",
                         f"{per_src_dest}/manifest.yaml"):
            absences.setdefault("manifest_missing", []).append(src)
        add_entry(entries, PILOTS_ROOT / src / "brief.md", f"{per_src_dest}/brief.md")
        add_entry(entries, PILOTS_ROOT / src / "indexing_contract.yaml",
                  f"{per_src_dest}/indexing_contract.yaml")

        # Capture state + dossier (data/<source>/stubs/)
        add_entry(entries, DATA_ROOT / src / "stubs" / "source_retrieval_receipt.json",
                  f"{per_src_dest}/retrieval_receipt.json")
        add_entry(entries, DATA_ROOT / src / "stubs" / "quality_dossier.json",
                  f"{per_src_dest}/quality_dossier.json")
        add_entry(entries, DATA_ROOT / src / "stubs" / "source_object_inventory.json",
                  f"{per_src_dest}/source_object_inventory.json")
        add_entry(entries, DATA_ROOT / src / "stubs" / "source_unit_inventory.json",
                  f"{per_src_dest}/source_unit_inventory.json")

        # Pipeline outputs (uniform 31/31 expected)
        if not add_entry(entries, V5_LIFTED / f"{src}_lifted.jsonl",
                         f"{per_src_dest}/lifted.jsonl"):
            absences.setdefault("lifted_missing", []).append(src)
        if not add_entry(entries, V7_ROOT / src / "per_item_contract.json",
                         f"{per_src_dest}/per_item_contract.json"):
            absences.setdefault("per_item_contract_missing", []).append(src)

        # OLIR conversions (uniform 31/31 expected)
        if not add_entry(entries,
                         OLIR_EXPORTS / f"concept_crosswalk_{src}.xml",
                         f"{per_src_dest}/olir_crosswalk.xml"):
            absences.setdefault("olir_xml_missing", []).append(src)
        if not add_entry(entries,
                         OLIR_EXPORTS / f"concept_crosswalk_{src}.json",
                         f"{per_src_dest}/olir_crosswalk.json"):
            absences.setdefault("olir_json_missing", []).append(src)
        if not add_entry(entries,
                         OLIR_SCHEMA_V1_1 / f"{src}_olir_v1_1.json",
                         f"{per_src_dest}/olir_schema_1_1.json"):
            absences.setdefault("olir_schema_1_1_missing", []).append(src)


def add_sources_archive(entries: list[Entry], absences: dict) -> None:
    """sources_archive/ — original source files zip (rebuilt deterministically)."""
    add_entry(entries, SOURCES_ARCHIVE_DIR / "sources_original.zip",
              "sources_archive/sources_original.zip")
    if not add_entry(entries, SOURCES_ARCHIVE_DIR / "sources_original_manifest.json",
                     "sources_archive/sources_original_manifest.json"):
        absences.setdefault("sources_archive_manifest_missing", []).append("manifest")


def add_substrate(entries: list[Entry], absences: dict) -> None:
    """substrate/ — corpus aggregates (SUPPLIER + TTL + SHACL + provenance + ontology side)."""
    items = [
        (SUPPLIER_PATH, "substrate/SUPPLIER_v7_0.json"),
        (V7_ROOT / "MANIFEST_v7_0.json", "substrate/MANIFEST_v7_0.json"),
        (REPORTS / "v7-substrate-claims.ttl", "substrate/claims.ttl"),
        (REPORTS / "v7-substrate-claims-shacl-report.md", "substrate/shacl_report.md"),
        (REPORTS / "v7-substrate-claims-shacl-report.json", "substrate/shacl_report.json"),
        (REPORTS / "source_provenance_consolidated.md", "substrate/source_provenance_consolidated.md"),
        (REPORTS / "source_provenance_consolidated.json", "substrate/source_provenance_consolidated.json"),
        (REPORTS / "ontology_side_index.json", "substrate/ontology_side_index.json"),
    ]
    for source_path, dest in items:
        if not add_entry(entries, source_path, dest):
            absences.setdefault("substrate_missing", []).append(dest)


def add_cross_validation(entries: list[Entry], absences: dict) -> None:
    """cross_validation/ — validation evidence + reports/ + k_way_analysis/."""
    items = [
        (REPORTS / "ssdf_crossval_v7.json", "cross_validation/ssdf_crossval.json"),
        (REPORTS / "ssdf_crossval_v7_filtered.json", "cross_validation/ssdf_crossval_filtered.json"),
        (REPORTS / "scf_crossval_v7.json", "cross_validation/scf_crossval.json"),
        (REPORTS / "frontier_match_and_per_task_audit_v7.json",
         "cross_validation/frontier_match_and_per_task_audit.json"),
        (REPORTS / "cross_validation_per_pair_audit.xlsx", "cross_validation/per_pair_audit.xlsx"),
        (REPORTS / "ldp_cluster_analysis.json", "cross_validation/ldp_cluster_analysis.json"),
        (REPORTS / "calibration_distribution.json", "cross_validation/calibration_distribution.json"),
        (REPORTS / "per_source_metadata_table.json", "cross_validation/per_source_metadata_table.json"),
        (REPORTS / "LABDEPTHPENDING_ACR_ANALYSIS.md",
         "cross_validation/reports/LABDEPTHPENDING_ACR_ANALYSIS.md"),
        (REPORTS / "H2_INVERTED_MAPPING_DECISION.md",
         "cross_validation/reports/H2_INVERTED_MAPPING_DECISION.md"),
        (REPORTS / "PROCESS_INTEGRITY_REPORT.md",
         "cross_validation/reports/PROCESS_INTEGRITY_REPORT.md"),
    ]
    for source_path, dest in items:
        if not add_entry(entries, source_path, dest):
            absences.setdefault("cross_validation_missing", []).append(dest)

    # k_way_analysis/ subdir (Phase A.5 dispatcher 2026-05-09 deliverables)
    if K_WAY_ANALYSIS.exists():
        for path in sorted(K_WAY_ANALYSIS.iterdir()):
            if path.is_file():
                add_entry(entries, path, f"cross_validation/k_way_analysis/{path.name}")
    else:
        absences.setdefault("k_way_analysis_missing_dir", []).append(repo_relative(K_WAY_ANALYSIS))


def add_method(entries: list[Entry], absences: dict) -> None:
    """method/ — methodology + decisions + DSR history."""
    items = [
        (DECISIONS / "0003-normalization-algorithm-redesign-2026-05-03.md",
         "method/decision_0003_main.md"),
        (DECISIONS / "0003-normalization-algorithm-redesign-2026-05-03-amendment-1-claims-not-chains.md",
         "method/decision_0003_amendment_1.md"),
        (DECISIONS / "0003-normalization-algorithm-redesign-2026-05-03-amendment-1-appendix-thresholds.md",
         "method/decision_0003_amendment_1_appendix_thresholds.md"),
        (DOCS_DSR / "cycle-a-iter-2-substrate-v6-2026-05-05.md", "method/dsr_history/iter_2.md"),
        (DOCS_DSR / "cycle-a-iter-3-2026-05-08.md", "method/dsr_history/iter_3.md"),
        (DOCS_DSR / "README.md", "method/dsr_history/README.md"),
        (REPORTS / "llm_assist_provenance_v7_addendum.md", "method/llm_assist_provenance.md"),
        (BRIEFS / "2026-05-08-iteration-3-evidence-package.md", "method/iteration_3_evidence_package.md"),
        (BRIEFS / "2026-05-09-olir-conversion-methodology.md", "method/olir_conversion_methodology.md"),
        (BRIEFS / "2026-05-08-figshare-substrate-inventory.md", "method/figshare_substrate_inventory.md"),
    ]
    for source_path, dest in items:
        if not add_entry(entries, source_path, dest):
            absences.setdefault("method_missing", []).append(dest)


def add_figures(entries: list[Entry], absences: dict) -> None:
    """figures/ — 3 figures × 4 formats + prompt specs."""
    if not FIGURES.exists():
        absences.setdefault("figures_missing_dir", []).append(repo_relative(FIGURES))
        return
    for path in sorted(FIGURES.iterdir()):
        if path.is_file():
            # Rename "figures-p7-section-8-2-prompt-specs.md" → "prompt_specs.md"
            if path.name == "figures-p7-section-8-2-prompt-specs.md":
                dest_name = "prompt_specs.md"
            else:
                dest_name = path.name
            add_entry(entries, path, f"figures/{dest_name}")


def add_olir_shared(entries: list[Entry], absences: dict) -> None:
    """olir/ — OLIR shared assets (ref doc + self-structural validator + jarsigner + Schema 1.1 shared)."""
    items = [
        (OLIR_EXPORTS / "appsec_core_v1_reference_doc.xml", "olir/reference_document.xml"),
        (OLIR_EXPORTS / "appsec_core_v1_reference_doc.json", "olir/reference_document.json"),
        (OLIR_EXPORTS / "olir_validator_report.md", "olir/self_structural_validator_report.md"),
        (OLIR_EXPORTS / "olir_validator_report.json", "olir/self_structural_validator_report.json"),
        (OLIR_EXPORTS / "jarsigner_verdict.md", "olir/jarsigner_verdict.md"),
        (OLIR_SCHEMA_V1_1 / "OLIR_Schema.json", "olir/schema_1_1/OLIR_Schema.json"),
        (OLIR_SCHEMA_V1_1 / "olir_schema_v1_1_validator_report.md",
         "olir/schema_1_1/validator_report.md"),
        (OLIR_SCHEMA_V1_1 / "olir_schema_v1_1_validator_report.json",
         "olir/schema_1_1/validator_report.json"),
    ]
    for source_path, dest in items:
        if not add_entry(entries, source_path, dest):
            absences.setdefault("olir_shared_missing", []).append(dest)


def add_scripts(entries: list[Entry], absences: dict) -> None:
    """scripts/ — reproducibility scripts organised into clean subdirs."""
    items = [
        # grounding/ — PIPELINE 2 + LDP analysis + supporting
        (REPO_ROOT / "scripts" / "v5_normalization" / "grounding" / "run_pipeline_v7.py",
         "scripts/grounding/run_pipeline_v7.py"),
        (REPO_ROOT / "scripts" / "v5_normalization" / "grounding" / "emit_substrate_v7_ttl.py",
         "scripts/grounding/emit_substrate_v7_ttl.py"),
        (REPO_ROOT / "scripts" / "v5_normalization" / "grounding" / "ldp_cluster_analysis_v7.py",
         "scripts/grounding/ldp_cluster_analysis_v7.py"),
        (REPO_ROOT / "scripts" / "v5_normalization" / "grounding" / "encode.py",
         "scripts/grounding/encode.py"),
        (REPO_ROOT / "scripts" / "v5_normalization" / "grounding" / "score.py",
         "scripts/grounding/score.py"),
        (REPO_ROOT / "scripts" / "v5_normalization" / "grounding" / "calibrate_thresholds.py",
         "scripts/grounding/calibrate_thresholds.py"),
        (REPO_ROOT / "scripts" / "v5_normalization" / "grounding" / "pydantic_schemas.py",
         "scripts/grounding/pydantic_schemas.py"),
        # cross_validation/ — cross-val drivers
        (REPO_ROOT / "scripts" / "cross_validate_ssdf_references_v7.py",
         "scripts/cross_validation/cross_validate_ssdf_references_v7.py"),
        (REPO_ROOT / "scripts" / "cross_validate_ssdf_references_v7_filtered.py",
         "scripts/cross_validation/cross_validate_ssdf_references_v7_filtered.py"),
        (REPO_ROOT / "scripts" / "cross_validate_scf_strm_v7.py",
         "scripts/cross_validation/cross_validate_scf_strm_v7.py"),
        (REPO_ROOT / "scripts" / "frontier_match_and_audit_v7.py",
         "scripts/cross_validation/frontier_match_and_audit_v7.py"),
        (REPO_ROOT / "scripts" / "k_way_null_model.py",
         "scripts/cross_validation/k_way_null_model.py"),
        # figures/ — figure emitter
        (REPO_ROOT / "scripts" / "figures" / "generate_p7_section_8_2_figures.py",
         "scripts/figures/generate_p7_section_8_2_figures.py"),
        # olir/ — OLIR converter + validator
        (REPO_ROOT / "scripts" / "olir" / "generate_olir_exports.py",
         "scripts/olir/generate_olir_exports.py"),
        (REPO_ROOT / "scripts" / "olir" / "validate_olir_jsonschema.py",
         "scripts/olir/validate_olir_jsonschema.py"),
        # provenance/ — consolidated provenance builder
        (REPO_ROOT / "scripts" / "build_source_provenance_consolidated.py",
         "scripts/provenance/build_source_provenance_consolidated.py"),
        # sources_archive/ — zip builder
        (REPO_ROOT / "scripts" / "build_sources_original_archive.py",
         "scripts/sources_archive/build_sources_original_archive.py"),
        # bundle helper (this script — self-reference for reproducibility)
        (REPO_ROOT / "scripts" / "build_paper7_bundle.py", "scripts/build_paper7_bundle.py"),
    ]
    for source_path, dest in items:
        if not add_entry(entries, source_path, dest):
            absences.setdefault("scripts_missing", []).append(dest)


def main() -> int:
    sources = supplier_sources()
    if len(sources) != 31:
        print(f"warning: SUPPLIER yielded {len(sources)} sources; expected 31", file=sys.stderr)

    entries: list[Entry] = []
    absences: dict[str, list[str]] = {}

    add_per_source(entries, sources, absences)
    add_sources_archive(entries, absences)
    add_substrate(entries, absences)
    add_cross_validation(entries, absences)
    add_method(entries, absences)
    add_figures(entries, absences)
    add_olir_shared(entries, absences)
    add_scripts(entries, absences)

    bundle = {
        "id": "paper7",
        "description": (
            "Method DSR cycle paper (P7) — coverage-preserving thesis evolution; "
            "substrate v7 + cross-validation evidence + 101 OLIR-track artefacts + "
            "DSR-HISTORY across 31-source corpus + 3 §8.2 multi-claim alignment "
            "figures + production scripts + sources_original.zip (29.93 MB; 76 raw "
            "source files; sha256 e222f066...) + 31/31 unified provenance with sha256. "
            "Layout: clean parallel structure with per-source consolidated dirs "
            "(sources/<source>/) plus substrate/ + cross_validation/ + method/ + "
            "figures/ + olir/ + scripts/ subtrees. Lineage: P7 evolves P2 v1.0.0 "
            "thesis (papers/02-coverage-preserving-knowledge-compilation) into "
            "operational substrate validation under DSR methodology."
        ),
        "files": [asdict(e) for e in entries],
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(bundle, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"emitted: {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"sources enumerated (SUPPLIER): {len(sources)}")
    print(f"entries: {len(entries)}")

    # Per-subtree breakdown
    from collections import Counter
    subtrees = Counter()
    for e in entries:
        rel = e.dest[len(DEST_PREFIX) + 1:]
        subtree = rel.split("/", 1)[0]
        subtrees[subtree] += 1
    print()
    print("Entries by subtree:")
    for st in sorted(subtrees):
        print(f"  {st}: {subtrees[st]}")

    if absences:
        print()
        print("Absences (documented):")
        for category, items in sorted(absences.items()):
            print(f"  {category}: {len(items)}")
            for item in items[:3]:
                print(f"    - {item}")
            if len(items) > 3:
                print(f"    ... and {len(items) - 3} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
