# How to: use MDAN with MCP clients

MDAN's tools, prompts and resources work with any [MCP](https://modelcontextprotocol.io/) client. `mdan install --mcp` writes the config below into `.mcp.json` for you; this page covers doing it by hand and per-client notes.

## Claude Code

`mdan install --mcp` (or manually) writes to `.mcp.json` at the project root:

```json
{
  "mcpServers": {
    "mdan": {
      "command": "npx",
      "args": ["-y", "mdan-method", "serve"],
      "env": { "MDAN_PROJECT_ROOT": "." }
    }
  }
}
```

Claude Code picks this up automatically for the project. Workflows and agents also appear as slash commands (`/mdan-*`) because every workflow/agent is registered as an MCP prompt.

## Claude Desktop

Claude Desktop reads its own config file (`claude_desktop_config.json`, platform-specific path). Add the same `mcpServers.mdan` block, with an absolute path in `MDAN_PROJECT_ROOT` since Desktop does not run from your project directory:

```json
{
  "mcpServers": {
    "mdan": {
      "command": "npx",
      "args": ["-y", "mdan-method", "serve"],
      "env": { "MDAN_PROJECT_ROOT": "/absolute/path/to/your/project" }
    }
  }
}
```

## Cursor

Cursor reads `.cursor/mcp.json` (project) or its global settings, same `mcpServers.mdan` shape as above.

## Without a project install

If `MDAN_PROJECT_ROOT` has no `_mdan/_config/workflow-manifest.csv` (no `mdan install` was run there), the server falls back to serving the content bundled in the `mdan-method` package itself, read-only. The context graph and decision records are still written into `MDAN_PROJECT_ROOT` — useful for trying MDAN against a project without committing to an install, or for the Glama-hosted server.

## HTTP transport (remote / shared server)

For a server reachable over the network instead of spawned per-client over stdio:

```bash
mdan serve --http --port 3100                                    # loopback only, no auth needed
mdan serve --http --host 0.0.0.0 --token "$MDAN_HTTP_TOKEN"       # exposed: token mandatory
```

- Binding a non-loopback host (`0.0.0.0`, a LAN IP, …) without `--token` / `MDAN_HTTP_TOKEN` is refused, unless you pass `--insecure` (don't, outside a sandboxed network).
- The token is checked as `Authorization: Bearer <token>`, constant-time compared.
- Endpoint: `POST /mcp` (Streamable HTTP, stateless — no session affinity needed). Health check: `GET /health`.
- Point your MCP client at the HTTP endpoint instead of a spawned command, per that client's docs for remote/HTTP MCP servers.

```bash
docker build -t mdan-mcp .
docker run -i --rm -v "$PWD:/workspace" mdan-mcp                              # stdio
docker run -p 3100:3100 -e MDAN_HTTP_TOKEN=... mdan-mcp --http --host 0.0.0.0 # HTTP
```

## Environment variables

| Variable | Effect |
|----------|--------|
| `MDAN_PROJECT_ROOT` | Project directory (context graph, decisions, state); defaults to the current directory |
| `MDAN_CLAUDE_DIR` | Overrides `~/.claude` for the ecosystem tools (`mdan_ecosystem_*`) |
| `MDAN_HTTP_TOKEN` | Bearer token for `--http`, alternative to `--token` |
| `PORT`, `HOST` | Defaults for `--port` / `--host` |

See the full tool/prompt/resource list in the [MCP reference](../reference/mcp.md).
