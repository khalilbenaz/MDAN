# Explanation: MDAN vs BMAD-METHOD

MDAN's method and its wizard/agent structure are directly inspired by [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) (the analyst → PM → architect → dev → QA pipeline, party mode, quick flows). This page is an honest comparison against BMAD-METHOD v6.12 (Sept 2026), not a pitch — where BMAD is ahead, it says so.

Facts about BMAD below are as documented for v6.12: a skill-first architecture (core + `bmm` ship as skills in the main repo; `bmb` builder, `cis` creative suite, `gds` game dev, and `tea` test architect with agent Murat are separate npm modules); five named `bmm` agents — Mary (analyst), John (PM), Winston (architect), Amelia (dev), Sally (UX) — with Bob (SM) and Paige (tech writer) no longer dedicated agents; phases analysis/planning/solutioning/implementation with `bmad-build` implicitly routing oneshot vs full; `bmad-correct-course` and `bmad-retrospective`; a 3-layer TOML customization (`customize.toml` shipped/team/user) via a `bmad-customize` skill; an installer with per-module channels (stable/next/pinned); web bundles for Gemini Gems and ChatGPT GPTs; a multilingual docs site (en, fr, ko, vi, zh); no native MCP server; party-mode discussion without persisted decision records; no artifact dependency graph.

## Feature comparison

| Capability | MDAN | BMAD-METHOD v6.12 |
|---|---|---|
| Native MCP server (tools, prompts, resources) | ✅ stdio + authenticated Streamable HTTP | ❌ none |
| Context/dependency graph over artifacts | ✅ DAG with `impacts`/`stale`/`--since` highlight | ❌ none |
| Decision records linked to a dependency graph | ✅ `DR-XXX` registered as graph nodes with `impacts` edges | ⚠️ party mode has discussion/debate, but no persisted, graph-linked decision record |
| Project state + resume | ✅ `MDAN-STATE.json`, wizards offer a resume point mid-step | ⚠️ some state tracking exists, but not exposed as a resumable-step contract the way MDAN's `mdan_run_workflow` progress section is |
| Agent persistent memory with decay | ✅ sidecars, confidence scoring, 5-session decay, relationships/outcomes | ❌ no equivalent memory system documented |
| Quality gates as a standalone, CI-usable check | ✅ `mdan check` — deterministic, exit codes, `--scale` strictness | ⚠️ quality is largely enforced inside wizard flow, not exposed as a separate CI-friendly command with its own exit code |
| Traceability (requirement → story → test) feeding the graph | ✅ `mdan trace`, `--graph` writes it into the DAG | ❌ no equivalent |
| Scope routing grounded in real dependency impact | ✅ `mdan scope` reads actual graph impact, not just heuristics on the text | ⚠️ `bmad-build` routes oneshot vs full implicitly, but from workflow config, not a measured downstream-impact query |
| Tracker export (GitHub/ADO/Jira) | ✅ `mdan export`, dry run + idempotent re-run | ❌ not part of the method itself |
| Web bundles (GPT, Gem, Claude Project) | ✅ | ✅ (BMAD had this first) |
| Layered customization | ✅ shipped/team/user YAML, exposed via MCP tool | ✅ shipped/team/user TOML, via a dedicated `bmad-customize` skill |
| Update channels | ✅ `mdan update --channel latest\|next\|<version>` | ✅ per-module channels (stable/next/pinned) — more granular than MDAN's single channel flag |
| Wizard evaluation harness | ✅ `npm run eval`, LLM-driven scripted personas + `mdan check` assertions | ❌ not documented as part of the method |
| Multilingual (Darija/French/English) | ✅ built into `_mdan/core/rules.md`, one config key | ⚠️ docs site is multilingual (en/fr/ko/vi/zh); the method's own agent output language isn't a first-class Darija-aware feature |
| Vertical/domain packs | ✅ `payments-ma`, `fintech`, `devops-azure`, `db-optimization`, `qa`, `ecosystem` bridge to `~/.claude` | ⚠️ domain coverage instead comes from separate specialized modules (`cis` creative, `gds` game dev) rather than industry-vertical packs like payments or fintech compliance |
| Skill-first architecture, larger skill ecosystem | ❌ MDAN is agent/workflow-first, not skill-first | ✅ core + `bmm` as skills, plus `bmb`/`cis`/`gds`/`tea` as separate modules |
| Named specialist test agent | ⚠️ `qa` pack has one Test Architect (Fatima) | ✅ `tea` module has Murat, a dedicated test-architecture agent with its own npm package |

## Where BMAD is still ahead

- **Community and maturity.** BMAD-METHOD has a much larger user base, more contributors, and a longer track record; MDAN is a smaller, newer project.
- **Documentation site in 5 languages.** BMAD publishes a proper docs site in English, French, Korean, Vietnamese and Chinese. MDAN's docs are English/French markdown in the repo, no dedicated site, no Korean/Vietnamese/Chinese.
- **Release cadence and modularity.** BMAD ships `core`, `bmm`, `bmb`, `cis`, `gds`, `tea` as separate, independently versioned npm packages with per-module update channels (stable/next/pinned). MDAN is a single package with a single version and a single `--channel` flag for the whole install.
- **Game development and creative suites.** `gds` (game dev) and `cis` (creative writing suite) have no MDAN equivalent — MDAN's optional packs are development/fintech/ops-oriented only.
- **Python-tested skills.** BMAD's skill-first architecture comes with its own testing story for skills that MDAN's markdown-content model doesn't need to replicate, but also doesn't offer.
- **Marketplace/plugin distribution.** BMAD's skill packaging fits natively into ecosystems that distribute skills/plugins (e.g. Claude Code's skill marketplace model); MDAN's content is installed as a monolithic copy into `_mdan/`, not as independently discoverable/installable plugins.
- **Dedicated test-architecture agent as a first-class module.** `tea`/Murat is a specialized, separately maintained module; MDAN folds test-architecture into one `qa` pack agent.

## Where they overlap and don't really compete

Both frameworks structure AI-assisted software delivery around the same core idea: specialized personas, staged wizards from discovery to delivery, and human-in-the-loop checkpoints rather than a single autonomous agent. If you value a mature ecosystem, a documented multi-language site, and separately versioned specialist modules (including game dev and creative writing), BMAD-METHOD is the more established choice today. If you want the method itself wired into an MCP server with a real dependency graph, decaying agent memory, CI-usable quality gates tied to traceability, and Morocco/fintech-specific packs, that's what MDAN adds on top of the same lineage.
