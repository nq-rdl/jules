# Jules Workflow Templates

Central management hub for Jules AI agent dispatch workflows used across
the nq-rdl organisation.

## What This Is

Templates and tooling for generating GitHub Actions workflows that dispatch
Jules (Google's AI coding agent) via issue comments. Supports five built-in
agent roles (SWE, Infra, Docs, Security, Issue Triage) and custom roles.

## Quick Start

### Option 1: Use the CLI

```bash
# Clone and install
git clone https://github.com/nq-rdl/jules.git
cd jules && pixi install

# Generate workflows from a config file
pixi run generate .claude/skills/jules-action/examples/data-platform.yml --output-dir /path/to/repo/.github/workflows/
```

### Option 2: Use Copier (no clone needed)

```bash
pip install copier
copier copy gh:nq-rdl/jules .github/workflows/
```

### Option 3: Use the Claude Code skill

```
/jules-actions
```

Skills live under `.claude/skills/`. For compatibility with other tooling,
`.agents/skills` is a symlink to the same directory.

## How It Works

1. Write a config YAML describing your project and desired agent roles
2. Run the generator — it renders Jinja2 templates into GitHub Actions workflows
3. Copy the workflows to your repo's `.github/workflows/`
4. Add your Jules API key as a repository secret
5. Trigger agents by commenting `@jules-swe`, `@jules-infra`, `@jules-docs`,
   `@jules-security`, or `@jules-issue`
   on issues

## Config Example

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

  - name: docs
    persona: "Technical Writer"
    writing_standards: "shared"
    instructions: "shared"

  - name: security
    persona: "Security Engineer"
    detect_pr_branch: true
    security_scope: |
      1. Secrets and credentials
      2. Dependency vulnerabilities
    instructions: "shared"
```

## Templates

| Template | Trigger | Purpose |
|----------|---------|---------|
| `jules-swe-dispatch.yml` | `@jules-swe` | Software engineering tasks |
| `jules-infra-dispatch.yml` | `@jules-infra` | Platform and infrastructure as code tasks |
| `jules-docs-dispatch.yml` | `@jules-docs` | Documentation tasks |
| `jules-security-dispatch.yml` | `@jules-security` | Security review |
| `jules-issue-dispatch.yml` | `@jules-issue` | Issue triage and routing |

Custom roles generate `jules-{name}-dispatch.yml` with `@jules-{name}` triggers.

## Development

```bash
pixi install           # Install dependencies
pixi run test          # Run tests
pixi run lint          # Lint Python + YAML
pixi run format        # Format Python code
```

## Licence

Apache 2.0
