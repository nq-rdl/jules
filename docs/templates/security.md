# Security Template

The Security template generates a workflow that dispatches Jules as a
Security Engineer when triggered via `@jules-security` comments.

## Trigger

```
@jules-security <instructions>
```

## What It Does

The Security agent:

1. Reads the issue context
2. Detects if the comment is on a PR (starts review from the PR branch)
3. Assesses the security scope defined in your config
4. Identifies vulnerabilities with severity ratings (Critical/High/Medium/Low)
5. Implements fixes where safe to automate
6. Documents findings with remediation guidance

## PR Branch Detection

Security workflows include a "Detect PR branch" step. When `@jules-security`
is used on a pull request comment, Jules starts from the PR's head branch
instead of `main`.

## Action Pinning

Security workflows should pin the action to a commit hash instead of `@main`.
This prevents supply-chain attacks where a compromised `@main` tag could
inject malicious code into security reviews.

## Config Options

```yaml
roles:
  - name: security
    persona: "Security Engineer"
    detect_pr_branch: true
    action_ref: "nq-rdl/jules-action@<commit-hash>"   # Pin to specific commit
    security_scope: |
      1. Secrets and credentials — hardcoded secrets, plaintext passwords
      2. Misconfigurations — insecure defaults, public exposure
      3. Dependencies — pinned vs floating versions, known CVEs
      4. Access control — overly broad permissions
    instructions: "shared"
```
