"""Shared validation and linting logic for Carta content nodes."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_TYPES = {
    "pattern", "antipattern", "standard", "solution", "context", "adr",
    "pillar", "principle", "decision-tree", "stage",
}
VALID_STAGES = {"prototype", "mvp", "production", "critical"}
VALID_MATURITIES = {"experimental", "stable", "deprecated"}
VALID_PATTERN_CATEGORIES = {
    # styles — system-shape patterns
    "style",
    # tactics — concern-scoped patterns
    "communication", "data", "resilience", "scaling",
    "security", "agentic", "observability",
    "refactoring", "deployment",
    # integration — messaging, routing, transformation
    "integration",
}
VALID_ENFORCEABILITIES = {"automated", "review", "advisory"}
VALID_ADR_STATUSES = {"proposed", "accepted", "superseded", "rejected"}
VALID_PILLARS = {
    "reliability", "security", "cost",
    "operational-excellence", "performance",
}

CONTENT_DIRS = ["foundations", "org", "teams", "projects"]

# Wikilink fields per type (fields that should contain [[...]] values)
WIKILINK_FIELDS = {
    "applies_to", "prerequisites", "related", "conflicts_with",
    "contradicted_by", "composes", "mitigated_by", "recommended_patterns",
    "recommended_standards", "common_antipatterns", "affects",
    "supersedes", "superseded_by",
    "pillars",               # patterns/antipatterns/solutions -> pillar nodes
    "pillar",                # principle -> its pillar
    "realised_by",           # pillar -> principles that realise it
    "related_patterns",      # principle / decision-tree -> pattern nodes
    "decides_between",       # decision-tree -> the options being chosen between
    "tradeoffs_with",        # pillar -> conflicting pillars
    "next_stage",            # stage -> the stage that comes after this one
    "typical_antipatterns",  # stage -> antipatterns seen at this stage
}

# Required body sections per type
REQUIRED_SECTIONS = {
    "pattern": ["## When to use", "## When NOT to use", "## Decision inputs", "## Solution sketch", "## Trade-offs"],
    "antipattern": ["## How to recognise", "## Why it happens", "## Consequences", "## How to fix"],
    "standard": ["## Requirement", "## Rationale", "## Compliance", "## Non-compliance"],
    "solution": ["## Problem", "## Composition", "## Decision inputs", "## Trade-offs", "## Implementation sequence"],
    "context": ["## Description", "## Key concerns"],
    "adr": ["## Context", "## Decision", "## Consequences"],
    "pillar": ["## Description", "## Trade-offs"],
    "principle": ["## Statement", "## Rationale", "## How to apply"],
    "decision-tree": ["## Problem", "## Criteria", "## Recommendation"],
    "stage": ["## Description", "## What relaxes", "## What stays baseline"],
}

# Required type-specific frontmatter fields
REQUIRED_TYPE_FIELDS = {
    "pattern": ["category", "applies_to"],
    "antipattern": ["category", "applies_to"],
    "standard": ["category", "enforceability"],
    "solution": ["composes", "applies_to"],
    "context": ["signals", "recommended_patterns"],
    "adr": ["status", "date", "affects"],
    "pillar": [],
    "principle": ["pillar"],
    "decision-tree": ["decides_between", "criteria"],
    "stage": [],
}

# Types that require non-empty sources
SOURCES_REQUIRED_TYPES = {"pattern", "antipattern", "solution"}

ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


# ---------------------------------------------------------------------------
# Writing rule thresholds (see 00-meta/writing-rules.md)
# ---------------------------------------------------------------------------

# Section word caps (total words in section body, excluding heading)
SECTION_WORD_CAPS: dict[str, int] = {
    "## Solution sketch": 150,
    "## Description": 150,
    "## Key concerns": 150,
    "## Problem": 120,
    "## Rationale": 120,
    "## Context": 150,
    "## Decision": 150,
    "## Consequences": 150,
}

# Sections where bullets are expected and capped
BULLET_SECTION_CAPS: dict[str, dict[str, int]] = {
    "## When to use":          {"max_bullets": 6, "max_words_per_bullet": 25},
    "## When NOT to use":      {"max_bullets": 6, "max_words_per_bullet": 25},
    "## Decision inputs":      {"max_bullets": 6, "max_words_per_bullet": 30},
    "## How to recognise":     {"max_bullets": 6, "max_words_per_bullet": 25},
    "## Why it happens":       {"max_bullets": 6, "max_words_per_bullet": 25},
    "## Consequences":         {"max_bullets": 6, "max_words_per_bullet": 25},
    "## How to fix":           {"max_bullets": 6, "max_words_per_bullet": 30},
    "## Implementation checklist": {"max_bullets": 10, "max_words_per_bullet": 30},
    "## Signals":              {"max_bullets": 8, "max_words_per_bullet": 20},
}

# Trade-offs table row cap
TRADEOFFS_MAX_ROWS = 5

# Phrases that typically indicate explanatory/tutorial prose
EXPLANATORY_PHRASES = [
    "in other words",
    "this means that",
    "for example, imagine",
    "it's important to note",
    "it is important to note",
    "historically",
    "as we can see",
    "as mentioned earlier",
    "to put it simply",
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Diagnostic:
    path: str
    severity: str  # "error" or "warning"
    check: str
    message: str

    def __str__(self) -> str:
        label = "ERROR " if self.severity == "error" else "WARN  "
        return f"{label} {self.path}\n       {self.check}: {self.message}"


@dataclass
class Node:
    path: Path
    rel_path: str
    frontmatter: dict
    body: str
    level: str          # "foundation", "org", "team", "project"
    level_name: str     # "" for foundation/org, team/project name otherwise

    @property
    def node_id(self) -> Optional[str]:
        return self.frontmatter.get("id")

    @property
    def node_type(self) -> Optional[str]:
        return self.frontmatter.get("type")

    @property
    def filename(self) -> str:
        return self.path.name


# ---------------------------------------------------------------------------
# File discovery and parsing
# ---------------------------------------------------------------------------

def discover_content_files(root: Path) -> list[Path]:
    """Find all .md content files in foundations/, org/, teams/, projects/."""
    files = []
    for dir_name in CONTENT_DIRS:
        content_dir = root / dir_name
        if content_dir.is_dir():
            for md in content_dir.rglob("*.md"):
                files.append(md)
    return sorted(files)


def parse_node(path: Path, root: Path) -> Optional[Node]:
    """Parse a markdown file into a Node. Returns None if no frontmatter."""
    text = path.read_text(encoding="utf-8")
    rel_path = str(path.relative_to(root))

    # Split frontmatter
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        fm = None

    if not isinstance(fm, dict):
        fm = {}

    body = parts[2]
    level, level_name = determine_level(rel_path)
    return Node(
        path=path,
        rel_path=rel_path,
        frontmatter=fm,
        body=body,
        level=level,
        level_name=level_name,
    )


def determine_level(rel_path: str) -> tuple[str, str]:
    """Determine the level and level name from a relative path.

    Returns (level, level_name) where:
    - ("foundation", "") for foundations/...
    - ("org", "") for org/...
    - ("team", "platform") for teams/platform/...
    - ("project", "payments-api") for projects/payments-api/...
    """
    parts = Path(rel_path).parts
    if parts[0] == "foundations":
        return ("foundation", "")
    elif parts[0] == "org":
        return ("org", "")
    elif parts[0] == "teams" and len(parts) >= 2:
        return ("team", parts[1])
    elif parts[0] == "projects" and len(parts) >= 2:
        return ("project", parts[1])
    return ("unknown", "")


def extract_wikilinks_from_value(value) -> list[str]:
    """Extract [[target]] IDs from a frontmatter field value."""
    targets = []
    if isinstance(value, str):
        for m in WIKILINK_RE.finditer(value):
            targets.append(m.group(1))
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                for m in WIKILINK_RE.finditer(item):
                    targets.append(m.group(1))
    return targets


def collect_all_wikilinks(fm: dict) -> list[str]:
    """Collect all wikilink targets from all frontmatter fields."""
    targets = []
    for key, value in fm.items():
        if key in WIKILINK_FIELDS:
            targets.extend(extract_wikilinks_from_value(value))
    return targets


def get_expected_filename(node: Node) -> str:
    """What the filename should be given the node's id and level."""
    node_id = node.node_id or ""
    if node.level == "foundation":
        return f"{node_id}.md"
    elif node.level == "org":
        return f"{node_id}.org.md"
    elif node.level == "team":
        return f"{node_id}.{node.level_name}.md"
    elif node.level == "project":
        return f"{node_id}.{node.level_name}.md"
    return f"{node_id}.md"


