# Manifest v2.0

This manifest defines the content selection for the second curated public release.

Publication rule for this manifest:

- `v2.0.0` extends the v1.0.x foundation (P1+P2+P3) with the second research wave (P6+P7+P8) plus their supporting artifact bundles
- v1.0.x papers + artifacts are carried forward unchanged at their v1.0.x state; v2.0.0 adds new paper folders and new bundle artifacts without modifying v1.0.x surfaces
- v2.0.0 is the cycle-close consolidation of the programme's first multi-cycle arc

## 1. Repository Topology

Continues the v1.0.0 decision: **one curated public repository** for the programme. v2.0.0 does not split into per-paper or per-wave repositories.

## 2. Final Public Repository Structure (v2.0.0)

```text
appsec-core-ontology-research/
  README.md
  LICENSE
  CITATION.cff                       # updated to v2.0.0 with 8 paper DOIs
  CHANGELOG.md                       # appended v2.0.0 entry
  RELEASE-NOTES-v1.0.md              # carry-over
  RELEASE-NOTES-v2.0.md              # NEW
  MANIFEST-v1.0.md                   # carry-over
  MANIFEST-v2.0.md                   # NEW (this file)
  publish_artifacts.json             # extended: paper6/7/8 bundles + development_governance source_root
  publish_docs.json                  # extended: paper6/7/8 PDF entries
  publish_arxiv.json                 # extended: paper6/7/8 arxiv entries
  scripts/                           # build helpers (sync_artifacts, create_pdf, create_arxiv_bundle, zenodo_publish)
  docs/
    RELEASE-TO-ZENODO.md             # carry-over
  papers/
    README.md
    01-appsec-core-normalized-ontology/        # carry-over v1.0.x
    02-coverage-preserving-knowledge-compilation/  # carry-over v1.0.x
    03-ontology-grounded-retrieval/            # carry-over v1.0.x
    04-empirical-evaluation/                   # frozen design mirror (v1.0.x)
    05-mcp-se-engineering/                     # frozen companion mirror (v1.0.x)
    06-appsec-core-v1-formalized-artefact/     # NEW v2.0.0
    07-method-dsr-cycle/                       # NEW v2.0.0
    08-pipeline-primitive-demonstration/       # NEW v2.0.0
```

## 3. v2.0.0 Wave Paper Set

| Paper | Title | OSF DOI | Construction tag chain |
|---|---|---|---|
| **P6** | AppSec Core v1: A Formalized Normalization Ontology for Application Security | `10.17605/OSF.IO/U9CRD` | `v2.0.0-construction-p6-final-draft` @ `d40aed5` |
| **P7** | Pressure-Testing AppSec Core: A Design Science Cycle for Bounded-Ontology Evolution Under Heterogeneous Application-Security Sources | `10.17605/OSF.IO/3E8G5` | `v2.0.0-construction-p7` @ `6a42141` → `-graph` @ `15ce6bb` → `-final-draft` @ `fab7317` |
| **P8** | Coverage-Preserving Compilation v2: A 31-Source Pipeline with Joint Manual and Knowledge-Graph Production | `10.17605/OSF.IO/TXW8P` | `v2.0.0-construction-p8-final-draft` @ `49fc452` → `-bundle-complete` @ `7b7da64` |

Each paper folder includes:

- `source/manuscript.md` — canonical paper source (Markdown)
- `source/figures/` or `source/images/` — figure assets (DOT + SVG + PDF)
- `pdf/<paper>.pdf` — preprint PDF (xelatex build)
- `arxiv/main.tex` + `arxiv/<paper>-arxiv.tar.gz` — arxiv submission bundle
- `arxiv_preview/<paper>-arxiv-preview.pdf` — arxiv preview render
- `artifacts/<subtree>/` — supporting bundle artifacts (synced from canonical source repositories via `scripts/sync_artifacts.py`)

## 4. v2.0.0 Wave Supporting Artifact Bundles

