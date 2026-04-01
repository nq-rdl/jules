# Infra Template

The Infra template generates a workflow that dispatches Jules as a Platform
Engineer when triggered via `@jules-infra` comments.

## Trigger

```
@jules-infra <instructions>
```

## What It Does

The Infra agent:

1. Reads the issue context
2. Understands the repository's infrastructure layers and conventions
3. Implements infrastructure-as-code changes in Ansible, Terraform or OpenTofu,
   ArgoCD, CI, or adjacent docs as needed
4. Validates with repository-local checks only
5. Opens a pull request

## Validation Constraints

Infra workflows are designed for repositories where Jules cannot reach live
infrastructure.

- No direct libvirt, hypervisor, Kubernetes, or ArgoCD access
- No claims of end-to-end platform verification
- Prefer lint, syntax, validate, dry-run, and pre-commit style checks
- If core validation tooling is missing, add the minimal tooling in the PR

## Config Options

```yaml
roles:
  - name: infra
    persona: "Platform Engineer"
    title_prefix: "Infra"
    role_display_name: "Infra"
    instructions: "shared"
```
