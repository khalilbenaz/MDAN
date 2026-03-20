# MDAN Memory System v3.0

## Pourquoi c'est différent de MDAN

MDAN n'a **aucun système de mémoire**. Chaque session repart de zéro. MDAN résout ça.

## Architecture

```
MDAN-STATE.json          ← État persistant du projet (phases, artifacts, décisions)
   ↕ lu/écrit par
Wizard Engine            ← Met à jour l'état après chaque wizard
   ↕ informé par
Context Summary          ← Résumé vivant du projet, mis à jour en continu
   ↕ alimenté par
Agent Observations       ← Notes des agents pendant leur travail
```

## Fonctionnement

### 1. Sauvegarde automatique
À la fin de chaque wizard, le moteur sauvegarde dans MDAN-STATE.json :
- Le wizard complété
- Les artifacts produits
- Les décisions prises
- Le résumé du contexte mis à jour
- Les observations des agents

### 2. Restauration automatique
Au début de chaque session, MDAN Master :
1. Charge MDAN-STATE.json
2. Restaure le contexte du projet
3. Identifie la phase actuelle
4. Propose la prochaine action logique
5. Rappelle les décisions clés à l'utilisateur

### 3. Mémoire cross-wizard
Quand un wizard démarre, il a accès à :
- Tous les artifacts des wizards précédents
- Les décisions d'architecture (pour le dev)
- Les user stories (pour le QA)
- Le product brief (pour tout le monde)

### 4. Context Summary
Un résumé vivant du projet en ~500 mots, mis à jour à chaque fin de wizard.
Inclut : objectif, décisions clés, stack technique, état actuel, prochaines étapes.

## Protocole de reprise

Quand l'utilisateur revient après une interruption :

```
1. MDAN Master charge MDAN-STATE.json
2. Affiche : "Bonjour {user_name} ! Voici où on en est sur {project_name}..."
3. Résumé : phase actuelle, dernière action, prochaine étape suggérée
4. Question : "On continue là où on s'était arrêté ?"
```

## Format de l'état

Voir `.mdan/state/MDAN-STATE.template.json` pour le schéma complet.
