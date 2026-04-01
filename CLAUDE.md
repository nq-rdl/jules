# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

Central hub for Jules AI agent dispatch workflow templates. A per-project config YAML describes roles (SWE, Docs, Security, or custom); a Python renderer expands a single Jinja2 template into one GitHub Actions workflow per role. Generated workflows trigger when an authorised user comments `@jules-{role}` on an issue.

Also includes Claude Code skills (`/jules-actions`, `/jules-prompt`, `/jules-test`), a Copier template for non-Claude scaffolding, and a Zensical documentation site.

## Commands

```bash
pixi run generate <config.yml>                          # Render workflows to stdout
pixi run generate <config.yml> -o <dir>                 # Render to directory
pixi run validate <workflow.yml>                        # Check for leftover Jinja2 placeholders
pixi run test                                           # Run all tests
pixi run test -- -k "TestNegativeFilters"               # Run a single test class
pixi run test -- tests/test_render.py::TestSecretName   # Run a single test class by path
pixi run lint                                           # ruff check + yamllint
pixi run format                                         # ruff format
pixi run docs                                           # Serve docs locally (Zensical)
pixi run docs-build                                     # Build docs
```

### Updating snapshots

When templates or shared prompts change, snapshot tests may fail. Regenerate with:

```bash
pixi run generate .claude/skills/jules-action/examples/data-platform.yml -o tests/snapshots/data-platform/
pixi run generate .claude/skills/jules-action/examples/claude-code.yml -o tests/snapshots/claude-code/
```

## Key Conventions

- **pixi in pyproject format** — all pixi config lives in `pyproject.toml` (no separate `pixi.toml`)
- **Build backend**: hatchling
- **Linting**: ruff (line-length 99, Python 3.11+) for Python; yamllint (max 120, `--unsafe` for `${{ }}`) for YAML
- **Tests**: pytest with snapshot testing against `tests/snapshots/`
- **Changelog**: changie (fragments in `.changes/`)
- **Git hooks**: pre-commit (trailing-whitespace, end-of-file-fixer, check-yaml `--unsafe`, ruff, ruff-format, yamllint)
- **yamllint** excludes `.j2` templates and `.changes/` directory

## Architecture

### Render pipeline

`config YAML → src/jules/render.py → templates/jules-dispatch.yml.j2 → one .yml per role`

1. `load_config()` reads the project config YAML
2. For each role in `config["roles"]`, `render_role()` merges `ROLE_DEFAULTS` with the role dict, resolves `instructions: "shared"` and `writing_standards: "shared"` from `.claude/skills/jules-prompt/references/shared/`, and renders the template
3. `validate_output()` strips GitHub Actions `${{ }}` expressions then checks for leftover Jinja2 syntax

### Custom Jinja2 delimiters

Templates use non-standard delimiters to avoid collision with GitHub Actions expressions:

| Purpose     | Standard | This repo |
|-------------|----------|-----------|
| Variables   | `{{ }}`  | `[= =]`  |
| Blocks      | `{% %}`  | `[% %]`  |
| Comments    | `{# #}`  | `[# #]`  |

### Key files

- `templates/jules-dispatch.yml.j2` — the single universal template; all role-specific behaviour is controlled by Jinja2 conditionals
- `templates/includes/` — three include fragments: `fetch-context` (gh issue JSON), `detect-branch` (PR branch lookup), `react-confirm` (rocket reaction)
- `src/jules/render.py` — renderer, validator, and CLI entry point (`python -m jules.render`)
- `tests/conftest.py` — shared fixtures (`minimal_config`, `multi_role_config`, `custom_role_config`) and path constants
- `.claude/skills/jules-action/examples/` — example config YAMLs used by both snapshot tests and CI validation

### Role resolution

Three built-in roles (`swe`, `docs`, `security`) have defaults in `ROLE_DEFAULTS`. Custom roles (any other name) must supply all fields themselves. The `instructions: "shared"` sentinel loads role-specific markdown from `references/shared/{role}-instructions.md`.

## Writing Standards

Australian English (favour, colour, organisation, licence/license).
Corporate technical tone — direct, professional, no marketing language.
