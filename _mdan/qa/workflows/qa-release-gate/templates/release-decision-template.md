---
title: '{title}'
slug: '{slug}'
release_scope: '{release_scope}'
created: '{date}'
status: 'in-progress'
gate_decision: ''
stepsCompleted: []
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Release Decision: {title}

**Scope:** {release_scope}
**Created:** {date}

## Release Scope

{release_scope_details}

## Artifact Verdicts

| Artifact | Node id | Verdict | Notes |
|---|---|---|---|
| Test design | | | |
| Traceability matrix | | | |
| NFR assessment | | | |
| Test review | | | |

## Open Defects

| ID | Severity | Blocks P0/P1 flow? | Workaround? |
|---|---|---|---|

## Staleness Check

| Changed artifact | Stale downstream node | Resolution (re-verified / waived) | Approver (if waived) |
|---|---|---|---|

## Gate Decision

**Decision:** {gate_decision}

{decision_justification}

## Decision Record Registration

- Node: `release-decision-{slug}`
- Impacts: {impacted_artifact_ids}
