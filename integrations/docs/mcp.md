# MDAN MCP Integration

> Configure Model Context Protocol for MDAN with your IDE

## Overview

MDAN supports MCP (Model Context Protocol) to provide your coding assistant (Cursor, Claude Code, Windsurf) with deep understanding of MDAN workflows, agents, and best practices.

## Quick Start

### 1. Generate MCP Config

```bash
# In your MDAN project
mdan mcp init
```

This creates `.mcp.json` in your project root.

### 2. Configure Your IDE

#### Cursor
1. Open Cursor Settings → Features → Models
2. MCP should auto-detect `.mcp.json`
3. Or manually add via: Settings → Developer → Edit MCP Config

#### Claude Code
```bash
claude mcp add mdan --project path/to/your/project
```

#### Windsurf
MCP configs are auto-discovered from `.mcp.json` in project root.

## Configuration

### .mcp.json Structure

```json
{
  "mcpServers": {
    "mdan-memory": { ... }
  },
  "capabilities": {
    "scenarios": {
      "enabled": true,
      "test_paths": ["tests/scenarios/"]
    },
    "evaluations": {
      "enabled": true,
      "eval_paths": ["tests/evaluations/"]
    }
  },
  "agent_prompts": {
    "dev": "templates/prompts/dev-agent.yaml"
  }
}
```

## Available MCP Tools

### mdan-state

Read/write MDAN project state.

```typescript
// Read current state
const state = await mdan_state({ action: "read" });

// Write state
await mdan_state({ action: "write", data: { phase: "BUILD", progress: 50 } });
```

### mdan-agents

List available MDAN agents.

```typescript
const agents = await mdan_agents();
```

### mdan-phases

Get phase information.

```typescript
const phase = await mdan_phases({ name: "VERIFY" });
```

## IDE Integration Examples

### Cursor Rules Auto-Generation

When you run `mdan init` or `mdan attach`, MDAN automatically generates:

- `.cursorrules` - Cursor-specific instructions
- `.windsurfrules` - Windsurf-specific instructions
- `.github/copilot-instructions.md` - Copilot instructions

### Agent Context

MCP provides your IDE with access to:

1. **Agent prompts** - Full agent definitions for context
2. **Phase workflows** - Current phase and next steps
3. **Quality gates** - What's required to pass
4. **Test templates** - Scenario and evaluation paths

## Troubleshooting

### MCP not detected

1. Check `.mcp.json` is valid JSON
2. Restart your IDE
3. Check IDE MCP documentation

### Tools not available

1. Verify MCP server is running
2. Check console for errors
3. Try regenerating config: `mdan mcp init --force`

## Commands

```bash
mdan mcp init          # Generate MCP config
mdan mcp validate      # Validate config
mdan mcp list          # Show available tools
mdan mcp update        # Update to latest version
```

## Framework Support

| IDE | MCP Support | Auto-detect |
|-----|--------------|-------------|
| Cursor | ✅ Full | ✅ |
| Claude Code | ✅ Full | ✅ |
| Windsurf | ✅ Full | ✅ |
| VS Code | ✅ Via extension | Manual |

## Integration with Better Agents

MDAN's MCP config is compatible with Better Agents:

- Scenarios in `tests/scenarios/` are auto-discovered
- Evaluations in `tests/evaluations/` are available
- Prompts from `templates/prompts/` are versioned

This allows you to use Better Agents CLI alongside MDAN:

```bash
npx @langwatch/better-agents test --scenarios tests/scenarios/
```