def get_id_from_filename(filename: str, level: str, level_name: str) -> str:
    """Extract the expected node ID from a filename given its level."""
    name = filename
    if name.endswith(".md"):
        name = name[:-3]
    if level == "org" and name.endswith(".org"):
        name = name[:-4]
    elif level in ("team", "project") and level_name and name.endswith(f".{level_name}"):
        name = name[: -(len(level_name) + 1)]
    return name


# ---------------------------------------------------------------------------
# Structural checks (validate.py)
# ---------------------------------------------------------------------------

def check_frontmatter_present(node: Node) -> list[Diagnostic]:
    """Check that frontmatter was parsed successfully."""
    if not node.frontmatter:
        return [Diagnostic(node.rel_path, "error", "Frontmatter", "No valid YAML frontmatter found")]
    return []


def check_required_universal_fields(node: Node) -> list[Diagnostic]:
    diags = []
    for field_name in ["id", "title", "type", "maturity", "tags"]:
        if field_name not in node.frontmatter:
            diags.append(Diagnostic(
                node.rel_path, "error", "Required field",
                f"Missing required field: {field_name}"
            ))
    return diags


def check_type_enum(node: Node) -> list[Diagnostic]:
    t = node.frontmatter.get("type")
    if t and t not in VALID_TYPES:
        return [Diagnostic(
            node.rel_path, "error", "Type enum",
            f"Invalid type '{t}', must be one of: {', '.join(sorted(VALID_TYPES))}"
        )]
    return []


