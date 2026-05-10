#!/usr/bin/env python3
"""
consumer_conformance_validator.py — AppSec Core V1 model-invariant SHACL validator.

Parametric validator that any consumer of AppSec Core V1 (Cartographer's
PIPELINE 2 substrate, future Manual KG, MCP plugin, IDE plugin) invokes
against its own normalized claim emission. Enforces the model-side
invariants M1' / M2 (subsumed) / M3 / M4 / M4-card from Decision 0003
Amendment 1 §A — i.e., the constraints AppSec Core V1 itself imposes on
any normalization that claims to be aligned with it.

Architectural boundary:

  - Model invariants (M1' / M2 / M3 / M4 / M4-card) — enforced HERE,
    via the shape graph at
    formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl
    against the consumer's data graph, with the V1 OWL skin loaded as
    ont_graph (non-null — this was one of the four failure layers
    diagnosed in SHACL-SLICE-COMPLETENESS-DIAGNOSIS-2026-05-03.md).

  - Process invariants (M5 semantic warrant, P1' grounded-implies-claim)
    — NOT enforced here. Those are construction-time guarantees of the
    consumer's algorithm, validated by Pydantic / inline assertions /
    unit tests in the consumer's own pipeline. SHACL is the wrong tool
    for them.

Usage (Python API):

    from consumer_conformance_validator import validate_consumer_substrate

    report = validate_consumer_substrate(
        data_graph_path = Path("path/to/consumer-substrate.ttl"),
        report_dir      = Path("path/to/report-out"),
        # optional overrides:
        shapes_path     = None,   # default: ../formal/.../appsec-core-v0-shapes.ttl
        ontology_path   = None,   # default: ../packages/.../appsec-core-v0-bounded-v1.ttl
    )
    print(report.conforms, report.n_violations_total)

Usage (CLI):

    python3 scripts/consumer_conformance_validator.py \\
        --data    path/to/consumer-substrate.ttl \\
        --report  path/to/report-out

The CLI emits two report files into --report dir:
    <basename>-shacl-report.json   structured findings (per-shape counts +
                                   per-violation focus_node + value)
    <basename>-shacl-report.md     human-readable summary

Reproducibility: pyshacl + rdflib are deterministic on the same inputs;
the JSON report is sorted by (source_shape, focus_node) so cross-run
diffs are stable.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pyshacl
import rdflib
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF as RDFNS

# ============================================================
# Defaults — derive from this file's location in sbd-toe-ontology/
# ============================================================

REPO_ROOT = Path(__file__).resolve().parents[1]  # sbd-toe-ontology/

DEFAULT_SHAPES_PATH = (
    REPO_ROOT
    / "formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl"
)
DEFAULT_ONTOLOGY_PATH = (
    REPO_ROOT
    / "packages/ontology/appsec-core/v1.0/formal/appsec-core-v0-bounded-v1.ttl"
)

SH = Namespace("http://www.w3.org/ns/shacl#")
AC = Namespace("https://securitybydesign.dev/ontology/appsec-core/v1#")

# Per-shape descriptive labels for the report (mirrors the .ttl file).
INVARIANT_LABELS: dict[str, str] = {
    str(AC.ClaimWellFormednessShape):
        "M4-card — Claim well-formedness (cardinalities + types)",
    str(AC.SliceCoherenceClaimShape):
        "M1' — Slice coherence on claim (subsumes M2 for CO-level)",
    str(AC.PracticeCOConsistencyShape):
        "M3 — Practice ∈ CO consistency (Practice-level claims)",
    str(AC.MechanismCOConsistencyShape):
        "M4 — Mechanism ∈ CO chain (Mechanism-level claims; gap 1)",
    str(AC.ClaimTargetReferentialIntegrityShape):
        "M4-card / referential integrity — claim target IRI resolves with matching level",
}


# ============================================================
# Report dataclass
# ============================================================

@dataclass
class ConformanceReport:
    """Structured conformance result. Caller serializes via .to_json()."""

    conforms: bool
    n_violations_total: int
    n_violations_per_shape: dict[str, int]
    violations: list[dict[str, Any]]
    inputs: dict[str, str]
    library_versions: dict[str, str]
    generated_at_utc: str
    apparatus_caveat: str = field(default="")

    def to_json(self) -> str:
        return json.dumps(
            {
                "schema": "appsec-core-v1-consumer-conformance-report/1.0",
                "conforms": self.conforms,
                "n_violations_total": self.n_violations_total,
                "n_violations_per_shape": dict(
                    sorted(self.n_violations_per_shape.items())
                ),
                "shape_labels": INVARIANT_LABELS,
                "violations": self.violations,
                "inputs": self.inputs,
                "library_versions": self.library_versions,
                "generated_at_utc": self.generated_at_utc,
                "apparatus_caveat": self.apparatus_caveat,
            },
            indent=2,
            ensure_ascii=False,
        )

    def to_markdown(self) -> str:
        lines: list[str] = []
        verdict = "✅ CONFORMS" if self.conforms else "❌ NON-CONFORMANT"
        lines.append("# AppSec Core V1 — Consumer Conformance Report")
        lines.append("")
        lines.append(f"**Verdict:** {verdict}")
        lines.append(f"**Generated:** {self.generated_at_utc}")
        lines.append(f"**Total violations:** {self.n_violations_total}")
        lines.append("")
        lines.append("## Inputs")
        for k, v in self.inputs.items():
            lines.append(f"- **{k}:** `{v}`")
        lines.append("")
        lines.append("## Per-shape (per-invariant) findings")
        lines.append("")
        lines.append("| Shape | Invariant | Violations |")
        lines.append("|---|---|---:|")
        for shape_iri, label in INVARIANT_LABELS.items():
            count = self.n_violations_per_shape.get(shape_iri, 0)
            lines.append(f"| `{shape_iri}` | {label} | {count} |")
        lines.append("")
        if self.violations:
            lines.append(f"## First violations (up to 25 of {self.n_violations_total})")
            lines.append("")
            lines.append("| # | Shape | Focus node | Value |")
            lines.append("|---:|---|---|---|")
            for i, v in enumerate(self.violations[:25], 1):
                lines.append(
                    f"| {i} | `{v.get('source_shape', '')}` | "
                    f"`{v.get('focus_node', '')}` | "
                    f"`{v.get('value', '') or '—'}` |"
                )
            lines.append("")
        if self.apparatus_caveat:
            lines.append("## Caveat")
            lines.append("")
            lines.append(self.apparatus_caveat)
            lines.append("")
        return "\n".join(lines)


# ============================================================
# Core validation
# ============================================================

def _load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(str(path))  # rdflib auto-detects format from extension
    return g


def validate_consumer_substrate(
    data_graph_path: Path,
    *,
    report_dir: Path | None = None,
    shapes_path: Path | None = None,
    ontology_path: Path | None = None,
    inference: str = "rdfs",
) -> ConformanceReport:
    """Validate a consumer's substrate against the model-invariant shapes.

    Args:
        data_graph_path:
            Path to the consumer's data graph (RDF/Turtle/N-Triples/JSON-LD;
            rdflib auto-detects format from extension).
        report_dir:
            Optional directory to write JSON + MD reports into. If None, no
            files are written; only the in-memory ConformanceReport is
            returned.
        shapes_path:
            Optional override of the consumer-conformance shapes file. Default:
            sbd-toe-ontology/formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl
        ontology_path:
            Optional override of the V1 OWL skin used as ont_graph. Default:
            sbd-toe-ontology/packages/ontology/appsec-core/v1.0/formal/appsec-core-v0-bounded-v1.ttl
        inference:
            pyshacl inference mode. Default "rdfs"; pass "none" to disable.

    Returns:
        ConformanceReport.

    Raises:
        FileNotFoundError if any input path does not exist.
        ValueError if pyshacl reports an internal failure.
    """

    shapes_path = shapes_path or DEFAULT_SHAPES_PATH
    ontology_path = ontology_path or DEFAULT_ONTOLOGY_PATH

    for label, p in (
        ("data_graph", data_graph_path),
        ("shapes", shapes_path),
        ("ontology", ontology_path),
    ):
        if not p.exists():
            raise FileNotFoundError(f"{label} not found at {p}")

    consumer_data_graph = _load_graph(data_graph_path)
    shapes_graph = _load_graph(shapes_path)
    ont_graph = _load_graph(ontology_path)

    # Merge ontology triples into the data graph BEFORE validation.
    # Reason: pyshacl's `ont_graph` parameter feeds RDFS/OWL inference but
    # does NOT expose ontology triples to sh:sparql constraints — those
    # queries only see the `data_graph`. The shape file's M1'/M3/M4 join
    # constraints query for ?target ac:belongsToSlice ?actual_slice etc.,
    # and those triples live in the ontology graph. Merging makes them
    # visible to the SPARQL evaluator. Same merging strategy the apparatus
    # validators use; harmless because ontology triples are read-only and
    # cannot be "violated" by any consumer-emitted claim.
    data_graph = Graph()
    for t in consumer_data_graph:
        data_graph.add(t)
    for t in ont_graph:
        data_graph.add(t)

    # The four failure layers diagnosed by SHACL-SLICE-COMPLETENESS-DIAGNOSIS-
    # 2026-05-03.md were: (1) no shape, (2) wrong target, (3) no join triple,
    # (4) ont_graph=None. We close all four here:
    #   (1) shapes_graph carries the M1'/M3/M4/M4-card targets.
    #   (2) shapes target ac:Claim (the consumer's normalized-item node per
    #       Amendment 1 §D), not ontology classes.
    #   (3) the SPARQL constraints in shapes_graph join via belongsToSlice /
    #       objective_realized_by_practice / objective_implemented_by_mechanism;
    #       these triples live in ont_graph and are merged into data_graph
    #       above so sh:sparql can see them.
    #   (4) ont_graph passed below is non-null (and additionally merged into
    #       the data graph for sh:sparql visibility).
    conforms, results_graph, results_text = pyshacl.validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        ont_graph=ont_graph,
        inference=inference,
        abort_on_first=False,
        meta_shacl=False,
        debug=False,
        advanced=True,  # required for sh:sparql constraints
    )

    # Walk pyshacl's results graph to extract structured per-violation findings.
    violations: list[dict[str, Any]] = []
    n_per_shape: dict[str, int] = {}

    for result_node in results_graph.subjects(
        RDFNS.type, URIRef(f"{SH}ValidationResult")
    ):
        record: dict[str, Any] = {}
        for p, o in results_graph.predicate_objects(result_node):
            p_local = str(p).rsplit("#", 1)[-1]
            if p_local in (
                "focusNode",
                "value",
                "resultPath",
                "sourceShape",
                "sourceConstraintComponent",
                "resultMessage",
                "resultSeverity",
            ):
                record[
                    {
                        "focusNode": "focus_node",
                        "value": "value",
                        "resultPath": "result_path",
                        "sourceShape": "source_shape",
                        "sourceConstraintComponent": "constraint_component",
                        "resultMessage": "message",
                        "resultSeverity": "severity",
                    }[p_local]
                ] = str(o)
        if "source_shape" in record:
            shape = record["source_shape"]
            n_per_shape[shape] = n_per_shape.get(shape, 0) + 1
        violations.append(record)

    # Sort violations for stable diffs across runs.
    violations.sort(key=lambda r: (r.get("source_shape", ""), r.get("focus_node", "")))

    report = ConformanceReport(
        conforms=bool(conforms),
        n_violations_total=len(violations),
        n_violations_per_shape=n_per_shape,
        violations=violations,
        inputs={
            "data_graph": str(data_graph_path),
            "shapes": str(shapes_path),
            "ontology": str(ontology_path),
            "data_triples": str(len(data_graph)),
            "shapes_triples": str(len(shapes_graph)),
            "ontology_triples": str(len(ont_graph)),
        },
        library_versions={
            "pyshacl": pyshacl.__version__,
            "rdflib": rdflib.__version__,
            "python": sys.version.split()[0],
        },
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        apparatus_caveat=(
            "Model-invariant shapes only (M1' / M2 subsumed / M3 / M4 via CO "
            "chain / M4-card). Process-side invariants (M5 semantic warrant, "
            "P1' grounded-implies-claim) are NOT enforced here; consumers "
            "guarantee them by construction (Pydantic + assertions + tests). "
            "Apparatus tag appsec-core-v0-shapes.ttl is NOT modified by this "
            "validator; this file ALONGSIDE it adds claim-targeted shapes "
            "without touching ontology-targeted apparatus shapes."
        ),
    )

    if report_dir is not None:
        report_dir.mkdir(parents=True, exist_ok=True)
        basename = data_graph_path.stem
        (report_dir / f"{basename}-shacl-report.json").write_text(
            report.to_json(), encoding="utf-8"
        )
        (report_dir / f"{basename}-shacl-report.md").write_text(
            report.to_markdown(), encoding="utf-8"
        )

    return report


# ============================================================
# CLI
# ============================================================

def main() -> int:
    p = argparse.ArgumentParser(
        description=(
            "Validate any consumer's AppSec Core V1 normalized substrate "
            "against the model-invariant SHACL shapes (M1' / M3 / M4 / M4-card)."
        )
    )
    p.add_argument(
        "--data",
        required=True,
        type=Path,
        help="Path to the consumer's data graph (Turtle / N-Triples / JSON-LD).",
    )
    p.add_argument(
        "--report",
        required=True,
        type=Path,
        help="Directory to write the JSON + MD conformance reports into.",
    )
    p.add_argument(
        "--shapes",
        type=Path,
        default=None,
        help="Override path to appsec-core-v0-shapes.ttl (default: bundled).",
    )
    p.add_argument(
        "--ontology",
        type=Path,
        default=None,
        help="Override path to AppSec Core V1 OWL skin (default: bundled).",
    )
    p.add_argument(
        "--inference",
        choices=("none", "rdfs", "owlrl", "both"),
        default="rdfs",
        help="pyshacl inference mode (default: rdfs).",
    )
    args = p.parse_args()

    report = validate_consumer_substrate(
        data_graph_path=args.data,
        report_dir=args.report,
        shapes_path=args.shapes,
        ontology_path=args.ontology,
        inference=args.inference,
    )

    verdict = "CONFORMS" if report.conforms else "NON-CONFORMANT"
    print(f"\n{verdict}")
    print(f"  total violations: {report.n_violations_total}")
    if report.n_violations_per_shape:
        print("  per-shape:")
        for shape, n in sorted(report.n_violations_per_shape.items()):
            label = INVARIANT_LABELS.get(shape, shape.rsplit("#", 1)[-1])
            print(f"    {n:5d}  {label}")
    print(f"\n  reports → {args.report}")
    return 0 if report.conforms else 1


if __name__ == "__main__":
    sys.exit(main())
