"""Generate paper §8.2 multi-claim alignment figures (3 figures).

Adopts the established programme convention from
appsec-core-ontology-research-authoring/papers/{00,05}/source/images/
(graphviz `.dot` source → `.svg` + `.pdf` + preview `.png`).

Style conventions (inherited):
  - Font: "STIX Two Text" (LaTeX-compatible)
  - Palette: fill #f4f4f8, border #2c3e50
  - Spacing: nodesep=0.35, ranksep=0.55 (compact academic)
  - HTML labels with <B>/<FONT POINT-SIZE> for typography control

Figures:
  Figure 1 — frontier match captures alignment that strict misses
             (PW.8 ↔ SA-11; programme-lead worked example)
  Figure 2 — strict primary CO match (clean baseline)
             (PO.1 ↔ SA-1; both → ACO-TMR-008)
  Figure 3 — frontier=FALSE, honest disclosure of genuine divergence
             (PO.2 ↔ SCAGILE-OPS-15; roles/responsibilities vs QA training)

Outputs (per figure, in `data/p7_olir_audit/p7_v2_corrected/v7/reports/figures/`):
  figure-N-<slug>.dot           ← LLM-authored declarative spec ("the prompt")
  figure-N-<slug>.svg           ← graphviz vector output
  figure-N-<slug>.pdf           ← LaTeX-ready
  figure-N-<slug>-preview.png   ← raster preview (150 dpi)

Run:
  python3 -m scripts.figures.generate_p7_section_8_2_figures
"""
from __future__ import annotations
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SUPPLIER = REPO / "data/p7_olir_audit/p7_v2_corrected/v7/SUPPLIER_v7_0.json"
OUT_DIR = REPO / "data/p7_olir_audit/p7_v2_corrected/v7/reports/figures"

SLICE_LABELS = {
    "ACO-SCBI": "Supply Chain & Build Integrity",
    "ACO-IAT":  "Identity, Access & Session Trust",
    "ACO-ATB":  "Architecture & Trust Boundaries",
    "ACO-TSV":  "Testing, Security Validation",
    "ACO-TMR":  "Threat Modeling & Risk",
    "ACO-SPC":  "Secret Handling, Protected Configuration",
    "ACO-IVF":  "Input/Output Validation, Safe Parsing",
    "ACO-ITS":  "Integration Trust & Service Security",
    "ACO-RPR":  "Release, Promotion & Rollback Readiness",
    "ACO-SLG":  "Security Logging & Audit Trail",
}


def derive(it: dict) -> dict:
    """Replicate frontier_match_and_audit_v7's derivation for an item."""
    claims = it.get("claims", [])
    if not claims:
        return None
    co_level = [c for c in claims if c.get("level") == "ControlObjective"]
    primary = max(co_level, key=lambda c: c.get("similarity_score", 0.0)) if co_level \
              else max(claims, key=lambda c: c.get("similarity_score", 0.0))
    primary_co = primary["target_id"]
    primary_slice = primary["slice"]
    # Top-5 claims by similarity
    top5 = sorted(claims, key=lambda c: -c.get("similarity_score", 0.0))[:5]
    frontier = sorted({primary_slice} | {c["slice"] for c in claims})
    return {
        "primary": {
            "target": primary_co,
            "slice": primary_slice,
            "level": primary["level"],
            "sim": float(primary["similarity_score"]),
        },
        "top5_claims": [
            {
                "target": c["target_id"],
                "slice": c["slice"],
                "level": c["level"],
                "sim": round(float(c["similarity_score"]), 3),
                "is_primary": c is primary,
            }
            for c in top5
        ],
        "frontier_slices": frontier,
        "source_text": (it.get("source_text") or "")[:160],
        "source_object_id": it["source_object_id"],
        "source_pilot": it["source"],
    }


def find_item(supplier, source, sid):
    for it in supplier["items"]:
        if it["source"] == source and it["source_object_id"] == sid:
            return it
    return None


# ============================================================================
# Visual encoding constants (graphviz attrs)
# ============================================================================
PILOT_BORDER = {
    "ssdf_sp800_218_v1_1": "#1f4e79",   # SSDF blue
    "nist_sp800_53_rev5":  "#2e6f40",   # NIST green
    "safecode_agile_2012": "#7f5f30",   # SafeCode brown
}

