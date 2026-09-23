# Explanation: concepts

## Wizards and agents

An **agent** is a persona (a name, a role, principles, a communication style, a numbered menu) that stays in character for a conversation — `/mdan-agent-architect` or `mdan_consult_agent { name: "architect" }`. A **wizard** (workflow) is a step-by-step process that produces a specific artifact — `/mdan-create-prd` or `mdan_run_workflow { name: "create-prd" }`. Agents can trigger wizards from their menu; wizards don't require staying in any one persona. Both are markdown/YAML content under `_mdan/`, not code — MDAN's "engine" (`tools/`) reads and serves that content, it doesn't hardcode the method's steps.

Two wizard kinds: a **free-form wizard** (`wizard.md`) is read and executed directly, step by step, by whichever LLM loaded it. A **structured workflow** (`workflow.yaml`) is instead passed as config to `_mdan/core/tasks/workflow.xml`, a shared engine that enforces things like "save output after each section" uniformly across workflows that use it (mostly build-phase ones: `code-review`, `dev-story`, `sprint-planning`).

## Context graph

A DAG of everything a project produces — the brief, PRD, architecture, epics, stories, decision records, and (if you run `mdan trace --graph` or `mdan_trace { register: true }`) requirements/tests too. Edges are typed: `input_to` (this fed into that), `derived_from`, `impacts` (a decision affected an artifact), `references`. Nodes record the file's hash at registration time, which is what makes staleness detection possible — `mdan stale` diffs the current file hash against what's recorded and reports both what changed and what downstream depends on it.

This is the mechanism behind two otherwise-hard questions: "what should I re-check if I change this?" (`mdan impact <id>`, `mdan stale`) and "how much process does this change actually need?" (`mdan_estimate_scope` — see below), both grounded in real recorded relationships rather than a guess.

## State and resume

`_mdan/state/MDAN-STATE.json` tracks the current workflow and step, every completed workflow, every registered artifact, and every decision. `mdan_run_workflow` (and the equivalent slash command) checks this before returning the wizard: if that workflow was interrupted mid-step, it tells the agent to offer resuming at the recorded step instead of restarting from scratch, and lists existing artifacts as available inputs. `mdan status` is the human-facing view of the same file.

## Agent memory sidecars

Separate from the context graph: each agent can have a persistent memory sidecar (`mdan_memory_remember`/`recall`/`forget`/`list`), storing typed observations with a confidence score (explicit decisions score highest, inferences lowest). Storing the same memory again reinforces it rather than duplicating it. Memory decays after 5 idle sessions the agent doesn't participate in, so stale context fades rather than accumulating forever. `mdan_memory_end_session` also records relationships between agents (who agreed/disagreed/complemented whom) and decision outcomes (won/lost/compromised) — this is what lets party-mode debates reference "last time we discussed this, X argued Y and lost."

This is distinct from the `memories` field in [agent customization](../how-to/customize-agents.md) — customization memories are permanent facts you set explicitly (e.g. "this project targets Azure"), sidecar memories are things agents observe and that naturally fade.

## Scale-adaptive routing

Both quality strictness and change routing scale with the project, via `project_scale` (`auto`/`solo`/`team`/`enterprise` — see [config reference](../reference/config.md#project-scale-project_scale----scale)):

- `mdan check` demands more (sections, measurable NFRs, acceptance criteria) at `enterprise` scale than at `solo`.
- `mdan scope` (`mdan_estimate_scope`) reads risk terms in the change description, touched file count, and the real downstream impact of any named artifacts in the context graph, and recommends `oneshot` (go straight to `quick-dev`), `spec` (write a `quick-spec` first) or `full` (re-run planning wizards) — with scale nudging the threshold.

## Quality gates

`mdan check` is pure deterministic text analysis — no LLM call, so it's fast and CI-safe. It looks for unfilled template placeholders, `TODO`/`TBD` markers, empty or missing sections, functional requirements without matching non-functional coverage, and stories without acceptance criteria — producing `PASS`/`CONCERNS`/`FAIL`. Planning wizards run it on their own output before marking a workflow complete; it's also callable standalone (CI, `/mdan-qa-release-gate`, ad hoc).

## Traceability

`mdan trace` extracts FR/NFR ids from the PRD, matches them against stories (epics document) and tests (test files in the repo), and reports coverage gaps plus a gate decision. `--graph` additionally writes requirement/story/test nodes into the context graph, which is what lets `mdan impact FR3` later answer "which stories and tests cover this requirement" directly instead of re-parsing documents.

## Decision records

Structured debates (`/mdan-debate`, or `debate`/`consensus` mode in `/mdan-party-mode`) end in a decision record (`DR-XXX`): topic, decision, rationale, confidence, participants, rounds, dissent if any. It's written to `mdan_output/decisions/` **and** registered as a `decision` node in the context graph with `impacts` edges to whatever it affects — so `mdan graph --since DR-001` shows the decision and everything downstream of it, and a later `mdan stale` on the architecture (say) can trace back to which decision drove it.
