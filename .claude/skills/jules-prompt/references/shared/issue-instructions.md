## Instructions

Perform issue triage only for the issue above.

Do not modify code, create commits, create branches, open or update a pull
request, or claim that fixes have been implemented. Your deliverable is a
structured assessment that helps a human decide the next action.

Review the issue against this repository and produce a triage assessment with
these checks:

1. **Verdict** — classify the issue as one of:
   - Ready for implementation
   - Needs clarification
   - Duplicate or already covered
   - Out of scope for this repository
   - Blocked by dependency or external decision
   - Needs human design or product input
2. **Scope assessment** — explain whether the requested work belongs in this
   repository. If only part is in scope, separate the in-repo and out-of-repo
   concerns.
3. **Clarity check** — identify missing reproduction details, expected
   behaviour, acceptance criteria, screenshots, logs, or examples. If the issue
   is not yet actionable, say exactly what information is missing.
4. **Likely code areas** — identify the most likely directories, files,
   functions, tests, workflows, or docs that would be involved. Distinguish
   clearly between confirmed evidence and likely touch points.
5. **Risk and blast radius** — assess likely risk as low, medium, or high, and
   note any impact on code, workflows, docs, tests, security, or user-facing
   behaviour.
6. **Related work and duplication** — call out obvious duplicates, overlaps,
   dependencies, or follow-up work only where the available evidence supports
   it. If you cannot verify duplication from the available context, say so
   explicitly rather than guessing.
7. **Routing recommendation** — recommend the most appropriate next owner and
   trigger:
   - `@jules-swe` for code changes in this repo
   - `@jules-docs` for documentation-only work
   - `@jules-security` for security review or remediation
   - human follow-up when clarification, design, or external coordination is required
8. **Task sizing** — state whether the work looks suitable for a single PR or
   should be split into smaller tasks. If it should be split, suggest the split
   boundaries.
9. **Implementation plan** — if the issue is ready, provide a short, concrete,
   ordered plan covering investigation, implementation, tests, and validation.
10. **Acceptance criteria** — if the issue is ready, propose clear checks that a
    follow-up implementation should satisfy.

Respond using this exact structure:

## Verdict
## Scope assessment
## Clarity and missing information
## Likely code areas
## Risk and blast radius
## Related issues or dependencies
## Recommended next action
## Proposed implementation plan
## Likely file targets
## Acceptance criteria

Under **Likely file targets**, use these sub-headings when applicable:
- Existing files likely touched
- Possible new files
- Tests likely required

Under **Recommended next action**, include a copy-pasteable follow-up comment
when appropriate, for example `@jules-swe implement using this triage plan`.

Prefer evidence over confidence. If something is uncertain, say so plainly.
Keep the assessment concise, decision-oriented, and useful to a team lead.
