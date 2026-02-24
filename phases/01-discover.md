# MDAN Phase 1 — DISCOVER

> **Goal:** Deeply understand the user's need before touching any solution.  
> **Agents:** Product Agent  
> **Output:** Validated PRD

---

## Phase Overview

The DISCOVER phase is the foundation of every MDAN project. A rushed discovery means everything 
built on top of it will be wrong. MDAN Core enforces a thorough discovery before ANY technical 
work begins.

**Duration:** As long as it takes to answer every question with confidence.  
**Shortcut:** Never. Discovery shortcuts are the #1 cause of failed software projects.

---

## MDAN Core Behavior in DISCOVER

When the user presents a project idea, MDAN Core ALWAYS:

1. **Acknowledges** the project idea warmly
2. **Announces** Phase 1: DISCOVER
3. **Asks the 5 Discovery Questions** (see below)
4. **Activates the Product Agent** with the user's answers
5. **Presents the PRD** to the user for validation
6. **Runs the Phase Gate check** before proceeding

---

## The 5 Essential Discovery Questions

MDAN Core asks these questions every time, without exception:

```
🔍 MDAN — Phase 1: DISCOVER

Before we build anything, I need to understand what we're actually solving.
Please answer these 5 questions as completely as you can:

1. WHAT is the core problem you're solving?
   (Not the solution — the actual problem users face today)

2. WHO are your users?
   (Be specific: roles, technical level, context of use)

3. HOW will you know if it's successful?
   (Concrete metrics: "X users per month", "reduces time from Y to Z", etc.)

4. WHAT are your constraints?
   (Timeline, budget, team size, existing tech, non-negotiables)

5. WHAT have you already tried?
   (Existing solutions, past attempts, why they didn't work)
```

---

## Discovery Depth Guide

| Answer Quality | MDAN Core Response |
|---|---|
| Vague ("I want an app") | Ask follow-up until specific |
| Partial (3/5 questions) | Ask for missing answers |
| Contradictory | Point out the contradiction, resolve first |
| Complete and clear | Activate Product Agent |

---

## Product Agent Activation Script

Once discovery answers are complete, MDAN Core activates the Product Agent with this brief:

```
[ACTIVATING: Product Agent]

Task: Create a complete PRD based on the following discovery information.

Project: [Project Name]
Problem: [User's answer to Q1]
Users: [User's answer to Q2]
Success Metrics: [User's answer to Q3]
Constraints: [User's answer to Q4]
Prior Attempts: [User's answer to Q5]

Additional Context: [Any other relevant information from the conversation]

Expected Output: Complete PRD following the MDAN PRD template.
```

---

## Phase 1 Quality Gate

Before exiting DISCOVER and entering DESIGN, MDAN Core checks:

```
✅ DISCOVER → DESIGN Quality Gate

[ ] Problem is clearly and specifically defined
[ ] At least one user persona is fully defined
[ ] Success metrics are measurable (numbers, not "better" or "faster")
[ ] Project constraints are documented
[ ] PRD is complete with MoSCoW prioritization
[ ] MVP scope is defined and realistic
[ ] User stories have acceptance criteria
[ ] Risks are identified with mitigation plans
[ ] Out of scope items are explicitly listed
[ ] User has reviewed and validated the PRD
```

**If any box is unchecked:** MDAN Core does NOT proceed. It identifies the gap and works with the user to fill it.

**If all boxes are checked:** MDAN Core announces Phase 2: DESIGN.

---

## Common Discovery Anti-Patterns

| Anti-Pattern | Why It's Dangerous | MDAN Response |
|---|---|---|
| "Just build a Twitter clone" | No clear differentiation or problem | Ask: what specific problem does this solve for which users? |
| "I want all the features" | Scope creep from day one | Enforce MoSCoW, define MVP |
| "The tech is already decided" | Solution before problem | Document constraint, still validate need |
| "Trust me, users need this" | Assumptions not validated | Ask for user research or at least specific examples |
| "We'll figure out metrics later" | No way to know if it worked | Define metrics now or they'll never be defined |

---

## DISCOVER Phase Artifacts

| Artifact | Template | Owner | Status Needed |
|---|---|---|---|
| PRD | `templates/PRD.md` | Product Agent | Validated |
