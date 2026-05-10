"""Path resolution for the AppSec Core formalization workbench."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WorkbenchPaths:
    repo_root: Path
    source_root: Path
    workbench_root: Path

    @property
    def grounding_generated(self) -> Path:
        return self.workbench_root / "00-grounding" / "generated"

    @property
    def owl_exports(self) -> Path:
        return self.workbench_root / "02-owl" / "exports"

    @property
    def shacl_shapes(self) -> Path:
        return self.workbench_root / "03-shacl" / "shapes"

    @property
    def status_root(self) -> Path:
        return self.workbench_root / "07-status"

    @property
    def validation_reports(self) -> Path:
        return self.workbench_root / "05-validation" / "reports"

    def ontology_file(self, relative_path: str) -> Path:
        return self.source_root / relative_path

    def ensure_dirs(self) -> None:
        self.grounding_generated.mkdir(parents=True, exist_ok=True)
        self.owl_exports.mkdir(parents=True, exist_ok=True)
        self.shacl_shapes.mkdir(parents=True, exist_ok=True)
        self.validation_reports.mkdir(parents=True, exist_ok=True)
        self.status_root.mkdir(parents=True, exist_ok=True)


def resolve_paths(repo_root: Path, source_root: Path | None, workbench_root: Path | None) -> WorkbenchPaths:
    resolved_source_root = (source_root or repo_root).resolve()
    resolved_workbench_root = (
        workbench_root
        or (repo_root / "formal" / "appsec_core")
    ).resolve()
    if not resolved_source_root.exists():
        raise FileNotFoundError(f"Source ontology root does not exist: {resolved_source_root}")
    if not resolved_workbench_root.exists():
        raise FileNotFoundError(f"Workbench root does not exist: {resolved_workbench_root}")
    return WorkbenchPaths(
        repo_root=repo_root.resolve(),
        source_root=resolved_source_root,
        workbench_root=resolved_workbench_root,
    )
