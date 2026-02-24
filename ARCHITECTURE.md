# MDAN — Architecture du Projet

> Documentation technique de la structure et des composants de MDAN v2.2.0

---

## Vue d'ensemble

MDAN (Multi-Agent Development Agentic Network) est une méthodologie agentique pour le développement logiciel assisté par IA. Le projet se compose de :

- **Un orchestrateur central** (MDAN Core) qui coordonne les agents
- **Neuf agents spécialisés** pour chaque phase du développement
- **Une CLI** multi-plateformes pour initialiser et gérer les projets
- **Un système de mémoire** pour la persistance entre sessions
- **Des intégrations IDE** pour Cursor, Windsurf, Claude Code, Copilot

```
┌─────────────────────────────────────────────────────────────────┐
│                         UTILISATEUR                              │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    CLI (mdan)                            │    │
│  │   init | attach | status | phase | agent | skills       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   MDAN Core                              │    │
│  │              (Orchestrateur Central)                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           │                                      │
│           ┌───────────────┼───────────────┐                     │
│           ▼               ▼               ▼                     │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐                │
│    │  Agents  │    │  Memory  │    │  Skills  │                │
│    │ Spécial. │    │  System  │    │ Option.  │                │
│    └──────────┘    └──────────┘    └──────────┘                │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Intégrations IDE                            │    │
│  │   Cursor │ Windsurf │ Claude Code │ Copilot             │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Structure des Dossiers

```
MDAN/
├── cli/                    # Interface en ligne de commande
│   ├── mdan.js            # CLI principale (Node.js)
│   ├── mdan.sh            # CLI alternative (Bash)
│   ├── mdan.py            # CLI alternative (Python)
│   └── postinstall.js     # Script post-installation npm
│
├── core/                   # Composants centraux
│   ├── orchestrator.md     # System prompt MDAN Core v2
│   └── universal-envelope.md # Format standard des agents
│
├── agents/                 # Définitions des agents
│   ├── AGENTS-REGISTRY.md  # Système de versioning
│   ├── product.md          # Agent Phase 1: DISCOVER
│   ├── architect.md        # Agent Phase 2: DESIGN
│   ├── ux.md               # Agent Phase 2: DESIGN
│   ├── dev.md              # Agent Phase 3: BUILD
│   ├── security.md         # Agent Phase 3-4: BUILD/VERIFY
│   ├── test.md             # Agent Phase 4: VERIFY
│   ├── devops.md           # Agent Phase 5: SHIP
│   ├── doc.md              # Agent Phase 5: SHIP
│   └── learn.md            # Agent transverse: Skills
│
├── phases/                 # Guides détaillés des phases
│   ├── 01-discover.md
│   ├── 02-design.md
│   ├── 03-build.md
│   ├── 04-verify.md
│   └── 05-ship.md
│
├── templates/              # Templates d'artifacts
│   ├── PRD.md              # Product Requirements Document
│   ├── ARCHITECTURE.md     # Document d'architecture
│   ├── SECURITY-REVIEW.md  # Revue de sécurité
│   ├── TEST-PLAN.md        # Plan de test
│   ├── CHANGELOG.md        # Journal des modifications
│   └── MDAN-KNOWLEDGE.md   # Base de connaissances
│
├── memory/                 # Système de persistance
│   ├── MEMORY-SYSTEM.md    # Documentation du système
│   └── MDAN-STATE.template.json # Template d'état
│
├── skills/                 # Compétences optionnelles
│   └── find-skills/        # Skill de découverte
│       └── skill.md
│
├── integrations/           # Intégrations IDE
│   ├── all-integrations.md # Vue d'ensemble
│   ├── cursor.md
│   ├── windsurf.md
│   └── claude.md
│
├── docs/                   # Documentation utilisateur
│   ├── en/                 # Anglais
│   └── fr/                 # Français
│
├── examples/               # Projets exemples
│   └── taskflow-api/       # Exemple complet
│       ├── EXAMPLE.md
│       └── MDAN-STATE.json
│
├── install.sh              # Script d'installation
├── package.json            # Configuration npm
├── README.md               # Documentation principale
├── CONTRIBUTING.md         # Guide de contribution
├── MDAN.md                 # Spécification complète
└── MDAN.fr.md              # Spécification (FR)
```

---

## Composants Principaux

### 1. MDAN Core (Orchestrateur)

**Fichier:** `core/orchestrator.md`

L'orchestrateur central est le cerveau de MDAN. Il :

- Détecte automatiquement le type de projet (MICRO, STANDARD, PRODUCT, ENTERPRISE, API-ONLY, DATA/ML)
- Coordonne les agents spécialisés
- Gère les transitions de phases avec quality gates
- Maintient le contexte global du projet
- Génère et met à jour `MDAN-STATE.json`

**Comportement:**
```
1. Recevoir la description du projet
2. Détecter le profil (MICRO/STANDARD/PRODUCT/ENTERPRISE/API-ONLY/DATA)
3. Annoncer le profil et les adaptations
4. Poser les 5 questions de discovery
5. Activer le Product Agent
6. Présenter le PRD pour validation
7. Vérifier le quality gate
8. Passer à la phase suivante
```

### 2. Agents Spécialisés

Chaque agent suit le format **Universal Envelope** :

```
[MDAN-AGENT]
NAME: [Nom]
VERSION: [X.Y.Z]
ROLE: [Description courte]
PHASE: [Phase(s)]
REPORTS_TO: MDAN Core

