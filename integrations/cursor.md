# MDAN Integration — Cursor IDE

## Setup

Cursor uses `.cursorrules` for persistent AI instructions at the project level.

### Step 1: Create `.cursorrules`

Copy `core/orchestrator.md` content into a `.cursorrules` file at your project root, then add:

```
## CURSOR-SPECIFIC INSTRUCTIONS

You are operating inside Cursor IDE. In addition to your MDAN orchestration role:

- You have access to the full codebase via @codebase
- You can read and write files directly
- Use @file to reference specific files when activating agents
- When the Dev Agent produces code, write it directly to the appropriate files
- When the Doc Agent produces documentation, write it to the mdan_output/ folder

### Agent File References
- Product Agent: @file mdan/agents/product.md
- Architect Agent: @file mdan/agents/architect.md
- UX Agent: @file mdan/agents/ux.md
- Dev Agent: @file mdan/agents/dev.md
- Test Agent: @file mdan/agents/test.md
- Security Agent: @file mdan/agents/security.md
- DevOps Agent: @file mdan/agents/devops.md
- Doc Agent: @file mdan/agents/doc.md
```

### Step 2: Copy agents to project

```bash
mkdir -p mdan/agents
cp agents/*.md mdan/agents/
```

### Step 3: Start using MDAN in Cursor

Open Cursor Chat (Cmd+L) and type:
```
MDAN: I want to build [your project idea]
```

## Cursor-Specific Features

### Composer Mode (Recommended)
Use Composer (Cmd+I) for BUILD phase — it can write multiple files simultaneously when the Dev Agent produces code.

### Agent Mode
Enable Agent mode for autonomous implementation. MDAN Core will orchestrate, and Cursor's agent will execute file operations.

### @references
- `@codebase` — Give MDAN Core full project context
- `@file path/to/file` — Reference specific files for agent review
- `@docs` — Reference documentation

## Example `.cursorrules` file structure

```
.cursorrules          ← MDAN Core orchestrator prompt
mdan/
  agents/
    product.md
    architect.md
    ux.md
    dev.md
    test.md
    security.md
    devops.md
    doc.md
```
