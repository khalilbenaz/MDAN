# MDAN Memory System

> La mémoire persistante de MDAN entre les sessions.  
> Chaque projet génère et maintient un fichier `MDAN-STATE.json` à la racine.

---

## Concept

Le problème fondamental des agents IA : chaque nouvelle conversation repart de zéro.  
MDAN résout ça avec un fichier d'état JSON versionné, lisible par n'importe quel LLM.

Au début de chaque session, l'utilisateur colle le contenu de `MDAN-STATE.json` dans la conversation.  
MDAN Core le lit, reconstruit le contexte complet, et reprend exactement où on s'était arrêté.

---

## Structure du fichier MDAN-STATE.json

```json
{
  "mdan_version": "2.0.0",
  "user": {
    "name": "Alex"
  },
  "project": {
    "name": "mon-projet",
    "type": "web-app",
    "created_at": "2025-01-15",
    "last_updated": "2025-01-20"
  },
  "current_phase": "BUILD",
  "phase_history": [
    {
      "phase": "DISCOVER",
      "started_at": "2025-01-15",
      "completed_at": "2025-01-15",
      "status": "VALIDATED",
      "artifacts": ["mdan_output/PRD.md"]
    },
    {
      "phase": "DESIGN",
      "started_at": "2025-01-16",
      "completed_at": "2025-01-17",
      "status": "VALIDATED",
      "artifacts": ["mdan_output/ARCHITECTURE.md", "mdan_output/UX-SPEC.md"]
    },
    {
      "phase": "BUILD",
      "started_at": "2025-01-18",
      "completed_at": null,
      "status": "IN_PROGRESS",
      "artifacts": []
    }
  ],
  "agents_used": {
    "product": "2.0.0",
    "architect": "2.0.0",
    "ux": "2.0.0",
    "dev": "2.0.0",
    "test": "2.0.0",
    "security": "2.0.0",
    "devops": "2.0.0",
    "doc": "2.0.0"
  },
  "features": [
    {
      "id": "US-001",
      "title": "User authentication",
      "status": "DONE",
      "implemented_at": "2025-01-18",
      "files": ["src/auth/auth.service.ts", "src/auth/auth.controller.ts"],
      "tests": "PASSING",
      "security_review": "APPROVED"
    },
    {
      "id": "US-002",
      "title": "User profile management",
      "status": "IN_PROGRESS",
      "implemented_at": null,
      "files": [],
      "tests": null,
      "security_review": null
    },
    {
      "id": "US-003",
      "title": "Dashboard",
      "status": "TODO",
      "implemented_at": null,
      "files": [],
      "tests": null,
      "security_review": null
    }
  ],
  "decisions": [
    {
      "id": "ADR-001",
      "title": "PostgreSQL over MongoDB",
      "made_at": "2025-01-16",
      "rationale": "Relational data, ACID needed"
    }
  ],
  "open_issues": [
    {
      "id": "ISSUE-001",
      "type": "BLOCKER",
      "description": "Rate limiting library choice not finalized",
      "phase": "BUILD"
    }
  ],
  "tech_stack": {
    "frontend": "React 18 + TypeScript",
    "backend": "Node.js 20 + Express",
    "database": "PostgreSQL 16",
    "cache": "Redis 7",
    "hosting": "Railway"
  },
  "llm_history": [
    { "session": 1, "llm": "Claude", "phase": "DISCOVER + DESIGN" },
    { "session": 2, "llm": "Cursor", "phase": "BUILD (US-001)" }
  ]
}
```

---

## Protocole de reprise de session

### Ce que l'utilisateur fait

```
1. Ouvrir MDAN-STATE.json du projet
2. Copier le contenu
3. Ouvrir son LLM avec le prompt MDAN Core
4. Coller ce message :

"MDAN RESUME SESSION
[coller le contenu de MDAN-STATE.json]"
```

### Ce que MDAN Core fait automatiquement

```
[MDAN CORE — REPRISE DE SESSION]

✅ Projet chargé : [nom]
✅ Phase courante : [phase] 
✅ Progression : [X/Y features complètes]
✅ Dernière session : [LLM utilisé, date]

Contexte reconstruit :
- PRD : [résumé en 2 lignes]
- Architecture : [stack + pattern]
- Fonctionnalités : [liste avec statuts]
- Issues ouvertes : [liste]

Prochaine action recommandée :
→ [Action précise à faire maintenant]

Souhaitez-vous continuer avec [action], ou autre chose ?
```

---

## Mise à jour de l'état

À la fin de chaque session, MDAN Core génère le MDAN-STATE.json mis à jour :

```
[MDAN CORE — FIN DE SESSION]

Voici votre MDAN-STATE.json mis à jour.
Remplacez le fichier existant avec ce contenu :

[JSON complet mis à jour]
```

---

## CLI — Commandes mémoire

```bash
# Initialiser l'état d'un projet
mdan memory init mon-projet

# Afficher l'état actuel
mdan memory status

# Mettre à jour le statut d'une feature
mdan memory feature US-001 done

# Générer le prompt de reprise
mdan memory resume

# Valider une phase
mdan memory phase-complete DISCOVER
```
