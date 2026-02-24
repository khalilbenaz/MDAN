# MDAN — Complete Documentation (English)

## Table of Contents

1. [Introduction](#introduction)
2. [Philosophy](#philosophy)
3. [Architecture](#architecture)
4. [The 5 Phases](#the-5-phases)
5. [Agent Reference](#agent-reference)
6. [Quality Gates](#quality-gates)
7. [LLM Compatibility](#llm-compatibility)
8. [Getting Started](#getting-started)
9. [FAQ](#faq)

---

## Introduction

MDAN is a structured method for AI-driven software development. It was designed to solve the limitations of existing agentic methods by introducing:

- A clear separation between **orchestration** and **execution**
- A **universal prompt standard** compatible with any LLM
- **Enforced quality gates** that prevent errors from compounding

MDAN is not a framework, library, or tool. It's a **method** — a way of working with AI agents to build software systematically and reliably.

### Why MDAN?

Most agent development methods suffer from three problems:

1. **No structure** — Agents invent tasks and skip steps without an enforced workflow
2. **LLM dependency** — Methods designed for one LLM work poorly with others
3. **No quality control** — There are no checkpoints between phases, problems accumulate

MDAN solves all three:
- The 5-phase workflow with quality gates prevents skipping and cumulative errors
- The Universal Envelope makes agents identical across all major LLMs
- MDAN Core is the single orchestrator that maintains context and enforces quality

---

## Philosophy

### Orchestrate, Don't Execute

MDAN Core doesn't write code. It doesn't design interfaces. It thinks, plans, delegates, and validates. This separation ensures each specialized agent can focus on their domain without losing the big picture.

### One Phase at a Time

Each phase must be fully completed and validated before moving to the next. This isn't a formality — it's the most important rule in MDAN. Skipping phases is the most common cause of rework in software projects.

### Validate Before Progressing

Each phase ends with explicit user validation. MDAN Core presents what was produced, highlights key decisions, and waits for an "APPROVED" before continuing. This keeps the human in control of the process.

### LLM-Agnostic by Design

MDAN was designed from day one to work with any LLM. The Universal Envelope standard ensures agent prompts produce consistent results whether you use Claude, GPT-4, Gemini, Qwen, or any other model.

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
          PRD | Architecture | UX Spec | Code | Tests | Security | Pipeline | Docs
```

### Information Flow

All information flows through MDAN Core. Agents don't communicate directly with each other. This avoids:
- Contradictory decisions between agents
- Context loss between agents
- Circular dependencies

### The Universal Envelope

Each agent in MDAN is wrapped in the Universal Envelope — a standardized prompt structure that defines:
- The agent's identity and expertise
- Its capabilities and constraints
- Expected input format
- Required output format
- Pre-submission quality self-check
- Escalation conditions

See `core/universal-envelope.md` for the full specification.

---

## The 5 Phases

### Phase 1: DISCOVER
**Goal:** Deeply understand the problem before proposing a solution.  
**Agent:** Product Agent  
**Result:** Validated PRD  

The 5 discovery questions must be answered:
1. What is the fundamental problem?
2. Who are the users?
3. How to measure success?
4. What are the constraints?
5. What has been tried before?

### Phase 2: DESIGN
**Goal:** Architect the complete solution before writing a single line of code.  
**Agents:** Architect Agent, UX Agent  
**Result:** Architecture document + UX Specification  

No code is written until DESIGN is complete. Architecture must cover: system design, tech stack, data models, API design, security architecture, and code conventions. UX spec must cover all screens with all states.

### Phase 3: BUILD
**Goal:** Implement precisely according to specifications.  
**Agents:** Dev Agent, Security Agent  
**Result:** Functional code, tested and security-reviewed  

Each feature follows the BUILD loop: Feature Brief → Dev Agent → Security Review → Validation.

### Phase 4: VERIFY
**Goal:** Prove the software works correctly, securely, and completely.  
**Agents:** Test Agent, Security Agent  
**Result:** Complete test suite, security approval  

No feature is assumed to work. It must be proven by tests. All acceptance criteria must have corresponding test cases.

### Phase 5: SHIP
**Goal:** Deploy with confidence, document completely.  
**Agents:** DevOps Agent, Doc Agent  
**Result:** Production deployment, complete documentation  

Shipping means: in production, monitored, documented, with a runbook for incidents.

---

## Agent Reference

| Agent | Phase | Expertise | Main Output |
|-------|-------|-----------|-------------|
| Learn Agent | All | Knowledge acquisition | Knowledge Capsules |
| Product Agent | DISCOVER | Requirements, UX research | PRD |
| Architect Agent | DESIGN | System design, tech choices | Architecture document |
| UX Agent | DESIGN | Interface design, accessibility | UX Specification |
| Dev Agent | BUILD | Implementation, code quality | Functional code + tests |
| Security Agent | BUILD + VERIFY | Vulnerability analysis | Security report |
| Test Agent | VERIFY | QA, test strategy | Test plan + suite |
| DevOps Agent | SHIP | CI/CD, infrastructure | Deployment pipeline |
| Doc Agent | SHIP | Technical writing | Documentation |

---

## Quality Gates

MDAN enforces quality gates between each phase. A gate is a checklist that must be fully satisfied before progressing.

| Gate | From → To | Key Checks |
|------|-----------|------------|
| Gate 1 | DISCOVER → DESIGN | Complete PRD, defined metrics, clear scope |
| Gate 2 | DESIGN → BUILD | Complete architecture, complete UX spec, both validated |
| Gate 3 | BUILD → VERIFY | All features implemented, security reviewed |
| Gate 4 | VERIFY → SHIP | All tests passing, security approved, docs ready |

---

## LLM Compatibility

MDAN works with all major LLMs. The Universal Envelope adapts to each model's strengths.

| LLM | Recommended For | Notes |
|-----|-----------------|-------|
| Claude | DISCOVER, DESIGN | Excellent for complex reasoning and structured outputs |
| GPT-4o | All phases | Very good in all areas |
| Gemini 1.5 Pro | Large projects | Very large context window |
| Qwen-Max | Asian market projects | Strong bilingual support |
| Kimi 128k | Long sessions | 128k context window |
| GLM-4 | Chinese projects | Native Chinese support |
| Cursor | BUILD | Best for in-IDE implementation |
| GitHub Copilot | BUILD | Best for inline code completion |

---

## Getting Started

### Step 1: Clone MDAN

```bash
git clone https://github.com/khalilbenaz/MDAN.git
cd MDAN
```

### Step 2: Initialize Your Project

```bash
# With Bash
bash cli/mdan.sh init my-project

# Or with Python
python3 cli/mdan.py init my-project
```

This creates a `my-project/` folder ready to use with:
- `.mdan/` — MDAN files (orchestrator, agents)
- `.cursorrules` — Cursor configuration
- `.windsurfrules` — Windsurf configuration
- `.github/copilot-instructions.md` — Copilot configuration
- `docs/` — Templates (PRD, Architecture, etc.)

### Step 3: Use with Your LLM

#### Claude / ChatGPT / Gemini (Web)

1. Copy the content of `my-project/.mdan/orchestrator.md`
2. Paste it as a system prompt (or first message)
3. Start with: `MDAN: I want to build...`

#### Cursor IDE

```bash
cursor my-project   # .cursorrules is already configured
```

#### Windsurf IDE

```bash
windsurf my-project   # .windsurfrules is already configured
```

### Step 4: Follow the Workflow

MDAN guides you through the 5 phases. Validate each phase before moving to the next.

---

## FAQ

**Q: Can phases be skipped?**  
A: No. Phases exist to avoid cumulative errors. Each skipped phase multiplies the rework needed later.

**Q: Can multiple LLMs be used in the same project?**  
A: Yes. MDAN is designed for this. Use Claude for DISCOVER/DESIGN, Cursor for BUILD, etc.

**Q: Are all 9 agents needed for every project?**  
A: No. MDAN Core automatically detects the project profile and adapts the agents used. A MICRO project will only use 2-3 agents.

**Q: How to resume a project after a break?**  
A: Use `MDAN RESUME SESSION` with the content of the MDAN-STATE.json file. MDAN Core reconstructs all context.

**Q: How to add custom skills?**  
A: Use the Learn Agent: `bash cli/mdan.sh learn --rules .cursorrules` or `--skill ./my-conventions.md`
