"""Shared fixtures for jules-templates tests."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
PROMPTS_DIR = ROOT / "prompts"
EXAMPLES_DIR = ROOT / "skill" / "jules-action" / "examples"
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
