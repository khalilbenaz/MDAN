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

### Option A : CLI (Recommandé)

```bash
# Cloner MDAN
git clone https://github.com/[votre-username]/MDAN.git

# Initialiser un projet
bash MDAN/cli/mdan.sh init mon-projet

# Ou avec Python
python3 MDAN/cli/mdan.py init mon-projet
```

### Option B : Configuration manuelle

1. Cloner le dépôt
2. Copier `core/orchestrator.md` comme prompt système de votre LLM
3. Choisir votre guide d'intégration dans `/integrations/`
4. Commencer par Phase 1 : DISCOVER

### Option C : Cursor / Windsurf

1. Cloner le dépôt
2. Lancer `mdan init mon-projet`
3. Ouvrir le dossier projet dans Cursor ou Windsurf
4. Le fichier `.cursorrules` / `.windsurfrules` est pré-configuré

---

## FAQ

**Q : Peut-on sauter des phases ?**  
R : Non. Les phases existent pour éviter les erreurs cumulatives. Chaque phase sautée multiplie le retravailler nécessaire plus tard.

**Q : Peut-on utiliser plusieurs LLMs dans le même projet ?**  
R : Oui. MDAN est conçu pour cela. Utilisez Claude pour DISCOVER/DESIGN, Cursor pour BUILD, etc.

**Q : A-t-on besoin des 8 agents pour chaque projet ?**  
R : Pour les petits projets, MDAN Core peut être instruit de n'activer que les agents pertinents. Un petit outil CLI n'a pas besoin de l'UX Agent, par exemple.

**Q : Comment gérer une découverte qui révèle que l'idée initiale est fausse ?**  
R : C'est le but de DISCOVER. Si l'idée est mauvaise, MDAN Core le documente et itère. Une mauvaise idée détectée en DISCOVER coûte des minutes. La même idée détectée en VERIFY coûte des jours.

**Q : Les équipes peuvent-elles utiliser MDAN ?**  
R : Oui. Chaque membre de l'équipe peut opérer un agent spécifique, avec MDAN Core coordonnant via des artefacts partagés dans le contrôle de version.
