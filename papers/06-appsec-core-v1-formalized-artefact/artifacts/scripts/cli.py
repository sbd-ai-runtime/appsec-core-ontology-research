"""CLI for the bounded AppSec Core formalization workbench."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .build_inventory import write_inventory
from .build_label_catalog import write_label_catalog
from .build_owl import write_owl_starter
from .build_shacl import write_shacl_starter
from .paths import resolve_paths
from .source_bundle import load_source_bundle
from .validate_shacl import write_validation_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("inventory", "label-catalog", "owl-starter", "shacl-starter", "validate-shacl", "all"),
        help="Operation to run.",
    )
    parser.add_argument(
        "--source-root",
        default=None,
        help="Path to the canonical sbd-toe-ontology repository.",
    )
    parser.add_argument(
        "--workbench-root",
        default=None,
        help="Path to the AppSec Core formalization workbench root.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[5]

    try:
        paths = resolve_paths(
            repo_root=repo_root,
            source_root=Path(args.source_root).resolve() if args.source_root else None,
            workbench_root=Path(args.workbench_root).resolve() if args.workbench_root else None,
        )
        paths.ensure_dirs()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        bundle = load_source_bundle(paths)

        if args.command in {"label-catalog", "all"}:
            catalog_path = write_label_catalog(bundle=bundle, paths=paths)
            print(f"labels: {catalog_path}")
            bundle = load_source_bundle(paths)

        if args.command in {"inventory", "all"}:
            json_path, md_path = write_inventory(bundle=bundle, output_dir=paths.grounding_generated)
            print(f"inventory: {json_path}")
            print(f"inventory: {md_path}")

        if args.command in {"owl-starter", "all"}:
            owl_path = write_owl_starter(bundle=bundle, output_dir=paths.owl_exports)
            print(f"owl: {owl_path}")

        if args.command in {"shacl-starter", "all"}:
            shacl_path = write_shacl_starter(bundle=bundle, output_dir=paths.shacl_shapes)
            print(f"shacl: {shacl_path}")

        if args.command in {"validate-shacl", "all"}:
            json_path, md_path, summary = write_validation_report(paths=paths)
            print(f"validation: {json_path}")
            print(f"validation: {md_path}")
            if summary["violation_count"]:
                print(
                    f"error: SHACL validation found {summary['violation_count']} violation(s)",
                    file=sys.stderr,
                )
                return 1
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0
