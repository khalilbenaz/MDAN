---
name: 'step-01-stack-detect'
description: 'Detect the language/framework/CI provider and design the pipeline stage plan'
templateFile: '../templates/ci-pipeline-template.md'
wipFile: '{mdan_output}/ci-gates-wip.md'
nextStepFile: './step-02-pipeline.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Detect Stack & Plan Stages

**Progress: Step 1 of 3** - Next: Generate Pipeline

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 0. Check for Work in Progress

Check `{wipFile}`; offer resume/archive if present (pattern: `{project-root}/_mdan/qa/workflows/qa-test-design/steps/step-01-scope.md`). HALT and wait.

### 1. Detect the Stack

Inspect the repo: `package.json`/`pyproject.toml`/`*.csproj`/`go.mod`/`Gemfile` for language + test framework; existing `.github/workflows/`, `azure-pipelines.yml`, `.gitlab-ci.yml` for the current CI provider (if any). Confirm with the user rather than assume when ambiguous (e.g. monorepo with multiple stacks).

### 2. Ask for the CI Provider

If no existing pipeline file, ask: "GitHub Actions or Azure DevOps?" (this workflow ships templates for both — say so). If another provider is requested, generate the same stage plan and note the provider-specific syntax is the user's to adapt.

### 3. Design the Stage Plan

Lay out stages in fail-fast order, each stage only runs if the previous passed:

1. **Lint / static analysis** (seconds) — formatting, linting, type-check.
2. **Unit tests** (seconds-minutes) — no network/DB, run in parallel/sharded if the suite is large.
3. **Security scan** — dependency audit (`npm audit`/`pip-audit`/`dotnet list package --vulnerable`) + secret scan; can run in parallel with stage 2.
4. **Integration tests** (minutes) — real DB/queue via service containers or ephemeral instances.
5. **Contract tests** (if applicable) — consumer-driven contract verification against provider stubs/broker.
6. **Coverage gate** — computed from unit+integration, enforced against `coverage_gate` (default 80%).
7. **E2E / smoke** (minutes, only on merge to main or nightly, not every PR, unless the suite is fast and stable) — critical journeys only.
8. **Mutation testing** (optional, nightly/weekly, not per-PR — too slow) — note as optional and explain the tradeoff (catches assertion-quality gaps unit coverage % cannot see, but is expensive).

### 4. Save Progress

a) Copy `{templateFile}` to `{wipFile}`.

b) Fill frontmatter (`title`, `slug`, `stack`, `ci_provider`, `created`, `status: in-progress`, `stepsCompleted: [1]`).

c) Fill the **Stack** and **Stage Plan** sections.

### 5. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Generate Pipeline (Step 2 of 3)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-ci-gates/steps/step-02-pipeline.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] Stack and CI provider identified/confirmed.
- [ ] Stage plan ordered fail-fast, mutation testing (if used) kept out of the per-PR critical path.
- [ ] `stepsCompleted: [1]` set.
