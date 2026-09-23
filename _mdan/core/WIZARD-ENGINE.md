# MDAN Wizard Engine v3.0

Le moteur de wizards est le cœur de MDAN. Il orchestre les workflows step-by-step avec des capacités que MDAN n'a pas.

## Architecture

```
wizard.md          → Définition du wizard (goal, role, init)
  └── steps/
       ├── step-01-init.md     → Initialisation + détection continuation
       ├── step-02-*.md        → Étapes séquentielles
       └── step-XX-complete.md → Finalisation + quality gate
  └── templates/
       └── output-template.md  → Template du document de sortie
```

## Principes fondamentaux

### 1. Step-File Architecture (comme MDAN)
- Chaque étape = 1 fichier isolé chargé en Just-In-Time
- Exécution séquentielle stricte, jamais de skip
- État suivi dans le frontmatter du document de sortie

### 2. Mémoire Cross-Wizard (MDAN exclusif)
Contrairement à MDAN où chaque wizard est isolé, MDAN maintient un état global :
- `MDAN-STATE.json` persiste entre les wizards ET entre les sessions
- Les décisions de l'architecte sont automatiquement disponibles pour le dev
- Le context summary est mis à jour à chaque fin de wizard
- Les observations des agents sont accumulées

### 3. Scale-Adaptive (MDAN exclusif)
Le moteur détecte automatiquement la complexité du projet et ajuste :
- **Solo** (< 5 stories) → Wizards simplifiés, steps fusionnés, pas de debate obligatoire
- **Team** (5-50 stories) → Wizards complets, debate sur architecture
- **Enterprise** (50+ stories) → Tous les quality gates, debates obligatoires, documentation complète

### 4. Debate Integration (MDAN exclusif)
Quand un wizard atteint une décision critique :
- Le moteur peut invoquer automatiquement 2-3 agents pour débattre
- Le debate protocol structure les arguments pour/contre
- L'utilisateur tranche, la décision est enregistrée dans MDAN-STATE

**v3: Multi-Mode Orchestration**
Party Mode supporte désormais 3 modes :
- **Discussion** — Mode original, conversation libre multi-agent
- **Debate** — Argumentation structurée à 3 rôles (proponent, opponent, arbitrator) avec Decision Records
- **Consensus** — N agents convergent vers une position commune via des phases structurées

Les protocols structurés sont définis dans :
- `party-mode/protocols/turn-protocol.md` — Tours de parole structurés avec contraintes
- `party-mode/protocols/memory-protocol.md` — Accumulation de mémoire agent

Les Decision Records sont automatiquement enregistrés dans le Context Graph.

### 4b. Context Graph Integration (MDAN v3)
Chaque wizard enregistre automatiquement ses artifacts dans le Context Graph :
- Le Context Graph est un DAG léger en JSON (`_mdan/state/context-graph.json`)
- Chaque noeud = artifact (PRD, architecture, epic, etc.)
- Chaque edge = relation (input_to, derived_from, impacts, references)
- `mdan impact <artifact>` montre l'analyse d'impact en aval
- `mdan graph` génère un diagramme Mermaid du graphe
- Les Decision Records des débats sont aussi des noeuds du graphe

### 4c. Agent Memory Sidecars
Les agents maintiennent une mémoire persistante entre les sessions :
- Stockée dans `_mdan/state/sidecars/{agent-name}.sidecar.json` (max 50 souvenirs, les moins sûrs sont élagués)
- Injectée automatiquement quand un agent est chargé (`mdan_consult_agent`, `mdan_party_mode`)
- Écriture : `mdan_memory_remember` (un souvenir identique est renforcé, pas dupliqué)
- Fin de session : `mdan_memory_end_session` (compteur de sessions, relations, decision history)
- Memory decay : la confiance baisse après 5 sessions sans renforcement ; sous 0.3 le souvenir est oublié
- CLI : `mdan memory [agent]`

### 4d. Progression et reprise
- Début de wizard : `mdan_state_update { action: "start" }` ; à chaque step : `action: "step"` ; fin : `action: "complete"` avec les artifacts
- `mdan_run_workflow` indique le point de reprise si le wizard a été interrompu
- `mdan status` / `mdan_status` : phase courante, artifacts, décisions, prochaine étape recommandée
- Sans outils MCP : mettre à jour `_mdan/state/MDAN-STATE.json` directement

### 5. Quality Gates Adaptatifs (MDAN exclusif)
À la fin de chaque wizard, un quality gate vérifie :
- Complétude du document (sections remplies)
- Cohérence avec les artifacts précédents
- Score de confiance (basé sur le nombre de questions résolues)
Le gate s'adapte au scale : strict en Enterprise, souple en Solo.

## Règles universelles (identiques pour TOUS les wizards)

- 🛑 **JAMAIS** charger plusieurs step files en même temps
- 📖 **TOUJOURS** lire le step file en entier avant d'agir
- 🚫 **JAMAIS** sauter d'étapes ou optimiser la séquence
- 💾 **TOUJOURS** mettre à jour le frontmatter avant de passer au step suivant
- ⏸️ **TOUJOURS** s'arrêter aux menus et attendre l'input utilisateur
- 🧠 **TOUJOURS** enregistrer la progression (`mdan_state_update`) et, en fin de wizard, les artifacts produits
- 📋 **JAMAIS** créer de todo lists mentales à partir des steps futurs
- 🗣️ **TOUJOURS** appliquer `{project-root}/_mdan/core/rules.md` (langue des échanges selon `communication_language`, langue des documents selon `document_output_language`)

## Format standard d'un step file

```markdown
---
name: 'step-XX-nom'
description: 'Ce que fait ce step'
nextStepFile: 'chemin/vers/step-suivant.md'
outputFile: '{planning_artifacts}/nom-output.md'
---

# Step XX: Titre

## STEP GOAL:
[Objectif clair de cette étape]

## MANDATORY EXECUTION RULES (READ FIRST):
[Règles spécifiques à ce step]

## CONTEXT BOUNDARIES:
[Ce qui est disponible, ce qui ne l'est pas]

## Sequence of Instructions:
### 1. [Première action]
### 2. [Deuxième action]
### N. Present MENU OPTIONS

## CRITICAL STEP COMPLETION NOTE
[Condition de passage au step suivant]

## 🚨 SYSTEM SUCCESS/FAILURE METRICS
### ✅ SUCCESS: [critères]
### ❌ FAILURE: [critères]
```
