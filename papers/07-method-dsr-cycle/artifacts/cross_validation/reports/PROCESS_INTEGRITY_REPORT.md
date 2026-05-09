# Substrate v7 — Process Integrity Report (Iteration 3 AI/ML expansion)

**Generated:** 2026-05-07
**Branch (ESI):** cartographer-iteration-3-ai-ml-expansion (off tag substrate-v6-acr004-incorporated = ff28860)
**Iteration:** Cycle A Iteration 3 (DSR Robustness Validation under AI/ML Expanded Source Pressure)
**Substrate baseline:** substrate-v6-acr004-incorporated (= ff28860; substrate v6)
**Ontology:** ontology-v1-next-acr004-promoted (V1.next, 212 entities)
**Apparatus:** apparatus-shacl-pyshacl-v3 (composition: appsec-core-v0-shapes.ttl + consumer-conformance-shapes.ttl)
**Embeddings:** appsec-core-embeddings-v1.1 (NPZ SHA `17f6aac4...23c8`, env-determinism mirrored §F)

## Termination gates — MIXED VERDICT (joint-review-resolved 2026-05-08)

| Gate | Required | Measured | Verdict | Joint-review (2026-05-08) |
|---|---|---|---|---|
| **SHACL CONFORMS** | 0 violations | **0** across M1' / M3 / M4 / M4-card / referential integrity | ✅ PASS | accepted |
| **GROUNDED ≥ 75.38%** (substrate v6 baseline) | ≥75.38% | **74.41%** (2873 / 3861 items) | ❌ FAIL (-0.97pp) | ✅ **ACCEPTED as corpus-expansion statistical artifact** |

## Joint-review HALT resolution (2026-05-08)

> Substrate v7 GROUNDED rate 74.41% (n=3861) is below substrate v6 baseline 75.38% (n=3457) by 0.97pp. This is a corpus-expansion statistical artifact, NOT methodology regression: 26 baseline sources reproduce bit-identically (zero shift); 5 Iteration 3 sources land at domain-appropriate rates spanning 58.5%–90% (OWASP LLM Top 10 90%, OWASP ML Top 10 90%, NIST AI 100-2 71.7%, MITRE ATLAS 64.7%, NIST AI RMF 58.5%). The 75.38% v6 baseline was itself a 26-source-mix measurement; corpus expansion mechanically shifts the global average even under bit-identical methodology. Per-source rates are the methodology-integrity signal; global average is corpus-mix-dependent. Two pre-iteration hypotheses falsified positive at this stage: NIST AI RMF NOT governance-heavy pathology (above EU regulatory peers +8 to +14pp); OWASP LLM Top 10 atomicity 6.4 NOT harming grounding (90% G with 146 claims from 64 lifted rows). H2 sub-hypothesis (inverted-mapping methodology generalizes from CWE/CAPEC to AI/ML problem-space-inverted sources) gains favorable gate-level evidence on TWO independent surfaces (ATLAS + OWASP ML Top 10); final H2 decision at Stage 7. Statistical artifact accepted by joint review (programme-lead Pedro Farinha + Orchestrator) 2026-05-08 per Iteration 3 dispatcher §"Per-source quality gate" decision discipline. Cartographer authorized to advance to Stage 6 LDP analysis recomputation under existing dispatcher authority.

**Substrate v7 RATIFIED for Iteration 3 evidence base.** Stages 6/7/8 advance under existing dispatcher authority.

## Aggregate counts

| Metric | Substrate v6 (26-source baseline) | Substrate v7 (31-source) | Δ |
|---|---:|---:|---:|
| ACTIVE_SOURCES | 26 | 31 | +5 |
| items_total | 3457 | 3861 | +404 |
| claims_total | 17507 | 18673 | +1166 |
| GROUNDED | 2606 (75.38%) | 2873 (74.41%) | +267 (-0.97pp) |
| LabDepthPending | 851 | 988 | +137 |
| OOS_AppSec | 0 | 0 | 0 |

