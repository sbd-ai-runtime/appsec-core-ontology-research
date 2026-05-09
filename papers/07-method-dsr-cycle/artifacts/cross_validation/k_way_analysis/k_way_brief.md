# k-way Intersection Analysis — Substrate v7 (Phase A.5)

**Date:** 2026-05-09
**Author:** Cartographer (under programme-lead Pedro Farinha)
**Substrate:** v7 (`SUPPLIER_v7_0.json` SHA `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04`)
**Generator:** `scripts/k_way_null_model.py` (deterministic; seed=42)

## Method (verbatim)

- **k-way intersection per entity** (set membership): `k(e) = |{ source ∈ ES : ∃ GROUNDED claim with target = e ∧ source = source }|`
- **Null model** (Type II permutation test): permute claim→source labels (preserve multiset per source + per-entity claim count); 1000 trials; empirical p-value = P(null_metric ≥ observed).
- **Scope:** 202 substantive AC V1 entities (75 CO + 69 P + 58 M; Slice 10 excluded as structural).

## Observed values (verbatim)

- n_entities: **202**
- n_claims_grounded: **18673**
- n_sources: **31**
- mean_k: **10.7673**
- median_k: **10.0**
- stdev_k: **6.2143**
- max_k: **26**
- min_k: **1**
- k≥3 fraction: **0.9307** (188/202)
- k≥5 fraction: **0.8267** (167/202)
- k≥10 fraction: **0.5198** (105/202)

### Histogram

| Bin | Count |
|---|---:|
| k=0 | 0 |
| k=1 | 6 |
| k=2 | 8 |
| k=3 | 12 |
| k=4 | 9 |
| k>=5 | 167 |
| k>=10 | 105 |

### By type (CO / P / M)

| Type | n | mean_k | median_k | stdev_k | max_k | min_k | k≥3 frac | k≥5 frac | k≥10 frac |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CO | 75 | 10.013 | 9.0 | 6.050 | 26 | 1 | 0.907 | 0.800 | 0.467 |
| P | 69 | 10.536 | 10.0 | 6.450 | 26 | 1 | 0.913 | 0.797 | 0.507 |
| M | 58 | 12.017 | 11.5 | 6.051 | 25 | 2 | 0.983 | 0.897 | 0.603 |

## Null-model baseline (verbatim)

- N trials: **1000**
- Random seed: **42**

### Null distribution (95% CI) + empirical p-values

| Metric | Null p5 | Null p50 | Null p95 | Observed | P(null ≥ obs) | P(null ≤ obs) | Two-sided p |
|---|---:|---:|---:|---:|---:|---:|---:|
| mean_k | 13.1188 | 13.2574 | 13.3911 | **10.7673** | 1.0000 | 0.0000 | **0.0000** |
| k≥3 fraction | 0.9406 | 0.9554 | 0.9653 | **0.9307** | 1.0000 | 0.0020 | **0.0040** |
| k≥5 fraction | 0.8713 | 0.8911 | 0.9059 | **0.8267** | 1.0000 | 0.0000 | **0.0000** |
| k≥10 fraction | 0.6485 | 0.6733 | 0.7030 | **0.5198** | 1.0000 | 0.0000 | **0.0000** |

**Interpretation pointer (verbatim):** Observed mean_k=10.7673 vs null median=13.2574 (95% CI [13.0941, 13.4208]). Observed is LOWER than null distribution; two-sided empirical p < 0.001 (extreme). One-sided P(null ≥ observed) = 1.0000; P(null ≤ observed) = 0.0000 (across 1000 trials, seed=42). Domain reading: observed mean_k LOWER than random shuffle baseline → sources cluster their GROUNDED claims onto FEWER distinct entities than uniform random assignment would predict. This is consistent with semantic specificity: methodology produces source-entity assignments with concentration structure beyond what claim-count marginals alone would generate.

## Top 10 entities by k (highest cross-source coverage)

