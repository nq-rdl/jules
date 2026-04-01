# Quick Reference

Command table and common testing patterns for Jules dispatch workflows.

## Command Table

| Task | Command |
|------|---------|
| List workflows | `gh workflow list` |
| Trigger via comment | `gh issue comment <N> --body "@jules-swe ..."` |
| Trigger manually | `gh workflow run <file>` |
| List recent runs | `gh run list --workflow=<file> --limit 5` |
| Watch a run | `gh run watch <RUN_ID>` |
| View run details | `gh run view <RUN_ID>` |
| Failed logs only | `gh run view <RUN_ID> --log-failed` |
| Full logs | `gh run view <RUN_ID> --log` |
| Job breakdown | `gh run view <RUN_ID> --json jobs` |
| Check secrets | `gh secret list` |
| Enable workflow | `gh workflow enable <file>` |
| Re-run failed | `gh run rerun <RUN_ID> --failed` |
| Check reactions | `gh api repos/<owner>/<repo>/issues/comments/<id>/reactions` |
| Check association | `gh api repos/<owner>/<repo>/collaborators/<user>/permission` |
| Cancel a run | `gh run cancel <RUN_ID>` |
| Delete a run | `gh run delete <RUN_ID>` |

## Common Patterns

### End-to-end test in one shot

```bash
# 1. Create test issue
ISSUE=$(gh issue create --title "Test: Jules SWE dispatch" \
  --body "Automated test of Jules SWE workflow." \
  --json number --jq '.number')

# 2. Trigger
gh issue comment "$ISSUE" --body "@jules-swe please analyse this test issue"

# 3. Wait for run to appear, then watch
sleep 15
RUN_ID=$(gh run list --workflow=jules-swe-dispatch.yml --limit 1 \
  --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID"
```

### Tail logs from the latest run

```bash
RUN_ID=$(gh run list --workflow=<file> --limit 1 \
  --json databaseId --jq '.[0].databaseId')
gh run view "$RUN_ID" --log-failed
```

### Check why a comment did not trigger

```bash
# Get last comment details
gh api "repos/<owner>/<repo>/issues/<N>/comments" \
  --jq '.[-1] | {id, author_association, body: .body[:120]}'

# Compare with workflow if condition
gh api "repos/<owner>/<repo>/contents/.github/workflows/<file>" \
  --jq '.content' | base64 -d | grep -A 5 'if:'
```

### Cancel a runaway workflow

```bash
# Find the run
RUN_ID=$(gh run list --workflow=<file> --status=in_progress --limit 1 \
  --json databaseId --jq '.[0].databaseId')

# Cancel it
gh run cancel "$RUN_ID"
```
