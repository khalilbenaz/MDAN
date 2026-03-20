# MDAN — Spécification de la méthode v1.0

> La spécification complète et faisant autorité de la méthode MDAN.

---

## Partie 1 : Vue d'ensemble

MDAN (prononcé "em-dan") est une méthode structurée pour le développement logiciel piloté par l'IA.

**Prémisse fondamentale :** Construire des logiciels avec des agents IA nécessite la même discipline que construire des logiciels avec des équipes humaines — des rôles clairs, des phases structurées, une qualité imposée et des transferts explicites. Sans cette structure, les agents IA inventent des tâches, se contredisent, sautent la validation et produisent des résultats incohérents.

**La réponse MDAN :** Un orchestrateur central (MDAN Core) qui coordonne des agents spécialisés à travers un workflow en 5 phases, avec des portes de qualité imposées à chaque transition.

---

## Partie 2 : Principes

### P1 — Orchestrer, pas exécuter
MDAN Core est un agent de réflexion et de planification. Il n'exécute jamais directement. L'exécution appartient aux agents spécialisés.

### P2 — Une phase à la fois
Les phases sont séquentielles et non négociables. Une phase DISCOVER complète produit un meilleur BUILD qu'un DISCOVER bâclé ne le fera jamais.

### P3 — Artefacts plutôt que mots
Chaque phase produit des artefacts — des documents structurés avec des modèles définis. Des mots dans une fenêtre de chat ne sont pas des artefacts.

### P4 — Validation explicite
Chaque phase se termine par l'approbation explicite des artefacts par l'utilisateur. MDAN Core ne progresse jamais sans approbation.

### P5 — Agnosticisme LLM
MDAN produit des résultats identiques quel que soit le LLM sous-jacent. L'Universal Envelope est le mécanisme technique qui permet cela.

### P6 — La sécurité n'est pas optionnelle
Le Security Agent est actif en BUILD et VERIFY. La sécurité n'est pas une liste de contrôle en fin de projet — c'est une préoccupation parallèle tout au long du développement.

### P7 — Échouer vite, échouer tôt
Un problème trouvé en DISCOVER coûte 1 unité d'effort. Le même problème trouvé en SHIP coûte 100 unités.

---

## Partie 3 : Le MDAN Core

MDAN Core est l'orchestrateur central. Il fonctionne selon ces règles :

**Sait tout :** MDAN Core dispose toujours du contexte complet — PRD, architecture, spec UX, fonctionnalité en cours, décisions précédentes.

**Délègue tout :** MDAN Core n'écrit jamais de code, ne conçoit pas d'interfaces, ne rédige pas de documentation. Il active l'agent approprié avec un brief précis.

**Valide tout :** Chaque sortie d'agent est examinée par MDAN Core avant d'être présentée à l'utilisateur.

**Guide et Assiste :** MDAN Core agit comme un collaborateur expert. L'utilisateur peut taper `/mdan-help` à tout moment pour obtenir des conseils contextuels sur la prochaine étape.

**Mode "Party" :** Pour les problèmes complexes, MDAN Core peut invoquer plusieurs agents simultanément avec `/party [sujet]` pour faciliter un débat entre experts (ex: l'Architecte et l'Agent de Sécurité) avant de prendre une décision.

**Contrôle les transitions de phase :** Seul MDAN Core peut déclarer une phase terminée et passer à la suivante. L'utilisateur doit approuver explicitement chaque transition.

---

## Partie 4 : Réseau d'agents

### Règles de conception des agents

Chaque agent MDAN est :
1. **Personnifié** — Possède un prénom (ex: Khalil, Reda) pour rendre la collaboration naturelle
2. **Spécialisé** — Un domaine, une expertise profonde
3. **Autonome** — Opère indépendamment dans son domaine
4. **Borné** — Ne peut pas prendre de décisions en dehors de son domaine (escalade au Core)
5. **Auto-vérificateur** — Exécute une checklist de qualité avant de soumettre
6. **Universel** — Fonctionne identiquement sur tous les LLMs via l'Universal Envelope

### Hiérarchie des agents

```
MDAN Core (Orchestrateur)
│
├── Phase 1 — DISCOVER
│   └── Product Agent
│
├── Phase 2 — DESIGN
│   ├── Architect Agent
│   └── UX Agent
│
├── Phase 3 — BUILD
│   ├── Dev Agent
│   └── Security Agent (concurrent)
│
├── Phase 4 — VERIFY
│   ├── Test Agent
│   └── Security Agent
│
└── Phase 5 — SHIP
    ├── DevOps Agent
    └── Doc Agent
```

---

## Partie 5 : L'Universal Envelope

L'Universal Envelope est la structure de prompt standard utilisée pour tous les agents MDAN. Il résout le problème de compatibilité LLM en normalisant le comportement des agents.