| # | entity_id | type | k | sources |
|---:|---|---|---:|---|
| 1 | `ACO-TMR-005` | CO | **26** | asvs_v5_0_0, capec_v3_9, cis_controls_v8_1_2, cwe_software_development_view_v4_19_1, enisa_multilayer_ai_cybersecurity_practices_2023 (+21 more) |
| 2 | `ACP-SLG-003` | P | **26** | asvs_v5_0_0, capec_v3_9, cis_controls_v8_1_2, cwe_software_development_view_v4_19_1, eu_nis2 (+21 more) |
| 3 | `ACP-TMR-005` | P | **26** | asvs_v5_0_0, capec_v3_9, cis_controls_v8_1_2, cwe_software_development_view_v4_19_1, eu_cra (+21 more) |
| 4 | `ACM-SLG-003` | M | **25** | asvs_v5_0_0, capec_v3_9, cis_controls_v8_1_2, cwe_software_development_view_v4_19_1, eu_nis2 (+20 more) |
| 5 | `ACO-RPR-009` | CO | **25** | asvs_v5_0_0, capec_v3_9, cis_controls_v8_1_2, cwe_software_development_view_v4_19_1, eu_cra (+20 more) |
| 6 | `ACM-IAT-002` | M | **24** | asvs_v5_0_0, capec_v3_9, cis_controls_v8_1_2, cwe_software_development_view_v4_19_1, eu_dora (+19 more) |
| 7 | `ACP-IAT-006` | P | **24** | asvs_v5_0_0, capec_v3_9, cis_controls_v8_1_2, cwe_software_development_view_v4_19_1, eu_dora (+19 more) |
| 8 | `ACM-SPC-001` | M | **23** | asvs_v5_0_0, capec_v3_9, cis_controls_v8_1_2, cwe_software_development_view_v4_19_1, eu_nis2 (+18 more) |
| 9 | `ACM-IAT-006` | M | **22** | asvs_v5_0_0, capec_v3_9, cis_controls_v8_1_2, cwe_software_development_view_v4_19_1, eu_dora (+17 more) |
| 10 | `ACO-ATB-002` | CO | **22** | asvs_v5_0_0, capec_v3_9, cis_controls_v8_1_2, cwe_software_development_view_v4_19_1, eu_nis2 (+17 more) |

## Bottom 10 entities by k (lowest cross-source coverage)

| # | entity_id | type | k | sources |
|---:|---|---|---:|---|
| 1 | `ACO-RPR-003` | CO | 1 | mitre_atlas |
| 2 | `ACO-RPR-006` | CO | 1 | nist_sp800_53_rev5 |
| 3 | `ACO-SLG-006` | CO | 1 | cwe_software_development_view_v4_19_1 |
| 4 | `ACP-RPR-006` | P | 1 | eu_dora |
| 5 | `ACP-SCBI-004` | P | 1 | owasp_llm_top_10 |
| 6 | `ACP-TMR-004` | P | 1 | owasp_samm_v2_1 |
| 7 | `ACM-ATB-003` | M | 2 | cwe_software_development_view_v4_19_1, nist_sp800_53_rev5 |
| 8 | `ACO-ATB-001` | CO | 2 | nist_sp800_53_rev5, owasp_samm_v2_1 |
| 9 | `ACO-ATB-003` | CO | 2 | mitre_atlas, nist_sp800_53_rev5 |
| 10 | `ACO-SPC-003` | CO | 2 | asvs_v5_0_0, cwe_software_development_view_v4_19_1 |

## Substrate v5 baseline (recall)

Comparison: substrate v5 (26 sources) → substrate v7 (31 sources, +5 AI/ML iter-3 sources).

| Metric | Substrate v5 | Substrate v7 | Δ (v7 − v5) |
|---|---:|---:|---:|
| n_sources | 26 | 31 | +5 |
| n_claims_grounded | 17446 | 18673 | +1227 |
| mean_k | 9.0941 | 10.7673 | +1.6733 |
| median_k | 8.0 | 10.0 | +2.0 |
| max_k | 22 | 26 | +4 |
| k≥3 fraction | 0.9010 | 0.9307 | +0.0297 |
| k≥5 fraction | 0.7574 | 0.8267 | +0.0693 |

**Scope-discrepancy reconciliation (verbatim):** Dispatcher cites v5 mean_k=8.63 from memory `project_substrate_v5_ratified_2026_05_03.md`. Computation on current `SUPPLIER_v5_0.json` yields:

- **scope 202 substantive** (excl. 10 Slice; matches dispatcher §Step 1 methodology): mean_k = **9.0941**
- **scope 212 (incl. Slice at k=0)**: mean_k = **8.6651** (≈ 8.63 cited; difference ~0.04 = rounding or minor v5 state evolution)

Per dispatcher §Step 1 directive ("Slice excluded as structural"), the 202-substantive scope is canonical for comparison. The cited 8.63 figure was likely computed on 212-scope including Slice with k=0.

**Cartographer note (verbatim):** substrate v5 → v7 shift recorded without interpretation per dispatcher §Step 1 directive ('register the shift verbatim; no interpretation; just numbers'). Curator §8.2 prose integration handles methodological commentary on shift.

## Out of scope (per dispatcher)

Reserved for P9 KEOD methodology paper:
- Full FCA lattice construction (Wille 1982; Ganter & Wille)
- OAEI track participation
- Newman modularity / community detection
- Mutual information analysis
- Bipartite common-neighbors similarity matrix (full)

## Cross-references

- Phase A.5 dispatcher: `sbd-ai-runtime/handover/em-curso/2026-05-09-orchestrator-cartographer-phase-a5-k-way-null-model-dispatch.md`
- Substrate v7 SUPPLIER: `data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json`
- AC V1 entity catalog: `formal/appsec_core/08-embeddings/augmented-text-corpus.json` (212 entities; 202 substantive analysed)
- v7 substrate claims TTL: `data/p7_olir_audit/p7_v2_corrected/v7/reports/v7-substrate-claims.ttl`
- Cycle A frozen substrate baseline tag: `substrate-v7-iter-3-ai-ml-incorporated`

