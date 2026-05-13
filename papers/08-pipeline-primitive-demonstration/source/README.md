# P8 — Pipeline Primitive Demonstration (pre-release)

This directory contains the **pre-release** source manuscript for Paper 8 (Demonstrating an Ontology-Grounded Pipeline as Programme Primitive: Joint Manual and Knowledge-Graph Production for Security-by-Design at 31-Source Scale). The paper itself may undergo revisions until the `v2.0.0` final tag is assigned to the public-repo bundle.

## Stability

- `source/manuscript.md` — **pre-release**; current state is Pass 8 (Phase 3 review absorption complete; 13,287 words; 20 references). Subject to revision before final v2.0.0 tag.
- `../artifacts/` — **STABLE** (frozen at Cycle B closure state; cross-repo closure ledger anchor `cycle-b-frozen-2026-05-12`); populated by `scripts/sync_artifacts.py paper8` from canonical source repositories.

## Lineage

P8 is built on the upstream artefacts of P7 (Method DSR Cycle — the two-stage normalization pipeline and the design-science method; `papers/07-method-dsr-cycle`; referenced as [4] in this manuscript) and P6 (AppSec Core V1 ontology + SHACL apparatus + embeddings v1.1; `papers/06-appsec-core-v1-formalized-artefact`; referenced as [3]). The cycle reported is Cycle B (`cycle-b-frozen-2026-05-12`); Cycle A (`cycle-a-frozen-2026-05-08`) is the prior cycle that closed the v0→v1 ontology transition reported by P6 and P7.

## Pre-release tag history

- `v2.0.0-construction-p8-final-draft` — paper folder + supporting artefacts scaffolded; source manuscript at Pass 8 state. Lands when scaffold + Cartographer-emitted `paper8` bundle integration + programme-lead Session sync execution complete.

## Final v2.0.0 tag

Final `v2.0.0` is assigned when the complete bundle (P6 + P7 + P8) is ready for figshare archive.

## See also

- `../README.md` — paper-level overview (stability matrix, public deposit framing, integration sequence, cross-references)
- `../../../publish_artifacts.json` — `paper8` bundle definition (21 file entries across three peer repositories; `sync_artifacts.py` input)
