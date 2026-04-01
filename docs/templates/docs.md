# Docs Template

The Docs (Technical Writer) template generates a workflow that dispatches
Jules as a Technical Writer when triggered via `@jules-docs` comments.

## Trigger

```
@jules-docs <instructions>
```

## What It Does

The Docs agent determines the task type and acts accordingly:

- **Draft** — Write new documentation from code analysis
- **Review** — Audit existing docs for accuracy against current code
- **Cleanup** — Fix spelling, tone, structure, and formatting

## Writing Standards

When `writing_standards: "shared"` is set, the agent follows a standard block:

- Australian English (favour, colour, organisation, licence/license)
- Corporate technical tone — direct, professional, no marketing
- No flowery language, no filler, no adverbs like "simply", "easily", "just"
- No exclamation marks, no emoji, no rhetorical questions
- Code blocks must specify language
- File paths and commands in backticks

## Config Options

```yaml
roles:
  - name: docs
    persona: "Technical Writer"
    writing_standards: "shared"        # Include standard writing rules
    docs_structure: |                  # Describe your docs layout
      - docs/architecture/   — System design
      - docs/operations/     — Runbooks
    instructions: "shared"             # Use shared Docs instructions
```
