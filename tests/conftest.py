"""Shared fixtures for jules-templates tests."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
PROMPTS_DIR = ROOT / ".claude" / "skills" / "jules-prompt" / "references"
EXAMPLES_DIR = ROOT / ".claude" / "skills" / "jules-action" / "examples"
SNAPSHOTS_DIR = Path(__file__).resolve().parent / "snapshots"


@pytest.fixture()
def templates_dir() -> Path:
    return TEMPLATES_DIR


@pytest.fixture()
def prompts_dir() -> Path:
    return PROMPTS_DIR


@pytest.fixture()
def examples_dir() -> Path:
    return EXAMPLES_DIR


@pytest.fixture()
def snapshots_dir() -> Path:
    return SNAPSHOTS_DIR


@pytest.fixture()
def minimal_config() -> dict:
    """A minimal valid config for a single SWE role."""
    return {
        "project_name": "Test Project",
        "project_description": "a test project",
        "secret_name": "JULES_API_KEY",
        "auth_roles": ["OWNER", "MEMBER"],
        "action_ref": "nq-rdl/jules-action@main",
        "repo_structure": "- src/    — Source code\n- tests/  — Tests\n",
        "coding_standards": "- Python: ruff for linting\n",
        "roles": [
            {
                "name": "swe",
                "persona": "Software Engineer",
                "negative_filters": False,
                "instructions": "shared",
            }
        ],
    }


@pytest.fixture()
def multi_role_config() -> dict:
    """Config with all three standard roles."""
    return {
        "project_name": "Multi Role Project",
        "project_description": "a project with all roles",
        "secret_name": "JULES_API_KEY",
        "auth_roles": ["OWNER", "MEMBER", "COLLABORATOR"],
        "action_ref": "nq-rdl/jules-action@main",
        "repo_structure": "- src/    — Source code\n",
        "coding_standards": "- Python: ruff\n",
        "roles": [
            {
                "name": "swe",
                "persona": "Software Engineer",
                "negative_filters": True,
                "instructions": "shared",
            },
            {
                "name": "docs",
                "persona": "Technical Writer",
                "writing_standards": "shared",
                "instructions": "shared",
            },
            {
                "name": "security",
                "persona": "Security Engineer",
                "detect_pr_branch": True,
                "security_scope": "1. Secrets\n2. Misconfigs\n",
                "instructions": "shared",
            },
        ],
    }


@pytest.fixture()
def custom_role_config() -> dict:
    """Config with a custom (non-standard) role."""
    return {
        "project_name": "Custom Role Project",
        "project_description": "a project with custom roles",
        "secret_name": "MY_JULES_KEY",
        "auth_roles": ["OWNER", "MEMBER"],
        "action_ref": "nq-rdl/jules-action@main",
        "repo_structure": "- src/    — Source code\n",
        "coding_standards": "- Python: ruff\n",
        "roles": [
            {
                "name": "test",
                "persona": "QA Engineer",
                "title_prefix": "QA",
                "role_display_name": "QA",
                "instructions": (
                    "Write comprehensive tests for the issue above.\n"
                    "Open a pull request with your changes when complete.\n"
                ),
            }
        ],
    }


@pytest.fixture()
def issue_role_config() -> dict:
    """Config for the built-in issue triage role."""
    return {
        "project_name": "Issue Role Project",
        "project_description": "a project using issue triage",
        "secret_name": "RJS_JULES_API",
        "auth_roles": ["OWNER", "MEMBER"],
        "action_ref": "nq-rdl/jules-action@main",
        "repo_structure": "- src/    — Source code\n- docs/   — Documentation\n",
        "coding_standards": "- Python: ruff\n",
        "roles": [{"name": "issue", "instructions": "shared"}],
    }


@pytest.fixture()
def scoped_role_config() -> dict:
    """Config for testing trigger scopes and custom permissions."""
    return {
        "project_name": "Scoped Role Project",
        "project_description": "a project with scoped custom roles",
        "secret_name": "MY_JULES_KEY",
        "auth_roles": ["OWNER", "MEMBER"],
        "action_ref": "nq-rdl/jules-action@main",
        "repo_structure": "- src/    — Source code\n",
        "coding_standards": "- Python: ruff\n",
        "roles": [
            {
                "name": "review",
                "persona": "Reviewer",
                "trigger_scope": "prs_only",
                "permissions": {
                    "contents": "read",
                    "pull-requests": "write",
                },
                "instructions": "Review the pull request above.\n",
            }
        ],
    }