### Champs de l'Envelope

| Champ | Objectif |
|-------|---------|
| NAME | Identifiant de l'agent |
| VERSION | Version du prompt pour le suivi |
| ROLE | Description du rôle en une ligne |
| PHASE | Phase(s) dans lesquelles l'agent opère |
| REPORTS_TO | Toujours MDAN Core |
| IDENTITY | Qui est l'agent — expertise et état d'esprit |
| CAPABILITIES | Ce que l'agent peut produire |
| CONSTRAINTS | Limites strictes sur ce que l'agent ne doit PAS faire |
| INPUT_FORMAT | Ce que l'agent attend de MDAN Core |
| OUTPUT_FORMAT | Comment l'agent doit structurer sa réponse |
| QUALITY_CHECKLIST | Auto-validation avant soumission |
| ESCALATION | Quand remonter des problèmes à MDAN Core |

---

## Partie 6 : Standard des artefacts

Chaque artefact produit par les agents MDAN suit cet en-tête :

```
---
Artefact : [Nom de l'artefact]
Phase : [Nom de la phase]
Agent : [Nom de l'agent]
Version : [X.Y]
Statut : Brouillon | Révision | Validé
Date : [AAAA-MM-JJ]
Projet : [Nom du projet]
---
```

---

## Partie 7 : Portes de qualité

### Porte 1 : DISCOVER → DESIGN

```
[ ] Le problème est spécifiquement défini
[ ] Au moins un persona utilisateur est complètement décrit
[ ] Les métriques de succès sont mesurables
[ ] Les contraintes sont documentées
[ ] Le PRD est complet avec priorisation MoSCoW
[ ] Le périmètre MVP est réaliste
[ ] Toutes les user stories ont des critères d'acceptation
[ ] Les risques sont identifiés avec plans de mitigation
[ ] Les éléments hors périmètre sont explicitement listés
[ ] L'utilisateur a approuvé le PRD
```

### Porte 2 : DESIGN → BUILD

```
[ ] Le diagramme d'architecture système est complet
[ ] Toutes les exigences du PRD sont adressées
[ ] La stack technique complète est spécifiée avec justifications
[ ] Tous les modèles de données sont définis
[ ] Tous les endpoints API sont spécifiés
[ ] L'architecture de sécurité est définie
[ ] Les exigences non-fonctionnelles sont adressées
[ ] Les conventions de code sont documentées
[ ] Au moins un ADR existe
[ ] Le design system est complet
[ ] Tous les écrans ont tous leurs états définis
[ ] Les deux documents sont approuvés par l'utilisateur
```

### Porte 3 : BUILD → VERIFY

```
[ ] Toutes les fonctionnalités MVP sont implémentées
[ ] Chaque fonctionnalité a des tests unitaires
[ ] Aucun constat de sécurité CRITIQUE non résolu
[ ] Aucun constat de sécurité ÉLEVÉ non résolu
[ ] Le code suit les conventions du projet
[ ] Pas de secrets codés en dur
[ ] Tous les chemins d'erreur sont gérés
```

### Porte 4 : VERIFY → SHIP

```
[ ] Tous les critères d'acceptation ont une couverture de test
[ ] Tous les tests passent
[ ] La couverture de tests atteint la cible
[ ] Les tests d'intégration passent
[ ] Au moins 3 scénarios E2E validés
[ ] Les critères de performance sont atteints
[ ] La revue de sécurité finale est complète
[ ] La documentation est complète
[ ] Le runbook de déploiement est complet
```

---

## Partie 8 : Cycle de vie MDAN

```
L'utilisateur présente l'idée de projet
         │
         ▼
Phase 1 : DISCOVER
   MDAN Core pose les 5 questions de découverte
   Product Agent crée le PRD
   L'utilisateur valide le PRD
         │
   [Porte 1]
         │
         ▼
Phase 2 : DESIGN
   Architect Agent crée le Document d'Architecture
   UX Agent crée la Spécification UX
   L'utilisateur valide les deux
         │
   [Porte 2]
         │
         ▼
Phase 3 : BUILD
   Pour chaque fonctionnalité :
     Dev Agent implémente
     Security Agent revoit
     MDAN Core valide
         │
   [Porte 3]
         │
         ▼
Phase 4 : VERIFY
   Test Agent crée et exécute la suite de tests
   Security Agent fait la revue finale
   L'utilisateur approuve
         │
   [Porte 4]
         │
         ▼
Phase 5 : SHIP
   DevOps Agent déploie
   Doc Agent documente
   Validation post-déploiement
         │
         ▼
   🚀 LANCÉ
         │
         ▼
   Itération suivante → Retour en Phase 1
```

---

## Partie 9 : Historique des versions

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2025 | Version initiale |
