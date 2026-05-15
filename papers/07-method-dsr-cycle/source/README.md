# P7 — Method DSR Cycle (pre-release)

This directory contains the **pre-release** source manuscript for Paper 7 (Method DSR Cycle). The paper itself may undergo revisions until the `v2.0.0` final tag is assigned to the public-repo bundle.

## Stability

- `source/manuscript.md` — **pre-release** at Pass 16; subject to revision before final v2.0.0 tag
- `../artifacts/` — **STABLE** (frozen at Cycle A frozen substrate v7 state; cross-repo peer tag `cycle-a-frozen-2026-05-08`); populated by `scripts/sync_artifacts.py paper7` from canonical source repositories

## v1.0.0 lineage

P7 evolves the coverage-preserving knowledge compilation thesis from `papers/02-coverage-preserving-knowledge-compilation` (the v1.0.0 baseline; `paper2` bundle in `publish_artifacts.json`) into operational substrate validation under Design Science Research (DSR) methodology, with a 31-source corpus and a deterministic ontology-grounded normalization pipeline.

## Pre-release current state — P7 Pass 16

Cumulative integration on top of Pass 10's OLIR substantiation (31/31 PASS NIST OLIR JSON Schema 1.1): Passes 11–16 propagate the k-way null-model evidence (Pillar 4 of §8.2) + title-rename + cross-paper coherence with P6 [4] and P8 [5].

## Pre-release tag history

- **`v2.0.0-construction-p7`** @ `6a42141` (2026-05-09) — paper folder + supporting artefacts scaffolded; Pass 10 manuscript; bundle integration + `artifacts/` populated.
- **`v2.0.0-construction-p7-graph`** @ `15ce6bb` — k-way intersection + null-model baseline (Phase A.5).
- **`v2.0.0-construction-p7-final-draft`** @ `fab7317` (2026-05-10) — Pass 16 manuscript ship; title-rename propagated at `fceacdc`.

## Final v2.0.0 tag

Final `v2.0.0` is assigned when the complete bundle (P6 + P7 + optional P8) is ready for figshare archive.

## See also

- `../README.md` — paper-level overview (stability matrix, integration sequence, cross-references)
- `../../../publish_artifacts.json` — `paper7` bundle definition (340 file entries; sync_artifacts.py input)
