# Release Notes: v2.0.0

## Summary

`v2.0.0` is the second curated public release of the AppSec Core research programme. It extends the v1.0.x foundation (P1+P2+P3) with the **second research wave** — papers P6, P7, and P8 — together with their supporting artefact bundles.

This release is the cycle-close consolidation of the programme's first multi-cycle arc: Cycle A (cycle-a-frozen-2026-05-08) closed the ontology v1 formalisation work supporting P6 and P7; Cycle B (cycle-b-frozen-2026-05-12) closed the Manual + Knowledge-Graph joint state supporting P8.

This release is designed for:

- academic citation
- paper support
- reviewer inspection
- stable GitHub release archival in figshare (and optionally B2SHARE, per v1.0.x mirror pattern)

This release is a **research programme release**:

- one curated repository snapshot (continues v1.0.0 topology decision)
- one cross-cutting figshare-backed release DOI (to be assigned at deposit)
- a six-paper public surface (3 v1.0.x carry-over + 3 v2.0.0 new) plus 2 frozen design mirrors (P4 + P5)

## v2.0.0 Wave Papers

### P6 — AppSec Core v1: A Formalized Normalization Ontology for Application Security

OSF preprint DOI: `10.17605/OSF.IO/U9CRD`

Publishes the v1 formalisation of the AppSec Core ontology introduced by P1 ([AppSec Core v0](papers/01-appsec-core-normalized-ontology/), v1.0.x). v1 is delivered as an OWL 2 DL ontology populated with 259 typed instances across the same ten domain slices as v0, accompanied by a SHACL Core constraint set. Three contributions: (1) formalisation as OWL 2 DL + SHACL apparatus; (2) schema preservation under multi-source pressure (5-source first-wave → 31-source cycle-close); (3) the AppSec Core Change Request (ACR) governance protocol demonstrated by four worked decisions.

### P7 — Pressure-Testing AppSec Core: A Design Science Cycle for Bounded-Ontology Evolution Under Heterogeneous Application-Security Sources

OSF preprint DOI: `10.17605/OSF.IO/3E8G5`

Reports the design science cycle through which the AppSec normalisation pipeline was iteratively refined under expansion from five first-wave sources to a thirty-one-source corpus across three iterations. Replaces P2's keyword-first heuristic with a two-layer architecture (sentence-embedding similarity pipeline + three curation disciplines). Exercises the ACR protocol across four cases. Pressure-tests the bounded thesis by extending the corpus with AI/ML-focused sources.

### P8 — Coverage-Preserving Compilation v2: A 31-Source Pipeline with Joint Manual and Knowledge-Graph Production

OSF preprint DOI: `10.17605/OSF.IO/TXW8P`

Succeeds P2 (Coverage-Preserving Knowledge Compilation, first-wave 5 sources) at expanded 31-source scale with joint Manual + Knowledge-Graph production output. Publishes the operational pipeline composing seven stages from external-source ingest to joint closure pinning with public-deposit mirroring. Empirical demonstration at V1 scale: 38 of 38 detected gaps resolved through three closure mechanisms (37 via deterministic traceability mechanisms with no new Manual prose; 1 registered for the future-work surface).

## Included Scope (v2.0.0 additions)

### Papers (new in v2.0.0)

- `papers/06-appsec-core-v1-formalized-artefact/`
- `papers/07-method-dsr-cycle/`
- `papers/08-pipeline-primitive-demonstration/`

Each folder includes manuscript source (Markdown), figure assets, PDF preprint (xelatex), arxiv source bundle (.tar.gz) + preview PDF, and supporting `artifacts/` subtrees.

### Paper 6 artifacts

AppSec Core v1 OWL 2 DL ontology + SHACL Core apparatus (schema-derived ontology shapes + consumer-conformance shapes) + embeddings + decisions + slice contracts + schema + governance. 106 files. Cycle A frozen substrate state (cycle-a-frozen-2026-05-08).

### Paper 7 artifacts

Substrate v7 (3,861 normalised items / 18,673 GROUNDED claims) + cross-validation outputs (SSDF + SCF + CSF) + per-source coverage analyses + figures + scripts + DSR-HISTORY records + Decision 0003 (normalisation against an imposed model) + LLM-assist provenance + OLIR-compatible per-source exports (108 artefacts) + k-way intersection + null-model baseline (Phase A.5). 340 files + 5 k-way entries.

### Paper 8 artifacts

