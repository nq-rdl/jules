---
name: jules-test
description: >
  Test, debug, and monitor Jules GitHub Actions dispatch workflows using the gh
  CLI. This skill should be used when triggering a Jules workflow, checking if a
  workflow fired, reading action run logs, diagnosing why a workflow did not
  trigger, watching a run in progress, verifying a dispatch reaction, inspecting
  gh run output, re-running failed jobs, or troubleshooting any Jules GitHub
  Action issue. Matches queries like "test the action", "run the workflow",
  "check the workflow", "why didn't it trigger", "workflow not working", "debug
  the action", "gh run", "re-run the job", or "action logs".
---

You are helping the user test and debug Jules GitHub Actions dispatch workflows
using the `gh` CLI. This skill covers the full lifecycle: trigger → monitor →
diagnose → verify.

For a command quick-reference table and common testing patterns, read
`skill/jules-test/references/quick-reference.md`.

## Before You Start

Resolve the repo context once so you can substitute into all subsequent commands:

```bash
gh repo view --json nameWithOwner,defaultBranchRef \
  --jq '{repo: .nameWithOwner, default_branch: .defaultBranchRef.name}'
```

Confirm `gh` is authenticated and has the required scopes:

```bash
gh auth status
```

Look for `Token scopes:` in the output. The token needs `repo` and `workflow`
scopes. If `workflow` is missing, the user needs to re-authenticate:

```bash
gh auth refresh -s workflow
```

The user also needs push access (for creating comments / triggering workflows),
and the Jules workflow must already be merged to the **default branch**. This
last point is critical for `issue_comment` triggers — GitHub's security model
prevents workflows defined on feature branches from running on comment events,
because that would let PR authors inject arbitrary workflow code. This is the
single most common cause of "nothing happened."

## Step 1: Identify What to Test

If the user hasn't specified, auto-detect from the current repo:

```bash
gh workflow list
```

This lists all workflows GitHub recognises on the default branch. If the
expected Jules workflow does not appear here, it either has a YAML syntax error
(GitHub silently ignores malformed workflow files) or is not yet on the default
branch.

Determine:
1. **Workflow file name** — e.g., `jules-swe-dispatch.yml`
2. **Trigger type** — `issue_comment`, `workflow_dispatch`, `schedule`, etc.

## Step 2: Trigger the Workflow

### For `issue_comment` dispatch workflows (most Jules workflows)

These trigger when a comment containing `@jules-<role>` is posted on an issue.

**Find or create a test issue:**

```bash
# List open issues
gh issue list --limit 10

# Create a dedicated test issue
gh issue create --title "Test: Jules dispatch" \
  --body "Testing Jules workflow triggers."
```

**Trigger the workflow by commenting:**

```bash
gh issue comment <ISSUE_NUMBER> \
  --body "@jules-swe please analyse this test issue"
```

Replace `@jules-swe` with the appropriate trigger tag (`@jules-docs`,
`@jules-security`, or custom role names). The tag must exactly match the
`contains()` check in the workflow's `if` condition.

**Important:** The comment author must match the `author_association` filter in
the workflow's `if` condition. GitHub assigns association based on the user's
relationship to the repo (owner, org member, outside collaborator, etc.) — not
their role on the specific issue. Check yours:

```bash
gh api "repos/<owner>/<repo>/collaborators/<username>/permission" \
  --jq '.permission'
```

### For `workflow_dispatch` workflows

```bash
# List inputs (if any)
gh workflow view <workflow-file> --yaml | head -30

# Trigger with no inputs
gh workflow run <workflow-file>

# Trigger with inputs
gh workflow run <workflow-file> -f input_name=value
```

### For `schedule` (cron) workflows

Cron workflows cannot be manually triggered unless the workflow also includes a
`workflow_dispatch` trigger. If it does, use `gh workflow run`. Otherwise, the
only option is to wait for the schedule or temporarily add `workflow_dispatch`.

### For `issues` (labeled) workflows

```bash
gh issue edit <ISSUE_NUMBER> --add-label "bug"
```

### For `workflow_run` (chained) workflows

Trigger the upstream workflow first, then monitor downstream:

```bash
gh workflow run <upstream-workflow>
# Wait, then check downstream
gh run list --workflow=<downstream-workflow> --limit 5
```

## Step 3: Monitor the Run

After triggering, watch for the run to appear:

```bash
gh run list --workflow=<workflow-file> --limit 5
```

If a run appears, watch it in real-time:

```bash
gh run watch <RUN_ID>
```

Or view its current status:

```bash
gh run view <RUN_ID>
```

To cancel a run that was triggered by mistake or is taking too long:

```bash
gh run cancel <RUN_ID>
```

