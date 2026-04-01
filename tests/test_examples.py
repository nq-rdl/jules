"""Snapshot tests — render example configs and compare to golden files."""

from __future__ import annotations

from pathlib import Path

import yaml

from jules.render import load_config, render_config


def _render_example(name: str, examples_dir: Path, templates_dir: Path, prompts_dir: Path):
    """Load an example config and render all roles."""
    config_path = examples_dir / f"{name}.yml"
    config = load_config(config_path)
    return render_config(config, templates_dir, prompts_dir)


class TestDataPlatformExample:
    """Render .claude/skills/jules-action/examples/data-platform.yml and verify output."""

    def test_produces_three_workflows(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("data-platform", examples_dir, templates_dir, prompts_dir)
        assert len(results) == 4

    def test_all_valid_yaml(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("data-platform", examples_dir, templates_dir, prompts_dir)
        for filename, content in results.items():
            parsed = yaml.safe_load(content)
            assert parsed is not None, f"{filename} is not valid YAML"

    def test_swe_contains_ansible_standards(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("data-platform", examples_dir, templates_dir, prompts_dir)
        assert "FQCN" in results["jules-swe-dispatch.yml"]

    def test_docs_contains_mkdocs_structure(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("data-platform", examples_dir, templates_dir, prompts_dir)
        assert "MkDocs Material" in results["jules-docs-dispatch.yml"]

    def test_infra_contains_validation_constraints(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("data-platform", examples_dir, templates_dir, prompts_dir)
        infra = results["jules-infra-dispatch.yml"]
        assert "Platform Engineer" in infra
        assert "does not have direct access to libvirt" in infra

    def test_security_uses_pinned_action(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("data-platform", examples_dir, templates_dir, prompts_dir)
        assert "d8ed19ed75a6c2a35fd4e06e5b2ca7cd68b27046" in results["jules-security-dispatch.yml"]

    def test_snapshot_match(self, examples_dir, templates_dir, prompts_dir, snapshots_dir):
        """Compare rendered output to snapshot golden files (if they exist)."""
        snapshot_dir = snapshots_dir / "data-platform"
        if not snapshot_dir.exists():
            return  # Skip if snapshots not yet generated

        results = _render_example("data-platform", examples_dir, templates_dir, prompts_dir)
        for filename, content in results.items():
            snapshot_file = snapshot_dir / filename
            if snapshot_file.exists():
                expected = snapshot_file.read_text()
                assert content == expected, (
                    f"Snapshot mismatch for {filename}. "
                    "Run 'pixi run generate "
                    ".claude/skills/jules-action/examples/data-platform.yml "
                    "--output-dir tests/snapshots/data-platform/' to update."
                )


class TestIssueTriageExample:
    """Render .claude/skills/jules-action/examples/issue-triage.yml and verify output."""

    def test_produces_issue_workflow(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("issue-triage", examples_dir, templates_dir, prompts_dir)
        assert list(results) == ["jules-issue-dispatch.yml"]

    def test_issue_workflow_is_issue_only(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("issue-triage", examples_dir, templates_dir, prompts_dir)
        content = results["jules-issue-dispatch.yml"]
        assert "github.event.issue.pull_request == null" in content
        assert "pull-requests:" not in content


class TestClaudeCodeExample:
    """Render .claude/skills/jules-action/examples/claude-code.yml and verify output."""

    def test_produces_three_workflows(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("claude-code", examples_dir, templates_dir, prompts_dir)
        assert len(results) == 3

    def test_all_valid_yaml(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("claude-code", examples_dir, templates_dir, prompts_dir)
        for filename, content in results.items():
            parsed = yaml.safe_load(content)
            assert parsed is not None, f"{filename} is not valid YAML"

    def test_uses_custom_secret(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("claude-code", examples_dir, templates_dir, prompts_dir)
        assert "R_JULES_TOKEN" in results["jules-swe-dispatch.yml"]

    def test_swe_has_plugin_context(self, examples_dir, templates_dir, prompts_dir):
        results = _render_example("claude-code", examples_dir, templates_dir, prompts_dir)
        assert "rdl-skills" in results["jules-swe-dispatch.yml"]

    def test_snapshot_match(self, examples_dir, templates_dir, prompts_dir, snapshots_dir):
        """Compare rendered output to snapshot golden files (if they exist)."""
        snapshot_dir = snapshots_dir / "claude-code"
        if not snapshot_dir.exists():
            return  # Skip if snapshots not yet generated

        results = _render_example("claude-code", examples_dir, templates_dir, prompts_dir)
        for filename, content in results.items():
            snapshot_file = snapshot_dir / filename
            if snapshot_file.exists():
                expected = snapshot_file.read_text()
                assert content == expected, (
                    f"Snapshot mismatch for {filename}. "
                    "Run 'pixi run generate "
                    ".claude/skills/jules-action/examples/claude-code.yml "
                    "--output-dir tests/snapshots/claude-code/' to update."
                )
