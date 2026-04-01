# Getting Started

## Prerequisites

- A GitHub repository in the `nq-rdl` organisation
- Access to `nq-rdl/jules-action` (the shared GitHub Action)
- A Jules API key stored as a repository secret

## Step 1: Create a Config

Create a YAML config file describing your project:

```yaml
project_name: "My Project"
project_description: "a Python web application"
secret_name: "JULES_API_KEY"
auth_roles: ["OWNER", "MEMBER", "COLLABORATOR"]
action_ref: "nq-rdl/jules-action@main"

repo_structure: |
  - src/           — Application source code
  - tests/         — Test suite
  - docs/          — Documentation

coding_standards: |
  - Python: ruff for linting, pytest for tests
  - Conventional commits

roles:
  - name: swe
    persona: "Software Engineer"
    negative_filters: true
    instructions: "shared"
```

See the [Config Reference](customisation/config-reference.md) for all available options.

Built-in roles include `swe`, `docs`, `security`, and `issue`.
Use `trigger_scope: issues_only` for issue-only triage workflows and `prs_only`
for PR-only review workflows.

## Step 2: Generate Workflows

```bash
pixi run generate my-config.yml --output-dir .github/workflows/
```

This produces one workflow per role (e.g., `jules-swe-dispatch.yml`).

## Step 3: Add the Secret

In your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add a new secret with the name matching your config (default: `JULES_API_KEY`)
3. Paste your Jules API key as the value

## Step 4: Trigger an Agent

Comment on any issue with the trigger keyword:

```
@jules-swe Please implement the feature described in this issue.
```

Jules will pick up the issue context and open a PR with the implementation.
A rocket reaction (🚀) confirms the dispatch.
