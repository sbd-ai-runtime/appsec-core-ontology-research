"""Build a bounded OWL/Turtle formalization for AppSec Core v0."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .source_bundle import SourceBundle


RELATION_DOMAIN_RANGE = {
    "objective_realized_by_practice": ("ControlObjective", "Practice"),
    "objective_implemented_by_mechanism": ("ControlObjective", "Mechanism"),
    "objective_expects_artifact": ("ControlObjective", "Artifact"),
    "objective_verified_by_evidence_pattern": ("ControlObjective", "EvidencePattern"),
    "artifact_supports_evidence_pattern": ("Artifact", "EvidencePattern"),
}

CLASS_LABEL_OVERRIDES = {
    "AppSecCoreEntity": "AppSec Core entity",
    "ControlledVocabularyValue": "Controlled vocabulary value",
    "Slice": "Slice",
    "ObjectiveKind": "Objective kind",
    "ObjectiveType": "Objective type",
    "ArtifactRole": "Artifact role",
    "PracticeFamily": "Practice family",
    "MechanismFamily": "Mechanism family",
    "DetectableSurface": "Detectable surface",
    "ControlObjective": "Control objective",
    "Practice": "Practice",
    "Mechanism": "Mechanism",
    "Artifact": "Artifact",
    "EvidencePattern": "Evidence pattern",
}

ACRONYM_MAP = {
    "api": "API",
    "appsec": "AppSec",
    "cd": "CD",
    "ci": "CI",
    "dfd": "DFD",
    "iac": "IaC",
    "id": "ID",
    "oidc": "OIDC",
    "sast": "SAST",
    "sbom": "SBOM",
    "sca": "SCA",
    "sdlc": "SDLC",
}

LOWERCASE_CONNECTORS = {"and", "by", "for", "in", "of", "or", "to", "with"}


def _literal(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _sanitize_local_name(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    if not normalized:
        normalized = "unnamed"
    if normalized[0].isdigit():
        normalized = f"N_{normalized}"
    return normalized


def _camelize(value: str) -> str:
    sanitized = _sanitize_local_name(value)
    parts = [part for part in sanitized.split("_") if part]
    if not parts:
        return "Unnamed"
    return "".join(part[:1].upper() + part[1:] for part in parts)


def _triple_block(subject: str, rdf_type: str, properties: list[tuple[str, str, bool]]) -> list[str]:
    lines = [f"{subject} a {rdf_type} ;"]
    for index, (predicate, obj, is_literal) in enumerate(properties):
        rendered_obj = _literal(obj) if is_literal else obj
        suffix = " ." if index == len(properties) - 1 else " ;"
        lines.append(f"    {predicate} {rendered_obj}{suffix}")
    lines.append("")
    return lines


def _annotation_block(subject: str, properties: list[tuple[str, str, bool]]) -> list[str]:
    lines = [f"{subject}"]
    for index, (predicate, obj, is_literal) in enumerate(properties):
        rendered_obj = _literal(obj) if is_literal else obj
        suffix = " ." if index == len(properties) - 1 else " ;"
        lines.append(f"    {predicate} {rendered_obj}{suffix}")
    lines.append("")
    return lines


def _split_words(value: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    return [token for token in re.split(r"[^A-Za-z0-9]+", spaced) if token]


def _humanize_value(value: str, *, title_case: bool) -> str:
    tokens = _split_words(value)
    if not tokens:
        return value

    rendered: list[str] = []
    index = 0
    while index < len(tokens):
        current = tokens[index].lower()
        following = tokens[index + 1].lower() if index + 1 < len(tokens) else None

        if current == "ci" and following == "cd":
            rendered.append("CI/CD")
            index += 2
            continue

        mapped = ACRONYM_MAP.get(current)
        if mapped:
            rendered.append(mapped)
        elif title_case and rendered and current in LOWERCASE_CONNECTORS:
            rendered.append(current)
        elif title_case:
            rendered.append(current.capitalize())
        else:
            rendered.append(current)
        index += 1

    return " ".join(rendered).strip()


def _catalog_item(bundle: SourceBundle, entity_type: str, identifier: str) -> dict[str, Any] | None:
    return bundle.label_catalog.get((entity_type, identifier))


def _catalog_label(bundle: SourceBundle, entity_type: str, identifier: str) -> str | None:
    item = _catalog_item(bundle, entity_type, identifier)
    if not item:
        return None
    label = str(item.get("canonical_label", "")).strip()
    return label or None


def _catalog_short_label(bundle: SourceBundle, entity_type: str, identifier: str) -> str | None:
    item = _catalog_item(bundle, entity_type, identifier)
    if not item:
        return None
    label = str(item.get("canonical_short_label", "")).strip()
    return label or None


def _catalog_diagram_label(bundle: SourceBundle, entity_type: str, identifier: str) -> str | None:
    item = _catalog_item(bundle, entity_type, identifier)
    if not item:
        return None
    render = item.get("render", {})
    if not isinstance(render, dict):
        return None
    label = str(render.get("diagram_label", "")).strip()
    return label or None


def _first_class_entities(bundle: SourceBundle) -> list[str]:
    boundary = bundle.surface_contract.get("entity_boundary", {})
    return [str(value) for value in boundary.get("first_class_for_v0", [])]


# P20 fix (Phase C 2026-05-10): override snake_case role strings with
# natural-language descriptions for first-class entity classes. OOPS!
# flagged ControlObjective + EvidencePattern as "Misusing ontology annotations"
# because the YAML schema role field is snake_case enum-shaped, not prose.
ENTITY_COMMENT_OVERRIDES = {
    "ControlObjective": "Reusable AppSec domain constraint or assurance goal that expresses what must hold true in the application security domain, without carrying SbD-ToE manual chapter or requirement structure.",
    "Practice": "Reusable human or process discipline that should exist independently of a specific tool or runtime product choice, and that helps realise one or more ControlObjective instances.",
    "Mechanism": "Concrete technical or enforceable means used to implement Practice instances or to directly realise ControlObjective instances.",
    "Artifact": "Control-relevant or evidence-bearing output used for review, traceability and assurance against AppSec Core ControlObjective instances.",
    "EvidencePattern": "Expected evidence shape used for deterministic review support of AppSec Core ControlObjective satisfaction; declarative first-class class with no populated instances in the bounded V1 cut (target_node_count=0 at V1 release).",
}


def _entity_comments(bundle: SourceBundle) -> dict[str, str]:
    comments: dict[str, str] = {}
    core_entities = bundle.entity_schema.get("core_entities", {})
    for entity_name, entity_body in core_entities.items():
        name = str(entity_name)
        if name in ENTITY_COMMENT_OVERRIDES:
            comments[name] = ENTITY_COMMENT_OVERRIDES[name]
        elif isinstance(entity_body, dict):
            # Fallback: humanize the snake_case role to natural language.
            role = str(entity_body.get("role", "")).strip()
            if role:
                humanized = role.replace("_", " ")
                comments[name] = humanized[:1].upper() + humanized[1:] + "."
            else:
                comments[name] = ""
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


def _stable_artifact_roles(bundle: SourceBundle) -> list[str]:
    return [
        str(value)
        for value in bundle.entity_schema.get("cross_slice_families", {}).get(
            "canonical_artifact_roles", []
        )
    ]


def _practice_families(bundle: SourceBundle) -> list[str]:
    return [
        str(value)
        for value in bundle.entity_schema.get("cross_slice_families", {}).get("practice_families", [])
    ]


def _mechanism_families(bundle: SourceBundle) -> list[str]:
    return [
        str(value)
        for value in bundle.entity_schema.get("cross_slice_families", {}).get("mechanism_families", [])
    ]


def _detectable_surfaces(bundle: SourceBundle) -> list[str]:
    return [
        str(value)
        for value in bundle.evidence_pattern_contract.get("normalization_rules", {})
        .get("detectable_surface_read", {})
        .get("stable_now", [])
    ]


def _slice_records(bundle: SourceBundle) -> list[dict[str, Any]]:
    registry = bundle.slice_registry.get("registry", {})
    slices = registry.get("slices", [])
    return [item for item in slices if isinstance(item, dict)]


def _instance_slice_records(bundle: SourceBundle) -> list[dict[str, Any]]:
    records = bundle.instance_index.get("slice_instances", [])
    return [item for item in records if isinstance(item, dict)]


def _class_label(name: str) -> str:
    return CLASS_LABEL_OVERRIDES.get(name, _humanize_value(name, title_case=True))


def _property_label(name: str) -> str:
    return _humanize_value(name, title_case=False)


def _value_label(value: str) -> str:
    return _humanize_value(value, title_case=True)


def _controlled_vocab_individuals(
    values: list[str],
    class_name: str,
    local_prefix: str,
    comment: str | None = None,
) -> list[list[str]]:
    blocks: list[list[str]] = []
    for value in values:
        subject = f"ac:{local_prefix}{_camelize(value)}"
        properties = [("rdfs:label", _value_label(value), True)]
        if comment:
            properties.append(("rdfs:comment", comment, True))
        blocks.append(_triple_block(subject, f"ac:{class_name}", properties))
    return blocks


def _slice_local_name(slice_id: str) -> str:
    return f"Slice{_camelize(slice_id)}"


def _entity_instance_label(bundle: SourceBundle, class_name: str, code: str) -> str:
    catalog_label = _catalog_label(bundle, class_name, code)
    if catalog_label:
        return catalog_label
    source_label = bundle.source_entity_labels.get(code)
    if source_label:
        return source_label
    return code


def _entity_instance_blocks(bundle: SourceBundle) -> list[list[str]]:
    blocks: list[list[str]] = []
    entity_mappings = {
        "control_objectives": ("ControlObjective", "objective_id"),
        "practices": ("Practice", "practice_id"),
        "mechanisms": ("Mechanism", "mechanism_id"),
        "artifacts": ("Artifact", "artifact_id"),
    }

    for slice_record in _instance_slice_records(bundle):
        slice_id = str(slice_record.get("slice_id"))
        slice_ref = f"ac:{_slice_local_name(slice_id)}"
        for key, (class_name, id_property) in entity_mappings.items():
            for raw_id in slice_record.get(key, []):
                code = str(raw_id)
                subject = f"ac:{_sanitize_local_name(code)}"
                properties = [
                    ("rdfs:label", _entity_instance_label(bundle, class_name, code), True),
                    (f"ac:{id_property}", code, True),
                    ("ac:belongsToSlice", slice_ref, False),
                ]
                short_label = _catalog_short_label(bundle, class_name, code)
                if short_label:
                    properties.append(("ac:shortLabel", short_label, True))
                diagram_label = _catalog_diagram_label(bundle, class_name, code)
                if diagram_label:
                    properties.append(("ac:diagramLabel", diagram_label, True))
                if class_name == "ControlObjective":
                    for practice_code in bundle.co_to_practices.get(code, []):
                        properties.append(
                            (
                                "ac:objective_realized_by_practice",
                                f"ac:{_sanitize_local_name(practice_code)}",
                                False,
                            )
                        )
                    for mechanism_code in bundle.co_to_mechanisms.get(code, []):
                        properties.append(
                            (
                                "ac:objective_implemented_by_mechanism",
                                f"ac:{_sanitize_local_name(mechanism_code)}",
                                False,
                            )
                        )
                    for artifact_code in bundle.co_to_artifacts.get(code, []):
                        properties.append(
                            (
                                "ac:objective_expects_artifact",
                                f"ac:{_sanitize_local_name(artifact_code)}",
                                False,
                            )
                        )
                blocks.append(_triple_block(subject, f"ac:{class_name}", properties))
    return blocks


def render_owl_starter(bundle: SourceBundle) -> str:
    entity_comments = _entity_comments(bundle)
    required_fields = _required_fields(bundle)
    first_class_entities = _first_class_entities(bundle)
    stable_relations = _stable_relations(bundle)
    version = str(bundle.surface_contract.get("meta", {}).get("version", "1.0"))
    ontology_comment = (
        "Bounded AppSec Core v1.0 OWL cut generated from the canonical surface contract, "
        "entity schema, cross-slice vocabulary, slice registry, global instance index, "
        "human-readable label catalog and source slice drafts. "
        "This cut covers first-class v1.0 entities, constitutive CO-Practice and "
        "CO-Mechanism relations, stable controlled vocabularies, ten slices and the "
        "full indexed instance set (74 COs, 68 Practices, 57 Mechanisms, 57 Artifacts)."
    )

    lines = [
        "@prefix ac: <https://securitybydesign.dev/ontology/appsec-core/v1#> .",
        "@prefix adms: <http://www.w3.org/ns/adms#> .",
        "@prefix cc: <http://creativecommons.org/ns#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix foaf: <http://xmlns.com/foaf/0.1/> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix vann: <http://purl.org/vocab/vann/> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "",
        "ac:AppSecCoreV1 a owl:Ontology ;",
        f"    rdfs:label {_literal('AppSec Core v1.1 bounded ontology cut')} ;",
        f"    rdfs:comment {_literal(ontology_comment)} ;",
        f"    dcterms:title {_literal('AppSec Core V1 — Application Security Control Objective Ontology')} ;",
        f"    dcterms:description {_literal(ontology_comment)} ;",
        f"    owl:versionInfo {_literal(version)} ;",
        f"    owl:versionIRI <https://securitybydesign.dev/ontology/appsec-core/v1.1> ;",
        f"    vann:preferredNamespacePrefix {_literal('ac')} ;",
        f"    vann:preferredNamespaceUri {_literal('https://securitybydesign.dev/ontology/appsec-core/v1#')} ;",
        f"    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;",
        f"    dcterms:rights {_literal('Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). See LICENSE in source repository.')} ;",
        f"    dcterms:creator {_literal('Pedro Farinha (programme-lead, SecurityByDesign-TheoryOfEverything)')} ;",
        f"    dcterms:publisher {_literal('SecurityByDesign-TheoryOfEverything programme')} ;",
        f"    dcterms:created {_literal('2026-04-15')}^^xsd:date ;",
        f"    dcterms:issued {_literal('2026-05-08')}^^xsd:date ;",
        f"    dcterms:modified {_literal('2026-05-10')}^^xsd:date ;",
        f"    dcterms:bibliographicCitation {_literal('Farinha, P. (2026). AppSec Core V1: A Normalization Ontology for Application Security Control Objectives. SecurityByDesign-TheoryOfEverything programme.')} ;",
        f"    foaf:depiction <https://securitybydesign.dev/assets/appsec-core-v1-logo.svg> ;",
        f"    adms:status <http://purl.org/adms/status/Completed> ;",
        f"    dcterms:source {_literal('canonical AppSec Core YAML surfaces in sbd-toe-ontology')} .",
        "",
        "ac:shortLabel a owl:AnnotationProperty ;",
        f"    rdfs:label {_literal('short label')} ;",
        f"    rdfs:comment {_literal('Human-friendly short label for compact views.')} .",
        "",
        "ac:diagramLabel a owl:AnnotationProperty ;",
        f"    rdfs:label {_literal('diagram label')} ;",
        f"    rdfs:comment {_literal('Compact label intended for diagrams or tight visual layouts.')} .",
        "",
        "ac:AppSecCoreEntity a owl:Class ;",
        f"    rdfs:label {_literal(_class_label('AppSecCoreEntity'))} ;",
        f"    rdfs:comment {_literal('Superclass for first-class AppSec Core v0 entities in the bounded formal cut.')} .",
        "",
        "ac:ControlledVocabularyValue a owl:Class ;",
        f"    rdfs:label {_literal(_class_label('ControlledVocabularyValue'))} ;",
        f"    rdfs:comment {_literal('Superclass for stable controlled vocabulary values explicitly modeled in the bounded formal cut.')} ;",
        "    owl:disjointWith ac:AppSecCoreEntity .",
        "",
        "ac:Slice a owl:Class ;",
        f"    rdfs:label {_literal(_class_label('Slice'))} ;",
        f"    rdfs:comment {_literal('Methodological slice in the AppSec Core v0 reference set.')} .",
        "",
        "ac:ObjectiveKind a owl:Class ;",
        "    rdfs:subClassOf ac:ControlledVocabularyValue ;",
        f"    rdfs:label {_literal(_class_label('ObjectiveKind'))} ;",
        f"    rdfs:comment {_literal('Enumeration of ControlObjective kinds (atomic or composite).')} .",
        "",
        "ac:ObjectiveType a owl:Class ;",
        "    rdfs:subClassOf ac:ControlledVocabularyValue ;",
        f"    rdfs:label {_literal(_class_label('ObjectiveType'))} ;",
        f"    rdfs:comment {_literal('Enumeration of ControlObjective types (governance/preventive/detective/corrective).')} .",
        "",
        "ac:ArtifactRole a owl:Class ;",
        "    rdfs:subClassOf ac:ControlledVocabularyValue ;",
        f"    rdfs:label {_literal(_class_label('ArtifactRole'))} ;",
        f"    rdfs:comment {_literal('Cross-slice canonical roles for Artifact instances (e.g. configuration, governance_record, report).')} .",
        "",
        "ac:PracticeFamily a owl:Class ;",
        "    rdfs:subClassOf ac:ControlledVocabularyValue ;",
        f"    rdfs:label {_literal(_class_label('PracticeFamily'))} ;",
        f"    rdfs:comment {_literal('Cross-slice family qualifiers for Practice instances (e.g. governance_and_review, validation_and_analysis).')} .",
        "",
        "ac:MechanismFamily a owl:Class ;",
        "    rdfs:subClassOf ac:ControlledVocabularyValue ;",
        f"    rdfs:label {_literal(_class_label('MechanismFamily'))} ;",
        f"    rdfs:comment {_literal('Cross-slice family qualifiers for Mechanism instances (e.g. policy_and_gate_enforcement, validation_and_analysis).')} .",
        "",
        "ac:DetectableSurface a owl:Class ;",
        "    rdfs:subClassOf ac:ControlledVocabularyValue ;",
        f"    rdfs:label {_literal(_class_label('DetectableSurface'))} ;",
        f"    rdfs:comment {_literal('Operational surface where an EvidencePattern is expected to be detectable.')} .",
        "",
    ]

    for entity_name in first_class_entities:
        comment = entity_comments.get(entity_name, "")
        lines.extend(
            _triple_block(
                f"ac:{entity_name}",
                "owl:Class",
                [
                    ("rdfs:subClassOf", "ac:AppSecCoreEntity", False),
                    ("rdfs:label", _class_label(entity_name), True),
                    ("rdfs:comment", comment, True),
                ],
            )
        )

    if first_class_entities:
        disjoint = " ".join(f"ac:{entity_name}" for entity_name in first_class_entities)
        lines.extend(
            [
                "[] a owl:AllDisjointClasses ;",
                f"    owl:members ( {disjoint} ) .",
                "",
            ]
        )

    # P08 fix (Phase C 2026-05-10): rdfs:comment added per property for VOC4 coverage.
    # P13 fix (Phase C 2026-05-10): owl:inverseOf declared per pair where semantically appropriate.
    lines.extend(
        [
            "ac:belongsToSlice a owl:ObjectProperty ;",
            "    rdfs:domain ac:AppSecCoreEntity ;",
            "    rdfs:range ac:Slice ;",
            f"    rdfs:label {_literal(_property_label('belongsToSlice'))} ;",
            f"    rdfs:comment {_literal('Membership relation from an AppSec Core entity instance to its methodological slice (ASC-NN).')} ;",
            "    owl:inverseOf ac:hasMember .",
            "",
            "ac:hasMember a owl:ObjectProperty ;",
            "    rdfs:domain ac:Slice ;",
            "    rdfs:range ac:AppSecCoreEntity ;",
            f"    rdfs:label {_literal('has member')} ;",
            f"    rdfs:comment {_literal('Inverse of ac:belongsToSlice; relates a Slice to the AppSec Core entity instances it contains.')} .",
            "",
            "ac:hasObjectiveKind a owl:ObjectProperty ;",
            "    rdfs:domain ac:ControlObjective ;",
            "    rdfs:range ac:ObjectiveKind ;",
            f"    rdfs:label {_literal(_property_label('hasObjectiveKind'))} ;",
            f"    rdfs:comment {_literal('Relates a ControlObjective to its kind (atomic or composite).')} ;",
            "    owl:inverseOf ac:isObjectiveKindOf .",
            "",
            "ac:isObjectiveKindOf a owl:ObjectProperty ;",
            "    rdfs:domain ac:ObjectiveKind ;",
            "    rdfs:range ac:ControlObjective ;",
            f"    rdfs:label {_literal('is objective kind of')} ;",
            f"    rdfs:comment {_literal('Inverse of ac:hasObjectiveKind; relates an ObjectiveKind value to ControlObjective instances that have it.')} .",
            "",
            "ac:hasObjectiveType a owl:ObjectProperty ;",
            "    rdfs:domain ac:ControlObjective ;",
            "    rdfs:range ac:ObjectiveType ;",
            f"    rdfs:label {_literal(_property_label('hasObjectiveType'))} ;",
            f"    rdfs:comment {_literal('Relates a ControlObjective to its objective type (governance/preventive/detective/corrective).')} ;",
            "    owl:inverseOf ac:isObjectiveTypeOf .",
            "",
            "ac:isObjectiveTypeOf a owl:ObjectProperty ;",
            "    rdfs:domain ac:ObjectiveType ;",
            "    rdfs:range ac:ControlObjective ;",
            f"    rdfs:label {_literal('is objective type of')} ;",
            f"    rdfs:comment {_literal('Inverse of ac:hasObjectiveType; relates an ObjectiveType value to ControlObjective instances that have it.')} .",
            "",
            "ac:hasPracticeFamily a owl:ObjectProperty ;",
            "    rdfs:domain ac:Practice ;",
            "    rdfs:range ac:PracticeFamily ;",
            f"    rdfs:label {_literal(_property_label('hasPracticeFamily'))} ;",
            f"    rdfs:comment {_literal('Relates a Practice to its cross-slice practice family qualifier.')} ;",
            "    owl:inverseOf ac:isPracticeFamilyOf .",
            "",
            "ac:isPracticeFamilyOf a owl:ObjectProperty ;",
            "    rdfs:domain ac:PracticeFamily ;",
            "    rdfs:range ac:Practice ;",
            f"    rdfs:label {_literal('is practice family of')} ;",
            f"    rdfs:comment {_literal('Inverse of ac:hasPracticeFamily; relates a PracticeFamily value to Practice instances that have it.')} .",
            "",
            "ac:hasMechanismFamily a owl:ObjectProperty ;",
            "    rdfs:domain ac:Mechanism ;",
            "    rdfs:range ac:MechanismFamily ;",
            f"    rdfs:label {_literal(_property_label('hasMechanismFamily'))} ;",
            f"    rdfs:comment {_literal('Relates a Mechanism to its cross-slice mechanism family qualifier.')} ;",
            "    owl:inverseOf ac:isMechanismFamilyOf .",
            "",
            "ac:isMechanismFamilyOf a owl:ObjectProperty ;",
            "    rdfs:domain ac:MechanismFamily ;",
            "    rdfs:range ac:Mechanism ;",
            f"    rdfs:label {_literal('is mechanism family of')} ;",
            f"    rdfs:comment {_literal('Inverse of ac:hasMechanismFamily; relates a MechanismFamily value to Mechanism instances that have it.')} .",
            "",
            "ac:hasCanonicalArtifactRole a owl:ObjectProperty ;",
            "    rdfs:domain ac:Artifact ;",
            "    rdfs:range ac:ArtifactRole ;",
            f"    rdfs:label {_literal(_property_label('hasCanonicalArtifactRole'))} ;",
            f"    rdfs:comment {_literal('Relates an Artifact to its canonical role in the AppSec Core taxonomy.')} ;",
            "    owl:inverseOf ac:isCanonicalArtifactRoleOf .",
            "",
            "ac:isCanonicalArtifactRoleOf a owl:ObjectProperty ;",
            "    rdfs:domain ac:ArtifactRole ;",
            "    rdfs:range ac:Artifact ;",
            f"    rdfs:label {_literal('is canonical artifact role of')} ;",
            f"    rdfs:comment {_literal('Inverse of ac:hasCanonicalArtifactRole; relates an ArtifactRole value to Artifact instances that have it.')} .",
            "",
            "ac:hasCanonicalEvidenceKind a owl:ObjectProperty ;",
            "    rdfs:domain ac:EvidencePattern ;",
            "    rdfs:range ac:ArtifactRole ;",
            f"    rdfs:label {_literal(_property_label('hasCanonicalEvidenceKind'))} ;",
            f"    rdfs:comment {_literal('Relates an EvidencePattern to the canonical evidence kind (typically reusing an ArtifactRole value).')} ;",
            "    owl:inverseOf ac:isCanonicalEvidenceKindOf .",
            "",
            "ac:isCanonicalEvidenceKindOf a owl:ObjectProperty ;",
            "    rdfs:domain ac:ArtifactRole ;",
            "    rdfs:range ac:EvidencePattern ;",
            f"    rdfs:label {_literal('is canonical evidence kind of')} ;",
            f"    rdfs:comment {_literal('Inverse of ac:hasCanonicalEvidenceKind; relates an ArtifactRole value used as canonical evidence kind to the EvidencePattern that adopts it.')} .",
            "",
            "ac:detectableInSurface a owl:ObjectProperty ;",
            "    rdfs:domain ac:EvidencePattern ;",
            "    rdfs:range ac:DetectableSurface ;",
            f"    rdfs:label {_literal(_property_label('detectableInSurface'))} ;",
            f"    rdfs:comment {_literal('Relates an EvidencePattern to the detectable surface where the evidence is expected to manifest.')} ;",
            "    owl:inverseOf ac:surfaceOfDetectableEvidencePattern .",
            "",
            "ac:surfaceOfDetectableEvidencePattern a owl:ObjectProperty ;",
            "    rdfs:domain ac:DetectableSurface ;",
            "    rdfs:range ac:EvidencePattern ;",
            f"    rdfs:label {_literal('surface of detectable evidence pattern')} ;",
            f"    rdfs:comment {_literal('Inverse of ac:detectableInSurface; relates a DetectableSurface to EvidencePattern instances detectable on it.')} .",
            "",
        ]
    )

    # P08+P13 fix (Phase C 2026-05-10): emit rdfs:comment + owl:inverseOf
    # for each stable relation; emit inverse property declaration too.
    RELATION_INVERSE = {
        "objective_realized_by_practice": "practice_realizes_objective",
        "objective_implemented_by_mechanism": "mechanism_implements_objective",
        "objective_expects_artifact": "artifact_supports_objective",
        "objective_verified_by_evidence_pattern": "evidence_pattern_verifies_objective",
        "artifact_supports_evidence_pattern": "evidence_pattern_supported_by_artifact",
    }
    RELATION_DESCRIPTION = {
        "objective_realized_by_practice": "Relates a ControlObjective to a Practice that realises it operationally.",
        "objective_implemented_by_mechanism": "Relates a ControlObjective to a Mechanism that implements it technically.",
        "objective_expects_artifact": "Relates a ControlObjective to an Artifact whose presence is expected as evidence of the objective.",
        "objective_verified_by_evidence_pattern": "Relates a ControlObjective to an EvidencePattern that supports its deterministic review.",
        "artifact_supports_evidence_pattern": "Relates an Artifact to an EvidencePattern it supports as evidence.",
    }
    for relation_name in stable_relations:
        domain_name, range_name = RELATION_DOMAIN_RANGE.get(relation_name, ("owl:Thing", "owl:Thing"))
        domain_ref = f"ac:{domain_name}" if not domain_name.startswith("owl:") else domain_name
        range_ref = f"ac:{range_name}" if not range_name.startswith("owl:") else range_name
        comment = RELATION_DESCRIPTION.get(
            relation_name,
            f"Stable cross-entity relation: {_humanize_value(relation_name, title_case=False)}.",
        )
        inverse_name = RELATION_INVERSE.get(relation_name)
        properties = [
            ("rdfs:label", _property_label(relation_name), True),
            ("rdfs:comment", comment, True),
            ("rdfs:domain", domain_ref, False),
            ("rdfs:range", range_ref, False),
        ]
        if inverse_name:
            properties.append(("owl:inverseOf", f"ac:{inverse_name}", False))
        lines.extend(
            _triple_block(
                f"ac:{relation_name}",
                "owl:ObjectProperty",
                properties,
            )
        )

    # Emit inverse property declarations (paired with above)
    for relation_name in stable_relations:
        inverse_name = RELATION_INVERSE.get(relation_name)
        if not inverse_name:
            continue
        domain_name, range_name = RELATION_DOMAIN_RANGE.get(relation_name, ("owl:Thing", "owl:Thing"))
        # Inverse: swap domain and range
        inv_domain_ref = f"ac:{range_name}" if not range_name.startswith("owl:") else range_name
        inv_range_ref = f"ac:{domain_name}" if not domain_name.startswith("owl:") else domain_name
        inv_comment = f"Inverse of ac:{relation_name}; {RELATION_DESCRIPTION.get(relation_name, '').lower()}"
        lines.extend(
            _triple_block(
                f"ac:{inverse_name}",
                "owl:ObjectProperty",
                [
                    ("rdfs:label", _property_label(inverse_name), True),
                    ("rdfs:comment", inv_comment, True),
                    ("rdfs:domain", inv_domain_ref, False),
                    ("rdfs:range", inv_range_ref, False),
                ],
            )
        )

    # P08 fix (Phase C 2026-05-10): rdfs:comment per Slice datatype property for VOC4.
    lines.extend(
        [
            "ac:slice_id a owl:DatatypeProperty ;",
            "    rdfs:domain ac:Slice ;",
            "    rdfs:range xsd:string ;",
            f"    rdfs:label {_literal(_property_label('slice_id'))} ;",
            f"    rdfs:comment {_literal('Stable identifier for an AppSec Core Slice (matches ASC-NN pattern).')} .",
            "",
            "ac:scope_key a owl:DatatypeProperty ;",
            "    rdfs:domain ac:Slice ;",
            "    rdfs:range xsd:string ;",
            f"    rdfs:label {_literal(_property_label('scope_key'))} ;",
            f"    rdfs:comment {_literal('Canonical scope label for the slice (e.g. input_output_data_safety_and_controlled_failure).')} .",
            "",
            "ac:objective_family_code a owl:DatatypeProperty ;",
            "    rdfs:domain ac:Slice ;",
            "    rdfs:range xsd:string ;",
            f"    rdfs:label {_literal(_property_label('objective_family_code'))} ;",
            f"    rdfs:comment {_literal('Family code shared by all ControlObjective instances inside the slice (e.g. ACO-IVF).')} .",
            "",
            "ac:current_control_mode a owl:DatatypeProperty ;",
            "    rdfs:domain ac:Slice ;",
            "    rdfs:range xsd:string ;",
            f"    rdfs:label {_literal(_property_label('current_control_mode'))} ;",
            f"    rdfs:comment {_literal('Slice control-mode descriptor at the current AppSec Core release (e.g. single_broad_control_surface).')} .",
            "",
            "ac:contract_path a owl:DatatypeProperty ;",
            "    rdfs:domain ac:Slice ;",
            "    rdfs:range xsd:string ;",
            f"    rdfs:label {_literal(_property_label('contract_path'))} ;",
            f"    rdfs:comment {_literal('Repository-relative path to the slice contract YAML in sbd-toe-ontology.')} .",
            "",
        ]
    )

    # P11+P08 fix (Phase C 2026-05-10): pre-compute field → entity set
    # so each schema-derived datatype property gets an explicit rdfs:domain
    # (single entity → ac:<Entity>; shared field → ac:AppSecCoreEntity)
    # plus an rdfs:comment derived from the field name for VOC4 coverage.
    field_to_entities: dict[str, list[str]] = {}
    skip_fields = {
        "objective_kind",
        "objective_type",
        "practice_family",
        "mechanism_family",
        "canonical_role",
        "canonical_evidence_kind",
    }
    for entity_name in first_class_entities:
        for field_name in required_fields.get(entity_name, []):
            if field_name in skip_fields:
                continue
            field_to_entities.setdefault(field_name, []).append(entity_name)

    field_descriptions = {
        "objective_id": "Stable identifier for a ControlObjective instance (matches ACO-<SLICE>-<NNN> pattern).",
        "practice_id": "Stable identifier for a Practice instance (matches ACP-<SLICE>-<NNN> pattern).",
        "mechanism_id": "Stable identifier for a Mechanism instance (matches ACM-<SLICE>-<NNN> pattern).",
        "artifact_id": "Stable identifier for an Artifact instance (matches ACA-<SLICE>-<NNN> pattern).",
        "evidence_pattern_id": "Stable identifier for an EvidencePattern instance.",
        "name": "Human-readable name for the AppSec Core entity instance.",
        "statement": "Normative statement of what a ControlObjective requires to hold true in the application security domain.",
        "expected_outcome": "Behavioural outcome that a ControlObjective expects to observe when satisfied.",
        "verification_posture": "Assurance stance qualifier indicating how a ControlObjective is verified.",
        "domain_key": "Slice-local domain key categorising a ControlObjective.",
        "local_practice_type": "Slice-local typing for a Practice (e.g. contract_validation, output_encoding).",
        "local_mechanism_type": "Slice-local typing for a Mechanism (e.g. rulepack, context_encoder).",
        "expectation": "Expected evidence shape that supports deterministic review of an EvidencePattern.",
        "validation_method": "Method describing how an EvidencePattern is interpreted (not its execution binding).",
    }

    for field_name in sorted(field_to_entities.keys()):
        owners = field_to_entities[field_name]
        # Domain: single owner → that entity; shared field → AppSecCoreEntity
        if len(owners) == 1:
            domain_ref = f"ac:{owners[0]}"
        else:
            domain_ref = "ac:AppSecCoreEntity"
        description = field_descriptions.get(
            field_name,
            f"Datatype property carrying the {_humanize_value(field_name, title_case=False)} value of an AppSec Core entity instance.",
        )
        lines.extend(
            _triple_block(
                f"ac:{field_name}",
                "owl:DatatypeProperty",
                [
                    ("rdfs:label", _property_label(field_name), True),
                    ("rdfs:comment", description, True),
                    ("rdfs:domain", domain_ref, False),
                    ("rdfs:range", "xsd:string", False),
                ],
            )
        )

    for block in _controlled_vocab_individuals(
        values=["atomic", "composite"],
        class_name="ObjectiveKind",
        local_prefix="ObjectiveKind",
    ):
        lines.extend(block)
    for block in _controlled_vocab_individuals(
        values=["governance", "preventive", "detective", "corrective"],
        class_name="ObjectiveType",
        local_prefix="ObjectiveType",
    ):
        lines.extend(block)
    for block in _controlled_vocab_individuals(
        values=_stable_artifact_roles(bundle),
        class_name="ArtifactRole",
        local_prefix="ArtifactRole",
    ):
        lines.extend(block)
    for block in _controlled_vocab_individuals(
        values=_practice_families(bundle),
        class_name="PracticeFamily",
        local_prefix="PracticeFamily",
    ):
        lines.extend(block)
    for block in _controlled_vocab_individuals(
        values=_mechanism_families(bundle),
        class_name="MechanismFamily",
        local_prefix="MechanismFamily",
    ):
        lines.extend(block)
    for block in _controlled_vocab_individuals(
        values=_detectable_surfaces(bundle),
        class_name="DetectableSurface",
        local_prefix="DetectableSurface",
    ):
        lines.extend(block)

    for slice_record in _slice_records(bundle):
        slice_id = str(slice_record.get("slice_id"))
        scope = str(slice_record.get("scope", ""))
        subject = f"ac:{_slice_local_name(slice_id)}"
        slice_label = _catalog_label(bundle, "Slice", slice_id) or _humanize_value(
            scope, title_case=True
        )
        properties: list[tuple[str, str, bool]] = [
            ("rdfs:label", slice_label, True),
            ("rdfs:comment", _humanize_value(scope, title_case=False), True),
            ("ac:slice_id", slice_id, True),
            ("ac:scope_key", scope, True),
            ("ac:objective_family_code", str(slice_record.get("objective_family", "")), True),
            ("ac:current_control_mode", str(slice_record.get("current_control_mode", "")), True),
            ("ac:contract_path", str(slice_record.get("contract", "")), True),
        ]
        short_label = _catalog_short_label(bundle, "Slice", slice_id)
        if short_label:
            properties.append(("ac:shortLabel", short_label, True))
        diagram_label = _catalog_diagram_label(bundle, "Slice", slice_id)
        if diagram_label:
            properties.append(("ac:diagramLabel", diagram_label, True))
        lines.extend(_triple_block(subject, "ac:Slice", properties))

    for block in _entity_instance_blocks(bundle):
        lines.extend(block)

    return "\n".join(lines)


def write_owl_starter(bundle: SourceBundle, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "appsec-core-v0-bounded-v1.ttl"
    output_path.write_text(render_owl_starter(bundle), encoding="utf-8")
    return output_path
