# Reference: CLI

`mdan <command> [options]`, `mdan --version`, `mdan --help` (or no arguments) lists every command. `mdan <command> --help` prints the command's own usage. Generated from `tools/cli/index.js` and each `tools/cli/commands/*.js` — run `--help` yourself if in doubt, it's the ground truth.

## `mdan install [dir]`

Installs MDAN (agents, wizards, IDE commands) into a project (default: current directory).

| Flag | Values | Default |
|------|--------|---------|
| `--lang <l>` | `fr-darija` \| `fr` \| `en` \| `darija` | `fr-darija` |
| `--ide <list>` | comma-separated: `claude-code`, `cursor`, `opencode`, `gemini`, `qwen` | `claude-code` |
| `--modules <list>` | comma-separated optional packs: `db-optimization`, `devops-azure`, `ecosystem`, `fintech`, `payments-ma`, `qa` \| `all` \| `none` | `none` |
| `--user <name>` | your name, used by the agents | OS user |
| `--scale <s>` | `auto` \| `solo` \| `team` \| `enterprise` — quality-gate strictness | `auto` |
| `--mcp` | add the MDAN MCP server to `.mcp.json` | off |
| `--force` | overwrite files you modified (default: write `<file>.mdan-new` next to them) | off |
| `-y`, `--yes` | non-interactive, accept defaults | off |

Without `-y` on a TTY, prompts interactively for language, modules, IDEs, name and MCP.

## `mdan update [dir] [--channel latest|next|<version>]`

Re-installs with the options recorded from the existing install (see `install`'s flags — any of them overrides the recorded value). `--channel` delegates to another published version's installer (`npx mdan-method@<channel> update`). See [Update and channels](../how-to/update-and-channels.md).

## `mdan status [--json]`

Where the project is: current workflow and step, completed phases, artifacts, decisions, recommended next step.

## `mdan memory`

```
mdan memory                       List agents with memories
mdan memory <agent> [query]       Show an agent's memories
mdan memory <agent> --forget <id> Delete a memory
```

## `mdan check [artifact.md ...] [--scale solo|team|enterprise] [--json]`

Quality gate on planning artifacts. Exit code `1` on FAIL (usable in CI). Without paths, checks the artifacts registered in the project state, falling back to `docs/`.

## `mdan trace [--graph] [--json]`

Requirement (FR/NFR) → stories → tests matrix. `--graph` also writes requirement/story/test nodes and edges into the context graph. Exit code `1` on FAIL.

## `mdan scope "<change description>" [--files a.js,b.js] [--artifacts prd,architecture] [--json]`

Recommends `oneshot` (quick-dev), `spec` (quick-spec) or full planning, from risk terms in the description, file count, and the real downstream impact of the named artifacts in the context graph.

## `mdan bundle [agent ...] [--all] [--out dist/bundles] [--lang "<language>"]`

Builds web bundles (instructions + knowledge file) for ChatGPT custom GPTs, Gemini Gems or Claude Projects. Without agents: `mdan-master`. `--all`: every installed agent. See [Web bundles](../how-to/web-bundles.md).

## `mdan export --to <csv|github|ado|jira> [options] [--apply]`

Exports the epics/stories document. Dry run by default: prints the planned requests; `--apply` sends them. Re-runs update the items already exported (ids kept in `_mdan/state/export-<target>.json`).

| Flag | Meaning |
|------|---------|
| `--file <epics.md>` | epics document (default: from the project state / `docs/`) |
| `--out <file.csv>` | csv target: output file (default: stdout) |
| `--repo <owner/name>` | github (token: `GITHUB_TOKEN` or `GH_TOKEN`) |
| `--org <org> --project <p>` | ado (token: `AZURE_DEVOPS_PAT`) |
| `--url <https://x.atlassian.net> --project <KEY>` | jira (`JIRA_EMAIL` + `JIRA_API_TOKEN`) |

See [Export the backlog](../how-to/export-backlog.md).

## `mdan serve [--http] [--port 3100] [--host 127.0.0.1]`

Starts the MDAN MCP server. Default transport is stdio.

| Flag | Meaning |
|------|---------|
| `--http` | Streamable HTTP transport on `/mcp` (health check on `/health`) |
| `--sse` | Deprecated alias of `--http` |
| `--port <n>` | HTTP port (default 3100, or `$PORT`) |
| `--host <h>` | HTTP bind address (default 127.0.0.1, or `$HOST`) |
| `--token <t>` | Require `Authorization: Bearer <t>` (or `$MDAN_HTTP_TOKEN`); mandatory off loopback |
| `--insecure` | Allow a non-loopback bind without a token |

## `mdan graph [--json | --html <file>] [--since <node-id>]`

Prints the context graph as Mermaid (default), raw JSON, or writes a standalone HTML page. `--since` highlights a node (e.g. a decision record) and everything downstream of it.

## `mdan impact <artifact-id>`

Upstream dependencies and downstream impact of an artifact in the context graph.

## `mdan stale [--touch <id>]`

Lists artifacts modified since they were registered and the downstream artifacts to review. `--touch <id>` marks an artifact as reviewed (records its current hash). Exit code `2` if anything is stale.

## `mdan validate`

Checks that every `{project-root}/...` and relative step reference in `_mdan` resolves to an existing file.

## `mdan serve`, MCP tools, prompts, resources

See the [MCP reference](mcp.md).
