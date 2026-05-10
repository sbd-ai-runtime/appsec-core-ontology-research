# P6 — AppSec Core v1 Formalized Artefact (pre-release)

This directory contains the **pre-release** source manuscript and supporting artefacts for Paper 6 (AppSec Core v1: A Formalized Normalization Ontology for Application Security). The paper itself may undergo revisions until the `v2.0.0` final tag is assigned to the public-repo bundle.

## Stability

| Surface | Status |
|---|---|
| `source/manuscript.md` | **Pre-release** — current state is P6 Pass 5 (Archon validation gate absorbed: §3.1 disjointness declaration; §6.1 additive OWL-level structural rigour; §10.7 NEW external-tool validation OOPS! and FOOPS!; §12 bibliography extended with Poveda-Villalón 2014 OOPS! + Garijo 2021 FOOPS!). Subject to revision before final v2.0.0 tag. |
| `artifacts/` | **TO BE POPULATED** — paper6 bundle preparation pending. When `scripts/sync_artifacts.py paper6` is invoked (post-paper6-bundle-spec integration), the directory will be populated from canonical source repository `sbd-toe-ontology` at tag `ontology-v1.1-fair-baseline` @ `84fe8bf` (FAIR-baseline refinement; OOPS! 0/0/2 + FOOPS! 13/15; bounded SHACL + pyshacl 0.31.0 composed v3 both conforms=True / 0 violations; entity counts 75 CO / 69 P / 58 M / 57 A = 259). |
| `pdf/` · `arxiv/` · `arxiv_preview/` | Empty — populated when paper finalises (PDF compile, arXiv source bundle, arXiv preview). |

## v1.0.0 lineage

P6 evolves the AppSec Core v0 ontology presented in `papers/01-appsec-core-normalized-ontology` (the v1.0.0 baseline; `paper1` bundle in `publish_artifacts.json`) into a formalized OWL 2 DL artefact with a SHACL Core constraint set. P6 publishes V1 as the cycle-close output of the design science cycle reported in P7 (`papers/07-method-dsr-cycle`); the +25 net entity-count delta (V0 234 → V1 259) decomposes by attribution to the four worked ACR governance decisions (ACR-001 / ACR-002 / ACR-004 promoted; ACR-003 not admitted under symmetric application of the four-condition threshold) plus a documented within-slice 4-Mechanism refinement.

## Companion-paper relationship

P6 (ontology artefact) and P7 (cycle methodology) are **companion papers** in the v2.0.0 wave:

- **P6** publishes V1 as the *artefact* — OWL 2 DL formalisation + SHACL apparatus + ACR protocol exercised across four worked decisions.
- **P7** publishes V1 as the *cycle output* — the three-iteration design science trajectory + multi-pillar acceptance criterion + per-source coverage map across thirty-one sources.

Each paper is readable independently; the cross-references (P6 §5 cites P7 [4] for cycle methodology; P7 §1.5 cites P6 [4] for ontology artefact) make the architecture coherent.

## Construction-stage tag history

- (To be assigned) **`v2.0.0-construction-p6-final-draft`** — paper folder + Pass 5 manuscript + Archon-emitted `paper6` bundle integration complete. Lands post-bundle scaffold + sync execution.

## Final v2.0.0 tag

Final `v2.0.0` is assigned when the complete bundle (P6 + P7 + optional P8) is ready for figshare archive. Until then, construction-stage tags `v2.0.0-construction-p<N>` anchor per-paper milestones; root-level `MANIFEST-v2.0.md` / `RELEASE-NOTES-v2.0.md` / `CHANGELOG.md` updates are deferred until the full bundle is ready (per the v1.0.0 release-discipline pattern).

## Integration sequence

The paper6 bundle is integrated into the public repo via the existing v1.0.0 publishing model:

1. **Archon** emits a deterministic `publish_artifacts.json` `paper6` bundle fragment enumerating the canonical source paths for the V1 ontology + slice contracts + OWL TTL exports + SHACL apparatus (schema-derived + consumer-conformance) + embeddings v1.1 + ACR decision records + build scripts at `sbd-toe-ontology` `ontology-v1.1-fair-baseline` @ `84fe8bf`.
2. **Curator** integrates the Archon-emitted fragment into the root `publish_artifacts.json`.
3. **Programme-lead Session** invokes `scripts/sync_artifacts.py --bundle paper6 [--source-root sbd_toe_ontology=<path>]` to populate this `artifacts/` directory from the canonical source repository.
4. **Construction-stage tag `v2.0.0-construction-p6-final-draft`** is created at the post-sync commit on this repo.

## Reproducibility anchor

The paper6 bundle is reproducible from:

- **Internal canonical commit (sbd-toe-ontology main):** `84fe8bf` (Phase D final state)
- **Internal tag:** `ontology-v1.1-fair-baseline` @ `84fe8bf` (FAIR-baseline anchor; tag object `82059122d5ed94b794f6871e72016abf9519e247`)
- **Predecessor (V1 baseline):** `ontology-v1-final` @ `b267cf3` (immutable; entity counts identical at v1.1-fair-baseline)
- **Apparatus:** `apparatus-shacl-pyshacl-v3` @ `58b1958` (shapes unchanged at v1.1-fair-baseline)
- **Embeddings:** `appsec-core-embeddings-v1.1` @ `b948356` (212 entities; unaffected by FAIR refinement)
- **Cycle A frozen evidence:** `cycle-a-frozen-2026-05-08` @ `6006e807` (programme V1 milestone roll-up)

## Cited external evaluators

- **OOPS!** — M. Poveda-Villalón, A. Gómez-Pérez, M. C. Suárez-Figueroa. *OOPS! (OntOlogy Pitfall Scanner!)*. International Journal on Semantic Web and Information Systems 10(2):7-34, 2014. — https://oops.linkeddata.es/
- **FOOPS!** — D. Garijo, O. Corcho, M. Poveda-Villalón. *FOOPS!: An ontology pitfall scanner for the FAIR principles*. ISWC 2021 Posters/Demos/Industry Tracks, CEUR-WS Vol-2980. — https://foops.linkeddata.es/

P6 §10.7 records the validation outcomes at `ontology-v1.1-fair-baseline`: OOPS! 0 Critical / 0 Important / 2 Minor (P04 + P22 documented design choices); FOOPS! 13/15 binary (87%); 5/6 OM3 sub-fields. Future-work trajectory: FOOPS! 14/15 at figshare DOI assignment; 15/15 if w3id.org persistent-IRI redirect lands in Cycle B.
