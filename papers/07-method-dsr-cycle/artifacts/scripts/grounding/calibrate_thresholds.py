"""Empirical calibration of E2 (admissibility) and E3 (disambiguation margin).

Per Decision 0003 Amendment 1 §B + §4: calibrate on cohort SSDF + CIS + SAMM + CWE
(four shape classes from Phase 0 audit). Thresholds fixed thereafter and applied
to remaining 22 sources.

Approach (deterministic, no ground truth):
  1. Load lifted rows from cohort sources.
  2. Encode contextualised_text with the pinned SBERT.
  3. Cosine vs ontology embeddings → top-K candidates per row.
  4. Per level (CO / Practice / Mechanism): collect top-1 scores; compute the
     20th, 30th, 40th, 50th percentiles of the top-1 score distribution.
  5. Per level: collect (top-1 - top-2-within-same-(slice,level)) margins;
     compute the same percentiles.
  6. Choose E2 = some percentile (recommendation: 30th — admit 70% of top-1
     scores, reject only the bottom 30% as too weak).
  7. Choose E3 = some percentile of margins (recommendation: 30th — emit only
     when the gap to next-best in same (slice, level) is above threshold).

Output:
  agentic/decisions/0003-normalization-algorithm-redesign-2026-05-03-amendment-1-appendix-thresholds.md
  reports/calibration_distribution.json (per-level histograms for paper §11)
"""
from __future__ import annotations
import json
import pathlib
from collections import defaultdict

import numpy as np

from scripts.v5_normalization.grounding.encode import encode_texts, load_ontology_embeddings
from scripts.v5_normalization.grounding.score import (
    cosine_scores,
    candidates_for_row,
    TARGET_LEVELS,
)


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
LIFTED_DIR = REPO_ROOT / "data/p7_olir_audit/p7_v2_corrected/v5/lifted"
REPORTS_DIR = REPO_ROOT / "data/p7_olir_audit/p7_v2_corrected/v5/reports"

CALIBRATION_COHORT = (
    "ssdf_sp800_218_v1_1",
    "cis_controls_v8_1_2",
    "owasp_samm_v2_1",
    "cwe_software_development_view_v4_19_1",
)


def load_lifted(source: str) -> list[dict]:
    p = LIFTED_DIR / f"{source}_lifted.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.open()]


def collect_score_stats(cohort: tuple[str, ...] = CALIBRATION_COHORT) -> dict:
    """Run cohort through encoder + cosine; collect two distributions per level:
      - global-top-1 per row (best pool's top-1 across all 10 slices) → calibrates E2.
      - within-(slice,level) margin (top-1 minus top-2 in the SAME pool) → calibrates E3.

    The first answers "what does a credible best match look like for this row?";
    the second answers "what gap separates a confident pick from an ambiguous one?".
    """
    ont = load_ontology_embeddings()
    ont_emb = ont["embeddings"]

    # Filter ontology to TARGET_LEVELS only (199 entities).
    ont_levels = ont["entity_levels"]
    keep_idx = [i for i, lvl in enumerate(ont_levels) if str(lvl) in TARGET_LEVELS]
    ont_emb_filt = ont_emb[keep_idx]
    ont_levels_filt = ont_levels[keep_idx]
    ont_iris_filt = ont["entity_iris"][keep_idx]
    ont_ids_filt = ont["entity_ids"][keep_idx]
    ont_fams_filt = ont["families"][keep_idx]

    # E2 distribution: global top-1 per (row, level), best pool wins.
    global_top1_by_level: dict[str, list[float]] = defaultdict(list)
    # E3 distribution: within-(slice,level) margin, all (slice,level) tuples per row.
    margin_by_level: dict[str, list[float]] = defaultdict(list)
    n_rows_per_source: dict[str, int] = {}

    for src in cohort:
        rows = load_lifted(src)
        n_rows_per_source[src] = len(rows)
        if not rows:
            continue
        texts = [r["contextualised_text"] for r in rows]
        src_emb = encode_texts(texts)
        sims = cosine_scores(src_emb, ont_emb_filt)  # (N_src, N_ont_filt)

        for i in range(len(rows)):
            # E2: per level, the GLOBAL maximum score for this row across all
            # entities of that level (= best pool's top-1 in that level).
            for level in TARGET_LEVELS:
                mask = (ont_levels_filt == level)
                if not mask.any():
                    continue
                level_max = float(sims[i][mask].max())
                global_top1_by_level[level].append(level_max)

            # E3: per (slice, level) pool, compute top-1 minus top-2 margin
            # for every pool that has at least one candidate.
            by_tuple: dict[tuple[str, str], list] = defaultdict(list)
            for j in range(len(sims[i])):
                lvl = str(ont_levels_filt[j])
                slice_f = str(ont_fams_filt[j])
                by_tuple[(slice_f, lvl)].append(float(sims[i][j]))
            for (slice_f, level), scores in by_tuple.items():
                scores.sort(reverse=True)
                top1 = scores[0]
                next_ = scores[1] if len(scores) >= 2 else 0.0
                margin_by_level[level].append(top1 - next_)

    return {
        "n_rows_per_source": n_rows_per_source,
        "global_top1_by_level": {k: list(v) for k, v in global_top1_by_level.items()},
        "margin_by_level": {k: list(v) for k, v in margin_by_level.items()},
    }


