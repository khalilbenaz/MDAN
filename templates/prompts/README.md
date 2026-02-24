# Prompts Versioning Index

> Version-controlled prompts for MDAN agents

## Overview

Prompts are versioned using YAML files for better collaboration, tracking, and rollback capabilities.

## Available Prompts

| Prompt | Version | Agent |
|--------|---------|-------|
| [orchestrator.yaml](prompts/orchestrator.yaml) | 2.2.0 | MDAN Core |
| [dev-agent.yaml](prompts/dev-agent.yaml) | 2.0.0 | Haytame (Dev) |
| [product-agent.yaml](prompts/product-agent.yaml) | 2.0.0 | Khalil (Product) |
| [architect-agent.yaml](prompts/architect-agent.yaml) | 2.0.0 | Reda (Architect) |
| [test-agent.yaml](prompts/test-agent.yaml) | 2.0.0 | Youssef (Test) |

## Prompt Format

Each prompt file follows this structure:

```yaml
handle: agent-handle
scope: PROJECT  # or GLOBAL
model: openai/gpt-4o
version: 1.0.0
last_updated: "2026-02-24"
maintainer: username

description: Brief description

system_prompt: |
  Full prompt content with:
  - Role definition
  - Capabilities
  - Constraints
  - Output format

capabilities:
  - Capability 1
  - Capability 2

constraints:
  - Constraint 1
  - Constraint 2

changelog:
  - version: 1.0.0
    date: "2026-02-24"
    changes:
      - Change 1
      - Change 2
```

## Using Prompts

### CLI Commands

```bash
# List all prompts
mdan prompt list

# Show specific prompt
mdan prompt show orchestrator

# Compare versions
mdan prompt diff orchestrator 2.1.0 2.2.0

# Rollback prompt
mdan prompt rollback orchestrator 2.1.0
```

### Integration with IDE

Prompts are synced to:
- `.claude/skills/` - For Claude/Cursor
- `.windsurfrules` - For Windsurf
- `.github/copilot-instructions.md` - For Copilot

## Registry

The `prompts.json` file tracks all prompts:

```json
{
  "prompts": {
    "orchestrator": {
      "version": "2.2.0",
      "active": true
    }
  }
}
```

## Best Practices

1. **Version bump on any change** - Even small tweaks warrant a version bump
2. **Document changes** - Always add changelog entries
3. **Test prompts** - Validate prompts before releasing
4. **Use semantic versioning** - MAJOR for breaking, MINOR for features, PATCH for fixes

## Adding New Prompts

1. Create YAML file in `templates/prompts/`
2. Add entry to `prompts.json`
3. Update registry version
4. Commit with descriptive message
