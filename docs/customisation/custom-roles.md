# Custom Roles

Beyond the four built-in roles (SWE, Docs, Security, Issue), you can define
custom agent roles for any specialisation.

## Defining a Custom Role

Add a role to your config's `roles` list with a unique name:

```yaml
roles:
  - name: test
    persona: "QA Engineer"
    title_prefix: "QA"
    role_display_name: "QA"
    instructions: |
      Write comprehensive tests for the issue above.
      Focus on edge cases, error handling, and integration tests.
      Follow the project's existing test patterns.
      Open a pull request with your changes when complete.
```

This generates `jules-test-dispatch.yml` triggered by `@jules-test` comments.

## Custom Role Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Role identifier — used as trigger (`@jules-{name}`) and filename |
| `persona` | Yes | Who the agent is (e.g., "QA Engineer", "Data Engineer") |
| `instructions` | Yes | What the agent should do (inline text or `"shared"`) |
| `title_prefix` | No | Prefix for PR titles (default: uppercase name) |
| `role_display_name` | No | Display name in workflow (default: uppercase name) |
| `negative_filters` | No | Add `!contains` guards for other roles (default: false) |
| `detect_pr_branch` | No | Detect PR branch for review (default: false) |
| `trigger_scope` | No | `all_comments`, `issues_only`, or `prs_only` |
| `permissions` | No | Per-role GitHub Actions job permissions |
| `action_ref` | No | Override action ref for this role |
| `secret_name` | No | Override secret name for this role |
| `writing_standards` | No | Include writing standards (`"shared"` or inline) |
| `security_scope` | No | Security areas to assess |
| `docs_structure` | No | Documentation structure |

## Examples

### Data Engineer

```yaml
- name: data
  persona: "Data Engineer"
  title_prefix: "Data"
  role_display_name: "Data Engineering"
  instructions: |
    Review and implement data pipeline changes for the issue above.
    Ensure data quality, idempotency, and proper error handling.
    Open a pull request with your changes when complete.
```

### DevOps / Platform Engineer

```yaml
- name: platform
  persona: "Platform Engineer"
  title_prefix: "Platform"
  role_display_name: "Platform"
  detect_pr_branch: true
  instructions: |
    Review and implement infrastructure changes for the issue above.
    Focus on reliability, observability, and cost efficiency.
    Open a pull request with your changes when complete.
```
