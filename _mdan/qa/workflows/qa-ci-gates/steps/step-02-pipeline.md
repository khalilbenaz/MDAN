---
name: 'step-02-pipeline'
description: 'Generate the concrete CI pipeline file(s) implementing the stage plan'
wipFile: '{mdan_output}/ci-gates-wip.md'
nextStepFile: './step-03-gates.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Generate Pipeline

**Progress: Step 2 of 3** - Next: Enforce Gates & Register

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Generate the Pipeline File

Write the actual pipeline file for the confirmed provider, implementing the stage plan from Step 1. Use the reference examples below as a starting skeleton, adapted to the detected stack's real commands (do not invent a command that doesn't exist in the project — check `package.json` scripts / `Makefile` / `justfile` first and call those).

**GitHub Actions** (`.github/workflows/ci.yml`):

```yaml
name: CI
on: [pull_request, push]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: <install deps>
      - run: <lint command>

  unit:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - run: <install deps>
      - run: <unit test command with coverage output>
      - uses: actions/upload-artifact@v4
        with: { name: coverage, path: <coverage report path> }

  security:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - run: <dependency audit command>

  integration:
    runs-on: ubuntu-latest
    needs: unit
    services:
      # e.g. postgres: { image: postgres:16, env: {...}, ports: ["5432:5432"] }
    steps:
      - uses: actions/checkout@v4
      - run: <integration test command>

  coverage-gate:
    runs-on: ubuntu-latest
    needs: [unit, integration]
    steps:
      - uses: actions/download-artifact@v4
        with: { name: coverage }
      - run: <fail the job if coverage < {coverage_gate}%>

  e2e:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    needs: coverage-gate
    steps:
      - uses: actions/checkout@v4
      - run: <e2e command>
```

**Azure DevOps** (`azure-pipelines.yml`):

```yaml
trigger: [main]
pr: ['*']

stages:
  - stage: Lint
    jobs:
      - job: Lint
        steps:
          - script: <install deps>
          - script: <lint command>

  - stage: Unit
    dependsOn: Lint
    jobs:
      - job: Unit
        steps:
          - script: <install deps>
          - script: <unit test command with coverage output>
          - publish: <coverage report path>
            artifact: coverage

  - stage: Security
    dependsOn: Lint
    jobs:
      - job: Audit
        steps:
          - script: <dependency audit command>

  - stage: Integration
    dependsOn: Unit
    jobs:
      - job: Integration
        # services via docker-compose task or Azure DevOps service containers
        steps:
          - script: <integration test command>

  - stage: CoverageGate
    dependsOn: [Unit, Integration]
    jobs:
      - job: Gate
        steps:
          - download: current
            artifact: coverage
          - script: <fail the job if coverage < {coverage_gate}%>

  - stage: E2E
    dependsOn: CoverageGate
    condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
    jobs:
      - job: E2E
        steps:
          - script: <e2e command>
```

### 2. Wire Real Commands

Replace every `<placeholder>` with the actual command from the project (npm scripts, dotnet test filters, pytest markers, etc.). If a command doesn't exist yet (e.g. no `test:integration` script), propose adding it and confirm with the user before writing the pipeline file.

### 3. Update WIP File

a) Write the final pipeline file path + its full content into the **Generated Pipeline** section of `{wipFile}`.

b) Update frontmatter: `stepsCompleted: [1, 2]`.

### 4. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Enforce Gates & Register (Step 3 of 3)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1, 2]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-ci-gates/steps/step-03-gates.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] Pipeline file generated for the confirmed provider with real project commands (no unresolved placeholders left).
- [ ] Stage dependencies match the fail-fast order from Step 1.
- [ ] `stepsCompleted: [1, 2]` set.
