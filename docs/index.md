---
icon: lucide/rocket
---

# Jules Workflow Templates

Central management hub for Jules AI agent dispatch workflows used across
the nq-rdl organisation.

## What This Is

Templates and tooling for generating GitHub Actions workflows that dispatch
Jules (Google's AI coding agent) via issue comments. Supports five built-in
agent roles and custom roles.

## Quick Start

=== "CLI"

    ```bash
    git clone https://github.com/nq-rdl/jules.git
    cd jules && pixi install
    pixi run generate .claude/skills/jules-action/examples/data-platform.yml --output-dir /path/to/repo/.github/workflows/
    ```

=== "Copier"

    ```bash
    pip install copier
    copier copy gh:nq-rdl/jules .github/workflows/
    ```

=== "Claude Code"

    ```
    /jules-actions
    ```

## How It Works

1. Write a config YAML describing your project and desired agent roles
2. Run the generator — it renders Jinja2 templates into GitHub Actions workflows
3. Copy the workflows to your repo's `.github/workflows/`
4. Add your Jules API key as a repository secret
5. Trigger agents by commenting `@jules-swe`, `@jules-infra`, `@jules-docs`,
   `@jules-security`, or `@jules-issue`
   on issues

## Built-in Roles

| Role | Trigger | Purpose |
|------|---------|---------|
| SWE | `@jules-swe` | Software engineering — implements code changes |
| Infra | `@jules-infra` | Platform engineering — infrastructure as code and automation |
| Docs | `@jules-docs` | Technical writing — documentation tasks |
| Security | `@jules-security` | Security review — vulnerability assessment |
| Issue | `@jules-issue` | Issue triage — assess scope, risk, and next action |

Custom roles generate `@jules-{name}` triggers.
See [Custom Roles](customisation/custom-roles.md) for details.