[IDENTITY]      → Qui est l'agent (expertise, mindset)
[CAPABILITIES]  → Ce qu'il peut faire
[CONSTRAINTS]   → Ce qu'il ne doit PAS faire
[INPUT_FORMAT]  → Ce qu'il attend de MDAN Core
[OUTPUT_FORMAT] → Structure de sa réponse
[QUALITY_CHECKLIST] → Auto-validation
[ESCALATION]    → Quand remonter à MDAN Core
[/MDAN-AGENT]
```

| Agent | Phase | Responsabilité |
|-------|-------|----------------|
| Product | DISCOVER | PRD, user stories, personas |
| Architect | DESIGN | Architecture, stack technique, ADRs |
| UX | DESIGN | Design system, flows, états UI |
| Dev | BUILD | Implémentation, tests unitaires |
| Security | BUILD+VERIFY | Revue de sécurité, vulnérabilités |
| Test | VERIFY | Tests E2E, performance, intégration |
| DevOps | SHIP | CI/CD, déploiement, infra |
| Doc | SHIP | Documentation, README, API docs |
| Learn | Toutes | Skills, MCP, règles métier |

### 3. CLI (Command Line Interface)

**Fichiers:** `cli/mdan.js`, `cli/mdan.sh`, `cli/mdan.py`

La CLI offre plusieurs implémentations pour la compatibilité :

| Commande | Description |
|----------|-------------|
| `mdan init [nom]` | Créer un nouveau projet |
| `mdan attach [--rebuild]` | Ajouter MDAN à un projet existant |
| `mdan status` | Voir le statut du projet |
| `mdan phase [1-5]` | Afficher le guide d'une phase |
| `mdan oc` | Copier le prompt de l'Orchestrateur dans le presse-papier |
| `mdan agent [nom]` | Afficher le prompt d'un agent |
| `mdan skills` | Lister les skills disponibles |
| `mdan version` | Afficher la version |

**Fichiers générés par `mdan init`:**
```
projet/
├── mdan/
│   ├── orchestrator.md      # System prompt
│   ├── universal-envelope.md
│   ├── agents/              # Prompts des agents
│   └── skills/              # Skills installés
├── docs/                    # Templates d'artifacts
├── .cursorrules             # Pour Cursor
├── .windsurfrules           # Pour Windsurf
├── .claude/skills/          # Pour Claude Code
└── .github/copilot-instructions.md
```

### 4. Memory System

**Fichier:** `memory/MEMORY-SYSTEM.md`

Le système de mémoire résout le problème de perte de contexte entre sessions LLM.

**Fichier d'état:** `MDAN-STATE.json`
```json
{
  "mdan_version": "2.2.0",
  "project": { "name", "type", "created_at", "last_updated" },
  "current_phase": "BUILD",
  "phase_history": [...],
  "agents_used": { "dev": "2.0.0", ... },
  "features": [{ "id", "title", "status", "files", "tests" }],
  "decisions": [{ "id", "title", "rationale" }],
  "open_issues": [...],
  "tech_stack": {...},
  "llm_history": [...]
}
```

**Protocole de reprise:**
```
1. Utilisateur colle MDAN-STATE.json
2. MDAN Core reconstruit le contexte
3. Affiche le résumé de progression
4. Propose la prochaine action
```

### 5. Skills System

**Dossier:** `skills/`

Les skills sont des capacités optionnelles extensibles :

```
skills/
└── [skill-name]/
    ├── skill.md           # Définition du skill
    ├── templates/         # Templates spécifiques
    └── examples/          # Exemples d'utilisation
```

**Intégration:**
- Copiés dans `mdan/skills/` lors de `mdan init`
- Copiés dans `.claude/skills/` pour Claude Code
- Référencés par le Learn Agent

---

## Flux de Données

### Workflow en 5 Phases

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  DISCOVER   │───▶│   DESIGN    │───▶│   BUILD     │
│             │    │             │    │             │
│ Product     │    │ Architect   │    │ Dev         │
│ Agent       │    │ UX Agent    │    │ Security    │
└─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │
      ▼                  ▼                  ▼
   [Gate 1]          [Gate 2]           [Gate 3]
      │                  │                  │
      │                  │                  ▼
      │                  │           ┌─────────────┐
      │                  │           │   VERIFY    │
      │                  │           │             │
      │                  │           │ Test        │
      │                  │           │ Security    │
      │                  │           └─────────────┘
      │                  │                  │
      │                  │                  ▼
      │                  │              [Gate 4]
      │                  │                  │
      │                  │                  ▼
      │                  │           ┌─────────────┐
      │                  │           │    SHIP     │
      │                  │           │             │
      │                  │           │ DevOps      │
      │                  │           │ Doc         │
      │                  │           └─────────────┘
      │                  │                  │
      ▼                  ▼                  ▼
    PRD.md        ARCHITECTURE.md     Code + Tests
                  UX-SPEC.md          SECURITY-REVIEW.md
                                      TEST-PLAN.md
                                      Deploy + Docs
```