LEVEL_FILL = {
    "ControlObjective": "#fef6e0",   # light yellow
    "Practice":         "#e0f0e0",   # light green
    "Mechanism":        "#e0e8f5",   # light blue
}

FRONTIER_HIGHLIGHT = "#ffd966"  # gold for frontier intersection
SLICE_NEUTRAL = "#f4f4f8"
ENTRY_FILL = "#f4f4f8"
BORDER_DEFAULT = "#2c3e50"


def html_truncate(s: str, n: int) -> str:
    """Escape minimal HTML chars in source_text + truncate."""
    if not s:
        return ""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if len(s) > n:
        s = s[:n - 1] + "…"
    return s


def emit_dot(figure_id: str, title: str, caption_anchor: str,
             left: dict, right: dict,
             frontier_slices: list[str],
             match_class: str,
             extra_annotations: list[str]) -> str:
    """Emit a graphviz .dot string for a 3-tier multi-claim alignment figure.

    Tier 1: two source-entry boxes (left + right)
    Tier 2: top-5 claims per side (10 nodes total) with arrows to slice nodes
    Tier 3: AppSec Core slices (frontier-intersection slices highlighted gold)
    """
    lines = []
    lines.append(f"// {figure_id}: {title}")
    lines.append(f"// Anchor: {caption_anchor}")
    lines.append(f"// Render: dot -Tsvg {figure_id}.dot -o {figure_id}.svg")
    lines.append(f"//         dot -Tpdf {figure_id}.dot -o {figure_id}.pdf")
    lines.append(f"//         dot -Tpng -Gdpi=150 {figure_id}.dot -o {figure_id}-preview.png")
    lines.append(f"// Generated by scripts/figures/generate_p7_section_8_2_figures.py")
    lines.append(f"// Style conventions inherited from appsec-core-ontology-research-authoring/papers/{{00,05}}/source/images/")
    lines.append("")
    lines.append("digraph " + figure_id.replace("-", "_") + " {")
    lines.append('    rankdir=TB;')
    lines.append('    fontname="STIX Two Text";')
    lines.append('    fontsize=11;')
    lines.append('    bgcolor="white";')
    lines.append('    pad=0.3;')
    lines.append('    nodesep=0.35;')
    lines.append('    ranksep=0.55;')
    lines.append('    splines=true;')
    lines.append('    compound=true;')
    lines.append('')
    lines.append('    node [shape=box, style="rounded,filled", fontname="STIX Two Text", fontsize=10, margin="0.15,0.10"];')
    lines.append('    edge [fontname="STIX Two Text", fontsize=8, color="#2c3e50", arrowsize=0.6];')
    lines.append('')

    # Title (top-of-figure annotation)
    lines.append(f'    figure_title [label=<<B>{title}</B>>, shape=plaintext, fillcolor=none];')

    # ====================================================================
    # Tier 1 — Source entries
    # ====================================================================
    def entry_node(side: str, data: dict) -> str:
        pilot = data["source_pilot"]
        sid = data["source_object_id"]
        text = html_truncate(data["source_text"], 140)
        border = PILOT_BORDER.get(pilot, BORDER_DEFAULT)
        label = (
            f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">'
            f'<TR><TD ALIGN="CENTER"><B>{pilot}</B></TD></TR>'
            f'<TR><TD ALIGN="CENTER"><FONT POINT-SIZE="11"><B>{sid}</B></FONT></TD></TR>'
            f'<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="#555"><I>{text}</I></FONT></TD></TR>'
            f'</TABLE>>'
        )
        return (
            f'    entry_{side} [label={label}, fillcolor="{ENTRY_FILL}", '
            f'color="{border}", penwidth=2, width=3.2];'
        )

    lines.append('    subgraph cluster_tier1 {')
    lines.append('        label=<<FONT POINT-SIZE="9" COLOR="#888"><I>Source entries (oracle-side)</I></FONT>>;')
    lines.append('        labelloc=t; style=invis;')
    lines.append('        ' + entry_node("left", left)[4:])
    lines.append('        ' + entry_node("right", right)[4:])
    # Force same rank for both entries
    lines.append('        {rank=same; entry_left; entry_right;}')
    lines.append('    }')
    lines.append('')

    # ====================================================================
    # Tier 2 — Claims (top-5 per side)
    # ====================================================================
    def claim_nodes(side: str, data: dict) -> list[str]:
        out = []
        for i, c in enumerate(data["top5_claims"], 1):
            level = c["level"]
            target = c["target"]
            sim = c["sim"]
            fill = LEVEL_FILL.get(level, "#f0f0f0")
            level_short = {"ControlObjective": "CO", "Practice": "P", "Mechanism": "M"}.get(level, level)
            if c["is_primary"]:
                style = "rounded,filled,bold"
                penwidth = 2.5
                border = "#a83232"  # red border for primary
            else:
                style = "rounded,filled,dashed"
                penwidth = 1
                border = BORDER_DEFAULT
            label = (
                f'<<FONT POINT-SIZE="8"><B>{level_short}</B></FONT><BR/>'
                f'<FONT POINT-SIZE="9"><B>{target}</B></FONT><BR/>'
                f'<FONT POINT-SIZE="7" COLOR="#555">sim {sim:.3f}</FONT>>'
            )
            node_id = f'claim_{side}_{i}'
            out.append(
                f'        {node_id} [label={label}, fillcolor="{fill}", '
                f'color="{border}", style="{style}", penwidth={penwidth}, width=1.4];'
            )
        return out

    lines.append('    subgraph cluster_tier2 {')
    lines.append('        label=<<FONT POINT-SIZE="9" COLOR="#888"><I>Claims (top-5 per item by similarity)</I></FONT>>;')
    lines.append('        labelloc=t; style=invis;')
    for n in claim_nodes("left", left):
        lines.append(n)
    for n in claim_nodes("right", right):
        lines.append(n)
    # Force same rank for all claim nodes
    same_rank = "; ".join(
        [f"claim_left_{i}" for i in range(1, 6)] + [f"claim_right_{i}" for i in range(1, 6)]
    )
    lines.append(f'        {{rank=same; {same_rank};}}')
    lines.append('    }')
    lines.append('')

    # ====================================================================
    # Tier 3 — AppSec Core slices
    # ====================================================================
    # Show all slices that appear in EITHER side's frontier; highlight intersection in gold.
    all_slices = sorted(set(left["frontier_slices"]) | set(right["frontier_slices"]))
    intersection = sorted(set(left["frontier_slices"]) & set(right["frontier_slices"]))
    lines.append('    subgraph cluster_tier3 {')
    lines.append('        label=<<FONT POINT-SIZE="9" COLOR="#888"><I>AppSec Core slices reached</I></FONT>>;')
    lines.append('        labelloc=t; style=invis;')
    for slc in all_slices:
        slc_label = SLICE_LABELS.get(slc, "").replace("&", "&amp;")
        is_intersect = slc in intersection
        fill = FRONTIER_HIGHLIGHT if is_intersect else SLICE_NEUTRAL
        marker = "★ frontier ★" if is_intersect else ""
        label = (
            f'<<FONT POINT-SIZE="9"><B>{slc}</B></FONT><BR/>'
            f'<FONT POINT-SIZE="7" COLOR="#444"><I>{slc_label}</I></FONT>'
            + (f'<BR/><FONT POINT-SIZE="7" COLOR="#7a4900"><B>{marker}</B></FONT>' if marker else '')
            + '>'
        )
        node_id = "slice_" + slc.replace("-", "_")
        penwidth = 2.5 if is_intersect else 1.5
        lines.append(
            f'        {node_id} [label={label}, fillcolor="{fill}", '
            f'color="{BORDER_DEFAULT}", penwidth={penwidth}, width=1.6];'
        )
    same_rank_slices = "; ".join("slice_" + s.replace("-", "_") for s in all_slices)
    lines.append(f'        {{rank=same; {same_rank_slices};}}')
    lines.append('    }')
    lines.append('')

    # ====================================================================
    # Edges: tier1 → tier2 → tier3
    # ====================================================================
    # Tier 1 → tier 2: thin connectors from entry to all its claims
    for i in range(1, 6):
        lines.append(f'    entry_left -> claim_left_{i} [style=dotted, color="#aaa", arrowsize=0.4];')
    for i in range(1, 6):
        lines.append(f'    entry_right -> claim_right_{i} [style=dotted, color="#aaa", arrowsize=0.4];')
    lines.append('')

    # Tier 2 → tier 3: claim → its slice (line thickness ∝ similarity)
    def edge_attrs(c):
        sim = c["sim"]
        # Map [0.4, 0.8] → [1, 4] px
        pen = max(1.0, min(4.0, 1.0 + (sim - 0.4) * 7.5))
        if c["is_primary"]:
            return f'style=solid, penwidth={pen:.1f}, color="#a83232"'
        else:
            return f'style=dashed, penwidth={pen:.1f}, color="#5b6770"'

    for side, data in [("left", left), ("right", right)]:
        for i, c in enumerate(data["top5_claims"], 1):
            slc_node = "slice_" + c["slice"].replace("-", "_")
            attr = edge_attrs(c)
            lines.append(f'    claim_{side}_{i} -> {slc_node} [{attr}];')
    lines.append('')

    # ====================================================================
    # Annotations (right-side text boxes)
    # ====================================================================
    if extra_annotations:
        for i, anno in enumerate(extra_annotations):
            border = "#a83232" if "FAIL" in anno else ("#1f6f3a" if "TRUE" in anno else BORDER_DEFAULT)
            lines.append(
                f'    annotation_{i} [label=<<FONT POINT-SIZE="9">{anno}</FONT>>, '
                f'shape=note, fillcolor="#fffbe6", color="{border}", margin="0.12,0.08"];'
            )

    # Legend
    legend = (
        '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">'
        '<TR><TD COLSPAN="2"><FONT POINT-SIZE="9"><B>Legend</B></FONT></TD></TR>'
        '<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8">━━ primary claim (CO-level pref.)</FONT></TD></TR>'
        '<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8">┄┄ secondary claim (P/M-level)</FONT></TD></TR>'
        '<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8">edge thickness ∝ similarity score</FONT></TD></TR>'
        '<TR><TD ALIGN="LEFT" BGCOLOR="#ffd966"><FONT POINT-SIZE="8">★ frontier intersection slice</FONT></TD></TR>'
        '</TABLE>>'
    )
    lines.append(f'    legend [label={legend}, shape=box, style="rounded", fillcolor="#fafaff", color="#888", fontsize=8];')

    # Close
    lines.append("}")
    return "\n".join(lines)


