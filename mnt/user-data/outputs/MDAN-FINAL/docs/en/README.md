# MDAN — Full Documentation (English)

## Table of Contents

1. [Introduction](#introduction)
2. [Core Philosophy](#core-philosophy)
3. [Architecture](#architecture)
4. [The 5 Phases](#the-5-phases)
5. [Agents Reference](#agents-reference)
6. [Quality Gates](#quality-gates)
7. [LLM Compatibility](#llm-compatibility)
8. [Getting Started](#getting-started)
9. [FAQ](#faq)

---

## Introduction

MDAN is a structured method for AI-driven software development. It was designed to address the 
limitations of existing agentic development methods by introducing a clear separation between 
**orchestration** and **execution**, a **universal prompt standard** compatible with any LLM, and 
**enforced quality gates** that prevent common failure modes.

MDAN is not a framework, not a library, and not a tool. It is a **method** — a way of working 
with AI agents to build software systematically and reliably.

### Why MDAN?

Most agentic coding methods suffer from three problems:

1. **No structure** — Agents hallucinate tasks and skip steps when there's no enforced workflow
2. **LLM lock-in** — Methods designed for one LLM don't work well with others
3. **No quality enforcement** — There's no checkpoint between phases, so problems compound

MDAN solves all three:
- The 5-phase workflow with quality gates prevents skipping and compounding errors
- The Universal Envelope makes agents work identically across all major LLMs
- MDAN Core is the single orchestrator that maintains context and enforces quality

---

## Core Philosophy

### Orchestrate, Don't Execute

MDAN Core doesn't write code. It doesn't design interfaces. It thinks, plans, delegates, and validates. This separation ensures that each specialized agent can focus on its domain without losing the big picture.

### One Phase at a Time

Every phase must be fully completed and validated before the next begins. This is not a formality — it's the most important rule in MDAN. Skipping phases is the single most common cause of rework in software projects.

### Validate Before Progressing

Every phase ends with an explicit user validation. MDAN Core presents what was produced, highlights key decisions, and waits for "APPROVED" before moving forward. This keeps humans in control of the process.

### LLM-Agnostic by Design

MDAN was designed from day one to work with any LLM. The Universal Envelope standard ensures that agent prompts produce consistent outputs whether you're using Claude, GPT-4, Gemini, Qwen, or any other model.

---

## Architecture

### The 3-Layer Model

```
Layer 1: MDAN Core (Orchestrator)
         Thinks • Plans • Delegates • Validates
                      |
Layer 2: Specialized Agents
         Product | Architect | UX | Dev | Test | Security | DevOps | Doc
                      |
Layer 3: Artifacts
         PRD | Architecture | UX Spec | Code | Tests | Security Report | Pipeline | Docs
```

### Information Flow

All information flows through MDAN Core. Agents do not communicate with each other directly. This prevents:
- Conflicting decisions between agents
- Context loss across agent boundaries
- Circular dependencies

### The Universal Envelope

Every agent in MDAN is wrapped in the Universal Envelope — a standardized prompt structure that defines:
- The agent's identity and expertise
- Its capabilities and constraints
- Expected input format
- Required output format
- Quality self-check before submission
- Escalation conditions

See `core/universal-envelope.md` for the full specification.

---

## The 5 Phases

### Phase 1: DISCOVER
**Goal:** Deeply understand the problem before proposing any solution.  
**Agent:** Product Agent  
**Output:** Validated PRD  

The 5 Discovery Questions must be answered:
1. What is the core problem?
2. Who are the users?
3. How will success be measured?
4. What are the constraints?
5. What has already been tried?

### Phase 2: DESIGN
**Goal:** Architect the complete solution before writing code.  
**Agents:** Architect Agent, UX Agent  
**Output:** Architecture Document + UX Specification  

No code is written until DESIGN is complete. The architecture must cover: system design, tech stack, data models, API design, security architecture, and coding conventions. The UX spec must cover all screens with all states.

### Phase 3: BUILD
**Goal:** Implement with precision against the specifications.  
**Agents:** Dev Agent, Security Agent  
**Output:** Working, tested, security-reviewed code  

Each feature follows the BUILD loop: Feature Brief → Dev Agent → Security Review → Validation.

### Phase 4: VERIFY
**Goal:** Prove the software works correctly, securely, and completely.  
**Agents:** Test Agent, Security Agent  
**Output:** Complete test suite, security sign-off  

No feature is assumed to work. It must be proven with tests. All acceptance criteria must have corresponding test cases.

### Phase 5: SHIP
**Goal:** Deploy with confidence, document completely.  
**Agents:** DevOps Agent, Doc Agent  
**Output:** Live deployment, complete documentation  

Shipping means: live in production, monitored, documented, and with a runbook for incidents.

---

## Agents Reference

| Agent | Phase | Expertise | Key Output |
|-------|-------|-----------|------------|
| Product Agent | DISCOVER | Requirements, UX research | PRD |
| Architect Agent | DESIGN | System design, tech selection | Architecture Document |
| UX Agent | DESIGN | Interface design, accessibility | UX Specification |
| Dev Agent | BUILD | Implementation, code quality | Working code + tests |
| Security Agent | BUILD + VERIFY | Vulnerability analysis | Security Report |
| Test Agent | VERIFY | QA, test strategy | Test Plan + Suite |
| DevOps Agent | SHIP | CI/CD, infrastructure | Deployment pipeline |
| Doc Agent | SHIP | Technical writing | Documentation |

---

## Quality Gates

MDAN enforces quality gates between each phase. A gate is a checklist that must be fully satisfied before progression.

| Gate | From → To | Key Checks |
|------|-----------|------------|
| Gate 1 | DISCOVER → DESIGN | PRD complete, metrics defined, scope clear |
| Gate 2 | DESIGN → BUILD | Architecture complete, UX spec complete, both validated |
| Gate 3 | BUILD → VERIFY | All features implemented, security reviewed, no critical issues |
| Gate 4 | VERIFY → SHIP | All tests passing, security signed off, docs ready |

---

## LLM Compatibility

MDAN works with all major LLMs. The Universal Envelope adapts to each model's strengths.

| LLM | Recommended For | Notes |
|-----|----------------|-------|
| Claude | DISCOVER, DESIGN | Best at complex reasoning and structured output |
| GPT-4o | All phases | Excellent all-rounder |
| Gemini 1.5 Pro | Large projects | Very large context window |
| Qwen-Max | Asian market projects | Strong bilingual support |
| Kimi 128k | Long sessions | 128k context window |
| GLM-4 | Chinese-language projects | Native Chinese support |
| Cursor | BUILD | Best for in-IDE implementation |
| GitHub Copilot | BUILD | Best for inline code completion |

---

## Getting Started

### Option A: CLI (Recommended)

```bash
# Clone MDAN
git clone https://github.com/[your-username]/MDAN.git

# Initialize a project
bash MDAN/cli/mdan.sh init my-project

# Or with Python
python3 MDAN/cli/mdan.py init my-project
```

### Option B: Manual Setup

1. Clone the repository
2. Copy `core/orchestrator.md` as your LLM's system prompt
3. Choose your integration guide from `/integrations/`
4. Start with Phase 1: DISCOVER

### Option C: Cursor / Windsurf

1. Clone the repository
2. Run `mdan init my-project`
3. Open the project folder in Cursor or Windsurf
4. The `.cursorrules` / `.windsurfrules` file is pre-configured

---

## FAQ

**Q: Can I skip phases?**  
A: No. Phases exist to prevent compounding errors. Every phase skipped multiplies the rework needed later.

**Q: Can I use multiple LLMs in the same project?**  
A: Yes. MDAN is designed for this. Use Claude for DISCOVER/DESIGN, Cursor for BUILD, etc.

**Q: Do I need all 8 agents for every project?**  
A: For small projects, MDAN Core can be instructed to activate only relevant agents. A small CLI tool may not need the UX Agent, for example.

**Q: How do I handle a discovery that reveals the initial idea is wrong?**  
A: This is the purpose of DISCOVER. If the idea is wrong, MDAN Core documents it and iterates. A bad idea caught in DISCOVER costs minutes. The same idea caught in VERIFY costs days.

**Q: Can teams use MDAN?**  
A: Yes. Each team member can operate a specific agent, with MDAN Core coordinating via shared artifacts in version control.
