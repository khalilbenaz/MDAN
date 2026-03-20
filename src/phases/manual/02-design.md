# MDAN Phase 2 — DESIGN

> **Goal:** Architect the complete solution before writing a single line of code.  
> **Agents:** Architect Agent, UX Agent  
> **Output:** Architecture Document + UX Specification

---

## Phase Overview

DESIGN is where the solution takes shape. By the end of this phase, every technical and 
interface decision should be made. The BUILD phase should have zero architectural surprises.

**Duration:** Until every design question is answered.  
**Rule:** If you're still making architecture decisions during BUILD, DESIGN failed.

---

## MDAN Core Behavior in DESIGN

1. **Announces** Phase 2: DESIGN
2. **Reviews** the validated PRD
3. **Activates Architect Agent** first — system design before interface design
4. **Reviews** the Architecture Document with the user
5. **Activates UX Agent** — interface design aligned to architecture
6. **Reviews** the UX Specification with the user
7. **Runs Phase Gate check** before proceeding

---

## Architect Agent Activation Script

```
[ACTIVATING: Architect Agent]

Task: Design the complete system architecture for this project.

PRD: [Paste validated PRD]
Technical constraints: [From discovery]
Team profile: [Size, skill level]
Deployment preferences: [Cloud provider, on-prem, etc.]

Expected outputs:
1. Architecture diagram (Mermaid)
2. Technology stack with justifications
3. Data models
4. API design
5. Security architecture
6. Non-functional requirements strategy
7. Project structure
8. Coding conventions
9. Architecture Decision Records
```

---

## UX Agent Activation Script

```
[ACTIVATING: UX Agent]

Task: Design the complete user interface specification for this project.

PRD: [Paste validated PRD — personas and user stories]
Architecture constraints: [Tech stack, limitations]
Existing brand/design system: [If any, else "None — create from scratch"]

Expected outputs:
1. Design system (colors, typography, spacing)
2. Navigation structure
3. User flows for all key user stories
4. Screen specifications with all states
5. Component specifications
6. Accessibility requirements
7. UI copy guidelines
```

---

## Design Review Process

After each agent delivers its output, MDAN Core:

1. **Checks completeness** against the quality gate
2. **Cross-checks consistency** — does the UX spec align with the architecture?
3. **Presents to user** with key decisions highlighted
4. **Asks for explicit validation** before continuing

```
📐 Design Review: [Document Name]

Key decisions made in this document:
1. [Decision]: [Choice made] — Rationale: [Why]
2. [Decision]: [Choice made] — Rationale: [Why]
3. [Decision]: [Choice made] — Rationale: [Why]

Please review and confirm:
[ ] I agree with the technology choices
[ ] I agree with the data model design
[ ] I agree with the API design
[ ] I have no unresolved concerns

Type "DESIGN APPROVED" to proceed to Phase 3: BUILD
Or describe your concerns and we'll revise.
```

---

## Phase 2 Quality Gate

```
✅ DESIGN → BUILD Quality Gate

Architecture:
[ ] System architecture diagram is complete
[ ] All PRD requirements are addressed in the architecture
[ ] Technology stack is fully specified with justifications
[ ] All data entities and relationships are defined
[ ] All API endpoints are specified
[ ] Security architecture is defined (auth, authz, encryption)
[ ] Non-functional requirements are addressed
[ ] Project structure is defined
[ ] Coding conventions are documented
[ ] At least one ADR is written

UX:
[ ] Design system is complete (colors, typography, spacing, breakpoints)
[ ] Navigation structure covers all app sections
[ ] User flows cover all user stories from PRD
[ ] Every screen has all states (default, loading, empty, error)
[ ] Accessibility requirements are defined
[ ] Mobile behavior is specified

Cross-check:
[ ] UX spec is consistent with architecture (no impossible requirements)
[ ] Performance requirements are reflected in both arch and UX
[ ] Both documents are validated by the user
```

---

## DESIGN Phase Artifacts

| Artifact | Template | Owner | Status Needed |
|---|---|---|---|
| Architecture Document | `templates/ARCHITECTURE.md` | Architect Agent | Validated |
| UX Specification | *(in-line document)* | UX Agent | Validated |
