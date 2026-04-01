# Prompt Anatomy

Every Jules dispatch workflow embeds a system prompt that tells the AI agent
who it is, what the project looks like, and what to do. Understanding the
prompt structure helps you write effective custom prompts.

## Sections

A system prompt has these sections in order:

### 1. Persona

Defines who the agent is and what project it works on.

```
You are a Software Engineer working on the RDL Data Platform — an
Infrastructure as Code monorepo that provisions a data platform from
bare metal through to Kubernetes services.
```

### 2. Standards (optional)

For docs roles, includes writing standards (Australian English, tone rules).
For all roles, can include coding standards.

### 3. Architecture Context

Lists the repository's directory structure and what each directory contains.
This gives the agent a map of the codebase.

```
## Architecture context
- ansible/       — Hypervisor layer: RHEL VMs via libvirt
- terraform/     — Thin bootstrap module: Vault auth, ArgoCD
```

### 4. Security Scope (security only)

Lists specific security areas to assess with numbered items.

### 5. Issue Context (auto-injected)

These sections are populated automatically by the workflow from GitHub:

- Issue number, title, and labels
- Issue body (description)
- The triggering comment text

### 6. Instructions

Task-specific guidance for the agent. Three shared instruction sets are
available:

- **SWE** — Implement the solution, determine task type, follow standards
- **Docs** — Draft/Review/Cleanup, open a PR
- **Security** — Assess severity, implement fixes, document findings
- **Issue** — Triage scope, assess risk, and recommend the next action

## Shared Prompt Blocks

Reusable blocks live in `.claude/skills/jules-prompt/references/shared/`:

| File | Used By | Content |
|------|---------|---------|
| `writing-standards.md` | Docs | Australian English, corporate tone |
| `swe-instructions.md` | SWE | Implementation guidance |
| `docs-instructions.md` | Docs | Draft/Review/Cleanup types |
| `security-instructions.md` | Security | Severity assessment, remediation |
| `issue-instructions.md` | Issue | Structured issue triage and routing |

Set `instructions: "shared"` in your config to use these. Override with
inline `instructions:` for custom behaviour.
