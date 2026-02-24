# MDAN — Agent Versioning System

> Comment les agents sont versionnés, mis à jour et rétrocompatibles.

---

## Pourquoi versionner les agents ?

Un projet peut durer des semaines. Entre deux sessions, tu peux mettre à jour un agent  
(meilleur prompt, nouveaux patterns de sécurité, format de sortie amélioré).  
Sans versioning, les projets en cours ne savent pas quelle version ils utilisent —  
et les résultats deviennent incohérents.

---

## Schéma de version

```
MAJOR.MINOR.PATCH

2.1.3
│ │ └── PATCH : correction de bug dans le prompt (même comportement, résultat plus propre)
│ └──── MINOR : nouvelle capacité ajoutée (rétrocompatible)
└────── MAJOR : changement de comportement ou format de sortie (breaking change)
```

---

## Registre des versions — AGENTS-REGISTRY.json

```json
{
  "registry_version": "1.0",
  "last_updated": "2025-01-20",
  "agents": {
    "product": {
      "current": "2.0.0",
      "changelog": [
        {
          "version": "2.0.0",
          "date": "2025-01-20",
          "type": "MAJOR",
          "changes": ["Added MoSCoW section", "Added risk matrix", "Added open questions table"]
        },
        {
          "version": "1.0.0",
          "date": "2025-01-01",
          "type": "MAJOR",
          "changes": ["Initial release"]
        }
      ]
    },
    "architect": {
      "current": "2.0.0",
      "changelog": [
        {
          "version": "2.0.0",
          "date": "2025-01-20",
          "type": "MAJOR",
          "changes": ["Added Mermaid diagram requirement", "Added ADR format", "Added non-functional requirements table"]
        }
      ]
    },
    "ux": {
      "current": "2.0.0",
      "changelog": [
        {
          "version": "2.0.0",
          "date": "2025-01-20",
          "type": "MAJOR",
          "changes": ["Added design system template", "Added all-states requirement", "Added accessibility section"]
        }
      ]
    },
    "dev": {
      "current": "2.0.0",
      "changelog": [
        {
          "version": "2.0.0",
          "date": "2025-01-20",
          "type": "MAJOR",
          "changes": ["Added implementation plan format", "Added setup instructions section", "Added coding standards reference"]
        }
      ]
    },
    "test": {
      "current": "2.0.0",
      "changelog": [
        {
          "version": "2.0.0",
          "date": "2025-01-20",
          "type": "MAJOR",
          "changes": ["Added performance test section", "Added security edge cases", "Added flakiness prevention rules"]
        }
      ]
    },
    "security": {
      "current": "2.0.0",
      "changelog": [
        {
          "version": "2.0.0",
          "date": "2025-01-20",
          "type": "MAJOR",
          "changes": ["Added STRIDE template", "Added VULN severity format", "Added compliance notes section"]
        }
      ]
    },
    "devops": {
      "current": "2.0.0",
      "changelog": [
        {
          "version": "2.0.0",
          "date": "2025-01-20",
          "type": "MAJOR",
          "changes": ["Added multi-environment table", "Added runbook template", "Added rollback procedure"]
        }
      ]
    },
    "doc": {
      "current": "2.0.0",
      "changelog": [
        {
          "version": "2.0.0",
          "date": "2025-01-20",
          "type": "MAJOR",
          "changes": ["Added API documentation template", "Added README template"]
        }
      ]
    },
    "learn": {
      "current": "2.0.0",
      "changelog": [
        {
          "version": "2.0.0",
          "date": "2025-01-20",
          "type": "MAJOR",
          "changes": ["Initial release", "Knowledge acquisition and distribution specialist", "MCP server integration", "Rules ingestion capabilities"]
        }
      ]
    }
  }
}
```

---

## Compatibilité projet/agent

Quand MDAN Core reprend une session depuis MDAN-STATE.json, il compare :

```
Project uses: dev agent v1.0.0
Current MDAN:  dev agent v2.0.0
```

Et affiche :

```
⚠️  Agent Update Available

Dev Agent: v1.0.0 → v2.0.0 (MAJOR)

Breaking changes in v2.0.0:
- Output format changed: now includes "Implementation Plan" section
- Notes section renamed to "Notes for MDAN Core"

Options:
  [1] Continue with v1.0.0 (no change, consistent with past output)
  [2] Upgrade to v2.0.0 (recommended, but review past artifacts)
  [3] Show full changelog

What do you prefer?
```

---

## Règles de versioning pour les contributeurs

### Quand incrémenter PATCH (2.0.X)
- Correction de faute de frappe dans le prompt
- Reformulation qui améliore la clarté sans changer le comportement
- Ajout d'un exemple dans la checklist

### Quand incrémenter MINOR (2.X.0)
- Nouvelle capacité ajoutée (ex: l'agent peut maintenant produire des diagrammes Mermaid)
- Nouvelle section dans le format de sortie (rétrocompatible)
- Nouvelles questions dans la checklist qualité

### Quand incrémenter MAJOR (X.0.0)
- Changement de format de sortie (les projets existants ne sont plus compatibles)
- Changement de responsabilités de l'agent
- Renommage de sections
- Suppression de sections existantes

---

## Header de version dans chaque agent

Chaque fichier agent commence par :

```markdown
# MDAN — [Agent Name]
<!-- version: 2.0.0 -->
<!-- last-updated: 2025-01-20 -->
<!-- breaking-changes-from: 1.x -->
```

Et dans l'Universal Envelope :

```
[MDAN-AGENT]
NAME: Dev Agent
VERSION: 2.0.0
...
```
