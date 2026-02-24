# MDAN — Multi-Agent Development Agentic Network

> Une méthode agentique moderne pour construire n'importe quel logiciel avec l'IA.

---

## 🌟 Pourquoi MDAN v2 ?

MDAN v2 a été repensé pour être un véritable collaborateur expert plutôt qu'un simple outil de génération de code.

- **🤖 Aide Intelligente IA** — Tapez `/mdan-help` à tout moment pour savoir quoi faire ensuite
- **⚖️ Auto-adaptatif (Scale-Domain)** — Ajuste automatiquement la profondeur de la planification selon la taille de votre projet (du script solo à l'application d'entreprise)
- **🎉 Party Mode** — Invoquez plusieurs agents avec `/party` pour débattre et collaborer sur des choix d'architecture ou de design
- **🧠 Workflow Structuré** — 5 phases claires et éprouvées (Discover, Design, Build, Verify, Ship)
- **🔌 Mémoire Persistante** — Avec le fichier `MDAN-STATE.json` qui vous permet de reprendre votre travail d'une session à l'autre

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

### Option 4 : Manuel

```bash
git clone https://github.com/khalilbenaz/MDAN.git
cd MDAN && bash install.sh
```

---

## 🚀 Utilisation

### Nouveau projet

```bash
mdan init mon-projet
cursor mon-projet
```

### Projet existant

```bash
cd votre-projet
mdan attach
cursor .
```

### Rebuild from scratch

```bash
cd votre-projet
mdan attach --rebuild
cursor .
```

---

## 📖 Commandes

MDAN v2 propose un installeur **interactif** : tapez simplement `mdan` pour être guidé ! 

Vous pouvez aussi utiliser les commandes directes :

```bash
mdan init                 # Lancer l'assistant de création (Wizard)
mdan init [nom]           # Créer un nouveau projet directement
mdan attach               # Ajouter MDAN au projet courant
mdan attach --rebuild     # Préparer pour un rebuild complet
mdan status               # Voir le statut du projet
mdan phase [1-5|nom]      # Voir le guide d'une phase (ex: mdan phase discover)
mdan workflow [nom]       # Voir une micro-procédure (ex: bug-fix, refactoring)
mdan module add [nom]     # Ajouter une extension métier (ex: agile-scrum)
mdan oc                   # Copier le prompt de l'Orchestrateur dans le presse-papier
mdan agent [nom]          # Voir le prompt d'un agent
mdan skills               # Lister les skills
mdan mcp [action]        # MCP config (init|validate|list)
mdan prompt [action]     # Gérer les prompts (list|show)
mdan version              # Version
```

*Astuce : Vous pouvez ajouter `copy` ou `-c` à la fin des commandes `phase` ou `workflow` pour copier le contenu directement dans votre presse-papier (ex: `mdan phase 1 copy`).*

---

## 🎯 Workflow

| Phase | Agent | Résultat |
|-------|-------|----------|
| **1. DISCOVER** | Product Agent | PRD validé |
| **2. DESIGN** | Architect + UX | Architecture + Specs |
| **3. BUILD** | Dev + Security | Code implémenté |
| **4. VERIFY** | Test + Security | Tests passants |
| **5. SHIP** | DevOps + Doc | Déployé + Documenté |

---

## 🤖 Agents

| Agent | Phase | Rôle |
|-------|-------|------|
| Learn Agent | Toutes | Skills, rules, MCP |
| Product Agent | DISCOVER | PRD, user stories |
| Architect Agent | DESIGN | Architecture, stack |
| UX Agent | DESIGN | Flows, design system |
| Dev Agent | BUILD | Code, tests unitaires |
| Security Agent | BUILD+VERIFY | Vulnérabilités |
| Test Agent | VERIFY | Tests E2E, perf |
| DevOps Agent | SHIP | CI/CD, infra |
| Doc Agent | SHIP | Documentation |

---

## 💡 Exemples de prompts

### Nouveau projet
```
MDAN: Je veux créer une app de gestion de tâches avec auth, 
dashboard et notifications. Commence par DISCOVER.
```

