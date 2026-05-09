"""SSDF cross-reference validation against substrate v7 (Pass 6 P7 paper data).

Adapts cross_validate_ssdf_references.py to read mappings from the substrate v7
SUPPLIER (claim-based) instead of v3-era data/instance_level_mapping/*.json.

Methodology disclosure (per dispatcher §"Methodology disclosure required"):
  - Oracle path: SSDF v1.1 published bibliography (NIST.SP.800-218.extracted.txt)
                 — same oracle as 2026-04-14 v1.1 reference run.
  - Pair-counting variant: B (GROUNDED both sides) — only pairs where SSDF item is
                 GROUNDED in v7 AND referenced source-item is GROUNDED in v7 are
                 counted. Variant A (all pairs) and C (GROUNDED source-only)
                 deliverable on demand; B is the conservative default for a
                 published-cycle metric.
  - Strict convergence (X%): exact_co matches at same-level pairs (process→process).
  - Adjusted convergence (Y%): exact_co + same_slice (slice-bridge counted).
  - "Hub-control + adjacency-explained slice bridges": SA-8 hub controls and any
                 cross-corpus pair where SSDF item's secondary slices include the
                 referenced item's primary slice. NIST 800-53 cross-level pairs
                 (process SSDF → impl 800-53) reported separately under
                 cross_level (not strict/adjusted denominator).

Run target: substrate v7 SUPPLIER at
  data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json
SHA256 596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04
"""
from __future__ import annotations
import hashlib
import json
import pathlib
import sys
from collections import Counter, defaultdict

# Reuse parsers + resolvers from the original script
from scripts.cross_validate_ssdf_references import (
    parse_ssdf_references,
    resolve_asvs_refs,
    resolve_samm_refs,
    resolve_agile_refs,
    resolve_fpssd_refs,
    resolve_pcisslc_refs,
    resolve_nist_refs,
    SAMM_ABBREV,
    NIST_PROCESS_FAMILIES,
    SA_PROCESS_CONTROLS,
    SA_IMPL_CONTROLS,
    SA_HUB_CONTROLS,
)


REPO = pathlib.Path(__file__).resolve().parents[1]
SUP_PATH = REPO / "data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json"

# SSDF source text. Lives in parent checkout (sources/ is gitignored).
SSDF_TXT = pathlib.Path(
    "/Volumes/G-DRIVE/Shared/SecurityByDesign-TheoryOfEverything/"
    "ExternalSourcesInventory/sources/ssdf_sp800_218_v1_1/"
    "NIST.SP.800-218.extracted.txt"
)


def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def derive_instance_map_from_v7(
    supplier: dict, source_filter: str | None = None, prefer_co_level: bool = True,
) -> dict:
    """Derive {source_object_id: {co, slice, secondary_cos, secondary_slices}} from v7 SUPPLIER.

    For each GROUNDED item:
      - primary claim = highest-similarity claim AT CONTROL-OBJECTIVE LEVEL if any,
                         else highest-similarity claim overall (fallback)
      - co = primary claim's target_id (will be CO id when CO-level claims exist)
      - slice = primary claim's slice (slice family of the picked target, e.g. ACO-TMR)
      - secondary_cos = unique target_ids of CO-level claims other than primary
      - secondary_slices = unique slices represented in any other claim

    `prefer_co_level=True` mirrors the v1.1-era "primary_core_anchor" convention
    (instance-level mapping always anchored at CO). When False, picks the absolute
    highest-similarity claim regardless of level (Practice/Mechanism allowed).
    """
    out = {}
    for it in supplier["items"]:
        if it["final_classification"] != "GROUNDED":
            continue
        if source_filter and it["source"] != source_filter:
            continue
        claims = it.get("claims", [])
        if not claims:
            continue
        if prefer_co_level:
            co_level = [c for c in claims if c.get("level") == "ControlObjective"]
            primary = max(co_level, key=lambda c: c.get("similarity_score", 0.0)) if co_level \
                      else max(claims, key=lambda c: c.get("similarity_score", 0.0))
        else:
            primary = max(claims, key=lambda c: c.get("similarity_score", 0.0))
        primary_co = primary["target_id"]
        primary_slice = primary["slice"]
        secondary_cos = []
        secondary_slices = set()
        for c in claims:
            if c is primary:
                continue
            t = c["target_id"]
            if c.get("level") == "ControlObjective" and t != primary_co and t not in secondary_cos:
                secondary_cos.append(t)
            secondary_slices.add(c["slice"])
        secondary_slices.discard(primary_slice)
        out[it["source_object_id"]] = {
            "co": primary_co,
            "slice": primary_slice,
            "secondary_cos": secondary_cos,
            "secondary_slices": list(secondary_slices),
        }
    return out


