# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## What This Repo Is

Central hub for Jules AI agent dispatch workflow templates. Contains:
- Jinja2 workflow templates for dispatching Jules via GitHub issue comments
- System prompt building blocks for SWE, Docs, and Security agent personas
- A Python renderer (`pixi run generate`) that renders config YAML into GitHub Actions workflows
- A Copier template for interactive scaffolding without Claude Code
- A Claude Code skill (`/jules-actions`) for interactive workflow generation
- Zensical documentation site

## Repository Layout

```
templates/              — Jinja2 workflow templates (.yml.j2) and includes
templates/includes/     — Shared Jinja2 template fragments (fetch context, reaction, branch detection)
prompts/                — Reference system prompts (markdown)
prompts/shared/         — Shared prompt blocks (writing standards, instruction footers)
src/jules/              — Python renderer and CLI
tests/                  — pytest tests with snapshot testing
tests/snapshots/        — Golden files for snapshot comparison
skill/jules-action/     — /jules-actions skill + example config YAML files
skill/jules-prompt/     — /jules-prompt skill + reference workflow examples
docs/                   — Zensical documentation site
.github/workflows/      — CI for this repo
```

## Key Conventions

- **pixi in pyproject format** — all pixi config lives in `pyproject.toml` (no separate `pixi.toml`)
- **Build backend**: hatchling
- **Linting**: ruff for Python, yamllint for YAML
- **Tests**: pytest with snapshot testing against `tests/snapshots/`
- **Changelog**: changie
- **Git hooks**: pre-commit (ruff, yamllint, pytest)
- **Docs**: Zensical (successor to Material for MkDocs)

## Commands

```bash
pixi run generate <config.yml>              # Render workflows from config
pixi run generate <config.yml> --output-dir # Render to specific directory
pixi run validate <workflow.yml>            # Check no Jinja2 placeholders remain
pixi run test                               # Run pytest
pixi run lint                               # ruff + yamllint
pixi run format                             # ruff format
```

## Architecture

- **Single universal template** (`templates/jules-dispatch.yml.j2`) drives all roles
- Role-specific behaviour via config variables + Jinja2 conditionals
- Per-project config YAML has a `roles` list; one config generates N workflows
- Shared prompt blocks loaded from `prompts/shared/` when config uses `instructions: "shared"`
- All templates use `openssl rand -hex 8` for secure output delimiters (not `ISSUE_EOF`)
- The `nq-rdl/jules-action` GitHub Action is invoked by all generated workflows

## Writing Standards

Australian English (favour, colour, organisation, licence/license).
Corporate technical tone — direct, professional, no marketing language.
