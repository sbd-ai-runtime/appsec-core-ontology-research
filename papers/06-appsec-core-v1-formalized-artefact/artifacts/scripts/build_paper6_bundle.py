#!/usr/bin/env python3
"""build_paper6_bundle.py — Generate paper6 bundle JSON for publish_artifacts.json.

Archon 2026-05-11 — programme-lead Pedro Farinha.

Pattern analogous to Cartographer's `build_paper7_bundle.py` (ESI 2026-05-09).

Layout (`papers/06-appsec-core-v1-formalized-artefact/artifacts/`):

  artifacts/
  ├── ontology/                         # canonical YAML (V1 instance population + governance)
  │   ├── instance_index.yaml
  │   ├── slice_registry.yaml
  │   ├── manual_mapping.yaml
  │   └── consolidated.yaml
  ├── schema/                           # 4-type entity schema + cross-slice vocab
  │   ├── entity_schema.yaml
  │   └── cross_slice_vocabulary.yaml
  ├── slice_contracts/<slice>/          # per-slice consolidated dir × 10
  │   ├── contract.yaml
  │   ├── draft.yaml
  │   ├── components.yaml
  │   └── mapping.yaml
  ├── evidence_patterns/                # 213-pattern supporting index
  │   ├── index.yaml
  │   └── contract.yaml
  ├── owl/                              # OWL exports
  │   ├── appsec_core_v1_bounded.ttl
  │   └── alt_formats/{owl,jsonld,nt}
  ├── shacl/                            # SHACL apparatus-v3 + validation reports
  │   ├── schema_derived_shapes.ttl
  │   ├── consumer_conformance_shapes.ttl
  │   ├── validation_bounded_summary.json
  │   ├── validation_bounded_report.md
  │   ├── validation_pyshacl_summary.json
  │   ├── validation_pyshacl_report.txt
  │   └── validation_pyshacl_results_graph.ttl
  ├── embeddings/                       # SBERT v1.1
  │   ├── augmented_text_corpus.json
  │   ├── embeddings.npz
  │   ├── manifest.json
  │   ├── augmentation_rule.yaml
  │   └── format_conventions_snippet.md
  ├── scripts/                          # reproducibility scripts
  │   ├── build_owl.py
  │   ├── build_shacl.py
  │   ├── validate_shacl.py
  │   ├── validate_pyshacl.py
  │   ├── build_label_catalog.py
  │   ├── build_inventory.py
  │   ├── source_bundle.py
  │   ├── paths.py
  │   ├── yaml_utils.py
  │   ├── cli.py
  │   ├── formalize_appsec_core.py      # top-level wrapper
  │   ├── consumer_conformance_validator.py
  │   ├── build_embeddings.py           # embeddings build (formal/appsec_core/08-embeddings/build-script.py)
  │   └── build_paper6_bundle.py        # this script (self-reference for reproducibility)
  ├── decisions/                        # ACR + architecture decision records
  │   ├── 0001_consumer_conformance_shapes_option_c.md
  │   ├── acr_001_repository_coverage.md     # legacy handover
  │   ├── acr_002_security_requirements_lifecycle.md  # legacy handover
  │   ├── acr_004_output_rendering_brief.md       # Phase 1 brief
  │   ├── acr_004_output_rendering_execution_close.md
  │   └── acr_004_shapes_regression_remediation.md
  ├── audit_trail/                      # validation + audit history
  │   ├── v0_to_v1_attribution_audit.md (P7 Pass 6 brief)
  │   ├── figshare_ontology_inventory.md
  │   ├── ontology_validation_phase_a.md (Phase A brief)
  │   ├── ontology_validation_phase_c_close.md
  │   └── ontology_validation_phase_d_close.md
  └── governance/                       # cumulative narrative + protocol
      ├── CHANGELOG.md (v1.0 cumulative)
      ├── FREEZE-REGISTRY.md
      ├── AGENTS.md (Archon persona)
      ├── PROGRAMME-PRESERVATION-PROTOCOL.md
      ├── LICENSE
      └── README.md

Authority: programme-lead Pedro Farinha 2026-05-11 ratified P6 sync to public
repo + paper6 bundle spec emission. Internal canonical anchor:
sbd-toe-ontology @ ontology-v1.1-fair-baseline (commit 84fe8bf;
tag object 82059122d5ed94b794f6871e72016abf9519e247).
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_REPO = "sbd_toe_ontology"
DEST_PREFIX = "papers/06-appsec-core-v1-formalized-artefact/artifacts"

ONTOLOGY_DIR = REPO_ROOT / "ontology"
FORMAL_DIR = REPO_ROOT / "formal" / "appsec_core"
OWL_EXPORTS = FORMAL_DIR / "02-owl" / "exports"
OWL_ALT_FORMATS = OWL_EXPORTS / "alt-formats"
SHACL_SHAPES = FORMAL_DIR / "03-shacl" / "shapes"
VALIDATION_REPORTS = FORMAL_DIR / "05-validation" / "reports"
EMBEDDINGS_DIR = FORMAL_DIR / "08-embeddings"
PYTHON_MODULE = FORMAL_DIR / "python" / "src" / "appsec_core_formalization"
SCRIPTS_DIR = REPO_ROOT / "scripts"
AGENTIC_BRIEFS = REPO_ROOT / "agentic" / "briefs"
AGENTIC_DONE = REPO_ROOT / "agentic" / "done"
AGENTIC_DECISIONS = REPO_ROOT / "agentic" / "decisions"
DOCS_HANDOVER = REPO_ROOT / "docs" / "handover"

OUTPUT_PATH = REPO_ROOT / "data" / "p6_publish_bundle" / "paper6_bundle.json"

# Slice family → canonical slice name (filename stem fragment)
SLICE_FAMILIES = [
    ("supply-chain-build-integrity", "ACO-SCBI", "ASC-01"),
    ("identity-access-session-trust", "ACO-IAT", "ASC-02"),
    ("architecture-trust-boundaries", "ACO-ATB", "ASC-03"),
    ("testing-security-validation", "ACO-TSV", "ASC-04"),
    ("threat-modeling-risk-disposition", "ACO-TMR", "ASC-05"),
    ("secrets-protected-config", "ACO-SPC", "ASC-06"),
    ("input-validation-safe-failure", "ACO-IVF", "ASC-07"),
    ("integration-trust-service-security", "ACO-ITS", "ASC-08"),
    ("release-promotion-controlled-rollout", "ACO-RPR", "ASC-09"),
    ("security-event-logging-audit-trail", "ACO-SLG", "ASC-10"),
]


@dataclass(frozen=True)
class Entry:
    source_repo: str
    source: str
    dest: str


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


def add_canonical_ontology(entries: list[Entry], absences: dict) -> None:
    """ontology/ — canonical YAML (V1 instance population + manual mapping)."""
    items = [
        (ONTOLOGY_DIR / "appsec-core-v0-instance-index.yaml", "ontology/instance_index.yaml"),
        (ONTOLOGY_DIR / "appsec-core-slice-registry-v0-draft.yaml", "ontology/slice_registry.yaml"),
        (ONTOLOGY_DIR / "appsec-core-manual-mapping-v0-draft.yaml", "ontology/manual_mapping.yaml"),
        (ONTOLOGY_DIR / "appsec-core-v0-consolidated.yaml", "ontology/consolidated.yaml"),
        (ONTOLOGY_DIR / "appsec-core-v0-surface-contract.yaml", "ontology/surface_contract.yaml"),
    ]
    for src, dest in items:
        if not add_entry(entries, src, dest):
            absences.setdefault("ontology_missing", []).append(dest)


def add_schema(entries: list[Entry], absences: dict) -> None:
    """schema/ — 4-type entity schema + cross-slice vocabulary."""
    items = [
        (ONTOLOGY_DIR / "appsec-core-entity-schema-v0-draft.yaml", "schema/entity_schema.yaml"),
        (ONTOLOGY_DIR / "appsec-core-cross-slice-vocabulary-v0-draft.yaml", "schema/cross_slice_vocabulary.yaml"),
    ]
    for src, dest in items:
        if not add_entry(entries, src, dest):
            absences.setdefault("schema_missing", []).append(dest)


def add_slice_contracts(entries: list[Entry], absences: dict) -> None:
    """slice_contracts/<slice>/ — per-slice contract + draft + components + mapping (× 10)."""
    for slice_stem, _family, _ascn in SLICE_FAMILIES:
        per_slice_dest = f"slice_contracts/{slice_stem}"
        items = [
            (ONTOLOGY_DIR / f"appsec-core-{slice_stem}-slice-contract.yaml", f"{per_slice_dest}/contract.yaml"),
            (ONTOLOGY_DIR / f"appsec-core-{slice_stem}-draft.yaml", f"{per_slice_dest}/draft.yaml"),
            (ONTOLOGY_DIR / f"appsec-core-{slice_stem}-components-draft.yaml", f"{per_slice_dest}/components.yaml"),
            (ONTOLOGY_DIR / f"appsec-core-{slice_stem}-mapping-draft.yaml", f"{per_slice_dest}/mapping.yaml"),
        ]
        for src, dest in items:
            if not add_entry(entries, src, dest):
                absences.setdefault("slice_contracts_missing", []).append(dest)


def add_evidence_patterns(entries: list[Entry], absences: dict) -> None:
    """evidence_patterns/ — V0 supporting index of 213 evidence patterns + contract."""
    items = [
        (ONTOLOGY_DIR / "appsec-core-evidence-pattern-index-v0.yaml", "evidence_patterns/index.yaml"),
        (ONTOLOGY_DIR / "appsec-core-evidence-pattern-v0-draft.yaml", "evidence_patterns/contract.yaml"),
    ]
    for src, dest in items:
        if not add_entry(entries, src, dest):
            absences.setdefault("evidence_patterns_missing", []).append(dest)


def add_owl(entries: list[Entry], absences: dict) -> None:
    """owl/ — canonical TTL + alt-formats (iterdir for forward-compat)."""
    canonical = OWL_EXPORTS / "appsec-core-v0-bounded-v1.ttl"
    if not add_entry(entries, canonical, "owl/appsec_core_v1_bounded.ttl"):
        absences.setdefault("owl_missing", []).append("owl/appsec_core_v1_bounded.ttl")

    # alt-formats via iterdir (forward-compat for new format additions)
    if OWL_ALT_FORMATS.exists():
        for path in sorted(OWL_ALT_FORMATS.iterdir()):
            if path.is_file() and path.suffix in (".owl", ".jsonld", ".nt", ".rdf"):
                add_entry(entries, path, f"owl/alt_formats/{path.name}")
    else:
        absences.setdefault("owl_alt_formats_missing_dir", []).append(repo_relative(OWL_ALT_FORMATS))


def add_shacl(entries: list[Entry], absences: dict) -> None:
    """shacl/ — apparatus-v3 composition (Decision 0001 Option C) + validation reports."""
    items = [
        (SHACL_SHAPES / "appsec-core-v0-shapes.ttl", "shacl/schema_derived_shapes.ttl"),
        (SHACL_SHAPES / "consumer-conformance-shapes.ttl", "shacl/consumer_conformance_shapes.ttl"),
        (VALIDATION_REPORTS / "appsec-core-v0-shacl-validation-summary.json", "shacl/validation_bounded_summary.json"),
        (VALIDATION_REPORTS / "appsec-core-v0-shacl-validation-report.md", "shacl/validation_bounded_report.md"),
        (VALIDATION_REPORTS / "appsec-core-v1-pyshacl-summary.json", "shacl/validation_pyshacl_summary.json"),
        (VALIDATION_REPORTS / "appsec-core-v1-pyshacl-report.txt", "shacl/validation_pyshacl_report.txt"),
        (VALIDATION_REPORTS / "appsec-core-v1-pyshacl-results-graph.ttl", "shacl/validation_pyshacl_results_graph.ttl"),
        # apparatus-v2 bucket reports (historical evidence per FREEZE-REGISTRY)
        (VALIDATION_REPORTS / "appsec-core-v1-pyshacl-v2-bucket-a-summary.json", "shacl/v2_bucket_a_summary.json"),
        (VALIDATION_REPORTS / "appsec-core-v1-pyshacl-v2-bucket-a-report.md", "shacl/v2_bucket_a_report.md"),
        (VALIDATION_REPORTS / "appsec-core-v1-pyshacl-v2-bucket-b-summary.json", "shacl/v2_bucket_b_summary.json"),
        (VALIDATION_REPORTS / "appsec-core-v1-pyshacl-v2-bucket-b-report.md", "shacl/v2_bucket_b_report.md"),
        (VALIDATION_REPORTS / "appsec-core-v1-pyshacl-v2-bucket-b-fixture.ttl", "shacl/v2_bucket_b_fixture.ttl"),
    ]
    for src, dest in items:
        if not add_entry(entries, src, dest):
            absences.setdefault("shacl_missing", []).append(dest)


def add_embeddings(entries: list[Entry], absences: dict) -> None:
    """embeddings/ — SBERT v1.1 release artefact (212 entities)."""
    items = [
        (EMBEDDINGS_DIR / "augmented-text-corpus.json", "embeddings/augmented_text_corpus.json"),
        (EMBEDDINGS_DIR / "embeddings-all-MiniLM-L6-v2-c9745ed1.npz", "embeddings/embeddings.npz"),
        (EMBEDDINGS_DIR / "embeddings-manifest.json", "embeddings/manifest.json"),
        (EMBEDDINGS_DIR / "augmentation-rule.yaml", "embeddings/augmentation_rule.yaml"),
        (EMBEDDINGS_DIR / "format-conventions-snippet.md", "embeddings/format_conventions_snippet.md"),
        (EMBEDDINGS_DIR / "README.md", "embeddings/README.md"),
    ]
    for src, dest in items:
        if not add_entry(entries, src, dest):
            absences.setdefault("embeddings_missing", []).append(dest)


def add_scripts(entries: list[Entry], absences: dict) -> None:
    """scripts/ — reproducibility scripts (build + validate + bundle helper self-ref)."""
    # Python formalization module (under formal/appsec_core/python/src/appsec_core_formalization/)
    if PYTHON_MODULE.exists():
        for path in sorted(PYTHON_MODULE.iterdir()):
            if path.is_file() and path.suffix == ".py":
                add_entry(entries, path, f"scripts/{path.name}")
    else:
        absences.setdefault("python_module_missing_dir", []).append(repo_relative(PYTHON_MODULE))

    # Top-level scripts (CLI wrapper + consumer validator)
    items = [
        (SCRIPTS_DIR / "formalize_appsec_core.py", "scripts/formalize_appsec_core.py"),
        (SCRIPTS_DIR / "consumer_conformance_validator.py", "scripts/consumer_conformance_validator.py"),
        (EMBEDDINGS_DIR / "build-script.py", "scripts/build_embeddings.py"),
        # Self-reference for reproducibility
        (SCRIPTS_DIR / "build_paper6_bundle.py", "scripts/build_paper6_bundle.py"),
    ]
    for src, dest in items:
        if not add_entry(entries, src, dest):
            absences.setdefault("scripts_missing", []).append(dest)


def add_decisions(entries: list[Entry], absences: dict) -> None:
    """decisions/ — architecture + ACR decision records."""
    items = [
        # Option C architectural decision
        (AGENTIC_DECISIONS / "0001-consumer-conformance-shapes-ontology-owned.md",
         "decisions/0001_consumer_conformance_shapes_option_c.md"),
        # ACR-002 promotion handover (legacy)
        (DOCS_HANDOVER / "2026-04-14-acr002-tmr008-promotion.md",
         "decisions/acr_002_security_requirements_lifecycle.md"),
        # ACR-001/v1 release coherence handover
        (DOCS_HANDOVER / "2026-04-13-v0-freeze-v1-draft.md",
         "decisions/acr_001_v0_freeze_v1_draft.md"),
        (DOCS_HANDOVER / "2026-04-15-v1.0-coherence-release.md",
         "decisions/acr_001_v1_coherence_release.md"),
        # ACR-004 brief + execution + remediation
        (AGENTIC_BRIEFS / "2026-05-05-acr004-output-rendering-slice-boundary.md",
         "decisions/acr_004_output_rendering_brief.md"),
        (AGENTIC_DONE / "2026-05-05-acr004-output-rendering-execution-close.md",
         "decisions/acr_004_execution_close.md"),
        (AGENTIC_DONE / "2026-05-05-acr004-shapes-regression-remediation.md",
         "decisions/acr_004_shapes_regression_remediation.md"),
        # README in decisions dir (if exists)
        (AGENTIC_DECISIONS / "README.md", "decisions/README.md"),
    ]
    for src, dest in items:
        if not add_entry(entries, src, dest):
            absences.setdefault("decisions_missing", []).append(dest)


def add_audit_trail(entries: list[Entry], absences: dict) -> None:
    """audit_trail/ — V0→V1 attribution + validation phase reports + inventory."""
    items = [
        # P7 Pass 6 V0→V1 audit
        (AGENTIC_BRIEFS / "2026-05-08-p7-pass-6-ontology-audit-delivery.md",
         "audit_trail/v0_to_v1_attribution_audit.md"),
        # Figshare ontology inventory
        (AGENTIC_BRIEFS / "2026-05-08-figshare-ontology-inventory.md",
         "audit_trail/figshare_ontology_inventory.md"),
        # P6 validation Phase A/C/D
        (AGENTIC_BRIEFS / "2026-05-10-p6-ontology-validation-phase-a.md",
         "audit_trail/ontology_validation_phase_a.md"),
        (AGENTIC_DONE / "2026-05-10-p6-ontology-validation-phase-c-close.md",
         "audit_trail/ontology_validation_phase_c_close.md"),
        (AGENTIC_DONE / "2026-05-10-p6-ontology-validation-phase-d-close.md",
         "audit_trail/ontology_validation_phase_d_close.md"),
        # Pre-history briefs (informational context)
        (AGENTIC_BRIEFS / "2026-04-17-archon-3-paper-supply.md",
         "audit_trail/archon_3_paper_supply_framing.md"),
    ]
    for src, dest in items:
        if not add_entry(entries, src, dest):
            absences.setdefault("audit_trail_missing", []).append(dest)


def add_governance(entries: list[Entry], absences: dict) -> None:
    """governance/ — cumulative CHANGELOG + protocol + Archon persona + LICENSE + README."""
    items = [
        (REPO_ROOT / "ontology" / "v1.0" / "CHANGELOG.md", "governance/CHANGELOG.md"),
        (REPO_ROOT / "FREEZE-REGISTRY.md", "governance/FREEZE-REGISTRY.md"),
        (REPO_ROOT / "AGENTS.md", "governance/AGENTS.md"),
        (REPO_ROOT / "PROGRAMME-PRESERVATION-PROTOCOL.md", "governance/PROGRAMME-PRESERVATION-PROTOCOL.md"),
        (REPO_ROOT / "LICENSE", "governance/LICENSE"),
        (REPO_ROOT / "README.md", "governance/README.md"),
    ]
    for src, dest in items:
        if not add_entry(entries, src, dest):
            absences.setdefault("governance_missing", []).append(dest)


def main() -> int:
    entries: list[Entry] = []
    absences: dict[str, list[str]] = {}

    add_canonical_ontology(entries, absences)
    add_schema(entries, absences)
    add_slice_contracts(entries, absences)
    add_evidence_patterns(entries, absences)
    add_owl(entries, absences)
    add_shacl(entries, absences)
    add_embeddings(entries, absences)
    add_scripts(entries, absences)
    add_decisions(entries, absences)
    add_audit_trail(entries, absences)
    add_governance(entries, absences)

    bundle = {
        "id": "paper6",
        "description": (
            "AppSec Core V1: A Formalized Normalization Ontology paper (P6) — "
            "v1.1-fair-baseline canonical artefactos for figshare deposit + arXiv "
            "companion bundle. Includes V1 canonical YAML (instance index + slice "
            "registry + manual mapping + consolidated + surface contract); 4-type "
            "entity schema + cross-slice vocabulary; 10 slice contracts + 30 "
            "per-slice drafts/components/mappings; V0 supporting 213 evidence "
            "pattern index; OWL TTL canonical + 3 alt-format exports (RDF/XML, "
            "JSON-LD, N-Triples); SHACL apparatus-v3 composition (6 schema-derived "
            "+ 5 consumer-conformance shapes per Decision 0001 Option C) + 2 "
            "validation summary reports; SBERT v1.1 embeddings release artefact "
            "(212 entities × 384 dim L2-normalized, model "
            "sentence-transformers/all-MiniLM-L6-v2 @ c9745ed1); 14 reproducibility "
            "scripts (OWL/SHACL builders + validators + CLI + bundle helper); "
            "architecture decision record (Option C apparatus composition) + ACR "
            "decision records (ACR-001/002/004); audit trail (V0→V1 attribution + "
            "figshare inventory + P6 validation Phase A/C/D briefs); governance "
            "(CHANGELOG + FREEZE-REGISTRY + AGENTS persona + Programme Preservation "
            "Protocol + LICENSE + README). "
            "Internal canonical anchor: sbd-toe-ontology @ "
            "ontology-v1.1-fair-baseline (commit 84fe8bf; tag object "
            "82059122d5ed94b794f6871e72016abf9519e247). "
            "Validation outcomes: bounded SHACL + pyshacl 0.31.0 both conforms=True "
            "/ 0 violations across 6 shapes (CO 75 / P 69 / M 58 / A 57 / Slice 10 "
            "/ EP 0); OOPS! 0 Critical / 0 Important / 2 Minor (P04 + P22 design "
            "choices documented); FOOPS!-equivalent 13/15 binary (PURL1 deferred "
            "Cycle B; OM3 DOI deferred to figshare deposit). Cumulative entity "
            "counts: 75 CO + 69 P + 58 M + 57 A = 259 typed instances across 10 "
            "AppSec methodological slices."
        ),
        "files": [asdict(e) for e in entries],
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(bundle, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"emitted: {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"entries: {len(entries)}")

    # Per-subtree breakdown
    subtrees: Counter = Counter()
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
