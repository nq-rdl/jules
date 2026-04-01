---
name: jules-actions
description: >
  Generate customised Jules GitHub Actions dispatch workflows for a repository.
  Use when setting up Jules SWE, Infra, Docs, Security, or Issue Triage agent
  workflows in a new or existing repo. Supports custom agent roles beyond the
  standard ones.
---

You are helping the user set up Jules AI agent dispatch workflows for their repository.

## What You Do

Generate GitHub Actions workflow files that allow dispatching Jules via issue comments
(e.g., `@jules-swe`, `@jules-infra`, `@jules-docs`, `@jules-security`, or
custom triggers).

## Step 1: Detect Context

Read the `CLAUDE.md` file in the user's current working directory (if it exists) to
auto-detect:
- Project name and description
- Repository structure (directories and their purposes)
- Tech stack and coding standards
- Documentation system

If no `CLAUDE.md` exists, ask the user for this information directly.

## Step 2: Gather Configuration

Ask the user to confirm or provide the following. Pre-fill from `CLAUDE.md` if available:

1. **Project name** — e.g., "RDL Data Platform"
2. **Project description** — one-line summary
3. **Repository structure** — list of key directories and their purposes
4. **Coding standards** — project-specific rules (language, linting, conventions)
5. **Secret name** — GitHub secret for Jules API key (default: `JULES_API_KEY`)
6. **Auth level** — who can trigger: `["OWNER", "MEMBER", "COLLABORATOR"]` or `["OWNER", "MEMBER"]`
7. **Which agent roles** to generate:
   - **SWE** (Software Engineer) - implements code changes
   - **Infra** (Platform Engineer) - infrastructure as code, automation, and repo-local validation
   - **Docs** (Technical Writer) - documentation tasks
   - **Security** (Security Engineer) - security review
   - **Issue** (Engineering Triage Lead) - assesses issue scope, risk, and routing
   - **Custom** - user defines the role name, persona, and instructions

If the user asks for Terraform, OpenTofu, Ansible, ArgoCD, hypervisor, or
platform automation work, recommend the built-in **Infra** role before suggesting
a custom role.

If the user mentions issue triage, backlog review, duplicate detection, scope
assessment, or "review this issue first", recommend the built-in **Issue** role
before suggesting a custom role.

For each role, ask whether it should trigger on:
- all issue comments (`all_comments`)
- issues only (`issues_only`)
- PR comments only (`prs_only`)

Also ask whether the role needs custom GitHub Actions job permissions. If not,
use the template defaults. Issue triage roles usually only need:

```yaml
permissions:
  contents: read
  issues: write
```

For each custom role, ask:
- Role name (used as `@jules-{name}` trigger)
- Persona (e.g., "QA Engineer", "Data Engineer")
- Custom instructions (what the agent should do)

## Step 3: Generate Config YAML

Create a config YAML file at `.jules-config.yml` in the user's repo with their answers.
The config follows this structure:

```yaml
project_name: "<name>"
project_description: "<description>"
secret_name: "<secret>"
auth_roles: ["OWNER", "MEMBER", "COLLABORATOR"]
action_ref: "nq-rdl/jules-action@main"

repo_structure: |
  <directory listing>

coding_standards: |
  <standards>

roles:
  - name: swe
    persona: "Software Engineer"
    negative_filters: true
    instructions: "shared"
  - name: infra
    instructions: "shared"
  # ... more roles
```

For docs roles, add `writing_standards: "shared"` to include the standard Australian English
corporate technical writing block.

For infra roles, use `name: infra`, `persona: "Platform Engineer"`, and
`instructions: "shared"`. Make sure the repo-level coding standards spell out
the available validation commands and any constraints such as no direct access
to live clusters or hypervisors.

For security roles, add `detect_pr_branch: true` and a `security_scope` field listing
the specific security areas to review.

For issue roles, use `instructions: "shared"`, `trigger_scope: issues_only`, and minimal
permissions unless the user explicitly wants broader access. This should be the
default recommendation for workflows like `@jules-issue please review and triage`.

## Step 4: Generate Workflow Files

Check if the `jules-templates` package is available (`pixi run generate --help`).

**If available:** Run `pixi run generate .jules-config.yml --output-dir .github/workflows/`

**If not available:** Generate the workflow files directly by rendering the template
pattern yourself. Each workflow follows this structure:

- Trigger: `on: issue_comment: types: [created]`
- Job filter: `if: contains(body, '@jules-{role}') && auth_association check`
- Optional scope guard: `github.event.issue.pull_request == null` for issues only or
  `github.event.issue.pull_request != null` for PR comments only
- Steps: Fetch issue context → Invoke Jules → React with rocket emoji
- The system prompt is embedded inline in the `prompt:` field

Write each workflow to `.github/workflows/jules-{role_name}-dispatch.yml`.

## Step 5: Remind About Secrets

After generating, remind the user:
- Add the Jules API key as a GitHub repository secret (Settings → Secrets → Actions)
- The secret name must match what's in the workflow (default: `JULES_API_KEY`)
- Workflows must be on the default branch to trigger from issue comments

## Important Notes

- The SWE workflow should include negative filters (`!contains`) for ALL other role
  triggers to prevent double-triggering. Do NOT include `!contains('@jules')` — this
  is a known bug that blocks `@jules-swe` since it's a substring match.
- `issue_comment` fires for both issues and PRs. Use `trigger_scope: issues_only` for
  issue triage and `prs_only` for PR-only review workflows.
- When the user wants a human-in-the-loop front door for implementation, prefer the
  built-in `issue` role first, then hand off to `@jules-swe`, `@jules-infra`,
  `@jules-docs`, or `@jules-security` after triage.
- Keep permissions least-privilege. Do not grant `pull-requests` access unless the role
  actually needs it.
- Security workflows should pin the action to a commit hash, not `@main`.
- All workflows use `openssl rand -hex 8` for secure output delimiters (not `ISSUE_EOF`).
- Writing standards block (for docs) uses Australian English and corporate technical tone.
