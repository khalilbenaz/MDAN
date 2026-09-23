# How to: build web bundles

Web bundles package an MDAN agent for a chat product with no file system and no IDE — a ChatGPT custom GPT, a Gemini Gem, or a Claude Project. There's no MCP and no local files there, so the agent, its rules and every workflow its menu can reach get flattened into two files:

```bash
mdan bundle                          # mdan-master only, to dist/bundles/
mdan bundle architect pm             # specific agents
mdan bundle --all                    # every installed agent
mdan bundle --all --out dist/bundles --lang "English"
```

For each agent you get:

- **`<agent>.instructions.md`** — the system prompt: identity, role, communication style, principles, menu summary. Kept under ~8000 characters (ChatGPT's custom-instructions limit); truncated with a marker if the persona text runs long.
- **`<agent>.knowledge.md`** — the knowledge file: `_mdan/core/rules.md`, the agent's own definition, and every workflow file its menu references (`exec="{project-root}/…"` / `workflow="{project-root}/…"`), each as a section titled `## FILE: <path>`. A reference to `{project-root}/<path>` inside the text means "the section titled `<path>`".

## Setup per platform

- **ChatGPT (custom GPT)**: paste `instructions.md` into the GPT's Instructions field; upload `knowledge.md` as a Knowledge file.
- **Gemini (Gem)**: paste `instructions.md` into the Gem's instructions; attach `knowledge.md` as a knowledge source.
- **Claude (Project)**: paste `instructions.md` into the Project's custom instructions; add `knowledge.md` to Project knowledge.

Since these platforms can't run `mdan_state_update` or write to a context graph, the bundle tells the agent to produce every document inline in the chat and tell the user where to save it, instead of writing files.

## Language

`--lang "<language>"` forces the agent to always answer in that language, overriding the language rules normally loaded from `_mdan/core/rules.md` (which the bundled agent can't dynamically resolve the way an MCP-connected one can).
