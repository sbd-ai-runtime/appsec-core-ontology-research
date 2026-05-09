"""SSDF v7 cross-val with version-drift-prone references filtered out.

Per dispatcher 2026-05-08-orchestrator-cartographer-scf-cross-val-v7-mini-dispatch.md
§Item 2: exclude SSDF cross-references whose target source is NOT in substrate v7
corpus OR is version-incompatible.

Filter rules:
  EXCLUDE OWASPASVS    — SSDF v1.1 references ASVS v4 IDs; corpus has v5 only
                         (asvs_v4_0_2 dropped 2026-04-27 per programme-lead amendment;
                         v5 content ≠ v4 content under same ID → version-drift).
  EXCLUDE OWASPMASVS   — source absent from corpus.
  EXCLUDE OWASPSCVS    — source absent from corpus.
  INCLUDE OWASPSAMM    — script translates SSDF v1.5 codes → SAMM v2.1; semantic drift acceptable.
  INCLUDE SP80053      — direct match (NIST SP800-53 rev5 in corpus).
  INCLUDE PCISSLC      — direct match.
  INCLUDE SCFPSSD      — direct match.
  INCLUDE SCAGILE      — direct match.

Tests version-drift hypothesis: if filtered subset recovers to ≥30% strict, the
v7 full-set rate (18.03%) is dragged predominantly by ASVS-axis contamination.
"""
from __future__ import annotations
import hashlib
import json
import pathlib
import sys
from collections import Counter, defaultdict

from scripts.cross_validate_ssdf_references import (
    parse_ssdf_references,
    resolve_samm_refs,
    resolve_agile_refs,
    resolve_fpssd_refs,
    resolve_pcisslc_refs,
    resolve_nist_refs,
)
from scripts.cross_validate_ssdf_references_v7 import (
    SUP_PATH, SSDF_TXT, sha256, derive_instance_map_from_v7,
)

REPO = pathlib.Path(__file__).resolve().parents[1]
OUT_PATH = REPO / "data/p7_olir_audit/p7_v2_corrected/v7/reports/ssdf_crossval_v7_filtered.json"


# Sources INCLUDED in filtered run (corpus-resolvable, no version-drift)
INCLUDED_REF_SOURCES = {"SP80053", "PCISSLC", "SCFPSSD", "SCAGILE", "OWASPSAMM"}
EXCLUDED_REF_SOURCES = {"OWASPASVS", "OWASPMASVS", "OWASPSCVS"}