def percentiles(arr: list[float]) -> dict[str, float]:
    if not arr:
        return {}
    a = np.array(arr)
    return {
        "n": int(len(a)),
        "min": float(a.min()),
        "p10": float(np.percentile(a, 10)),
        "p20": float(np.percentile(a, 20)),
        "p30": float(np.percentile(a, 30)),
        "p40": float(np.percentile(a, 40)),
        "p50": float(np.percentile(a, 50)),
        "p60": float(np.percentile(a, 60)),
        "p70": float(np.percentile(a, 70)),
        "p80": float(np.percentile(a, 80)),
        "p90": float(np.percentile(a, 90)),
        "max": float(a.max()),
        "mean": float(a.mean()),
        "std": float(a.std()),
    }


def choose_thresholds(stats: dict, e2_pct: int = 25, e3_pct: int = 30) -> dict:
    """Pick E2 (admissibility per level) and E3 (disambiguation per level).

    e2_pct: percentile of GLOBAL top-1 per row distribution (per level).
            E2 = p25 admits 75% of rows that have at least one credible match
            at that level; rejects rows whose best match in that level is in
            the bottom 25% (likely noise).

    e3_pct: percentile of within-(slice,level) margin distribution (per level).
            E3 = p30 requires the chosen pool's top-1 to exceed its top-2 by
            at least the 30th-percentile gap — rejects ambiguous pool picks
            (the bottom 30% of within-pool gaps).

    Both percentiles are programme-lead-controllable parameters; documented in
    the thresholds appendix.
    """
    e2 = {}
    e3 = {}
    for level in TARGET_LEVELS:
        top1_arr = stats["global_top1_by_level"].get(level, [])
        margin_arr = stats["margin_by_level"].get(level, [])
        e2[level] = float(np.percentile(top1_arr, e2_pct)) if top1_arr else 0.0
        e3[level] = float(np.percentile(margin_arr, e3_pct)) if margin_arr else 0.0
    return {"e2_per_level": e2, "e3_per_level": e3, "e2_pct": e2_pct, "e3_pct": e3_pct}


def main():
    print(f"[calibrate] cohort: {CALIBRATION_COHORT}", flush=True)
    stats = collect_score_stats(CALIBRATION_COHORT)
    print(f"[calibrate] rows per source: {stats['n_rows_per_source']}", flush=True)

    # Per-level distribution stats
    distribution = {
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
    }

    chosen = choose_thresholds(stats, e2_pct=40, e3_pct=60)

    distribution["chosen_thresholds"] = chosen

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REPORTS_DIR / "calibration_distribution.json"
    with out_path.open("w") as f:
        json.dump(distribution, f, indent=2)
    print(f"[calibrate] wrote {out_path}", flush=True)

    print("\n=== Chosen thresholds ===")
    print(f"E2 (admissibility, p{chosen['e2_pct']} of top-1 score):")
    for lvl in TARGET_LEVELS:
        print(f"  {lvl}: {chosen['e2_per_level'][lvl]:.4f}")
    print(f"E3 (disambiguation, p{chosen['e3_pct']} of within-(slice,level) margin):")
    for lvl in TARGET_LEVELS:
        print(f"  {lvl}: {chosen['e3_per_level'][lvl]:.4f}")

    return chosen


if __name__ == "__main__":
    main()
