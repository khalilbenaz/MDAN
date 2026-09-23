---
name: 'step-03-gates'
description: 'Finalize enforcement thresholds for each gate and register the pipeline design in the context graph'
wipFile: '{mdan_output}/ci-gates-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Enforce Gates & Register

**Progress: Step 3 of 3** - Final Step

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Confirm Gate Thresholds

For each gate that can fail the build, state the exact enforced threshold and confirm with the user:

- **Lint/type-check**: zero errors (warnings may be non-blocking if the project allows it — ask).
- **Unit tests**: 100% pass, zero skipped without an approved ticket reference in the skip annotation.
- **Security**: zero Critical/High dependency vulnerabilities unwaived; zero committed secrets.
- **Coverage**: line/branch coverage ≥ `coverage_gate` (default 80%) — and, if the project tracks it, no PR may LOWER coverage vs. the base branch even if still above the floor (prevents death-by-a-thousand-cuts erosion).
- **Integration/Contract**: 100% pass.
- **E2E/smoke**: 100% pass on the critical-journey subset; failures here should page/alert, not just fail silently on main.
- **Mutation testing (optional)**: if enabled, a mutation score floor (commonly 60-80% depending on maturity) — report-only initially, enforced once the baseline is known.

### 2. Explain Required Branch Protection

Tell the user which of these stage/job names must be added as required status checks in the repo's branch protection rules (GitHub) or build validation policy (Azure DevOps) — a gate that isn't required can be bypassed by a force-merge, which defeats the point.

### 3. Present and Confirm

Display the full pipeline design + gate thresholds. "**Select:** [C] Continue [E] Edit [P] Party Mode"

HALT and wait.

- IF E: apply edits, redisplay.
- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: proceed.

### 4. Finalize

a) Write the actual pipeline file(s) to the repository (with the user's confirmation of the path).

b) Update `{wipFile}` frontmatter: `status: 'configured'`, `stepsCompleted: [1, 2, 3]`.

c) Rename `{wipFile}` → `{mdan_output}/ci-gates-{slug}.md`. Store as `finalFile`.

### 5. Register in the Context Graph

If MCP tools are available:

a) `mdan_graph_add_node { id: "ci-gates-{slug}", type: "artifact", path: "<finalFile relative path>", workflow: "qa-ci-gates", agent: "test-architect" }`

b) If this pipeline enforces the coverage gate that a `qa-traceability` or `qa-nfr-assessment` node depends on, `mdan_graph_add_edge { source: "<that-node-id>", target: "ci-gates-{slug}", relation: "impacts" }` — the pipeline is upstream of whether those artifacts' claims stay true.

c) `mdan_state_update { workflow: "qa-ci-gates", action: "complete", artifacts: ["{finalFile}", "<pipeline file path>"] }`.

### 6. Final Message

```
**CI Gates Configured!**

Pipeline: <pipeline file path>
Design doc: {finalFile}

Required status checks to add in branch protection: {gate_job_names}

Remember: run `qa-test-review` periodically on this suite — a gate is only as trustworthy
as the tests behind it.
```

---

## REQUIRED OUTPUTS:

- MUST state an explicit enforced threshold for every gate.
- MUST tell the user which checks need to be marked required in branch protection.
- MUST register the node when MCP tools are available.

## VERIFICATION CHECKLIST:

- [ ] Every gate has a stated, confirmed threshold — none left as "TBD."
- [ ] Branch protection / required-check guidance given.
- [ ] `stepsCompleted: [1, 2, 3]` set, file renamed, node registered.
