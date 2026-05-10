"""Generate a grounded presentation label catalog for AppSec Core v0."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any

from .paths import WorkbenchPaths
from .source_bundle import SourceBundle
from .yaml_utils import load_yaml


ENTITY_ORDER = {
    "Slice": 0,
    "ControlObjective": 1,
    "Practice": 2,
    "Mechanism": 3,
    "Artifact": 4,
}

ENTITY_COLLECTIONS = (
    ("ControlObjective", "control_objectives"),
    ("Practice", "practices"),
    ("Mechanism", "mechanisms"),
    ("Artifact", "artifacts"),
)

_ACRONYM_MAP = {
    "api": "API",
    "appsec": "AppSec",
    "cd": "CD",
    "ci": "CI",
    "dfd": "DFD",
    "iac": "IaC",
    "oidc": "OIDC",
    "sast": "SAST",
    "sbom": "SBOM",
    "sca": "SCA",
    "sdlc": "SDLC",
    "s2s": "S2S",
}

_LOWERCASE_CONNECTORS = {"and", "by", "for", "in", "of", "or", "to", "with"}


def _catalog_path(paths: WorkbenchPaths) -> Path:
    return paths.ontology_file("mappings/labels/appsec-core-taxonomy-labels.yaml")


def _optional_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return load_yaml(path)


def _split_words(value: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    return [token for token in re.split(r"[^A-Za-z0-9]+", spaced) if token]


def _humanize_scope(value: str) -> str:
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

        mapped = _ACRONYM_MAP.get(current)
        if mapped:
            rendered.append(mapped)
        elif rendered and current in _LOWERCASE_CONNECTORS:
            rendered.append(current)
        else:
            rendered.append(current.capitalize())
        index += 1

    return " ".join(rendered).strip()


def _existing_catalog_payload(paths: WorkbenchPaths) -> dict[str, Any]:
    return _optional_yaml(_catalog_path(paths))


def _existing_item_index(payload: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for item in payload.get("items", []):
        if not isinstance(item, dict):
            continue
        entity_type = str(item.get("entity_type", "")).strip()
        identifier = str(item.get("id", "")).strip()
        if entity_type and identifier:
            index[(entity_type, identifier)] = item
    return index


def _merge_nested_defaults(
    current: dict[str, Any],
    key: str,
    defaults: dict[str, Any],
) -> None:
    if not defaults:
        return
    existing = current.get(key)
    if not isinstance(existing, dict):
        current[key] = deepcopy(defaults)
        return
    for nested_key, nested_value in defaults.items():
        if nested_key not in existing:
            existing[nested_key] = deepcopy(nested_value)
            continue
        if isinstance(existing[nested_key], dict) and isinstance(nested_value, dict):
            for leaf_key, leaf_value in nested_value.items():
                existing[nested_key].setdefault(leaf_key, leaf_value)


def _merge_catalog_item(generated: dict[str, Any], existing: dict[str, Any] | None) -> dict[str, Any]:
    merged = deepcopy(existing) if existing else {}
    for key in ("entity_type", "id", "canonical_label", "canonical_short_label", "source_scope"):
        value = generated.get(key)
        if value is None or value == "":
            continue
        if key not in merged or str(merged.get(key, "")).strip() == "":
            merged[key] = value

    _merge_nested_defaults(merged, "locales", generated.get("locales", {}))
    _merge_nested_defaults(merged, "render", generated.get("render", {}))
    return merged


def _slice_item(bundle: SourceBundle, slice_record: dict[str, Any]) -> dict[str, Any]:
    slice_id = str(slice_record.get("slice_id", "")).strip()
    scope = str(slice_record.get("scope", "")).strip()
    label = (
        bundle.label_catalog.get(("Slice", slice_id), {}).get("canonical_label")
        or _humanize_scope(scope)
    )
    item: dict[str, Any] = {
        "entity_type": "Slice",
        "id": slice_id,
        "canonical_label": str(label).strip(),
        "source_scope": scope,
        "locales": {
            "en": {
                "label": str(label).strip(),
            }
        },
    }
    existing = bundle.label_catalog.get(("Slice", slice_id), {})
    short_label = str(existing.get("canonical_short_label", "")).strip()
    if short_label:
        item["canonical_short_label"] = short_label
        item["locales"]["en"]["short_label"] = short_label
    render = existing.get("render", {})
    if isinstance(render, dict) and render:
        item["render"] = deepcopy(render)
    return item


def _entity_item(
    bundle: SourceBundle,
    *,
    entity_type: str,
    identifier: str,
    scope: str,
) -> dict[str, Any]:
    label = str(bundle.source_entity_labels.get(identifier, "")).strip()
    if not label:
        raise ValueError(
            f"Missing human-readable label for {entity_type} {identifier}; "
            "the AppSec Core label catalog generator expects canonical slice drafts "
            "and component drafts to provide these labels."
        )
    return {
        "entity_type": entity_type,
        "id": identifier,
        "canonical_label": label,
        "source_scope": scope,
        "locales": {
            "en": {
                "label": label,
            }
        },
    }


def build_label_catalog_payload(bundle: SourceBundle, paths: WorkbenchPaths) -> dict[str, Any]:
    existing_payload = _existing_catalog_payload(paths)
    existing_items = _existing_item_index(existing_payload)

    items: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for slice_record in bundle.instance_index.get("slice_instances", []):
        if not isinstance(slice_record, dict):
            continue
        slice_id = str(slice_record.get("slice_id", "")).strip()
        if not slice_id:
            continue
        slice_key = ("Slice", slice_id)
        items.append(_merge_catalog_item(_slice_item(bundle, slice_record), existing_items.get(slice_key)))
        seen.add(slice_key)

    for entity_type, collection_key in ENTITY_COLLECTIONS:
        for slice_record in bundle.instance_index.get("slice_instances", []):
            if not isinstance(slice_record, dict):
                continue
            scope = str(slice_record.get("scope", "")).strip()
            for raw_identifier in slice_record.get(collection_key, []):
                identifier = str(raw_identifier).strip()
                if not identifier:
                    continue
                item_key = (entity_type, identifier)
                if item_key in seen:
                    continue
                items.append(
                    _merge_catalog_item(
                        _entity_item(
                            bundle,
                            entity_type=entity_type,
                            identifier=identifier,
                            scope=scope,
                        ),
                        existing_items.get(item_key),
                    )
                )
                seen.add(item_key)

    items.sort(key=lambda item: (ENTITY_ORDER.get(str(item.get("entity_type")), 99), str(item.get("id", ""))))

    return {
        "meta": {
            "name": "AppSec Core Taxonomy Labels",
            "version": "0.2",
            "status": "working_draft",
            "artifact_type": "presentation_label_catalog",
            "scope": "appsec_core_v0",
            "description": (
                "Human-readable labels, locale variants and render hints keyed by stable "
                "AppSec Core identifiers. This catalog does not redefine ontology "
                "semantics; it provides a human readability layer over stable IDs."
            ),
            "related_artifacts": {
                "slice_registry": "ontology/appsec-core-slice-registry-v0-draft.yaml",
                "instance_index": "ontology/appsec-core-v0-instance-index.yaml",
                "formal_owl": "formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl",
            },
        },
        "purpose": {
            "current_goal": (
                "Improve the readability of canonical AppSec Core identifiers in diagrams, "
                "formal views and reviewer-facing materials without changing the stable IDs."
            ),
            "non_goals": [
                "renaming_canonical_ids",
                "redefining_ontology_semantics",
                "replacing_source_artifact_names",
                "acting_as_a_runtime_translation_service",
            ],
        },
        "schema_notes": {
            "item_key": "entity_type + id",
            "required_fields": [
                "entity_type",
                "id",
                "canonical_label",
            ],
            "optional_fields": [
                "canonical_short_label",
                "locales",
                "render",
                "source_scope",
            ],
        },
        "items": items,
        "current_read": {
            "stable_enough_now": [
                "full_v0_label_catalog_exists_for_slices_and_indexed_first_class_instances",
                "canonical_ids_remain_machine_stable",
                "owl_generation_can_prefer_catalog_labels_over_raw_ids",
            ],
            "not_stable_enough_yet": [
                "generic_multilingual_policy_for_all_ontology_surfaces",
                "evidence_pattern_label_catalog_before_global_index_exists",
            ],
        },
    }


def _dump_yaml(payload: dict[str, Any]) -> str:
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(
            "PyYAML is required for AppSec Core formalization helpers. "
            "Install it before running this command."
        ) from exc
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=100)


def write_label_catalog(bundle: SourceBundle, paths: WorkbenchPaths) -> Path:
    output_path = _catalog_path(paths)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_label_catalog_payload(bundle, paths)
    output_path.write_text(_dump_yaml(payload), encoding="utf-8")
    return output_path
