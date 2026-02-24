# MDAN — Guide du Contributeur Développeur

> Comment étendre, modifier et contribuer au code de MDAN

---

## Table des Matières

1. [Configuration de l'environnement](#configuration-de-lenvironnement)
2. [Architecture du code](#architecture-du-code)
3. [Créer un agent](#créer-un-agent)
4. [Créer un skill](#créer-un-skill)
5. [Ajouter un template](#ajouter-un-template)
6. [Règles de versioning](#règles-de-versioning)
7. [Tests et validation](#tests-et-validation)
8. [Process de Pull Request](#process-de-pull-request)

---

## Configuration de l'environnement

### Prérequis

- **Node.js** >= 14.0.0
- **Git**
- Un éditeur de texte (Cursor, VS Code, etc.)

### Cloner et installer

```bash
# Cloner le repository
git clone https://github.com/khalilbenaz/MDAN.git
cd MDAN

# Tester la CLI localement
node cli/mdan.js help

# Installation globale pour tests
npm link
mdan help
```

### Structure de développement

```
MDAN/
├── cli/                    # Code de la CLI à modifier
├── core/                   # Orchestrateur à modifier
├── agents/                 # Agents à modifier/créer
├── templates/              # Templates à modifier/créer
├── skills/                 # Skills à créer
├── memory/                 # Système mémoire
├── tests/                  # Tests (à créer)
└── package.json            # Configuration npm
```

---

## Architecture du code

### CLI (`cli/mdan.js`)

La CLI est un script Node.js pur sans dépendances externes.

**Structure:**
```javascript
// Constants
const VERSION = '2.2.0';
const MDAN_DIR = path.resolve(__dirname, '..');

// Fonctions principales
function banner() { ... }        // Affiche le logo
function showHelp() { ... }      // Affiche l'aide
function cmdInit(name) { ... }   // Commande init
function cmdAttach(rebuild) { .. } // Commande attach
function cmdStatus() { ... }     // Commande status
function cmdPhase(num) { ... }   // Commande phase
function cmdAgent(name) { ... }  // Commande agent
function cmdSkills() { ... }     // Commande skills

// Point d'entrée
switch (cmd) {
  case 'init': cmdInit(args[0]); break;
  // ...
}
```

**Pour ajouter une commande:**

1. Ajouter une fonction `cmdNouvelleCommande()`
2. Ajouter le case dans le switch
3. Mettre à jour `showHelp()`

### Orchestrateur (`core/orchestrator.md`)

L'orchestrateur est un prompt markdown pur. Il définit:

- Détection du profil projet
- Workflow adaptatif
- Protocole de reprise de session
- Quality gates

**Pour modifier l'orchestrateur:**
1. Éditer `core/orchestrator.md`
2. Tester avec plusieurs LLMs (Claude, GPT-4, Gemini)
3. Valider que le comportement reste cohérent

### Agents (`agents/*.md`)

Chaque agent suit le format Universal Envelope.

---

## Créer un agent

### Étape 1: Créer le fichier

Créer `agents/[nom].md`:

```markdown
# MDAN — [Agent Name]

```
[MDAN-AGENT]
NAME: [Agent Name]
VERSION: 1.0.0
ROLE: [Description en une ligne du rôle]
PHASE: [Phase(s) où l'agent opère]
REPORTS_TO: MDAN Core

[IDENTITY]
[Qui est cet agent - expertise, expérience, mindset]

[CAPABILITIES]
- [Capacité 1]
- [Capacité 2]
- [Capacité 3]

[CONSTRAINTS]
- Do NOT [contrainte 1]
- Do NOT [contrainte 2]

[INPUT_FORMAT]
MDAN Core fournira:
- [Élément 1]
- [Élément 2]

[OUTPUT_FORMAT]
---
Artifact: [Nom de l'artifact]
Phase: [Phase]
Agent: [Agent Name]
Version: 1.0
Status: Draft
---

[Structure de sortie attendue]

[QUALITY_CHECKLIST]
Avant de soumettre, vérifier:
- [ ] [Critère 1]
- [ ] [Critère 2]

[ESCALATION]
Remonter à MDAN Core si:
- [Condition 1]
- [Condition 2]
[/MDAN-AGENT]
```

### Étape 2: Définir l'IDENTITY

L'identité définit la personnalité et l'expertise de l'agent.

**Exemple (Dev Agent):**
```markdown
[IDENTITY]
You are a senior full-stack developer with 15+ years of experience. 
You write clean, well-documented, secure code. You follow SOLID 
principles, DRY, and YAGNI. You never write code you don't understand.
```

**Bonnes pratiques:**
- Définir le niveau d'expertise (senior, expert)
- Mentionner les principes clés
- Préciser le mindset (pragmatique, rigoureux, etc.)

### Étape 3: Définir les CAPABILITIES

Lister ce que l'agent peut produire.

**Format:**
```markdown
[CAPABILITIES]
- [Action] basé sur [input]
- Créer [artifact]
- Valider [critère]
```

**Exemple (Test Agent):**
```markdown
[CAPABILITIES]
- Create comprehensive test plans
- Write unit tests, integration tests, E2E tests
- Define performance benchmarks
- Identify edge cases and security test scenarios
```

### Étape 4: Définir les CONSTRAINTS

Ce que l'agent ne doit JAMAIS faire.

**Exemple (Dev Agent):**
```markdown
[CONSTRAINTS]
- Do NOT make architectural decisions — escalate to MDAN Core
- Do NOT skip error handling for speed
- Do NOT hardcode secrets or credentials
- Do NOT introduce unapproved dependencies
```

### Étape 5: Définir l'OUTPUT_FORMAT

Structure standardisée de la sortie.

**Template d'artifact:**
```markdown
---
Artifact: [Nom]
Phase: [Phase]
Agent: [Agent Name]
Version: 1.0
Status: Draft | Review | Validated
Date: YYYY-MM-DD
Project: [Nom du projet]
---

## Section 1
## Section 2
## Notes for MDAN Core
```

### Étape 6: Définir la QUALITY_CHECKLIST

Liste de vérification avant soumission.

**Exemple:**
```markdown
[QUALITY_CHECKLIST]
Avant de soumettre, vérifier:
- [ ] Le code compile sans erreurs
- [ ] Tous les cas limites sont gérés
- [ ] Les tests couvrent au moins 80%
- [ ] Pas de secrets en dur
```

### Étape 7: Ajouter au registre

Mettre à jour `agents/AGENTS-REGISTRY.md`:

```json
"mon-agent": {
  "current": "1.0.0",
  "changelog": [
    {
      "version": "1.0.0",
      "date": "2025-02-24",
      "type": "MAJOR",
      "changes": ["Initial release"]
    }
  ]
}
```

### Étape 8: Mettre à jour la CLI

Ajouter dans `cli/mdan.js`:

1. Dans `cmdInit()`, s'assurer que l'agent est copié
2. Dans `cmdAgent()`, ajouter le nom à la liste

---

## Créer un skill

### Qu'est-ce qu'un skill?

Un skill est une capacité optionnelle et modulaire qui étend MDAN.

**Différence avec un agent:**
- **Agent**: Rôle permanent dans le workflow
- **Skill**: Capacité optionnelle, activée selon le contexte

### Structure d'un skill

```
skills/
└── mon-skill/
    ├── skill.md           # Définition obligatoire
    ├── templates/         # Templates optionnels
    │   └── exemple.md
    └── examples/          # Exemples optionnels
        └── demo.md
```

### Créer `skill.md`

```markdown
---
name: mon-skill
description: Description courte du skill. Visible par le Learn Agent.
---

# [Skill Name]

[Description détaillée]

## Quand utiliser ce skill

[Conditions d'activation]

## Comment utiliser

[Instructions]

## Exemples

[Exemples d'utilisation]

## Templates

[Référence aux templates si applicable]
```

### Exemple: skill testing-avance

```markdown
---
name: testing-avance
description: Techniques de test avancées: mutation testing, property-based testing, visual regression
---

# Testing Avancé

Ce skill étend le Test Agent avec des techniques de test avancées.

## Quand utiliser

- Le projet nécessite une qualité de test élevée (>90% coverage)
- Tests de robustesse requis (mutation testing)
- UI avec tests visuels (visual regression)

## Techniques

### 1. Mutation Testing

```bash
npx stryker run
```

Configuration: [exemple]

### 2. Property-Based Testing

```javascript
// Avec fast-check
fc.assert(fc.property(
  fc.string(),
  (s) => expect(reverse(reverse(s))).toBe(s)
))
```

### 3. Visual Regression

[Instructions pour Playwright/Percy]
```

### Intégration

1. Créer le dossier et le fichier
2. Le Learn Agent peut maintenant le référencer
3. `mdan init` et `mdan attach` le copieront automatiquement

---

## Ajouter un template

### Emplacement

`templates/[NOM].md`

### Structure standard

```markdown
# [Template Name]

> Description en une ligne

---

## Section 1

[Contenu avec placeholders {{placeholder}}]

## Section 2

[Contenu]

---

## Notes

- [Instruction pour l'agent]
- [Ce qui doit être rempli par l'utilisateur]
```

### Exemple: template API-DOCUMENTATION

```markdown
# API Documentation

> Document généré par le Doc Agent pour les APIs REST/GraphQL

---

## Overview

{{api_description}}

## Base URL

```
{{base_url}}
```

## Authentication

{{auth_method}}

## Endpoints

### {{endpoint_name}}

**Method:** `{{method}}`
**Path:** `{{path}}`

#### Request

```json
{{request_body}}
```

#### Response

```json
{{response_body}}
```

#### Errors

| Code | Description |
|------|-------------|
| {{code}} | {{description}} |

---

## Rate Limits

{{rate_limits}}
```

### Intégration

1. Créer le fichier dans `templates/`
2. Référencer dans l'agent approprié
3. La CLI le copiera automatiquement

---

## Règles de versioning

MDAN utilise SemVer (Semantic Versioning): `MAJOR.MINOR.PATCH`

### Incrémenter PATCH (X.Y.Z → X.Y.Z+1)

**Quand:**
- Correction de typo dans un prompt
- Reformulation mineure sans changement de comportement
- Ajout d'un exemple dans une checklist

**Exemple:**
```markdown
<!-- Avant: version 2.0.0 -->
<!-- Après: version 2.0.1 -->
```

### Incrémenter MINOR (X.Y.0 → X.Y+1.0)

**Quand:**
- Nouvelle capacité ajoutée (rétrocompatible)
- Nouvelle section dans le format de sortie
- Nouvelles questions dans la checklist qualité

**Exemple:**
```markdown
<!-- version: 2.1.0 -->
<!-- last-updated: 2025-02-24 -->
<!-- changes: Added Mermaid diagram support -->
```

### Incrémenter MAJOR (X.0.0 → X+1.0.0)

**Quand:**
- Changement de format de sortie (breaking change)
- Changement de responsabilités de l'agent
- Renommage/suppression de sections

**Exemple:**
```markdown
<!-- version: 3.0.0 -->
<!-- last-updated: 2025-02-24 -->
<!-- breaking-changes-from: 2.x -->
```

### Mise à jour du registre

Après chaque changement:

```json
{
  "mon-agent": {
    "current": "2.1.0",
    "changelog": [
      {
        "version": "2.1.0",
        "date": "2025-02-24",
        "type": "MINOR",
        "changes": ["Added performance benchmarks section"]
      },
      {
        "version": "2.0.0",
        "date": "2025-01-20",
        "type": "MAJOR",
        "changes": ["Initial v2 release"]
      }
    ]
  }
}
```

---

## Tests et validation

### Tests manuels

#### Tester un agent

```bash
# 1. Voir le prompt
mdan agent mon-agent

# 2. Copier dans un LLM et tester avec différents inputs
# 3. Vérifier:
#    - Le format de sortie est correct
#    - Les contraintes sont respectées
#    - La checklist qualité est applicable
```

#### Tester la CLI

```bash
# Test init
rm -rf test-project
node cli/mdan.js init test-project
ls -la test-project/.mdan/

# Test attach
mkdir test-attach && cd test-attach
node ../cli/mdan.js attach
ls -la .mdan/

# Test rebuild
node ../cli/mdan.js attach --rebuild
cat .cursorrules | grep -A5 "REBUILD"
```

#### Tester multi-LLM

Tester chaque agent sur au moins 2 LLMs:
- Claude (format XML `[SECTION]`)
- GPT-4 (format markdown `## SECTION`)
- Gemini (format markdown uniquement)

### Validation avant PR

- [ ] Le code fonctionne localement
- [ ] Les agents testés sur 2+ LLMs
- [ ] La documentation est mise à jour
- [ ] Le registre des versions est à jour
- [ ] Les templates sont complets
- [ ] Pas de secrets ou credentials dans le code

---

## Process de Pull Request

### 1. Créer une branche

```bash
git checkout -b feature/mon-agent
# ou
git checkout -b fix/dev-agent-typo
# ou
git checkout -b docs/api-reference
```

### 2. Faire les modifications

- Modifier les fichiers concernés
- Tester localement
- Mettre à jour la documentation

### 3. Commiter

```bash
git add .
git commit -m "feat(agents): add Data Agent for ML projects

- Add agents/data.md with Universal Envelope
- Add DATA profile detection in orchestrator
- Update AGENTS-REGISTRY.md
- Update CLI to support data agent"
```

**Convention de commit:**
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `refactor:` Refactoring
- `test:` Tests

### 4. Pousser et créer la PR

```bash
git push origin feature/mon-agent
```

Sur GitHub, créer la Pull Request avec:

**Template de PR:**
```markdown
## Description

[Description du changement]

## Type de changement

- [ ] Nouvel agent
- [ ] Modification d'agent
- [ ] Nouveau skill
- [ ] Bug fix
- [ ] Documentation

## Tests effectués

- [ ] Testé sur Claude
- [ ] Testé sur GPT-4
- [ ] Testé sur [autre LLM]
- [ ] CLI testée localement

## Checklist

- [ ] Le code suit les conventions MDAN
- [ ] La documentation est mise à jour
- [ ] Le versioning est correct
- [ ] Pas de breaking changes non documentés
```

### 5. Review

Attendre la review. Répondre aux commentaires et ajuster si nécessaire.

---

## Conventions de code

### Markdown

- Utiliser des headers ATX (`#`, `##`)
- Limiter les lignes à 80 caractères
- Pas d'emojis dans les prompts agents (sauf si demandé)

### JavaScript (CLI)

- Pas de dépendances externes
- Functions pure quand possible
- Comments en anglais
- Error handling explicite

### JSON

- Indentation 2 espaces
- Pas de trailing commas
- Keys en snake_case

---

## Ressources

- [ARCHITECTURE.md](../ARCHITECTURE.md) - Architecture détaillée
- [MDAN.md](../MDAN.md) - Spécification complète
- [core/universal-envelope.md](../core/universal-envelope.md) - Format des agents
- [agents/AGENTS-REGISTRY.md](../agents/AGENTS-REGISTRY.md) - Registre des versions
