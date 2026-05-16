# P8 — Coverage-Preserving Compilation v2 (pre-release)

This directory contains the **pre-release** source manuscript and supporting artefacts for Paper 8 (Coverage-Preserving Compilation v2: A 31-Source Pipeline with Joint Manual and Knowledge-Graph Production). The paper succeeds Paper 2 (Coverage-Preserving Knowledge Compilation) at 31-source scale and extends the output to joint Manual + Knowledge-Graph production. The paper itself may undergo revisions until the `v2.0.0` final tag is assigned to the public-repo bundle.

## Stability

| Surface | Status |
|---|---|
| `source/manuscript.md` | **Pre-release** — current state is P8 Pass 8 (Phase 3 review absorption complete: substantive items 1–5 + editorial 6–8 + sub-substantive items §3.2 / §6.4 / §7.2 + second-pass polish items + third-pass Stage 7 / §9 title / Table 5 visibility column + external-bibliography anchoring [13]–[21] including Reimers & Gurevych Sentence-BERT, Wilkinson FAIR principles, Noy semantic integration, Manning IR base, Cimiano ontology learning, Buckland & Gey recall-precision, Noy & Klein ontology evolution, Euzenat & Shvaiko ontology matching, Isaac & Summers SKOS Primer; Wave 1 closure adds P0 Programme Prospectus as ref [3] with cross-paper coherent renumbering [3]–[21]; 13,298 words; 21 references). Subject to revision before final v2.0.0 tag. |
| `artifacts/` | **STABLE** — frozen at Cycle B closure state (cross-repo closure ledger anchor `cycle-b-frozen-2026-05-12` + KG-canonical Manual freeze ref at `kg-v1-cycle-b-manual-ref-2026-05-14`). Artefacts populated by `scripts/sync_artifacts.py paper8` from canonical source repositories (`sbd-toe-knowledge-graph` at the cycle's closure commit `dacfaca5` plus the Manual-freeze-ref tag descendant; `ExternalSourcesInventory` at `d5da1a0`; `DevelopmentGovernance` at `db60b1b`). **28 file entries** spanning three peer repositories across 6 subtrees: `kg_v1_2/` (11) + `kg_indexes/` (6) + `manual_freeze/` (1, Codex KG-canonical) + `gap_analysis/` (8, including `phase2_3/`) + `closure_brief/` (1) + `scripts/` (1, self-referenced helper). |
| `pdf/` · `arxiv/` · `arxiv_preview/` | Empty — populated when paper finalises (PDF compile, arXiv source bundle, arXiv preview). |

## Public deposit framing (manuscript §11)

The cycle's joint Manual + knowledge-graph snapshot is the citable deliverable referenced by the paper's reproducibility chain. The snapshot encompasses four artefact classes; only one of the four origin repositories is publicly accessible.

| Artefact class | Origin repository (visibility) | Public deposit surface |
|---|---|---|
| Manual prose corpus (15 chapters, 4 document families, 322 markdown files) | `SbD-ToE/sbd-toe-manual` (PUBLIC) | `SbD-ToE/sbd-toe-manual@cycle-b-frozen-2026-05-12` (Git tag in the independently public Manual repository) |
| Knowledge graph runtime v1.2 + Manual ontology V2 (1,964 linkage records; 245 V1 entity surfaces; 529 OWL relation triples) | `SbD-ToE/sbd-toe-knowledge-graph` (INTERNAL) | This folder under `artifacts/kg_v1_2/` |
| Substrate-grounding evidence + gap-analysis outputs (per-entity source map; Phase 1 coverage; Phase 2/3 refined closure-mechanism taxonomy) | `SbD-ToE/external-sources-inventory` (PRIVATE) | This folder under `artifacts/gap_analysis/` |
| Closure brief (Cycle B frozen state consolidated) | `SbD-ToE/DevelopmentGovernance` (PRIVATE) | This folder under `artifacts/closure_brief/` |

The Manual prose corpus is the only artefact class cited at its origin repository because that origin is the only publicly accessible one; the remaining three artefact classes are deposited here under this paper's published-paper folder because their origin repositories are not publicly accessible. The closure ledger anchor `cycle-b-frozen-2026-05-12` (manuscript §9.1) is the programme-internal governance snapshot from which the public deposits are mirrored; it is not the external citation form. A cross-cutting figshare bundle DOI (analogous to the programme's precedent `cycle-a-frozen-2026-05-08`) is assigned at manuscript submission and becomes the canonical archival citation form thereafter.

## Lineage

P8 is built on the upstream artefacts of P7 (Method DSR Cycle — the two-stage normalization pipeline and the design-science method) and P6 (AppSec Core V1 ontology — the FAIR-baseline ontology and SHACL apparatus). The cycle reported in this paper is Cycle B in the programme's cycle ledger (anchored at `cycle-b-frozen-2026-05-12`); Cycle A (anchored at `cycle-a-frozen-2026-05-08`) is the prior cycle that closed the v0→v1 ontology transition reported by P6 and P7. The pipeline composes seven stages from external-source ingest through joint closure pinning with public-deposit mirroring (manuscript §3.1); 38 of 38 detected gaps are resolved through three closure mechanisms at the V1 substantive surface (manuscript §6: 31 Semantic / 6 Partial / 1 Gap registered for the future-work surface under the anti-rush content discipline).

