#!/usr/bin/env python3
"""build_paper8_bundle.py — Generate paper8 bundle JSON for publish_artifacts.json.

Cartographer 2026-05-13 (initial) + 2026-05-14 (extension) — programme-lead Pedro Farinha.

Paper 8 (Pipeline Primitive Demonstration) is a multi-repo deposit. Per the
Pass 8 manuscript §11.5 deposit chain, three of the four artefact classes
mirror into `appsec-core-ontology-research/papers/08-pipeline-primitive-demonstration/artifacts/`
because their origin repositories are not publicly accessible:

  1. knowledge_graph runtime v1.2 (sbd-toe-knowledge-graph @ cycle-b-frozen-2026-05-12)
  2. substrate-grounding gap-analysis outputs (ExternalSourcesInventory @ cycle-b-frozen-2026-05-12)
  3. closure brief (DevelopmentGovernance @ cycle-b-frozen-2026-05-12)

The fourth artefact class (Manual prose corpus) is deposited at the public
Manual repository SbD-ToE/sbd-toe-manual at the same closure tag and is NOT
mirrored into the paper8 bundle. A locator artefact (`manual_freeze_ref.{json,md}`,
authored by Cartographer 2026-05-14) is included to give a paper8 reader the
canonical pointer to that independent Manual deposit.

The substrate v7 itself (3,861 items, 18,673 GROUNDED claims, SUPPLIER SHA
596783ed…) is deposited under paper7 (`v2.0.0-construction-p7`) and cited via
the manuscript's cross-paper reference [4]; it is not re-included here.

EXTENSION HISTORY:

  - 2026-05-13 (b32166b): initial 21 entries (kg_v1_2 + gap_analysis + closure_brief + scripts)
    shipped at public tag v2.0.0-construction-p8-final-draft (@49fc452, preserved immutable).
  - 2026-05-14 (14d3be6): +8 entries (6 kg_indexes + 2 manual_freeze, ESI-Cartographer-authored)
    per 2026-05-14-orchestrator-cartographer-paper8-bundle-extension-dispatch.md.
    Cartographer surfaced 5 hallucinated `data/reports/*_summary.json` paths in
    the dispatcher (none exist at KG cycle-b-frozen tag); programme-lead
    ratified Cartographer substitution (3 dispatcher-named chunks JSONL +
    3 cartographer-chosen substitutes from data/publish/indexes/).
  - 2026-05-14 (this): −2 ESI-Cartographer manual_freeze artefacts + 1 KG-Codex
    canonical manual_freeze_ref.json pinned at tag kg-v1-cycle-b-manual-ref-2026-05-14.
    Net: 29 → 28 entries. Programme-lead Pedro Farinha 2026-05-14 ratified
    KG-derivative architecture: Codex owns Manual freeze ref in KG repo at its
    own programme tag. Cartographer's prior manual_freeze_ref.{json,md} in ESI
    superseded + deleted from ESI per persona-ownership cleanup discipline.

LAYOUT:

  papers/08-pipeline-primitive-demonstration/artifacts/
  ├── kg_v1_2/                ← KG runtime v1.2 (11 files; unchanged since baseline)
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
  ├── kg_indexes/             ← NEW 2026-05-14: KG publish/indexes chunks layer (6 files)
  │   ├── canonical_chunks.jsonl             (canonical chunks index)
  │   ├── mcp_chunks.jsonl                   (MCP-facing chunks projection)
  │   ├── vector_chunks.jsonl                (vector-backend chunks projection)
  │   ├── chunk_entity_mentions.jsonl        (per-chunk entity mention records)
  │   ├── chunk_relation_hints.jsonl         (per-chunk relation hints)
  │   └── publication_manifest.json          (indexes-layer publication manifest)
  ├── manual_freeze/          ← AMENDED 2026-05-14: Codex-canonical KG-derivative (1 file)
  │   └── manual_freeze_ref.json             (Codex KG canonical; pinned at
  │                                          kg-v1-cycle-b-manual-ref-2026-05-14)
  ├── gap_analysis/           ← ESI Phase 1 + Phase 2/3 outputs (8 files; unchanged since baseline)
  │   ├── per_entity_source_map.json         (Phase 1 input: per-entity source map)
  │   ├── coverage_manual_to_v1.json         (Phase 1: Manual → V1 direction)
  │   ├── coverage_v1_to_manual.json         (Phase 1: V1 → Manual direction)
  │   ├── gap_analysis_brief.md              (Phase 1 narrative)
  │   ├── gap_taxonomy_summary.json          (initial 38-entry taxonomy)
  │   └── phase2_3/
  │       ├── phase2_3_brief.md
  │       ├── phase2_3_per_entity_classification.json
  │       └── phase2_3_refined_taxonomy.json (31 Sem / 6 Partial / 1 Gap closure mechanism breakdown)
  ├── closure_brief/          ← DevGov consolidated brief (1 file; unchanged since baseline)
  │   └── cycle-b-frozen-state-consolidated.md
  └── scripts/                ← reproducibility (1 file; updated 2026-05-14)
      └── build_paper8_bundle.py             (this script — self-reference)

Authority: programme-lead Pedro Farinha 2026-05-13 + 2026-05-14. Decisions ratified:
  - exclude Manual prose (manuscript §11.5 places Manual at public Manual repo)
  - cross-cite paper7 for substrate v7 (manuscript §11.2 Stage 3)
  - register new source_root `development_governance` for cycle-b closure brief
  - chunks belong to paper8 ("publica o KG"; ratified 2026-05-14)
  - Manual represented by commitish ref artefact — authored by Codex
    in KG repo (KG-derivative architecture; ratified 2026-05-14 amend);
    Manual prose itself stays in independent Manual repo + site channels
  - Cartographer substitution for 5 hallucinated `*_summary.json` paths
    (ratified 2026-05-14 — substitute with actual JSONL siblings in same KG layer)

Verification model: each entry's source path is verified to exist at
`cycle-b-frozen-2026-05-12` in its origin repository via `git ls-tree`. The
script aborts (non-zero exit) if any expected file is absent at the tag.
Cartographer-authored artefacts (helper script + manual freeze ref) are flagged
via SELF_REFERENCED and skip verify-at-tag (they post-date the closure tag).
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

# Per-artefact tag overrides (entries pinned at tags other than CLOSURE_TAG).
# 2026-05-14 amend: Manual freeze ref is Codex-canonical in KG repo, pinned at
# its own programme tag — not at the multi-repo cycle-b-frozen anchor.
MANUAL_FREEZE_TAG = "kg-v1-cycle-b-manual-ref-2026-05-14"

DEST_PREFIX = "papers/08-pipeline-primitive-demonstration/artifacts"
OUTPUT_PATH = REPO_ROOT / "data" / "p8_publish_bundle" / "paper8_bundle.json"

REPO_KEYS = {
    "knowledge_graph": WORKSPACE_ROOT / "sbd-toe-knowledge-graph",
    "external_sources_inventory": ESI_MAIN,
    "development_governance": WORKSPACE_ROOT / "DevelopmentGovernance",
}

# Cartographer-authored artefact post-dating the closure tag. Skip
# verify-at-tag; resolution at sync_artifacts time happens against whichever
# tag Curator checks out (expected: paper8 construction tag).
SELF_REFERENCED = {
    ("external_sources_inventory", "scripts/build_paper8_bundle.py"),
}


@dataclass(frozen=True)
class Entry:
    source_repo: str
    source: str
    dest: str


def verify_at_tag(repo_key: str, source_path: str, tag: str = CLOSURE_TAG) -> bool:
    """Return True if source_path exists in repo @ tag (default CLOSURE_TAG)."""
    repo_root = REPO_KEYS[repo_key]
    result = subprocess.run(
        ["git", "-C", str(repo_root), "ls-tree", tag, "--", source_path],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() != ""


def add_entry(entries: list[Entry], absences: list[tuple[str, str]],
              repo_key: str, source: str, dest: str,
              tag: str = CLOSURE_TAG) -> None:
    if (repo_key, source) in SELF_REFERENCED or verify_at_tag(repo_key, source, tag):
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


def add_kg_indexes(entries: list[Entry], absences: list[tuple[str, str]]) -> None:
    """kg_indexes/ — KG publish/indexes chunks layer from sbd-toe-knowledge-graph
    @ cycle-b-frozen-2026-05-12.

    2026-05-14 extension. Three dispatcher-named chunks JSONL + three
    cartographer-chosen substitutes for hallucinated `data/reports/*_summary.json`
    paths (none of which exist at the KG closure tag). Substitutes are the
    actual JSONL siblings in the same `data/publish/indexes/` layer.
    """
    items = [
        # Dispatcher-named (verified exist at cycle-b-frozen)
        ("data/publish/indexes/canonical_chunks.jsonl", "canonical_chunks.jsonl"),
        ("data/publish/indexes/mcp_chunks.jsonl", "mcp_chunks.jsonl"),
        ("data/publish/indexes/vector_chunks.jsonl", "vector_chunks.jsonl"),
        # Cartographer substitutes (ratified 2026-05-14)
        ("data/publish/indexes/chunk_entity_mentions.jsonl",
         "chunk_entity_mentions.jsonl"),
        ("data/publish/indexes/chunk_relation_hints.jsonl",
         "chunk_relation_hints.jsonl"),
        ("data/publish/indexes/publication_manifest.json",
         "publication_manifest.json"),
    ]
    for source, dest in items:
        add_entry(entries, absences, "knowledge_graph", source, f"kg_indexes/{dest}")


def add_manual_freeze(entries: list[Entry], absences: list[tuple[str, str]]) -> None:
    """manual_freeze/ — Codex-canonical locator for the fourth artefact class.

    2026-05-14 amended (canonical): the Manual freeze ref lives in the
    knowledge_graph repo at its own programme tag
    `kg-v1-cycle-b-manual-ref-2026-05-14`, NOT at the multi-repo cycle-b-frozen
    anchor. Codex owns this artefact as KG-derivative authoring (Manual
    repository identifier + tag SHAs + ontology V2 pointer + figshare DOI
    placeholder). Cartographer's prior ESI-authored manual_freeze_ref.{json,md}
    were superseded by this Codex output per programme-lead ratification
    2026-05-14 (KG-derivative architecture; Cartographer's removed from bundle
    + deleted from ESI).
    """
    add_entry(
        entries, absences, "knowledge_graph",
        "data/publish/runtime/v1/manual_freeze_ref.json",
        "manual_freeze/manual_freeze_ref.json",
        tag=MANUAL_FREEZE_TAG,
    )


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
    add_kg_indexes(entries, absences)
    add_manual_freeze(entries, absences)
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
            "the four artefact classes deposited here: (1) KG runtime v1.2 — "
            "11 entity/linkage tables (1,964 linkage records: 1,105 "
            "rastreabilidade + 336 maturity + 523 threat_mitigation) plus "
            "6 publish/indexes chunks (3 dispatcher-named JSONL + 3 cartographer-"
            "chosen substitutes in the same KG indexes layer; 2026-05-14 "
            "extension); (2) substrate-grounding gap-analysis outputs including "
            "per-entity source map + Phase 1 coverage + Phase 2/3 refined "
            "closure-mechanism taxonomy; (3) DevGov closure brief. The fourth "
            "artefact class (Manual prose corpus) is deposited independently at "
            "the public Manual repository SbD-ToE/sbd-toe-manual at the same "
            "closure tag; this bundle includes a Codex-authored KG-canonical "
            "locator artefact (`manual_freeze_ref.json` at "
            "knowledge_graph:data/publish/runtime/v1/) pointing to that "
            "independent deposit. Substrate v7 (3,861 items, 18,673 GROUNDED "
            "claims) is cited via paper7's deposit chain (v2.0.0-construction-p7) "
            "and is not re-included. Cycle B = Iteration 2 of the coverage-"
            "preserving compilation method of paper7; one instantiation of the "
            "pipeline against 31 sources, V1 ontology (10 slices, 259 typed "
            "instances), and the practitioner Manual. 38/38 detected gaps "
            "resolved via three closure mechanisms (31 Semantic + 6 Partial + 1 "
            "Gap registered for future-work surface). Manual freeze ref is "
            "Codex-canonical (KG-derivative) and pinned at "
            "kg-v1-cycle-b-manual-ref-2026-05-14, not at the multi-repo "
            "cycle-b-frozen anchor."
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