def check_maturity_enum(node: Node) -> list[Diagnostic]:
    m = node.frontmatter.get("maturity")
    if m and m not in VALID_MATURITIES:
        return [Diagnostic(
            node.rel_path, "error", "Maturity enum",
            f"Invalid maturity '{m}', must be one of: {', '.join(sorted(VALID_MATURITIES))}"
        )]
    return []


def check_id_filename_match(node: Node) -> list[Diagnostic]:
    node_id = node.frontmatter.get("id")
    if not node_id:
        return []  # Already caught by required fields check
    expected_id = get_id_from_filename(node.filename, node.level, node.level_name)
    if node_id != expected_id:
        return [Diagnostic(
            node.rel_path, "error", "ID-filename match",
            f"id '{node_id}' does not match filename '{node.filename}' "
            f"(expected id '{expected_id}')"
        )]
    return []


def check_level_suffix(node: Node) -> list[Diagnostic]:
    filename = node.filename
    if node.level == "foundation":
        # Should NOT have a level suffix — just <id>.md
        # Check it doesn't have .org.md or similar
        parts = filename.rsplit(".", 2)
        if len(parts) > 2:
            # e.g. something.org.md — has a suffix
            return [Diagnostic(
                node.rel_path, "error", "Level suffix",
                f"Foundation file should not have a level suffix, got '{filename}'"
            )]
    elif node.level == "org":
        if not filename.endswith(".org.md"):
            return [Diagnostic(
                node.rel_path, "error", "Level suffix",
                f"Org-level file should end with '.org.md', got '{filename}'"
            )]
    elif node.level == "team":
        expected_suffix = f".{node.level_name}.md"
        if not filename.endswith(expected_suffix):
            return [Diagnostic(
                node.rel_path, "error", "Level suffix",
                f"Team-level file should end with '{expected_suffix}', got '{filename}'"
            )]
    elif node.level == "project":
        expected_suffix = f".{node.level_name}.md"
        if not filename.endswith(expected_suffix):
            return [Diagnostic(
                node.rel_path, "error", "Level suffix",
                f"Project-level file should end with '{expected_suffix}', got '{filename}'"
            )]
    return []


def check_tag_consistency(node: Node) -> list[Diagnostic]:
    diags = []
    tags = node.frontmatter.get("tags", [])
    if not isinstance(tags, list):
        return [Diagnostic(node.rel_path, "error", "Tag consistency", "tags must be a list")]
    node_type = node.frontmatter.get("type")
    maturity = node.frontmatter.get("maturity")
    if node_type and node_type not in tags:
        diags.append(Diagnostic(
            node.rel_path, "error", "Tag consistency",
            f"tags missing type value '{node_type}' (has: {tags})"
        ))
    if maturity and maturity not in tags:
        diags.append(Diagnostic(
            node.rel_path, "error", "Tag consistency",
            f"tags missing maturity value '{maturity}' (has: {tags})"
        ))
    return diags


