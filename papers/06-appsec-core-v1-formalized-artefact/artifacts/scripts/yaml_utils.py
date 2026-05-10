"""YAML loading helpers for the formalization workbench."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(
            "PyYAML is required for AppSec Core formalization helpers. "
            "Install it before running this command."
        ) from exc

    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Expected top-level mapping in {path}")
    return loaded
