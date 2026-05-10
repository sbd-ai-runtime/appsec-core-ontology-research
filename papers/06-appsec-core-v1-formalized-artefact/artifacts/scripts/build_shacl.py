"""Build a bounded SHACL/Turtle shape set for AppSec Core v0.

REGENERATION SCOPE (architectural commitment, programme-lead 2026-05-05 — Option C)
----------------------------------------------------------------------------------

This module regenerates ONLY ``appsec-core-v0-shapes.ttl`` — the 6
schema-derived ontology shapes (SliceShape / ControlObjectiveShape /
PracticeShape / MechanismShape / ArtifactShape / EvidencePatternShape).
Source of truth: the AppSec Core YAML schema + per-slice instance drafts.

It MUST NOT touch ``consumer-conformance-shapes.ttl``, which lives
alongside in ``formal/appsec_core/03-shacl/shapes/`` and contains the 5
hand-maintained Claim shapes (M1' / M3 / M4 via CO chain / M4-card
cardinality / M4-card referential integrity) derived from Decision 0003 +
Amendment 1 model invariants. That file is ontology-owned, hand-maintained
by Archon, and updated only via cross-persona dispatcher when Decision
0003 receives an amendment that alters model invariants.

Apparatus tags (``apparatus-shacl-pyshacl-vN``) declare composition of both
files explicitly; pyshacl runners merge them as a single shapes graph
before validation.

Background: commit ``7ee0373`` regenerated ``appsec-core-v0-shapes.ttl``
from scratch via this module and stripped the 5 claim shapes that
apparatus-v2 (``ee73c19``) had consolidated. The Option C ratification on
2026-05-05 split the two concerns into separate files; this docstring
preserves the regen-safety boundary.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .source_bundle import SourceBundle


ID_PROPERTY_BY_CLASS = {
    "ControlObjective": "objective_id",
    "Practice": "practice_id",
    "Mechanism": "mechanism_id",
    "Artifact": "artifact_id",
    "EvidencePattern": "evidence_pattern_id",
}

ID_PATTERN_BY_CLASS = {
    "Slice": r"^ASC-[0-9]{2}$",
    "ControlObjective": r"^ACO-[A-Z]+-[0-9]{3}$",
    "Practice": r"^ACP-[A-Z]+-[0-9]{3}$",
    "Mechanism": r"^ACM-[A-Z]+-[0-9]{3}$",
    "Artifact": r"^ACA-[A-Z]+-[0-9]{3}$",
}

OPTIONAL_LABEL_PROPERTIES = (
    ("ac:shortLabel", "xsd:string"),
    ("ac:diagramLabel", "xsd:string"),
)

RELATION_TARGETS = {
    "objective_realized_by_practice": "Practice",
    "objective_implemented_by_mechanism": "Mechanism",
    "objective_expects_artifact": "Artifact",
    "objective_verified_by_evidence_pattern": "EvidencePattern",
    "artifact_supports_evidence_pattern": "EvidencePattern",
}


def _literal(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _entity_comments(bundle: SourceBundle) -> dict[str, str]:
    comments: dict[str, str] = {}
    core_entities = bundle.entity_schema.get("core_entities", {})
    for entity_name, entity_body in core_entities.items():
        if isinstance(entity_body, dict):
            comments[str(entity_name)] = str(entity_body.get("role", "")).strip()
    return comments


def _required_fields(bundle: SourceBundle) -> dict[str, list[str]]:
    required: dict[str, list[str]] = {}
    core_entities = bundle.entity_schema.get("core_entities", {})
    for entity_name, entity_body in core_entities.items():
        if isinstance(entity_body, dict):
            required[str(entity_name)] = [str(value) for value in entity_body.get("required_fields", [])]
    return required


def _stable_relations(bundle: SourceBundle) -> list[str]:
    relation_schema = bundle.entity_schema.get("relation_schema", {})
    return [str(value) for value in relation_schema.get("stable_core_relations", [])]


def _first_class_entities(bundle: SourceBundle) -> list[str]:
    boundary = bundle.surface_contract.get("entity_boundary", {})
    return [str(value) for value in boundary.get("first_class_for_v0", [])]


def _current_control_modes(bundle: SourceBundle) -> list[str]:
    modes: set[str] = set()
    registry = bundle.slice_registry.get("registry", {})
    for slice_record in registry.get("slices", []):
        if not isinstance(slice_record, dict):
            continue
        mode = str(slice_record.get("current_control_mode", "")).strip()
        if mode:
            modes.add(mode)
    return sorted(modes)


def _property_block(
    *,
    path: str,
    datatype: str | None = None,
    target_class: str | None = None,
    min_count: int | None = None,
    max_count: int | None = None,
    pattern: str | None = None,
    in_values: list[str] | None = None,
    description: str | None = None,
) -> list[str]:
    lines = [
        "    sh:property [",
        f"        sh:path {path} ;",
    ]
    if datatype:
        lines.append(f"        sh:datatype {datatype} ;")
    if target_class:
        lines.append(f"        sh:class ac:{target_class} ;")
    if min_count is not None:
        lines.append(f"        sh:minCount {min_count} ;")
    if max_count is not None:
        lines.append(f"        sh:maxCount {max_count} ;")
    if pattern:
        lines.append(f"        sh:pattern {_literal(pattern)} ;")
    if in_values:
        rendered = " ".join(_literal(value) for value in in_values)
        lines.append(f"        sh:in ( {rendered} ) ;")
    if description:
        lines.append(f"        sh:description {_literal(description)} ;")
    lines.append("    ] ;")
    return lines


def _shape_header(target_class: str, shape_name: str, description: str) -> list[str]:
    return [
        f"ac:{shape_name} a sh:NodeShape ;",
        f"    sh:targetClass ac:{target_class} ;",
        f"    sh:name {_literal(shape_name)} ;",
        f"    sh:description {_literal(description)} ;",
    ]


def _common_label_blocks() -> list[list[str]]:
    blocks = [
        _property_block(
            path="rdfs:label",
            datatype="xsd:string",
            min_count=1,
            max_count=1,
            description="Human-readable canonical label for the bounded formal cut.",
        )
    ]
    for predicate, datatype in OPTIONAL_LABEL_PROPERTIES:
        blocks.append(
            _property_block(
                path=predicate,
                datatype=datatype,
                max_count=1,
                description="Optional compact presentation label.",
            )
        )
    return blocks


def _slice_shape_blocks(bundle: SourceBundle) -> list[str]:
    lines = _shape_header(
        "Slice",
        "SliceShape",
        "Validates slice registry instances in the bounded AppSec Core v0 formal cut.",
    )
    property_blocks: list[list[str]] = []
    property_blocks.extend(_common_label_blocks())
    property_blocks.append(
        _property_block(
            path="ac:slice_id",
            datatype="xsd:string",
            min_count=1,
            max_count=1,
            pattern=ID_PATTERN_BY_CLASS["Slice"],
            description="Stable slice identifier.",
        )
    )
    property_blocks.append(
        _property_block(
            path="ac:scope_key",
            datatype="xsd:string",
            min_count=1,
            max_count=1,
            description="Canonical scope key for the slice.",
        )
    )
    property_blocks.append(
        _property_block(
            path="ac:objective_family_code",
            datatype="xsd:string",
            min_count=1,
            max_count=1,
            pattern=r"^ACO-[A-Z]+$",
            description="Objective family code attached to the slice.",
        )
    )
    property_blocks.append(
        _property_block(
            path="ac:current_control_mode",
            datatype="xsd:string",
            min_count=1,
            max_count=1,
            in_values=_current_control_modes(bundle),
            description="Current control packaging mode declared in the slice registry.",
        )
    )
    property_blocks.append(
        _property_block(
            path="ac:contract_path",
            datatype="xsd:string",
            min_count=1,
            max_count=1,
            pattern=r"^ontology/appsec-core-.*\.yaml$",
            description="Relative path to the governing slice contract.",
        )
    )

    for block in property_blocks:
        lines.extend(block)
    lines[-1] = lines[-1].rstrip(";")
    lines.append("    .")
    lines.append("")
    return lines


def _entity_shape_blocks(bundle: SourceBundle, entity_name: str) -> list[str]:
    comments = _entity_comments(bundle)
    required_fields = _required_fields(bundle)
    stable_relations = _stable_relations(bundle)

    description = comments.get(entity_name) or f"Validates bounded {entity_name} instances."
    lines = _shape_header(entity_name, f"{entity_name}Shape", description)

    property_blocks: list[list[str]] = []
    property_blocks.extend(_common_label_blocks())

    id_property = ID_PROPERTY_BY_CLASS.get(entity_name)
    if id_property:
        property_blocks.append(
            _property_block(
                path=f"ac:{id_property}",
                datatype="xsd:string",
                min_count=1,
                max_count=1,
                pattern=ID_PATTERN_BY_CLASS.get(entity_name),
                description="Stable canonical identifier.",
            )
        )

    property_blocks.append(
        _property_block(
            path="ac:belongsToSlice",
            target_class="Slice",
            min_count=1,
            max_count=1,
            description="Slice membership in the bounded formal cut.",
        )
    )

    if entity_name == "ControlObjective":
        property_blocks.append(
            _property_block(
                path="ac:hasObjectiveKind",
                target_class="ObjectiveKind",
                max_count=1,
                description="Optional objective kind binding when the bounded export is enriched.",
            )
        )
        property_blocks.append(
            _property_block(
                path="ac:hasObjectiveType",
                target_class="ObjectiveType",
                max_count=1,
                description="Optional objective type binding when the bounded export is enriched.",
            )
        )
        for relation_name in stable_relations:
            target = RELATION_TARGETS.get(relation_name)
            if not target or not relation_name.startswith("objective_"):
                continue
            if relation_name in (
                "objective_realized_by_practice",
                "objective_implemented_by_mechanism",
            ):
                property_blocks.append(
                    _property_block(
                        path=f"ac:{relation_name}",
                        target_class=target,
                        min_count=1,
                        description=(
                            "Each ControlObjective must be constitutively linked "
                            f"to at least one {target.lower()}."
                        ),
                    )
                )
            else:
                property_blocks.append(
                    _property_block(
                        path=f"ac:{relation_name}",
                        target_class=target,
                        description="Optional stable cross-entity relation in the bounded model.",
                    )
                )

    if entity_name == "Practice":
        property_blocks.append(
            _property_block(
                path="ac:hasPracticeFamily",
                target_class="PracticeFamily",
                max_count=1,
                description="Optional practice family binding when the bounded export is enriched.",
            )
        )

    if entity_name == "Mechanism":
        property_blocks.append(
            _property_block(
                path="ac:hasMechanismFamily",
                target_class="MechanismFamily",
                max_count=1,
                description="Optional mechanism family binding when the bounded export is enriched.",
            )
        )

    if entity_name == "Artifact":
        property_blocks.append(
            _property_block(
                path="ac:hasCanonicalArtifactRole",
                target_class="ArtifactRole",
                max_count=1,
                description="Optional artifact role binding when the bounded export is enriched.",
            )
        )
        if "artifact_supports_evidence_pattern" in stable_relations:
            property_blocks.append(
                _property_block(
                    path="ac:artifact_supports_evidence_pattern",
                    target_class="EvidencePattern",
                    description="Optional artifact-to-evidence relation in the bounded model.",
                )
            )

    if entity_name == "EvidencePattern":
        if "expectation" in required_fields.get(entity_name, []):
            property_blocks.append(
                _property_block(
                    path="ac:expectation",
                    datatype="xsd:string",
                    min_count=1,
                    max_count=1,
                    description="Expected evidence statement.",
                )
            )
        if "validation_method" in required_fields.get(entity_name, []):
            property_blocks.append(
                _property_block(
                    path="ac:validation_method",
                    datatype="xsd:string",
                    min_count=1,
                    max_count=1,
                    description="Validation method description.",
                )
            )
        property_blocks.append(
            _property_block(
                path="ac:hasCanonicalEvidenceKind",
                target_class="ArtifactRole",
                max_count=1,
                description="Optional canonical evidence-kind binding when evidence patterns are materialized.",
            )
        )
        property_blocks.append(
            _property_block(
                path="ac:detectableInSurface",
                target_class="DetectableSurface",
                description="Optional detectable surface binding when evidence patterns are materialized.",
            )
        )

    for block in property_blocks:
        lines.extend(block)
    lines[-1] = lines[-1].rstrip(";")
    lines.append("    .")
    lines.append("")
    return lines


def render_shacl_starter(bundle: SourceBundle) -> str:
    lines = [
        "@prefix ac: <https://securitybydesign.dev/ontology/appsec-core/v1#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix sh: <http://www.w3.org/ns/shacl#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "",
        "ac:AppSecCoreV1ShapeSet a sh:NodeShape ;",
        '    sh:name "AppSecCoreV1ShapeSet" ;',
        '    sh:description "Bounded SHACL shape set for the AppSec Core v1.0 formal cut." ;',
        '    sh:message "Validates the slice and first-class instance surface emitted by the AppSec Core v1.0 formal workbench." .',
        "",
    ]

    lines.extend(_slice_shape_blocks(bundle))
    for entity_name in _first_class_entities(bundle):
        lines.extend(_entity_shape_blocks(bundle, entity_name))

    return "\n".join(lines)


def write_shacl_starter(bundle: SourceBundle, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "appsec-core-v0-shapes.ttl"
    output_path.write_text(render_shacl_starter(bundle), encoding="utf-8")
    return output_path
