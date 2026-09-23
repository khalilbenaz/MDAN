---
name: 'step-03-score'
description: 'Score each category, issue an overall NFR verdict, and register in the context graph'
wipFile: '{mdan_output}/nfr-assessment-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Score & Finalize

**Progress: Step 3 of 3** - Final Step

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Score Each Category

Per category, apply:

- **PASS** — all thresholds Met.
- **CONCERNS** — at least one Unknown, or a Not Met item that is non-critical (does not affect a P0/P1 path per `qa-test-design`/`qa-traceability` if available).
- **FAIL** — at least one Not Met item on a critical path (security Critical/High finding; reliability gap on a P0 flow; performance breach on a P0 endpoint under expected load).

### 2. Overall Verdict

Overall = the worst of the four category scores (FAIL if any category FAILs, else CONCERNS if any CONCERNS, else PASS). Do not average — a PASS on maintainability cannot offset a FAIL on security.

### 3. Present and Confirm

Present the full scored assessment. Display: "**Select:** [C] Continue [E] Edit [P] Party Mode"

HALT and wait.

- IF E: apply edits, redisplay.
- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: proceed.

### 4. Finalize

a) Update `{wipFile}` frontmatter: `status: 'assessed'`, `overall_verdict: 'PASS'|'CONCERNS'|'FAIL'`, `stepsCompleted: [1, 2, 3]`.

b) Rename `{wipFile}` → `{mdan_output}/nfr-assessment-{slug}.md`. Store as `finalFile`.

### 5. Register in the Context Graph

If MCP tools are available:

a) `mdan_graph_add_node { id: "nfr-{slug}", type: "artifact", path: "<finalFile relative path>", workflow: "qa-nfr-assessment", agent: "test-architect" }`

b) Link it to the target system/story/epic node: `mdan_graph_add_edge { source: "nfr-{slug}", target: "<target-node-id>", relation: "references" }`.

c) `mdan_state_update { workflow: "qa-nfr-assessment", action: "complete", artifacts: ["{finalFile}"] }`.

### 6. Final Message

```
**NFR Assessment Complete — Overall: {overall_verdict}**

Saved to: {finalFile}
Performance: {perf_verdict} | Security: {sec_verdict} | Reliability: {rel_verdict} | Maintainability: {maint_verdict}

{list any FAIL/CONCERNS items with their remediation}

Feed this into qa-release-gate alongside test-design and traceability for the go/no-go decision.
```

---

## REQUIRED OUTPUTS:

- MUST issue a per-category verdict and an overall verdict (worst-of, not averaged).
- MUST register the node when MCP tools are available.

## VERIFICATION CHECKLIST:

- [ ] Every category scored PASS/CONCERNS/FAIL against its evidence.
- [ ] Overall verdict = worst category, not an average.
- [ ] `stepsCompleted: [1, 2, 3]` set, file renamed, node registered.
