# AppSec Core V1 — Consumer Conformance Report

**Verdict:** ❌ NON-CONFORMANT
**Generated:** 2026-05-04T13:22:25.502663+00:00
**Total violations:** 7

## Inputs
- **data_graph:** `/tmp/archon-2026-05-04-apparatus-v2/formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-v2-bucket-b-fixture.ttl`
- **shapes:** `/tmp/archon-2026-05-04-apparatus-v2/formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl`
- **ontology:** `/tmp/archon-2026-05-04-apparatus-v2/packages/ontology/appsec-core/v1.0/formal/appsec-core-v0-bounded-v1.ttl`
- **data_triples:** `1879`
- **shapes_triples:** `398`
- **ontology_triples:** `1808`

## Per-shape (per-invariant) findings

| Shape | Invariant | Violations |
|---|---|---:|
| `https://securitybydesign.dev/ontology/appsec-core/v1#ClaimWellFormednessShape` | M4-card — Claim well-formedness (cardinalities + types) | 0 |
| `https://securitybydesign.dev/ontology/appsec-core/v1#SliceCoherenceClaimShape` | M1' — Slice coherence on claim (subsumes M2 for CO-level) | 3 |
| `https://securitybydesign.dev/ontology/appsec-core/v1#PracticeCOConsistencyShape` | M3 — Practice ∈ CO consistency (Practice-level claims) | 1 |
| `https://securitybydesign.dev/ontology/appsec-core/v1#MechanismCOConsistencyShape` | M4 — Mechanism ∈ CO chain (Mechanism-level claims; gap 1) | 1 |
| `https://securitybydesign.dev/ontology/appsec-core/v1#ClaimTargetReferentialIntegrityShape` | M4-card / referential integrity — claim target IRI resolves with matching level | 1 |

## First violations (up to 25 of 7)

| # | Shape | Focus node | Value |
|---:|---|---|---|
| 1 | `https://securitybydesign.dev/ontology/appsec-core/v1#ClaimTargetReferentialIntegrityShape` | `https://example.test/v2-fixture/claim-bad-D` | `https://example.test/v2-fixture/claim-bad-D` |
| 2 | `https://securitybydesign.dev/ontology/appsec-core/v1#MechanismCOConsistencyShape` | `https://example.test/v2-fixture/claim-bad-C` | `https://example.test/v2-fixture/claim-bad-C` |
| 3 | `https://securitybydesign.dev/ontology/appsec-core/v1#PracticeCOConsistencyShape` | `https://example.test/v2-fixture/claim-bad-B` | `https://example.test/v2-fixture/claim-bad-B` |
| 4 | `https://securitybydesign.dev/ontology/appsec-core/v1#SliceCoherenceClaimShape` | `https://example.test/v2-fixture/claim-bad-A` | `https://example.test/v2-fixture/claim-bad-A` |
| 5 | `https://securitybydesign.dev/ontology/appsec-core/v1#SliceCoherenceClaimShape` | `https://example.test/v2-fixture/claim-bad-B` | `https://example.test/v2-fixture/claim-bad-B` |
| 6 | `https://securitybydesign.dev/ontology/appsec-core/v1#SliceCoherenceClaimShape` | `https://example.test/v2-fixture/claim-bad-C` | `https://example.test/v2-fixture/claim-bad-C` |
| 7 | `n92ea1d3f56be4af4875c66a8fdee6e13b58` | `https://example.test/v2-fixture/claim-bad-E` | `—` |

## Caveat

Model-invariant shapes only (M1' / M2 subsumed / M3 / M4 via CO chain / M4-card). Process-side invariants (M5 semantic warrant, P1' grounded-implies-claim) are NOT enforced here; consumers guarantee them by construction (Pydantic + assertions + tests). Apparatus tag appsec-core-v0-shapes.ttl is NOT modified by this validator; this file ALONGSIDE it adds claim-targeted shapes without touching ontology-targeted apparatus shapes.
