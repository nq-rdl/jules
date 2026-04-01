# Config Reference

A config YAML file drives the template renderer. One config generates all
workflow files for a project.

## Top-Level Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `project_name` | string | Yes | — | Project display name |
| `project_description` | string | No | — | One-line description |
| `secret_name` | string | No | `JULES_API_KEY` | GitHub secret name |
| `auth_roles` | list | No | `["OWNER", "MEMBER", "COLLABORATOR"]` | Allowed author associations |
| `action_ref` | string | No | `nq-rdl/jules-action@main` | GitHub Action reference |
| `repo_structure` | string | Yes | — | Directory listing (multiline) |
| `coding_standards` | string | No | — | Project coding rules (multiline) |
| `roles` | list | Yes | — | List of agent role definitions |

## Role Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | Yes | — | Role identifier (`@jules-{name}` trigger) |
| `persona` | string | Yes | — | Agent persona description |
| `instructions` | string | Yes | — | Task instructions (`"shared"` or inline) |
| `title_prefix` | string | No | `NAME` | PR title prefix |
| `role_display_name` | string | No | `NAME` | Display name in workflow |
| `negative_filters` | bool | No | `false` | Add `!contains` guards |
| `detect_pr_branch` | bool | No | `false` | Detect PR branch |
| `action_ref` | string | No | top-level | Override action reference |
| `secret_name` | string | No | top-level | Override secret name |
| `writing_standards` | string | No | — | `"shared"` or inline |
| `security_scope` | string | No | — | Security areas to assess |
| `docs_structure` | string | No | — | Documentation layout |

## Full Example

```yaml
project_name: "RDL Data Platform"
project_description: "an IaC monorepo from bare metal to Kubernetes"
secret_name: "JULES_API_KEY"
auth_roles: ["OWNER", "MEMBER", "COLLABORATOR"]
action_ref: "nq-rdl/jules-action@main"

repo_structure: |
  - ansible/       — Hypervisor layer: RHEL VMs via libvirt
  - terraform/     — Bootstrap module: Vault auth, ArgoCD
  - argocd/        — App-of-apps: platform services
  - src/da/        — Python package

coding_standards: |
  - Ansible: FQCN always, lean roles
  - Terraform: single thin bootstrap module
  - Python: managed via pixi, hatchling

roles:
  - name: swe
    persona: "Software Engineer"
    negative_filters: true
    instructions: "shared"

  - name: docs
    persona: "Technical Writer"
    writing_standards: "shared"
    docs_structure: |
      - docs/architecture/   — System design
      - docs/hypervisor/     — Bare metal setup
      - docs/kubernetes/     — K8s deployment
      - docs/operations/     — Runbooks
    instructions: "shared"

  - name: security
    persona: "Security Engineer"
    detect_pr_branch: true
    action_ref: "nq-rdl/jules-action@<commit-hash>"
    security_scope: |
      1. Secrets and credentials
      2. IaC misconfigurations
      3. Kubernetes security
      4. Supply chain
    instructions: "shared"
```
