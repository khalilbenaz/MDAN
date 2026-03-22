# MDAN — Multi-Agent Development Agentic Network

![MDAN](https://i.imgur.com/YwfB0Gx.jpeg)

[![npm](https://img.shields.io/npm/v/mdan-method.svg)](https://www.npmjs.com/package/mdan-method)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Wizards](https://img.shields.io/badge/wizards-17-purple)]()
[![Agents](https://img.shields.io/badge/agents-19-blue)]()
[![Packs](https://img.shields.io/badge/packs-3-orange)]()

**MDAN** howa framework dial développement b l'IA, fih des agents spécialisés, des wizards interactifs step-by-step, un système de mémoire persistante, w un protocole de débat structuré.

**100% gratuit w open source.** Made in Morocco.

---

## Jdid f v3 🚀

### MCP Server

Daba MDAN kaychtaghel bhal **MCP server** — ay IDE compatible b [MCP](https://modelcontextprotocol.io/) (Claude Code, Cursor, etc.) ygdar yconnecter directement w yst3mel ga3 les workflows w les agents bhal des tools.

```bash
mdan serve            # stdio transport
mdan serve --sse      # SSE l remote
```

Zid had la config f `.mcp.json` dyalek :

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

**Les MCP tools li disponibles :**

| Tool | Chnou kadir |
|------|-------------|
| `mdan_list-workflows` | Kaylisté ga3 les workflows |
| `mdan_workflow_{name}` | Kayexécuté un workflow (create-prd, create-architecture, etc.) |
| `mdan_list-agents` | Kaylisté ga3 les agents installés |
| `mdan_agent_{name}` | Kayconsulté un agent spécifique |
| `mdan_graph_impact` | Analyse d'impact en aval d'un artifact |
| `mdan_graph_visualize` | Diagramme Mermaid dial le context graph |
| `mdan_orchestrate_party-mode` | Session multi-agent (discussion/debate/consensus) |
| `mdan_orchestrate_create-decision-record` | Créé un decision record |

**MCP resources :** `mdan://state`, `mdan://config`, `mdan://graph`

### Context Graph

DAG léger li kaytracké ga3 les relations entre les artifacts. Kol workflow mlli kaykmel, l'artifact automatiquement kayt-enregistré f le graphe.

```bash
mdan impact <artifact-id>   # Analyse d'impact en aval
mdan graph                   # Diagramme Mermaid
mdan graph --json            # JSON brut
```

```mermaid
graph TD
  prd[PRD] -->|input_to| arch[Architecture]
  arch -->|input_to| epics[Epics & Stories]
  epics -->|input_to| sprint[Sprint Plan]
  dr-001[DR-001: API Strategy] -->|impacts| arch
```

Les Decision Records dial les débats aussi kayt-enregistrów f le graphe.

### Multi-Agent Orchestration Avancée

Party Mode daba 3endo **3 modes** :

| Mode | Chnou fih |
|------|-----------|
| **Discussion** | Conversation libre multi-agent (mode original) |
| **Debate** | Argumentation structurée b 3 d les rôles → Decision Record |
| **Consensus** | N agents kayt-convergéw vers position mochterka |

**Debate mode** — 3 rôles : Proponent 🟢, Opponent 🔴, Arbitrator ⚖️. 3 rounds structurés. Automatiquement kayproduisé Decision Record (DR-XXX) w kayt-enregistré f le Context Graph. Disponible comme sous-mode de party-mode OU directement via `/mdan-debate`.

**Consensus mode** — 3-5 agents kaymchiw f 4 phases : positions initiales → mapping d'accord/désaccord → itérations de convergence → synthèse.

**Agent Sidecars** — Mémoire persistante l kol agent entre les sessions. Les agents kaytfekrów les observations, les préférences, w les décisions dial les sessions précédentes.

---

## Bdew mn hna — Quick Start

```bash
npx mdan-method install
```

L'installeur kayguide-k bach tkhtar les modules w l'IDE dyalek (Claude Code, Gemini CLI, OpenCode, QwenCoder...).

Mn b3d, f l'IDE dyalek, kteb `/mdan-` w ghadi tchof ga3 les commandes li disponibles.

---

## Les commandes li kaynin

Ga3 les commandes kaybdaw b `/mdan-`.

### Wizards — Phase 1 : Discover (Lektichaf)

| Commande | Chnou kadir |
|----------|-------------|
| `/mdan-create-product-brief` | Kaycréé lik product brief collaboratif f 6 d les étapes. Kaydéfini la vision, les utilisateurs cibles, le scope w les métriques de succès. |
| `/mdan-market-research` | Recherche dial souk : analyse concurrentielle, comportement dial les clients, pain points w les opportunités. |
| `/mdan-technical-research` | Recherche technique : les technologies, patterns d'architecture, intégrations w les tendances. |
| `/mdan-domain-research` | Recherche dial domaine : analyse sectorielle, réglementation, paysage concurrentiel. |

### Wizards — Phase 2 : Plan (Tkhtiit)

| Commande | Chnou kadir |
|----------|-------------|
| `/mdan-create-prd` | Kaycréé Product Requirements Document kamel f 12 étape. Fih la vision, les user journeys, le scoping, les requirements fonctionnels w non-fonctionnels. |
| `/mdan-create-ux-design` | Kayplani le design UX f 14 étape : discovery, design system, fondations visuelles, user journeys, composants w responsive. |

### Wizards — Phase 3 : Architect (L'handasa)

| Commande | Chnou kadir |
|----------|-------------|
| `/mdan-create-architecture` | Kaycréé l'architecture technique f 8 étapes : contexte, décisions, patterns, structure w validation. |
| `/mdan-create-epics-and-stories` | Kayfssel les requirements l epics w user stories prêtes bach tbda le développement. |

### Wizards — Phase 4 : Build (Lbni)

| Commande | Chnou kadir |
|----------|-------------|
| `/mdan-sprint-planning` | Kaygénéré sprint plan mn les epics. Kayorganisi les stories f les sprints b estimation. |
| `/mdan-dev-story` | Kayimplémenté une story b le fichier de spec dyalha. TDD, tests, w documentation automatique. |
| `/mdan-code-review` | Review de code adversariale : kaylga les bugs, les problèmes de sécurité w les violations dial patterns. |

### Wizards — Phase 5 : Ship (Tslim)

| Commande | Chnou kadir |
|----------|-------------|
| `/mdan-document-project` | Kaygénéré la documentation kamla dial le projet : overview, deep-dives, source tree. |

### Quick Flows (Bsser3a)

| Commande | Chnou kadir |
|----------|-------------|
| `/mdan-quick-dev` | Dev b ssre3a f 6 étapes l les changements sghir. Détection de mode, contexte, exécution, self-check w review. |
| `/mdan-quick-spec` | Spec technique b ssre3a f 4 étapes. Kayproduit spec prête l l'implémentation. |

### Special (Khassa)

| Commande | Chnou kadir |
|----------|-------------|
| `/mdan-party-mode` | Mode multi-agents : 3 modes — Discussion, Debate, Consensus. Agent sidecars, Decision Records, Context Graph. |
| `/mdan-debate` | Débat structuré standalone entre agents (Proponent 🟢 vs Opponent 🔴 + Arbitrator ⚖️). 3 rounds → Arbitration → Decision Record. Accès direct sans passer par party-mode. |
| `/mdan-brainstorming` | Session de brainstorming b 12+ techniques créatives (SCAMPER, Six Thinking Hats, Mind Mapping, etc.). |

### CLI Commands (Jdid f v3)

| Commande | Chnou kadir |
|----------|-------------|
| `mdan serve` | Kaystart le MCP server (stdio ou SSE) |
| `mdan impact <id>` | Analyse d'impact d'un artifact f le Context Graph |
| `mdan graph` | Kayaffiche le Context Graph bhal Mermaid diagram |

---

## Les Agents

Les agents homa des personnalités IA spécialisées, t9der t3ayyet 3lihom directement.

### L'équipe principale

| Commande | Agent | Chnou kaydir |
|----------|-------|-------------|
| `/mdan-agent-pm` | Khalil | **Product Manager** — Vision produit, PRD, priorisation, roadmap |
| `/mdan-agent-analyst` | Amina | **Business Analyst** — Recherche, briefs, analyse de marché |
| `/mdan-agent-architect` | Reda | **Architect** — Architecture système, tech stack, patterns |
| `/mdan-agent-dev` | Haytame | **Developer** — Implémentation, TDD, code propre |
| `/mdan-agent-qa` | Fatima | **QA Engineer** — Tests, qualité, stratégie de test |
| `/mdan-agent-ux-designer` | Jihane | **UX Designer** — Design UX/UI, wireframes, prototypes |
| `/mdan-agent-tech-writer` | Youssef | **Technical Writer** — Documentation technique, guides, API docs |
| `/mdan-agent-sm` | Nadia | **Scrum Master** — Gestion agile, sprints, rétrospectives |
| `/mdan-agent-security` | Yassir | **Security Engineer** — Audit de sécurité, threat modeling (STRIDE), OWASP Top 10, audit de dépendances, hardening |
| `/mdan-agent-quick-flow-solo-dev` | — | **Solo Dev** — Mode rapide tout-en-un l les développeurs solo |

### Pack FinTech

| Commande | Agent | Chnou kaydir |
|----------|-------|-------------|
| `/mdan-agent-fintech-compliance-officer` | Rachid | **Compliance Officer** — Conformité réglementaire (GDPR, PCI DSS, AML/KYC), audit, policies |
| `/mdan-agent-fintech-financial-analyst` | Amina | **Financial Analyst** — Modélisation financière, analyse de marché, reporting |
| `/mdan-agent-fintech-risk-manager` | Karim | **Risk Manager** — Identification w mitigation dial les risques, stress testing |

### Pack DevOps & Azure

| Commande | Agent | Chnou kaydir |
|----------|-------|-------------|
| `/mdan-agent-devops-azure-azure-specialist` | Reda | **Azure Specialist** — Architecture cloud Azure, migration, optimisation dial les coûts |
| `/mdan-agent-devops-azure-cicd-architect` | Yassine | **CI/CD Architect** — Pipelines CI/CD, déploiement blue-green/canary, automatisation |
| `/mdan-agent-devops-azure-devops-engineer` | Omar | **DevOps Engineer** — Infrastructure as Code (Terraform, Bicep), monitoring, Kubernetes |

### Pack Database Optimization

| Commande | Agent | Chnou kaydir |
|----------|-------|-------------|
| `/mdan-agent-db-optimization-query-optimizer` | Driss | **Query Optimizer** — Analyse dial plans d'exécution, tuning SQL, détection N+1 |
| `/mdan-agent-db-optimization-indexing-specialist` | Salma | **Indexing Specialist** — Stratégie d'indexation, index composites, audit d'index |
| `/mdan-agent-db-optimization-performance-analyst` | Mehdi | **DB Performance Analyst** — Monitoring, diagnostic, capacity planning, tuning |

---

## Système de Mémoire

```
_mdan/
├── core/config.yaml            ← Configuration dial le projet
├── state/
│   ├── MDAN-STATE.json         ← État global persistant
│   ├── context-graph.json      ← DAG dial les artifacts w les relations
│   └── sidecars/               ← Mémoire persistante dial kol agent
└── _config/manifest.yaml       ← État dial l'installation

Le contexte kaybqa entre :
- Les wizards (le PRD 3endo accès l le brief)
- Les sessions (reprise automatique)
- Les agents (les décisions partagées + sidecars)
- Le Context Graph (traçabilité dial ga3 les artifacts)
```

---

## Debate Protocol

Mlli katwsel décision critique (choix de stack, pattern, priorisation), les agents kaydébatiw :

### Discussion Mode (Original)
Conversation libre, 2-3 agents kaytjawbow b turn rotation.

### Debate Mode (Jdid f v3) ⚔️
```
3 rôles : Proponent 🟢, Opponent 🔴, Arbitrator ⚖️

Round 1: Opening      → Kol agent kayprésenté la position dyalo (max 150 mots)
Round 2: Rebuttal     → Kol agent kayrépondé directement l l'autre
Round 3: Final        → Derniers arguments avant l'arbitrage

→ Arbitration : L'arbitre kaydécidé b rationale, confidence score w dissent
→ Decision Record (DR-XXX) : Kayt-enregistré automatiquement f le Context Graph
```

### Consensus Mode (Jdid f v3) 🤝
```
3-5 agents kayt-convergéw :

Phase 1: Positions    → Kol agent kayprésenté la position dyalo
Phase 2: Mapping      → Zones d'accord ✅ w de tension ⚠️
Phase 3: Convergence  → Les agents kaybddlo positions, concessions
Phase 4: Synthèse     → Position merguée li kaydkhol fiha ga3 les perspectives

→ Decision Record kayt-enregistré f le Context Graph
```

---

## Architecture (v3)

```
_mdan/                          ← Modules MDAN installés
├── _config/                    ← Manifests, config agents
├── core/                       ← Moteur (wizard engine, workflow.xml)
├── mdan/                       ← Module principal (workflows, teams)
├── state/                      ← État runtime (graph, sidecars)
└── {module}/                   ← Modules de domaine (fintech, devops-azure, etc.)

tools/                          ← Nouveau f v3
├── cli/                        ← Commandes CLI (serve, impact, graph)
│   └── lib/                    ← Librairies (context-graph)
└── mcp/                        ← MCP Server
    ├── tools/                  ← Enregistrement dial les MCP tools
    └── resources/              ← Enregistrement dial les MCP resources
```

---

## Installation

### B npm (recommandé)

```bash
npx mdan-method install
```

### Manuellement

```bash
git clone https://github.com/khalilbenaz/MDAN.git
cd MDAN && npm install
node tools/cli/mdan-cli.js install
```

### Les IDE supportés

Claude Code, Gemini CLI, OpenCode, QwenCoder, Cursor, Windsurf, Cline, Codex, w bzzaf d'autres.

---

## Licence

MIT

---

<p align="center">
  <strong>17 wizards · 19 agents · 3 packs · MCP Server · Context Graph · Debate/Consensus</strong><br>
  Msnou3 f lMghrib par <a href="https://github.com/khalilbenaz">@khalilbenaz</a>
</p>
