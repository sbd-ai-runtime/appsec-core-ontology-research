"""SCF cross-reference cross-validation against substrate v7 (P7 Pass 6 §8.2 PRIMARY).

Methodology (per dispatcher 2026-05-08-orchestrator-cartographer-scf-cross-val-v7-mini-dispatch.md):
  Forward direction (same as SSDF v7 cross-val, validated correct in joint review).
  For each pair (substrate-v7 item A, substrate-v7 item B) co-referenced by the same
  SCF control in SCF's published STRM tables:
    - look up primary substrate-v7 CO mapping for both sides
    - strict match: pipeline_co_left == pipeline_co_right (exact CO)
    - adjusted match: slice(left) == slice(right) (same slice; slice-bridge)
    - different-slice: else
    - cross-level: not applicable in SCF cross-val (all pilot items are at comparable
                   abstraction levels; no SSDF-style process→implementation hierarchy)

Variant B (GROUNDED both sides) per Stage 7.bis precedent.

CO-level-preferred primary anchor (mirrors v1.1-era primary_core_anchor convention).

Inputs:
  - data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json (substrate v7)
  - data/p7_olir_audit/scf_audit/scf_strm_extracted/<pilot>_scf_strm_mappings.json (10 pilots)
"""
from __future__ import annotations
import hashlib
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

REPO = pathlib.Path(__file__).resolve().parents[1]
SUPPLIER = REPO / "data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json"
STRM_DIR = REPO / "data/p7_olir_audit/scf_audit/scf_strm_extracted"
OUT_PATH = REPO / "data/p7_olir_audit/p7_v2_corrected/v7/reports/scf_crossval_v7.json"


def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def derive_v7_primary_map(supplier: dict, prefer_co_level: bool = True) -> dict:
    """For each GROUNDED v7 item, derive primary CO + slice (CO-level-preferred)."""
    out: dict[str, dict] = {}
    for it in supplier["items"]:
        if it["final_classification"] != "GROUNDED":
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
        out[(it["source"], it["source_object_id"])] = {
            "co": primary["target_id"],
            "slice": primary["slice"],
            "level": primary["level"],
        }
    return out


# ============================================================================
# Per-pilot SCF foreign_id → substrate v7 source_object_id normalizers
# ============================================================================

def normalize_nist(fid: str) -> list[str]:
    """SCF format: 'AC-01' / 'AC-1(1)' / 'PM-01'. v7: 'SP800-53-AC-1', 'SP800-53-AC-1.1'."""
    fid = fid.strip()
    # Strip leading zero in numeric component: AC-01 → AC-1
    m = re.match(r"^([A-Z]{2})-0*(\d+)(.*)$", fid)
    if not m:
        return []
    fam, n, suffix = m.group(1), m.group(2), m.group(3).strip()
    candidates = [f"SP800-53-{fam}-{n}"]
    # Suffix handling: parens → dot, e.g. AC-1(1) → AC-1.1
    if suffix:
        sm = re.match(r"\((\d+)\)", suffix)
        if sm:
            candidates.append(f"SP800-53-{fam}-{n}.{sm.group(1)}")
        else:
            cleaned = suffix.replace("(", ".").replace(")", "").replace(" ", "")
            if cleaned:
                candidates.append(f"SP800-53-{fam}-{n}{cleaned}")
    return candidates


def normalize_cis(fid: str) -> list[str]:
    """SCF format: '1.1', '1.0', '13.10'. v7: 'CIS-1', 'CIS-1.1'."""
    fid = fid.strip()
    # Strip ".0" trailing → "1.0" → "1"
    if fid.endswith(".0"):
        fid_main = fid[:-2]
        return [f"CIS-{fid_main}"]
    return [f"CIS-{fid}"]


def normalize_ssdf(fid: str) -> list[str]:
    """SCF format: 'PO.1', 'PO.1.2', 'PS.1'. v7: 'SSDF-PRACTICE-PO.1' (no task-level)."""
    fid = fid.strip()
    # v7 has only PRACTICE-level (PO.1, PO.2, etc., not PO.1.2 task level)
    parts = fid.split(".")
    if len(parts) >= 2:
        # Extract practice (e.g., "PO.1" from "PO.1.2")
        practice = ".".join(parts[:2])
    else:
        practice = fid
    return [f"SSDF-PRACTICE-{practice}", f"SSDF-PRACTICE-{fid}"]


