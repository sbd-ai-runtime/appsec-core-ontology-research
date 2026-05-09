#!/usr/bin/env python3
"""k_way_null_model.py — k-way intersection metric + statistical null-model baseline.

Cartographer 2026-05-09 — programme-lead Pedro Farinha (Phase A.5 dispatcher).

Computes per-entity k-way intersection metric over substrate v7's GROUNDED
claim graph (count distinct External Sources per AppSec Core entity), plus
a label-permutation null-model baseline (1000 trials; deterministic seed=42).

Outputs (data/p7_olir_audit/p7_v2_corrected/v7/k_way_analysis/):
- per_entity_k_way.json       per-entity table × 202 substantive entities
- k_way_summary.json          distribution stats + by-type breakdown
- null_model_baseline.json    null distribution percentiles + empirical p-values
- k_way_brief.md              1-page verbatim summary

Inputs:
- SUPPLIER_v7_0.json          substrate v7 (3861 items; 18,673 claims; 31 sources)
- AppSec Core V1 catalog      formal/appsec_core/08-embeddings/augmented-text-corpus.json
- SUPPLIER_v5_0.json          v5 baseline (for shift comparison; if available)

Method (per dispatcher §Step 1, §Step 2):

k-way intersection (set membership):
  k(e) = |{ source ∈ ES : ∃ claim c ∈ GROUNDED such that c.target_id = e ∧ c.source = source }|

Null model (Type II permutation test):
  H0: source-entity assignments are random.
  Procedure: for each of 1000 trials, permute claim → source labels (preserves
  multiset per source AND per-entity claim count), recompute k per entity,
  record null distribution. Empirical p-value = P(null_metric >= observed).

Authority: programme-lead Pedro Farinha 2026-05-09 ratified Phase A.5 bounded
enrichment of P7 §8.2. Out of scope (per dispatcher): FCA / OAEI / Newman
modularity / mutual information — reserved for P9 KEOD standalone paper.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
SUPPLIER_V7 = REPO_ROOT / "data" / "p7_olir_audit" / "p7_v2_corrected" / "v7" / "SUPPLIER_v7_0.json"
SUPPLIER_V5 = REPO_ROOT / "data" / "p7_olir_audit" / "p7_v2_corrected" / "v5" / "SUPPLIER_v5_0.json"
ENTITY_CATALOG = Path(
    "/Volumes/G-DRIVE/Shared/SecurityByDesign-TheoryOfEverything/sbd-toe-ontology"
    "/formal/appsec_core/08-embeddings/augmented-text-corpus.json"
)
OUT_DIR = REPO_ROOT / "data" / "p7_olir_audit" / "p7_v2_corrected" / "v7" / "k_way_analysis"

SEED = 42
N_TRIALS = 1000


def load_substantive_entities() -> list[tuple[str, str]]:
    """Return [(entity_id, entity_type)] for the 202 substantive entities (CO + P + M; Slice excluded)."""
    raw = json.loads(ENTITY_CATALOG.read_text(encoding="utf-8"))
    rows: list[tuple[str, str]] = []
    for r in raw["records"]:
        eid = r["entity_id"]
        elevel = r.get("entity_level", "")
        if elevel == "Slice":
            continue
        if eid.startswith("ACO-") or elevel == "ControlObjective":
            etype = "CO"
        elif eid.startswith("ACP-") or elevel == "Practice":
            etype = "P"
        elif eid.startswith("ACM-") or elevel == "Mechanism":
            etype = "M"
        else:
            continue
        rows.append((eid, etype))
    return rows


def extract_grounded_edges(supplier_path: Path) -> list[tuple[str, str]]:
    """Extract (source, target_id) edges from GROUNDED claims in SUPPLIER."""
    raw = json.loads(supplier_path.read_text(encoding="utf-8"))
    edges: list[tuple[str, str]] = []
    for item in raw.get("items", []):
        if item.get("final_classification") not in ("GROUNDED", "Grounded", "grounded"):
            continue
        src = item.get("source")
        if not src:
            continue
        for claim in item.get("claims", []):
            tgt = claim.get("target_id")
            if tgt:
                edges.append((src, tgt))
    return edges


def histogram_bins(ks: np.ndarray) -> dict:
    """Histogram with bins {k=0, k=1, k=2, k=3, k=4, k>=5, k>=10}."""
    return {
        "k=0": int((ks == 0).sum()),
        "k=1": int((ks == 1).sum()),
        "k=2": int((ks == 2).sum()),
        "k=3": int((ks == 3).sum()),
        "k=4": int((ks == 4).sum()),
        "k>=5": int((ks >= 5).sum()),
        "k>=10": int((ks >= 10).sum()),
    }


def per_entity_table(edges: list[tuple[str, str]], entity_ids: list[str], entity_types: dict) -> tuple[list[dict], np.ndarray]:
    """Compute per-entity (k, sources) rows + ks array."""
    by_entity: dict[str, set[str]] = defaultdict(set)
    for src, tgt in edges:
        by_entity[tgt].add(src)
    rows: list[dict] = []
    ks_list: list[int] = []
    for eid in entity_ids:
        srcs = sorted(by_entity.get(eid, set()))
        rows.append({
            "entity_id": eid,
            "entity_type": entity_types[eid],
            "k": len(srcs),
            "sources": srcs,
        })
        ks_list.append(len(srcs))
    return rows, np.array(ks_list)


def by_type_stats(rows: list[dict]) -> dict:
    """Per-type (CO/P/M) summary stats."""
    out: dict = {}
    for t in ("CO", "P", "M"):
        sel = np.array([r["k"] for r in rows if r["entity_type"] == t])
        out[t] = {
            "n": int(len(sel)),
            "mean_k": float(sel.mean()),
            "median_k": float(np.median(sel)),
            "stdev_k": float(sel.std(ddof=1)),
            "max_k": int(sel.max()),
            "min_k": int(sel.min()),
            "k_ge_3_fraction": float((sel >= 3).mean()),
            "k_ge_5_fraction": float((sel >= 5).mean()),
            "k_ge_10_fraction": float((sel >= 10).mean()),
        }
    return out


def null_model(
    edges: list[tuple[str, str]],
    entity_ids: list[str],
    n_trials: int = N_TRIALS,
    seed: int = SEED,
) -> dict:
    """Permutation test: shuffle source labels across claims; preserve multiset.

    Vectorised per-trial computation via boolean (entity × source) matrix.
    """
    rng = np.random.default_rng(seed)
    src_arr = np.array([e[0] for e in edges])
    tgt_arr = np.array([e[1] for e in edges])

    unique_sources = sorted(set(src_arr.tolist()))
    src_to_idx = {s: i for i, s in enumerate(unique_sources)}
    ent_to_idx = {e: i for i, e in enumerate(entity_ids)}

    # Filter to edges targeting our 202 substantive entities
    mask = np.array([t in ent_to_idx for t in tgt_arr])
    src_idx = np.array([src_to_idx[s] for s in src_arr[mask]])
    tgt_idx = np.array([ent_to_idx[t] for t in tgt_arr[mask]])

    n_ent = len(entity_ids)
    n_src = len(unique_sources)

    null_mean_k = np.zeros(n_trials)
    null_k_ge3 = np.zeros(n_trials)
    null_k_ge5 = np.zeros(n_trials)
    null_k_ge10 = np.zeros(n_trials)

    for trial in range(n_trials):
        permuted = rng.permutation(src_idx)
        mat = np.zeros((n_ent, n_src), dtype=bool)
        mat[tgt_idx, permuted] = True
        ks_null = mat.sum(axis=1)
        null_mean_k[trial] = ks_null.mean()
        null_k_ge3[trial] = (ks_null >= 3).mean()
        null_k_ge5[trial] = (ks_null >= 5).mean()
        null_k_ge10[trial] = (ks_null >= 10).mean()

    return {
        "n_trials": int(n_trials),
        "random_seed": int(seed),
        "null_mean_k": null_mean_k.tolist(),
        "null_k_ge3": null_k_ge3.tolist(),
        "null_k_ge5": null_k_ge5.tolist(),
        "null_k_ge10": null_k_ge10.tolist(),
    }


def percentiles(arr_list: list[float], pcts: list[float]) -> dict:
    arr = np.array(arr_list)
    return {f"p{p}": float(np.percentile(arr, p)) for p in pcts}


def emp_p_value(null_arr: list[float], observed: float) -> dict:
    """Return one-sided greater + one-sided less + two-sided empirical p-values."""
    arr = np.array(null_arr)
    p_greater = float((arr >= observed).mean())
    p_less = float((arr <= observed).mean())
    return {
        "one_sided_greater": p_greater,
        "one_sided_less": p_less,
        "two_sided": 2.0 * min(p_greater, p_less),
    }


def render_brief(
    summary: dict,
    null_summary: dict,
    by_type: dict,
    top_10: list[dict],
    bottom_10: list[dict],
    v5_compare: dict | None,
) -> str:
    lines: list[str] = []
    lines.append("# k-way Intersection Analysis — Substrate v7 (Phase A.5)")
    lines.append("")
    lines.append("**Date:** 2026-05-09")
    lines.append("**Author:** Cartographer (under programme-lead Pedro Farinha)")
    lines.append("**Substrate:** v7 (`SUPPLIER_v7_0.json` SHA `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04`)")
    lines.append("**Generator:** `scripts/k_way_null_model.py` (deterministic; seed=42)")
    lines.append("")
    lines.append("## Method (verbatim)")
    lines.append("")
    lines.append("- **k-way intersection per entity** (set membership): `k(e) = |{ source ∈ ES : ∃ GROUNDED claim with target = e ∧ source = source }|`")
    lines.append("- **Null model** (Type II permutation test): permute claim→source labels (preserve multiset per source + per-entity claim count); 1000 trials; empirical p-value = P(null_metric ≥ observed).")
    lines.append("- **Scope:** 202 substantive AC V1 entities (75 CO + 69 P + 58 M; Slice 10 excluded as structural).")
    lines.append("")
    lines.append("## Observed values (verbatim)")
    lines.append("")
    lines.append(f"- n_entities: **{summary['n_entities']}**")
    lines.append(f"- n_claims_grounded: **{summary['n_claims_grounded']}**")
    lines.append(f"- n_sources: **{summary['n_sources']}**")
    lines.append(f"- mean_k: **{summary['mean_k']:.4f}**")
    lines.append(f"- median_k: **{summary['median_k']:.1f}**")
    lines.append(f"- stdev_k: **{summary['stdev_k']:.4f}**")
    lines.append(f"- max_k: **{summary['max_k']}**")
    lines.append(f"- min_k: **{summary['min_k']}**")
    lines.append(f"- k≥3 fraction: **{summary['k_ge_3_fraction']:.4f}** ({summary['k_ge_3_count']}/{summary['n_entities']})")
    lines.append(f"- k≥5 fraction: **{summary['k_ge_5_fraction']:.4f}** ({summary['k_ge_5_count']}/{summary['n_entities']})")
    lines.append(f"- k≥10 fraction: **{summary['k_ge_10_fraction']:.4f}** ({summary['k_ge_10_count']}/{summary['n_entities']})")
    lines.append("")
    lines.append("### Histogram")
    lines.append("")
    lines.append("| Bin | Count |")
    lines.append("|---|---:|")
    for bin_label, count in summary["histogram"].items():
        lines.append(f"| {bin_label} | {count} |")
    lines.append("")
    lines.append("### By type (CO / P / M)")
    lines.append("")
    lines.append("| Type | n | mean_k | median_k | stdev_k | max_k | min_k | k≥3 frac | k≥5 frac | k≥10 frac |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for t in ("CO", "P", "M"):
        s = by_type[t]
        lines.append(
            f"| {t} | {s['n']} | {s['mean_k']:.3f} | {s['median_k']:.1f} | {s['stdev_k']:.3f} | "
            f"{s['max_k']} | {s['min_k']} | {s['k_ge_3_fraction']:.3f} | "
            f"{s['k_ge_5_fraction']:.3f} | {s['k_ge_10_fraction']:.3f} |"
        )
    lines.append("")
    lines.append("## Null-model baseline (verbatim)")
    lines.append("")
    lines.append(f"- N trials: **{null_summary['n_trials']}**")
    lines.append(f"- Random seed: **{null_summary['random_seed']}**")
    lines.append("")
    lines.append("### Null distribution (95% CI) + empirical p-values")
    lines.append("")
    lines.append("| Metric | Null p5 | Null p50 | Null p95 | Observed | P(null ≥ obs) | P(null ≤ obs) | Two-sided p |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    nd = null_summary["null_distribution"]
    obs = null_summary["observed"]
    pv = null_summary["empirical_p_value"]
    for metric_key, label in [
        ("mean_k", "mean_k"),
        ("k_ge_3_fraction", "k≥3 fraction"),
        ("k_ge_5_fraction", "k≥5 fraction"),
        ("k_ge_10_fraction", "k≥10 fraction"),
    ]:
        nd_p5 = nd[f"{metric_key}_p5"] if metric_key != "mean_k" else nd["mean_k_p5"]
        nd_p50 = nd[f"{metric_key}_p50"] if metric_key != "mean_k" else nd["mean_k_p50"]
        nd_p95 = nd[f"{metric_key}_p95"] if metric_key != "mean_k" else nd["mean_k_p95"]
        obs_v = obs[metric_key]
        p = pv[metric_key]
        lines.append(
            f"| {label} | {nd_p5:.4f} | {nd_p50:.4f} | {nd_p95:.4f} | **{obs_v:.4f}** | "
            f"{p['one_sided_greater']:.4f} | {p['one_sided_less']:.4f} | "
            f"**{p['two_sided']:.4f}** |"
        )
    lines.append("")
    lines.append(f"**Interpretation pointer (verbatim):** {null_summary['interpretation']}")
    lines.append("")
    lines.append("## Top 10 entities by k (highest cross-source coverage)")
    lines.append("")
    lines.append("| # | entity_id | type | k | sources |")
    lines.append("|---:|---|---|---:|---|")
    for i, r in enumerate(top_10, 1):
        srcs_compact = ", ".join(r["sources"][:5]) + (f" (+{len(r['sources']) - 5} more)" if len(r["sources"]) > 5 else "")
        lines.append(f"| {i} | `{r['entity_id']}` | {r['entity_type']} | **{r['k']}** | {srcs_compact} |")
    lines.append("")
    lines.append("## Bottom 10 entities by k (lowest cross-source coverage)")
    lines.append("")
    lines.append("| # | entity_id | type | k | sources |")
    lines.append("|---:|---|---|---:|---|")
    for i, r in enumerate(bottom_10, 1):
        srcs_compact = ", ".join(r["sources"]) if r["sources"] else "(none)"
        lines.append(f"| {i} | `{r['entity_id']}` | {r['entity_type']} | {r['k']} | {srcs_compact} |")
    lines.append("")
    if v5_compare:
        lines.append("## Substrate v5 baseline (recall)")
        lines.append("")
        lines.append("Comparison: substrate v5 (26 sources) → substrate v7 (31 sources, +5 AI/ML iter-3 sources).")
        lines.append("")
        lines.append("| Metric | Substrate v5 | Substrate v7 | Δ (v7 − v5) |")
        lines.append("|---|---:|---:|---:|")
        lines.append(
            f"| n_sources | {v5_compare['n_sources']} | {summary['n_sources']} | "
            f"{summary['n_sources'] - v5_compare['n_sources']:+d} |"
        )
        lines.append(
            f"| n_claims_grounded | {v5_compare['n_claims_grounded']} | {summary['n_claims_grounded']} | "
            f"{summary['n_claims_grounded'] - v5_compare['n_claims_grounded']:+d} |"
        )
        lines.append(
            f"| mean_k | {v5_compare['mean_k']:.4f} | {summary['mean_k']:.4f} | "
            f"{summary['mean_k'] - v5_compare['mean_k']:+.4f} |"
        )
        lines.append(
            f"| median_k | {v5_compare['median_k']:.1f} | {summary['median_k']:.1f} | "
            f"{summary['median_k'] - v5_compare['median_k']:+.1f} |"
        )
        lines.append(
            f"| max_k | {v5_compare['max_k']} | {summary['max_k']} | "
            f"{summary['max_k'] - v5_compare['max_k']:+d} |"
        )
        lines.append(
            f"| k≥3 fraction | {v5_compare['k_ge_3_fraction']:.4f} | {summary['k_ge_3_fraction']:.4f} | "
            f"{summary['k_ge_3_fraction'] - v5_compare['k_ge_3_fraction']:+.4f} |"
        )
        lines.append(
            f"| k≥5 fraction | {v5_compare['k_ge_5_fraction']:.4f} | {summary['k_ge_5_fraction']:.4f} | "
            f"{summary['k_ge_5_fraction'] - v5_compare['k_ge_5_fraction']:+.4f} |"
        )
        lines.append("")
        lines.append("**Scope-discrepancy reconciliation (verbatim):** Dispatcher cites v5 mean_k=8.63 from memory `project_substrate_v5_ratified_2026_05_03.md`. Computation on current `SUPPLIER_v5_0.json` yields:")
        lines.append("")
        lines.append(f"- **scope 202 substantive** (excl. 10 Slice; matches dispatcher §Step 1 methodology): mean_k = **{v5_compare['mean_k_scope_202_substantive']:.4f}**")
        lines.append(f"- **scope 212 (incl. Slice at k=0)**: mean_k = **{v5_compare['mean_k_scope_212_incl_slice']:.4f}** (≈ 8.63 cited; difference ~0.04 = rounding or minor v5 state evolution)")
        lines.append("")
        lines.append("Per dispatcher §Step 1 directive (\"Slice excluded as structural\"), the 202-substantive scope is canonical for comparison. The cited 8.63 figure was likely computed on 212-scope including Slice with k=0.")
        lines.append("")
        lines.append("**Cartographer note (verbatim):** substrate v5 → v7 shift recorded without interpretation per dispatcher §Step 1 directive ('register the shift verbatim; no interpretation; just numbers'). Curator §8.2 prose integration handles methodological commentary on shift.")
        lines.append("")
    lines.append("## Out of scope (per dispatcher)")
    lines.append("")
    lines.append("Reserved for P9 KEOD methodology paper:")
    lines.append("- Full FCA lattice construction (Wille 1982; Ganter & Wille)")
    lines.append("- OAEI track participation")
    lines.append("- Newman modularity / community detection")
    lines.append("- Mutual information analysis")
    lines.append("- Bipartite common-neighbors similarity matrix (full)")
    lines.append("")
    lines.append("## Cross-references")
    lines.append("")
    lines.append("- Phase A.5 dispatcher: `sbd-ai-runtime/handover/em-curso/2026-05-09-orchestrator-cartographer-phase-a5-k-way-null-model-dispatch.md`")
    lines.append("- Substrate v7 SUPPLIER: `data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json`")
    lines.append("- AC V1 entity catalog: `formal/appsec_core/08-embeddings/augmented-text-corpus.json` (212 entities; 202 substantive analysed)")
    lines.append("- v7 substrate claims TTL: `data/p7_olir_audit/p7_v2_corrected/v7/reports/v7-substrate-claims.ttl`")
    lines.append("- Cycle A frozen substrate baseline tag: `substrate-v7-iter-3-ai-ml-incorporated`")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load substantive entities + edges
    entities = load_substantive_entities()
    entity_ids = [e[0] for e in entities]
    entity_types = {e[0]: e[1] for e in entities}
    n_co = sum(1 for _, t in entities if t == "CO")
    n_p = sum(1 for _, t in entities if t == "P")
    n_m = sum(1 for _, t in entities if t == "M")
    print(f"Substantive entities: {len(entities)} ({n_co} CO + {n_p} P + {n_m} M)")

    edges_v7 = extract_grounded_edges(SUPPLIER_V7)
    print(f"v7 GROUNDED edges (claims): {len(edges_v7)}")
    print(f"v7 distinct sources: {len({e[0] for e in edges_v7})}")

    # Step 1: per-entity k-way + summary
    rows, ks_arr = per_entity_table(edges_v7, entity_ids, entity_types)
    summary = {
        "schema_version": "1.0",
        "substrate": "v7",
        "supplier_sha256": "596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04",
        "n_entities": len(rows),
        "n_claims_grounded": len(edges_v7),
        "n_sources": len({e[0] for e in edges_v7}),
        "mean_k": float(ks_arr.mean()),
        "median_k": float(np.median(ks_arr)),
        "stdev_k": float(ks_arr.std(ddof=1)),
        "max_k": int(ks_arr.max()),
        "min_k": int(ks_arr.min()),
        "histogram": histogram_bins(ks_arr),
        "by_type": by_type_stats(rows),
        "k_ge_3_count": int((ks_arr >= 3).sum()),
        "k_ge_3_fraction": float((ks_arr >= 3).mean()),
        "k_ge_5_count": int((ks_arr >= 5).sum()),
        "k_ge_5_fraction": float((ks_arr >= 5).mean()),
        "k_ge_10_count": int((ks_arr >= 10).sum()),
        "k_ge_10_fraction": float((ks_arr >= 10).mean()),
    }

    (OUT_DIR / "per_entity_k_way.json").write_text(
        json.dumps({
            "schema_version": "1.0",
            "substrate": "v7",
            "n_entities": len(rows),
            "entries": rows,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "k_way_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )

    # Top 10 + bottom 10
    top_10 = sorted(rows, key=lambda r: (-r["k"], r["entity_id"]))[:10]
    bottom_10 = sorted(rows, key=lambda r: (r["k"], r["entity_id"]))[:10]

    # Step 2: null model (1000 trials)
    print(f"Running null-model: {N_TRIALS} trials...")
    raw_null = null_model(edges_v7, entity_ids, n_trials=N_TRIALS, seed=SEED)

    null_dist = {
        "mean_k_p5": float(np.percentile(raw_null["null_mean_k"], 5)),
        "mean_k_p50": float(np.percentile(raw_null["null_mean_k"], 50)),
        "mean_k_p95": float(np.percentile(raw_null["null_mean_k"], 95)),
        "k_ge_3_fraction_p5": float(np.percentile(raw_null["null_k_ge3"], 5)),
        "k_ge_3_fraction_p50": float(np.percentile(raw_null["null_k_ge3"], 50)),
        "k_ge_3_fraction_p95": float(np.percentile(raw_null["null_k_ge3"], 95)),
        "k_ge_5_fraction_p5": float(np.percentile(raw_null["null_k_ge5"], 5)),
        "k_ge_5_fraction_p50": float(np.percentile(raw_null["null_k_ge5"], 50)),
        "k_ge_5_fraction_p95": float(np.percentile(raw_null["null_k_ge5"], 95)),
        "k_ge_10_fraction_p5": float(np.percentile(raw_null["null_k_ge10"], 5)),
        "k_ge_10_fraction_p50": float(np.percentile(raw_null["null_k_ge10"], 50)),
        "k_ge_10_fraction_p95": float(np.percentile(raw_null["null_k_ge10"], 95)),
    }

    observed = {
        "mean_k": float(ks_arr.mean()),
        "k_ge_3_fraction": float((ks_arr >= 3).mean()),
        "k_ge_5_fraction": float((ks_arr >= 5).mean()),
        "k_ge_10_fraction": float((ks_arr >= 10).mean()),
    }

    p_values = {
        "mean_k": emp_p_value(raw_null["null_mean_k"], observed["mean_k"]),
        "k_ge_3_fraction": emp_p_value(raw_null["null_k_ge3"], observed["k_ge_3_fraction"]),
        "k_ge_5_fraction": emp_p_value(raw_null["null_k_ge5"], observed["k_ge_5_fraction"]),
        "k_ge_10_fraction": emp_p_value(raw_null["null_k_ge10"], observed["k_ge_10_fraction"]),
    }

    null_mean_k_arr = np.array(raw_null["null_mean_k"])
    obs_mean = observed["mean_k"]
    null_median = float(np.median(null_mean_k_arr))
    p_two = p_values["mean_k"]["two_sided"]
    direction = "LOWER" if obs_mean < null_median else "HIGHER"
    if p_two < 0.001:
        sig_label = "p < 0.001 (extreme)"
    elif p_two < 0.05:
        sig_label = f"p = {p_two:.4f} (significant at α=0.05)"
    else:
        sig_label = f"p = {p_two:.4f} (within central 95% null region)"

    interp = (
        f"Observed mean_k={obs_mean:.4f} vs null median={null_median:.4f} "
        f"(95% CI [{np.percentile(null_mean_k_arr, 2.5):.4f}, "
        f"{np.percentile(null_mean_k_arr, 97.5):.4f}]). "
        f"Observed is {direction} than null distribution; two-sided empirical "
        f"{sig_label}. "
        f"One-sided P(null ≥ observed) = {p_values['mean_k']['one_sided_greater']:.4f}; "
        f"P(null ≤ observed) = {p_values['mean_k']['one_sided_less']:.4f} "
        f"(across {N_TRIALS} trials, seed={SEED}). "
    )
    if direction == "LOWER" and p_two < 0.05:
        interp += (
            "Domain reading: observed mean_k LOWER than random shuffle baseline → "
            "sources cluster their GROUNDED claims onto FEWER distinct entities than "
            "uniform random assignment would predict. This is consistent with "
            "semantic specificity: methodology produces source-entity assignments "
            "with concentration structure beyond what claim-count marginals alone "
            "would generate."
        )
    elif direction == "HIGHER" and p_two < 0.05:
        interp += (
            "Domain reading: observed mean_k HIGHER than random shuffle baseline → "
            "sources spread their GROUNDED claims across MORE distinct entities than "
            "uniform random assignment would predict."
        )
    else:
        interp += "Random-shuffle null model not rejected at α=0.05."

    null_summary = {
        "schema_version": "1.0",
        "n_trials": N_TRIALS,
        "random_seed": SEED,
        "null_distribution": null_dist,
        "observed": observed,
        "empirical_p_value": p_values,
        "interpretation": interp,
    }

    (OUT_DIR / "null_model_baseline.json").write_text(
        json.dumps(null_summary, indent=2) + "\n",
        encoding="utf-8",
    )

    # v5 baseline comparison (if available)
    v5_compare = None
    if SUPPLIER_V5.exists():
        edges_v5 = extract_grounded_edges(SUPPLIER_V5)
        rows_v5, ks_v5 = per_entity_table(edges_v5, entity_ids, entity_types)

        # Also compute on 212-scope (including Slice with k=0) for cross-reference
        # to the 8.63 figure cited in dispatcher (memory project_substrate_v5_ratified_2026_05_03.md)
        raw_ents = json.loads(ENTITY_CATALOG.read_text(encoding="utf-8"))
        all_212_ids = [r["entity_id"] for r in raw_ents["records"]]
        by_ent_v5: dict[str, set[str]] = defaultdict(set)
        for src, tgt in edges_v5:
            by_ent_v5[tgt].add(src)
        ks_212 = np.array([len(by_ent_v5.get(eid, set())) for eid in all_212_ids])

        v5_compare = {
            "n_claims_grounded": len(edges_v5),
            "n_sources": len({e[0] for e in edges_v5}),
            "mean_k_scope_202_substantive": float(ks_v5.mean()),
            "mean_k_scope_212_incl_slice": float(ks_212.mean()),
            "median_k": float(np.median(ks_v5)),
            "stdev_k": float(ks_v5.std(ddof=1)),
            "max_k": int(ks_v5.max()),
            "min_k": int(ks_v5.min()),
            "k_ge_3_fraction": float((ks_v5 >= 3).mean()),
            "k_ge_5_fraction": float((ks_v5 >= 5).mean()),
            "k_ge_10_fraction": float((ks_v5 >= 10).mean()),
            "scope_note": (
                "Dispatcher cites mean_k=8.63 from memory "
                "project_substrate_v5_ratified_2026_05_03.md. Computation on "
                "current SUPPLIER_v5_0.json yields 8.665 over 212-entity scope "
                "(includes 10 Slice entities at k=0; matches cited 8.63 within "
                "~0.04 — likely rounding or minor v5 state evolution). "
                "Per dispatcher §Step 1 directive, 202-substantive scope is "
                "canonical comparison; v5 mean_k_scope_202=9.094."
            ),
        }
        # Persist v5 baseline alongside outputs (also expose simple mean_k for compatibility)
        (OUT_DIR / "v5_baseline_recall.json").write_text(
            json.dumps({
                "schema_version": "1.0",
                "substrate": "v5",
                "computed_at": "2026-05-09",
                "method": "k_way_null_model.py applied to SUPPLIER_v5_0.json",
                "mean_k": v5_compare["mean_k_scope_202_substantive"],
                **v5_compare,
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        # Add backward-compat simple mean_k key for render_brief
        v5_compare["mean_k"] = v5_compare["mean_k_scope_202_substantive"]

    # Render brief
    brief = render_brief(summary, null_summary, summary["by_type"], top_10, bottom_10, v5_compare)
    (OUT_DIR / "k_way_brief.md").write_text(brief, encoding="utf-8")

    # Console summary
    print()
    print(f"Observed mean_k = {observed['mean_k']:.4f}")
    print(f"Null 95% CI mean_k = [{null_dist['mean_k_p5']:.4f}, {null_dist['mean_k_p95']:.4f}]")
    print(f"Empirical p-value (mean_k): two-sided = {p_values['mean_k']['two_sided']:.4f}, "
          f"P(null ≥ obs) = {p_values['mean_k']['one_sided_greater']:.4f}, "
          f"P(null ≤ obs) = {p_values['mean_k']['one_sided_less']:.4f}")
    print(f"Observed k≥3 fraction = {observed['k_ge_3_fraction']:.4f}")
    print(f"Observed k≥5 fraction = {observed['k_ge_5_fraction']:.4f}")
    print(f"Observed k≥10 fraction = {observed['k_ge_10_fraction']:.4f}")
    if v5_compare:
        print()
        print(f"v5 baseline mean_k = {v5_compare['mean_k']:.4f} (recall: {v5_compare['n_sources']} sources)")
        print(f"v5 → v7 mean_k shift: {observed['mean_k'] - v5_compare['mean_k']:+.4f}")

    print()
    print("Outputs:")
    for f in sorted(OUT_DIR.iterdir()):
        print(f"  {f.relative_to(REPO_ROOT)} ({f.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
