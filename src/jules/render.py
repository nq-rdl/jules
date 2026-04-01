"""Jinja2 renderer for Jules dispatch workflow templates.

Usage:
    python -m jules.render <config.yml> [--output-dir <dir>]
    python -m jules.render --validate <workflow.yml>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = ROOT / "templates"
PROMPTS_DIR = ROOT / ".claude" / "skills" / "jules-prompt" / "references"

# Map role names to their shared instruction files
SHARED_INSTRUCTIONS = {
    "swe": "swe-instructions.md",
    "docs": "docs-instructions.md",
    "security": "security-instructions.md",
    "issue": "issue-instructions.md",
}

DEFAULT_PERMISSIONS = {
    "contents": "read",
    "issues": "write",
    "pull-requests": "read",
}

TRIGGER_SCOPE_CONDITIONS = {
    "all_comments": None,
    "issues_only": "github.event.issue.pull_request == null",
    "prs_only": "github.event.issue.pull_request != null",
}

# Role defaults when not specified in config
ROLE_DEFAULTS = {
    "swe": {
        "persona": "Software Engineer",
        "title_prefix": "SWE",
        "role_display_name": "SWE",
        "negative_filters": True,
        "detect_pr_branch": False,
    },
    "docs": {
        "persona": "Technical Writer",
        "title_prefix": "Docs",
        "role_display_name": "Docs",
        "negative_filters": False,
        "detect_pr_branch": False,
    },
    "security": {
        "persona": "Security Engineer",
        "title_prefix": "Security",
        "role_display_name": "Security Review",
        "negative_filters": False,
        "detect_pr_branch": True,
    },
    "issue": {
        "persona": "Engineering Triage Lead",
        "title_prefix": "Issue",
        "role_display_name": "Issue Triage",
        "negative_filters": False,
        "detect_pr_branch": False,
        "trigger_scope": "issues_only",
        "permissions": {
            "contents": "read",
            "issues": "write",
        },
    },
}


def load_config(config_path: Path) -> dict:
    """Load a project config YAML file."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def _load_shared_prompt(name: str, prompts_dir: Path) -> str:
    """Load a shared prompt block from .claude/skills/jules-prompt/references/shared/."""
    path = prompts_dir / "shared" / name
    if not path.exists():
        raise FileNotFoundError(f"Shared prompt not found: {path}")
    content = path.read_text().strip()
    # Remove the leading ## heading — the template adds its own structure
    lines = content.split("\n")
    if lines and lines[0].startswith("## "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def _resolve_instructions(role: dict, prompts_dir: Path) -> str:
    """Resolve the instructions for a role — either shared or inline."""
    instructions_value = role.get("instructions", "")
    if instructions_value == "shared":
        role_name = role["name"]
        filename = SHARED_INSTRUCTIONS.get(role_name)
        if filename:
            return _load_shared_prompt(filename, prompts_dir)
        raise ValueError(
            f"No shared instructions for role '{role_name}'. "
            f"Known roles: {list(SHARED_INSTRUCTIONS.keys())}. "
            f"Provide inline instructions instead."
        )
    return instructions_value


def _resolve_writing_standards(role: dict, prompts_dir: Path) -> str:
    """Resolve writing standards — either shared or inline."""
    ws_value = role.get("writing_standards", "")
    if ws_value == "shared":
        return _load_shared_prompt("writing-standards.md", prompts_dir)
    return ws_value


def _compute_other_triggers(config: dict, current_role_name: str) -> list[str]:
    """Compute the list of other role trigger keywords for negative filters."""
    triggers = []
    for role in config.get("roles", []):
        if role["name"] != current_role_name:
            triggers.append(f"@jules-{role['name']}")
    return triggers


def _persona_article(persona: str) -> str:
    """Return 'a' or 'an' depending on the persona."""
    first_word = persona.strip().split()[0].lower() if persona.strip() else ""
    return "an" if first_word[0:1] in "aeiou" else "a"


def _resolve_trigger_scope(role: dict) -> str:
    """Resolve and validate the comment trigger scope for a role."""
    scope = role.get("trigger_scope", "all_comments")
    if scope not in TRIGGER_SCOPE_CONDITIONS:
        raise ValueError(
            f"Invalid trigger_scope '{scope}'. "
            f"Expected one of: {list(TRIGGER_SCOPE_CONDITIONS.keys())}."
        )
    return scope


def _build_trigger_if(
    role_name: str,
    auth_roles: list[str],
    trigger_scope: str,
    other_triggers: list[str],
) -> str:
    """Build the GitHub Actions if-expression for a role trigger."""
    conditions = [f"contains(github.event.comment.body, '@jules-{role_name}')"]
    conditions.extend(
        f"!contains(github.event.comment.body, '{trigger}')" for trigger in other_triggers
    )
    scope_condition = TRIGGER_SCOPE_CONDITIONS[trigger_scope]
    if scope_condition:
        conditions.append(scope_condition)
    conditions.append(
        f"contains(fromJSON('{json.dumps(auth_roles)}'), github.event.comment.author_association)"
    )
    return " &&\n      ".join(conditions)


def _describe_trigger(role_name: str, trigger_scope: str, other_triggers: list[str]) -> str:
    """Return a human-readable description of the trigger behaviour."""
    description = f"Trigger on @jules-{role_name}"
    if other_triggers:
        description += f" (but NOT {' or '.join(other_triggers)})"
    description += " comments from authorised users"
    if trigger_scope == "issues_only":
        description += " on issues only"
    elif trigger_scope == "prs_only":
        description += " on PRs only"
    return description


def render_role(
    config: dict,
    role: dict,
    templates_dir: Path,
    prompts_dir: Path,
) -> str:
    """Render a single role's workflow from the universal template."""
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        keep_trailing_newline=True,
        lstrip_blocks=True,
        trim_blocks=True,
        variable_start_string="[=",
        variable_end_string="=]",
        block_start_string="[%",
        block_end_string="%]",
        comment_start_string="[#",
        comment_end_string="#]",
    )
    template = env.get_template("jules-dispatch.yml.j2")

    role_name = role["name"]

    # Merge defaults for known roles
    defaults = ROLE_DEFAULTS.get(role_name, {})
    merged = {**defaults, **role}

    # Resolve instructions and writing standards
    instructions = _resolve_instructions(role, prompts_dir)
    writing_standards = _resolve_writing_standards(role, prompts_dir)

    # Compute negative filter triggers
    other_triggers = []
    if merged.get("negative_filters"):
        other_triggers = _compute_other_triggers(config, role_name)

    auth_roles = config.get("auth_roles", ["OWNER", "MEMBER"])
    trigger_scope = _resolve_trigger_scope(merged)
    permissions = merged.get("permissions", config.get("permissions", DEFAULT_PERMISSIONS))

    context = {
        "role_name": role_name,
        "role_display_name": merged.get("role_display_name", role_name.upper()),
        "title_prefix": merged.get("title_prefix", role_name.upper()),
        "persona": merged.get("persona", role_name.title()),
        "persona_article": _persona_article(merged.get("persona", "")),
        "project_name": config.get("project_name", ""),
        "project_description": config.get("project_description", ""),
        "repo_structure": config.get("repo_structure", ""),
        "coding_standards": config.get("coding_standards", ""),
        "secret_name": role.get("secret_name", config.get("secret_name", "JULES_API_KEY")),
        "action_ref": role.get("action_ref", config.get("action_ref", "nq-rdl/jules-action@main")),
        "detect_pr_branch": merged.get("detect_pr_branch", False),
        "trigger_description": _describe_trigger(role_name, trigger_scope, other_triggers),
        "trigger_if": _build_trigger_if(role_name, auth_roles, trigger_scope, other_triggers),
        "permissions": permissions,
        "writing_standards": writing_standards,
        "security_scope": role.get("security_scope", ""),
        "docs_structure": role.get("docs_structure", ""),
        "instructions": instructions,
    }

    return template.render(**context)


