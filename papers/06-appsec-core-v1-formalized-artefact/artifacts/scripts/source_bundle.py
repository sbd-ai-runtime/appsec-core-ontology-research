"""Read the canonical AppSec Core source bundle used for formalization."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from .paths import WorkbenchPaths
from .yaml_utils import load_yaml


@dataclass(frozen=True)
class SourceBundle:
    surface_contract: dict[str, Any]
    consolidated: dict[str, Any]
    entity_schema: dict[str, Any]
    cross_slice_vocabulary: dict[str, Any]
    instance_index: dict[str, Any]
    slice_registry: dict[str, Any]
    evidence_pattern_contract: dict[str, Any]
    formalization_roadmap: str
    label_catalog: dict[tuple[str, str], dict[str, Any]]
    source_entity_labels: dict[str, str]
    co_to_practices: dict[str, list[str]]
    co_to_mechanisms: dict[str, list[str]]
    co_to_artifacts: dict[str, list[str]]


_ACRONYM_MAP = {
    "api": "API",
    "appsec": "AppSec",
    "ci": "CI",
    "cd": "CD",
    "dfd": "DFD",
    "iac": "IaC",
    "oidc": "OIDC",
    "sast": "SAST",
    "sbom": "SBOM",
    "sca": "SCA",
}


def _optional_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return load_yaml(path)


def _render_token(token: str) -> str:
    lower = token.lower()
    return _ACRONYM_MAP.get(lower, token.capitalize())


def _humanize_slug(value: str) -> str:
    tokens = [token for token in re.split(r"[^A-Za-z0-9]+", value) if token]
    rendered: list[str] = []
    index = 0
    while index < len(tokens):
        current = tokens[index].lower()
        following = tokens[index + 1].lower() if index + 1 < len(tokens) else None
        if current == "ci" and following == "cd":
            rendered.append("CI/CD")
            index += 2
            continue
        rendered.append(_render_token(tokens[index]))
        index += 1
    return " ".join(rendered).strip()


def _artifact_label_from_source_id(source_artifact_id: str) -> str:
    normalized = re.sub(r"^ART-", "", source_artifact_id)
    normalized = re.sub(r"-[0-9a-f]{10}$", "", normalized)
    return _humanize_slug(normalized)


def _load_label_catalog(paths: WorkbenchPaths) -> dict[tuple[str, str], dict[str, Any]]:
    payload = _optional_yaml(
        paths.ontology_file("mappings/labels/appsec-core-taxonomy-labels.yaml")
    )
    items = payload.get("items", [])
    catalog: dict[tuple[str, str], dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        entity_type = str(item.get("entity_type", "")).strip()
        identifier = str(item.get("id", "")).strip()
        if not entity_type or not identifier:
            continue
        catalog[(entity_type, identifier)] = item
    return catalog


def _extract_named_entries(
    payload: dict[str, Any],
    *,
    label_field: str = "name",
) -> dict[str, str]:
    labels: dict[str, str] = {}
    for identifier, body in payload.items():
        if not isinstance(body, dict):
            continue
        label = str(body.get(label_field, "")).strip()
        if label:
            labels[str(identifier)] = label
    return labels


def _extract_artifact_entries(payload: dict[str, Any]) -> dict[str, str]:
    labels: dict[str, str] = {}
    for identifier, body in payload.items():
        if not isinstance(body, dict):
            continue
        if "name" in body and str(body.get("name", "")).strip():
            labels[str(identifier)] = str(body.get("name", "")).strip()
            continue
        source_artifact_id = str(body.get("source_artifact_id", "")).strip()
        if source_artifact_id:
            labels[str(identifier)] = _artifact_label_from_source_id(source_artifact_id)
    return labels


def _load_source_entity_labels(
    paths: WorkbenchPaths,
    instance_index: dict[str, Any],
) -> dict[str, str]:
    labels: dict[str, str] = {}
    slice_instances = instance_index.get("slice_instances", [])
    for slice_record in slice_instances:
        if not isinstance(slice_record, dict):
            continue

        objective_draft = str(slice_record.get("objective_draft", "")).strip()
        if objective_draft:
            objective_payload = _optional_yaml(paths.ontology_file(objective_draft))
            labels.update(
                _extract_named_entries(objective_payload.get("normalized_objectives", {}))
            )

        components_draft = str(slice_record.get("components_draft", "")).strip()
        if components_draft:
            components_payload = _optional_yaml(paths.ontology_file(components_draft))
            labels.update(
                _extract_named_entries(components_payload.get("normalized_practices", {}))
            )
            labels.update(
                _extract_named_entries(components_payload.get("normalized_mechanisms", {}))
            )
            labels.update(
                _extract_artifact_entries(components_payload.get("normalized_artifacts", {}))
            )
    return labels


def _load_entity_relations(
    paths: WorkbenchPaths,
    instance_index: dict[str, Any],
) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, list[str]]]:
    """Return (co_to_practices, co_to_mechanisms, co_to_artifacts) dicts.

    Relations are resolved from slice component YAMLs:
      - Practices → COs via `supports_objectives`
      - Mechanisms → COs via `supports_objectives` (if present) OR transitively
        via `supports_practices` → practice.supports_objectives
      - Artifacts → COs via `supports_objectives`
    """
    co_to_practices: dict[str, list[str]] = {}
    co_to_mechanisms: dict[str, list[str]] = {}
    co_to_artifacts: dict[str, list[str]] = {}
    practice_to_cos: dict[str, list[str]] = {}

    def _add(target: dict[str, list[str]], co: str, value: str) -> None:
        bucket = target.setdefault(co, [])
        if value not in bucket:
            bucket.append(value)

    slice_instances = instance_index.get("slice_instances", [])
    for slice_record in slice_instances:
        if not isinstance(slice_record, dict):
            continue
        components_draft = str(slice_record.get("components_draft", "")).strip()
        if not components_draft:
            continue
        components_payload = _optional_yaml(paths.ontology_file(components_draft))

        practices = components_payload.get("normalized_practices", {}) or {}
        for practice_id, body in practices.items():
            if not isinstance(body, dict):
                continue
            objectives = [str(v) for v in body.get("supports_objectives", []) or []]
            practice_to_cos[str(practice_id)] = objectives
            for co in objectives:
                _add(co_to_practices, co, str(practice_id))

        mechanisms = components_payload.get("normalized_mechanisms", {}) or {}
        for mechanism_id, body in mechanisms.items():
            if not isinstance(body, dict):
                continue
            direct_cos = [str(v) for v in body.get("supports_objectives", []) or []]
            for co in direct_cos:
                _add(co_to_mechanisms, co, str(mechanism_id))
            supported_practices = [str(v) for v in body.get("supports_practices", []) or []]
            for practice_id in supported_practices:
                for co in practice_to_cos.get(practice_id, []):
                    _add(co_to_mechanisms, co, str(mechanism_id))

        artifacts = components_payload.get("normalized_artifacts", {}) or {}
        for artifact_id, body in artifacts.items():
            if not isinstance(body, dict):
                continue
            objectives = [str(v) for v in body.get("supports_objectives", []) or []]
            for co in objectives:
                _add(co_to_artifacts, co, str(artifact_id))

    return co_to_practices, co_to_mechanisms, co_to_artifacts


def load_source_bundle(paths: WorkbenchPaths) -> SourceBundle:
    surface_contract = load_yaml(paths.ontology_file("ontology/appsec-core-v0-surface-contract.yaml"))
    consolidated = load_yaml(paths.ontology_file("ontology/appsec-core-v0-consolidated.yaml"))
    entity_schema = load_yaml(paths.ontology_file("ontology/appsec-core-entity-schema-v0-draft.yaml"))
    cross_slice_vocabulary = load_yaml(
        paths.ontology_file("ontology/appsec-core-cross-slice-vocabulary-v0-draft.yaml")
    )
    instance_index = load_yaml(paths.ontology_file("ontology/appsec-core-v0-instance-index.yaml"))
    slice_registry = load_yaml(paths.ontology_file("ontology/appsec-core-slice-registry-v0-draft.yaml"))
    evidence_pattern_contract = load_yaml(
        paths.ontology_file("ontology/appsec-core-evidence-pattern-v0-draft.yaml")
    )

    co_to_practices, co_to_mechanisms, co_to_artifacts = _load_entity_relations(
        paths, instance_index
    )

    return SourceBundle(
        surface_contract=surface_contract,
        consolidated=consolidated,
        entity_schema=entity_schema,
        cross_slice_vocabulary=cross_slice_vocabulary,
        instance_index=instance_index,
        slice_registry=slice_registry,
        evidence_pattern_contract=evidence_pattern_contract,
        formalization_roadmap=(
            paths.ontology_file("docs/formalization-roadmap.md").read_text(encoding="utf-8")
        ),
        label_catalog=_load_label_catalog(paths),
        source_entity_labels=_load_source_entity_labels(paths, instance_index),
        co_to_practices=co_to_practices,
        co_to_mechanisms=co_to_mechanisms,
        co_to_artifacts=co_to_artifacts,
    )
