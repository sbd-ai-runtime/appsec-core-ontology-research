# P6 — AppSec Core v1 Formalized Artefact (pre-release source)

This directory contains the **pre-release** source manuscript for Paper 6 (AppSec Core v1: A Formalized Normalization Ontology for Application Security). The paper itself may undergo revisions until the `v2.0.0` final tag is assigned to the public-repo bundle.

## Stability

- `source/manuscript.md` — **pre-release**; subject to revision before final v2.0.0 tag
- `../artifacts/` — **TO BE POPULATED** via `scripts/sync_artifacts.py paper6` from canonical source repository `sbd-toe-ontology` at tag `ontology-v1.1-fair-baseline` @ `84fe8bf`

## v1.0.0 lineage

P6 evolves the AppSec Core v0 ontology presented in `papers/01-appsec-core-normalized-ontology` (the v1.0.0 baseline; `paper1` bundle in `publish_artifacts.json`) into a formalized OWL 2 DL artefact with a SHACL Core constraint set. P6 publishes V1 as the cycle-close output of the design science cycle reported in P7.

## Pre-release current state — P6 Pass 5

Cumulative integration of Passes 1-5:
- Pass 1: Slice naming canonical reconciliation + Authority enumeration verbatim from substrate v7 SUPPLIER + Four-pillar acceptance reference + Relation-name canonicalisation
- Pass 2-3: Manuscript polish (light citations + bibliographic alignments)
- Pass 4: Framework absorption hypothesis + engineering vs governance split + engagement-scale vignette + conservative-extension literature relation (Grau 2008 / Konev 2009) + near-miss honest absence (§10.6) + decidable phrasing canonical reasoners (HermiT/Pellet/OpenLLET)
- **Pass 5** (current): Archon validation gate absorbed — §3.1 disjointness declaration + §6.1 additive OWL-level structural rigour + §10.7 NEW external-tool validation (OOPS! 0/0/2 + FOOPS! 13/15) + §12 bibliography Poveda-Villalón 2014 + Garijo 2021

## Reproducibility anchors (post-Pass-5)

- **Internal canonical commit (sbd-toe-ontology main):** `84fe8bf`
- **Internal tag:** `ontology-v1.1-fair-baseline` @ `84fe8bf` (tag object `82059122d5ed94b794f6871e72016abf9519e247`)
- **Predecessor (V1 baseline immutable):** `ontology-v1-final` @ `b267cf3`
- **Apparatus:** `apparatus-shacl-pyshacl-v3` @ `58b1958`
- **Embeddings:** `appsec-core-embeddings-v1.1` @ `b948356`
- **Cycle A frozen evidence:** `cycle-a-frozen-2026-05-08` @ `6006e807`

## Companion-paper relationship

P6 (ontology artefact) ↔ P7 (cycle methodology) are companion papers. P7 cites P6 as the artefact paper [4]; P6 cites P7 as the cycle paper [4] (cross-reference numbering preserved across both papers under each paper's own reference table).

## Final v2.0.0 tag

Final `v2.0.0` is assigned when the complete bundle (P6 + P7 + optional P8) is ready for figshare archive.
