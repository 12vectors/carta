#!/usr/bin/env python3
"""Carta structural validator — CI gate.

Checks all content nodes in foundations/, org/, teams/, projects/ for
schema compliance. Exits 0 if clean, 1 if errors found.

Usage:
    python tools/validate.py [--root /path/to/carta]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from carta_checks import (
    Diagnostic,
    check_bidirectional_contradictions,
    discover_content_files,
    parse_node,
    run_structural_checks,
)
from build_index import INDEX_REL_PATH, build_index, dump_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Carta content nodes")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Root of the Carta repository (default: current directory)",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    files = discover_content_files(root)
    if not files:
        print(f"No content files found in {root}")
        return 0

    all_diags: list[Diagnostic] = []
    nodes = []

    for path in files:
        node = parse_node(path, root)
        if node is None:
            all_diags.append(Diagnostic(
                str(path.relative_to(root)), "error", "Frontmatter",
                "File has no valid YAML frontmatter"
            ))
            continue
        nodes.append(node)
        all_diags.extend(run_structural_checks(node))

    # Cross-node checks
    all_diags.extend(check_bidirectional_contradictions(nodes))

    # Index freshness
    index_path = root / INDEX_REL_PATH
    if index_path.exists():
        expected = dump_yaml(build_index(root)).strip()
        actual = index_path.read_text(encoding="utf-8").strip()
        if expected != actual:
            all_diags.append(Diagnostic(
                INDEX_REL_PATH, "error", "Index freshness",
                "INDEX.yaml is stale — regenerate with: python tools/build_index.py"
            ))
    else:
        all_diags.append(Diagnostic(
            INDEX_REL_PATH, "error", "Index freshness",
            "INDEX.yaml is missing — generate with: python tools/build_index.py"
        ))

    # Output
    errors = [d for d in all_diags if d.severity == "error"]

    if errors:
        for diag in errors:
            print(diag)
            print()
        print(f"✗ {len(errors)} error(s) in {len(files)} files")
        return 1
    else:
        print(f"✓ {len(files)} files validated, no errors")
        return 0


if __name__ == "__main__":
    sys.exit(main())