## Regression decomposition — CORPUS-EXPANSION ARTIFACT, NOT METHODOLOGY DEGRADATION

### Existing 26 sources — BIT-IDENTICAL reproduction

The 26 baseline sources reproduce v6 EXACTLY in (n, GROUNDED, LabDepthPending, claims) tuples. Zero shift from v6. Calibration thresholds re-derived deterministically (same model + revision + cohort + library versions per Decision 0003 Amendment 1 §F augmentation symmetry); thresholds bit-stable.

| 26-baseline subset within substrate v7 | n | GROUNDED | G% |
|---|---:|---:|---:|
| (calculated from per-source contracts) | 3457 | 2606 | **75.38%** ← matches v6 baseline exactly |

### 5 Iteration 3 new sources — corpus-expansion delta

| Pilot | Mapping direction | n | GROUNDED | G% | Outcome A criterion (≥70%) |
|---|---|---:|---:|---:|---|
| `mitre_atlas` | problem_space_inverted | 278 | 180 | **64.7%** | ❌ |
| `nist_ai_100_2_e2025` | mixed | 53 | 38 | 71.7% | ✅ |
| `nist_ai_rmf_1_0` | mixed (governance-leaning) | 53 | 31 | **58.5%** | ❌ |
| `owasp_llm_top_10` | solution_space_direct | 10 | 9 | 90.0% | ✅ |
| `owasp_ml_top_10` | problem_space_inverted | 10 | 9 | 90.0% | ✅ |
| **iter-3 aggregate** | mixed | 404 | 267 | **66.1%** | ❌ |

### Structural-peer comparison — Iteration 3 sources at parity with corpus peers

| Iteration 3 source | G% | Closest structural peer in corpus | Peer G% | Comparison |
|---|---:|---|---:|---|
| mitre_atlas (problem-space-inverted) | 64.7% | capec_v3_9 (problem-space-inverted) | 63.5% | **+1.2pp** — ATLAS performs at parity with CAPEC, the inverted-mapping precedent. **H2 sub-hypothesis empirically supported at the GROUNDED-rate level.** |
| nist_ai_rmf_1_0 (governance-leaning) | 58.5% | eu_rgpd / eu_dora / eu_cra (governance) | 50.0% / 45.8% / 44.4% | **+8 to +14pp** — RMF outperforms EU regulatory peers despite expected governance pathology. Pre-iteration "expected high lifted-concern" hypothesis empirically refined: RMF more methodologically valuable than predicted (echoes Stage 3 dossier surprise). |
| nist_ai_100_2_e2025 (mixed taxonomy) | 71.7% | (no precise peer; mid-range) | — | Above 70% Outcome A criterion. |
| owasp_llm_top_10 + owasp_ml_top_10 | 90.0% each | (10-item OWASP risk-page format peers) | — | Above corpus average. |

### All 31 sources sorted by GROUNDED rate ascending

The 5 Iteration 3 sources do NOT occupy the lowest-performing positions:

```
cwe_software_development_view_v4_19_1                    38.1%
eu_cra                                                   44.4%
eu_dora                                                  45.8%
eu_rgpd                                                  50.0%
nist_ai_rmf_1_0                                          58.5% ← iter-3
mcp_official_security_foundations_2025                   61.5%
capec_v3_9                                               63.5%
mitre_atlas                                              64.7% ← iter-3
nist_ai_100_2_e2025                                      71.7% ← iter-3
asvs_v5_0_0                                              72.5%
... (rest above 75%)
owasp_llm_top_10                                         90.0% ← iter-3
owasp_ml_top_10                                          90.0% ← iter-3
```

CWE / EU CRA / EU DORA / EU RGPD all sit BELOW the 5 Iter-3 sources' lowest performer (NIST AI RMF). The 26-source baseline already contained 4 sources below 50% GROUNDED — the 75.38% global baseline is itself an artifact of source-mix composition. Adding 5 sources at heterogeneous structural-peer-parity rates necessarily shifts the global average mechanically.