**If no run appears within 60 seconds**, the workflow likely did not trigger.
GitHub Actions can take a minute or more to queue, especially on shared runners.
If nothing shows after that, jump to **Step 5: Diagnose "No Run" Problems**.

## Step 4: Read Logs

### Quick log inspection

```bash
# Only failed step logs — almost always what you want first
gh run view <RUN_ID> --log-failed

# Full logs for a run
gh run view <RUN_ID> --log
```

### Job-level inspection

```bash
# List jobs within a run
gh run view <RUN_ID> --json jobs \
  --jq '.jobs[] | {name, status, conclusion}'

# View a specific job's logs
gh run view <RUN_ID> --log --job=<JOB_ID>
```

### Download log archives

For very large logs or offline analysis:

```bash
gh api "repos/<owner>/<repo>/actions/runs/<RUN_ID>/logs" \
  -H "Accept: application/zip" > logs.zip
```

### Inspect step outputs

Check what the "Fetch issue context" step captured (useful for verifying the
prompt that was assembled and sent to Jules):

```bash
gh run view <RUN_ID> --log | grep -A 20 "Fetch issue context"
```

## Step 5: Diagnose "No Run" Problems

When `gh run list` shows nothing after triggering, work through this checklist
in order — the items are ranked by how frequently they cause the problem.

### 5a. Workflow not on default branch

`issue_comment` workflows only run from the default branch. This restriction
exists because GitHub treats comment-triggered workflows as potentially
attacker-controlled (the comment body is user input), so it only trusts the
workflow definition from the protected default branch.

```bash
# Check default branch
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'

# Check if workflow exists on that branch
gh api "repos/<owner>/<repo>/contents/.github/workflows/<workflow-file>" \
  --jq '.name'
```

### 5b. `if` condition not met

The workflow's `if` expression may have silently evaluated to false. Common
causes:

- **Wrong trigger tag** — comment said `@jules` but workflow expects `@jules-swe`
- **Author association mismatch** — user is not `OWNER`/`MEMBER`/`COLLABORATOR`
- **Negative filter matched** — e.g., commenting `@jules-swe @jules-docs` in
  one comment causes the SWE workflow's `!contains(body, '@jules-docs')` filter
  to block the run. Each role trigger must be in a separate comment.

Inspect the exact `if` condition from the workflow on the default branch:

```bash
gh api "repos/<owner>/<repo>/contents/.github/workflows/<workflow-file>" \
  --jq '.content' | base64 -d | grep -A 5 'if:'
```

Check the comment that was posted:

```bash
gh api "repos/<owner>/<repo>/issues/<ISSUE_NUMBER>/comments" \
  --jq '.[-1] | {id, author_association, body}'
```

### 5c. Workflow disabled

GitHub auto-disables workflows after 60 days of repo inactivity.

```bash
gh workflow list --all | grep <workflow-name>
```

If the state shows `disabled_manually` or `disabled_inactivity`:

```bash
gh workflow enable <workflow-file>
```

### 5d. Secrets missing

The workflow may have started but failed immediately due to a missing secret.
GitHub does not expose secret values, but you can check which names exist:

```bash
gh secret list
```

Verify the expected secret name matches what the workflow references (e.g.,
`JULES_API_KEY` or `R_JULES_TOKEN`).

### 5e. YAML syntax errors

Workflows with YAML syntax errors are silently ignored — they do not appear in
`gh workflow list` at all. Fetch the raw file to inspect:

```bash
gh api "repos/<owner>/<repo>/contents/.github/workflows/<workflow-file>" \
  --jq '.content' | base64 -d
```

Review for: bad indentation, unclosed quotes, unrendered Jinja2 placeholders.

## Step 6: Verify Success

### Check the reaction

Jules dispatch workflows post a rocket emoji reaction on the triggering comment
when the dispatch succeeds. This is the quickest way to confirm it worked:

```bash
gh api "repos/<owner>/<repo>/issues/comments/<COMMENT_ID>/reactions" \
  --jq '.[] | {content, user: .user.login}'
```

To find the comment ID:

```bash
gh api "repos/<owner>/<repo>/issues/<ISSUE_NUMBER>/comments" \
  --jq '.[] | {id, body: .body[:80]}'
```

### Check for a created PR

If the workflow creates a pull request:

```bash
gh pr list --state open --limit 10

# Or search by branch pattern
gh pr list --head "jules/" --state open
```

### Re-run a failed run

```bash
# Re-run all jobs
gh run rerun <RUN_ID>

# Re-run only failed jobs
gh run rerun <RUN_ID> --failed
```

## Related Skills

- **`/jules-actions`** — Generate Jules dispatch workflow files from config YAML.
  Use this first if the user does not yet have workflow files.
- **`/jules-prompt`** — Craft effective prompts for Jules agent workflows.
  Use this to refine what the agent does once the workflow is triggering correctly.
