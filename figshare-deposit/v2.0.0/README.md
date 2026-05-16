# AppSec Core Ontology Research — v2.0.0 Bundle Deposit

**Authors:** Pedro Farinha (Independent Researcher, Shiftleft) — corresponding author
**Programme:** Security-by-Design Theory of Everything (SbD-ToE)
**Programme DOI:** [10.17605/OSF.IO/7T849](https://doi.org/10.17605/OSF.IO/7T849)
**figshare DOI:** [10.6084/m9.figshare.32307669](https://doi.org/10.6084/m9.figshare.32307669) (assigned 2026-05-17; back-stamped via v2.0.1 patch tag)
**B2SHARE DOI:** *(to be assigned at deposit; back-stamped via v2.0.2 patch tag)*
**License:** CC-BY-4.0 (CITATION.cff declaration)
**Date:** 2026-05-16 (v2.0.0 final tag)
**Bundle identifier:** `v2.0.0`
**GitHub Release URL:** <https://github.com/sbd-ai-runtime/appsec-core-ontology-research/releases/tag/v2.0.0>
**GitHub Release auto-archive asset:** `appsec-core-ontology-research-v2.0.0.zip` (attached to the GitHub Release)

---

## 1. Overview

The **Security-by-Design Theory of Everything (SbD-ToE)** programme operates a Design Science Research (DSR) cycle producing a bounded application-security ontology, a comprehensive practitioner manual, and an MCP-grounded retrieval apparatus that combines both at a developer's workspace.

This deposit is the **v2.0.0 release snapshot** of the curated research repository, comprising the second research wave (P6+P7+P8) consolidating the programme's first multi-cycle arc (Cycle A frozen 2026-05-08 + Cycle B frozen 2026-05-12), plus the carry-over v1.0.x wave (P1+P2+P3+P4+P5).

This is an **incremental release** over v1.0.x: the v2.0.0 snapshot contains all v1.0.x material PLUS the new v2.0.0 wave (papers P6/P7/P8 + supporting artefact bundles + repository metadata updates). The figshare/B2SHARE deposits at v2.0.0 supersede the v1.0.x deposits in coverage but the v1.0.x deposits remain individually citable for historical reproducibility.

## 2. v2.0.0 Wave Papers (new in this release)

| Paper | Title | OSF preprint DOI |
|---|---|---|
| P6 | AppSec Core v1: A Formalized Normalization Ontology for Application Security | [10.17605/OSF.IO/U9CRD](https://doi.org/10.17605/OSF.IO/U9CRD) |
| P7 | Pressure-Testing AppSec Core: A Design Science Cycle for Bounded-Ontology Evolution Under Heterogeneous Application-Security Sources | [10.17605/OSF.IO/3E8G5](https://doi.org/10.17605/OSF.IO/3E8G5) |
| P8 | Coverage-Preserving Compilation v2: A 31-Source Pipeline with Joint Manual and Knowledge-Graph Production | [10.17605/OSF.IO/TXW8P](https://doi.org/10.17605/OSF.IO/TXW8P) |

## 3. Carry-over from v1.0.x

| Paper | Title | OSF preprint DOI |
|---|---|---|
| P1 | AppSec Core v0 — Normalized Ontology | [10.17605/OSF.IO/WG8PV](https://doi.org/10.17605/OSF.IO/WG8PV) |
| P2 | Coverage-Preserving Knowledge Compilation | [10.17605/OSF.IO/A6ZFJ](https://doi.org/10.17605/OSF.IO/A6ZFJ) |
| P3 | Ontology-Grounded Retrieval | [10.17605/OSF.IO/S3HET](https://doi.org/10.17605/OSF.IO/S3HET) |
| P4 | Empirical Evaluation — pre-registered design | [10.17605/OSF.IO/H5AJE](https://doi.org/10.17605/OSF.IO/H5AJE) |
| P5 | MCP-SE Engineering | [10.17605/OSF.IO/KH8Y7](https://doi.org/10.17605/OSF.IO/KH8Y7) |

## 4. Repository Contents (v2.0.0 snapshot)

```text
appsec-core-ontology-research/        # repository root at v2.0.0
  README.md
  LICENSE
  CITATION.cff                        # v2.0.0; 8 paper DOIs enumerated
  CHANGELOG.md                        # v2.0.0 entry appended
  MANIFEST-v1.0.md  RELEASE-NOTES-v1.0.md   # v1.0.x metadata (carry-over)
  MANIFEST-v2.0.md  RELEASE-NOTES-v2.0.md   # v2.0.0 metadata (new)
  publish_artifacts.json              # paper1-8 bundles; 4 source_roots
  publish_docs.json publish_arxiv.json
  scripts/                            # build helpers (sync, PDF, arxiv, zenodo)
  docs/RELEASE-TO-ZENODO.md
  figshare-deposit/
    cycle-a-frozen-2026-05-08/        # historical figshare bundle scaffold
    v2.0.0/                           # this deposit
  papers/
    01-appsec-core-normalized-ontology/        # P1 (carry-over)
    02-coverage-preserving-knowledge-compilation/  # P2 (carry-over)
    03-ontology-grounded-retrieval/            # P3 (carry-over)
    04-empirical-evaluation/                   # P4 design mirror (carry-over)
    05-mcp-se-engineering/                     # P5 companion mirror (carry-over)
    06-appsec-core-v1-formalized-artefact/     # P6 NEW (manuscript + 106-file artifacts bundle)
    07-method-dsr-cycle/                       # P7 NEW (manuscript + 340+5-file artifacts bundle)
    08-pipeline-primitive-demonstration/       # P8 NEW (manuscript + 28-file artifacts bundle)
```

Each new paper folder includes: `source/manuscript.md` + figures + `pdf/<paper>.pdf` + `arxiv/main.tex` + `arxiv/<paper>-arxiv.tar.gz` + `arxiv_preview/<paper>-arxiv-preview.pdf` + `artifacts/<subtrees>/`.

## 5. Reproducibility

The v2.0.0 snapshot was built deterministically from canonical source repositories at cycle-close anchor tags:

- `sbd-toe-ontology` at `cycle-a-frozen-2026-05-08` @ `6006e807`
- `ExternalSourcesInventory` at `cycle-b-frozen-2026-05-12` @ `d5da1a0`
- `sbd-toe-knowledge-graph` at `cycle-b-frozen-2026-05-12` @ `dacfaca` + `kg-v1-cycle-b-manual-ref-2026-05-14` @ `72f5aafa`
- `SbD-ToE-Manual` at `cycle-b-frozen-2026-05-12` @ `455124a1` + `v1.2.0` (Manual public release 2026-05-14)
- `DevelopmentGovernance` at `cycle-b-frozen-2026-05-12` @ `db60b1b`

PDF preprints + arxiv source bundles were built with `pandoc` + `xelatex` per `publish_docs.json` and `publish_arxiv.json` configurations using `scripts/create_pdf.py` and `scripts/create_arxiv_bundle.py`.

The Manual is published separately as an independent OSS artefact at <https://github.com/SbD-ToE/sbd-toe-manual> (CC BY-SA 4.0; registered IGAC 949/2025).

## 6. License

The repository carries a CC-BY-4.0 license per `CITATION.cff`. Per-asset licensing nuances (data licenses for substrate artefacts; Apache-2.0 for code) are inherited from source repositories where applicable; consult the `LICENSE` files in the relevant subtrees.

## 7. Citation Guidance

Cite both the specific paper used (per-paper OSF DOI) and the versioned repository release (figshare or B2SHARE DOI assigned at v2.0.1/v2.0.2 patch tag).

Until the figshare/B2SHARE bundle DOIs are assigned, cite:

- The SbD-ToE Programme Prospectus OSF DOI as programme-level anchor: `10.17605/OSF.IO/7T849`
- The per-paper OSF preprint DOIs for individual contributions

Sample BibTeX entry for the bundle (post-figshare-deposit):

```bibtex
@misc{farinha2026appseccore_v200,
  title  = {AppSec Core Ontology Research v2.0.0: Curated Research Program Release (P6+P7+P8 Wave)},
  author = {Farinha, Pedro},
  year   = 2026,
  month  = 5,
  version = {v2.0.0},
  doi    = {10.6084/m9.figshare.XXXXXX},
  url    = {https://github.com/sbd-ai-runtime/appsec-core-ontology-research/releases/tag/v2.0.0}
}
```

## 8. Construction Tag Chain (v2.0.0 wave trajectory)

| Tag | Commit | Milestone |
|---|---|---|
| `v2.0.0-construction-p6-final-draft` | `d40aed5` | P6 manuscript + 106-file artifacts bundle |
| `v2.0.0-construction-p7` | `6a42141` | P7 scaffold + 340-file artifacts bundle |
| `v2.0.0-construction-p7-graph` | `15ce6bb` | P7 + Phase A.5 k-way intersection + null-model |
| `v2.0.0-construction-p7-final-draft` | `fab7317` | P7 manuscript final-draft (Pass 16) |
| `v2.0.0-construction-p8-final-draft` | `49fc452` | P8 scaffold + Pass 8 manuscript + 21-file bundle |
| `v2.0.0-construction-p8-bundle-complete` | `7b7da64` | P8 bundle extended to 28 files (kg_indexes + Codex Manual freeze ref) |
| `v2.0.0` | `487148a` | v2.0.0 wave consolidation (this deposit) |

All construction tags are immutable per Programme Preservation Protocol §3.2.

## 9. Cross-citation Matrix (v2.0.0 wave)

| Paper cites | DOI |
|---|---|
| P6 [4] → P7 | `10.17605/OSF.IO/3E8G5` |
| P6 [5] → P8 | `10.17605/OSF.IO/TXW8P` |
| P7 [4] → P6 | `10.17605/OSF.IO/U9CRD` |
| P7 [5] → P8 | `10.17605/OSF.IO/TXW8P` |
| P8 [4] → P6 | `10.17605/OSF.IO/U9CRD` |
| P8 [5] → P7 | `10.17605/OSF.IO/3E8G5` |

Zero placeholders. Fully resolved at v2.0.0.
