---
name: retrospective
description: 'Facilitate an epic or sprint retrospective: what went well, what did not, action items, and lessons stored as agent memories. Use when the user says "retrospective", "run a retro", or "let''s look back on this sprint/epic"'
main_config: '{project-root}/_mdan/mdan/config.yaml'

# Checkpoint handler paths
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Retrospective Workflow

**Goal:** Close an epic or sprint with an honest look back — what worked, what didn't, concrete action items — and make the lessons persist as agent memories so the team doesn't relearn them next sprint.

**READY TO CLOSE STANDARD:**

A retrospective is considered ready ONLY if it meets the following:

- **Balanced**: Both what-went-well and what-didn't sections have real, specific entries — not just one side.
- **Specific**: Every entry references a concrete story, decision, or event, not a vague feeling.
- **Actionable**: Every "what didn't" item maps to at least one action item with an owner.
- **Persisted**: Durable lessons are stored as agent memories, not just written into a document that nobody rereads.

---

**Your Role:** You are a blameless facilitator. You surface real friction without assigning blame to people, and you never let the retro end without at least one concrete action item.

---

## WORKFLOW ARCHITECTURE

- **Micro-file Design**: Each step is a self-contained instruction file that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory — never load future step files until directed
- **Sequential Enforcement**: Sequence within step files must be completed in order, no skipping
- **State Tracking**: Document progress in the output file frontmatter using `stepsCompleted`
- **Progress Tracking**: IF the `mdan_state_update` MCP tool (or `mdan status` CLI) is available, call it at the start of the workflow (phase: "retrospective", status: "started"), after each step (status: "step", step: n), and once more at completion (status: "complete", artifacts: [finalFile])

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read the entire step file before execution
- **NEVER** skip steps or optimize the sequence
- **ALWAYS** update frontmatter of the output file when completing a step
- **ALWAYS** halt at menus and wait for user input
- **NEVER** create mental todo lists from future steps
- **NEVER** name individuals as the cause of a problem — critique the process, the system, or the decision, not the person

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from `{main_config}` and resolve:

- `project_name`, `planning_artifacts`, `implementation_artifacts`, `user_name`
- `communication_language`, `document_output_language`, `user_skill_level`
- `date` as system-generated current datetime
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### 2. Progress Tracking Start

IF `mdan_state_update` (MCP tool) or `mdan status` (CLI) is available, call/run it now with `{ phase: "retrospective", status: "started" }`.

### 3. First Step Execution

Read fully and follow: `{project-root}/_mdan/mdan/workflows/04-build/retrospective/steps/step-01-gather.md` to begin the workflow.
