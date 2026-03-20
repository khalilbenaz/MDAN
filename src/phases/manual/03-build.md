# MDAN Phase 3 — BUILD

> **Goal:** Implement the solution with precision, security, and quality.  
> **Agents:** Dev Agent, Security Agent (concurrent)  
> **Output:** Working, tested, reviewed code

---

## Phase Overview

BUILD is where the code is written. But in MDAN, BUILD is not "just coding" — it's a structured 
process where every feature is implemented against a spec, reviewed, and security-checked before 
moving on.

**Rule:** No feature is "done" until it has tests and passes a security check.

---

## BUILD Workflow (per feature)

```
For each feature in the PRD (MVP scope):

1. MDAN Core prepares a Feature Brief
2. Dev Agent implements the feature
3. Security Agent reviews the implementation
4. MDAN Core reviews the combined output
5. User validates (or flags issues)
6. Move to next feature
```

---

## Feature Brief Template

MDAN Core creates this before activating the Dev Agent:

```
[ACTIVATING: Dev Agent]

Feature: [US-XXX: User story title]
Acceptance Criteria:
  - Given [context], When [action], Then [outcome]
  - [Additional criteria]

Architecture context:
  - Tech stack: [Stack]
  - Relevant data models: [Models]
  - Relevant API endpoints: [Endpoints]
  - Coding conventions: [Link/summary]

UX context:
  - Relevant screens: [Screen names]
  - Relevant components: [Component names]

Definition of Done:
  - [ ] All acceptance criteria met
  - [ ] Unit tests written and passing
  - [ ] No critical security issues
  - [ ] Code follows project conventions
```

---

## Concurrent Security Review

After Dev Agent delivers code, Security Agent reviews immediately:

```
[ACTIVATING: Security Agent]

Task: Security review of the following implementation.
Feature: [Feature name]
Code: [Dev Agent output]

Focus areas:
- Input validation
- Authentication/authorization
- Data exposure
- Error handling (no sensitive data in errors)
- Dependency risks
```

---

## Phase 3 Quality Gate

```
✅ BUILD → VERIFY Quality Gate

For each feature:
[ ] All acceptance criteria are implemented
[ ] Unit tests exist and pass
[ ] No CRITICAL or HIGH security findings unresolved
[ ] Code follows project conventions
[ ] Error handling is complete
[ ] No hardcoded secrets

Overall:
[ ] All MVP features are implemented
[ ] Code is in version control
[ ] Environment is reproducible (setup script or Docker)
```

---

## BUILD Phase Artifacts

| Artifact | Owner | Status Needed |
|---|---|---|
| Feature implementations | Dev Agent | Reviewed |
| Unit tests | Dev Agent | Passing |
| Security findings (per feature) | Security Agent | Resolved or accepted |