KG runtime v1.2 (1,964 Manual-to-ontology linkage records + 245 V1 entity surfaces + Manual ontology V2 YAML) spanning three sub-subtrees: `artifacts/kg_v1_2/` (11 entries; traceability + maturity + threat linkage tables + V1 entity tables + v1 manifest); `artifacts/kg_indexes/` (6 entries; chunks-layer bundle-complete extension); `artifacts/manual_freeze/` (1 entry; KG-canonical Manual freeze ref at `kg-v1-cycle-b-manual-ref-2026-05-14`). Gap-analysis outputs (Phase 1 + Phase 2/3; 8 entries). Cycle B closure brief consolidated (1 entry). Bundle helper script (1 entry). 28 files total. Cycle B frozen substrate state (cycle-b-frozen-2026-05-12).

### Repository metadata (updated)

- `CITATION.cff` — v2.0.0; 8 paper DOIs enumerated; figshare bundle DOI placeholder for back-stamp
- `MANIFEST-v2.0.md` — new
- `RELEASE-NOTES-v2.0.md` — new (this file)
- `CHANGELOG.md` — v2.0.0 entry appended
- `publish_artifacts.json` — extended: paper6 + paper7 + paper8 bundles + `development_governance` source_root
- `publish_docs.json` + `publish_arxiv.json` — extended: paper6 + paper7 + paper8 build entries
- `scripts/create_arxiv_bundle.py` — extended with `copy_source_assets()` helper + SVG-to-PDF post-processor (Fase 1 build infrastructure)

## Carry-over from v1.0.x

The following v1.0.x surfaces are carried forward unchanged at their v1.0.x state:

- `papers/01-appsec-core-normalized-ontology/` (P1)
- `papers/02-coverage-preserving-knowledge-compilation/` (P2)
- `papers/03-ontology-grounded-retrieval/` (P3)
- `papers/04-empirical-evaluation/` (P4 — frozen OSF-authoritative design mirror)
- `papers/05-mcp-se-engineering/` (P5 — frozen companion apparatus mirror)
- `MANIFEST-v1.0.md`, `RELEASE-NOTES-v1.0.md` — historical record

## Excluded Scope

This release excludes:

- internal working notes from Wave 1+2+3 audit cycles, render-fix sessions, OSF round-robin sessions (preserved in commit history)
- raw heterogeneous source captures (framework PDFs, standards HTML, supply-chain reference documents)
- internal development repositories as wholes (ExternalSourcesInventory, sbd-toe-knowledge-graph, SbD-ToE-Manual, DevelopmentGovernance) — only SHA-256-pinned artefact subsets at cycle-close tags are mirrored
- temporary or contradictory drafts
- internal handover orchestration files (`sbd-ai-runtime/handover/` — programme-internal coordination surface, not part of public release scope)
- environment-specific files, credentials, build artefacts beyond canonical PDF + arxiv outputs

## Publication Position

This release should be understood as:

- a curated research publication surface for the v2.0.0 wave (P6+P7+P8) consolidating Cycle A + Cycle B closure states
- the programme's first multi-cycle arc closed
- not a publication of internal cycle-by-cycle development history
- not a mirror of internal development repositories
- one single curated public repository release (continues v1.0.0 topology decision)

## Recommended Citation Practice

For citations involving v2.0.0 wave papers:

1. Cite the specific paper used (per-paper OSF preprint DOI; see [`MANIFEST-v2.0.md §3`](MANIFEST-v2.0.md))
2. Cite the versioned figshare-archived repository release DOI (assigned at the v2.0.1 patch tag after figshare deposit)

Until the v2.0.0 figshare bundle DOI is assigned, cite:

- The SbD-ToE Programme Prospectus OSF DOI as the programme-level anchor: `10.17605/OSF.IO/7T849`
- The per-paper OSF preprint DOIs for individual contributions (P6/P7/P8)

## Construction Tag Chain (v2.0.0 wave build trajectory)

| Tag | Commit | Milestone |
|---|---|---|
| `v2.0.0-construction-p6-final-draft` | `d40aed5` | P6 manuscript + artifacts bundle |
| `v2.0.0-construction-p7` | `6a42141` | P7 scaffold + Phase A figshare bundle (340 entries) |
| `v2.0.0-construction-p7-graph` | `15ce6bb` | P7 + Phase A.5 k-way intersection + null-model baseline |
| `v2.0.0-construction-p7-final-draft` | `fab7317` | P7 manuscript final-draft (Pass 16; post title-rename) |
| `v2.0.0-construction-p8-final-draft` | `49fc452` | P8 scaffold + Pass 8 manuscript + 21-file paper8 bundle |
| `v2.0.0-construction-p8-bundle-complete` | `7b7da64` | P8 bundle extended to 28 files (kg_indexes + Codex Manual freeze ref) |
| `v2.0.0` | (this release) | Final v2.0.0 wave consolidation |

All construction tags are immutable per Programme Preservation Protocol §3.2.