def render_config(
    config: dict,
    templates_dir: Path | None = None,
    prompts_dir: Path | None = None,
) -> dict[str, str]:
    """Render all roles from a config into a dict of {filename: content}."""
    if templates_dir is None:
        templates_dir = TEMPLATES_DIR
    if prompts_dir is None:
        prompts_dir = PROMPTS_DIR

    results = {}
    for role in config.get("roles", []):
        role_name = role["name"]
        filename = f"jules-{role_name}-dispatch.yml"
        results[filename] = render_role(config, role, templates_dir, prompts_dir)

    return results


def validate_output(content: str, filename: str = "<unknown>") -> list[str]:
    """Check rendered output for leftover Jinja2 placeholders."""
    github_actions = re.compile(r"\$\{\{.*?\}\}")
    stripped = github_actions.sub("", content)
    jinja2_pattern = re.compile(r"\{\{.*?\}\}|\{%.*?%\}")
    matches = jinja2_pattern.findall(stripped)
    errors = []
    if matches:
        errors.append(f"{filename}: leftover Jinja2 placeholders: {matches}")
    try:
        yaml.safe_load(content)
    except yaml.YAMLError as e:
        errors.append(f"{filename}: invalid YAML: {e}")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Jules workflow template renderer")
    parser.add_argument("config", nargs="?", help="Path to config YAML file")
    parser.add_argument("--output-dir", "-o", help="Output directory (default: stdout)")
    parser.add_argument(
        "--validate", action="store_true", help="Validate a rendered workflow file"
    )
    args = parser.parse_args()

    if args.validate:
        if not args.config:
            parser.error("--validate requires a workflow file path")
        path = Path(args.config)
        content = path.read_text()
        errors = validate_output(content, path.name)
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            sys.exit(1)
        print(f"OK: {path.name}")
        sys.exit(0)

    if not args.config:
        parser.error("config file required")

    config = load_config(Path(args.config))
    results = render_config(config)

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in results.items():
            output_path = output_dir / filename
            output_path.write_text(content)
            print(f"Written: {output_path}")
    else:
        for filename, content in results.items():
            print(f"--- {filename} ---")
            print(content)


if __name__ == "__main__":
    main()
