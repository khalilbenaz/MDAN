# MDAN — Multi-Agent Development Agentic Network

![MDAN Banner](https://i.imgur.com/YwfB0Gx.jpeg)

[![Version](https://img.shields.io/npm/v/mdan-cli?color=blue&label=version)](https://www.npmjs.com/package/mdan-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen)](https://nodejs.org)
[![Discord](https://img.shields.io/badge/Discord-Join%20Community-7289da?logo=discord&logoColor=white)](https://discord.gg/mdan)

**Multi-Agent Development Agentic Network** — Une méthode agentique moderne et adaptative pour construire n'importe quel logiciel avec l'IA. MDAN est votre collaborateur expert qui guide le développement de l'analyse jusqu'au déploiement.

**100% gratuit et open source.** Pas de paywall. Pas de contenu bloqué. Nous croyons en l'accessibilité pour tous.

---

## Pourquoi MDAN ?

Les outils IA traditionnels font le travail à votre place, produisant des résultats médiocres. Les agents MDAN et ses workflows structurés agissent comme des collaborateurs experts qui vous guident à travers un processus structuré pour exploiter au maximum votre potentiel en partenariat avec l'IA.

- **🤖 Aide Intelligente IA** — Tapez `/mdan-help` à tout moment pour savoir quoi faire ensuite
- **⚖️ Auto-adaptatif (Scale-Domain)** — Ajuste automatiquement la profondeur de la planification selon la taille du projet (du script solo à l'application d'entreprise)
- **🎉 Party Mode** — Invokequez plusieurs agents avec `/party` pour débattre et collaborer sur des choix d'architecture
- **🧠 Workflow Structuré** — 5 phases claires et éprouvées (DISCOVER, DESIGN, BUILD, VERIFY, SHIP)
- **🔌 Mémoire Persistante** — Reprenez votre travail d'une session à l'autre avec `MDAN-STATE.json`
- **👥 Agents Personnalisés** — Chaque agent a un nom et une personnalité unique (Khalil, Reda, Jihane, Haytame, etc.)
- **✅ Quality Gates** — Portes de qualité adaptatives selon le profil du projet

---

## 🚀 Nouveautés dans MDAN v2.5

**MDAN évolue rapidement avec des optimisations incluant :**

- **MDAN-AUTO v1.0** — Mode de développement autonome sans intervention humaine
- **Context Save/Resume** — Sauvegarde et reprise automatique du contexte à 80% des tokens
- **Multi-Agent Debates** — Débats entre agents pour les décisions complexes
- **Cross Platform Agent Team** — Agents multi-plateformes (Cursor, Windsurf, Claude Code, VS Code)
- **Sub Agent Inclusion** — Sous-agents spécialisés pour des tâches ciblées
- **Skills Architecture** — Architecture de skills extensible et modulable
- **MDAN Builder v1** — Créez vos propres agents et workflows
- **Dev Loop Automation** — Automatisation complète du cycle de développement
- **Better Agents Integration** — Scenarios et evaluations intégrés
- **Templates Génériques** — Templates services externes, .NET Blazor, SQL Server
- **Architecture Modulaire** — Skills extensibles et modules spécialisés

---

## ⚡ Installation

### Option 1 : npm (Recommandé)

```bash
npm install -g mdan-cli
```

### Option 2 : npx (Sans installation)

```bash
npx mdan-cli init mon-projet
```

### Option 3 : Script d'installation

```bash
curl -fsSL https://raw.githubusercontent.com/khalilbenaz/MDAN/main/install.sh | bash
```

Suivez les instructions de l'installeur, puis ouvrez votre IDE IA (Claude Code, Cursor, etc.) dans votre dossier de projet.

---

## 🚀 Démarrage Rapide

```bash
# Créer un nouveau projet
mdan init mon-projet

# Ou attacher à un projet existant
cd mon-projet
mdan attach

# Ouvrir dans votre IDE
cursor .
```

**Pas sûr de quoi faire ?** Tapez `/mdan-help` — cela vous dit exactement quoi faire ensuite.

---

## 🎯 Phases de Développement

| Phase | Agent | Résultat |
|-------|-------|----------|
| **1. DISCOVER** | Product Agent (Khalil) | PRD validé, user stories |
| **2. DESIGN** | Architect (Reda) + UX (Jihane) | Architecture + Specs |
| **3. BUILD** | Dev (Haytame) + Security (Said) | Code implémenté |
| **4. VERIFY** | Test (Youssef) + Security (Said) | Tests passants, sécurité |
| **5. SHIP** | DevOps (Anas) + Doc (Amina) | Déployé + Documenté |

---

## 🤖 Agents Spécialisés

MDAN dispose de 9 agents spécialisés avec personnalité :

| Agent | Nom | Phase | Rôle |
|-------|-----|-------|------|
| Product | Khalil | DISCOVER | PRD, user stories, priorisation |
| Architect | Reda | DESIGN | Architecture, stack, ADR |
| UX | Jihane | DESIGN | Flows, design system, accessibilité |
| Dev | Haytame | BUILD | Code, tests, refactoring |
| Test | Youssef | VERIFY | Tests unitaires, E2E, scénarios |
| Security | Said | BUILD+VERIFY | Vulnérabilités, audit |
| DevOps | Anas | SHIP | CI/CD, déploiement,监控 |
| Doc | Amina | SHIP | Documentation, API docs |
| Learn | - | Toutes | Skills, rules, MCP |

---

## 📦 Modules

MDAN s'étend avec des modules officiels pour domaines spécialisés :

| Module | Description |
|--------|-------------|
| **MDAN Core** | Framework principal avec 5 phases |
| **MDAN-AUTO** | Mode de développement autonome (8 phases) |
| **External Services** | Templates d'intégration services externes génériques |
| **.NET Blazor** | Templates projets .NET 8.0 Blazor Server |
| **SQL Server** | Templates SQL Server (schema, stored procedures, functions) |
| **Azure DevOps** | Skills pour Azure DevOps Services |
| **Agile Scrum** | Workflows Agile/Scrum (Sprint, backlog, retrospectives) |

```bash
# Ajouter un module
mdan module add agile-scrum
```

---

## 📋 Templates Disponibles

MDAN fournit des templates génériques et réutilisables pour accélérer le développement :

### External Services

Templates d'intégration de services externes (APIs, microservices) :

- `IService.cs` — Interface de base pour les services
- `ServiceBase.cs` — Classe de base avec logging et gestion d'erreurs
- `ServiceProvider.cs` — Gestionnaire de dépendances
- `ExampleService.cs` — Exemple d'implémentation

```bash
# Utiliser le template
cp templates/external-services/IService.cs src/Services/
```

### .NET Blazor

Templates pour projets .NET 8.0 Blazor Server :

- Structure de projet standard
- Configuration de base
- Exemples de composants

```bash
# Initialiser un projet Blazor
mdan init mon-projet --template dotnet-blazor
```

### SQL Server

Templates SQL Server pour bases de données :

- `schema.sql` — Schéma de base de données
- `stored-procedures.sql` — Procédures stockées
- `functions.sql` — Fonctions SQL

```bash
# Utiliser les templates SQL
cp templates/sql-server/schema.sql database/
```

---

## 🔧 Fonctionnalités Avancées

### MDAN-AUTO v1.0 — Mode Autonome

Développement entièrement autonome sans intervention humaine :

```bash
# Démarrer le mode autonome
mdan auto

# Reprendre depuis une sauvegarde
mdan resume /tmp/mdan-save-1234567890.json
```

**Phases Autonomes** :
1. **LOAD** — Chargement du contexte et des exigences
2. **DISCOVER** — Analyse des exigences et user stories
3. **PLAN** — Plan d'implémentation détaillé (#PHASE1, #PHASE2...)
4. **ARCHITECT** — Conception de l'architecture système
5. **IMPLEMENT** — Exécution de l'implémentation
6. **TEST** — Tests complets (unitaires, intégration, E2E)
7. **DEPLOY** — Déploiement en production
8. **DOC** — Génération de la documentation

**Fonctionnalités Clés** :
- 🔄 Sauvegarde automatique à 80% des tokens
- 🎯 Débats multi-agents pour décisions complexes
- ⚡ Exécution séquentielle sans pause
- 🚨 Fail-fast sur erreurs critiques
- 📊 Signaux de progression (PHASE X COMPLETE ✅)

### Scenarios (Better Agents)

Tests conversationnels end-to-end pour valider le comportement des agents.

```bash
# Créer un scenario
tests/scenarios/auth.test.md

# Exécuter
npm test -- tests/scenarios/
```

### Evaluations

Benchmarking structuré pour les composants RAG/ML.

```bash
# Évaluer la qualité RAG
langwatch evaluate --dataset customer-support
```

### Prompts Versionnés

Tous les prompts sont versionnés en YAML avec historique.

```bash
# Lister les prompts
mdan prompt list

# Voir un prompt
mdan prompt show orchestrator
```

### MCP Integration

Configuration automatique pour Cursor, Claude Code, Windsurf.

```bash
# Générer la config MCP
mdan mcp init
```

---

## 📖 Commandes

```bash
mdan init [nom]           # Créer un nouveau projet
mdan attach [--rebuild]   # Ajouter MDAN à un projet existant
mdan status               # Voir le statut du projet
mdan phase [1-5]         # Afficher le guide d'une phase
mdan workflow [nom]      # Afficher un workflow détaillé
mdan module add [nom]    # Installer un module
mdan oc                  # Copier l'orchestrateur
mdan agent [nom]         # Voir un agent
mdan skills              # Lister les skills
mdan auto                # Démarrer le mode autonome
mdan resume <save-file>  # Reprendre depuis une sauvegarde
mdan mcp [action]        # Config MCP
mdan prompt [action]     # Gérer les prompts
```

---

## 🔌 IDE Supportés

- **Cursor** — `.cursorrules` auto-généré
- **Windsurf** — `.windsurfrules` auto-généré
- **Claude Code** — `.claude/skills/` auto-généré
- **VS Code** — Via MCP
- **GitHub Copilot** — `.github/copilot-instructions.md`

---

## 📁 Structure du Projet

```
projet/
├── mdan/
│   ├── orchestrator.md      # System prompt principal
│   ├── universal-envelope.md
│   ├── agents/              # Prompts des agents
│   │   ├── dev.md
│   │   ├── test.md
│   │   └── ...
│   └── skills/              # Skills installés
├── tests/
│   ├── scenarios/           # Tests conversationnels
│   └── evaluations/        # Évaluations benchmarks
├── templates/
│   ├── external-services/   # Templates services externes génériques
│   ├── dotnet-blazor/       # Templates .NET 8.0 Blazor Server
│   ├── sql-server/          # Templates SQL Server
│   ├── prompts/             # Prompts versionnés (YAML)
│   └── prompts.json         # Registre des prompts
├── phases/
│   ├── auto-01-load.md      # Phase LOAD (autonome)
│   ├── auto-02-discover.md  # Phase DISCOVER (autonome)
│   ├── auto-03-plan.md      # Phase PLAN (autonome)
│   ├── auto-04-architect.md # Phase ARCHITECT (autonome)
│   ├── auto-05-implement.md # Phase IMPLEMENT (autonome)
│   ├── auto-06-test.md      # Phase TEST (autonome)
│   ├── auto-07-deploy.md    # Phase DEPLOY (autonome)
│   └── auto-08-doc.md       # Phase DOC (autonome)
├── mdan_output/            # Artifacts générés par les agents
├── .cursorrules            # Pour Cursor
├── .windsurfrules         # Pour Windsurf
├── .claude/skills/        # Pour Claude Code
├── .github/               # Pour Copilot
├── .mcp.json             # Configuration MCP
├── AGENTS.md              # Guidelines de développement
└── MDAN-STATE.json        # État de la session
```

---

## 🏗️ Architecture Technique

MDAN se compose de plusieurs composants interconnectés :

| Composant | Rôle |
|-----------|------|
| **MDAN Core** | Orchestrateur central qui coordonne les agents |
| **Agents** | 9 agents spécialisés avec personnalité |
| **CLI** | Interface en ligne de commande |
| **Memory** | Persistance entre sessions |
| **Skills** | Compétences optionnelles extensibles |
| **Scenarios** | Tests conversationnels |
| **Evaluations** | Benchmarking de composants |
| **Prompts** | Versionnage YAML |

---

## 🧪 Tests et Qualité

MDAN inclut une suite de tests complète pour garantir la qualité du code :

### Framework de Tests

- **pytest** — Framework de tests Python
- **pytest-cov** — Couverture de code
- **pytest-mock** — Mocking pour tests

### Types de Tests

| Type | Description | Emplacement |
|------|-------------|-------------|
| **Tests CLI** | Commandes CLI (init, attach, auto, etc.) | `tests/test_cli.py` |
| **Tests Templates** | Validation des templates | `tests/test_templates.py` |
| **Tests Services** | Patterns services externes | `tests/test_external_services.py` |
| **Tests Installation** | Vérification installation | `tests/test_installation.py` |
| **Tests Régression** | Pas de références wallet | `tests/test_regression.py` |

### Exécuter les Tests

```bash
# Tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=cli --cov-report=html

# Tests spécifiques
pytest tests/test_cli.py -v
```

### CI/CD

GitHub Actions configurés pour :

- **Tests automatiques** à chaque push
- **Linting** avec ruff et mypy
- **Couverture de code** minimale 80%

```bash
# Workflows CI/CD
.github/workflows/test.yml
.github/workflows/lint.yml
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Architecture technique |
| [MDAN.md](MDAN.md) | Spécification complète |
| [AGENTS.md](AGENTS.md) | Guidelines de développement |
| [docs/fr/](docs/fr/) | Documentation en français |

---

## 🔗 Liens

- [GitHub](https://github.com/khalilbenaz/MDAN)
- [NPM](https://www.npmjs.com/package/mdan-cli)
- [Documentation](https://github.com/khalilbenaz/MDAN#readme)
- [Discord](https://discord.gg/mdan)

---

## 📄 Licence

MIT License — voir [LICENSE](LICENSE) pour les détails.

---