def cross_validate_v7():
    print("=" * 90)
    print("SSDF Cross-Reference Validation — Substrate v7 (Pass 6 P7 paper data)")
    print("=" * 90)
    print()

    sup = json.load(SUP_PATH.open())
    sup_sha = sha256(SUP_PATH)
    print(f"Substrate v7 SUPPLIER: {SUP_PATH.relative_to(REPO)}")
    print(f"SHA256: {sup_sha}")
    print(f"Total items: {len(sup['items'])}; GROUNDED: {sup['meta']['n_grounded']}")
    print()

    # Derive per-source mappings from v7 SUPPLIER
    ssdf_map = derive_instance_map_from_v7(sup, "ssdf_sp800_218_v1_1")
    asvs5_map = derive_instance_map_from_v7(sup, "asvs_v5_0_0")
    asvs4_map = {}  # not in v7 corpus (excluded per 2026-04-27 amendment)
    samm_map = derive_instance_map_from_v7(sup, "owasp_samm_v2_1")
    nist_map = derive_instance_map_from_v7(sup, "nist_sp800_53_rev5")
    pcisslc_map = derive_instance_map_from_v7(sup, "pci_sslc_v1_1")
    fpssd_map = derive_instance_map_from_v7(sup, "safecode_fpssd_2018")
    agile_map = derive_instance_map_from_v7(sup, "safecode_agile_2012")
    asvs_map = {**asvs4_map, **asvs5_map}

    print("Per-source GROUNDED items derived from v7:")
    for label, m in [("SSDF", ssdf_map), ("ASVS", asvs_map), ("SAMM", samm_map),
                     ("NIST 800-53", nist_map), ("PCI-SSLC", pcisslc_map),
                     ("SAFECode FPSSD", fpssd_map), ("SAFECode Agile", agile_map)]:
        print(f"  {label:<18} {len(m):>5}")
    print()

    if not SSDF_TXT.exists():
        print(f"ERR: SSDF text not found at {SSDF_TXT}", file=sys.stderr)
        sys.exit(1)

    ssdf_refs = parse_ssdf_references(SSDF_TXT)
    print(f"SSDF tasks with bibliography references: {len(ssdf_refs)}")
    print()

    # Categories of validation (mirror original script)
    same_level = {"exact_co": [], "same_slice": [], "different_slice": []}
    cross_level = {"ssdf_scope_covers": [], "expected_divergence": []}
    unresolved_per_source = Counter()
    n_pairs_per_source = Counter()

    for task_id, refs in sorted(ssdf_refs.items()):
        ssdf_sid = f"SSDF-TASK-{task_id}"
        if ssdf_sid not in ssdf_map:
            ssdf_sid = f"SSDF-PRACTICE-{task_id}"
        if ssdf_sid not in ssdf_map:
            continue

        ssdf_info = ssdf_map[ssdf_sid]
        ssdf_co = ssdf_info["co"]
        ssdf_slice = ssdf_info["slice"]
        ssdf_all_slices = {ssdf_slice} | set(ssdf_info.get("secondary_slices", []))

        # NIST 800-53
        if "SP80053" in refs:
            resolved = resolve_nist_refs(refs["SP80053"], nist_map)
            n_pairs_per_source["NIST-800-53"] += len(resolved)
            for r in resolved:
                entry = {"ssdf_task": task_id, "ssdf_co": ssdf_co, "ssdf_slice": ssdf_slice,
                         "source": "NIST-800-53", "ref": r["ref"], "ref_co": r["co"],
                         "ref_slice": r["slice"]}
                if r["level"] == "hub":
                    cross_level["expected_divergence"].append(entry)
                elif r["level"] == "process":
                    if r["co"] == ssdf_co:
                        same_level["exact_co"].append(entry)
                    elif r["slice"] == ssdf_slice:
                        same_level["same_slice"].append(entry)
                    else:
                        same_level["different_slice"].append(entry)
                else:
                    if r["slice"] in ssdf_all_slices or r["co"] == ssdf_co:
                        cross_level["ssdf_scope_covers"].append(entry)
                    else:
                        cross_level["expected_divergence"].append(entry)
            if not resolved:
                unresolved_per_source["NIST-800-53"] += 1

        # ASVS (always cross-level: process → implementation)
        if "OWASPASVS" in refs:
            resolved = resolve_asvs_refs(refs["OWASPASVS"], asvs_map)
            n_pairs_per_source["ASVS"] += len(resolved)
            for r in resolved:
                entry = {"ssdf_task": task_id, "ssdf_co": ssdf_co, "ssdf_slice": ssdf_slice,
                         "source": "ASVS", "ref": r["ref"], "ref_co": r["co"],
                         "ref_slice": r["slice"], "n_items": r["n_items"]}
                if r["co"] == ssdf_co or r["slice"] == ssdf_slice:
                    cross_level["ssdf_scope_covers"].append(entry)
                else:
                    cross_level["expected_divergence"].append(entry)
            if not resolved:
                unresolved_per_source["ASVS"] += 1

        # SAFECode Agile
        if "SCAGILE" in refs:
            resolved = resolve_agile_refs(refs["SCAGILE"], agile_map)
            n_pairs_per_source["SAFECode-Agile"] += len(resolved)
            for r in resolved:
                entry = {"ssdf_task": task_id, "ssdf_co": ssdf_co, "ssdf_slice": ssdf_slice,
                         "source": "SAFECode-Agile", "ref": r["ref"], "ref_co": r["co"],
                         "ref_slice": r["slice"]}
                if r["co"] == ssdf_co:
                    same_level["exact_co"].append(entry)
                elif r["slice"] == ssdf_slice:
                    same_level["same_slice"].append(entry)
                else:
                    same_level["different_slice"].append(entry)
            if not resolved:
                unresolved_per_source["SAFECode-Agile"] += 1

        # SAFECode FPSSD
        if "SCFPSSD" in refs:
            resolved = resolve_fpssd_refs(refs["SCFPSSD"], fpssd_map)
            n_pairs_per_source["SAFECode-FPSSD"] += len(resolved)
            for r in resolved:
                entry = {"ssdf_task": task_id, "ssdf_co": ssdf_co, "ssdf_slice": ssdf_slice,
                         "source": "SAFECode-FPSSD", "ref": r["ref"], "ref_co": r["co"],
                         "ref_slice": r["slice"]}
                if r["co"] == ssdf_co:
                    same_level["exact_co"].append(entry)
                elif r["slice"] == ssdf_slice:
                    same_level["same_slice"].append(entry)
                else:
                    same_level["different_slice"].append(entry)
            if not resolved:
                unresolved_per_source["SAFECode-FPSSD"] += 1

        # PCI SSLC
        if "PCISSLC" in refs:
            resolved = resolve_pcisslc_refs(refs["PCISSLC"], pcisslc_map)
            n_pairs_per_source["PCI-SSLC"] += len(resolved)
            for r in resolved:
                entry = {"ssdf_task": task_id, "ssdf_co": ssdf_co, "ssdf_slice": ssdf_slice,
                         "source": "PCI-SSLC", "ref": r["ref"], "ref_co": r["co"],
                         "ref_slice": r["slice"]}
                if r["co"] == ssdf_co:
                    same_level["exact_co"].append(entry)
                elif r["slice"] == ssdf_slice:
                    same_level["same_slice"].append(entry)
                else:
                    same_level["different_slice"].append(entry)
            if not resolved:
                unresolved_per_source["PCI-SSLC"] += 1

        # SAMM
        if "OWASPSAMM" in refs:
            resolved = resolve_samm_refs(refs["OWASPSAMM"], samm_map)
            n_pairs_per_source["SAMM"] += len(resolved)
            for r in resolved:
                entry = {"ssdf_task": task_id, "ssdf_co": ssdf_co, "ssdf_slice": ssdf_slice,
                         "source": "SAMM", "ref": r["ref"], "ref_co": r["co"],
                         "ref_slice": r["slice"]}
                if r["co"] == ssdf_co:
                    same_level["exact_co"].append(entry)
                elif r["slice"] == ssdf_slice:
                    same_level["same_slice"].append(entry)
                else:
                    same_level["different_slice"].append(entry)
            if not resolved:
                unresolved_per_source["SAMM"] += 1

    # Compute strict / adjusted convergence
    # Strict denominator: same-level pairs only (process→process directly comparable)
    n_exact = len(same_level["exact_co"])
    n_same_slice = len(same_level["same_slice"])
    n_diff_slice = len(same_level["different_slice"])
    n_same_level_total = n_exact + n_same_slice + n_diff_slice

    n_cross_covers = len(cross_level["ssdf_scope_covers"])
    n_cross_div = len(cross_level["expected_divergence"])
    n_cross_total = n_cross_covers + n_cross_div

    strict_pct = (n_exact / n_same_level_total * 100) if n_same_level_total else 0.0
    adjusted_pct = ((n_exact + n_same_slice) / n_same_level_total * 100) if n_same_level_total else 0.0
    cross_covered_pct = (n_cross_covers / n_cross_total * 100) if n_cross_total else 0.0

    # Per-source breakdown
    print("Per-source pair counts (Variant B — GROUNDED both sides):")
    print(f"{'Source':<20} {'pairs':>6}  {'unresolved tasks':>18}")
    for src, cnt in sorted(n_pairs_per_source.items()):
        ur = unresolved_per_source.get(src, 0)
        print(f"  {src:<18} {cnt:>6}  {ur:>18}")
    print()

    print("Same-level convergence (process→process):")
    print(f"  Exact CO match:      {n_exact:>4} ({n_exact/max(1,n_same_level_total)*100:.1f}%)")
    print(f"  Same-slice match:    {n_same_slice:>4} ({n_same_slice/max(1,n_same_level_total)*100:.1f}%)")
    print(f"  Different slice:     {n_diff_slice:>4} ({n_diff_slice/max(1,n_same_level_total)*100:.1f}%)")
    print(f"  Total same-level:    {n_same_level_total:>4}")
    print()

    print("Cross-level (process→implementation):")
    print(f"  SSDF scope covers:   {n_cross_covers:>4} ({n_cross_covers/max(1,n_cross_total)*100:.1f}%)")
    print(f"  Expected divergence: {n_cross_div:>4} ({n_cross_div/max(1,n_cross_total)*100:.1f}%)")
    print(f"  Total cross-level:   {n_cross_total:>4}")
    print()

    print("=" * 90)
    print(f"STRICT  convergence (exact_co / same-level total): {strict_pct:.2f}% ({n_exact}/{n_same_level_total})")
    print(f"ADJUSTED convergence (exact_co+same_slice / same-level total): {adjusted_pct:.2f}% ({n_exact+n_same_slice}/{n_same_level_total})")
    print(f"CROSS-LEVEL coverage (SSDF scope covers / cross-level total): {cross_covered_pct:.2f}% ({n_cross_covers}/{n_cross_total})")
    print(f"TOTAL pairs evaluated: {n_same_level_total + n_cross_total}")
    print("=" * 90)

    # JSON output for paper data
    out_path = REPO / "data/p7_olir_audit/p7_v2_corrected/v7/reports/ssdf_crossval_v7.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_payload = {
        "schema": "ssdf_crossval_v7/1.0",
        "substrate": "v7 (post-AI/ML Iteration 3)",
        "substrate_supplier_path": str(SUP_PATH.relative_to(REPO)),
        "substrate_supplier_sha256": sup_sha,
        "substrate_tag": "substrate-v7-iter-3-ai-ml-incorporated",
        "ontology_tag": "ontology-v1-next-acr004-promoted",
        "methodology": {
            "oracle_path": "SSDF v1.1 published bibliography (NIST.SP.800-218.extracted.txt)",
            "pair_counting_variant": "B (GROUNDED both sides)",
            "strict_definition": "exact_co match between SSDF item primary CO and referenced item primary CO, restricted to same-level pairs (process→process)",
            "adjusted_definition": "strict + same-slice match counted as convergent (slice-bridge)",
            "hub_controls_treatment": "NIST 800-53 SA-8 hub controls counted under cross_level.expected_divergence (not in strict/adjusted denominator)",
            "cross_level_treatment": "process→implementation pairs (SSDF→ASVS, SSDF→NIST-impl) reported separately under cross_level (not in strict/adjusted denominator)",
        },
        "totals": {
            "ssdf_tasks_with_bibliography_refs": len(ssdf_refs),
            "n_same_level_total": n_same_level_total,
            "n_cross_level_total": n_cross_total,
            "n_pairs_total": n_same_level_total + n_cross_total,
            "n_exact_co": n_exact,
            "n_same_slice": n_same_slice,
            "n_different_slice": n_diff_slice,
            "n_cross_scope_covers": n_cross_covers,
            "n_cross_expected_divergence": n_cross_div,
        },
        "convergence_rates": {
            "strict_pct": round(strict_pct, 2),
            "adjusted_pct": round(adjusted_pct, 2),
            "cross_level_covered_pct": round(cross_covered_pct, 2),
        },
        "per_source_pair_counts": dict(n_pairs_per_source),
        "per_source_unresolved_tasks": dict(unresolved_per_source),
        "comparison_to_v1_1_reference_2026_04_14": {
            "v1_1_co_match_pct": 81,
            "v1_1_co_plus_slice_pct": 100,
            "v1_1_total_comparisons": 69,
            "note": "v1.1 reference run on 2026-04-14 reported 81% co_match / 100% co+slice on 69 comparisons. Methodology variant differs slightly (v1.1 used different pair-counting; v7 uses Variant B).",
        },
    }
    out_path.write_text(json.dumps(out_payload, indent=2))
    print(f"\n[write] {out_path.relative_to(REPO)}")


if __name__ == "__main__":
    cross_validate_v7()