### Projet existant
```
MDAN: Analyse ce projet et propose des améliorations.
Identifie la dette technique et suggère des optimizations.
```

### Rebuild complet
```
MDAN REBUILD: Analyse tout le code existant, documente 
chaque feature, et propose une architecture moderne 
pour tout réécrire from scratch.
```

---

## 🔌 IDE Supportés

- **Cursor** — `.cursorrules` auto-généré
- **Windsurf** — `.windsurfrules` auto-généré
- **Claude Code** — `.claude/skills/` auto-généré
- **GitHub Copilot** — `.github/copilot-instructions.md` auto-généré
- **Claude Web** — Copier `mdan/orchestrator.md`

---

## 📁 Structure créée

```
projet/
├── mdan/
│   ├── orchestrator.md      # System prompt
│   ├── agents/              # Prompts des agents
│   ├── skills/              # Skills installés
│   └── STATUS.md            # Progression
├── tests/
│   ├── scenarios/           # Tests conversationnels (Better Agents)
│   └── evaluations/        # Évaluations (RAG, classification)
├── templates/
│   ├── prompts/             # Prompts versionnés (YAML)
│   └── prompts.json         # Registre des prompts
├── mdan_output/             # Dossier où les agents génèrent leurs livrables (PRD, Archi...)
├── .cursorrules             # Pour Cursor
├── .windsurfrules           # Pour Windsurf
├── .claude/skills/          # Pour Claude Code
├── .github/copilot-instructions.md
├── .mcp.json               # Configuration MCP
└── AGENTS.md               # Guidelines de développement
```

### Fonctionnalités Better Agents intégrées

| Feature | Description |
|---------|-------------|
| **Scenarios** | Tests conversationnels end-to-end dans `tests/scenarios/` |
| **Evaluations** | Benchmarking structuré (RAG, classification) dans `tests/evaluations/` |
| **Prompts** | Versionnage des prompts en YAML dans `templates/prompts/` |
| **MCP** | Configuration pour Cursor/Claude via `.mcp.json` |
| **AGENTS.md** | Guidelines de développement (copie de Better Agents) |

---

## 📄 Licence

MIT — Libre d'utilisation.

---

## 🏗️ Architecture

MDAN se compose de plusieurs composants interconnectés:

| Composant | Rôle |
|-----------|------|
| **MDAN Core** | Orchestrateur central qui coordonne les agents |
| **Agents** | 9 agents spécialisés (Product, Architect, UX, Dev, etc.) |
| **CLI** | Interface en ligne de commande (`mdan init`, `mdan attach`) |
| **Memory** | Système de persistance entre sessions (`MDAN-STATE.json`) |
| **Skills** | Compétences optionnelles extensibles |
| **Scenarios** | Tests conversationnels (Better Agents) |
| **Evaluations** | Benchmarking de composants (Better Agents) |
| **Prompts** | Versionnage YAML des prompts |

```
Utilisateur → CLI → MDAN Core → Agents → Artifacts
                            ↓
                        Memory System
```

Voir [ARCHITECTURE.md](ARCHITECTURE.md) pour la documentation technique complète.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Architecture technique du projet |
| [MDAN.md](MDAN.md) | Spécification complète de la méthode |
| [CLI-REFERENCE.md](docs/fr/CLI-REFERENCE.md) | Référence des commandes CLI |
| [CONTRIBUTING-DEV.md](docs/fr/CONTRIBUTING-DEV.md) | Guide du contributeur développeur |
| [Exemple complet](examples/taskflow-api/EXAMPLE.md) | Projet exemple TaskFlow API |

---

## 🔗 Liens

- [Documentation EN](docs/en/README.md)
- [Documentation FR](docs/fr/README.md)
- [GitHub](https://github.com/khalilbenaz/MDAN)
- [NPM](https://www.npmjs.com/package/mdan-cli)
- [Better Agents](https://langwatch.ai/docs/better-agents) — Fonctionnalités de test intégrées
