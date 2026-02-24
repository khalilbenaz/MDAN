# MDAN — Documentation Complète (Français)

## Table des matières

1. [Introduction](#introduction)
2. [Philosophie](#philosophie)
3. [Architecture](#architecture)
4. [Les 5 phases](#les-5-phases)
5. [Référence des agents](#référence-des-agents)
6. [Portes de qualité](#portes-de-qualité)
7. [Compatibilité LLM](#compatibilité-llm)
8. [Démarrage](#démarrage)
9. [FAQ](#faq)

---

## Introduction

MDAN est une méthode structurée pour le développement logiciel piloté par l'IA. Elle a été conçue pour résoudre les limitations des méthodes agentiques existantes en introduisant :

- Une séparation claire entre **orchestration** et **exécution**
- Un **standard de prompt universel** compatible avec n'importe quel LLM
- Des **portes de qualité imposées** qui empêchent les erreurs de se multiplier

MDAN n'est pas un framework, ni une bibliothèque, ni un outil. C'est une **méthode** — une façon de travailler avec les agents IA pour construire des logiciels de manière systématique et fiable.

### Pourquoi MDAN ?

La plupart des méthodes de développement agentique souffrent de trois problèmes :

1. **Pas de structure** — Les agents inventent des tâches et sautent des étapes sans workflow imposé
2. **Dépendance à un LLM** — Les méthodes conçues pour un LLM fonctionnent mal avec d'autres
3. **Pas de contrôle qualité** — Il n'y a pas de point de contrôle entre les phases, les problèmes s'accumulent

MDAN résout ces trois problèmes :
- Le workflow en 5 phases avec portes de qualité empêche les sauts et les erreurs cumulatives
- L'Universal Envelope rend les agents identiques sur tous les LLMs majeurs
- MDAN Core est l'orchestrateur unique qui maintient le contexte et impose la qualité

---

## Philosophie

### Orchestrer, pas exécuter

MDAN Core n'écrit pas de code. Il ne conçoit pas d'interfaces. Il réfléchit, planifie, délègue et valide. Cette séparation garantit que chaque agent spécialisé peut se concentrer sur son domaine sans perdre la vue d'ensemble.

### Une phase à la fois

Chaque phase doit être entièrement terminée et validée avant de passer à la suivante. Ce n'est pas une formalité — c'est la règle la plus importante de MDAN. Sauter des phases est la cause la plus fréquente de retravailler dans les projets logiciels.

### Valider avant de progresser

Chaque phase se termine par une validation explicite de l'utilisateur. MDAN Core présente ce qui a été produit, met en évidence les décisions clés, et attend un "APPROUVÉ" avant de continuer. Cela garde l'humain en contrôle du processus.

### Agnostique au LLM par conception

MDAN a été conçu dès le premier jour pour fonctionner avec n'importe quel LLM. Le standard Universal Envelope garantit que les prompts des agents produisent des résultats cohérents, que vous utilisiez Claude, GPT-4, Gemini, Qwen ou tout autre modèle.

---

## Architecture

### Le modèle en 3 couches

```
Couche 1 : MDAN Core (Orchestrateur)
           Réfléchit • Planifie • Délègue • Valide
                            |
Couche 2 : Agents spécialisés
           Product | Architect | UX | Dev | Test | Security | DevOps | Doc
                            |
Couche 3 : Artefacts
           PRD | Architecture | UX Spec | Code | Tests | Sécurité | Pipeline | Docs
```

### Flux d'information

Toutes les informations transitent par MDAN Core. Les agents ne communiquent pas directement entre eux. Cela évite :
- Les décisions contradictoires entre agents
- La perte de contexte entre les agents
- Les dépendances circulaires

### L'Universal Envelope

Chaque agent dans MDAN est enveloppé dans l'Universal Envelope — une structure de prompt standardisée qui définit :
- L'identité et l'expertise de l'agent
- Ses capacités et contraintes
- Le format d'entrée attendu
- Le format de sortie requis
- L'auto-vérification qualité avant soumission
- Les conditions d'escalade

Voir `core/universal-envelope.md` pour la spécification complète.

---

## Les 5 phases

### Phase 1 : DISCOVER (Découverte)
**Objectif :** Comprendre profondément le problème avant de proposer une solution.  
**Agent :** Product Agent  
**Résultat :** PRD validé  

Les 5 questions de découverte doivent recevoir une réponse :
1. Quel est le problème fondamental ?
2. Qui sont les utilisateurs ?
3. Comment mesurer le succès ?
4. Quelles sont les contraintes ?
5. Qu'a-t-on déjà essayé ?

### Phase 2 : DESIGN (Conception)
**Objectif :** Architecturer la solution complète avant d'écrire une ligne de code.  
**Agents :** Architect Agent, UX Agent  
**Résultat :** Document d'architecture + Spécification UX  

Aucun code n'est écrit tant que DESIGN n'est pas terminé. L'architecture doit couvrir : conception système, stack technique, modèles de données, conception API, architecture de sécurité et conventions de code. La spec UX doit couvrir tous les écrans avec tous les états.

### Phase 3 : BUILD (Construction)
**Objectif :** Implémenter avec précision selon les spécifications.  
**Agents :** Dev Agent, Security Agent  
**Résultat :** Code fonctionnel, testé et revu en sécurité  

Chaque fonctionnalité suit la boucle BUILD : Brief de fonctionnalité → Dev Agent → Revue sécurité → Validation.

### Phase 4 : VERIFY (Vérification)
**Objectif :** Prouver que le logiciel fonctionne correctement, de manière sécurisée et complète.  
**Agents :** Test Agent, Security Agent  
**Résultat :** Suite de tests complète, approbation sécurité  

Aucune fonctionnalité n'est supposée fonctionner. Elle doit être prouvée par des tests. Tous les critères d'acceptation doivent avoir des cas de test correspondants.

### Phase 5 : SHIP (Livraison)
**Objectif :** Déployer avec confiance, documenter complètement.  
**Agents :** DevOps Agent, Doc Agent  
**Résultat :** Déploiement en production, documentation complète  

Livrer signifie : en production, monitoré, documenté, avec un runbook pour les incidents.

---

## Référence des agents

| Agent | Phase | Expertise | Résultat principal |
|-------|-------|-----------|-------------------|
| Learn Agent | Toutes | Acquisition de connaissances | Knowledge Capsules |
| Product Agent | DISCOVER | Exigences, recherche UX | PRD |
| Architect Agent | DESIGN | Conception système, choix tech | Document d'architecture |
| UX Agent | DESIGN | Design interface, accessibilité | Spécification UX |
| Dev Agent | BUILD | Implémentation, qualité code | Code fonctionnel + tests |
| Security Agent | BUILD + VERIFY | Analyse vulnérabilités | Rapport de sécurité |
| Test Agent | VERIFY | QA, stratégie de tests | Plan de test + Suite |
| DevOps Agent | SHIP | CI/CD, infrastructure | Pipeline de déploiement |
| Doc Agent | SHIP | Rédaction technique | Documentation |

---

## Portes de qualité

MDAN impose des portes de qualité entre chaque phase. Une porte est une checklist qui doit être entièrement satisfaite avant de progresser.

| Porte | De → Vers | Vérifications clés |
|-------|-----------|-------------------|
| Porte 1 | DISCOVER → DESIGN | PRD complet, métriques définies, périmètre clair |
| Porte 2 | DESIGN → BUILD | Architecture complète, spec UX complète, les deux validés |
| Porte 3 | BUILD → VERIFY | Toutes les fonctionnalités implémentées, sécurité revue |
| Porte 4 | VERIFY → SHIP | Tous les tests passent, sécurité approuvée, docs prêtes |

---

## Compatibilité LLM

MDAN fonctionne avec tous les LLMs majeurs. L'Universal Envelope s'adapte aux forces de chaque modèle.

| LLM | Recommandé pour | Notes |
|-----|----------------|-------|
| Claude | DISCOVER, DESIGN | Excellent pour le raisonnement complexe et les sorties structurées |
| GPT-4o | Toutes les phases | Très bon dans tous les domaines |
| Gemini 1.5 Pro | Grands projets | Très large fenêtre de contexte |
| Qwen-Max | Projets marché asiatique | Fort support bilingue |
| Kimi 128k | Sessions longues | Fenêtre de contexte 128k |
| GLM-4 | Projets en chinois | Support natif chinois |
| Cursor | BUILD | Meilleur pour l'implémentation dans l'IDE |
| GitHub Copilot | BUILD | Meilleur pour la complétion de code inline |

---

## Démarrage

### Étape 1 : Cloner MDAN

```bash
git clone https://github.com/khalilbenaz/MDAN.git
cd MDAN
```

### Étape 2 : Initialiser votre projet

```bash
# Avec Bash
bash cli/mdan.sh init mon-projet

# Ou avec Python
python3 cli/mdan.py init mon-projet
```

Cela crée un dossier `mon-projet/` prêt à l'emploi avec :
- `.mdan/` — Fichiers MDAN (orchestrator, agents)
- `.cursorrules` — Configuration Cursor
- `.windsurfrules` — Configuration Windsurf
- `.github/copilot-instructions.md` — Configuration Copilot
- `docs/` — Templates (PRD, Architecture, etc.)

### Étape 3 : Utiliser avec votre LLM

#### Claude / ChatGPT / Gemini (Web)

1. Copier le contenu de `mon-projet/.mdan/orchestrator.md`
2. Le coller comme system prompt (ou premier message)
3. Démarrer avec : `MDAN: Je veux créer...`

#### Cursor IDE

```bash
cursor mon-projet   # .cursorrules est déjà configuré
```

#### Windsurf IDE

```bash
windsurf mon-projet   # .windsurfrules est déjà configuré
```

### Étape 4 : Suivre le workflow

MDAN vous guide à travers les 5 phases. Validez chaque phase avant de passer à la suivante.

---

## FAQ

**Q : Peut-on sauter des phases ?**  
R : Non. Les phases existent pour éviter les erreurs cumulatives. Chaque phase sautée multiplie le retravailler nécessaire plus tard.

**Q : Peut-on utiliser plusieurs LLMs dans le même projet ?**  
R : Oui. MDAN est conçu pour cela. Utilisez Claude pour DISCOVER/DESIGN, Cursor pour BUILD, etc.

**Q : A-t-on besoin des 9 agents pour chaque projet ?**  
R : Non. MDAN Core détecte automatiquement le profil du projet et adapte les agents utilisés. Un projet MICRO n'utilisera que 2-3 agents.

**Q : Comment reprendre un projet après une pause ?**  
R : Utilisez `MDAN RESUME SESSION` avec le contenu du fichier MDAN-STATE.json. MDAN Core reconstruit tout le contexte.

**Q : Comment ajouter des compétences personnalisées ?**  
R : Utilisez le Learn Agent : `bash cli/mdan.sh learn --rules .cursorrules` ou `--skill ./mes-conventions.md`
