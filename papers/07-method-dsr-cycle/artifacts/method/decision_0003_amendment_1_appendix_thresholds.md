# Amendment 1 — Appendix: Calibrated E2 + E3 Thresholds (Phase 1b, 2026-05-03)

**Authority:** Cartographer Phase 1b execution under Decision 0003 Amendment 1 ratified 2026-05-03.
**Companion to:** `0003-normalization-algorithm-redesign-2026-05-03-amendment-1-claims-not-chains.md` (§B PIPELINE 2 step 2.2/2.3, §4 E2 calibration cohort).
**Pipeline:** Cartographer scripts/v5_normalization/grounding/ on substrate flattener_version v1.2 (post ASVS extractor fix + CIS augmentation + contextual_grouping filter + redirect filter).
**Ontology release artefact consumed:** Archon Part A `sbd-toe-ontology/formal/appsec_core/08-embeddings/` (199 entities at target levels; 209 total including Slice).

## 1. Calibration cohort

Per Amendment 1 §4: SSDF + CIS + SAMM + CWE (four shape classes from Phase 0 audit covering chain-depth-3, chain-depth-2-atomic, chain-with-overlays, flat).

Cohort row counts (post v1.2 filters):
- `ssdf_sp800_218_v1_1`: 76 lifted rows
- `cis_controls_v8_1_2`: 327 lifted rows
- `owasp_samm_v2_1`: 295 lifted rows
- `cwe_software_development_view_v4_19_1`: 405 lifted rows
- **Total cohort:** 1103 lifted rows

## 2. Methodology

Two distributions are computed on the cohort:

- **Global per-level top-1 distribution:** for each (row, level), the maximum cosine score across the level's 199 candidate entities. Answers "what does a credible best match look like for this row at this level?".
- **Within-(slice, level) margin distribution:** for each (row, slice, level) tuple, top-1 minus top-2 within the same pool. Answers "what gap separates a confident pick from an ambiguous one?".

Threshold choice is a controllable percentile of these distributions. Lower percentile = more permissive (more claims emitted). Higher percentile = stricter.

## 3. Chosen percentiles

- **E2 (admissibility per level)** = **p40 of global per-level top-1**. Rejects rows whose best match in a level falls in the bottom 40% of the cohort distribution. Admits 60% of rows' best level matches per level.
- **E3 (disambiguation per level)** = **p60 of within-(slice, level) margin**. Requires a pool's top-1 to exceed its top-2 by at least the 60th-percentile gap. Rejects 60% of pool picks where the top-1 is too close to runner-up.

## 4. Calibrated values

Computed directly from the cohort distributions:

| Level | E2 admissibility (p40) | E3 disambiguation (p60) |
|---|---:|---:|
| ControlObjective | **0.4116** | **0.0428** |
| Practice | **0.4159** | **0.0468** |
| Mechanism | **0.4080** | **0.0468** |

Distribution percentiles (full):

**Global per-level top-1 (n=1103 per level):**

| Level | min | p10 | p25 | p50 | p75 | p90 | max | mean | std |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ControlObjective | 0.087 | 0.290 | 0.357 | 0.450 | 0.522 | 0.592 | 0.762 | 0.439 | 0.108 |
| Practice | 0.084 | 0.279 | 0.355 | 0.449 | 0.522 | 0.579 | 0.782 | 0.435 | 0.110 |
| Mechanism | 0.045 | 0.256 | 0.358 | 0.436 | 0.507 | 0.575 | 0.735 | 0.422 | 0.108 |

**Within-(slice, level) margin (n varies; per-pool count × 1103 rows):**

| Level | min | p10 | p30 | p50 | p60 | p70 | p90 | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ControlObjective | 0.0 | 0.0061 | 0.0177 | 0.0332 | 0.0428 | 0.0543 | 0.0850 | ~0.3 |
| Practice | 0.0 | 0.0066 | 0.0191 | 0.0362 | 0.0468 | 0.0601 | 0.0928 | ~0.3 |
| Mechanism | 0.0 | 0.0067 | 0.0195 | 0.0366 | 0.0468 | 0.0606 | 0.0934 | ~0.3 |

Full distributions in `data/p7_olir_audit/p7_v2_corrected/v5/reports/calibration_distribution.json`.

## 5. Resulting metrics on full 26-source corpus (post-calibration)

With E2=p40 + E3=p60 applied to all 26 sources:

- **Total items:** 3457
- **Total claims emitted:** 14479
- **GROUNDED:** ~3134 items (~90.7%)
- **LabDepthPending:** ~323 items (~9.3%)
- **OOS_AppSec:** 0 items (no OOS rules fired; OOS pre-filtering was upstream of PIPELINE 2)

Average claims per item: 4.2. Distribution by level: split across CO / Practice / Mechanism per source (see PROCESS_INTEGRITY_REPORT.md §Per-source summary).

Comparison with permissive baseline (E2=p25 + E3=p30) tested earlier: ~36k claims / ~94.6% GROUNDED. Stricter calibration reduced claims by ~60%; LabDepthPending rate roughly doubled. Reasonableness check: the stricter values feel more honest given known semantic ambiguity in heterogeneous source corpora.

## 6. Operational note

Thresholds are FIXED for the v5 substrate emission. If programme-lead later wants to test alternative percentiles (e.g., p30/p50 for more permissive, or p60/p70 for stricter), Cartographer can re-emit substrate quickly (~2 min for full corpus encode + scoring + emit) by passing different `e2_pct` / `e3_pct` to `choose_thresholds()` — the decision document records the percentile, not the score, so re-calibration on the same cohort is reproducible.

## 7. Caveats for paper §11 reproducibility

- Encoder pinning: `sentence-transformers/all-MiniLM-L6-v2` @ HF revision `c9745ed1d9f207416be6d2e6f8de32d1f16199bf`, transformers 4.57.1, torch 2.2.2, numpy 1.24.4 (mirror of Archon Part A manifest).
- Cosine on L2-normalized embeddings (dot product).
- Thresholds reproducible from the cohort distribution by selecting the named percentile; cohort distribution is committed to the substrate output.
- No ground-truth labels were used for calibration. Threshold selection is a percentile of an empirical score distribution, not a precision/recall optimum. Validation against ground truth is future work (Paper 3 §11 limitation).
