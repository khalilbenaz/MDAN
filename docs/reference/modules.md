# Reference: modules

MDAN ships a required core + main module, and six optional packs installed with `--modules`. Generated from `_mdan/_config/{agent,workflow}-manifest.csv` (produced by `npm run build`) — the [README](../../README.md#the-agents) has the same agent table kept current automatically; this page adds the workflows per module and a short description of what each pack is for.

## `core` + `mdan` — always installed

The engine (`core`: `mdan-master`, `rules.md`, `workflow.xml`, quality/traceability logic) and the main module (`mdan`: every phase-1 through phase-5 wizard, quick flows, special modes). See the [available commands](../../README.md#commandes-disponibles) table for the full wizard list, phase by phase.

**Agents:** Amina (analyst), Reda (architect), Haytame (dev), MDAN Master (orchestrator), Khadija (PM), Nadia (scrum master), Yassir (security), Youssef (tech writer), Jihane (UX designer).

**Workflows (`mdan` module):** `create-product-brief`, `domain-research`, `market-research`, `technical-research`, `create-prd`, `create-ux-design`, `create-architecture`, `create-epics-and-stories`, `code-review`, `correct-course`, `dev-story`, `retrospective`, `sprint-planning`, `document-project`, `quick-dev`, `quick-spec`, `brainstorming`, `debate`, `party-mode`.

## `qa` — Test Architect pack

`--modules qa`. Risk-based test design, ATDD, traceability, NFR assessment, test review, CI gates, release gate — every artifact linked into the context graph so "what tests should re-run if this story changes" has a real answer.

**Agent:** Fatima (Test Architect).

**Workflows:** `qa-test-design`, `qa-atdd`, `qa-traceability`, `qa-nfr-assessment`, `qa-test-review`, `qa-ci-gates`, `qa-release-gate`.

## `payments-ma` — Morocco Payments pack

`--modules payments-ma`. Wallets, payment institutions, banks: BAM requirements, ISO 8583/20022, reconciliation. Regulatory ceilings are flagged "verify against the current BAM circular" rather than hardcoded.

**Agents:** Houda (BAM Compliance Officer), Anas (Payments Systems Architect), Samira (Reconciliation & Settlement Lead).

**Workflows:** `pay-kyc-limits`, `pay-txn-flow`, `pay-iso8583`, `pay-recon`, `pay-compliance-review`.

**Reference data:** `_mdan/payments-ma/data/rib-iban.md` (Morocco RIB/IBAN structure and key computation), plus an ISO 8583 cheat sheet used by `pay-iso8583`.

## `fintech` — FinTech pack

`--modules fintech`. General financial-services agents for compliance and risk work outside the Morocco-specific payments domain.

**Agents:** Rachid (Compliance Officer), Sanae (Financial Analyst), Karim (Risk Manager).

## `devops-azure` — DevOps & Azure pack

`--modules devops-azure`. Azure-focused infrastructure and delivery agents.

**Agents:** Hamza (Azure Specialist), Yassine (CI/CD Architect), Omar (DevOps Engineer).

## `db-optimization` — Database Optimization pack

`--modules db-optimization`. Query and schema performance agents.

**Agents:** Salma (Indexing Specialist), Mehdi (DB Performance Analyst), Driss (Query Optimizer).

## `ecosystem` — Ecosystem pack

`--modules ecosystem`. Bridges MDAN to a local `~/.claude` install (skills, agents, commands from `khalilbenaz/claude-skills-collection` and `davila7/claude-code-templates`), plus a catalog and orchestrator agents that route into that larger ecosystem.

**Agents:** Fayçal (IA Master), Saad (Data Scientist), Ilyas (DevOps Commander), Amine (Fullstack Architect), Imane (Marketing Strategist), Adnane (Product Lead), Leila (Deep Research Team Lead), Samir (Security Specialist), Zineb (Ecosystem Skill Dispatcher).

**Requires:** `_mdan/ecosystem/catalog/CATALOG.md` for `mdan_ecosystem_catalog`; the search/read/stats tools work against `MDAN_CLAUDE_DIR` (default `~/.claude`) directly, independent of this module's own install.

---

Install several packs at once: `mdan install --modules qa,payments-ma,fintech`, or `--modules all` for every optional pack. See [`mdan install`](cli.md#mdan-install-dir).
