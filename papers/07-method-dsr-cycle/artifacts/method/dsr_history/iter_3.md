# Cycle A Iteration 3 — DSR Robustness Validation under AI/ML Expanded Source Pressure (2026-05-08)

**Status:** evidence package emitted; pending Stage 8 joint-review Outcome A/B/C decision
**Cycle / Iteration:** Cycle A / Iteration 3
**Programme lead:** Pedro Farinha
**Agent:** Claude Opus 4.7 (Cartographer persona)
**Pre-registration:** `DevelopmentGovernance/docs/dsr-iteration-3-robustness-validation.md`

---

## Inputs (immutable baselines)

| Repo | Tag / Branch | Commit | Date |
|---|---|---|---|
| `ExternalSourcesInventory` (substrate v6 baseline) | `substrate-v6-acr004-incorporated` | `ff28860` | 2026-05-05 |
| `sbd-toe-ontology` (V1.next) | `ontology-v1-next-acr004-promoted` (merged to main `6006e80`) | `b267cf3` | 2026-05-06 |
| `sbd-toe-ontology` (apparatus) | `apparatus-shacl-pyshacl-v3` | `58b1958` | 2026-05-06 |
| `sbd-toe-ontology` (embeddings) | `appsec-core-embeddings-v1.1` | `b948356` | 2026-05-05 |

NPZ verification: `embeddings-all-MiniLM-L6-v2-c9745ed1.npz` SHA256 `17f6aac4...23c8` ✅ matches across all stages.

## Pre-registered hypotheses

- **H1 (DEFAULT):** AppSec Core V1.next robust to AI/ML pressure per cross-tech-wave precedent.
- **H2 (sub-hypothesis):** Inverted-mapping methodology generalises from CWE/CAPEC to MITRE ATLAS without refinement. Falsifiable.
- **Outcomes A/B/C** with asymmetric burden of proof (immutable mid-iteration).

## Source corpus expansion

| Pilot (5 added) | Direction | Source artefact | Items | Lifted | GROUNDED |
|---|---|---|---:|---:|---:|
| `mitre_atlas` (REQUIRED) | problem-inverted | ATLAS v5.6.0 YAML | 278 | 329 | 180 (64.7%) |
| `owasp_llm_top_10` (REQUIRED) | solution-direct | LLM01-10:2025 HTML | 10 | 64 | 9 (90%) |
| `owasp_ml_top_10` | problem-inverted | ML01-10:2023 HTML | 10 | 23 | 9 (90%) |
| `nist_ai_100_2_e2025` | mixed | PDF taxonomy | 53 | 66 | 38 (71.7%) |
| `nist_ai_rmf_1_0` | mixed | PDF RMF | 53 | 68 | 31 (58.5%) |
| **iter-3 aggregate** | mixed | — | **404** | **550** | **267 (66.1%)** |

**ENISA AI 2024 DROPPED with caveat** — no discrete 2024 successor publication exists to ENISA Multilayer Framework 2023 (already in 26-source baseline corpus).

ACTIVE_SOURCES: 26 → **31**.

## Iteration timeline

| Date | Stage | Outcome |
|---|---|---|
| 2026-05-06 | Acks 1-4 + Stage 1 opening | Pre-registration confirmed |
| 2026-05-07 | Stage 1-3 (acquisition + lifting + quality dossier) | 4 PROCEED + 1 FLAG (OWASP LLM Top 10 atomicity 6.4) |
| 2026-05-07 | Joint-review #1 — FLAG resolution | PROCEED ratified (programme-lead + Orchestrator); single-pass option (X) ratified |
| 2026-05-07 | Stage 4-5 (grounding + substrate v7 emission) | SHACL ✅; GROUNDED 74.41% < 75.38% baseline ❌ → halt |
| 2026-05-08 | Joint-review #2 — HALT resolution | Regression accepted as corpus-expansion artifact (programme-lead + Orchestrator); substrate v7 ratified |
| 2026-05-08 | Stage 6 (FULL LDP analysis) | 988 LDP / 77 clusters / 27 STRONG (≥3 INDEPENDENT families) / 14 AI/ML-inflected |
| 2026-05-08 | Stage 7 (H2 decision) | **H2 CONFIRMED** — three independent signals support |
| 2026-05-08 | Stage 8 (evidence package) | this record |

## Substrate v7 termination evidence

| Gate | Required | Measured | Verdict | Joint-review (2026-05-08) |
|---|---|---|---|---|
| SHACL CONFORMS | 0 violations | 0 across M1' / M3 / M4 / M4-card / referential | ✅ PASS | accepted |
| GROUNDED ≥ 75.38% | ≥75.38% | 74.41% (2873/3861) | ❌ FAIL (-0.97pp) | ✅ ACCEPTED as corpus-expansion artifact |

**26 baseline sources reproduce v6 BIT-IDENTICALLY** (zero shift on existing items). Δ-0.97pp entirely from 5 iter-3 sources at structural-peer parity.

## Sub-hypothesis H2 — CONFIRMED

| Signal | Verdict |
|---|---|
| GROUNDED rate parity (ATLAS 64.7% vs CAPEC 63.5%; OWASP ML 90%) | ✅ Strong support |
| LDP top-1 adjacency parity (ATLAS ~0.32 ≈ CAPEC 0.319) | ✅ Parity confirmed |
| Cluster-level cross-corpus convergence (CID7-027 8-family ATLAS×CAPEC on TMR/TSV) | ✅ Strong support |

**No methodology refinement required.** MappingDirection enum (Decision 0003 Stage 2.5) + augmentation symmetry §F (Amendment 1) suffice for AI/ML problem-space-inverted sources.

Full reasoning: `data/p7_olir_audit/p7_v2_corrected/v7/reports/H2_INVERTED_MAPPING_DECISION.md`.

