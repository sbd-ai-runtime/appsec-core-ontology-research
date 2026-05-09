# Cycle A Iteration 2 — Substrate v6 emission (2026-05-05)

**Status:** closed (substrate v6 emitted; all four termination gates pass; tag proposal pending programme-lead authority)
**Cycle / Iteration:** Cycle A / Iteration 2 (substrate-quality cycle, post-ACR-004 incorporation)
**Programme lead:** Pedro Farinha
**Agent:** Claude Opus 4.7 (Cartographer persona)

> **Note on convention:** the DSR-HISTORY README scopes per-round records to P2-v2 manual gap analysis (Phase 2). This record is kept here per dispatcher §"Three-file pattern" because the Iteration 2 termination is a formal milestone in the same iterative-refinement spirit, even though it precedes Phase 2 Manual gap analysis. Round-numbered files (`round-N-YYYY-MM-DD.md`) remain reserved for P2-v2 Phase 2.

---

## Inputs (tagged + branch state)

| Repo | Identifier | Commit | Date |
|---|---|---|---|
| `ExternalSourcesInventory` (substrate v5 baseline) | `cycle-a-iter-1-frozen-2026-05-04` | `e404b56` | 2026-05-04 |
| `sbd-toe-ontology` (V1.next + embeddings v1.1) | branch `acr004-output-rendering` | `c6f6059` | 2026-05-05 |
| Apparatus baseline (SHACL claim shapes used) | `apparatus-shacl-pyshacl-v2` | `ee73c19` | 2026-05-04 |

NPZ verification: `embeddings-all-MiniLM-L6-v2-c9745ed1.npz` SHA256 `17f6aac4...23c8` ✅ matches Archon close note. Corpus SHA256 `5951fd82...96c42` ✅ matches.

## Pipeline executed

1. `scripts/v5_normalization/grounding/run_pipeline_v6.py` — calibrated thresholds on cohort {SSDF, CIS, SAMM, CWE} at e2_pct=40 / e3_pct=60 against new (212-entity) ontology embedding space; grounded 26 sources from reused `data/.../v5/lifted/*.jsonl`; emitted SUPPLIER_v6_0.json + per-source contracts + ontology-side index + manifest + process integrity report. Pydantic invariants (P1' + M5 E2/E3) all pass; M1' by construction.
2. `scripts/v5_normalization/grounding/emit_substrate_v6_ttl.py` — emitted v6-substrate-claims.ttl (169758 triples).
3. `sbd-toe-ontology/scripts/consumer_conformance_validator.py` — pyshacl 0.31.0 / rdflib 7.6.0 against apparatus-v2 shapes (398 triples) + V1.next bounded ontology TTL (1824 triples).

## Outputs

| Artefact | Path | Count / notes |
|---|---|---|
| Substrate supplier | `data/p7_olir_audit/p7_v2_corrected/v6/SUPPLIER_v6_0.json` | 3457 items / 17507 claims |
| Substrate manifest | `data/p7_olir_audit/p7_v2_corrected/v6/MANIFEST_v6_0.json` | per-source + thresholds + ACR-004 incorporation block |
| Per-source contracts | `data/p7_olir_audit/p7_v2_corrected/v6/<source>/per_item_contract.json` | 26 files |
| Ontology-side index | `data/p7_olir_audit/p7_v2_corrected/v6/reports/ontology_side_index.json` | 200 targets reached |
| Calibration distribution | `data/p7_olir_audit/p7_v2_corrected/v6/reports/calibration_distribution.json` | per-level percentile evidence |
| Substrate claims TTL | `data/p7_olir_audit/p7_v2_corrected/v6/reports/v6-substrate-claims.ttl` | 169758 triples |
| SHACL conformance reports | `data/p7_olir_audit/p7_v2_corrected/v6/reports/v6-substrate-claims-shacl-report.{md,json}` | conforms=True / 0 violations |
| Process integrity report | `data/p7_olir_audit/p7_v2_corrected/v6/reports/PROCESS_INTEGRITY_REPORT.md` | full evidence |

## Termination gate results

| Gate | Required | Measured | Verdict |
|---|---|---|---|
| GROUNDED ≥ 74.6% | ≥74.6% | **75.38%** (2606 / 3457) | ✅ PASS |
| SHACL CONFORMS | 0 violations on M1' / M3 / M4 / M4-card / referential integrity | **0** across all 5 shapes | ✅ PASS |
| Cluster CID-26 collapse | partial-to-total | 30 v5-LDP items in CID-26 footprint → GROUNDED via ACR-004; 66 total v6 items carry ACR-004 claims (95.5% in 5-source footprint) | ✅ PASS |
| No other cluster regressions | top-N stable | top-15 entities ±2 claims drift; no shifts to ACR-004 from CID-25 / CID-55 / CID-8 / CID-46 | ✅ PASS |

**All four gates pass.**

## Substrate evolution v5 → v6

| Metric | v5 | v6 | Δ |
|---|---:|---:|---:|
| items | 3457 | 3457 | 0 |
| claims | 17446 | 17507 | +61 |
| GROUNDED | 2580 (74.63%) | 2606 (75.38%) | +26 |
| LDP | 877 | 851 | -26 |

## Decision (programme-lead)

**Pending.** Cartographer proposes tag `substrate-v6-acr004-incorporated` at the substrate v6 emission commit. Authority per Programme Preservation Protocol §7 Rule 6 — Cartographer proposes, programme-lead executes (and signs FREEZE-REGISTRY entry).

Substrate v5 remains canonical at tag `cycle-a-iter-1-frozen-2026-05-04` (immutable per Protocol §7 Rule 2). Substrate v6 supersedes for downstream consumption only after programme-lead tag execution.

## Archon-side regression flag

Archon's V1.next OWL/SHACL rebuild commit `7ee0373` regenerated `formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl` from scratch and stripped the 380-line consumer-conformance Claim shapes that `apparatus-shacl-pyshacl-v2` had consolidated. Substrate v6 SHACL gate completed via apparatus-v2 shapes restored from `ee73c19`; the regression itself is upstream of substrate v6 emission and does not invalidate it.

Recommendation: Archon to re-emit shapes with consumer-conformance consolidation re-applied, OR follow-up commit on `acr004-output-rendering` branch before merge. Programme-lead-controllable.

## Cross-references

- Substrate v6 brief: `agentic/briefs/2026-05-05-substrate-v6-acr004-incorporated.md`
- Process integrity report: `data/p7_olir_audit/p7_v2_corrected/v6/reports/PROCESS_INTEGRITY_REPORT.md`
- Programme-wide mirror: `sbd-ai-runtime/handover/em-curso/2026-05-05-cartographer-substrate-v6-emission-close.md`
- Upstream dispatchers: `sbd-ai-runtime/handover/em-curso/2026-05-05-orchestrator-cartographer-acr004-substrate-v6-prep.md` + `…-trigger-substrate-v6.md`
- Decision 0003 + Amendment 1: `agentic/decisions/0003-normalization-algorithm-redesign-2026-05-03.md` + `…-amendment-1-claims-not-chains.md`
