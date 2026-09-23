# MDAN documentation

Docs are organized by what you're trying to do ([Diátaxis](https://diataxis.fr/)): learn by doing, solve a specific problem, look up a fact, or understand how something works.

## Tutorials — learning by doing

- [Your first project](tutorials/first-project.md) — from `npx mdan-method install` to a shipped story, walking every phase: brief → PRD → architecture → epics → sprint → dev-story → code-review.

## How-to guides — solving a specific problem

- [Use MDAN with MCP clients](how-to/use-with-mcp-clients.md) — Claude Code, Claude Desktop, Cursor; stdio and authenticated HTTP.
- [Customize an agent](how-to/customize-agents.md) — shipped / team / personal layers, `mdan_customize_agent`.
- [Export the backlog to a tracker](how-to/export-backlog.md) — CSV, GitHub Issues, Azure DevOps, Jira; dry run, env vars, idempotency.
- [Build web bundles](how-to/web-bundles.md) — ChatGPT GPTs, Gemini Gems, Claude Projects.
- [Wire quality gates into CI](how-to/quality-gates-in-ci.md) — `mdan check` / `mdan trace` exit codes, GitHub Actions and Azure DevOps examples.
- [Update and release channels](how-to/update-and-channels.md) — `mdan update`, `--channel next`, conflict resolution.
- [Write a module](how-to/write-a-module.md) — add an agent or workflow, file layout, frontmatter, `npm run build`, `mdan validate`, tests.

## Reference — looking things up

- [CLI](reference/cli.md) — every `mdan` command and flag.
- [MCP server](reference/mcp.md) — every tool, prompt and resource, with inputs.
- [Modules](reference/modules.md) — every module with its agents and workflows.
- [Configuration](reference/config.md) — `config.yaml` keys, state and custom files.

## Explanation — understanding the design

- [Concepts](explanation/concepts.md) — wizards, agents, context graph, state/resume, memory sidecars, scale-adaptive routing, quality gates, decision records.
- [MDAN vs MDAN-METHOD](explanation/mdan-vs-mdan.md) — an honest comparison with MDAN-METHOD v6.12.

---

French speakers: the main [README.md](../README.md) covers the same ground in French and is the canonical quick-start.