### Quality Gates

Chaque transition de phase est validée par un quality gate :

| Gate | Critères clés |
|------|---------------|
| 1: DISCOVER→DESIGN | PRD validé, personas définis, MoSCoW complet, métriques mesurables |
| 2: DESIGN→BUILD | Architecture complète, stack définie, UX spec validée, ADRs documentés |
| 3: BUILD→VERIFY | Features implémentées, tests unitaires, pas de vulnérabilités critiques |
| 4: VERIFY→SHIP | Tests passants, couverture OK, sécurité validée, docs complètes |

---

## Universal Envelope

**Fichier:** `core/universal-envelope.md`

L'Universal Envelope assure la compatibilité multi-LLM :

| LLM | Format Recommandé |
|-----|-------------------|
| Claude | Tags XML `[SECTION]` |
| ChatGPT/GPT-4 | Headers markdown `## SECTION` |
| Gemini | Headers markdown uniquement |
| Qwen/GLM/Kimi | Tags XML ou markdown |

**Structure:**
```
[MDAN-AGENT]
NAME / VERSION / ROLE / PHASE / REPORTS_TO
[IDENTITY]
[CAPABILITIES]
[CONSTRAINTS]
[INPUT_FORMAT]
[OUTPUT_FORMAT]
[QUALITY_CHECKLIST]
[ESCALATION]
[/MDAN-AGENT]
```

---

## Système de Versioning

**Fichier:** `agents/AGENTS-REGISTRY.md`

### Schéma SemVer

```
MAJOR.MINOR.PATCH

MAJOR: Changement de comportement ou format de sortie (breaking)
MINOR: Nouvelle capacité rétrocompatible
PATCH: Correction mineure (typos, exemples)
```

### Header de version

Chaque agent inclut :
```markdown
# MDAN — [Agent Name]
<!-- version: 2.0.0 -->
<!-- last-updated: 2025-01-20 -->
<!-- breaking-changes-from: 1.x -->
```

### Détection de mise à jour

MDAN Core compare les versions au démarrage :
```
Project uses: dev agent v1.0.0
Current MDAN:  dev agent v2.0.0 (MAJOR)

⚠️  Breaking changes detected
Options: [1] Keep v1.0.0  [2] Upgrade to v2.0.0
```

---

## Intégrations IDE

| IDE | Fichier généré | Contenu |
|-----|----------------|---------|
| Cursor | `.cursorrules` | orchestrator.md + instructions |
| Windsurf | `.windsurfrules` | orchestrator.md + instructions |
| Claude Code | `.claude/skills/` | Skills copiés |
| GitHub Copilot | `.github/copilot-instructions.md` | orchestrator.md |
| Claude Web | Copie manuelle | `mdan/orchestrator.md` |

---

## Dépendances

### Runtime

- **Node.js** >= 14.0.0 (pour CLI npm)
- **Bash** (pour install.sh)
- **Python 3** (optionnel, pour CLI alternative)

### Aucune dépendance externe

MDAN fonctionne sans dépendances npm externes. Tout est en fichiers markdown et scripts shell.

---

## Points d'Extension

### Ajouter un agent

1. Créer `agents/[nom].md` avec l'Universal Envelope
2. Ajouter au registre dans `AGENTS-REGISTRY.md`
3. Mettre à jour la CLI pour le supporter

### Ajouter un skill

1. Créer `skills/[nom]/skill.md`
2. Optionnel: ajouter templates/examples
3. Le Learn Agent peut maintenant le référencer

### Ajouter une intégration

1. Créer `integrations/[ide].md`
2. Mettre à jour `integrations/all-integrations.md`
3. Modifier la CLI pour générer les fichiers appropriés

---

## Fichiers Critiques

| Fichier | Rôle | Impact si supprimé |
|---------|------|-------------------|
| `core/orchestrator.md` | System prompt principal | CLI non fonctionnelle |
| `core/universal-envelope.md` | Format des agents | Incohérence multi-LLM |
| `cli/mdan.js` | CLI principale | Commandes `mdan` non disponibles |
| `package.json` | Configuration npm | Installation npm impossible |
| `install.sh` | Installation manuelle | Installation sans npm impossible |
