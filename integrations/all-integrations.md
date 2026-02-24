# MDAN Integration — ChatGPT / OpenAI

## Setup

### GPT-4o / GPT-4 (Web)

1. Go to chat.openai.com
2. Start a new conversation
3. Paste the content of `core/orchestrator.md` as your first message, prefixed with:
   ```
   Please adopt the following role and follow these instructions for our entire conversation:
   
   [paste orchestrator.md content here]
   ```

### Custom GPT

1. Go to GPT Builder
2. In "Instructions", paste `core/orchestrator.md`
3. Upload agent files as knowledge files
4. Name your GPT "MDAN Core"

### API

```python
from openai import OpenAI

with open("core/orchestrator.md") as f:
    system_prompt = f.read()

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "I want to build [your project idea]"}
    ]
)
```

## Notes for ChatGPT

- Replace `[MDAN-AGENT]` XML tags with `## MDAN AGENT` markdown headers if tags cause issues
- GPT-4o handles the full Universal Envelope well
- For long projects, use Projects (ChatGPT Plus) to maintain context

---

# MDAN Integration — Google Gemini

## Setup

### Gemini (Web)

Gemini works best with markdown-formatted prompts. Convert the orchestrator to markdown:

```
# MDAN Core — Orchestrator

You are MDAN Core, the central orchestrator...
[rest of orchestrator.md, with [MDAN-AGENT] blocks replaced by ## headers]
```

### Gemini API

```python
import google.generativeai as genai

with open("core/orchestrator.md") as f:
    system_prompt = f.read()

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_prompt
)
chat = model.start_chat()
response = chat.send_message("I want to build [your project idea]")
```

## Notes for Gemini

- Gemini handles markdown well; prefer `## Headers` over XML-style tags
- Gemini 1.5 Pro has a very large context window — excellent for long MDAN sessions
- Use Gemini Advanced for best results

---

# MDAN Integration — Alibaba Qwen

## Setup

### Qwen Web (Tongyi)

1. Go to tongyi.aliyun.com
2. Paste the orchestrator prompt as the first message
3. Qwen handles structured prompts well

### Qwen API

```python
from openai import OpenAI  # Qwen uses OpenAI-compatible API

with open("core/orchestrator.md") as f:
    system_prompt = f.read()

client = OpenAI(
    api_key="YOUR_DASHSCOPE_KEY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
response = client.chat.completions.create(
    model="qwen-max",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "I want to build [your project idea]"}
    ]
)
```

## Notes for Qwen

- Qwen supports the Universal Envelope as-is
- Qwen-Max gives best results for complex orchestration
- Chinese language support is native — useful for Chinese-language projects

---

# MDAN Integration — Moonshot Kimi

## Setup

### Kimi API

```python
from openai import OpenAI

with open("core/orchestrator.md") as f:
    system_prompt = f.read()

client = OpenAI(
    api_key="YOUR_KIMI_KEY",
    base_url="https://api.moonshot.cn/v1"
)
response = client.chat.completions.create(
    model="moonshot-v1-128k",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "I want to build [your project idea]"}
    ]
)
```

## Notes for Kimi

- Kimi's 128k context window makes it excellent for full project sessions
- Use markdown headers over XML tags for best compatibility
- Moonshot-v1-128k is recommended for MDAN due to large context support

---

# MDAN Integration — Zhipu GLM

## Setup

### GLM API

```python
from zhipuai import ZhipuAI

with open("core/orchestrator.md") as f:
    system_prompt = f.read()

client = ZhipuAI(api_key="YOUR_API_KEY")
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "I want to build [your project idea]"}
    ]
)
```

## Notes for GLM

- GLM-4 handles structured prompts well
- Use markdown formatting for best results
- GLM is particularly strong for Chinese-language software projects

---

# MDAN Integration — MiniMax

## Setup

### MiniMax API

```python
import requests

with open("core/orchestrator.md") as f:
    system_prompt = f.read()

response = requests.post(
    "https://api.minimax.chat/v1/text/chatcompletion_v2",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "abab6.5s-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "I want to build [your project idea]"}
        ]
    }
)
```

## Notes for MiniMax

- MiniMax handles the Universal Envelope well
- Use structured markdown for agent prompts

---

# MDAN Integration — Opencode

## Setup

Opencode is a terminal-based AI coding tool. MDAN integrates via its system prompt configuration.

### Configuration

```bash
# In your project root, create opencode.json
cat > opencode.json << 'EOF'
{
  "system": "$(cat core/orchestrator.md)"
}
EOF
```

Or set via environment:

```bash
export OPENCODE_SYSTEM="$(cat core/orchestrator.md)"
opencode
```

### Usage

```bash
# Start MDAN session
opencode "I want to build [your project idea]"

# Reference agent prompts
opencode "@file mdan/agents/dev.md Implement the user authentication feature"
```

## Notes for Opencode

- Opencode excels in the BUILD phase — it can directly edit files
- Use MDAN feature briefs as opencode tasks
- Place agent files in `mdan/agents/` for easy reference

---

# MDAN Integration — GitHub Copilot

## Setup

GitHub Copilot supports workspace instructions via `.github/copilot-instructions.md`.

### Step 1: Create workspace instructions

```bash
mkdir -p .github
cat core/orchestrator.md > .github/copilot-instructions.md
```

### Step 2: Activate in VS Code

1. Open VS Code with GitHub Copilot extension
2. Open Copilot Chat (Ctrl+Shift+I)
3. The workspace instructions are automatically loaded

### Step 3: Use MDAN phases

```
@workspace MDAN Phase 1: I want to build [your project idea]
```

## Limitations with GitHub Copilot

- Copilot Chat has a shorter context window than dedicated LLM APIs
- Orchestration is more limited than with Claude or GPT-4
- Best used for the BUILD phase with pre-written architecture docs
- Use `@workspace` to give Copilot context from your codebase

## Recommended Usage

Use Copilot primarily for the BUILD phase — once the architecture and PRD are written 
(using Claude, GPT-4, or Gemini), Copilot excels at implementing features directly in your IDE.