| Bundle | Files | Source repositories (cycle-close anchor) |
|---|---:|---|
| **paper6** | 106 | sbd-toe-ontology @ `cycle-a-frozen-2026-05-08` (ontology v1 OWL + SHACL apparatus + embeddings + decisions + schema + slice_contracts + governance) |
| **paper7** | 340 | sbd-toe-ontology + ExternalSourcesInventory @ `cycle-a-frozen-2026-05-08` (substrate v7 + cross-validation + OLIR exports + figures + scripts + DSR-HISTORY + Decision 0003 + LLM-assist provenance) + 5 k-way analysis entries (Phase A.5) |
| **paper8** | 28 | sbd-toe-knowledge-graph + ExternalSourcesInventory + DevelopmentGovernance @ `cycle-b-frozen-2026-05-12` (KG runtime v1.2 + chunks + gap analysis + closure brief + scripts) + Codex KG-canonical Manual freeze ref @ `kg-v1-cycle-b-manual-ref-2026-05-14` |

All bundle entries are SHA-256-pinned at the cycle-close anchor tag chain. The `publish_artifacts.json` driver resolves source paths and synchronises into the public repo via `scripts/sync_artifacts.py`.

## 5. v2.0.0 Lineage to v1.0.x

The v2.0.0 wave is positioned in continuity with v1.0.0:

- **P6** publishes the v1 formalization of the ontology introduced by **P1** (AppSec Core v0).
- **P7** evolves the compilation methodology from **P2** (Coverage-Preserving Knowledge Compilation at 5-source first-wave scale) into a design-science cycle at 31-source scale, with the cycle's method refined and the ontology pressure-tested.
- **P8** publishes the second execution of the coverage-preserving compilation method (succeeding **P2**'s first execution) at 31-source scale with joint Manual + Knowledge-Graph output as a programme-internal pipeline primitive.

Cross-citation matrix is fully resolved with OSF DOIs (no placeholders) at v2.0.0:

- P6 [4] → P7 (`3E8G5`); P6 [5] → P8 (`TXW8P`)
- P7 [4] → P6 (`U9CRD`); P7 [5] → P8 (`TXW8P`)
- P8 [4] → P6 (`U9CRD`); P8 [5] → P7 (`3E8G5`)

## 6. Excluded Scope (v2.0.0)

Same as v1.0.0 exclusion principles, applied to v2.0.0 wave:

- internal working notes from authoring sessions
- raw source captures (heterogeneous source PDFs, framework HTML)
- internal development scripts beyond `scripts/{sync_artifacts,create_pdf,create_arxiv_bundle}.py`
- temporary or contradictory drafts (Wave 1+2+3 audit deltas, Render fixes deltas — preserved in commit history, not in artefact bundles)
- environment-specific files and credentials
- the internal development repositories as wholes (ExternalSourcesInventory, sbd-toe-knowledge-graph, SbD-ToE-Manual, DevelopmentGovernance) — only the SHA-256-pinned artefact subsets at cycle-close tags are mirrored

## 7. Publication Position

This release should be understood as:

- a curated research publication surface for the v2.0.0 wave (P6+P7+P8) plus carry-over v1.0.x (P1+P2+P3)
- the cycle-close consolidation of the programme's first multi-cycle arc (Cycle A + Cycle B closed)
- not a publication of internal cycle-by-cycle development history
- not a mirror of internal development repositories
- one single curated public repository release (continues v1.0.0 topology decision)

## 8. Recommended Citation Practice

For citations involving v2.0.0 wave papers, cite:

1. The specific paper used (per-paper OSF DOI; see §3 above)
2. The versioned figshare-archived repository release DOI (assigned at v2.0.0 → v2.0.1 patch tag after figshare deposit)

Until the v2.0.0 figshare bundle DOI is assigned, cite the SbD-ToE Programme Prospectus OSF DOI (`10.17605/OSF.IO/7T849`) as the programme-level anchor + per-paper OSF DOIs for individual contributions.