def render_dot(dot_path: pathlib.Path, formats=("svg", "pdf", "png")):
    base = dot_path.with_suffix("")
    for fmt in formats:
        if fmt == "png":
            out = pathlib.Path(str(base) + "-preview.png")
            args = ["dot", "-Tpng", "-Gdpi=150", str(dot_path), "-o", str(out)]
        else:
            out = pathlib.Path(str(base) + f".{fmt}")
            args = ["dot", f"-T{fmt}", str(dot_path), "-o", str(out)]
        subprocess.run(args, check=True)
        print(f"  [render] {out.name}", file=sys.stderr)


# ============================================================================
# Figure specifications (3 figures)
# ============================================================================

def main():
    sup = json.load(SUPPLIER.open())
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ----- Figure 1: PW.8 / SA-11 (frontier-only match) -----
    fig1_left = derive(find_item(sup, "ssdf_sp800_218_v1_1", "SSDF-PRACTICE-PW.8"))
    fig1_right = derive(find_item(sup, "nist_sp800_53_rev5", "SP800-53-SA-11"))
    if not fig1_left or not fig1_right:
        print("ERR: Figure 1 source items missing", file=sys.stderr)
        sys.exit(1)
    fig1 = emit_dot(
        figure_id="figure-1-pw8-sa11-multi-claim-alignment",
        title="Multi-claim alignment: SSDF PW.8 ↔ SP800-53 SA-11 — frontier match captures alignment that strict misses",
        caption_anchor="P7 §8.2 worked example: programme-lead's hypothesis (multi-claim graph captures semantic alignment that single-primary-CO equality under-reports)",
        left=fig1_left, right=fig1_right,
        frontier_slices=sorted(set(fig1_left["frontier_slices"]) & set(fig1_right["frontier_slices"])),
        match_class="frontier_only",
        extra_annotations=[
            f"Strict primary CO match: <B>FAIL</B> ({fig1_left['primary']['target']} ≠ {fig1_right['primary']['target']})",
            "Slice-primary match: <B>FAIL</B> (different primary slices)",
            "Frontier match: <B>TRUE</B> (multi-claim slice intersection: ACO-TSV)",
        ],
    )
    p1 = OUT_DIR / "figure-1-pw8-sa11-multi-claim-alignment.dot"
    p1.write_text(fig1)
    print(f"[write] {p1.relative_to(REPO)}", file=sys.stderr)
    render_dot(p1)

    # ----- Figure 2: PO.1 / SA-1 (strict match clean baseline) -----
    fig2_left = derive(find_item(sup, "ssdf_sp800_218_v1_1", "SSDF-PRACTICE-PO.1"))
    fig2_right = derive(find_item(sup, "nist_sp800_53_rev5", "SP800-53-SA-1"))
    if not fig2_left or not fig2_right:
        print("ERR: Figure 2 source items missing", file=sys.stderr)
        sys.exit(1)
    fig2 = emit_dot(
        figure_id="figure-2-po1-sa1-strict-match-baseline",
        title="Multi-claim alignment: SSDF PO.1 ↔ SP800-53 SA-1 — strict primary CO match (clean baseline)",
        caption_anchor="P7 §8.2 strict-match worked example: easy alignment case (28/142 = 19.72% of SSDF same-level pairs)",
        left=fig2_left, right=fig2_right,
        frontier_slices=sorted(set(fig2_left["frontier_slices"]) & set(fig2_right["frontier_slices"])),
        match_class="strict",
        extra_annotations=[
            f"Strict primary CO match: <B>TRUE</B> ({fig2_left['primary']['target']} = {fig2_right['primary']['target']})",
            "Frontier also matches (broader slice neighbourhood reinforces alignment)",
        ],
    )
    p2 = OUT_DIR / "figure-2-po1-sa1-strict-match-baseline.dot"
    p2.write_text(fig2)
    print(f"[write] {p2.relative_to(REPO)}", file=sys.stderr)
    render_dot(p2)

    # ----- Figure 3: PO.2 / SCAGILE-OPS-15 (frontier=FALSE, divergence) -----
    fig3_left = derive(find_item(sup, "ssdf_sp800_218_v1_1", "SSDF-PRACTICE-PO.2"))
    fig3_right = derive(find_item(sup, "safecode_agile_2012", "SCAGILE-OPS-15"))
    if not fig3_left or not fig3_right:
        print("ERR: Figure 3 source items missing", file=sys.stderr)
        sys.exit(1)
    fig3 = emit_dot(
        figure_id="figure-3-po2-ops15-genuine-divergence",
        title="Multi-claim alignment: SSDF PO.2 ↔ SCAGILE-OPS-15 — frontier match also FAILS (genuine semantic divergence)",
        caption_anchor="P7 §8.2 honest disclosure: ~5% of SSDF same-level pairs (7/142) exhibit genuine slice-level divergence",
        left=fig3_left, right=fig3_right,
        frontier_slices=sorted(set(fig3_left["frontier_slices"]) & set(fig3_right["frontier_slices"])),
        match_class="different",
        extra_annotations=[
            f"Strict primary CO match: <B>FAIL</B> ({fig3_left['primary']['target']} ≠ {fig3_right['primary']['target']})",
            "Slice-primary match: <B>FAIL</B>",
            "Frontier match: <B>FAIL</B> (slice sets disjoint)",
            "<I>Concept divergence: PO.2 = roles &amp; responsibilities (governance) ≠ OPS-15 = QA testing training</I>",
        ],
    )
    p3 = OUT_DIR / "figure-3-po2-ops15-genuine-divergence.dot"
    p3.write_text(fig3)
    print(f"[write] {p3.relative_to(REPO)}", file=sys.stderr)
    render_dot(p3)

    # Summary
    print(f"\n[done] 3 figures emitted in {OUT_DIR.relative_to(REPO)}", file=sys.stderr)


if __name__ == "__main__":
    main()
