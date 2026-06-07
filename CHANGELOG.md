# Changelog

All notable changes to this curated public research repository should be documented in this file.

The format is based on Keep a Changelog, adapted for artifact-first academic releases.

## [v2.0.4] - 2026-06-07

**First venue submission surfaced publicly — ICSME 2026 Tool Demonstration.**

### Added

- `submitted-peer-reviewed/icsme-2026/tool-demonstration/` — manuscript of the ICSME 2026 Tool Demonstration submission ("SbD-ToE MCP: Coverage-Preserving, Ontology-Grounded Retrieval for Security-by-Design Code Generation"; single-anonymous, submitted 2026-05-28), as `manuscript.pdf` + `manuscript.md` + `manuscript.tex` with SHA-256 verification in the folder README. Manuscript only — screencast and tool artefact live at OSF DOI 10.17605/OSF.IO/PGDR6; the tool has its own public repository.
- `SUBMITTED-PEER-REVIEWED.md` (root) — index of venue submissions surfaced publicly, inclusion rule, and honest accounting of what is retained (RR in review; double-anonymous cycles; JOWO pending submission).
- `FREEZE-REGISTRY.md` — first commit of the preservation registry (existed at root since 2026-04-17, never versioned; v2.0.0–v2.0.3 were cut without it — Class B discipline item, documented in the registry).

### Changed

- `CITATION.cff` — version → v2.0.4 (was still v2.0.2 through the v2.0.3 content patch), `date-released` → 2026-06-07, title updated.
- `README.md` § DOI Model — updated from the stale v1.0-only model to the full programme model: P0–P8 OSF DOIs and the v2.0.0 + v1.0.x repository archive DOIs (kept in lockstep with the authoring repository).
- `.github/CODEOWNERS` — read-only rule added for `submitted-peer-reviewed/**`.

### Notes

- Repository content of the v2.0.x papers and artefacts is untouched; this is an additive release.
- v2.0.0–v2.0.3 tags and deposits unchanged — no history rewrite (Programme Preservation Protocol).

## [v2.0.3] - 2026-06-04

First **content** patch of the v2.0 wave (v2.0.1/v2.0.2 were metadata-only DOI back-stamps of the v2.0.0 snapshot).

### Changed

- **P6 and P7 — ACR promotion-threshold correction** (per ADR 0004). The promotion bar is stated as the applied canonical threshold: **≥3 independent sources** (Tier B — new Core entities) / **≥4 + structural inadequacy** (Tier C — new slice), with **no organisational-authorities gate**. Reported evidence is promotion-time (ACR-001 = 4, ACR-002 = 5, ACR-004 = 5 independent sources; all Tier B), replacing the prior "≥5 sources / ≥3 organisational authorities" statement substantiated with cycle-close counts (27 / 21 / 8). P7 Table 4 detection criteria (B = ≥3 / C = ≥4) were already correct and are preserved. Manuscripts, PDFs, and arXiv bundles for P6 and P7 were rebuilt. KEOD paper-draft-v4 §6 is the value reference; P6, P7, and KEOD are now mutually consistent on the threshold.

### Removed

- **Research-process documents purged from the public bundles** (per ADR 0005 / programme ADR 0011 — "public = report + produced artefacts only"): 43 mappings removed from `publish_artifacts.json` and their synced files deleted — agent-coordination briefs, internal decision records, done-logs, handover notes, `AGENTS.md`, the Preservation Protocol copy, per-source pilot briefs, and a phase-close narrative. Distribution: P6 ×17, P7 ×18, P2 ×5, P8 ×3. The stale "ACR-002 deferred" bundle artefacts are resolved by removal (the ontology source already records ACR-002 as promoted to `ACO-TMR-008`). Produced artefacts (ontology, SHACL, substrate/data, embeddings, validation outputs, P7 DSR-HISTORY) are retained.

### Notes

- v2.0.0 / v2.0.1 / v2.0.2 tags and deposits are unchanged — no history rewrite (Programme Preservation Protocol).
- P8 (`10.17605/OSF.IO/TXW8P`) manuscript untouched; only its 3 process-doc bundle mappings were purged.

## [v2.0.2] - 2026-05-17

### Added

- B2SHARE archive DOI back-stamp for v2.0.0 snapshot (secondary mirror): `10.23728/b2share.p2kzz-hpk37`
- `CITATION.cff` updated:
  - version → v2.0.2
  - title bumped to "v2.0.2"
  - identifiers list extended with the new B2SHARE DOI (positioned right after figshare v2.0.0 as logical pairing — primary + secondary mirrors of the same snapshot)
  - abstract reflects both archives
  - preferred-citation note clarifies primary (figshare) + secondary (B2SHARE) split

### Publication Notes

- v2.0.2 is a metadata-only release: repository content matches v2.0.1
- B2SHARE upload via GitHub Release import was attempted but blocked by platform-side `issubclass() arg 1 must be a class` TypeError (EUDAT B2SHARE backend bug); fallback to manual `.zip` upload + manual metadata fill succeeded
- v2.0.x archival mirror set now complete (figshare primary + B2SHARE secondary; per v1.0.x precedent of v1.0.1 figshare + v1.0.2 B2SHARE)

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