## Cartographer characterisation

The -0.97pp regression is **mechanical corpus-expansion arithmetic**, not methodology degradation:

1. **No shift on existing 26 sources** (bit-identical reproduction).
2. **Iteration 3 sources land at structural-peer parity** in the existing corpus.
3. **Calibration thresholds re-derived deterministically** (cohort SSDF + CIS + SAMM + CWE unchanged; thresholds reproducible).
4. **SHACL CONFORMS** — substrate structurally valid against all 5 model invariants.

The dispatcher §"Termination criteria" gate at "GROUNDED ≥ 75.38%" is a 26-source-specific number that becomes mechanically harder to clear under corpus expansion, even when the new sources behave well. The Outcome A criterion (§4: "AI/ML new-source items GROUNDED ≥ 70% via existing Core entities") is the more meaningful measurement: AI/ML aggregate 66.1% < 70% — but this is dragged by 2 of 5 sources (ATLAS + RMF) that sit at structural-peer parity, NOT at outlier underperformance.

## Sub-hypothesis H2 (preliminary signal — formal Stage 7 decision pending joint-review resolution)

H2: *Inverted-mapping methodology generalises from CWE/CAPEC to MITRE ATLAS without refinement.*

Preliminary evidence at substrate v7 emission:
- **MITRE ATLAS GROUNDED rate**: 64.7% / 113 distinct entities reached / 610 claims emitted.
- **CAPEC GROUNDED rate**: 63.5% / 125 entities / 1400 claims (substrate v7; identical to v6).
- **OWASP ML Top 10 GROUNDED rate** (H2 secondary surface): 90.0% / 51 entities / 107 claims.
- ATLAS-vs-CAPEC parity at the GROUNDED-rate level: **+1.2pp** — H2 confirmed at the gate level. OWASP ML at 90% performs ABOVE corpus average for problem-space-inverted, providing a second supporting data point.

Formal H2 decision (confirmed / refined / refuted) requires Stage 7 cluster analysis, which awaits joint-review halt resolution.

## Calibration thresholds (e2_pct=40 / e3_pct=60; cohort SSDF + CIS + SAMM + CWE)

| Level | E2 | E3 |
|---|---:|---:|
| ControlObjective | 0.4110 | 0.0430 |
| Practice | 0.4144 | 0.0470 |
| Mechanism | 0.4082 | 0.0471 |

Thresholds reproducible from substrate v6 baseline (cohort items unchanged; ontology unchanged; encoder unchanged).

## SHACL conformance evidence

| Shape | Invariant | Violations |
|---|---|---:|
| `ClaimWellFormednessShape` | M4-card | 0 |
| `SliceCoherenceClaimShape` | M1' (subsumes M2 for CO-level) | 0 |
| `PracticeCOConsistencyShape` | M3 | 0 |
| `MechanismCOConsistencyShape` | M4 (CO chain; gap 1 charitable) | 0 |
| `ClaimTargetReferentialIntegrityShape` | M4-card / referential integrity | 0 |

Inputs:
- data: `data/p7_olir_audit/p7_v2_corrected/v7/reports/v7-substrate-claims.ttl` (181464 triples; 18673 claims, 3861 items)
- shapes: apparatus-v3 composed graph (appsec-core-v0-shapes.ttl + consumer-conformance-shapes.ttl; 398 triples)
- ontology: `sbd-toe-ontology/formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` (1824 triples; V1.next)

Validator: `sbd-toe-ontology/scripts/consumer_conformance_validator.py` (pyshacl 0.31.0 / rdflib 7.6.0).

## Iteration 3 caveats (substrate provenance per joint-review 2026-05-07 ratification)

