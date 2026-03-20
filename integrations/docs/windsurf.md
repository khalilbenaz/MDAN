# MDAN Integration — Windsurf IDE

## Setup

Windsurf uses `.windsurfrules` for persistent AI instructions.

### Step 1: Create `.windsurfrules`

```bash
cp core/orchestrator.md .windsurfrules
```

Then append at the end:

```
## WINDSURF-SPECIFIC INSTRUCTIONS

You are operating inside Windsurf IDE with Cascade AI.

- Cascade can autonomously execute multi-step coding tasks
- Use MDAN phases to structure Cascade's work
- When activating the Dev Agent, Cascade will implement and write files directly
- Use Cascade's flow awareness to maintain MDAN phase context across sessions

### File Organization
All MDAN artifacts should be saved to `mdan/artifacts/` for reference.
```

### Step 2: Copy agents

```bash
mkdir -p mdan/agents mdan/artifacts
cp agents/*.md mdan/agents/
```

### Step 3: Using MDAN with Cascade

Cascade's multi-step reasoning pairs well with MDAN's structured phases. When starting a phase:

```
@MDAN Phase 2: DESIGN — activate Architect Agent for [project name]
```

## Tips for Windsurf

- Windsurf's Cascade is excellent for the BUILD phase — it can implement entire features autonomously
- Use MDAN's Feature Briefs as Cascade tasks for predictable, structured implementation
- Save architecture documents to `mdan/artifacts/` so Cascade can reference them in context
