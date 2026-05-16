# Changelog

All notable changes to this curated public research repository should be documented in this file.

The format is based on Keep a Changelog, adapted for artifact-first academic releases.

## [v2.0.1] - 2026-05-17

### Added

- figshare archive DOI back-stamp for v2.0.0 snapshot: `10.6084/m9.figshare.32307669`
- `CITATION.cff` updated:
  - version → v2.0.1
  - identifiers list extended with the new figshare DOI as primary
  - preferred-citation DOI updated from programme-level placeholder (P0) to the assigned figshare bundle DOI
  - abstract reflects assigned DOI (previous text said "to be assigned")
- title bumped to "v2.0.1" reflecting back-stamp release per v1.0.x precedent (v1.0.0 → v1.0.1 figshare → v1.0.2 B2SHARE)

### Publication Notes

- v2.0.1 is a metadata-only release: repository content matches v2.0.0 except for the CITATION.cff DOI fields + CHANGELOG entry
- v2.0.0 figshare deposit registered as a new item (Approach A — separate DOI from v1.0.0), not as new version of `10.6084/m9.figshare.32043771` (figshare web UI restricts new-version flow to institutional accounts)
- v1.0.x predecessor DOIs preserved in `identifiers` list for historical anchor
- B2SHARE mirror for v2.0.0 pending; v2.0.2 back-stamp if pursued

## [v2.0.0] - 2026-05-16

### Added

- second research wave: P6 + P7 + P8 paper folders + supporting bundles
  - P6 (AppSec Core v1: A Formalized Normalization Ontology for Application Security) — OSF DOI `10.17605/OSF.IO/U9CRD`
  - P7 (Pressure-Testing AppSec Core: A Design Science Cycle for Bounded-Ontology Evolution Under Heterogeneous Application-Security Sources) — OSF DOI `10.17605/OSF.IO/3E8G5`
  - P8 (Coverage-Preserving Compilation v2: A 31-Source Pipeline with Joint Manual and Knowledge-Graph Production) — OSF DOI `10.17605/OSF.IO/TXW8P`
- paper6 supporting bundle: 106 files (ontology v1 OWL + SHACL apparatus + embeddings + decisions + schema + slice contracts + governance) @ `cycle-a-frozen-2026-05-08`
- paper7 supporting bundle: 340 files + 5 k-way analysis entries (substrate v7 + cross-validation + OLIR exports + figures + scripts + DSR-HISTORY + Decision 0003 + LLM-assist provenance) @ `cycle-a-frozen-2026-05-08`
- paper8 supporting bundle: 28 files (KG runtime v1.2 + chunks + gap analysis + closure brief + scripts + KG-canonical Manual freeze ref) @ `cycle-b-frozen-2026-05-12` + `kg-v1-cycle-b-manual-ref-2026-05-14`
- repository metadata updates: `CITATION.cff` (8 paper DOIs); `MANIFEST-v2.0.md`; `RELEASE-NOTES-v2.0.md`
- `publish_artifacts.json` extended: paper6/7/8 bundles + `development_governance` source_root (4 source_roots total)
- `publish_docs.json` + `publish_arxiv.json` extended: paper6/7/8 build entries
- `scripts/create_arxiv_bundle.py` extended: `copy_source_assets()` helper + SVG-to-PDF post-processor

### Programme cycle milestones

- Cycle A frozen 2026-05-08 (ontology v1 formalisation; substrate v7 first-wave) — supports P6 + P7
- Cycle B frozen 2026-05-12 (KG runtime v1.2 + Manual joint state) — supports P8
- Manual published 2026-05-14: v1.2.0 + programme-v2.0.0-aligned tags on `SbD-ToE/sbd-toe-manual` master
- Audit closure: 47/47 audit items resolved (11 BLOCKING + 22 SHOULD-FIX + 14 NICE-TO-HAVE)
- Fase 1 build complete: 3 PDF preprints + 3 arxiv source bundles + render fixes (longtables + SHA prefix discipline + Figure 1 re-author)
- Fase 2 OSF deposit complete: 3 preprint DOIs assigned + cross-citation matrix coherent (P6/P7/P8 mutual citations carry real DOIs, zero placeholders)

### Construction tag chain (v2.0.0 wave trajectory)

- `v2.0.0-construction-p6-final-draft` @ `d40aed5`
- `v2.0.0-construction-p7` @ `6a42141`
- `v2.0.0-construction-p7-graph` @ `15ce6bb`
- `v2.0.0-construction-p7-final-draft` @ `fab7317`
- `v2.0.0-construction-p8-final-draft` @ `49fc452`
- `v2.0.0-construction-p8-bundle-complete` @ `7b7da64`

All construction tags immutable per Programme Preservation Protocol §3.2.

### Publication Notes

- v2.0.0 continues the v1.0.0 single-curated-repository topology decision
- figshare archive DOI for v2.0.0 bundle is assigned at deposit; back-stamped via `v2.0.1` patch tag
- B2SHARE secondary mirror optional (per v1.0.x precedent) via `v2.0.2`
- Zenodo remains blocked at programme level (legacy orphan deposition pending cleanup)
- v1.0.x carry-over surfaces (P1+P2+P3+P4+P5) preserved unchanged
- Public-facing prose convention adopted: short SHA prefix (8-12 chars) in paper body; full SHA-256 strings in bundle manifests / CHECKSUMS / archive deliverables

### Deferred

- Zenodo bundle DOI (programme-level block; orphan deposition `19469818` pending cleanup)
- per-paper figshare mirrors (only cross-cutting v2.0.0 bundle deposit at this release)
- B2SHARE mirror deposit (optional; `v2.0.2` patch if pursued)
- OSF preprint v2 PDF updates post-arxiv submission (separate workflow)
- v3.0 wave scope (programme cycles after Cycle B)

## [v1.0.0] - 2026-04-05

### Added

- initial curated public repository structure for the AppSec Core research line
- paper slots for the current `V1` set:
  - AppSec Core ontology / normalization
  - coverage-preserving knowledge compilation
  - ontology-grounded retrieval
- ontology artifact structure for the `AppSec Core v0` surface
- curated first-wave pilot artifact structure for the current `V1` paper support set
- minimal retrieval artifact structure for contract, runtime snapshot, and optional curated examples
- repository-level metadata:
  - `README.md`
  - `LICENSE`
  - `CITATION.cff`
  - `RELEASE-NOTES-v1.0.md`
  - `MANIFEST-v1.0.md`
  - `docs/RELEASE-TO-ZENODO.md`

### Publication Notes

- this release is intended to be GitHub-release-driven and Zenodo-archived
- the public repository is a curated subset and not a publication of the internal development repositories
- the public repository is intentionally limited to the artifact surface that supports the current `V1` papers
- the recommended topology for this release is one curated public repository, not multiple public repositories

### Deferred

- paper-source files beyond the canonical public paper versions
- executable tooling beyond what is strictly needed for public reproducibility
- broad publication of internal runtime/build/test infrastructure
- richer retrieval examples if not explicitly curated before release
- later pilot waves beyond the first-wave `V1` paper set
- `SAMM`, `DSOMM`, `ACR-001`, `ACR-002`, and regulatory-wave materials
- `V2` prompt packs, delta notes, and companion-paper preparation artifacts