def check_type_specific_fields(node: Node) -> list[Diagnostic]:
    diags = []
    node_type = node.frontmatter.get("type")
    if not node_type or node_type not in REQUIRED_TYPE_FIELDS:
        return []

    for field_name in REQUIRED_TYPE_FIELDS[node_type]:
        value = node.frontmatter.get(field_name)
        if value is None:
            diags.append(Diagnostic(
                node.rel_path, "error", "Type-specific field",
                f"{node_type} requires field '{field_name}'"
            ))
        elif isinstance(value, list) and len(value) == 0:
            # Required list fields must be non-empty
            if field_name in ("applies_to", "composes", "signals", "recommended_patterns", "affects", "decides_between", "criteria"):
                diags.append(Diagnostic(
                    node.rel_path, "error", "Type-specific field",
                    f"{node_type} requires non-empty '{field_name}'"
                ))
    return diags


def check_type_specific_enums(node: Node) -> list[Diagnostic]:
    diags = []
    node_type = node.frontmatter.get("type")

    if node_type == "pattern":
        cat = node.frontmatter.get("category")
        if cat and cat not in VALID_PATTERN_CATEGORIES:
            diags.append(Diagnostic(
                node.rel_path, "error", "Category enum",
                f"Invalid pattern category '{cat}', must be one of: {', '.join(sorted(VALID_PATTERN_CATEGORIES))}"
            ))
        floor = node.frontmatter.get("stage_floor")
        if floor is not None and floor not in VALID_STAGES:
            diags.append(Diagnostic(
                node.rel_path, "error", "stage_floor enum",
                f"Invalid stage_floor '{floor}', must be one of: {', '.join(sorted(VALID_STAGES))}"
            ))

    if node_type == "standard":
        enf = node.frontmatter.get("enforceability")
        if enf and enf not in VALID_ENFORCEABILITIES:
            diags.append(Diagnostic(
                node.rel_path, "error", "Enforceability enum",
                f"Invalid enforceability '{enf}', must be one of: {', '.join(sorted(VALID_ENFORCEABILITIES))}"
            ))

    if node_type == "adr":
        status = node.frontmatter.get("status")
        if status and status not in VALID_ADR_STATUSES:
            diags.append(Diagnostic(
                node.rel_path, "error", "ADR status enum",
                f"Invalid status '{status}', must be one of: {', '.join(sorted(VALID_ADR_STATUSES))}"
            ))
        date = node.frontmatter.get("date")
        if date and not ISO_DATE_RE.match(str(date)):
            diags.append(Diagnostic(
                node.rel_path, "error", "ADR date format",
                f"Invalid date '{date}', must be ISO 8601 (YYYY-MM-DD)"
            ))

    return diags


def check_wikilink_format(node: Node) -> list[Diagnostic]:
    diags = []
    for key in WIKILINK_FIELDS:
        value = node.frontmatter.get(key)
        if value is None:
            continue
        items = [value] if isinstance(value, str) else (value if isinstance(value, list) else [])
        for item in items:
            if not isinstance(item, str):
                continue
            if not item.strip():
                continue
            # Should be [[...]] format
            if not WIKILINK_RE.search(item):
                diags.append(Diagnostic(
                    node.rel_path, "error", "Wikilink format",
                    f"Field '{key}' contains '{item}' which is not in [[...]] format"
                ))
    return diags


def check_sources_required(node: Node) -> list[Diagnostic]:
    node_type = node.frontmatter.get("type")
    if node_type not in SOURCES_REQUIRED_TYPES:
        return []
    sources = node.frontmatter.get("sources")
    if not sources or (isinstance(sources, list) and len(sources) == 0):
        return [Diagnostic(
            node.rel_path, "error", "Sources required",
            f"{node_type} requires at least one source"
        )]
    if isinstance(sources, list) and all(not s.strip() for s in sources if isinstance(s, str)):
        return [Diagnostic(
            node.rel_path, "error", "Sources required",
            f"{node_type} has only empty sources"
        )]
    return []


def check_required_body_sections(node: Node) -> list[Diagnostic]:
    diags = []
    node_type = node.frontmatter.get("type")
    if not node_type or node_type not in REQUIRED_SECTIONS:
        return []

    for section in REQUIRED_SECTIONS[node_type]:
        # Check for the heading (case-insensitive for robustness)
        if section.lower() not in node.body.lower():
            diags.append(Diagnostic(
                node.rel_path, "error", "Required body section",
                f"Missing section: {section}"
            ))
    return diags


