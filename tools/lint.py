#!/usr/bin/env python3
"""Carta semantic linter — graph health check.

Runs all structural checks from validate.py plus graph-level analysis
(missing pages, orphans, broken prerequisites, override ADR coverage).

Usage:
    python tools/lint.py [--root /path/to/carta]
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from carta_checks import (
    Diagnostic,
    check_bidirectional_contradictions,
    discover_content_files,
    parse_node,
    run_graph_checks,
    run_structural_checks,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Carta knowledge base")
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

    # Cross-node structural checks
    all_diags.extend(check_bidirectional_contradictions(nodes))

    # Graph / semantic checks
    all_diags.extend(run_graph_checks(nodes))

    # Output
    errors = [d for d in all_diags if d.severity == "error"]
    warnings = [d for d in all_diags if d.severity == "warning"]

    if errors:
        print("ERRORS")
        print("=" * 60)
        for diag in errors:
            print(diag)
            print()

    if warnings:
        print("WARNINGS")
        print("=" * 60)
        for diag in warnings:
            print(diag)
            print()

    # Summary
    print("-" * 60)
    print(f"Files scanned: {len(files)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors or warnings:
        # Breakdown by check
        check_counts: Counter[str] = Counter()
        for d in all_diags:
            check_counts[f"{d.severity}:{d.check}"] += 1
        print()
        for key, count in sorted(check_counts.items()):
            severity, check = key.split(":", 1)
            label = "error" if severity == "error" else "warning"
            print(f"  {count} {label}: {check}")

    # Exit code: 1 if errors, 0 otherwise (warnings don't block)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
