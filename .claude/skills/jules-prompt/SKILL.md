---
name: jules-prompt
description: >
  Help users craft effective prompts for Jules AI agent workflows.
  Shows prompt patterns, trigger types, and reference examples for different
  Jules use cases (bug fixing, cleanup, performance, CI repair, security).
---

You are helping the user craft an effective prompt for a Jules AI agent workflow.

Jules is an asynchronous AI coding agent — prompts need to be self-contained and
detailed because there is no interactive back-and-forth once the agent starts.

## Reference Examples

This skill includes ready-to-use workflow examples at
`.claude/skills/jules-prompt/references/examples/`. Here is a summary:

| Example | Trigger | Pattern |
|---------|---------|---------|
| `bug-fixer.yml` | Issue labeled `bug` | Structured debugging (analyse → diagnose → fix → test) |
| `autonomous-bug-fixer.yml` | Issue labeled `bug` | Fully autonomous with `AUTO_CREATE_PR` + session tracking |
| `ci-failure-fix.yml` | CI workflow fails | Reactive repair on the failing branch |
| `performance-improver.yml` | Daily cron (4 AM UTC) | Persona-driven agent ("TURBO") with process pipeline |
| `weekly-cleanup.yml` | Weekly cron (Mon 2 AM) | Checklist-driven maintenance (dead code, duplication, naming) |
| `unblocked-issues.yml` | Issue closed | Dependency chain — works on newly unblocked issues |
| `session-cleanup-on-merge.yml` | PR merged | Housekeeping — deletes Jules session after merge |

Point the user to these examples as starting points. They can be copied directly
into `.github/workflows/` and customised.

## Step 1: Identify the Use Case

Ask the user what they want Jules to do. Common patterns:

1. **Reactive** — respond to an event (bug report, CI failure, security alert)
2. **Scheduled** — periodic maintenance (cleanup, performance, auditing)
3. **Chained** — triggered by another workflow completing (unblocked issues, post-merge)
4. **On-demand** — manual `workflow_dispatch` with optional inputs

## Step 2: Choose a Trigger Type

Based on the use case, recommend a trigger:

| Trigger | Event | Best For |
|---------|-------|----------|
| `issues: [labeled]` | Issue gets a label | Bug fixes, feature requests, triage |
| `issue_comment: [created]` | Comment on an issue | Interactive dispatch (`@jules-swe`) |
| `workflow_run: [completed]` | Another workflow finishes | CI failure repair |
| `schedule: cron` | Time-based | Cleanup, auditing, performance sweeps |
| `issues: [closed]` | Issue is closed | Dependency chains, follow-up work |
| `pull_request: [closed]` | PR merged or closed | Session cleanup, post-merge tasks |
| `workflow_dispatch` | Manual button | On-demand tasks, testing prompts |

## Step 3: Craft the Prompt

Guide the user through building an effective Jules prompt using these building blocks.
A good Jules prompt has **5 layers** (not all are needed for every use case):

### Layer 1: Persona (optional but powerful)

Give Jules a role identity. This anchors behaviour for the entire session.

```
You are TURBO, a performance optimization agent.
```

```
You are a Software Engineer working on the RDL Data Platform.
```

### Layer 2: Context

Provide the information Jules needs. For issue-triggered workflows, this comes
from GitHub event context variables:

```
## ${{ github.event.issue.title }}
${{ github.event.issue.body }}
```

For CI failures:
```
**Failed Run:** ${{ github.event.workflow_run.html_url }}
**Branch:** ${{ github.event.workflow_run.head_branch }}
```

### Layer 3: Instructions

Tell Jules exactly what to do. Two effective patterns:

**Numbered steps** (for structured processes):
```
1. Analyze the bug report and identify the root cause
2. Trace the issue through the codebase
3. Implement a minimal, targeted fix
4. Add a regression test
```

**Checklist with categories** (for broad sweeps):
```
## Focus Areas
1. **Dead Code** — unused variables, commented-out blocks
2. **Duplication** — repeated logic that should be extracted
3. **Complexity** — deeply nested conditionals, long functions
```

### Layer 4: Constraints (important for async agents)

Set boundaries so Jules doesn't go off-track:

```
- Keep changes under 100 lines
- Don't sacrifice readability for micro-gains
- Only create a PR if there's measurable impact
- Run tests before opening PR
```

### Layer 5: Output Format

Tell Jules how to present results, especially for PRs:

```
## PR Format
Title: "Fix: ${{ github.event.issue.title }}"
Include:
- Root cause explanation
- The fix with all necessary changes
- Test cases to prevent regression
```

## Step 4: Add Security

Remind the user about security patterns. Jules workflows should always restrict
who can trigger them:

**User allowlist** (for label/issue triggers):
```yaml
if: >
  contains(fromJSON('["user1", "user2"]'),
  github.event.issue.user.login)
```

**Author association** (for comment triggers — our dispatch template uses this):
```yaml
if: >
  contains(fromJSON('["OWNER", "MEMBER", "COLLABORATOR"]'),
  github.event.comment.author_association)
```

## Step 5: Choose Automation Level

Two modes for the `nq-rdl/jules-action`:

| Setting | Behaviour |
|---------|-----------|
| `require_plan_approval: true` (default) | Jules proposes a plan, waits for human approval |
| `require_plan_approval: false` | Jules executes immediately, no approval gate |

Add `automation_mode: AUTO_CREATE_PR` for fully autonomous PR creation.

## Integration with Templates

If the user is building an `issue_comment` dispatch workflow, suggest using the
`/jules-actions` skill instead — it generates complete workflows from the `.j2`
templates in this repo.

If the user wants issue triage, duplicate detection, scope assessment, or a
human-in-the-loop front door before implementation, recommend the built-in
`issue` role and an `@jules-issue` trigger before suggesting a custom prompt.

For other trigger types, the reference examples are the best starting point.
The examples can be adapted to use `nq-rdl/jules-action@main` instead of
`google-labs-code/jules-invoke@v1` for org-level features (session tracking,
autonomous mode, PR auto-creation).

## Important Notes

- Jules prompts must be **self-contained** — the agent cannot ask clarifying questions
- Include **repository context** (structure, standards) directly in the prompt for
  non-dispatch workflows (dispatch workflows get this from the template)
- Use **`starting_branch`** to control which branch Jules works from
- Use **`include_commit_log: true`** to give Jules recent git history context
- Scheduled workflows should include a **"don't create PR if no changes"** guard