def check_category_directory_match(node: Node) -> list[Diagnostic]:
    """For foundation patterns, category should match the subdirectory layout.

    Expected tree:
        foundations/20-patterns/styles/<file>              -> category: style
        foundations/20-patterns/tactics/<concern>/<file>   -> category: <concern>
        foundations/20-patterns/integration/<file>         -> category: integration
    """
    if node.level != "foundation" or node.frontmatter.get("type") != "pattern":
        return []
    category = node.frontmatter.get("category")
    if not category:
        return []
    parts = Path(node.rel_path).parts
    if len(parts) < 3 or parts[1] != "20-patterns":
        return []

    top = parts[2]
    if top == "styles":
        expected = "style"
        if category != expected:
            return [Diagnostic(
                node.rel_path, "error", "Category-directory match",
                f"files in styles/ must have category '{expected}', got '{category}'"
            )]
    elif top == "integration":
        expected = "integration"
        if category != expected:
            return [Diagnostic(
                node.rel_path, "error", "Category-directory match",
                f"files in integration/ must have category '{expected}', got '{category}'"
            )]
    elif top == "tactics":
        if len(parts) < 4:
            return [Diagnostic(
                node.rel_path, "error", "Category-directory match",
                "tactics/ patterns must be nested one level deeper (tactics/<concern>/)"
            )]
        dir_concern = parts[3]
        if dir_concern != category:
            return [Diagnostic(
                node.rel_path, "error", "Category-directory match",
                f"category '{category}' does not match directory 'tactics/{dir_concern}/'"
            )]
    else:
        return [Diagnostic(
            node.rel_path, "error", "Category-directory match",
            f"pattern must live under styles/, tactics/<concern>/, or integration/, got '{top}/'"
        )]
    return []


def check_pillars(node: Node) -> list[Diagnostic]:
    """Validate the `pillars` field (list of wikilinks to pillar nodes).

    Format is checked by the generic wikilink check; this only enforces that
    the value, when present, is a list (not a bare string).
    """
    if node.frontmatter.get("type") not in {"pattern", "antipattern", "solution"}:
        return []
    pillars = node.frontmatter.get("pillars")
    if pillars is None:
        return []
    if not isinstance(pillars, list):
        return [Diagnostic(
            node.rel_path, "error", "Pillars format",
            "pillars must be a list of wikilinks to pillar nodes"
        )]
    return []


def check_bidirectional_contradictions(nodes: list[Node]) -> list[Diagnostic]:
    """Check that contradicted_by links are bidirectional across all nodes."""
    diags = []
    # Build map of id -> contradicted_by targets
    contradiction_map: dict[str, set[str]] = {}
    id_to_path: dict[str, str] = {}
    for node in nodes:
        nid = node.node_id
        if not nid:
            continue
        # Use the first occurrence of each id (foundation level)
        if nid not in id_to_path:
            id_to_path[nid] = node.rel_path
        targets = extract_wikilinks_from_value(node.frontmatter.get("contradicted_by", []))
        if targets:
            contradiction_map[nid] = set(targets)

    for nid, targets in contradiction_map.items():
        for target in targets:
            reverse = contradiction_map.get(target, set())
            if nid not in reverse:
                diags.append(Diagnostic(
                    id_to_path.get(nid, nid), "error", "Bidirectional contradictions",
                    f"contradicted_by lists [[{target}]] but {target} does not list [[{nid}]]"
                ))
    return diags


# Collect all structural checks
def run_structural_checks(node: Node) -> list[Diagnostic]:
    """Run all per-node structural checks."""
    diags = []
    diags.extend(check_frontmatter_present(node))
    if not node.frontmatter:
        return diags  # Can't check further without frontmatter
    diags.extend(check_required_universal_fields(node))
    diags.extend(check_type_enum(node))
    diags.extend(check_maturity_enum(node))
    diags.extend(check_id_filename_match(node))
    diags.extend(check_level_suffix(node))
    diags.extend(check_tag_consistency(node))
    diags.extend(check_type_specific_fields(node))
    diags.extend(check_type_specific_enums(node))
    diags.extend(check_wikilink_format(node))
    diags.extend(check_sources_required(node))
    diags.extend(check_required_body_sections(node))
    diags.extend(check_category_directory_match(node))
    diags.extend(check_pillars(node))
    return diags


