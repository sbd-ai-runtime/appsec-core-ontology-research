"""Grounded inventory generation for AppSec Core formalization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .source_bundle import SourceBundle


def _first_class_entities(bundle: SourceBundle) -> list[str]:
    entity_boundary = bundle.surface_contract.get("entity_boundary", {})
    values = entity_boundary.get("first_class_for_v0", [])
    return [str(value) for value in values]


def _stable_relations(bundle: SourceBundle) -> list[str]:
    relation_schema = bundle.entity_schema.get("relation_schema", {})
    values = relation_schema.get("stable_core_relations", [])
    return [str(value) for value in values]


def _summary_counts(bundle: SourceBundle) -> dict[str, int]:
    summary = bundle.instance_index.get("summary", {})
    counts = summary.get("counts", {})
    return {str(key): int(value) for key, value in counts.items()}


def build_inventory_payload(bundle: SourceBundle) -> dict[str, Any]:
    entity_schema = bundle.entity_schema
    vocabulary = bundle.cross_slice_vocabulary
    surface_contract = bundle.surface_contract
    instance_index = bundle.instance_index

    core_entities = entity_schema.get("core_entities", {})
    cross_slice_families = entity_schema.get("cross_slice_families", {})
    stable_enums = vocabulary.get("stable_enums", {})
    slice_instances = instance_index.get("slice_instances", [])

    return {
        "decision": "ready_for_bounded_first_formal_cut",
        "scope": "AppSec Core v0",
        "first_class_entities": _first_class_entities(bundle),
        "supporting_but_not_core_driving": [
            str(value)
            for value in surface_contract.get("entity_boundary", {}).get(
                "supporting_but_not_core_driving", []
            )
        ],
        "deferred_entities": [
            str(value)
            for value in surface_contract.get("entity_boundary", {}).get("explicitly_deferred", [])
        ],
        "stable_relations": _stable_relations(bundle),
        "stable_enum_names": sorted(str(name) for name in stable_enums.keys()),
        "canonical_artifact_roles": [
            str(value)
            for value in cross_slice_families.get("canonical_artifact_roles", [])
        ],
        "practice_families": [
            str(value) for value in cross_slice_families.get("practice_families", [])
        ],
        "mechanism_families": [
            str(value) for value in cross_slice_families.get("mechanism_families", [])
        ],
        "indexed_counts": _summary_counts(bundle),
        "slice_count": int(instance_index.get("summary", {}).get("slices", 0)),
        "slice_ids": [str(item.get("slice_id")) for item in slice_instances if isinstance(item, dict)],
        "entity_required_fields": {
            entity_name: [str(field) for field in entity_body.get("required_fields", [])]
            for entity_name, entity_body in core_entities.items()
            if isinstance(entity_body, dict)
        },
        "evidence_pattern_boundary_note": surface_contract.get("instance_policy", {})
        .get("supporting_global_surfaces", {})
        .get("EvidencePattern", {})
        .get("public_claim", {}),
        "stays_out_of_v0_surface": [
            str(value)
            for value in surface_contract.get("boundary_rules", {}).get("stays_out_of_v0_surface", [])
        ],
    }


def render_inventory_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# AppSec Core Formalization Inventory",
        "",
        f"- Scope: `{payload['scope']}`",
        f"- Decision: `{payload['decision']}`",
        "",
        "## First-Class Entities",
        "",
    ]
    lines.extend(f"- `{value}`" for value in payload["first_class_entities"])
    lines.extend(
        [
            "",
            "## Stable Relations",
            "",
        ]
    )
    lines.extend(f"- `{value}`" for value in payload["stable_relations"])
    lines.extend(
        [
            "",
            "## Indexed Counts",
            "",
        ]
    )
    for key, value in payload["indexed_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(
        [
            "",
            "## Explicit Exclusions",
            "",
        ]
    )
    lines.extend(f"- `{value}`" for value in payload["stays_out_of_v0_surface"])
    lines.append("")
    return "\n".join(lines)


def write_inventory(bundle: SourceBundle, output_dir: Path) -> tuple[Path, Path]:
    payload = build_inventory_payload(bundle)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "appsec-core-formalization-inventory.json"
    md_path = output_dir / "appsec-core-formalization-inventory.md"

    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_inventory_markdown(payload), encoding="utf-8")
    return json_path, md_path
