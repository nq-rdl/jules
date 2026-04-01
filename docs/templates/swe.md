# SWE Template

The SWE (Software Engineering) template generates a workflow that dispatches
Jules as a Software Engineer when triggered via `@jules-swe` comments.

## Trigger

```
@jules-swe <instructions>
```

## What It Does

The SWE agent:

1. Reads the issue context (title, body, labels)
2. Understands the repository structure and coding standards
3. Determines the task type (bug fix, feature, config change, docs)
4. Implements the solution
5. Opens a pull request

## Negative Filters

The SWE workflow includes `!contains` guards for other role triggers to prevent
double-triggering. If you comment `@jules-docs fix the README`, only the Docs
workflow fires — the SWE workflow explicitly excludes itself.

**Important:** The negative filters only exclude other defined role triggers
(e.g., `@jules-docs`, `@jules-security`). They do NOT include a bare `@jules`
filter — this was a bug in earlier versions that prevented `@jules-swe` from
ever triggering.

## Config Options

```yaml
roles:
  - name: swe
    persona: "Software Engineer"        # Customise the persona
    negative_filters: true              # Add !contains for other roles
    instructions: "shared"              # Use shared SWE instructions
    # instructions: |                   # Or provide custom instructions
    #   Implement the solution...
```
