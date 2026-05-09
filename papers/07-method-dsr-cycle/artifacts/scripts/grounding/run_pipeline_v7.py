"""Substrate v7 driver — Cycle A Iteration 3 AI/ML expanded corpus re-grounding.

Runs PIPELINE 2 against the 31-source ACTIVE_SOURCES (26 baseline + 5 AI/ML
new) and AppSec Core V1.next + appsec-core-embeddings-v1.1 (212 entities).

Same model + revision + lib versions as substrate v6 baseline per Decision
0003 Amendment 1 §F (env-determinism mirror): sentence-transformers
all-MiniLM-L6-v2 @ HF revision c9745ed1; transformers 4.57.1 / torch 2.2.2 /
numpy 1.24.4; Darwin x86_64 / Python 3.10.1.

Inputs:
  data/p7_olir_audit/p7_v2_corrected/v5/lifted/<source>_lifted.jsonl  (×31)
  /Volumes/G-DRIVE/Shared/.../sbd-toe-ontology/formal/appsec_core/08-embeddings/
    embeddings-all-MiniLM-L6-v2-c9745ed1.npz  (SHA 17f6aac4...; 212 entities)

Outputs (substrate v7):
  data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json
  data/p7_olir_audit/p7_v2_corrected/v7/MANIFEST_v7_0.json
  data/p7_olir_audit/p7_v2_corrected/v7/<source>/per_item_contract.json (×31)
  data/p7_olir_audit/p7_v2_corrected/v7/reports/ontology_side_index.json
  data/p7_olir_audit/p7_v2_corrected/v7/reports/calibration_distribution.json
  data/p7_olir_audit/p7_v2_corrected/v7/reports/PROCESS_INTEGRITY_REPORT.md

Joint-review FLAG resolution caveat (programme-lead 2026-05-07):
  owasp_llm_top_10 atomicity 6.4 = structural intentional bundling, NOT
  pathology. Source PROCEEDS via single-pass substrate emission.
"""
from __future__ import annotations
import datetime as _dt
import json
import pathlib
import sys
from collections import defaultdict

from scripts.v5_normalization.grounding.encode import (
    load_ontology_embeddings,
    MODEL_ID,
    MODEL_REVISION,
)
from scripts.v5_normalization.grounding.calibrate_thresholds import (
    collect_score_stats,
    choose_thresholds,
    percentiles,
    CALIBRATION_COHORT,
)
from scripts.v5_normalization.grounding.score import TARGET_LEVELS
from scripts.v5_normalization.grounding.pydantic_schemas import (
    Substrate,
    SubstrateMeta,
    Claim,
)
from scripts.v5_normalization.configs.source_configs import ACTIVE_SOURCES

import scripts.v5_normalization.grounding.run_pipeline_2 as p2


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
LIFTED_DIR = REPO_ROOT / "data/p7_olir_audit/p7_v2_corrected/v5/lifted"
V7_OUT = REPO_ROOT / "data/p7_olir_audit/p7_v2_corrected/v7"
REPORTS = V7_OUT / "reports"

SUBSTRATE_VERSION = "v7.0"
BRANCH_LABEL = "cartographer-iteration-3-ai-ml-expansion"
ONTOLOGY_TAG = "ontology-v1-next-acr004-promoted"
APPARATUS_TAG = "apparatus-shacl-pyshacl-v3"
EMBEDDINGS_TAG = "appsec-core-embeddings-v1.1"
SUBSTRATE_BASELINE_TAG = "substrate-v6-acr004-incorporated"
GROUNDED_BASELINE = 0.7538  # substrate v6 = 75.38%

# Iteration 3 AI/ML new pilots (5)
ITERATION_3_PILOTS = (
    "mitre_atlas",
    "owasp_llm_top_10",
    "owasp_ml_top_10",
    "nist_ai_100_2_e2025",
    "nist_ai_rmf_1_0",
)


def load_lifted(source: str) -> list[dict]:
    p = LIFTED_DIR / f"{source}_lifted.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.open()]


