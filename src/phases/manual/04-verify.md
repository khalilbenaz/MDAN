# MDAN Phase 4 — VERIFY

> **Goal:** Validate that what was built works correctly, securely, and completely.  
> **Agents:** Test Agent, Security Agent  
> **Output:** Validated test suite, security report, signed-off quality gate

---

## Phase Overview

VERIFY is where MDAN proves the software works — not assumes it does. Every acceptance criterion 
is tested. Every security finding from BUILD is verified as resolved. Performance is measured.

**Rule:** "It works on my machine" is not verification. Repeatable, automated tests are.

---

## MDAN Core Behavior in VERIFY

1. **Announces** Phase 4: VERIFY
2. **Activates Test Agent** for full test suite creation
3. **Activates Security Agent** for final security review
4. **Validates all findings** are resolved or explicitly accepted
5. **Runs Phase Gate check**

---

## Test Agent Activation Script

```
[ACTIVATING: Test Agent]

Task: Create and execute the full test suite for this project.

PRD (acceptance criteria): [Link/paste]
Architecture: [Link/paste]
Implemented features: [List of completed features]

Expected output:
1. Complete test plan
2. Unit tests for all features (80%+ coverage)
3. Integration tests for critical flows
4. E2E test scenarios
5. Scenario tests (Better Agents format)
6. Evaluation datasets (if RAG/ML features)
7. Performance test criteria
8. Test results summary
```

---

## Final Security Review Activation

```
[ACTIVATING: Security Agent]

Task: Final security review of the complete application.

Previous security findings: [List with resolution status]
Full codebase: [Context/summary]
Deployment configuration: [From DevOps Agent if available]

Expected output:
1. Verification that previous findings are resolved
2. Any new findings discovered
3. Final security sign-off (or list of blockers)
```

---

## Phase 4 Quality Gate

```
✅ VERIFY → SHIP Quality Gate

Testing:
[ ] All acceptance criteria have corresponding tests
[ ] All tests pass (0 failures)
[ ] Test coverage meets target (e.g., 80%)
[ ] Integration tests pass
[ ] At least 3 E2E scenarios pass
[ ] Scenario tests pass (Better Agents format)
[ ] Evaluation benchmarks pass (if RAG/ML features)
[ ] Performance criteria are met

Security:
[ ] All CRITICAL findings resolved
[ ] All HIGH findings resolved or explicitly accepted with rationale
[ ] Final security review completed
[ ] No new CRITICAL findings

Quality:
[ ] No known bugs that affect MVP functionality
[ ] Error messages are user-friendly (no stack traces exposed)
[ ] Application handles edge cases gracefully
```

---

## VERIFY Phase Artifacts

| Artifact | Template | Owner | Status Needed |
|---|---|---|---|
| Test Plan | `templates/TEST-PLAN.md` | Test Agent | Complete |
| Security Report | `templates/SECURITY-REVIEW.md` | Security Agent | Signed off |
| Scenarios | `templates/tests/scenarios/*.test.md` | Test Agent | Pass |
| Evaluations | `templates/tests/evaluations/*.md` | Test Agent | Pass thresholds |
