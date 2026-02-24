# MDAN Integration — Claude (Anthropic)

## Setup

Claude is the reference implementation for MDAN. It handles the Universal Envelope natively.

### Option 1: claude.ai (Web/App)

1. Open a new Claude conversation
2. Start your message with the content of `core/orchestrator.md`
3. Optionally add the relevant agent prompts for your current phase
4. Begin your project

### Option 2: API / Custom Claude App

```python
import anthropic

with open("core/orchestrator.md") as f:
    system_prompt = f.read()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=8096,
    system=system_prompt,
    messages=[
        {"role": "user", "content": "I want to build [your project idea]"}
    ]
)
```

### Option 3: Claude Projects

1. Create a new Claude Project
2. In Project Instructions, paste the content of `core/orchestrator.md`
3. Upload relevant agent files to Project Knowledge
4. Start new conversations within the project

## Tips for Claude

- Claude handles XML-style `[MDAN-AGENT]` tags natively — use them as-is
- For long projects, use Claude Projects to maintain context
- Claude responds well to "DESIGN APPROVED" / "PRD APPROVED" validation phrases
- Use extended thinking (if available) for complex architecture decisions