def normalize_pci_dss(fid: str) -> list[str]:
    """SCF format: '12.4', '1.1.1', 'A3.1.2'. v7: 'PCI-REQ-12', 'PCI-REQ-1'."""
    fid = fid.strip()
    # Top-level requirement number; PCI-REQ-N in v7
    m = re.match(r"^([A-Z]?\d+)", fid)
    if m:
        top = m.group(1)
        return [f"PCI-REQ-{top}", f"PCI-REQ-{fid}"]
    return []


def normalize_top10(fid: str) -> list[str]:
    """SCF format: 'A01:2025', 'A05:2025'. v7: 'TOP10-A01-2021'.
    Year mismatch (SCF→2025 vs corpus→2021): extract category prefix."""
    fid = fid.strip()
    m = re.match(r"^(A\d{2})", fid)
    if m:
        return [f"TOP10-{m.group(1)}-2021"]
    return []


def normalize_hipaa(fid: str) -> list[str]:
    """SCF format: '164.308(a)(1)(i)', '164.306(a)(1)'. v7: 'HIPAA-164-308a1'."""
    fid = fid.strip()
    # 164.308(a)(1)(i) → 164-308a1 (strip parens; concat first level)
    m = re.match(r"^164\.(\d+)\(([a-z])\)\((\d+)\)", fid)
    if m:
        return [f"HIPAA-164-{m.group(1)}{m.group(2)}{m.group(3)}"]
    m2 = re.match(r"^164\.(\d+)\(([a-z])\)", fid)
    if m2:
        # 164.316(a) → look for HIPAA-164-316a
        return [f"HIPAA-164-{m2.group(1)}{m2.group(2)}"]
    return []


def normalize_eu(prefix: str) -> callable:
    """EU regulatory: 'Article 10.13', 'Article 5.1' → '<PREFIX>-ART-10', '<PREFIX>-ART-5'."""
    def _norm(fid: str) -> list[str]:
        m = re.match(r"^Article\s+(\d+)", fid.strip())
        if m:
            return [f"{prefix}-ART-{m.group(1)}"]
        return []
    return _norm


PILOT_NORMALIZERS = {
    "nist_sp800_53_rev5": normalize_nist,
    "cis_controls_v8_1_2": normalize_cis,
    "ssdf_sp800_218_v1_1": normalize_ssdf,
    "pci_dss_v4_0_1": normalize_pci_dss,
    "owasp_top_10_2021": normalize_top10,
    "hipaa_security_rule": normalize_hipaa,
    "eu_cra": normalize_eu("CRA"),
    "eu_dora": normalize_eu("DORA"),
    "eu_nis2": normalize_eu("NIS2"),
    "eu_rgpd": normalize_eu("GDPR"),
}


