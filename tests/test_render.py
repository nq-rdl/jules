"""Tests for the Jinja2 template renderer."""

from __future__ import annotations

import yaml

from jules.render import render_config, render_role


class TestRenderSingleRole:
    """Test rendering a config with a single role."""

    def test_returns_dict_with_role_filename(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        assert "jules-swe-dispatch.yml" in results

    def test_output_is_valid_yaml(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        for filename, content in results.items():
            parsed = yaml.safe_load(content)
            assert parsed is not None, f"{filename} did not parse as valid YAML"

    def test_output_has_expected_top_level_keys(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        parsed = yaml.safe_load(results["jules-swe-dispatch.yml"])
        assert "name" in parsed
        # YAML parses bare `on:` as boolean True — GitHub Actions quirk
        assert True in parsed or "on" in parsed
        assert "jobs" in parsed

    def test_workflow_name_includes_role(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        parsed = yaml.safe_load(results["jules-swe-dispatch.yml"])
        assert "SWE" in parsed["name"]

    def test_trigger_is_issue_comment(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        parsed = yaml.safe_load(results["jules-swe-dispatch.yml"])
        # YAML parses bare `on:` as boolean True
        trigger = parsed.get("on") or parsed.get(True)
        assert trigger == {"issue_comment": {"types": ["created"]}}


class TestRenderMultipleRoles:
    """Test rendering a config with multiple roles."""

    def test_produces_file_per_role(self, multi_role_config, templates_dir, prompts_dir):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        assert len(results) == 3
        assert "jules-swe-dispatch.yml" in results
        assert "jules-docs-dispatch.yml" in results
        assert "jules-security-dispatch.yml" in results

    def test_each_output_is_valid_yaml(self, multi_role_config, templates_dir, prompts_dir):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        for filename, content in results.items():
            parsed = yaml.safe_load(content)
            assert parsed is not None, f"{filename} did not parse as valid YAML"


class TestCustomRole:
    """Test rendering a config with a custom (non-standard) role."""

    def test_custom_role_filename(self, custom_role_config, templates_dir, prompts_dir):
        results = render_config(custom_role_config, templates_dir, prompts_dir)
        assert "jules-test-dispatch.yml" in results

    def test_custom_role_trigger_keyword(self, custom_role_config, templates_dir, prompts_dir):
        results = render_config(custom_role_config, templates_dir, prompts_dir)
        content = results["jules-test-dispatch.yml"]
        assert "@jules-test" in content

    def test_custom_role_persona(self, custom_role_config, templates_dir, prompts_dir):
        results = render_config(custom_role_config, templates_dir, prompts_dir)
        content = results["jules-test-dispatch.yml"]
        assert "QA Engineer" in content

    def test_custom_role_instructions(self, custom_role_config, templates_dir, prompts_dir):
        results = render_config(custom_role_config, templates_dir, prompts_dir)
        content = results["jules-test-dispatch.yml"]
        assert "Write comprehensive tests" in content


class TestNegativeFilters:
    """Test that SWE negative filters work correctly (bug fix)."""

    def test_swe_has_negative_filters_for_other_roles(
        self, multi_role_config, templates_dir, prompts_dir
    ):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        content = results["jules-swe-dispatch.yml"]
        # Should have negative filters for docs and security
        assert "!contains(github.event.comment.body, '@jules-docs')" in content
        assert "!contains(github.event.comment.body, '@jules-security')" in content

    def test_swe_does_not_have_bare_jules_filter(
        self, multi_role_config, templates_dir, prompts_dir
    ):
        """Regression test for the bug where !contains('@jules') blocked @jules-swe."""
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        content = results["jules-swe-dispatch.yml"]
        # Must NOT have the bare @jules filter (this was the bug)
        assert "!contains(github.event.comment.body, '@jules')" not in content

    def test_docs_has_no_negative_filters(self, multi_role_config, templates_dir, prompts_dir):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        content = results["jules-docs-dispatch.yml"]
        assert "!contains" not in content


class TestSecureDelimiters:
    """Test that all outputs use secure random delimiters."""

    def test_uses_openssl_rand(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        content = results["jules-swe-dispatch.yml"]
        assert "openssl rand -hex 8" in content

    def test_does_not_use_issue_eof(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        content = results["jules-swe-dispatch.yml"]
        assert "ISSUE_EOF" not in content


class TestDetectPRBranch:
    """Test that security role includes branch detection step."""

    def test_security_has_branch_detection(self, multi_role_config, templates_dir, prompts_dir):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        content = results["jules-security-dispatch.yml"]
        assert "Detect PR branch" in content
        assert "starting_branch" in content

    def test_swe_has_no_branch_detection(self, multi_role_config, templates_dir, prompts_dir):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        content = results["jules-swe-dispatch.yml"]
        assert "Detect PR branch" not in content
        assert "starting_branch" not in content


class TestSharedInstructions:
    """Test that 'instructions: shared' loads from references/shared/."""

    def test_swe_shared_instructions(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        content = results["jules-swe-dispatch.yml"]
        assert "Implement the appropriate solution" in content

    def test_docs_shared_instructions(self, multi_role_config, templates_dir, prompts_dir):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        content = results["jules-docs-dispatch.yml"]
        assert "Determine the documentation task type" in content

    def test_infra_shared_instructions(self, infra_role_config, templates_dir, prompts_dir):
        results = render_config(infra_role_config, templates_dir, prompts_dir)
        content = results["jules-infra-dispatch.yml"]
        assert "Implement the appropriate infrastructure-as-code solution" in content
        assert "does not have direct access to libvirt" in content

    def test_security_shared_instructions(self, multi_role_config, templates_dir, prompts_dir):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        content = results["jules-security-dispatch.yml"]
        assert "Identify concrete vulnerabilities" in content

    def test_issue_shared_instructions(self, issue_role_config, templates_dir, prompts_dir):
        results = render_config(issue_role_config, templates_dir, prompts_dir)
        content = results["jules-issue-dispatch.yml"]
        assert "Perform issue triage only" in content
        assert "## Verdict" in content


class TestSharedWritingStandards:
    """Test that docs role includes writing standards."""

    def test_docs_has_writing_standards(self, multi_role_config, templates_dir, prompts_dir):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        content = results["jules-docs-dispatch.yml"]
        assert "Australian English" in content

    def test_swe_has_no_writing_standards(self, multi_role_config, templates_dir, prompts_dir):
        results = render_config(multi_role_config, templates_dir, prompts_dir)
        content = results["jules-swe-dispatch.yml"]
        assert "Australian English" not in content


class TestSecretName:
    """Test that the configured secret name is used."""

    def test_default_secret_name(self, minimal_config, templates_dir, prompts_dir):
        results = render_config(minimal_config, templates_dir, prompts_dir)
        content = results["jules-swe-dispatch.yml"]
        assert "secrets.JULES_API_KEY" in content

    def test_custom_secret_name(self, custom_role_config, templates_dir, prompts_dir):
        results = render_config(custom_role_config, templates_dir, prompts_dir)
        content = results["jules-test-dispatch.yml"]
        assert "secrets.MY_JULES_KEY" in content


class TestTriggerScopeAndPermissions:
    """Test trigger scope guards and per-role permissions."""

    def test_issue_role_is_limited_to_issues(self, issue_role_config, templates_dir, prompts_dir):
        results = render_config(issue_role_config, templates_dir, prompts_dir)
        content = results["jules-issue-dispatch.yml"]
        assert "github.event.issue.pull_request == null" in content
        assert "pull-requests:" not in content

    def test_prs_only_scope_is_supported(self, scoped_role_config, templates_dir, prompts_dir):
        results = render_config(scoped_role_config, templates_dir, prompts_dir)
        content = results["jules-review-dispatch.yml"]
        assert "github.event.issue.pull_request != null" in content

    def test_custom_permissions_are_rendered(self, scoped_role_config, templates_dir, prompts_dir):
        results = render_config(scoped_role_config, templates_dir, prompts_dir)
        content = results["jules-review-dispatch.yml"]
        assert "contents: read" in content
        assert "pull-requests: write" in content
        assert "issues:" not in content


class TestRenderRole:
    """Test the lower-level render_role function."""

    def test_render_role_returns_string(self, minimal_config, templates_dir, prompts_dir):
        role = minimal_config["roles"][0]
        result = render_role(minimal_config, role, templates_dir, prompts_dir)
        assert isinstance(result, str)
        assert len(result) > 0
