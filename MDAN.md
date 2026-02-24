# MDAN — Method Specification v1.0

> The complete, authoritative specification of the MDAN method.

---

## Part 1: Overview

MDAN (pronounced "em-dan") is a structured method for AI-driven software development.

**Core premise:** Building software with AI agents requires the same discipline that building software with human teams requires — clear roles, structured phases, enforced quality, and explicit handoffs. Without this structure, AI agents hallucinate tasks, contradict each other, skip validation, and produce inconsistent results.

**MDAN's answer:** A central orchestrator (MDAN Core) that coordinates specialized agents through a 5-phase workflow, with quality gates enforced at every transition.

---

## Part 2: Principles

### P1 — Orchestrate, Don't Execute
MDAN Core is a thinking and planning agent. It never executes directly. Execution belongs to the specialized agents.

### P2 — One Phase at a Time
Phases are sequential and non-negotiable. A completed DISCOVER phase produces a better BUILD than a rushed DISCOVER ever could.

### P3 — Artifacts Over Words
Every phase produces artifacts — structured documents with defined templates. Words in a chat window are not artifacts.

### P4 — Explicit Validation
Every phase ends with the user explicitly approving the artifacts. MDAN Core never proceeds without approval.

### P5 — LLM Agnosticism
MDAN produces identical results regardless of the underlying LLM. The Universal Envelope is the technical mechanism that achieves this.

### P6 — Security Is Not Optional
The Security Agent is active in BUILD and VERIFY. Security is not a checklist at the end — it's a parallel concern throughout.

### P7 — Fail Fast, Fail Early
A problem found in DISCOVER costs 1 unit of effort. The same problem found in SHIP costs 100 units.

---

## Part 3: The MDAN Core

MDAN Core is the central orchestrator. It operates on these rules:

**Knows everything:** MDAN Core always has the full context — PRD, architecture, UX spec, current feature, previous decisions.

**Delegates everything:** MDAN Core never writes code, designs interfaces, or drafts documentation. It activates the appropriate agent with a precise brief.

**Validates everything:** Every agent output is reviewed by MDAN Core before being presented to the user. MDAN Core checks completeness against quality checklists.

**Provides Intelligent Help:** MDAN Core acts as a guide. When users feel lost or need direction, they can use the `/mdan-help` command, and MDAN Core will instantly summarize the current state and provide concrete next steps.

**Facilitates "Party Mode":** For complex problems requiring multiple perspectives, MDAN Core can invoke multiple agents simultaneously using `/party [topic]` to foster a collaborative debate (e.g., between the Architect and Security agents) before a decision is made.

**Controls phase transitions:** Only MDAN Core can declare a phase complete and move to the next. The user must explicitly approve each transition.

---

## Part 4: Agent Network

### Agent Design Rules

Every MDAN agent is:
1. **Personified** — Has a name (e.g., Khalil, Reda) to make collaboration natural
2. **Specialized** — One domain, deep expertise
3. **Autonomous** — Operates independently within its domain
4. **Bounded** — Cannot make decisions outside its domain (escalates to Core)
5. **Self-checking** — Runs a quality checklist before submitting output
6. **Universal** — Works identically across all LLMs via the Universal Envelope

### Agent Hierarchy

```
MDAN Core (Orchestrator)
│
├── Phase 1 — DISCOVER
│   └── Product Agent
│
├── Phase 2 — DESIGN
│   ├── Architect Agent
│   └── UX Agent
│
├── Phase 3 — BUILD
│   ├── Dev Agent
│   └── Security Agent (concurrent)
│
├── Phase 4 — VERIFY
│   ├── Test Agent
│   └── Security Agent
│
└── Phase 5 — SHIP
    ├── DevOps Agent
    └── Doc Agent
```

---

## Part 5: The Universal Envelope

The Universal Envelope is the standard prompt structure used for all MDAN agents. It solves the LLM compatibility problem by normalizing agent behavior.

### Envelope Fields

| Field | Purpose |
|-------|---------|
| NAME | Agent identifier |
| VERSION | Prompt version for tracking |
| ROLE | One-line role description |
| PHASE | Which phase(s) this agent operates in |
| REPORTS_TO | Always MDAN Core |
| IDENTITY | Who the agent is — expertise and mindset |
| CAPABILITIES | What the agent can produce |
| CONSTRAINTS | Hard limits on what the agent must NOT do |
| INPUT_FORMAT | What the agent expects from MDAN Core |
| OUTPUT_FORMAT | How the agent must structure its response |
| QUALITY_CHECKLIST | Self-validation before submission |
| ESCALATION | When to flag issues back to MDAN Core |