def main():
    print("=" * 90)
    print("SCF Cross-Reference Validation — Substrate v7 (P7 Pass 6 §8.2 PRIMARY)")
    print("=" * 90)

    sup = json.load(SUPPLIER.open())
    sup_sha = sha256(SUPPLIER)
    print(f"\nSubstrate v7 SUPPLIER: {SUPPLIER.relative_to(REPO)}")
    print(f"SHA256: {sup_sha}")
    print(f"Total items: {len(sup['items'])}")
    print()

    # Build (pilot, source_object_id) → primary CO/slice map
    primary_map = derive_v7_primary_map(sup, prefer_co_level=True)
    print(f"GROUNDED items (primary CO derived): {len(primary_map)}")
    print()

    # Build SCF inverted index: scf_id → {pilot: [normalized_v7_ids]}
    scf_inv: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    per_pilot_resolved = Counter()
    per_pilot_unresolved = Counter()
    for f in sorted(STRM_DIR.glob("*_scf_strm_mappings.json")):
        d = json.load(f.open())
        pilot = d["pilot_id"]
        normalize = PILOT_NORMALIZERS.get(pilot)
        if not normalize:
            continue
        scf_version = d.get("scf_version")
        for m in d.get("mappings", []):
            scf_id = m.get("scf_control_id")
            if not scf_id:
                continue
            for fid in m.get("foreign_ids", []):
                candidates = normalize(fid)
                # Pick first candidate that exists in v7 GROUNDED
                resolved = None
                for c in candidates:
                    if (pilot, c) in primary_map:
                        resolved = c
                        break
                if resolved:
                    scf_inv[scf_id][pilot].append(resolved)
                    per_pilot_resolved[pilot] += 1
                else:
                    per_pilot_unresolved[pilot] += 1

    print("Per-pilot SCF foreign_id → v7 GROUNDED resolution:")
    print(f"{'pilot':<32}  {'resolved':>9}  {'unresolved':>10}")
    total_pilots = sorted(set(list(per_pilot_resolved.keys()) + list(per_pilot_unresolved.keys())))
    for p in total_pilots:
        r, u = per_pilot_resolved[p], per_pilot_unresolved[p]
        print(f"  {p:<30}  {r:>9}  {u:>10}")
    print()

    # Generate cross-pilot pairs from SCF inverted index
    pairs = []  # list of (scf_id, pilot_A, item_A, pilot_B, item_B)
    for scf_id, p2items in scf_inv.items():
        pilots = sorted(p2items.keys())
        for i in range(len(pilots)):
            for j in range(i + 1, len(pilots)):
                items_a = p2items[pilots[i]]
                items_b = p2items[pilots[j]]
                seen = set()
                for ia in items_a:
                    for ib in items_b:
                        key = (pilots[i], ia, pilots[j], ib)
                        if key in seen:
                            continue
                        seen.add(key)
                        pairs.append((scf_id, pilots[i], ia, pilots[j], ib))

    n_total_pairs = len(pairs)
    print(f"Total SCF-mediated cross-pilot pairs (Variant A): {n_total_pairs}")

    # Variant B: both sides GROUNDED (already filtered via resolution above; all resolved sides are GROUNDED)
    # So all pairs in `pairs` are decidable under Variant B.
    n_decidable = n_total_pairs

    # Compute strict / adjusted / different-slice
    n_strict = 0
    n_same_slice = 0
    n_diff_slice = 0
    pair_examples = {"strict": [], "same_slice": [], "different_slice": []}
    per_pilot_pair_counts = Counter()
    per_outcome_pilot_pair = defaultdict(lambda: Counter())

    for scf_id, pa, ia, pb, ib in pairs:
        key = tuple(sorted([pa, pb]))
        per_pilot_pair_counts[key] += 1
        ma = primary_map[(pa, ia)]
        mb = primary_map[(pb, ib)]
        if ma["co"] == mb["co"]:
            n_strict += 1
            per_outcome_pilot_pair[key]["strict"] += 1
            if len(pair_examples["strict"]) < 5:
                pair_examples["strict"].append({
                    "scf_id": scf_id, "left": f"{pa}/{ia}", "right": f"{pb}/{ib}",
                    "co": ma["co"], "slice": ma["slice"],
                })
        elif ma["slice"] == mb["slice"]:
            n_same_slice += 1
            per_outcome_pilot_pair[key]["same_slice"] += 1
            if len(pair_examples["same_slice"]) < 5:
                pair_examples["same_slice"].append({
                    "scf_id": scf_id, "left": f"{pa}/{ia} → {ma['co']}",
                    "right": f"{pb}/{ib} → {mb['co']}", "slice": ma["slice"],
                })
        else:
            n_diff_slice += 1
            per_outcome_pilot_pair[key]["different_slice"] += 1
            if len(pair_examples["different_slice"]) < 5:
                pair_examples["different_slice"].append({
                    "scf_id": scf_id,
                    "left": f"{pa}/{ia} → {ma['co']} ({ma['slice']})",
                    "right": f"{pb}/{ib} → {mb['co']} ({mb['slice']})",
                })

    strict_pct = n_strict / max(1, n_decidable) * 100
    adjusted_pct = (n_strict + n_same_slice) / max(1, n_decidable) * 100

    print()
    print("Same-CO / same-slice / different-slice breakdown:")
    print(f"  Strict (exact CO):      {n_strict:>5} ({n_strict/max(1,n_decidable)*100:.2f}%)")
    print(f"  Same-slice match:       {n_same_slice:>5} ({n_same_slice/max(1,n_decidable)*100:.2f}%)")
    print(f"  Different slice:        {n_diff_slice:>5} ({n_diff_slice/max(1,n_decidable)*100:.2f}%)")
    print(f"  Total decidable (Var B):{n_decidable:>5}")
    print()

    print("=" * 90)
    print(f"STRICT  convergence X% : {strict_pct:.2f}% ({n_strict}/{n_decidable})")
    print(f"ADJUSTED convergence Y%: {adjusted_pct:.2f}% ({n_strict+n_same_slice}/{n_decidable})")
    print("=" * 90)
    print()

    print("Top pilot-pair couplings (decidable pair counts):")
    for (a, b), n in per_pilot_pair_counts.most_common(15):
        s = per_outcome_pilot_pair[(a, b)]["strict"]
        ss = per_outcome_pilot_pair[(a, b)]["same_slice"]
        ds = per_outcome_pilot_pair[(a, b)]["different_slice"]
        sp = (s / max(1, n)) * 100
        ap = ((s + ss) / max(1, n)) * 100
        print(f"  ({a:<28}, {b:<28}) n={n:>5}  strict {s:>4} ({sp:>5.1f}%)  adj {s+ss:>4} ({ap:>5.1f}%)  diff {ds:>4}")

    # Comparison vs v4.2 era
    print()
    print("v4.2 era reference (per memory project_p7_scf_tier1_convergence_validation_2026_04_22):")
    print("  442 decidable / 504 pairs / 38.46% strict / 56.14% adjusted")
    print(f"v7 result: {n_decidable} decidable / {n_total_pairs} pairs / {strict_pct:.2f}% strict / {adjusted_pct:.2f}% adjusted")
    print()
    print("Note: v4.2 era used a DIFFERENT methodology (curated SCF-domain → AC-slice map; per-item")
    print("convergence assessment). v7 uses forward-direction pair matching across substrate v7.")
    print("Numbers NOT directly comparable; both methodologies disclose explicitly.")

    # Write output JSON
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    out = {
        "schema": "scf_crossval_v7/1.0",
        "substrate": "v7 (post-AI/ML Iteration 3)",
        "substrate_supplier_path": str(SUPPLIER.relative_to(REPO)),
        "substrate_supplier_sha256": sup_sha,
        "substrate_tag": "substrate-v7-iter-3-ai-ml-incorporated",
        "ontology_tag": "ontology-v1-next-acr004-promoted",
        "scf_version": "2026.1",
        "methodology": {
            "oracle_path": "SCF 2026.1 STRM published cross-references (10 pilots; data/p7_olir_audit/scf_audit/scf_strm_extracted/)",
            "pair_counting_variant": "B (GROUNDED both sides)",
            "primary_anchor_derivation": "CO-level-preferred (highest-similarity CO-level claim if any; else highest claim overall)",
            "strict_definition": "exact_co match between substrate-v7 primary CO of item A and primary CO of item B, where (A, B) is a cross-pilot pair sharing an SCF control reference",
            "adjusted_definition": "strict + same-slice match counted as convergent (slice-bridge)",
            "pair_generation": "for each SCF control with ≥2 pilots referencing it: cross-pilot product of normalized substrate-v7 source_object_ids that resolve to GROUNDED items",
            "level_treatment": "all pilot items are at comparable abstraction levels in v7 (no SSDF-style process→implementation hierarchy distinction); no separate cross-level bucket",
            "pilots_with_strm_extracts": list(PILOT_NORMALIZERS.keys()),
            "version_drift_caveats": [
                "owasp_top_10_2021: SCF references 'A01:2025' — corpus has 2021. Category code (A01) used as primary key; year mismatch tolerated.",
                "Other pilots: direct version match per scf_strm_extracted/<pilot>_scf_strm_mappings.json `version_match: exact` field.",
            ],
        },
        "totals": {
            "n_total_pairs_variant_a": n_total_pairs,
            "n_decidable_variant_b": n_decidable,
            "n_strict": n_strict,
            "n_same_slice": n_same_slice,
            "n_different_slice": n_diff_slice,
        },
        "convergence_rates": {
            "strict_pct": round(strict_pct, 2),
            "adjusted_pct": round(adjusted_pct, 2),
        },
        "per_pilot_resolution": {
            "resolved": dict(per_pilot_resolved),
            "unresolved": dict(per_pilot_unresolved),
        },
        "per_pilot_pair_counts": {f"{a} × {b}": n for (a, b), n in per_pilot_pair_counts.most_common()},
        "per_pilot_pair_outcomes": {
            f"{a} × {b}": dict(per_outcome_pilot_pair[(a, b)])
            for (a, b) in per_pilot_pair_counts
        },
        "pair_examples": pair_examples,
        "comparison_to_v4_2_era": {
            "v4_2_strict_pct": 38.46,
            "v4_2_adjusted_pct": 56.14,
            "v4_2_n_decidable": 442,
            "v4_2_n_total_pairs": 504,
            "v4_2_methodology": "curated SCF-domain → AC-slice map; per-item convergence assessment (NOT direct pair matching)",
            "note": "v4.2 numbers used a DIFFERENT methodology than v7 forward-direction pair matching. Both methodologies disclose explicitly; v7 is forward-direction (primary anchor on both sides).",
        },
    }
    OUT_PATH.write_text(json.dumps(out, indent=2))
    print(f"\n[write] {OUT_PATH.relative_to(REPO)}")


if __name__ == "__main__":
    main()
