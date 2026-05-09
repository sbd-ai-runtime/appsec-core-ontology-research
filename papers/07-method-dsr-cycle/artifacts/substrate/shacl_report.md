# AppSec Core V1 — Consumer Conformance Report

**Verdict:** ✅ CONFORMS
**Generated:** 2026-05-07T18:48:28.351460+00:00
**Total violations:** 0

## Inputs
- **data_graph:** `/Volumes/G-DRIVE/Shared/SecurityByDesign-TheoryOfEverything/ExternalSourcesInventory/.claude/worktrees/cartographer-iteration-3-ai-ml/data/p7_olir_audit/p7_v2_corrected/v7/reports/v7-substrate-claims.ttl`
- **shapes:** `/tmp/apparatus-v3-composed.ttl`
- **ontology:** `/Volumes/G-DRIVE/Shared/SecurityByDesign-TheoryOfEverything/sbd-toe-ontology/formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl`
- **data_triples:** `181464`
- **shapes_triples:** `398`
- **ontology_triples:** `1824`

## Per-shape (per-invariant) findings

| Shape | Invariant | Violations |
|---|---|---:|
| `https://securitybydesign.dev/ontology/appsec-core/v1#ClaimWellFormednessShape` | M4-card — Claim well-formedness (cardinalities + types) | 0 |
| `https://securitybydesign.dev/ontology/appsec-core/v1#SliceCoherenceClaimShape` | M1' — Slice coherence on claim (subsumes M2 for CO-level) | 0 |
| `https://securitybydesign.dev/ontology/appsec-core/v1#PracticeCOConsistencyShape` | M3 — Practice ∈ CO consistency (Practice-level claims) | 0 |
| `https://securitybydesign.dev/ontology/appsec-core/v1#MechanismCOConsistencyShape` | M4 — Mechanism ∈ CO chain (Mechanism-level claims; gap 1) | 0 |
| `https://securitybydesign.dev/ontology/appsec-core/v1#ClaimTargetReferentialIntegrityShape` | M4-card / referential integrity — claim target IRI resolves with matching level | 0 |

## Caveat

Model-invariant shapes only (M1' / M2 subsumed / M3 / M4 via CO chain / M4-card). Process-side invariants (M5 semantic warrant, P1' grounded-implies-claim) are NOT enforced here; consumers guarantee them by construction (Pydantic + assertions + tests). Apparatus tag appsec-core-v0-shapes.ttl is NOT modified by this validator; this file ALONGSIDE it adds claim-targeted shapes without touching ontology-targeted apparatus shapes.
