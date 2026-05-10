#!/usr/bin/env python3
"""Run the bounded AppSec Core formalization workbench helpers."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    package_src = repo_root / "formal" / "appsec_core" / "python" / "src"
    sys.path.insert(0, str(package_src))

    from appsec_core_formalization.cli import main as cli_main

    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
