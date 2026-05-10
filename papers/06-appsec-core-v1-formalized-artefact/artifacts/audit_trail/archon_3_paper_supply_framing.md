# Brief: what Archon supplies to the 3-paper plan

**Date:** 2026-04-17
**Authoritative source:** `/Volumes/G-DRIVE/Shared/sbd-ai-runtime/appsec-core-ontology-research-authoring/handover/HANDOVER-new-papers-scope-v2.md`

---

## Summary

Archon is the **primary artifact owner** for P1-C (ontology DSR paper). For Pα (method DSR) and P2-v2 (corpus DSR), Archon supplies the ontology as validation target and compilation anchor respectively.

---

## Per-paper supply detail

### P1-C — AppSec Core v1: A Normalization Ontology Robust to Expanded Source Pressure

**DSR cycle on the ontology artifact.**

Archon supplies:

1. **v0 frozen snapshot** — the ontology as of P1 publication (OSF WG8PV). Tagged `ontology-v0-frozen`. Immutable.
2. **v1 YAML** — the refined ontology incorporating ACR-001 → ACO-RPR-008 promotion. Working snapshot exists at `ExternalSourcesInventory/configs/appsec_core_v0_instances_working_snapshot.json`; canonical source is the YAML under `sbd-toe-ontology/ontology/`.
3. **OWL 2 / SHACL formal export** — at `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` (47.7 KB) + `03-shacl/shapes/appsec-core-v0-shapes.ttl`. To be regenerated against v1 state before P1-C staging.
4. **ACR-001 promotion rationale** — dated note under `docs/` covering: evidence thresholds met, three-analysis convergence (V1 normalization + SAMM/DSOMM stress-test + instance-level mapping 14 Apr 2026), commit reference `46792f6`, infrastructure already existing in 5 YAMLs.
5. **ACR-002 deferral rationale** — dated note covering: TMR-007 decomposition (45 items, only 1 about security-requirements governance), SAMM D-SR single-source pressure, decision to defer to v2 under same threshold.
6. **Schema invariance evidence** — 10 slices unchanged, no new entity types, no cross-slice adjuncts between v0 and v1.

### Pα — Normalizing Heterogeneous Security Sources against a Common Ontology

**DSR cycle on the mapping method.**

Archon supplies:

1. **Ontology as validation target** — the object against which the 11-test protocol is validated. Provides OWL/SHACL as the formal surface for structural validation.
2. **Schema stability under method iteration** — evidence that schema did not drift as method refined. Supports Pα's argument that refinements R1 (source-category aware cohesion) and R2 (ontological-level aware cohesion) modified the measurement, not the subject.

### P2-v2 / β — Coverage-Preserving Compilation as an Iterative Design Science Cycle

**DSR cycle on the corpus.**

Archon supplies:

1. **v1 as compilation anchor** — per-DSR-round ontology state that Cartographer uses for gap analysis against the manual.
2. **Tagged inputs per round** — `paper-p2v2-ontology-input-round-<N>-<YYYY-MM-DD>`.

---

## Coordination

- Proposed promotions: Archon drafts, programme lead authorizes.
- Tag creation: Archon proposes, programme lead authorizes (protocol §6).
- Cross-repo implications: submit to Orchestrator before executing.
- Downstream contract impact: coordinate with Codex on any schema change affecting `data/publish/` consumption.

---

## Open items (2026-04-17)

- OWL CO→Practice→Mechanism relationship triples still pending per `PROMPT-ontology-owl-emit-relations.md`
- ACR-002 Practices (ACP-TMR-009) and Mechanisms (ACM-TMR-008) missing from OWL → 11 instance violations
- Full SHACL conformance against v1 not yet confirmed
- `FREEZE-REGISTRY.md` not yet created (deadline 2026-05-15)
