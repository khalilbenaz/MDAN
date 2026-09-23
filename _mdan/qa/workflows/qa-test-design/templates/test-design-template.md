---
title: '{title}'
slug: '{slug}'
target_id: '{target_id}'
created: '{date}'
status: 'in-progress'
stepsCompleted: []
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Test Design: {title}

**Target:** {target_id}
**Created:** {date}

## Scope

{scope_description}

## Scenarios (unscored)

| # | Scenario | Type | AC/Requirement ref |
|---|---|---|---|

## Risk Scoring

| # | Scenario | Probability | Impact | Score | Priority |
|---|---|---|---|---|---|

## Test Level Mapping

| # | Scenario | Priority | Level | Test Idea (Given/When/Then) |
|---|---|---|---|---|

## Level Distribution

- Unit: {unit_pct}%
- Integration: {integration_pct}%
- E2E: {e2e_pct}%
- Contract: {contract_count}

## Known Gaps

{known_gaps}

## Context Graph Registration

- Node: `test-design-{slug}`
- Edges: {edges_list}
