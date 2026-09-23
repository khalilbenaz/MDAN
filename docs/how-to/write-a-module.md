# How to: write a module (agent or workflow)

`_mdan/` is the single source of truth. Everything else — the CSV manifests in `_mdan/_config/`, the `.claude/commands/mdan-*.md` slash commands, the generated sections of `README.md`/`README.en.md` — is derived from it by `npm run build` (`tools/build/build.js`, via `tools/lib/sources.js`). Never hand-edit a generated file; it will be overwritten and CI's `build:check` will flag the drift.

## Module layout

```
_mdan/<module>/
├── agents/            *.md — one file per agent
├── workflows/          wizard.md / workflow.yaml / workflow-*.md, in subfolders (steps/, templates/, data/)
├── tasks/              *.xml or *.md — standalone tasks (optional)
├── teams/              *.csv — party-mode team rosters (mdan module only)
└── config.yaml         module config written at install
```

To add a brand-new module (a new pack like `qa` or `payments-ma`), just create the folder under `_mdan/<name>/` with this layout — `modulesOf()` (`tools/lib/sources.js`) discovers modules by directory, no registry to update. Add it to `install.js`'s optional-module list automatically happens too (`optionalModules()` reads the same directory listing).

## Adding an agent

Create `_mdan/<module>/agents/<name>.md`. It needs two things:

1. A frontmatter block (used by IDE-native subagent formats):
   ```yaml
   ---
   name: "my-agent"
   description: "One-line role"
   ---
   ```
2. An `<agent>` XML tag MDAN's own parser reads — this is what actually populates the manifest and the README table:
   ```xml
   <agent id="my-agent.agent.yaml" name="Persona Name" title="Role Title" icon="🔧" capabilities="…">
   <role>What this agent is responsible for.</role>
   <identity>Who they are, their background.</identity>
   <communication_style>How they talk.</communication_style>
   <principles>Their guiding principles.</principles>
   <activation critical="MANDATORY">
     ...
   </activation>
   ...menu, handlers, etc. — copy the structure of an existing agent in the same module...
   </agent>
   ```

The display name (`displayName`, from the tag's `name` attribute) must be unique across **all** agents in every module — `npm run build` / `npm test` enforce it. If the agent joins the default party-mode roster, add it to `_mdan/mdan/teams/default-party.csv`; CI checks every listed member resolves to a real agent file.

## Adding a workflow

Create `_mdan/<module>/workflows/<name>/wizard.md` (step-by-step, free-form) or `workflow.yaml` (structured, driven by `_mdan/core/tasks/workflow.xml`). Either way it needs frontmatter (wizard.md) or top-level YAML scalars (workflow.yaml):

```yaml
---
name: "my-workflow"
description: "What it does. Use when the user says \"...\"."
---
```

`workflow.name` must be unique across the whole project. The `description` is what an MCP client sees for `mdan_list_workflows` and as the prompt description — write it as you would a tool description, including trigger phrases ("Use when the user says…"), since some clients route on it.

Split a step-heavy wizard into a `steps/` (or `<name>-steps/`) subfolder — `readWorkflows()` doesn't recurse into `steps/`, `templates/`, or `steps`-suffixed folders looking for more top-level workflows, so you can nest freely without accidentally registering a step file as its own workflow.

## Adding a task

Standalone tasks (`/mdan-shard-doc`, `/mdan-help`, …) live in `_mdan/<module>/tasks/`, either `.xml` (`<task name="…" description="…">`, skipped if `internal="true"`) or `.md` (frontmatter `name`/`description`).

## After editing content

```bash
npm run build       # regenerate manifests, .claude/commands/, README generated sections
npm run validate     # every {project-root}/... reference in _mdan resolves to a real file
npm run lint
npm test             # unique names, party team validity, no BMAD leftovers, generated files up to date
```

or all at once: `npm run check` (what CI runs). If you only want to know whether generated output is stale without writing it, `npm run build:check`.

## Evaluating a wizard end to end

If your change touches a wizard's flow, `tools/eval/` runs it against a scripted user persona with an LLM and checks the resulting document with `mdan check` plus content assertions:

```bash
ANTHROPIC_API_KEY=... npm run eval
```

See the scenarios under `tools/eval/scenarios/` for the format.
