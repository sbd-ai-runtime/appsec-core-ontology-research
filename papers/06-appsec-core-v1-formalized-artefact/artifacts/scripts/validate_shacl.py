"""Validate the bounded AppSec Core OWL export against the emitted SHACL subset."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from rdflib import BNode, Graph, Literal, RDF, URIRef, XSD
from rdflib.collection import Collection
from rdflib.namespace import RDFS, SH

from .paths import WorkbenchPaths


@dataclass(frozen=True)
class PropertyConstraint:
    path: URIRef
    min_count: int | None
    max_count: int | None
    datatype: URIRef | None
    target_class: URIRef | None
    pattern: str | None
    allowed_values: list[str]


@dataclass(frozen=True)
class ShapeSpec:
    shape: URIRef
    target_class: URIRef
    name: str
    description: str
    constraints: list[PropertyConstraint]


def _as_int(graph: Graph, subject: BNode | URIRef, predicate: URIRef) -> int | None:
    value = graph.value(subject, predicate)
    if value is None:
        return None
    return int(str(value))


def _as_text(graph: Graph, subject: BNode | URIRef, predicate: URIRef) -> str | None:
    value = graph.value(subject, predicate)
    if value is None:
        return None
    return str(value)


def _allowed_values(graph: Graph, subject: BNode | URIRef) -> list[str]:
    head = graph.value(subject, SH["in"])
    if head is None:
        return []
    return [str(item) for item in Collection(graph, head)]


def _load_shapes(shapes_graph: Graph) -> list[ShapeSpec]:
    specs: list[ShapeSpec] = []
    for shape in shapes_graph.subjects(RDF.type, SH.NodeShape):
        if not isinstance(shape, URIRef):
            continue
        target_class = shapes_graph.value(shape, SH.targetClass)
        if not isinstance(target_class, URIRef):
            continue
        name = _as_text(shapes_graph, shape, SH.name) or shape.split("#")[-1]
        description = _as_text(shapes_graph, shape, SH.description) or ""
        constraints: list[PropertyConstraint] = []
        for prop in shapes_graph.objects(shape, SH.property):
            if not isinstance(prop, BNode):
                continue
            path = shapes_graph.value(prop, SH.path)
            if not isinstance(path, URIRef):
                continue
            datatype = shapes_graph.value(prop, SH.datatype)
            target = shapes_graph.value(prop, SH["class"])
            constraints.append(
                PropertyConstraint(
                    path=path,
                    min_count=_as_int(shapes_graph, prop, SH.minCount),
                    max_count=_as_int(shapes_graph, prop, SH.maxCount),
                    datatype=datatype if isinstance(datatype, URIRef) else None,
                    target_class=target if isinstance(target, URIRef) else None,
                    pattern=_as_text(shapes_graph, prop, SH.pattern),
                    allowed_values=_allowed_values(shapes_graph, prop),
                )
            )
        specs.append(
            ShapeSpec(
                shape=shape,
                target_class=target_class,
                name=name,
                description=description,
                constraints=constraints,
            )
        )
    return specs


def _literal_matches_datatype(value: Literal, datatype: URIRef) -> bool:
    if datatype == XSD.string:
        return value.language is None and (value.datatype in {None, XSD.string})
    return value.datatype == datatype


def _validate_constraint(
    data_graph: Graph,
    node: URIRef,
    constraint: PropertyConstraint,
) -> list[str]:
    values = list(data_graph.objects(node, constraint.path))
    violations: list[str] = []
    path_name = str(constraint.path).split("#")[-1]
    node_name = str(node).split("#")[-1]

    if constraint.min_count is not None and len(values) < constraint.min_count:
        violations.append(
            f"{node_name}: property {path_name} requires at least {constraint.min_count} value(s), found {len(values)}."
        )

    if constraint.max_count is not None and len(values) > constraint.max_count:
        violations.append(
            f"{node_name}: property {path_name} allows at most {constraint.max_count} value(s), found {len(values)}."
        )

    for value in values:
        if constraint.datatype:
            if not isinstance(value, Literal) or not _literal_matches_datatype(value, constraint.datatype):
                violations.append(
                    f"{node_name}: property {path_name} must use datatype {constraint.datatype.split('#')[-1]}, got {value!r}."
                )
                continue

        if constraint.target_class:
            if not isinstance(value, URIRef) or (value, RDF.type, constraint.target_class) not in data_graph:
                violations.append(
                    f"{node_name}: property {path_name} must point to an instance of {constraint.target_class.split('#')[-1]}."
                )

        if constraint.pattern and isinstance(value, Literal):
            if not re.match(constraint.pattern, str(value)):
                violations.append(
                    f"{node_name}: property {path_name} value {str(value)!r} does not match pattern {constraint.pattern!r}."
                )

        if constraint.allowed_values and isinstance(value, Literal):
            if str(value) not in constraint.allowed_values:
                allowed = ", ".join(constraint.allowed_values)
                violations.append(
                    f"{node_name}: property {path_name} value {str(value)!r} is outside allowed set [{allowed}]."
                )

    return violations


def validate_generated_assets(paths: WorkbenchPaths) -> dict[str, Any]:
    data_graph_path = paths.owl_exports / "appsec-core-v0-bounded-v1.ttl"
    shapes_graph_path = paths.shacl_shapes / "appsec-core-v0-shapes.ttl"

    if not data_graph_path.exists():
        raise FileNotFoundError(f"Missing OWL export for validation: {data_graph_path}")
    if not shapes_graph_path.exists():
        raise FileNotFoundError(f"Missing SHACL shapes for validation: {shapes_graph_path}")

    data_graph = Graph()
    data_graph.parse(data_graph_path, format="turtle")

    shapes_graph = Graph()
    shapes_graph.parse(shapes_graph_path, format="turtle")

    shape_specs = _load_shapes(shapes_graph)
    violations: list[str] = []
    shape_summaries: list[dict[str, Any]] = []

    for spec in shape_specs:
        targets = sorted(
            {
                node
                for node in data_graph.subjects(RDF.type, spec.target_class)
                if isinstance(node, URIRef)
            },
            key=str,
        )
        shape_violations_before = len(violations)
        for node in targets:
            for constraint in spec.constraints:
                violations.extend(_validate_constraint(data_graph, node, constraint))

        shape_summaries.append(
            {
                "shape": str(spec.shape),
                "shape_name": spec.name,
                "target_class": str(spec.target_class),
                "target_node_count": len(targets),
                "constraint_count": len(spec.constraints),
                "violation_count": len(violations) - shape_violations_before,
            }
        )

    return {
        "status": "conforms" if not violations else "violations_found",
        "validator": "bounded_subset_validator",
        "scope": "AppSec Core v0 bounded OWL/SHACL workbench",
        "data_graph": str(data_graph_path),
        "shapes_graph": str(shapes_graph_path),
        "data_triple_count": len(data_graph),
        "shape_triple_count": len(shapes_graph),
        "shape_count": len(shape_specs),
        "shape_summaries": shape_summaries,
        "violation_count": len(violations),
        "violations": violations,
        "notes": [
            "This validator evaluates the SHACL subset emitted by the local workbench.",
            "Supported constraints: sh:minCount, sh:maxCount, sh:datatype, sh:class, sh:pattern and sh:in.",
            "It is sufficient for the bounded generated shape set, but it is not a general-purpose SHACL engine.",
        ],
    }


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# AppSec Core SHACL Validation Report",
        "",
        f"- Status: `{summary['status']}`",
        f"- Validator: `{summary['validator']}`",
        f"- Scope: `{summary['scope']}`",
        f"- Data graph: `{summary['data_graph']}`",
        f"- Shapes graph: `{summary['shapes_graph']}`",
        f"- Data triples: {summary['data_triple_count']}",
        f"- Shape triples: {summary['shape_triple_count']}",
        f"- Shapes: {summary['shape_count']}",
        f"- Violations: {summary['violation_count']}",
        "",
        "## Notes",
        "",
    ]
    lines.extend(f"- {note}" for note in summary["notes"])
    lines.extend(
        [
            "",
            "## Shape Coverage",
            "",
        ]
    )
    for item in summary["shape_summaries"]:
        lines.append(
            f"- `{item['shape_name']}` targets {item['target_node_count']} node(s), "
            f"applies {item['constraint_count']} constraint(s), "
            f"violations: {item['violation_count']}"
        )
    lines.extend(
        [
            "",
            "## Violations",
            "",
        ]
    )
    if summary["violations"]:
        lines.extend(f"- {message}" for message in summary["violations"])
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def write_validation_report(paths: WorkbenchPaths) -> tuple[Path, Path, dict[str, Any]]:
    summary = validate_generated_assets(paths)
    report_dir = paths.validation_reports
    report_dir.mkdir(parents=True, exist_ok=True)

    json_path = report_dir / "appsec-core-v0-shacl-validation-summary.json"
    md_path = report_dir / "appsec-core-v0-shacl-validation-report.md"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=False), encoding="utf-8")
    md_path.write_text(_render_markdown(summary), encoding="utf-8")
    return json_path, md_path, summary
