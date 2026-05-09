# LLM-assist provenance log — substrate v7 addendum (publishability transparency)

**Purpose:** Continues the discipline established at `data/p7_olir_audit/p7_v2_corrected/v4_0_substrate_construction/llm_assist_provenance.md` (Stage 6 v4.0 era 2026-04-28, frozen at that era's state). This v7 addendum logs LLM-assist contributions to substrate v7 cycle artefacts (Iteration 3 + P7 Pass 6 follow-ups).

**Branch:** `cartographer-iteration-3-ai-ml-expansion`
**Author of this log:** Cartographer (Claude Opus 4.7) — same model that produced the contributions logged below.
**Discipline (inherited):** *"log what model did, not pretend agent and model are different"*.

---

## Discipline summary (rule, not aspiration)

- **Runtime LLM calls in pipeline execution layer at substrate v7 cycle: 0 (zero).** All grounding (Stage 4 PIPELINE 2), substrate emission (Stage 5), LDP cluster analysis (Stage 6), H2 evaluation (Stage 7), cross-validation runs (P7 §8.2 deliveries) executed via deterministic Python + pinned SBERT model.
- **LLM-assist permitted at:** script authorship, methodology heuristic proposals, brief drafting, decision documentation, evidence-package authoring, figure layout & caption authoring.
- **LLM-assist NOT permitted at:** per-item GROUNDED/LDP/OOS classification, calibration threshold derivation, claim emission, cluster membership assignment, ACR-candidacy verdicts, or any per-pair convergence determination — those flow through deterministic algorithm in `score.py`/`run_pipeline_v7.py`/`ldp_cluster_analysis_v7.py`/etc.

---

## Phase-by-phase log (substrate v7 cycle)

### Phase 7.1 — Iteration 3 source acquisition + lifting + substrate v7 emission

**LLM contribution:** Cartographer (Claude Opus 4.7) authored the following Python scripts:
- `scripts/extract_iteration_3_ai_ml_sources.py` (5-pilot batched extractor)
- `scripts/v5_normalization/flattening/{mitre_atlas, owasp_llm_top_10, owasp_ml_top_10, nist_ai_100_2_e2025, nist_ai_rmf_1_0}_flattener.py`
- `scripts/v5_normalization/run_iteration_3_flatteners.py`
- `scripts/v5_normalization/grounding/run_pipeline_v7.py`
- `scripts/v5_normalization/grounding/emit_substrate_v7_ttl.py`
- `scripts/v5_normalization/grounding/ldp_cluster_analysis_v7.py`

Plus all corresponding briefs, DSR-HISTORY records, evidence packages, and programme-wide mirror handovers.

**LLM did NOT:**
- Run the model API for any per-item judgment during substrate v7 production (deterministic Python + pinned SBERT)
- Compute claim similarity scores (deterministic from `encode.py`)
- Choose match classifications (deterministic from `score.py` thresholds)

**Inputs LLM consumed:**
- Iteration 3 declaration `DevelopmentGovernance/docs/dsr-iteration-3-robustness-validation.md`
- Programme-lead dispatchers (read-only)
- Substrate v6 baseline at `substrate-v6-acr004-incorporated`
- AppSec Core V1.next + embeddings v1.1 (read-only)

**Verifiability:** re-running the pipeline against the same SUPPLIER + SBERT model + lib versions produces byte-identical output (modulo wall-clock timestamps in metadata).

### Phase 7.2 — P7 §8.2 cross-validation deliveries

**LLM contribution:** Cartographer authored:
- `scripts/cross_validate_ssdf_references_v7.py` (SSDF v7 forward-direction port from v3-era)
- `scripts/cross_validate_ssdf_references_v7_filtered.py` (filtered NON-ASVS variant)
- `scripts/cross_validate_scf_strm_v7.py` (SCF cross-pilot pair generation + per-pilot ID normalizers)
- `scripts/frontier_match_and_audit_v7.py` (3-tier metric + per-task hit rate + XLSX writer)

**Heuristic proposals (J-points) — LLM judgment, programme-lead may revise:**
- **J-V7-A1:** CO-level-preferred primary anchor derivation (mirrors v1.1-era `primary_core_anchor` convention; alternative `prefer_co_level=False` parameter exposed for sensitivity).
- **J-V7-A2:** Variant B (GROUNDED both sides) chosen as default per-pair counting variant (Variant A all-pairs / Variant C GROUNDED-source-only available on demand).
- **J-V7-A3:** Per-pilot ID normalizers (NIST zero-pad, CIS .0-strip, SSDF practice-prefix, PCI sub-req collapse, OWASP year tolerance, EU Article→prefix-ART, HIPAA parens→concat). Heuristic; per-pilot resolution counts disclosed in JSON output for audit.
- **J-V7-A4:** Task-to-practice rollup fallback (PW.8.1 → PW.8 when v7 substrate has only Practice-level SSDF items). Documented; affects same-level pair count (122 → 142).
- **J-V7-A5:** Frontier metric definition `(left.{primary∪secondary} slices) ∩ (right.{primary∪secondary} slices) ≠ ∅`. Per dispatcher §"Frontier match metric" exact spec.
- **J-V7-A6:** ASVS-contamination flag classification (OWASPASVS / OWASPMASVS / OWASPSCVS) per dispatcher 2026-05-08 §"Filter rules".

**LLM did NOT:**
- Compute any cosine similarity (deterministic from SBERT encoder)
- Compute any cluster membership (deterministic from scipy agglomerative)
- Decide any individual pair's match class (deterministic from comparison of derived primary anchors / slices)

**Verifiability:** all scripts byte-deterministic against the same substrate v7 SUPPLIER. JSON outputs include all derivation parameters (e2_pct, e3_pct, prefer_co_level flag, oracle path, methodology variant) for audit reproducibility.

### Phase 7.3 — P7 §8.2 multi-claim alignment SVG figures

**LLM contribution:** Cartographer authored:
- `scripts/figures/generate_p7_section_8_2_figures.py` (3-figure emitter; reads SUPPLIER_v7 + emits `.dot` per figure; subprocess `dot -Tsvg/-Tpdf/-Tpng`)
- 3 graphviz `.dot` source files (the deterministic figure specs / "prompts"):
  - `figure-1-pw8-sa11-multi-claim-alignment.dot`
  - `figure-2-po1-sa1-strict-match-baseline.dot`
  - `figure-3-po2-ops15-genuine-divergence.dot`
- Natural-language prompt-spec doc `figures-p7-section-8-2-prompt-specs.md` (this addendum's companion)

**LLM did NOT:**
- Generate raster pixels via image generation model (no DALL-E / Imagen / Midjourney / etc. — figures are 100% vector graphviz output)
- Compute any claim similarity score, frontier set, or match class for the figures (all data extracted deterministically from substrate v7 SUPPLIER)
- Choose pair examples in any classifier sense (programme-lead specified PW.8/SA-11; Cartographer selected variants 2+3 via documented heuristics — see J-V7-B1, J-V7-B2 below)

**Heuristic proposals (J-points) — LLM judgment, programme-lead may revise:**

- **J-V7-B1:** Selection of pair for Figure 2 (strict-match clean baseline). Cartographer selected `SSDF-PRACTICE-PO.1 ↔ SP800-53-SA-1` from 28 strict-match pairs in same-level pool. Selection criteria documented in script: ≥3 claims per side; both substantively meaningful (not edge cases); substrate v7 yields both → ACO-TMR-008. Programme-lead may revise to a different strict-match pair (3 candidates surfaced: PO.1↔SA-1, PO.1↔SA-4, PO.2↔SA-3).
- **J-V7-B2:** Selection of pair for Figure 3 (frontier-FALSE genuine divergence). Cartographer selected `SSDF-PRACTICE-PO.2 ↔ SCAGILE-OPS-15` from 7 frontier-FALSE same-level pairs. Selection criterion: clearest pedagogical divergence (governance vs training is a recognisable cross-domain example). Programme-lead may revise (other 6 candidates surfaced — e.g., PW.6.2 ↔ SCFPSSD-COMPILER would emphasise within-domain substrate-disagreement instead).
- **J-V7-B3:** Visual encoding choices: 3-tier vertical layout (rankdir=TB); pilot-coloured borders (SSDF blue / NIST green / SafeCode brown); level fill colours (CO yellow / Practice green / Mechanism blue); primary claim red border; frontier intersection slice gold fill; edge thickness mapped 0.4-0.8 → 1-4px. All encoding choices arbitrary within paper-quality conventions; LLM judgement; programme-lead may revise via simple `.dot` source edit.
- **J-V7-B4:** Caption wording: drafted by Cartographer; semantic claims grounded in measured substrate v7 numbers (verified at SHA `596783ed...62be04`); rhetorical phrasing is LLM judgement.
- **J-V7-B5:** Style conventions inherited verbatim from `appsec-core-ontology-research-authoring/papers/{00,05}/source/images/` (font `STIX Two Text`; palette `#f4f4f8`/`#2c3e50`; HTML labels). Cartographer chose to inherit rather than invent; programme-lead consistency with prior paper figures.

**Inputs LLM consumed:**
- Mini-dispatcher `2026-05-08-orchestrator-cartographer-multi-claim-alignment-svg-mini-dispatch.md` §"Figure specification"
- Substrate v7 SUPPLIER (read-only; SHA `596783ed...62be04`)
- Programme convention exemplars at `appsec-core-ontology-research-authoring/papers/{00,05}/source/images/*.dot` (read-only)
- Per-pair audit XLSX (already-emitted artefact)

**Verifiability:** Re-running `python3 -m scripts.figures.generate_p7_section_8_2_figures` against the same SUPPLIER produces byte-identical `.dot` files (modulo HTML attribute ordering quirks in some graphviz versions, which the test framework can disambiguate via canonical re-render). The `.dot` → `.svg` step is 100% deterministic graphviz output.

---

## Joint-review judgement points outstanding

Programme-lead inspection at joint-review session may revise any of:
- J-V7-A1 — CO-level-preferred primary anchor derivation (alternative: highest-similarity-overall regardless of level)
- J-V7-A4 — Task-to-practice rollup convention
- J-V7-B1 — Figure 2 pair selection (3 candidates surfaced)
- J-V7-B2 — Figure 3 pair selection (7 candidates surfaced)
- J-V7-B3 — Visual encoding (palette / typography / etc.)
- J-V7-B4 — Caption wording

Programme-lead revisions feed back via dispatcher; Cartographer re-emits affected artefacts (scripts byte-deterministic, so re-run is mechanical).

## Pre-existing log (frozen, NOT modified by this addendum)

`data/p7_olir_audit/p7_v2_corrected/v4_0_substrate_construction/llm_assist_provenance.md` is preserved at its 2026-04-28 v4.0-era state (J10–J16 logged for V1 lab-overlay phase). This v7 addendum is additive; the v4.0 log is NOT modified.

## Date trail

| Date | Phase | Event |
|---|---|---|
| 2026-05-06 | 7.1 | Iteration 3 declared; Cartographer authoring begins |
| 2026-05-08 (early) | 7.1 | Substrate v7 emitted; ratified; tagged `substrate-v7-iter-3-ai-ml-incorporated` |
| 2026-05-08 (mid) | 7.2 | P7 Pass 6 cross-validation deliveries (SSDF v7, SCF v7, filtered SSDF, frontier+per-task) |
| 2026-05-08 (late) | 7.3 | P7 §8.2 multi-claim alignment SVG figures (this addendum) |
