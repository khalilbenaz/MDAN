# MDAN — Multi-Agent Development Agentic Network

![MDAN](https://i.imgur.com/YwfB0Gx.jpeg)

[![npm](https://img.shields.io/npm/v/mdan-method.svg)](https://www.npmjs.com/package/mdan-method)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Wizards](https://img.shields.io/badge/wizards-16-purple)]()
[![Agents](https://img.shields.io/badge/agents-18-blue)]()
[![Packs](https://img.shields.io/badge/packs-3-orange)]()

**MDAN** est un framework de développement piloté par l'IA avec des agents spécialisés, des wizards interactifs step-by-step, un système de mémoire persistante, et un protocole de débat structuré.

**100% gratuit et open source.**

---

## Quick Start

```bash
npx mdan-method install
```

L'installeur vous guide pour choisir vos modules et IDE (Claude Code, Gemini CLI, OpenCode, QwenCoder...).

Puis dans votre IDE, tapez `/mdan-` pour voir toutes les commandes disponibles.

---

## Commandes disponibles

Toutes les commandes commencent par `/mdan-`.

### Wizards — Phase 1 : Discover

| Commande | Description |
|----------|-------------|
| `/mdan-create-product-brief` | Crée un product brief collaboratif en 6 étapes. Définit la vision, les utilisateurs cibles, le scope et les métriques de succès. |
| `/mdan-market-research` | Recherche marché : analyse concurrentielle, comportement client, pain points et opportunités. |
| `/mdan-technical-research` | Recherche technique : technologies, patterns d'architecture, intégrations et tendances. |
| `/mdan-domain-research` | Recherche domaine : analyse sectorielle, réglementation, paysage concurrentiel. |

### Wizards — Phase 2 : Plan

| Commande | Description |
|----------|-------------|
| `/mdan-create-prd` | Crée un Product Requirements Document complet en 12 étapes. Couvre la vision, les user journeys, le scoping, les requirements fonctionnels et non-fonctionnels. |
| `/mdan-create-ux-design` | Planifie le design UX en 14 étapes : discovery, design system, fondations visuelles, user journeys, composants et responsive. |

### Wizards — Phase 3 : Architect

| Commande | Description |
|----------|-------------|
| `/mdan-create-architecture` | Crée l'architecture technique en 8 étapes : contexte, décisions, patterns, structure et validation. |
| `/mdan-create-epics-and-stories` | Découpe les requirements en epics et user stories prêtes pour le développement. |

### Wizards — Phase 4 : Build

| Commande | Description |
|----------|-------------|
| `/mdan-sprint-planning` | Génère un sprint plan à partir des epics. Organise les stories en sprints avec estimation. |
| `/mdan-dev-story` | Implémente une story en suivant son fichier de spec. TDD, tests, et documentation automatique. |
| `/mdan-code-review` | Review de code adversariale : trouve les bugs, problèmes de sécurité et violations de patterns. |

### Wizards — Phase 5 : Ship

| Commande | Description |
|----------|-------------|
| `/mdan-document-project` | Génère la documentation complète du projet : overview, deep-dives, source tree. |

### Quick Flows

| Commande | Description |
|----------|-------------|
| `/mdan-quick-dev` | Dev rapide en 6 étapes pour les petits changements. Détection de mode, contexte, exécution, self-check et review. |
| `/mdan-quick-spec` | Spec technique rapide en 4 étapes. Produit une spec prête pour l'implémentation. |

### Special

| Commande | Description |
|----------|-------------|
| `/mdan-party-mode` | Mode multi-agents : réunit tous les agents MDAN dans une discussion de groupe. Chaque agent intervient avec sa personnalité et expertise. |
| `/mdan-brainstorming` | Session de brainstorming avec 12+ techniques créatives (SCAMPER, Six Thinking Hats, Mind Mapping, etc.). |

---

## Agents

Les agents sont des personnalités IA spécialisées que vous pouvez invoquer directement.

### Equipe principale

| Commande | Agent | Role |
|----------|-------|------|
| `/mdan-agent-pm` | Khalil | **Product Manager** — Vision produit, PRD, priorisation, roadmap |
| `/mdan-agent-analyst` | Amina | **Business Analyst** — Recherche, briefs, analyse de marché |
| `/mdan-agent-architect` | Reda | **Architect** — Architecture système, tech stack, patterns |
| `/mdan-agent-dev` | Haytame | **Developer** — Implémentation, TDD, code propre |
| `/mdan-agent-qa` | Fatima | **QA Engineer** — Tests, qualité, stratégie de test |
| `/mdan-agent-ux-designer` | Jihane | **UX Designer** — Design UX/UI, wireframes, prototypes |
| `/mdan-agent-tech-writer` | Youssef | **Technical Writer** — Documentation technique, guides, API docs |
| `/mdan-agent-sm` | Nadia | **Scrum Master** — Gestion agile, sprints, rétrospectives |
| `/mdan-agent-quick-flow-solo-dev` | — | **Solo Dev** — Mode rapide tout-en-un pour développeurs solo |

### Pack FinTech

| Commande | Agent | Role |
|----------|-------|------|
| `/mdan-agent-fintech-compliance-officer` | Rachid | **Compliance Officer** — Conformité réglementaire (GDPR, PCI DSS, AML/KYC), audit, policies |
| `/mdan-agent-fintech-financial-analyst` | Amina | **Financial Analyst** — Modélisation financière, analyse de marché, reporting |
| `/mdan-agent-fintech-risk-manager` | Karim | **Risk Manager** — Identification et mitigation des risques, stress testing |

### Pack DevOps & Azure

| Commande | Agent | Role |
|----------|-------|------|
| `/mdan-agent-devops-azure-azure-specialist` | Reda | **Azure Specialist** — Architecture cloud Azure, migration, optimisation des coûts |
| `/mdan-agent-devops-azure-cicd-architect` | Yassine | **CI/CD Architect** — Pipelines CI/CD, déploiement blue-green/canary, automatisation |
| `/mdan-agent-devops-azure-devops-engineer` | Omar | **DevOps Engineer** — Infrastructure as Code (Terraform, Bicep), monitoring, Kubernetes |

### Pack Database Optimization

| Commande | Agent | Role |
|----------|-------|------|
| `/mdan-agent-db-optimization-query-optimizer` | Driss | **Query Optimizer** — Analyse de plans d'exécution, tuning SQL, détection N+1 |
| `/mdan-agent-db-optimization-indexing-specialist` | Salma | **Indexing Specialist** — Stratégie d'indexation, index composites, audit d'index |
| `/mdan-agent-db-optimization-performance-analyst` | Mehdi | **DB Performance Analyst** — Monitoring, diagnostic, capacity planning, tuning |

---

## Systeme de Memoire

```
_mdan/
├── core/config.yaml            ← Configuration projet
└── _config/manifest.yaml       ← État de l'installation

Le contexte survit entre :
- Les wizards (le PRD a accès au brief)
- Les sessions (reprise automatique)
- Les agents (décisions partagées)
```

---

## Debate Protocol

Quand une décision critique arrive (choix de stack, pattern, priorisation), les agents débattent :

```
Round 1: Ouverture     → Chaque agent présente sa position
Round 2: Challenge     → Chaque agent attaque la position adverse
Round 3: Données       → Preuves concrètes (benchmarks, patterns, risques)
Round 4: Synthèse      → Position finale intégrant les objections
Round 5: Scoring       → Score automatique + décision utilisateur
```

---

## Installation

### Via npm (recommandé)

```bash
npx mdan-method install
```

### Manuellement

```bash
git clone https://github.com/khalilbenaz/MDAN.git
cd MDAN && npm install
node tools/cli/mdan-cli.js install
```

### IDE supportés

Claude Code, Gemini CLI, OpenCode, QwenCoder, Cursor, Windsurf, Cline, Codex, et d'autres.

---

## Licence

MIT

---

<p align="center">
  <strong>16 wizards · 18 agents · 3 packs · Mémoire persistante · Debate Protocol</strong><br>
  Construit par <a href="https://github.com/khalilbenaz">@khalilbenaz</a>
</p>