def main():
    p2.LIFTED_DIR = LIFTED_DIR
    p2.V5_OUT = V7_OUT
    p2.REPORTS = REPORTS

    print(f"[pipeline_v7] {len(ACTIVE_SOURCES)} ACTIVE_SOURCES (26 baseline + 5 Iteration 3)", file=sys.stderr)
    print("[pipeline_v7] loading ontology embeddings (V1.next, 212 entities)...", file=sys.stderr)
    ont = load_ontology_embeddings()
    n_ont = len(ont["entity_iris"])
    print(f"[pipeline_v7] ontology embeddings loaded: {n_ont} entities", file=sys.stderr)

    print("[pipeline_v7] calibrating thresholds on cohort...", file=sys.stderr)
    stats = collect_score_stats(CALIBRATION_COHORT)
    chosen = choose_thresholds(stats, e2_pct=40, e3_pct=60)
    e2 = chosen["e2_per_level"]
    e3 = chosen["e3_per_level"]
    print(f"[pipeline_v7] E2 per level: {e2}", file=sys.stderr)
    print(f"[pipeline_v7] E3 per level: {e3}", file=sys.stderr)

    REPORTS.mkdir(parents=True, exist_ok=True)
    cal_distribution = {
        "cohort": list(CALIBRATION_COHORT),
        "n_rows_per_source": stats["n_rows_per_source"],
        "global_top1_distribution_by_level": {
            level: percentiles(stats["global_top1_by_level"].get(level, []))
            for level in TARGET_LEVELS
        },
        "margin_distribution_by_level": {
            level: percentiles(stats["margin_by_level"].get(level, []))
            for level in TARGET_LEVELS
        },
        "chosen_thresholds": chosen,
    }
    (REPORTS / "calibration_distribution.json").write_text(json.dumps(cal_distribution, indent=2))

    all_items = []
    all_claims: list[Claim] = []
    flattener_version_observed: list[str] = []
    per_source_summary: list[dict] = []
    per_source_items: dict[str, list] = {}

    for source in ACTIVE_SOURCES:
        rows = load_lifted(source)
        if not rows:
            print(f"[pipeline_v7] {source}: no lifted rows", file=sys.stderr)
            continue
        items, claims = p2._ground_one_source(
            source, rows, ont, e2, e3, flattener_version_observed
        )
        all_items.extend(items)
        all_claims.extend(claims)
        per_source_items[source] = items

        n_grounded = sum(1 for it in items if it.final_classification == "GROUNDED")
        n_lab = sum(1 for it in items if it.final_classification == "LabDepthPending")
        n_oos = sum(1 for it in items if it.final_classification == "OOS_AppSec")
        n_claims_src = sum(len(it.claims) for it in items)
        level_counts: dict[str, int] = defaultdict(int)
        for cl in claims:
            level_counts[cl.level] += 1
        entities_reached = len({cl.target_core_entity for cl in claims})
        per_source_summary.append({
            "source": source,
            "is_iteration_3_pilot": source in ITERATION_3_PILOTS,
            "n_lifted_rows": len(rows),
            "n_items": len(items),
            "n_grounded": n_grounded,
            "n_lab_depth_pending": n_lab,
            "n_oos": n_oos,
            "n_claims_emitted": n_claims_src,
            "claim_emission_ratio": round(n_claims_src / max(1, len(rows)), 3),
            "atomicity_ratio": round(len(rows) / max(1, len(items)), 3),
            "distinct_core_entities_reached": entities_reached,
            "claims_by_level": dict(level_counts),
        })
        marker = " [iter-3]" if source in ITERATION_3_PILOTS else ""
        print(
            f"[pipeline_v7] {source}{marker}: {len(items)} items, {n_grounded}G/{n_lab}L/{n_oos}O, "
            f"{n_claims_src} claims, {entities_reached} entities",
            file=sys.stderr,
        )

    flatv = sorted(set(flattener_version_observed))
    flat_v = flatv[0] if len(flatv) == 1 else "mixed"
    version_str = flat_v.split("_v")[-1] if "_v" in flat_v else flat_v

    meta = SubstrateMeta(
        flattener_version=f"v{version_str}",
        grounding_model=MODEL_ID,
        grounding_model_revision=MODEL_REVISION,
        e2_per_level=e2,
        e3_per_level=e3,
        calibration_cohort=list(CALIBRATION_COHORT),
        n_active_sources=len(ACTIVE_SOURCES),
        n_lifted_rows_total=sum(s["n_lifted_rows"] for s in per_source_summary),
        n_items_total=len(all_items),
        n_claims_total=len(all_claims),
        n_grounded=sum(1 for it in all_items if it.final_classification == "GROUNDED"),
        n_lab_depth_pending=sum(1 for it in all_items if it.final_classification == "LabDepthPending"),
        n_oos=sum(1 for it in all_items if it.final_classification == "OOS_AppSec"),
        generated_at=_dt.datetime.now(_dt.timezone.utc).isoformat(),
    )

    for it in all_items:
        if it.final_classification == "GROUNDED":
            assert len(it.claims) >= 1, f"P1' violation: {it.item_id}"
            for cl in it.claims:
                assert cl.similarity_score >= e2[cl.level], f"M5 E2 violation: {cl.claim_id}"
                assert cl.disambiguation_margin >= e3[cl.level], f"M5 E3 violation: {cl.claim_id}"
    print(
        f"[pipeline_v7] all {len(all_items)} items + {len(all_claims)} claims pass invariant checks",
        file=sys.stderr,
    )

    onto_index = p2._build_ontology_side_index(all_claims)

    V7_OUT.mkdir(parents=True, exist_ok=True)
    substrate = Substrate(meta=meta, items=all_items)
    supplier_path = V7_OUT / "SUPPLIER_v7_0.json"
    supplier_path.write_text(substrate.model_dump_json(indent=2))
    print(f"[write] {supplier_path}", file=sys.stderr)

    for source, items in per_source_items.items():
        src_dir = V7_OUT / source
        src_dir.mkdir(parents=True, exist_ok=True)
        contract = {
            "schema": "appsec_core_v7_per_item_contract/1.0",
            "source": source,
            "is_iteration_3_pilot": source in ITERATION_3_PILOTS,
            "n_items": len(items),
            "items": [it.model_dump() for it in items],
        }
        (src_dir / "per_item_contract.json").write_text(json.dumps(contract, indent=2))

    grounded_pct = (meta.n_grounded / max(1, meta.n_items_total)) * 100.0
    grounded_baseline_pct = GROUNDED_BASELINE * 100.0

    manifest = {
        "schema": "v7_manifest/1.0",
        "supplier_version": SUBSTRATE_VERSION,
        "generated_at": meta.generated_at,
        "branch": BRANCH_LABEL,
        "iteration": "Cycle A Iteration 3",
        "iteration_authority": "programme-lead Pedro Farinha 2026-05-06",
        "ontology_tag": ONTOLOGY_TAG,
        "apparatus_tag": APPARATUS_TAG,
        "embeddings_tag": EMBEDDINGS_TAG,
        "substrate_baseline_tag": SUBSTRATE_BASELINE_TAG,
        "ontology_npz_sha256": "17f6aac496b9896dae977a83745480322e1594a214bd9aa7b905f2cf9ddf23c8",
        "ontology_corpus_sha256": "5951fd82e4b7547b37989af5b2f403ff3fd5e8b484b760ce4c565a6756b96c42",
        "ontology_n_entities": n_ont,
        "active_sources": list(ACTIVE_SOURCES),
        "n_active_sources": meta.n_active_sources,
        "n_lifted_rows_total": meta.n_lifted_rows_total,
        "n_items_total": meta.n_items_total,
        "n_claims_total": meta.n_claims_total,
        "classifications": {
            "GROUNDED": meta.n_grounded,
            "LabDepthPending": meta.n_lab_depth_pending,
            "OOS_AppSec": meta.n_oos,
        },
        "per_source_summary": per_source_summary,
        "grounding": {
            "model": meta.grounding_model,
            "model_revision": meta.grounding_model_revision,
            "e2_per_level": meta.e2_per_level,
            "e3_per_level": meta.e3_per_level,
            "calibration_cohort": meta.calibration_cohort,
        },
        "termination_gates": {
            "grounded_rate": {
                "measured": round(grounded_pct, 4),
                "baseline": grounded_baseline_pct,
                "verdict": "PASS" if grounded_pct >= grounded_baseline_pct else "FAIL",
            },
            "shacl_conforms": "to_verify_externally_via_consumer_conformance_validator",
        },
        "iteration_3_caveats": {
            "owasp_llm_top_10": {
                "atomicity_ratio_at_pipeline_1": 6.4,
                "flag": "HIGH_DECOMPOSITION_RATIO",
                "joint_review_resolution": "PROCEED — atomicity 6.4 reflects intentional editorial bundling (Description + Common Examples + Prevention Strategies per LLMNN page); structurally correct, semantically benign. Programme-lead Pedro Farinha + Orchestrator ratification 2026-05-07.",
                "duplicate_fraction": 0.0,
                "governance_fraction": 0.031,
                "evidence_path": "data/owasp_llm_top_10/stubs/quality_dossier.json",
            },
            "enisa_ai_2024_dropped": {
                "reason": "no discrete 2024 successor publication exists to ENISA Multilayer Framework 2023 (already in 26-source corpus)",
                "iteration_3_corpus_actual": "5 sources added (not 6)",
            },
            "nist_ai_rmf_governance_surprise": {
                "pre_iteration_hypothesis": "RMF expected governance-heavy pathology",
                "stage_3_finding": "RMF governance fraction = 19% (under 40% threshold); falsified at Stage 3",
                "deferred_to_stage_6": "lifted-concern fraction final assessment in LDP analysis post-grounding",
            },
        },
        "h2_test_surfaces": {
            "primary": "mitre_atlas",
            "secondary": "owasp_ml_top_10",
            "decision_pending": "Stage 7 sub-hypothesis evaluation",
        },
    }
    (V7_OUT / "MANIFEST_v7_0.json").write_text(json.dumps(manifest, indent=2))
    print(f"[write] {V7_OUT / 'MANIFEST_v7_0.json'}", file=sys.stderr)

    (REPORTS / "ontology_side_index.json").write_text(
        json.dumps([o.model_dump() for o in onto_index], indent=2)
    )
    print(f"[write] {REPORTS / 'ontology_side_index.json'}", file=sys.stderr)

    # Process integrity report
    report_lines = [
        f"# Substrate v7 — Process Integrity Report (Iteration 3 AI/ML expansion)\n",
        f"**Generated:** {meta.generated_at}",
        f"**Branch (ESI):** {BRANCH_LABEL}",
        f"**Iteration:** Cycle A Iteration 3",
        f"**Substrate baseline:** {SUBSTRATE_BASELINE_TAG} (= ff28860; substrate v6)",
        f"**Ontology:** {ONTOLOGY_TAG} (V1.next, 212 entities)",
        f"**Apparatus:** {APPARATUS_TAG} (composition, 11 shapes)",
        f"**Embeddings:** {EMBEDDINGS_TAG} (NPZ SHA 17f6aac4...23c8 verified)",
        "",
        "## Aggregate counts",
        "",
        f"- **Items total:** {meta.n_items_total}",
        f"- **Claims total:** {len(all_claims)}",
        f"- **GROUNDED:** {meta.n_grounded} ({grounded_pct:.2f}%)",
        f"- **LabDepthPending:** {meta.n_lab_depth_pending}",
        f"- **OOS_AppSec:** {meta.n_oos}",
        f"- **ACTIVE_SOURCES:** {meta.n_active_sources} (= 26 baseline + 5 Iteration 3)",
        "",
        "## Termination gate (Iteration 3)",
        "",
        f"- **GROUNDED ≥ {grounded_baseline_pct:.2f}% (substrate v6 baseline):** "
        f"{'PASS ✅' if grounded_pct >= grounded_baseline_pct else 'FAIL ❌'} "
        f"(measured {grounded_pct:.2f}%, Δ {grounded_pct - grounded_baseline_pct:+.2f}pp)",
        "- **SHACL CONFORMS:** verify externally via consumer_conformance_validator.py against apparatus-shacl-pyshacl-v3 composition",
        "",
        "## Iteration 3 new pilots (5)",
        "",
    ]
    for s in per_source_summary:
        if s["is_iteration_3_pilot"]:
            g_pct = s["n_grounded"] / max(1, s["n_items"]) * 100
            report_lines.append(
                f"- **{s['source']}**: {s['n_items']} items / {s['n_grounded']}G ({g_pct:.1f}%) / {s['n_claims_emitted']} claims / {s['distinct_core_entities_reached']} entities reached"
            )
    report_lines.extend([
        "",
        "## Calibration thresholds (e2_pct=40 / e3_pct=60; cohort SSDF + CIS + SAMM + CWE)",
        "",
        f"- **E2 per level:**",
    ])
    for lvl in TARGET_LEVELS:
        report_lines.append(f"  - {lvl}: {e2[lvl]:.4f}")
    report_lines.append("- **E3 per level:**")
    for lvl in TARGET_LEVELS:
        report_lines.append(f"  - {lvl}: {e3[lvl]:.4f}")
    report_lines.extend([
        "",
        "## Caveats (Iteration 3)",
        "",
        "- **owasp_llm_top_10 atomicity 6.4:** ratified PROCEED 2026-05-07 by programme-lead + Orchestrator; structural intentional bundling, NOT pathology.",
        "- **enisa_ai_2024 DROPPED:** no discrete 2024 successor exists to ENISA Multilayer Framework 2023.",
        "- **nist_ai_rmf governance surprise:** Stage 3 dossier governance-fraction 19% (under 40% threshold); pre-iteration hypothesis falsified; final lifted-concern assessment deferred to Stage 6 LDP analysis.",
        "",
        "## Stages 6 + 7 + 8 next",
        "",
        "- Stage 6 — FULL LDP analysis recomputation (cluster identification + ACR-candidacy lens; AI/ML cluster isolation)",
        "- Stage 7 — H2 sub-hypothesis decision (inverted-mapping methodology on ATLAS + OWASP ML Top 10)",
        "- Stage 8 — Joint review evidence package for Outcome A/B/C decision",
    ])
    (REPORTS / "PROCESS_INTEGRITY_REPORT.md").write_text("\n".join(report_lines))
    print(f"[write] {REPORTS / 'PROCESS_INTEGRITY_REPORT.md'}", file=sys.stderr)

    print(
        f"\n[pipeline_v7] DONE — {meta.n_items_total} items / {len(all_claims)} claims / "
        f"GROUNDED {grounded_pct:.2f}% (baseline {grounded_baseline_pct:.2f}%)",
        file=sys.stderr,
    )
    print(
        f"[pipeline_v7] gate verdict: {'PASS ✅' if grounded_pct >= grounded_baseline_pct else 'FAIL ❌'}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