def main():
    print("=" * 90)
    print("SSDF v7 cross-validation — FILTERED (corpus-resolvable references only)")
    print("=" * 90)
    print()
    print(f"INCLUDED reference sources: {sorted(INCLUDED_REF_SOURCES)}")
    print(f"EXCLUDED reference sources: {sorted(EXCLUDED_REF_SOURCES)}")
    print()

    sup = json.load(SUP_PATH.open())
    sup_sha = sha256(SUP_PATH)
    print(f"Substrate v7 SUPPLIER SHA256: {sup_sha}")

    ssdf_map = derive_instance_map_from_v7(sup, "ssdf_sp800_218_v1_1")
    samm_map = derive_instance_map_from_v7(sup, "owasp_samm_v2_1")
    nist_map = derive_instance_map_from_v7(sup, "nist_sp800_53_rev5")
    pcisslc_map = derive_instance_map_from_v7(sup, "pci_sslc_v1_1")
    fpssd_map = derive_instance_map_from_v7(sup, "safecode_fpssd_2018")
    agile_map = derive_instance_map_from_v7(sup, "safecode_agile_2012")

    if not SSDF_TXT.exists():
        print(f"ERR: SSDF text not found at {SSDF_TXT}", file=sys.stderr)
        sys.exit(1)

    ssdf_refs = parse_ssdf_references(SSDF_TXT)
    print(f"SSDF tasks with bibliography references: {len(ssdf_refs)}")

    same_level = {"exact_co": [], "same_slice": [], "different_slice": []}
    cross_level = {"ssdf_scope_covers": [], "expected_divergence": []}
    n_pairs_per_source = Counter()
    n_unresolved_per_source = Counter()
    n_excluded_per_source = Counter()

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

        # Track excluded references for transparency
        for ref_src in EXCLUDED_REF_SOURCES:
            if ref_src in refs:
                n_excluded_per_source[ref_src] += 1

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
                n_unresolved_per_source["NIST-800-53"] += 1

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
                n_unresolved_per_source["SAFECode-Agile"] += 1

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
                n_unresolved_per_source["SAFECode-FPSSD"] += 1

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
                n_unresolved_per_source["PCI-SSLC"] += 1

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
                n_unresolved_per_source["SAMM"] += 1

    n_exact = len(same_level["exact_co"])
    n_same_slice = len(same_level["same_slice"])
    n_diff_slice = len(same_level["different_slice"])
    n_same_total = n_exact + n_same_slice + n_diff_slice
    n_cross_covers = len(cross_level["ssdf_scope_covers"])
    n_cross_div = len(cross_level["expected_divergence"])
    n_cross_total = n_cross_covers + n_cross_div

    strict_pct = (n_exact / n_same_total * 100) if n_same_total else 0
    adjusted_pct = ((n_exact + n_same_slice) / n_same_total * 100) if n_same_total else 0

    print()
    print("Per-source pair counts (filtered, Variant B):")
    for src, n in n_pairs_per_source.most_common():
        ur = n_unresolved_per_source.get(src, 0)
        print(f"  {src:<22} {n:>4}  unresolved tasks: {ur}")
    print()

    print("Excluded references (would have been counted in full SSDF v7 run):")
    for src, n in n_excluded_per_source.most_common():
        print(f"  {src:<22} {n:>4} task(s) had {src} refs (excluded under filter)")
    print()

    print("Same-level convergence (process→process):")
    print(f"  Exact CO:       {n_exact:>4} ({n_exact/max(1,n_same_total)*100:.2f}%)")
    print(f"  Same-slice:     {n_same_slice:>4} ({n_same_slice/max(1,n_same_total)*100:.2f}%)")
    print(f"  Different slice:{n_diff_slice:>4} ({n_diff_slice/max(1,n_same_total)*100:.2f}%)")
    print(f"  Total:          {n_same_total:>4}")
    print()
    print("Cross-level (process→implementation):")
    print(f"  Scope covers:   {n_cross_covers:>4}")
    print(f"  Expected diverge:{n_cross_div:>4}")
    print(f"  Total:          {n_cross_total:>4}")
    print()
    print("=" * 90)
    print(f"FILTERED STRICT  X% : {strict_pct:.2f}% ({n_exact}/{n_same_total})")
    print(f"FILTERED ADJUSTED Y%: {adjusted_pct:.2f}% ({n_exact+n_same_slice}/{n_same_total})")
    print("=" * 90)
    print()
    print("Comparison vs full SSDF v7 (with ASVS contamination):")
    print(f"  Full v7    : 18.03% strict / 35.25% adjusted on 122 same-level / 285 total")
    print(f"  Filtered v7: {strict_pct:.2f}% strict / {adjusted_pct:.2f}% adjusted on {n_same_total} same-level / {n_same_total + n_cross_total} total")
    print()

    out = {
        "schema": "ssdf_crossval_v7_filtered/1.0",
        "substrate_supplier_sha256": sup_sha,
        "filter_rules": {
            "included_ref_sources": sorted(INCLUDED_REF_SOURCES),
            "excluded_ref_sources": sorted(EXCLUDED_REF_SOURCES),
            "rationale": {
                "OWASPASVS": "SSDF v1.1 references ASVS v4 IDs; corpus has ASVS v5 only (v4 dropped 2026-04-27 amendment); v5 content ≠ v4 content under same ID = version-drift contamination",
                "OWASPMASVS": "Source not in substrate v7 corpus",
                "OWASPSCVS": "Source not in substrate v7 corpus",
            },
        },
        "totals": {
            "n_same_level_total": n_same_total,
            "n_cross_level_total": n_cross_total,
            "n_pairs_total": n_same_total + n_cross_total,
            "n_exact_co": n_exact,
            "n_same_slice": n_same_slice,
            "n_different_slice": n_diff_slice,
        },
        "convergence_rates": {
            "filtered_strict_pct": round(strict_pct, 2),
            "filtered_adjusted_pct": round(adjusted_pct, 2),
        },
        "per_source_pair_counts": dict(n_pairs_per_source),
        "per_source_unresolved_tasks": dict(n_unresolved_per_source),
        "per_source_excluded_task_count": dict(n_excluded_per_source),
        "comparison_to_full_ssdf_v7": {
            "full_strict_pct": 18.03,
            "full_adjusted_pct": 35.25,
            "full_n_same_level": 122,
            "full_n_total": 285,
        },
        "version_drift_hypothesis_test": {
            "hypothesis": "v7 SSDF full-set rate (18.03%) depressed by ASVS-axis contamination (v4 IDs in SSDF refs vs v5-only corpus)",
            "filtered_strict_recovery_threshold": "≥30% would empirically confirm hypothesis",
            "filtered_strict_observed": round(strict_pct, 2),
            "verdict": "CONFIRMED" if strict_pct >= 30.0 else (
                "PARTIAL" if strict_pct >= 22.0 else "NOT CONFIRMED — version drift not the dominant factor"
            ),
        },
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2))
    print(f"[write] {OUT_PATH.relative_to(REPO)}")


if __name__ == "__main__":
    main()
