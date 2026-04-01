"""Tests for template validation — no Jinja2 placeholders in output."""

from __future__ import annotations

import re

import yaml

from jules.render import render_config

JINJA2_PATTERN = re.compile(r"\{\{.*?\}\}|\{%.*?%\}")
# GitHub Actions expressions are allowed — only flag Jinja2 syntax
GITHUB_ACTIONS_PATTERN = re.compile(r"\$\{\{.*?\}\}")


def _strip_github_expressions(content: str) -> str:
    """Remove GitHub Actions ${{ }} expressions so we only check for Jinja2 leftovers."""
    return GITHUB_ACTIONS_PATTERN.sub("", content)


class TestNoJinjaPlaceholders:
    """Rendered output must not contain leftover Jinja2 placeholders."""

    def test_minimal_config_no_placeholders(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        for filename, content in results.items():
            stripped = _strip_github_expressions(content)
            matches = JINJA2_PATTERN.findall(stripped)
            assert not matches, f"{filename} has leftover Jinja2: {matches}"

    def test_multi_role_config_no_placeholders(
        self, multi_role_config, templates_dir, prompts_dir
    ):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        for filename, content in results.items():
            stripped = _strip_github_expressions(content)
            matches = JINJA2_PATTERN.findall(stripped)
            assert not matches, f"{filename} has leftover Jinja2: {matches}"

    def test_custom_role_config_no_placeholders(
        self, custom_role_config, templates_dir, prompts_dir
    ):
        results = render_config(custom_role_config, templates_dir, prompts_dir)
        for filename, content in results.items():
            stripped = _strip_github_expressions(content)
            matches = JINJA2_PATTERN.findall(stripped)
            assert not matches, f"{filename} has leftover Jinja2: {matches}"


class TestValidGitHubActionsYAML:
    """Rendered output must be valid YAML with expected GitHub Actions structure."""

    def test_has_required_keys(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        for filename, content in results.items():
            parsed = yaml.safe_load(content)
            assert "name" in parsed, f"{filename} missing 'name'"
            assert "on" in parsed or True in parsed, f"{filename} missing 'on'"
            assert "jobs" in parsed, f"{filename} missing 'jobs'"

    def test_job_has_runs_on(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        for filename, content in results.items():
            parsed = yaml.safe_load(content)
            for job_name, job in parsed["jobs"].items():
                assert "runs-on" in job, f"{filename}/{job_name} missing 'runs-on'"

    def test_job_has_steps(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        for filename, content in results.items():
            parsed = yaml.safe_load(content)
            for job_name, job in parsed["jobs"].items():
                assert "steps" in job, f"{filename}/{job_name} missing 'steps'"
                assert len(job["steps"]) >= 2, f"{filename}/{job_name} has too few steps"