# ---------------------------------------------------------------------------
# Graph / semantic checks (lint.py additions)
# ---------------------------------------------------------------------------

def check_missing_pages(nodes: list[Node]) -> list[Diagnostic]:
    """Find wikilink targets that don't resolve to any file."""
    diags = []
    # Build set of all known IDs and filenames (without .md)
    known_ids: set[str] = set()
    known_filenames: set[str] = set()
    for node in nodes:
        if node.node_id:
            known_ids.add(node.node_id)
        fname = node.filename
        if fname.endswith(".md"):
            known_filenames.add(fname[:-3])

    # Collect all wikilink targets
    all_targets: dict[str, set[str]] = {}  # target -> set of files referencing it
    for node in nodes:
        targets = collect_all_wikilinks(node.frontmatter)
        for t in targets:
            all_targets.setdefault(t, set()).add(node.rel_path)

    # Also collect all body wikilinks
    for node in nodes:
        for m in WIKILINK_RE.finditer(node.body):
            t = m.group(1)
            all_targets.setdefault(t, set()).add(node.rel_path)

    for target, referencing_files in sorted(all_targets.items()):
        if target not in known_ids and target not in known_filenames:
            # Pick first referencing file for the diagnostic
            ref_file = sorted(referencing_files)[0]
            diags.append(Diagnostic(
                ref_file, "warning", "Missing page",
                f"Wikilink target [[{target}]] has no corresponding node"
            ))
    return diags


def check_orphan_nodes(nodes: list[Node]) -> list[Diagnostic]:
    """Find nodes that nothing else links to."""
    diags = []
    # Build set of all inbound targets (both bare IDs and suffixed filenames)
    inbound: set[str] = set()
    for node in nodes:
        targets = collect_all_wikilinks(node.frontmatter)
        inbound.update(targets)
        # Also check body for wikilinks (e.g. [[adr-0001-fastapi-as-default.org]])
        for m in WIKILINK_RE.finditer(node.body):
            inbound.add(m.group(1))

    for node in nodes:
        nid = node.node_id
        if not nid:
            continue
        # Contexts are entry points — they're expected to have no inbound from patterns
        if node.frontmatter.get("type") == "context":
            continue
        # Check both bare ID and suffixed filename (without .md)
        suffixed_name = node.filename[:-3] if node.filename.endswith(".md") else node.filename
        if nid not in inbound and suffixed_name not in inbound:
            diags.append(Diagnostic(
                node.rel_path, "warning", "Orphan node",
                f"Node '{nid}' has no inbound wikilinks from other nodes"
            ))
    return diags


def check_broken_prerequisites(nodes: list[Node]) -> list[Diagnostic]:
    """Check for circular or dangling prerequisite chains."""
    diags = []
    known_ids: set[str] = set()
    prereq_map: dict[str, list[str]] = {}
    id_to_path: dict[str, str] = {}

    for node in nodes:
        nid = node.node_id
        if not nid:
            continue
        known_ids.add(nid)
        if nid not in id_to_path:
            id_to_path[nid] = node.rel_path
        prereqs = extract_wikilinks_from_value(node.frontmatter.get("prerequisites", []))
        if prereqs:
            prereq_map[nid] = prereqs

    # Check for dangling
    for nid, prereqs in prereq_map.items():
        for p in prereqs:
            if p not in known_ids:
                diags.append(Diagnostic(
                    id_to_path[nid], "error", "Broken prerequisite",
                    f"Prerequisite [[{p}]] does not exist"
                ))

    # Check for cycles using DFS
    def has_cycle(start: str, visited: set[str], path: list[str]) -> Optional[list[str]]:
        if start in visited:
            return path + [start]
        visited.add(start)
        path.append(start)
        for prereq in prereq_map.get(start, []):
            if prereq in known_ids:
                result = has_cycle(prereq, visited, path[:])
                if result:
                    return result
        return None

    checked: set[str] = set()
    for nid in prereq_map:
        if nid not in checked:
            cycle = has_cycle(nid, set(), [])
            if cycle:
                cycle_str = " → ".join(cycle)
                diags.append(Diagnostic(
                    id_to_path[nid], "error", "Circular prerequisites",
                    f"Cycle detected: {cycle_str}"
                ))
            checked.add(nid)

    return diags


