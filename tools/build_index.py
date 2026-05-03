#!/usr/bin/env python3
"""Build INDEX.yaml (at the repository root) from the content tree.

The index is a derived artefact — content files stay the source of truth.
It pre-computes the inverted lookups that a traversal would otherwise get
by scanning every file in a directory (context→patterns, pillar→principles,
pattern→dtrees, etc.), plus a per-node frontmatter snapshot and the
transitive prerequisites closure.

Usage:
    python tools/build_index.py              # rebuild INDEX.yaml
    python tools/build_index.py --check      # fail if INDEX.yaml is stale
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml

from carta_checks import (
    discover_content_files,
    extract_wikilinks_from_value,
    parse_node,
)

INDEX_REL_PATH = "INDEX.yaml"

# Fields copied verbatim (non-wikilink values) into the per-entry snapshot.
SCALAR_FIELDS = [
    "category", "maturity", "stage_floor", "enforceability",
    "status", "date", "level_name",
]

# Fields whose values are wikilinks — stored as bare id lists in the index.
WIKILINK_LIST_FIELDS = [
    "applies_to", "prerequisites", "related", "conflicts_with",
    "contradicted_by", "composes", "mitigated_by", "pillars",
    "recommended_patterns", "recommended_standards",
    "common_antipatterns", "decides_between", "realised_by",
    "tradeoffs_with", "affects", "related_patterns",
    "related_antipatterns", "typical_antipatterns",
]

WIKILINK_SCALAR_FIELDS = ["pillar", "next_stage", "stage", "supersedes", "superseded_by"]


def _entry_key(node) -> str:
    """Unique key for a node based on its filename without the .md suffix.

    - Foundation: pattern-circuit-breaker
    - Org override: pattern-rest-api.org
    - Team extension: pattern-rate-limiting.platform
    - Project ADR: adr-0001-relaxed-circuit-breaker-timeouts.payments-api
    """
    name = node.filename
    return name[:-3] if name.endswith(".md") else name


def _node_snapshot(node) -> dict:
    fm = node.frontmatter
    snap: dict = {
        "id": node.node_id,
        "type": fm.get("type"),
        "level": node.level,
        "path": node.rel_path,
    }
    if node.level_name:
        snap["level_name"] = node.level_name
    for f in SCALAR_FIELDS:
        if f in fm and fm[f] not in (None, ""):
            snap[f] = fm[f]
    for f in WIKILINK_LIST_FIELDS:
        if f in fm:
            targets = extract_wikilinks_from_value(fm[f])
            if targets:
                snap[f] = targets
    for f in WIKILINK_SCALAR_FIELDS:
        if f in fm:
            targets = extract_wikilinks_from_value(fm[f])
            if targets:
                snap[f] = targets[0]
    # decision-tree carries a free-form criteria string list
    if fm.get("type") == "decision-tree" and "criteria" in fm:
        crit = fm["criteria"]
        if isinstance(crit, list):
            snap["criteria"] = [str(c) for c in crit]
    return snap


def _sort_values(d: dict) -> dict:
    return {
        k: sorted(set(v)) if isinstance(v, list) else v
        for k, v in sorted(d.items())
    }


def _compute_prereq_closure(nodes_by_entry: dict) -> dict:
    """Transitive prerequisites per pattern, cycle-safe. Keys and values are entry keys.

    Uses entry keys (foundation-level) since prerequisites reference ids that resolve
    to foundation entries in the normal case. Extensions with prereqs of the same id
    fall back to the foundation entry via id-lookup.
    """
    # id -> foundation entry key
    id_to_foundation_entry = {
        snap["id"]: entry
        for entry, snap in nodes_by_entry.items()
        if snap["level"] == "foundation"
    }

    def resolve(pat_id):
        return id_to_foundation_entry.get(pat_id, pat_id)

    closure_memo: dict = {}

    def walk(entry: str, visiting: frozenset) -> list:
        if entry in closure_memo:
            return closure_memo[entry]
        if entry in visiting:
            return []  # cycle
        snap = nodes_by_entry.get(entry)
        if not snap:
            return []
        direct = snap.get("prerequisites", [])
        result: list = []
        for p in direct:
            p_entry = resolve(p)
            if p_entry not in result:
                result.append(p_entry)
            for tp in walk(p_entry, visiting | {entry}):
                if tp not in result:
                    result.append(tp)
        closure_memo[entry] = result
        return result

    out: dict = {}
    for entry, snap in nodes_by_entry.items():
        if snap.get("type") != "pattern":
            continue
        closure = walk(entry, frozenset())
        if closure:
            out[entry] = closure
    return _sort_values(out)


def build_index(root: Path) -> dict:
    files = discover_content_files(root)

    # First pass: parse all nodes, collect snapshots keyed by entry key.
    nodes_by_entry: dict = {}
    by_id: dict = {}
    for path in files:
        node = parse_node(path, root)
        if node is None or not node.node_id:
            continue
        entry = _entry_key(node)
        nodes_by_entry[entry] = _node_snapshot(node)
        by_id.setdefault(node.node_id, []).append(entry)

    # Overrides: pattern_id -> {org: entry_key, teams: {name: key}, projects: {name: key}}
    overrides: dict = {}
    for entry, snap in nodes_by_entry.items():
        if "/overrides/" not in snap["path"]:
            continue
        nid = snap["id"]
        ov = overrides.setdefault(nid, {"org": None, "teams": {}, "projects": {}})
        if snap["level"] == "org":
            ov["org"] = entry
        elif snap["level"] == "team":
            ov["teams"][snap.get("level_name", "")] = entry
        elif snap["level"] == "project":
            ov["projects"][snap.get("level_name", "")] = entry
    # Drop empty nested dicts for readability
    for nid, ov in list(overrides.items()):
        if not ov["teams"]:
            del ov["teams"]
        if not ov["projects"]:
            del ov["projects"]
        if ov["org"] is None:
            del ov["org"]

    # Inverted indexes.
    ctx_patterns: dict = {}
    ctx_antipatterns: dict = {}
    ctx_standards: dict = {"__universal": []}
    pillar_principles: dict = {}
    pattern_principles: dict = {}
    pattern_dtrees: dict = {}
    affects_adrs: dict = {}
    solution_composes: dict = {}

    for entry, snap in nodes_by_entry.items():
        ntype = snap.get("type")
        applies_to = snap.get("applies_to", [])

        if ntype == "pattern":
            for ctx in applies_to:
                ctx_patterns.setdefault(ctx, []).append(entry)
        elif ntype == "antipattern":
            for ctx in applies_to:
                ctx_antipatterns.setdefault(ctx, []).append(entry)
        elif ntype == "standard":
            if applies_to:
                for ctx in applies_to:
                    ctx_standards.setdefault(ctx, []).append(entry)
            else:
                ctx_standards["__universal"].append(entry)

        if ntype == "principle":
            pillar = snap.get("pillar")
            if pillar:
                pillar_principles.setdefault(pillar, []).append(entry)
            for pat in snap.get("related_patterns", []):
                pattern_principles.setdefault(pat, []).append(entry)

        if ntype == "decision-tree":
            for pat in snap.get("decides_between", []):
                pattern_dtrees.setdefault(pat, []).append(entry)

        if ntype == "adr":
            for affected in snap.get("affects", []):
                affects_adrs.setdefault(affected, []).append(entry)

        if ntype == "solution":
            solution_composes[entry] = sorted(snap.get("composes", []))

        # Symmetric forward-edge collection from context nodes.
        #
        # Above, context_to_patterns / context_to_antipatterns /
        # context_to_standards are populated by walking each pattern /
        # antipattern / standard and reading its `applies_to` — a pattern
        # declares which contexts it applies to, and that reverse edge
        # builds the lookup.
        #
        # That alone is insufficient when a new context is introduced at
        # org / team / project level and references *foundation* patterns
        # via its `recommended_patterns`. Foundation nodes cannot declare
        # `applies_to: [[<extension-context>]]` without violating the
        # four-level dependency rule (foundations must not depend on
        # extensions). The reverse edge therefore never appears, and the
        # extension context lands in the index with an empty candidate
        # set even though it has explicit recommendations.
        #
        # The fix: also walk each context node and treat its forward
        # edges (recommended_patterns, common_antipatterns,
        # recommended_standards) as additional contributions to the same
        # three reverse lookups. The edge gets recorded the same way
        # regardless of which side declared it. _sort_values() runs
        # set() afterward so duplicates from both sides are deduped.
        if ntype == "context":
            ctx_id = snap["id"]
            for pat_id in snap.get("recommended_patterns", []):
                for pat_entry in by_id.get(pat_id, []):
                    pat_snap = nodes_by_entry.get(pat_entry)
                    if pat_snap and pat_snap.get("type") == "pattern":
                        ctx_patterns.setdefault(ctx_id, []).append(pat_entry)
            for ap_id in snap.get("common_antipatterns", []):
                for ap_entry in by_id.get(ap_id, []):
                    ap_snap = nodes_by_entry.get(ap_entry)
                    if ap_snap and ap_snap.get("type") == "antipattern":
                        ctx_antipatterns.setdefault(ctx_id, []).append(ap_entry)
            for std_id in snap.get("recommended_standards", []):
                for std_entry in by_id.get(std_id, []):
                    std_snap = nodes_by_entry.get(std_entry)
                    if std_snap and std_snap.get("type") == "standard":
                        ctx_standards.setdefault(ctx_id, []).append(std_entry)

    prereq_closure = _compute_prereq_closure(nodes_by_entry)

    # Freshness hash over all content file bytes.
    hasher = hashlib.sha256()
    for p in files:
        hasher.update(p.read_bytes())
    content_hash = hasher.hexdigest()[:16]

    return {
        "version": 1,
        "generated_from": content_hash,
        "node_count": len(nodes_by_entry),
        "entries": {k: nodes_by_entry[k] for k in sorted(nodes_by_entry)},
        "by_id": {k: sorted(v) for k, v in sorted(by_id.items())},
        "overrides": {k: overrides[k] for k in sorted(overrides)},
        "context_to_patterns": _sort_values(ctx_patterns),
        "context_to_antipatterns": _sort_values(ctx_antipatterns),
        "context_to_standards": _sort_values(ctx_standards),
        "pillar_to_principles": _sort_values(pillar_principles),
        "pattern_to_principles": _sort_values(pattern_principles),
        "pattern_to_dtrees": _sort_values(pattern_dtrees),
        "affects_to_adrs": _sort_values(affects_adrs),
        "solution_composes": _sort_values(solution_composes),
        "prerequisites_closure": prereq_closure,
    }


def dump_yaml(index: dict) -> str:
    return yaml.safe_dump(
        index, sort_keys=False, default_flow_style=False, width=100, allow_unicode=True
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build or check Carta INDEX.yaml")
    parser.add_argument(
        "--root", type=Path, default=Path.cwd(),
        help="Root of the Carta repository (default: cwd)",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Fail with non-zero exit if INDEX.yaml is missing or stale",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    index = build_index(root)
    rendered = dump_yaml(index)
    index_path = root / INDEX_REL_PATH

    if args.check:
        if not index_path.exists():
            print(f"✗ {INDEX_REL_PATH} is missing. Run: python tools/build_index.py")
            return 1
        current = index_path.read_text(encoding="utf-8")
        if current.strip() != rendered.strip():
            print(
                f"✗ {INDEX_REL_PATH} is stale. "
                f"Regenerate with: python tools/build_index.py"
            )
            return 1
        print(f"✓ {INDEX_REL_PATH} is fresh ({index['node_count']} nodes)")
        return 0

    index_path.write_text(rendered, encoding="utf-8")
    print(f"✓ Wrote {INDEX_REL_PATH} ({index['node_count']} nodes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
