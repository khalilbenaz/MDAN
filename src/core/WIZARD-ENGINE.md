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
- 🧠 **TOUJOURS** sauvegarder dans MDAN-STATE à la fin du wizard
- 📋 **JAMAIS** créer de todo lists mentales à partir des steps futurs
- 🗣️ **TOUJOURS** parler dans la langue configurée (communication_language)
- 📝 **TOUJOURS** rédiger les documents dans la langue configurée (document_output_language)

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
