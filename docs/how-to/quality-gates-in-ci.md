# How to: wire quality gates into CI

MDAN's quality checks are plain deterministic text analysis (no LLM call), so they run fine in CI. Three commands, three exit codes to gate on:

| Command | Checks | Exit code |
|---------|--------|-----------|
| `mdan check [files...]` | Unfilled placeholders, TODO/TBD, empty/missing sections, measurable NFRs, FR coverage by stories, NFR coverage by architecture, acceptance criteria | `1` on `FAIL` (`0` on `PASS`/`CONCERNS`) |
| `mdan trace [--graph]` | Requirement (FR/NFR) → story → test coverage matrix | `1` on `FAIL` |
| `mdan stale` | Artifacts changed since they were registered in the context graph, and what downstream needs re-review | `2` if anything is stale, `0` otherwise |

Add `--json` to any of them for machine-readable output in a later step (e.g. posting a PR comment).

Strictness (what counts as FAIL vs CONCERNS) follows the project scale — `auto` (from story count), `solo`, `team`, or `enterprise` — set at install with `--scale`, or overridden per call with `mdan check --scale enterprise`.

## GitHub Actions

```yaml
name: MDAN quality gate

on:
  pull_request:
    paths: ["mdan_output/planning-artifacts/**", "docs/**"]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npx mdan-method check
      - run: npx mdan-method trace
      - run: npx mdan-method stale   # non-blocking: remove `continue-on-error` to fail the build
        continue-on-error: true
```

## Azure DevOps

```yaml
trigger: none
pr:
  paths:
    include:
      - mdan_output/planning-artifacts/*
      - docs/*

pool:
  vmImage: ubuntu-latest

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: "22.x"
  - script: npx mdan-method check
    displayName: "MDAN quality gate"
  - script: npx mdan-method trace
    displayName: "MDAN traceability"
  - script: npx mdan-method stale
    displayName: "MDAN staleness (informational)"
    continueOnError: true
```

## Notes

- These commands read `_mdan/state/` and the context graph, so the checkout needs those files (don't `.gitignore` them if you rely on CI checks — or restore them from wherever your team stores project state).
- `mdan check` without arguments checks the artifacts registered in the project state (falling back to `docs/`); pass explicit paths (`mdan check docs/prd.md docs/architecture.md`) to pin exactly what CI checks.
- This is the same gate the planning wizards run before marking a workflow complete — CI is a second, independent enforcement point, not a duplicate of manual work.
