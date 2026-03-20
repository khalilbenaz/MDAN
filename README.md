# MDAN — Multi-Agent Development Agentic Network

![MDAN](https://i.imgur.com/YwfB0Gx.jpeg)

[![npm](https://img.shields.io/npm/v/mdan-method.svg)](https://www.npmjs.com/package/mdan-method)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Wizards](https://img.shields.io/badge/wizards-25-purple)]()
[![Agents](https://img.shields.io/badge/agents-29-blue)]()
[![Packs](https://img.shields.io/badge/packs-3-orange)]()

**MDAN** est un framework de développement piloté par l'IA avec des agents spécialisés, des wizards interactifs step-by-step, un système de mémoire persistante, et un protocole de débat structuré.

**100% gratuit et open source.** 🇲🇦

🇫🇷 [Spécification française](./MDAN.fr.md)

---

## MDAN vs MDAN — Ce qui nous différencie

| Fonctionnalité | MDAN V0 | MDAN |
|---|---|---|
| Wizards step-by-step | ✅ | ✅ Même qualité + améliorations |
| **Mémoire persistante** | ❌ | ✅ MDAN-STATE cross-wizard et cross-session |
| **Debate Protocol** | Party Mode (informel) | ✅ Protocole formel en 5 rounds avec scoring |
| **Scale-Adaptive** | Mentionné | ✅ Implémenté — auto-détecte solo/team/enterprise |
| **Quality Gates adaptatifs** | Statiques | ✅ S'ajustent au scale du projet |
| **CrewAI** (agents Python réels) | ❌ | ✅ Orchestration multi-agents exécutable |
| **Universal Envelope** | ❌ | ✅ Format inter-agents standardisé |
| **Bilingue FR/EN** | English only | ✅ Natif |
| **Personnalités marocaines** | Noms génériques | ✅ Khalil, Reda, Jihane, Haytame... |
| Cross-wizard context | ❌ Wizards isolés | ✅ Contexte partagé via MDAN-STATE |
| Auto-debate on conflict | ❌ | ✅ Déclenché automatiquement |

---

## 🚀 Quick Start

```bash
# Installation
npx mdan-method install

# Ou manuellement
git clone https://github.com/khalilbenaz/MDAN.git
cd MDAN && npm install
```

Puis dans votre IDE (Claude Code, Cursor, Windsurf...) :

```
/mdan-help        → Que faire ensuite ?
/discover         → Créer un product brief
/prd              → Créer un PRD
/architect        → Concevoir l'architecture
/dev              → Implémenter une story
/party            → Multi-agents collaboration
/debate           → Débat structuré
/status           → État du projet
/resume           → Reprendre la session
```

---

## 📋 Les 25 Wizards

### Phase 1 — Discover
| Wizard | Commande | Steps | Description |
|--------|---------|-------|-------------|
| Product Brief | `/discover` | 6 | Brief produit collaboratif |
| Research (Market) | `/research market` | 6 | Recherche marché |
| Research (Technical) | `/research tech` | 6 | Recherche technique |
| Research (Domain) | `/research domain` | 6 | Recherche domaine |

### Phase 2 — Plan
| Wizard | Commande | Steps | Description |
|--------|---------|-------|-------------|
| Create PRD | `/prd` | 12 | Product Requirements Document complet |
| Edit PRD | `/prd edit` | 4 | Modifier un PRD existant |
| Validate PRD | `/prd validate` | 13 | Validation en profondeur |
| UX Design | `/ux` | 14 | Design UX complet |

### Phase 3 — Architect
| Wizard | Commande | Steps | Description |
|--------|---------|-------|-------------|
| Architecture | `/architect` | 8 | Architecture technique + debate |
| Epics & Stories | `/epics` | 4 | Découpage en epics et stories |
| Readiness Check | `/ready` | 6 | Vérifier si prêt pour l'implémentation |

### Phase 4 — Build
| Wizard | Commande | Steps | Description |
|--------|---------|-------|-------------|
| Sprint Planning | `/sprint` | — | Planifier un sprint |
| Dev Story | `/dev` | — | Implémenter une story |
| Code Review | `/review` | — | Review structurée |
| Sprint Status | `/sprint status` | — | État du sprint |
| Retrospective | `/retro` | — | Rétrospective |

### Phase 5 — Ship
| Wizard | Commande | Steps | Description |
|--------|---------|-------|-------------|
| Deploy | `/deploy` | — | Préparer le déploiement |
| Document Project | `/docs` | — | Documentation complète |
| E2E Tests | `/e2e` | — | Générer tests end-to-end |

### Quick Flows
| Wizard | Commande | Steps | Description |
|--------|---------|-------|-------------|
| Quick Dev | `/quick` | 6 | Dev rapide sans planification lourde |
| Quick Spec | `/spec` | 4 | Spec technique rapide |

### Special
| Wizard | Commande | Description |
|--------|---------|-------------|
| Brainstorming | `/brainstorm` | 12+ techniques de brainstorming |
| Party Mode | `/party` | Multi-agents dans une session |
| Debate | `/debate` | Débat structuré en 5 rounds |
| Retrospective | `/retro` | Rétrospective de sprint |

---

## 🤖 Les 29 Agents

### Équipe principale (MMM)
| Agent | Nom 🇲🇦 | Rôle |
|-------|---------|------|
| PM | Khalil | Product Manager — vision, PRD |
| Analyst | Amina | Business Analyst — research, brief |
| Architect | Reda | Architecture système, tech stack |
| Dev | Haytame | Développement, implémentation |
| QA | Fatima | Tests, qualité |
| UX Designer | Jihane | Design UX/UI |
| Tech Writer | Youssef | Documentation technique |
| Scrum Master | Nadia | Gestion agile, sprints |
| Solo Dev | — | Mode rapide tout-en-un |

### Builders (MMB)
| Agent Builder | Module Builder | Workflow Builder |

### Creative Suite (CIS)
| Brainstorming Coach | Creative Solver | Design Thinking | Innovation Strategist | Storyteller | Presentation Master |

### Packs spécialisés
| 💰 **FinTech** | Financial Analyst · Compliance Officer · Risk Manager |
| ☁️ **DevOps/Azure** | Azure Specialist · CI/CD Architect · DevOps Engineer |
| 🗄️ **DB Optimization** | Query Optimizer · Indexing Specialist · Performance Analyst |

---

## 🧠 Système de Mémoire (exclusif MDAN)

```
.mdan/
├── config/config.yaml          ← Configuration projet
└── state/MDAN-STATE.json       ← État persistant

Le contexte survit entre :
✅ Les wizards (le PRD a accès au brief)
✅ Les sessions (reprise automatique)
✅ Les agents (décisions partagées)
```

---

## ⚔️ Debate Protocol (exclusif MDAN)

Quand une décision critique arrive (choix de stack, pattern, priorisation) :

```
Round 1: Ouverture     → Chaque agent présente sa position
Round 2: Challenge     → Chaque agent attaque la position adverse
Round 3: Données       → Preuves concrètes (benchmarks, patterns, risques)
Round 4: Synthèse      → Position finale intégrant les objections
Round 5: Scoring       → Score automatique + décision utilisateur
→ Résultat enregistré dans MDAN-STATE
```

---

## 📁 Architecture

```
MDAN/
├── .mdan/                      # Config + État
│   ├── config/config.yaml
│   └── state/MDAN-STATE.json
├── src/
│   ├── core/                   # Moteur : master agent, tasks
│   ├── wizards/                # 25 wizards step-by-step
│   │   ├── 01-discover/
│   │   ├── 02-plan/
│   │   ├── 03-architect/
│   │   ├── 04-build/
│   │   ├── 05-ship/
│   │   ├── quick/
│   │   └── special/
│   ├── agents/                 # Définitions YAML des agents
│   ├── packs/                  # FinTech, DevOps-Azure, DB
│   ├── memory/                 # Système de mémoire
│   ├── protocols/              # Debate, Envelope
│   └── phases/                 # 13 phases (5 manual + 8 auto)
├── integrations/crewai/        # Agents Python exécutables
├── prompts/                    # Prompts YAML versionnés
├── tools/cli/                  # CLI Node.js
├── docs/                       # Documentation Diataxis
├── tests/                      # Tests JS + Python
└── website/                    # Site Astro
```

---

## 📖 Documentation

| Doc | Contenu |
|-----|---------|
| [Getting Started](./docs/tutorials/getting-started.md) | Premier projet |
| [Installation](./INSTALL.md) | Guide installation |
| [Usage](./USAGE.md) | Utilisation quotidienne |
| [Agents](./AGENTS_LIST.md) | Catalogue agents |
| [Architecture](./ARCHITECTURE.md) | Architecture technique |
| [MDAN Spec FR](./MDAN.fr.md) | Spécification française |
| [Contributing](./CONTRIBUTING.md) | Contribution |

---

## 📄 Licence

MIT

---

<p align="center">
  <strong>25 wizards · 29 agents · 3 packs · Mémoire persistante · Debate Protocol</strong><br>
  Construit avec 🇲🇦 par <a href="https://github.com/khalilbenaz">@khalilbenaz</a>
</p>
