#!/usr/bin/env python3
"""build_paper8_bundle.py — Generate paper8 bundle JSON for publish_artifacts.json.

Cartographer 2026-05-13 — programme-lead Pedro Farinha.

Paper 8 (Pipeline Primitive Demonstration) is a multi-repo deposit. Per the
Pass 7.1 manuscript §11.5 deposit chain, three of the four artefact classes
mirror into `appsec-core-ontology-research/papers/08-pipeline-primitive-demonstration/artifacts/`
because their origin repositories are not publicly accessible:

  1. knowledge_graph runtime v1.2 (sbd-toe-knowledge-graph @ cycle-b-frozen-2026-05-12)
  2. substrate-grounding gap-analysis outputs (ExternalSourcesInventory @ cycle-b-frozen-2026-05-12)
  3. closure brief (DevelopmentGovernance @ cycle-b-frozen-2026-05-12)

The fourth artefact class (Manual prose corpus) is deposited at the public
Manual repository SbD-ToE/sbd-toe-manual at the same closure tag and is NOT
mirrored into the paper8 bundle.

The substrate v7 itself (3,861 items, 18,673 GROUNDED claims, SUPPLIER SHA
596783ed…) is deposited under paper7 (`v2.0.0-construction-p7`) and cited via
the manuscript's cross-paper reference [4]; it is not re-included here.

LAYOUT:

  papers/08-pipeline-primitive-demonstration/artifacts/
  ├── kg_v1_2/                ← KG runtime v1.2 (11 files)
  │   ├── v1_manifest.json
  │   ├── manual_rastreabilidade.jsonl       (1,105 records; §26 5-section)
  │   ├── manual_maturity_progression.jsonl  (336 records; SAMM/DSOMM/SLSA)
  │   ├── manual_threat_mitigation.jsonl     (523 records; CAPEC/CWE)
  │   ├── artifacts.json                     (57 declared / 53 actual)
  │   ├── control_objectives.json            (75)
  │   ├── mechanisms.json                    (58 declared / 51 actual)
  │   ├── practices.json                     (69 declared / 66 actual)
  │   ├── slices.json                        (10 ASC slices)
  │   ├── relations.jsonl                    (structural)
  │   └── evidence_patterns_v1_annotation.json
  ├── gap_analysis/           ← ESI Phase 1 + Phase 2/3 outputs (8 files)
  │   ├── per_entity_source_map.json         (Phase 1 input: per-entity source map)
  │   ├── coverage_manual_to_v1.json         (Phase 1: Manual → V1 direction)
  │   ├── coverage_v1_to_manual.json         (Phase 1: V1 → Manual direction)
  │   ├── gap_analysis_brief.md              (Phase 1 narrative)
  │   ├── gap_taxonomy_summary.json          (initial 38-entry taxonomy)
  │   └── phase2_3/
  │       ├── phase2_3_brief.md
  │       ├── phase2_3_per_entity_classification.json
  │       └── phase2_3_refined_taxonomy.json (31 Sem / 6 Partial / 1 Gap closure mechanism breakdown)
  ├── closure_brief/          ← DevGov consolidated brief (1 file)
  │   └── cycle-b-frozen-state-consolidated.md
  └── scripts/                ← reproducibility (1 file)
      └── build_paper8_bundle.py             (this script — self-reference)

Authority: programme-lead Pedro Farinha 2026-05-13. Decisions ratified for
this paper8 bundle:
  - exclude Manual prose (manuscript §11.5 places Manual at public Manual repo)
  - cross-cite paper7 for substrate v7 (manuscript §11.2 Stage 3)
  - register new source_root `development_governance` for cycle-b closure brief

Verification model: each entry's source path is verified to exist at
`cycle-b-frozen-2026-05-12` in its origin repository via `git ls-tree`. The
script aborts (non-zero exit) if any expected file is absent at the tag.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _esi_main_checkout() -> Path:
    """Return ESI main checkout dir (works from worktree or main; via git-common-dir)."""
    common = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        capture_output=True, text=True, cwd=REPO_ROOT, check=True,
    ).stdout.strip()
    return (REPO_ROOT / common).resolve().parent


ESI_MAIN = _esi_main_checkout()
WORKSPACE_ROOT = ESI_MAIN.parent
CLOSURE_TAG = "cycle-b-frozen-2026-05-12"

DEST_PREFIX = "papers/08-pipeline-primitive-demonstration/artifacts"
OUTPUT_PATH = REPO_ROOT / "data" / "p8_publish_bundle" / "paper8_bundle.json"

REPO_KEYS = {
    "knowledge_graph": WORKSPACE_ROOT / "sbd-toe-knowledge-graph",
    "external_sources_inventory": ESI_MAIN,
    "development_governance": WORKSPACE_ROOT / "DevelopmentGovernance",
}

# Self-reference: this script is new in the paper8 branch, not yet in the
# cycle-b-frozen tag. Skip verify-at-tag for these paths; resolution at
# sync_artifacts time happens against whichever tag Curator checks out
# (expected to be the paper8 construction tag once authorised).
SELF_REFERENCED = {
    ("external_sources_inventory", "scripts/build_paper8_bundle.py"),
}


@dataclass(frozen=True)
class Entry:
    source_repo: str
    source: str
    dest: str


def verify_at_tag(repo_key: str, source_path: str) -> bool:
    """Return True if source_path exists in repo @ CLOSURE_TAG."""
    repo_root = REPO_KEYS[repo_key]
    result = subprocess.run(
        ["git", "-C", str(repo_root), "ls-tree", CLOSURE_TAG, "--", source_path],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() != ""


def add_entry(entries: list[Entry], absences: list[tuple[str, str]],
              repo_key: str, source: str, dest: str) -> None:
    if (repo_key, source) in SELF_REFERENCED or verify_at_tag(repo_key, source):
        entries.append(Entry(
            source_repo=repo_key,
            source=source,
            dest=f"{DEST_PREFIX}/{dest}",
        ))
    else:
        absences.append((repo_key, source))


def add_kg_runtime(entries: list[Entry], absences: list[tuple[str, str]]) -> None:
    """kg_v1_2/ — KG runtime v1.2 from sbd-toe-knowledge-graph @ cycle-b-frozen-2026-05-12.

    Per manuscript Stage 6: 1,964 linkage records (1,105 + 336 + 523) plus
    V1 entity tables + manifest + structural surfaces. Origin path
    `data/publish/runtime/v1/` is the canonical v1.2 surface.
    """
    items = [
        ("data/publish/runtime/v1/v1_manifest.json", "v1_manifest.json"),
        ("data/publish/runtime/v1/manual_rastreabilidade.jsonl",
         "manual_rastreabilidade.jsonl"),
        ("data/publish/runtime/v1/manual_maturity_progression.jsonl",
         "manual_maturity_progression.jsonl"),
        ("data/publish/runtime/v1/manual_threat_mitigation.jsonl",
         "manual_threat_mitigation.jsonl"),
        ("data/publish/runtime/v1/artifacts.json", "artifacts.json"),
        ("data/publish/runtime/v1/control_objectives.json", "control_objectives.json"),
        ("data/publish/runtime/v1/mechanisms.json", "mechanisms.json"),
        ("data/publish/runtime/v1/practices.json", "practices.json"),
        ("data/publish/runtime/v1/slices.json", "slices.json"),
        ("data/publish/runtime/v1/relations.jsonl", "relations.jsonl"),
        ("data/publish/runtime/v1/evidence_patterns_v1_annotation.json",
         "evidence_patterns_v1_annotation.json"),
    ]
    for source, dest in items:
        add_entry(entries, absences, "knowledge_graph", source, f"kg_v1_2/{dest}")


def add_gap_analysis(entries: list[Entry], absences: list[tuple[str, str]]) -> None:
    """gap_analysis/ — Cartographer Phase 1 + Phase 2/3 outputs from ESI."""
    items = [
        ("data/p8_inputs/per_entity_source_map.json", "per_entity_source_map.json"),
        ("data/p8_gap_analysis/coverage_manual_to_v1.json",
         "coverage_manual_to_v1.json"),
        ("data/p8_gap_analysis/coverage_v1_to_manual.json",
         "coverage_v1_to_manual.json"),
        ("data/p8_gap_analysis/gap_analysis_brief.md", "gap_analysis_brief.md"),
        ("data/p8_gap_analysis/gap_taxonomy_summary.json", "gap_taxonomy_summary.json"),
        ("data/p8_gap_analysis/phase2_3/phase2_3_brief.md",
         "phase2_3/phase2_3_brief.md"),
        ("data/p8_gap_analysis/phase2_3/phase2_3_per_entity_classification.json",
         "phase2_3/phase2_3_per_entity_classification.json"),
        ("data/p8_gap_analysis/phase2_3/phase2_3_refined_taxonomy.json",
         "phase2_3/phase2_3_refined_taxonomy.json"),
    ]
    for source, dest in items:
        add_entry(entries, absences, "external_sources_inventory", source,
                  f"gap_analysis/{dest}")


def add_closure_brief(entries: list[Entry], absences: list[tuple[str, str]]) -> None:
    """closure_brief/ — DevGov consolidated brief at cycle-b-frozen."""
    add_entry(
        entries, absences, "development_governance",
        "docs/cycle-b-frozen-state-consolidated.md",
        "closure_brief/cycle-b-frozen-state-consolidated.md",
    )


def add_scripts(entries: list[Entry], absences: list[tuple[str, str]]) -> None:
    """scripts/ — bundle helper (self-reference for reproducibility)."""
    add_entry(
        entries, absences, "external_sources_inventory",
        "scripts/build_paper8_bundle.py",
        "scripts/build_paper8_bundle.py",
    )


def main() -> int:
    entries: list[Entry] = []
    absences: list[tuple[str, str]] = []

    add_kg_runtime(entries, absences)
    add_gap_analysis(entries, absences)
    add_closure_brief(entries, absences)
    add_scripts(entries, absences)

    if absences:
        print(f"ERROR: {len(absences)} expected file(s) absent at {CLOSURE_TAG}:",
              file=sys.stderr)
        for repo_key, source in absences:
            print(f"  - {repo_key}:{source}", file=sys.stderr)
        return 1

    bundle = {
        "id": "paper8",
        "description": (
            "Pipeline primitive demonstration paper (P8) — joint Manual + "
            "knowledge-graph snapshot at cycle-b-frozen-2026-05-12. Three of "
            "the four artefact classes deposited here (KG runtime v1.2 with "
            "1,964 linkage records; substrate-grounding gap-analysis outputs "
            "including per-entity source map + Phase 1 coverage + Phase 2/3 "
            "refined closure-mechanism taxonomy; DevGov closure brief). The "
            "fourth artefact class (Manual prose corpus) is deposited "
            "independently at the public Manual repository SbD-ToE/sbd-toe-manual "
            "at the same closure tag. Substrate v7 (3,861 items, 18,673 GROUNDED "
            "claims) is cited via paper7's deposit chain (v2.0.0-construction-p7) "
            "and is not re-included. Cycle B = Iteration 2 of the coverage-"
            "preserving compilation method of paper7; one instantiation of the "
            "pipeline against 31 sources, V1 ontology (10 slices, 259 typed "
            "instances), and the practitioner Manual. 38/38 detected gaps "
            "resolved via three closure mechanisms (31 Semantic + 6 Partial + 1 "
            "Gap registered for future-work surface)."
        ),
        "files": [asdict(e) for e in entries],
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(bundle, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"emitted: {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"closure tag: {CLOSURE_TAG}")
    print(f"entries: {len(entries)}")

    from collections import Counter
    by_repo = Counter(e.source_repo for e in entries)
    by_subtree = Counter(
        e.dest[len(DEST_PREFIX) + 1:].split("/", 1)[0] for e in entries
    )
    print()
    print("Entries by source_repo:")
    for repo in sorted(by_repo):
        print(f"  {repo}: {by_repo[repo]}")
    print()
    print("Entries by subtree:")
    for st in sorted(by_subtree):
        print(f"  {st}: {by_subtree[st]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
