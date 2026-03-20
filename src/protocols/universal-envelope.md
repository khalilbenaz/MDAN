# MDAN Universal Envelope v3.0

Format standard pour la communication inter-agents dans MDAN.

## Format

```yaml
envelope:
  from: "architect"           # Agent émetteur
  to: "dev"                   # Agent destinataire (ou "all")
  type: "handoff"             # handoff | question | observation | alert | debate-request
  priority: "normal"          # low | normal | high | critical
  context:
    wizard: "create-architecture"
    step: "step-05-patterns"
    artifact: "docs/mdan-output/planning/architecture.md"
  
  payload:
    summary: "Architecture décidée : microservices avec API Gateway"
    key_decisions:
      - "PostgreSQL comme DB principale"
      - "Redis pour le cache"
      - "Docker + K8s pour le déploiement"
    constraints:
      - "Pas de vendor lock-in cloud"
      - "API REST, pas GraphQL (équipe junior)"
    next_action: "Créer les epics basés sur cette architecture"
    
  memory_update:
    add_to_context: true
    add_to_decisions: true
```

## Types d'enveloppes

| Type | Usage | Déclenche |
|------|-------|-----------|
| `handoff` | Passage de relais entre wizards | Chargement du wizard suivant avec contexte |
| `question` | Un agent a besoin d'info | Pause + question à l'utilisateur ou autre agent |
| `observation` | Note pour mémoire | Ajout dans MDAN-STATE.agent_observations |
| `alert` | Problème détecté | Notification + suggestion d'action |
| `debate-request` | Conflit entre agents | Déclenchement du Debate Protocol |