Substrate v7 (3,861 items; 18,673 GROUNDED claims) is the cycle-close deliverable of P7 and is cross-cited via paper7's deposit chain (`v2.0.0-construction-p7`); it is not re-deposited under this paper. The V1 ontology archive at the `v1.1-fair-baseline` tag is the deliverable of P6 and is cross-cited via paper6's deposit chain; it is not re-deposited here.

## Construction-stage tag history

- **`v2.0.0-construction-p8-final-draft`** @ `49fc452` (2026-05-13) — paper folder + Pass 8 manuscript + initial 21-entry `paper8` bundle integration in root `publish_artifacts.json`; `development_governance` source_root added; first sync populated `artifacts/` from `cycle-b-frozen-2026-05-12` state across KG / ESI / DevGov.
- **`v2.0.0-construction-p8-bundle-complete`** @ `7b7da64` (2026-05-14) — bundle extension milestone: 21 → 28 file entries (+6 `kg_indexes/` chunks layer; +1 `manual_freeze/manual_freeze_ref.json` Codex KG-canonical at programme tag `kg-v1-cycle-b-manual-ref-2026-05-14`); Pass 6.2 description re-aligned to honest framing (37/38 false positives finding; manuscript §6.5).

## Final v2.0.0 tag

Final `v2.0.0` is assigned when the complete bundle (P6 + P7 + P8) is ready for figshare archive. Until then, construction-stage tags `v2.0.0-construction-p<N>` anchor per-paper milestones; root-level `MANIFEST-v2.0.md` / `RELEASE-NOTES-v2.0.md` / `CHANGELOG.md` updates are deferred until the full bundle is ready (per the v1.0.0 release-discipline pattern).

## Integration sequence

The paper8 bundle is integrated into the public repo via the existing v1.0.0 publishing model:

1. **Cartographer** emitted a deterministic `publish_artifacts.json` `paper8` bundle fragment enumerating the canonical source paths across three peer repositories. Initial (`v2.0.0-construction-p8-final-draft`): 21 entries (11 KG runtime + 9 ESI gap-analysis + 1 DevGov closure brief; helper script `build_paper8_bundle.py` self-referenced). Extension (`v2.0.0-construction-p8-bundle-complete`): 28 entries (+6 KG indexes `kg_indexes/` + 1 KG-canonical Manual freeze ref at programme tag `kg-v1-cycle-b-manual-ref-2026-05-14`).
2. **Curator** integrated both bundle revisions into the root `publish_artifacts.json` and added the `development_governance` source_root entry (the fourth `source_roots` key, alongside `knowledge_graph`, `external_sources_inventory`, and `sbd_toe_ontology`).
3. **Programme-lead** ran `scripts/sync_artifacts.py --bundle paper8 [--source-root external_sources_inventory=<worktree>]` to populate `artifacts/` from the canonical source repositories.
4. **Curator** mirrored integration delivery handovers (2026-05-13 initial + 2026-05-14 delta).

Until step 3 completes, the `artifacts/` subdirectories under this folder are empty placeholders — the canonical artefacts live at the source-repository closure commits listed in manuscript §9.1 Table 5 and are not duplicated here. The Manual prose corpus is deposited separately at the public Manual repository (see deposit-framing table above).

## See also

- **Manuscript:** `source/manuscript.md` — Pass 8 state with §3 pipeline architecture, §4 method (coverage classification + per-family reading + ontology layer separation + anti-rush content discipline), §5 cycle execution, §6 closure mechanisms, §7 three-way routing taxonomy, §8 between-execution gap-class redistribution, §9 cycle closure state and public deposits, §10 future work and limitations (including §10.7 independent-validation caveat for §26 deterministic refinement), §11 reproducibility (citation convention, pipeline-stage citation chain, build environment, OWL/SHACL validation evidence, public deposit chain Table 7).
- **Cycle B closure ledger:** the closure ledger anchor `cycle-b-frozen-2026-05-12` pins the four artefact-class closure commits documented at manuscript §9.1 Table 5; the per-artefact tag object SHAs are recorded for bit-identical verification at audit.
- **P6 lineage:** `papers/06-appsec-core-v1-formalized-artefact/` — the V1 ontology + SHACL apparatus + embeddings v1.1 release (referenced as [3] in this manuscript; construction-stage tag `v2.0.0-construction-p6-final-draft`).
- **P7 lineage:** `papers/07-method-dsr-cycle/` — the two-stage normalization pipeline + 31-source corpus + DSR-HISTORY (referenced as [4] in this manuscript; construction-stage tag `v2.0.0-construction-p7`).
- **Paper-series context:** see the public repo root `MANIFEST-v1.0.md` (v1.0.0 baseline papers 1–5) and the future `MANIFEST-v2.0.md` (deferred until full v2.0.0 bundle ready).
- **Cycle A frozen state precedent:** `figshare-deposit/cycle-a-frozen-2026-05-08/` (programme's deposit bundle precedent at the public-repo root; analogous `figshare-deposit/cycle-b-frozen-2026-05-12/` to be created at submission per manuscript §11.5).
