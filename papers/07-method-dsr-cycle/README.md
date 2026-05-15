# P7 — Method DSR Cycle (pre-release)

This directory contains the **pre-release** source manuscript and supporting artefacts for Paper 7 (Method DSR Cycle). The paper itself may undergo revisions until the `v2.0.0` final tag is assigned to the public-repo bundle.

## Stability

| Surface | Status |
|---|---|
| `source/manuscript.md` | **Pre-release** — current state is P7 Pass 16 (cumulative integration of Passes 11–16 on top of Pass 10's OLIR substantiation; k-way intersection + null-model baseline (Phase A.5) materially evaluated; four evidence pillars at §8.2; title-rename propagated; cross-paper coherence with P6 [4] and P8 [5]). Subject to revision before final v2.0.0 tag. |
| `artifacts/` | **STABLE** — frozen at Cycle A frozen substrate v7 state (cross-repo peer tag `cycle-a-frozen-2026-05-08`). Artefacts populated by `scripts/sync_artifacts.py paper7` from canonical source repositories (`ExternalSourcesInventory` at `cycle-a-frozen-2026-05-08`; OLIR track at `olir-conversion-cycle-a-validated`). |
| `pdf/` · `arxiv/` · `arxiv_preview/` | Empty — populated when paper finalises (PDF compile, arXiv source bundle, arXiv preview). |

## v1.0.0 lineage

P7 evolves the coverage-preserving knowledge compilation thesis from `papers/02-coverage-preserving-knowledge-compilation` (the v1.0.0 baseline; `paper2` bundle in `publish_artifacts.json`) into operational substrate validation under Design Science Research (DSR) methodology, with a 31-source corpus and a deterministic ontology-grounded normalization pipeline. The paper-level positioning of P7 as P2-evolution is a separate framing work item; the present scaffold reflects the artefact set as concluded at Cycle A close.

## Construction-stage tag history

- **`v2.0.0-construction-p7`** @ `6a42141` (2026-05-09) — paper folder + supporting artefacts scaffolded; Pass 10 manuscript; Cartographer-emitted `paper7` bundle (340 entries) integrated; `artifacts/` populated from `ExternalSourcesInventory` at `cycle-a-frozen-2026-05-08` + OLIR track at `olir-conversion-cycle-a-validated`.
- **`v2.0.0-construction-p7-graph`** @ `15ce6bb` — k-way intersection + null-model baseline (Phase A.5) milestone; Pillar 4 evidence materialised.
- **`v2.0.0-construction-p7-final-draft`** @ `fab7317` (2026-05-10) — Pass 16 manuscript ship (cumulative Passes 11–16 integration); title-rename propagated at `fceacdc`.

## Final v2.0.0 tag

Final `v2.0.0` is assigned when the complete bundle (P6 + P7 + optional P8) is ready for figshare archive. Until then, construction-stage tags `v2.0.0-construction-p<N>` anchor per-paper milestones; root-level `MANIFEST-v2.0.md` / `RELEASE-NOTES-v2.0.md` / `CHANGELOG.md` updates are deferred until the full bundle is ready (per the v1.0.0 release-discipline pattern).

## Integration sequence

The paper7 bundle is integrated into the public repo via the existing v1.0.0 publishing model:

1. **Cartographer** emits a deterministic `publish_artifacts.json` `paper7` bundle fragment enumerating the canonical source paths for substrate v7 + cross-validation + figures + OLIR exports + scripts + DSR-HISTORY + Decision 0003 + LLM-assist provenance.
2. **Curator** integrates the Cartographer-emitted fragment into the root `publish_artifacts.json`.
3. **Programme-lead** runs `scripts/sync_artifacts.py paper7` (and/or `--dry-run` for verification) to populate `artifacts/` from the canonical source repositories.
4. **Curator** mirrors integration delivery handover.

Until step 3 completes, the `artifacts/` subdirectories under this folder are empty placeholders — the canonical artefacts live at the source-repository tags listed above and are not duplicated here.

## See also

- **Manuscript-side OLIR substantiation:** `source/manuscript.md` §12 (the OLIR-compatible publication form) + §15.6 (AI Use Statement) + §13.5 (OLIR submission and external validation future work).
- **Cycle A frozen state:** the cross-repo peer tag `cycle-a-frozen-2026-05-08` anchors V1 ontology + apparatus-shacl-pyshacl-v3 + appsec-core-embeddings-v1.1 + substrate v7.
- **OLIR track closure:** the lightweight tag `olir-conversion-cycle-a-validated` (at commit `3a3b713` of `ExternalSourcesInventory` branch `cartographer-iteration-3-ai-ml-expansion`) anchors the 108-artefact OLIR-track delivery — including the NIST OLIR JSON Schema 1.1 conformant per-pilot submissions (31/31 PASS), the deterministic conversion + validator scripts, the methodology brief, and the jarsigner verification evidence.
- **Paper-series context:** see the public repo root `MANIFEST-v1.0.md` (v1.0.0 baseline papers 1–3) and the future `MANIFEST-v2.0.md` (deferred until full v2.0.0 bundle ready).