### LLM Adaptation

| LLM Family | Tag Style | Notes |
|---|---|---|
| Claude | `[TAG]` XML-style | Native support |
| OpenAI | `## SECTION` Markdown | Replace brackets with headers |
| Google | `## SECTION` Markdown | Prefer markdown throughout |
| Chinese LLMs | Either style | Test and use what works |

---

## Part 6: Artifact Standard

Every artifact produced by MDAN agents follows this header:

```
---
Artifact: [Artifact Name]
Phase: [Phase Name]
Agent: [Agent Name]
Version: [X.Y]
Status: Draft | Review | Validated
Date: [YYYY-MM-DD]
Project: [Project Name]
---
```

### Artifact Registry

| Artifact | Phase | Template | Owner |
|---|---|---|---|
| PRD | DISCOVER | `templates/PRD.md` | Product Agent |
| Architecture Document | DESIGN | `templates/ARCHITECTURE.md` | Architect Agent |
| UX Specification | DESIGN | *(inline)* | UX Agent |
| Feature Implementation | BUILD | *(inline)* | Dev Agent |
| Security Review | BUILD/VERIFY | `templates/SECURITY-REVIEW.md` | Security Agent |
| Test Plan | VERIFY | `templates/TEST-PLAN.md` | Test Agent |
| Deployment Config | SHIP | *(inline)* | DevOps Agent |
| README | SHIP | *(inline)* | Doc Agent |
| CHANGELOG | SHIP | `templates/CHANGELOG.md` | Doc Agent |

---

## Part 7: Quality Gates

### Gate 1: DISCOVER → DESIGN

```
[ ] Problem is specifically defined (not "build an app")
[ ] At least one user persona is fully described
[ ] Success metrics are measurable (numbers, not adjectives)
[ ] Constraints are documented
[ ] PRD is complete with MoSCoW prioritization
[ ] MVP scope is realistic for the given constraints
[ ] All user stories have acceptance criteria
[ ] Risks are identified with mitigation plans
[ ] Out-of-scope items are explicitly listed
[ ] User has approved the PRD
```

### Gate 2: DESIGN → BUILD

```
[ ] System architecture diagram is complete
[ ] All PRD requirements are addressed
[ ] Full technology stack is specified with justifications
[ ] All data models are defined
[ ] All API endpoints are specified
[ ] Security architecture is defined
[ ] Non-functional requirements are addressed
[ ] Coding conventions are documented
[ ] At least one ADR exists
[ ] Design system is complete
[ ] Navigation covers all sections
[ ] All screens have all states defined
[ ] Both documents are user-approved
```

### Gate 3: BUILD → VERIFY

```
[ ] All MVP features are implemented
[ ] Each feature has unit tests
[ ] No unresolved CRITICAL security findings
[ ] No unresolved HIGH security findings
[ ] Code follows project conventions
[ ] No hardcoded secrets
[ ] All error paths are handled
[ ] Code is in version control
```

### Gate 4: VERIFY → SHIP

```
[ ] All acceptance criteria have test coverage
[ ] All tests pass (zero failures)
[ ] Test coverage meets target
[ ] Integration tests pass
[ ] At least 3 E2E scenarios validated
[ ] Performance criteria met
[ ] Final security review complete
[ ] All CRITICAL and HIGH findings resolved
[ ] Documentation complete
[ ] Deployment runbook complete
```

---

## Part 8: MDAN Lifecycle

```
User presents project idea
         │
         ▼
Phase 1: DISCOVER
   MDAN Core asks 5 discovery questions
   Product Agent creates PRD
   User validates PRD
         │
   [Gate 1]
         │
         ▼
Phase 2: DESIGN
   Architect Agent creates Architecture Document
   UX Agent creates UX Specification
   User validates both
         │
   [Gate 2]
         │
         ▼
Phase 3: BUILD
   For each feature:
     Dev Agent implements
     Security Agent reviews
     MDAN Core validates
         │
   [Gate 3]
         │
         ▼
Phase 4: VERIFY
   Test Agent creates & runs test suite
   Security Agent final review
   User signs off
         │
   [Gate 4]
         │
         ▼
Phase 5: SHIP
   DevOps Agent deploys
   Doc Agent documents
   Post-deployment validation
         │
         ▼
   🚀 LAUNCHED
         │
         ▼
   Next iteration → Back to Phase 1
```

---

## Part 9: Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025 | Initial release |
