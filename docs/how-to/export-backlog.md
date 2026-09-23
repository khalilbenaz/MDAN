# How to: export the backlog to a tracker

`mdan export` reads the epics/stories document (`## Epic N: …` / `### Story N.M: …` headings — the format produced by `/mdan-create-epics-and-stories`) and turns it into CSV rows or tracker items.

```bash
mdan export --to csv                    # to stdout
mdan export --to csv --out backlog.csv
mdan export --to github --repo owner/name
mdan export --to ado --org my-org --project MyProject
mdan export --to jira --url https://my-site.atlassian.net --project KEY
```

Or via MCP: `mdan_export_backlog { target, apply, file?, repo?/org?+project?/url?+project? }`.

## Dry run by default

Without `--apply` (CLI) or `apply: true` (MCP), nothing is sent: the command prints the planned requests (method, URL, body) so you can review before touching your tracker. Add `--apply` to actually send them:

```bash
mdan export --to github --repo owner/name --apply
```

## Authentication

| Target | Env vars |
|--------|----------|
| `github` | `GITHUB_TOKEN` or `GH_TOKEN` |
| `ado` | `AZURE_DEVOPS_PAT` |
| `jira` | `JIRA_EMAIL` + `JIRA_API_TOKEN` |
| `csv` | none — local file, no network call |

## What gets created

- **GitHub**: one Issue per epic and per story; each story issue body references its epic ("Part of #N").
- **Azure DevOps**: Epic work items and User Story work items, with parent links from story to epic.
- **Jira**: issues in Atlassian Document Format (ADF) for the description, with parent keys linking stories to epics.
- **CSV**: `type,key,parent,title,description,requirements` — one row per epic and per story.

## Idempotency

Exported item ids are recorded in `_mdan/state/export-<target>.json` (e.g. `export-github.json`). Re-running `mdan export --to github --apply` after editing the epics document updates the existing GitHub issues instead of creating duplicates. Delete that file if you want a clean re-export (it will create new items).

## Choosing the epics file

By default MDAN picks up the epics document registered in the project state (or found under `docs/`). Override it with `--file`:

```bash
mdan export --to csv --file mdan_output/planning-artifacts/epics.md
```