## LDP cluster analysis (Stage 6)

- 988 LDP items / 77 coarse clusters
- 27 STRONG (≥3 INDEPENDENT families per Iter-3 pre-registration)
- 14 AI/ML-inflected (≥1 iter-3 source)
- 0 STRONG-AI/ML clusters showing structural inadequacy (all absorb to existing Core entities at moderate adjacency 0.30-0.40)
- Hotspot CID7-027 (102 items / 8 families / 83% iter-3): adversarial-RE / model-stealing → ACO-TMR-005 + ACM-TSV-001 + ACO-TSV-006

Full analysis: `data/p7_olir_audit/p7_v2_corrected/v7/reports/LABDEPTHPENDING_ACR_ANALYSIS.md`.

## Cartographer-recommended Outcome — A (DEFAULT, prose only)

H1 preliminarily supported. Bounded thesis holds across web/mobile/cloud/microservices/containers/serverless/AI-ML — uniform discipline. AI/ML pressure absorbed by existing Core entities; cross-corpus convergence (CID7-027) confirms semantic alignment with traditional adversarial patterns.

Two pre-iteration hypotheses falsified positive:
- NIST AI RMF NOT governance-pathology (above EU regulatory peers +8 to +14pp)
- OWASP LLM Top 10 atomicity 6.4 NOT harming grounding (90% G with rich claim surface)

Both falsifications are publishable transparency for P6/P7 papers.

Joint-review participants for Stage 8 outcome decision: programme-lead Pedro Farinha + Orchestrator + Cartographer + Archon (Archon if Outcome B/C ratified).

## Outputs (Iteration 3 evidence base)

| Artefact | Path |
|---|---|
| Substrate v7 supplier | `data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json` |
| Substrate v7 manifest | `data/p7_olir_audit/p7_v2_corrected/v7/MANIFEST_v7_0.json` |
| Per-source contracts (×31) | `data/p7_olir_audit/p7_v2_corrected/v7/<source>/per_item_contract.json` |
| Process integrity report | `data/p7_olir_audit/p7_v2_corrected/v7/reports/PROCESS_INTEGRITY_REPORT.md` |
| LDP cluster analysis (Stage 6) | `data/p7_olir_audit/p7_v2_corrected/v7/reports/LABDEPTHPENDING_ACR_ANALYSIS.md` + `ldp_cluster_analysis.json` |
| H2 decision (Stage 7) | `data/p7_olir_audit/p7_v2_corrected/v7/reports/H2_INVERTED_MAPPING_DECISION.md` |
| Iteration 3 evidence brief (Stage 8) | `agentic/briefs/2026-05-08-iteration-3-evidence-package.md` |
| Substrate claims TTL | `data/p7_olir_audit/p7_v2_corrected/v7/reports/v7-substrate-claims.ttl` (181464 triples) |
| SHACL conformance report | `data/p7_olir_audit/p7_v2_corrected/v7/reports/v7-substrate-claims-shacl-report.{md,json}` (CONFORMS / 0 violations) |
| Calibration distribution | `data/p7_olir_audit/p7_v2_corrected/v7/reports/calibration_distribution.json` |
| Ontology side index | `data/p7_olir_audit/p7_v2_corrected/v7/reports/ontology_side_index.json` |
| Quality dossiers (×5) | `data/<pilot>/stubs/quality_dossier.json` + `data/p7_olir_audit/p7_v2_corrected/iteration_3/quality_dossier_aggregate.json` |
| Source object inventories (×5) | `data/<pilot>/stubs/source_object_inventory.json` |
| Pipeline drivers (5 added) | `scripts/v5_normalization/grounding/run_pipeline_v7.py` + `emit_substrate_v7_ttl.py` + `ldp_cluster_analysis_v7.py`; `scripts/v5_normalization/run_iteration_3_flatteners.py`; `scripts/extract_iteration_3_ai_ml_sources.py` |
| 5 new flatteners | `scripts/v5_normalization/flattening/{mitre_atlas,owasp_llm_top_10,owasp_ml_top_10,nist_ai_100_2_e2025,nist_ai_rmf_1_0}_flattener.py` |

## Tag proposal (programme-lead authority, pending Stage 8 ratification)

`substrate-v7-iter-3-ai-ml-incorporated` at the Stage 8 closing commit on branch `cartographer-iteration-3-ai-ml-expansion`.

If Cartographer-recommended Outcome A is ratified at Stage 8 → this tag becomes the **Cycle A frozen substrate**. Substrate v6 + v5 preserved as historical baselines.

## Pending Stage 8 joint-review decision

1. Outcome A / B / C ratification per pre-registered asymmetric burden of proof.
2. If A: prose reinforcement queued for Cycle B Iteration 2 (no ontology change).
3. Tag execution authority + push authorisation.
4. Cycle A frozen ceremony scheduling.

## Cross-references

- Pre-registration: `DevelopmentGovernance/docs/dsr-iteration-3-robustness-validation.md`
- Iteration 2 retrospective: `DevelopmentGovernance/docs/retrospective-2026-05-06-iteration-2-end.md`
- Cartographer dispatcher: `sbd-ai-runtime/handover/em-curso/2026-05-06-orchestrator-cartographer-iteration-3-source-acquisition.md`
- Stage 1/3/5 closes: `sbd-ai-runtime/handover/em-curso/2026-05-07-cartographer-iteration-3-stage-{1,3,5}-*.md`
- Stage 8 evidence brief: `agentic/briefs/2026-05-08-iteration-3-evidence-package.md`
- Programme-wide mirror: `sbd-ai-runtime/handover/em-curso/2026-05-08-cartographer-iteration-3-evidence-package.md`
