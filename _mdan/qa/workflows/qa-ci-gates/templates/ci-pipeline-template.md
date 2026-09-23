---
title: '{title}'
slug: '{slug}'
stack: '{stack}'
ci_provider: '{ci_provider}'
created: '{date}'
status: 'in-progress'
stepsCompleted: []
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# CI Test Pipeline Design: {title}

**Stack:** {stack}
**CI Provider:** {ci_provider}
**Created:** {date}

## Stack

{stack_details}

## Stage Plan

| # | Stage | Runs on | Depends on | Blocking? |
|---|---|---|---|---|

## Generated Pipeline

**File:** {pipeline_file_path}

```yaml
{pipeline_content}
```

## Gate Thresholds

| Gate | Threshold | Enforced how |
|---|---|---|

## Required Status Checks (Branch Protection)

{required_checks_list}