- **owasp_llm_top_10 atomicity 6.4 (Stage 3 FLAG)** — ratified PROCEED 2026-05-07 by programme-lead Pedro Farinha + Orchestrator. Structural intentional bundling (Description + Common Examples + Prevention Strategies per LLMNN page); duplicate-fraction 0; governance-fraction 3.1%; NOT pathology. 90% GROUNDED rate at substrate v7 confirms PROCEED was correct.
- **enisa_ai_2024 DROPPED** — no discrete 2024 successor exists to ENISA Multilayer Framework 2023.
- **nist_ai_rmf governance surprise** — Stage 3 governance-fraction 19% (under 40% threshold); pre-iteration "RMF expected governance-heavy pathology" hypothesis falsified at Stage 3. Substrate v7 GROUNDED rate 58.5% confirms RMF performs ABOVE EU regulatory peers (50%/45.8%/44.4%) despite governance leaning — RMF more methodologically valuable than predicted.

## Halt + joint-review signal

Per dispatcher §"Authorization scope" trigger 1 (programme-lead + Orchestrator joint review 2026-05-07): "GROUNDED < 75.38% baseline regression" requires halt + joint-review signal before Stage 6 (LDP analysis) + Stage 7 (H2 decision) + Stage 8 (evidence package) proceed.

Cartographer-recommended joint-review options:

| Option | Description | Implication |
|---|---|---|
| (i) Accept regression as corpus-expansion-attributed | Recognise -0.97pp delta is mechanical, not methodology failure; Outcome A criterion at AI/ML-aggregate level (66.1%) acknowledged as below 70% but dragged by 2 of 5 sources at structural-peer parity; proceed Stage 6+7+8 | Pre-registration discipline preserved (criteria immutable mid-iteration); Stage 8 joint review weighs full evidence including H2 + cluster analysis to decide A/B/C |
| (ii) Refine pre-registration criteria for Iteration 3 | Programme-lead amends §"GROUNDED ≥ 75.38%" gate to "26-baseline subset must reproduce exactly + iter-3 must clear Outcome A criterion" | Methodologically cleaner; explicit acknowledgement that global-rate gate is corpus-mix-dependent; pre-registration honesty respected |
| (iii) Investigate methodology refinement | Calibration thresholds tighter? Different cohort? | Disrupts pre-registration discipline mid-iteration; not recommended |
| (iv) Drop low-performers | Exclude ATLAS or RMF from substrate; rerun | Loses H2 primary test surface; sacrifices methodological contribution; not recommended |

**Cartographer-default lean: option (i) — accept as corpus-expansion artifact + proceed to Stage 6+7+8.** Outcome A/B/C decision at Stage 8 evaluates the full evidence base (cluster analysis + H2 + multi-source convergence) under the pre-registered asymmetric burden of proof. The 26-baseline-bit-identical reproduction + structural-peer parity for iter-3 sources is empirical evidence that AI/ML pressure does NOT degrade methodology.

Programme-lead + Orchestrator decide.

## Outputs

| Path | Description |
|---|---|
| `SUPPLIER_v7_0.json` | Substrate v7 supplier (Pydantic-validated) |
| `MANIFEST_v7_0.json` | Substrate v7 manifest with iteration_3_caveats + termination_gates blocks |
| `<source>/per_item_contract.json` (×31) | Per-source items + claims |
| `reports/ontology_side_index.json` | Per-target claim aggregation |
| `reports/calibration_distribution.json` | Threshold derivation evidence |
| `reports/v7-substrate-claims.ttl` | RDF emission for SHACL (181464 triples) |
| `reports/v7-substrate-claims-shacl-report.{md,json}` | SHACL CONFORMS (0 violations) |
| `reports/PROCESS_INTEGRITY_REPORT.md` | this file |

## Worktree state

- Branch: `cartographer-iteration-3-ai-ml-expansion`
- Base: `substrate-v6-acr004-incorporated` (= ff28860)
- NOT pushed; NOT tagged. Awaiting joint-review halt resolution before Stage 6+ proceed.