def check_override_has_adr(nodes: list[Node]) -> list[Diagnostic]:
    """Check that override files have a corresponding ADR at the same level."""
    diags = []
    # Group nodes by level
    decisions_by_level: dict[str, set[str]] = {}  # "org" or "team:platform" -> set of affected ids
    for node in nodes:
        if node.frontmatter.get("type") != "adr":
            continue
        level_key = node.level if node.level in ("foundation", "org") else f"{node.level}:{node.level_name}"
        affects = extract_wikilinks_from_value(node.frontmatter.get("affects", []))
        decisions_by_level.setdefault(level_key, set()).update(affects)

    for node in nodes:
        # Check if this is in an overrides/ directory
        if "/overrides/" not in node.rel_path:
            continue
        nid = node.node_id
        if not nid:
            continue
        level_key = node.level if node.level in ("foundation", "org") else f"{node.level}:{node.level_name}"
        affected_ids = decisions_by_level.get(level_key, set())
        if nid not in affected_ids:
            diags.append(Diagnostic(
                node.rel_path, "warning", "Override without ADR",
                f"Override for '{nid}' has no corresponding ADR at the {node.level} level "
                f"with affects: [[{nid}]]"
            ))
    return diags


def check_adr_supersedes_consistency(nodes: list[Node]) -> list[Diagnostic]:
    """Check that supersedes/superseded_by are bidirectional and status is consistent."""
    diags = []
    adr_nodes = [n for n in nodes if n.frontmatter.get("type") == "adr"]
    id_to_path: dict[str, str] = {}
    supersedes_map: dict[str, str] = {}  # id -> target
    superseded_by_map: dict[str, str] = {}  # id -> target

    for node in adr_nodes:
        nid = node.node_id
        if not nid:
            continue
        id_to_path[nid] = node.rel_path

        sup = extract_wikilinks_from_value(node.frontmatter.get("supersedes", ""))
        if sup:
            supersedes_map[nid] = sup[0]
        sup_by = extract_wikilinks_from_value(node.frontmatter.get("superseded_by", ""))
        if sup_by:
            superseded_by_map[nid] = sup_by[0]

        # Status consistency
        status = node.frontmatter.get("status")
        if status == "superseded" and not sup_by:
            diags.append(Diagnostic(
                node.rel_path, "warning", "ADR supersedes consistency",
                "status is 'superseded' but superseded_by is empty"
            ))
        if sup_by and status != "superseded":
            diags.append(Diagnostic(
                node.rel_path, "warning", "ADR supersedes consistency",
                f"superseded_by is set but status is '{status}', expected 'superseded'"
            ))

    # Bidirectionality
    for nid, target in supersedes_map.items():
        reverse = superseded_by_map.get(target)
        if reverse != nid:
            diags.append(Diagnostic(
                id_to_path.get(nid, nid), "warning", "ADR supersedes consistency",
                f"supersedes [[{target}]] but {target} does not have superseded_by: [[{nid}]]"
            ))

    return diags


def run_graph_checks(nodes: list[Node]) -> list[Diagnostic]:
    """Run all graph-level checks."""
    diags = []
    diags.extend(check_missing_pages(nodes))
    diags.extend(check_orphan_nodes(nodes))
    diags.extend(check_broken_prerequisites(nodes))
    diags.extend(check_override_has_adr(nodes))
    diags.extend(check_adr_supersedes_consistency(nodes))
    return diags


# ---------------------------------------------------------------------------
# Writing rule checks (soft — warnings only)
# ---------------------------------------------------------------------------

def split_body_into_sections(body: str) -> dict[str, str]:
    """Split a node body into a dict of {heading: content} for H2 sections.

    Heading keys are kept in their original form (e.g. "## When to use").
    """
    sections: dict[str, str] = {}
    current_heading: Optional[str] = None
    current_lines: list[str] = []

    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            # Flush previous section
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = stripped
            current_lines = []
        else:
            if current_heading is not None:
                current_lines.append(line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()
    return sections


def _strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks from text so word counts exclude code."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def _count_words(text: str) -> int:
    return len(_strip_code_blocks(text).split())


def _extract_top_level_bullets(text: str) -> list[str]:
    """Return top-level bullet items from a section (ignoring nested bullets)."""
    bullets: list[str] = []
    current: Optional[list[str]] = None
    in_fence = False

    for line in _strip_code_blocks(text).splitlines():
        # A top-level bullet starts with '-' or '*' with no leading whitespace
        # (allow up to 1 leading space for formatting tolerance).
        raw = line.rstrip()
        if raw.startswith("- ") or raw.startswith("* "):
            if current is not None:
                bullets.append(" ".join(current).strip())
            current = [raw[2:].strip()]
        elif raw.startswith("  ") and current is not None:
            # Continuation of the current bullet (wrapped line or nested content).
            current.append(raw.strip())
        elif raw == "":
            # Blank line — preserve current; continuation stops only on new content.
            continue
        else:
            # Non-bullet content ends the current bullet.
            if current is not None:
                bullets.append(" ".join(current).strip())
                current = None
    if current is not None:
        bullets.append(" ".join(current).strip())
    return [b for b in bullets if b]


def _count_tradeoffs_rows(text: str) -> int:
    """Count data rows in the Trade-offs markdown table.

    The table format is:
        | Gain | Cost |
        |------|------|
        | ...  | ...  |
    """
    rows = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        # Skip the header row and separator row
        if set(stripped.replace("|", "").strip()) <= set("-: "):
            continue  # separator
        # Heuristic: the header row contains "Gain" and "Cost"
        lower = stripped.lower()
        if "gain" in lower and "cost" in lower and rows == 0:
            continue
        rows += 1
    return rows


def check_writing_rules(node: Node) -> list[Diagnostic]:
    """Soft warnings for verbosity and tutorial-style prose.

    Backed by 00-meta/writing-rules.md. Warnings only — never blocking.
    """
    diags: list[Diagnostic] = []
    node_type = node.frontmatter.get("type")
    if node_type not in {"pattern", "antipattern", "standard", "solution", "context", "adr"}:
        return diags

    sections = split_body_into_sections(node.body)

    # Section word caps (prose sections)
    for heading, cap in SECTION_WORD_CAPS.items():
        content = sections.get(heading)
        if content is None:
            continue
        words = _count_words(content)
        if words > cap:
            diags.append(Diagnostic(
                node.rel_path, "warning", "Writing rule: section length",
                f"{heading} is {words} words (soft cap: {cap}). "
                f"Consider trimming or linking to a source for depth."
            ))

    # Bullet-shaped sections
    for heading, caps in BULLET_SECTION_CAPS.items():
        content = sections.get(heading)
        if content is None:
            continue
        bullets = _extract_top_level_bullets(content)
        if not bullets:
            # Section exists but has no bullets — likely prose where bullets were expected.
            # Only warn if the section has substantive content.
            if _count_words(content) > 40:
                diags.append(Diagnostic(
                    node.rel_path, "warning", "Writing rule: bullets preferred",
                    f"{heading} appears to be prose. Prefer bullets (see writing-rules.md)."
                ))
            continue
        if len(bullets) > caps["max_bullets"]:
            diags.append(Diagnostic(
                node.rel_path, "warning", "Writing rule: too many bullets",
                f"{heading} has {len(bullets)} bullets (soft cap: {caps['max_bullets']}). "
                f"Consider consolidating."
            ))
        over_long = [
            (i + 1, _count_words(b))
            for i, b in enumerate(bullets)
            if _count_words(b) > caps["max_words_per_bullet"]
        ]
        if over_long:
            example = ", ".join(f"#{i}={w}w" for i, w in over_long[:3])
            diags.append(Diagnostic(
                node.rel_path, "warning", "Writing rule: long bullets",
                f"{heading} has {len(over_long)} bullet(s) over "
                f"{caps['max_words_per_bullet']} words ({example}). "
                f"Bullets should be directive, not prose."
            ))

    # Trade-offs row cap
    tradeoffs = sections.get("## Trade-offs")
    if tradeoffs:
        rows = _count_tradeoffs_rows(tradeoffs)
        if rows > TRADEOFFS_MAX_ROWS:
            diags.append(Diagnostic(
                node.rel_path, "warning", "Writing rule: trade-offs table",
                f"## Trade-offs has {rows} rows (soft cap: {TRADEOFFS_MAX_ROWS}). "
                f"Keep the top trade-offs; cut the rest."
            ))

    # Explanatory phrases anywhere in the body
    body_lower = node.body.lower()
    hits = [p for p in EXPLANATORY_PHRASES if p in body_lower]
    if hits:
        diags.append(Diagnostic(
            node.rel_path, "warning", "Writing rule: explanatory phrasing",
            f"Body contains explanatory phrase(s): {', '.join(repr(h) for h in hits)}. "
            f"These often signal deletable content — see writing-rules.md."
        ))

    return diags
