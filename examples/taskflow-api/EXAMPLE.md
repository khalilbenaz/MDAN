# MDAN — Exemple Complet : TaskFlow API

> Exemple de projet de bout en bout passant par les 5 phases MDAN.  
> Projet : une API REST de gestion de tâches collaboratives.  
> Profil détecté : STANDARD

---

## Contexte

L'utilisateur arrive avec cette idée :
> "Je veux créer une API de gestion de tâches pour que mon équipe de 5 développeurs  
> puisse gérer nos sprints sans dépendre de Jira."

Voici exactement ce qui se passe, session par session.

---

# PHASE 1 : DISCOVER

## Session 1 — LLM : Claude

**Utilisateur :** Je veux créer une API de gestion de tâches pour que mon équipe de 5 développeurs puisse gérer nos sprints sans dépendre de Jira.

---

**MDAN Core :**

```
[MDAN CORE — PROJECT PROFILE DETECTED]

Je classe ce projet comme STANDARD.

Raisons :
- Équipe existante (5 devs) = utilisateurs réels identifiés
- Scope clair et délimité = API uniquement
- Pas de contraintes enterprise/compliance mentionnées

Adaptations :
- Workflow 5 phases complet
- UX Agent → Skip (API-only, pas d'interface)
- Profil affiné vers API-ONLY possible selon vos réponses

Est-ce que ça vous convient ? (Oui / Non + correction)
```

**Utilisateur :** Oui c'est bon.

---

**MDAN Core :**

```
🔍 MDAN — Phase 1 : DISCOVER

5 questions avant qu'on construise quoi que ce soit :

1. Quel est le problème exact avec Jira ?
2. Qui utilise l'outil ? (rôles dans l'équipe, niveaux tech)
3. Comment mesurez-vous que c'est un succès ?
4. Contraintes ? (tech existante, délai, budget)
5. Avez-vous essayé des alternatives ? Pourquoi ça n'a pas marché ?
```

**Utilisateur :**
1. Jira est trop lourd, on passe plus de temps à le configurer qu'à coder. On veut juste des tâches, des statuts, et des assignations.
2. 5 devs, tous seniors. Ils consomment l'API via leur propre tooling (scripts, IDE plugins).
3. Succès = 100% de l'équipe l'utilise après 2 semaines. Moins de 5min pour créer et assigner une tâche.
4. On est en Node.js/TypeScript côté serveur. Pas de deadline stricte, on veut faire ça bien. Pas de budget alloué = on s'auto-héberge.
5. Linear trop cher, GitHub Projects trop basique, Trello pas d'API correcte.

---

**MDAN Core :** `[ACTIVATING: Product Agent v2.0.0]`

---

**Product Agent output :**

```markdown
---
Artifact: Product Requirements Document
Phase: DISCOVER
Agent: Product Agent v2.0.0
Version: 1.0
Status: Draft
Date: 2025-01-15
Project: TaskFlow API
---

# PRD : TaskFlow API

## 1. Executive Summary
TaskFlow est une API REST légère de gestion de tâches conçue pour des équipes de développeurs techniques. Elle remplace des outils comme Jira en offrant simplicité, rapidité et une API first-class que les développeurs peuvent intégrer dans leur propre workflow.

## 2. Problem Statement
**Le problème :** Les outils de gestion de tâches existants (Jira, Linear) sont soit trop lourds à configurer, soit trop coûteux pour une petite équipe autonome.
**Qui :** Équipes de développeurs seniors qui veulent contrôler leur tooling.
**Douleur actuelle :** Jira prend plus de temps à maintenir qu'à utiliser. Linear coûte $8/user/mois inutilement.
**Coût de l'inaction :** Désorganisation, réunions de synchro inutiles, overhead administratif.

## 3. Persona principale : Dev Senior
| Attribut | Détail |
|----------|--------|
| Rôle | Développeur senior |
| Objectif | Gérer ses tâches sans friction |
| Pain point | Outils trop complexes, pas d'API propre |
| Niveau technique | Expert — consomme des APIs REST nativement |
| Contexte d'usage | Terminal, scripts, IDE plugins |

## 4. Solution
API REST JSON, auth par token API, gestion de tâches (create/read/update/delete), assignation, statuts customisables, filtres par assignee/status/sprint.

## 5. User Stories — Epic : Task Management

- [x] **US-001** : En tant que dev, je veux créer une tâche (titre, description, assignee, priority) via API pour la tracker.
  - Given: token valide, When: POST /tasks with valid body, Then: 201 + task object
  - Given: token valide, When: POST /tasks with missing title, Then: 400 + validation error

- [x] **US-002** : En tant que dev, je veux lister les tâches filtrées par status/assignee/sprint pour voir mon backlog.
  - Given: token valide, When: GET /tasks?status=todo, Then: 200 + filtered array

- [x] **US-003** : En tant que dev, je veux changer le statut d'une tâche pour refléter sa progression.
  - Given: token valide + task owner, When: PATCH /tasks/:id {status: "in_progress"}, Then: 200 + updated task

- [x] **US-004** : En tant que dev, je veux créer et gérer des sprints pour organiser le travail en itérations.
  - Given: token admin, When: POST /sprints, Then: 201 + sprint object

- [x] **US-005** : En tant que dev, je veux m'authentifier via token API pour accéder sécuritairement.
  - Given: valid credentials, When: POST /auth/token, Then: 200 + API token

## 6. MoSCoW
### Must Have
- CRUD tâches complet (US-001, US-002, US-003)
- Authentification par token API (US-005)
- Assignation de tâches

### Should Have
- Gestion de sprints (US-004)
- Filtres avancés
- Pagination

### Could Have
- Webhooks sur changement de statut
- Labels/tags
- Time tracking

### Won't Have (v1)
- Interface web
- Notifications email/Slack
- Rapports / analytics

## 7. Métriques de succès
| Métrique | Baseline | Cible | Délai |
|----------|---------|-------|-------|
| Adoption équipe | 0% | 100% | 2 semaines post-launch |
| Temps création tâche | 5min (Jira) | <1min | Au launch |
| Latence API p95 | N/A | <100ms | Au launch |
| Uptime | N/A | >99.5% | 30j post-launch |

## 8. Contraintes
- Backend : Node.js / TypeScript (non-négociable)
- Hébergement : auto-hébergé (pas de cloud payant)
- Budget : $0 (outils open source uniquement)

## 9. Risques
| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| L'équipe n'adopte pas | Faible | Élevé | Impliquer l'équipe dans le design API |
| Scope creep | Moyen | Moyen | MoSCoW strict, no v1.x features |

## 10. Hors périmètre
- Interface web (any)
- Intégrations tierces (GitHub, Slack)
- Mobile
```

---

**MDAN Core :** PRD produit. Validez pour passer en DESIGN.

**Utilisateur :** DISCOVER APPROVED ✅

**MDAN Core génère la mise à jour MDAN-STATE.json :**

```json
{
  "mdan_version": "2.0.0",
  "project": { "name": "taskflow-api", "type": "api-only", "detected_profile": "STANDARD" },
  "current_phase": "DESIGN",
  "phase_history": [
    { "phase": "DISCOVER", "status": "VALIDATED", "artifacts": ["mdan_output/PRD.md"] }
  ]
}
```

---

# PHASE 2 : DESIGN

## Session 2 — LLM : Claude (reprise)

**Utilisateur :** MDAN RESUME SESSION [colle MDAN-STATE.json]

**MDAN Core :**
```
[MDAN CORE — SESSION RESUMED]
📁 TaskFlow API — STANDARD profile
📍 Phase : DESIGN
✅ DISCOVER validé — PRD disponible

→ Action recommandée : Activer Architect Agent
```

---

**MDAN Core :** `[ACTIVATING: Architect Agent v2.0.0]`

**Architect Agent output (extrait) :**

```markdown
---
Artifact: Architecture Document
Phase: DESIGN
Agent: Architect Agent v2.0.0
---

## Architecture : TaskFlow API

### Pattern : Monolithe modulaire
Justification : Équipe de 5, scope délimité, pas besoin de microservices.
Un monolithe bien structuré est plus simple à maintenir et déployer.

### Stack
| Layer | Technologie | Justification |
|-------|------------|---------------|
| Runtime | Node.js 20 LTS | Contrainte équipe |
| Language | TypeScript 5.x | Type safety, DX |
| Framework | Fastify | 3x plus rapide qu'Express, validation native |
| Database | PostgreSQL 16 | ACID, relations claires |
| ORM | Prisma | Type-safe, migrations |
| Auth | JWT + API tokens | Stateless, developer-friendly |
| Test | Vitest + Supertest | Rapide, compatible TS |

### Data Models
```
Task
  id: UUID PK
  title: VARCHAR(255) NOT NULL
  description: TEXT
  status: ENUM('todo','in_progress','review','done') DEFAULT 'todo'
  priority: ENUM('low','medium','high','critical') DEFAULT 'medium'
  assignee_id: UUID FK → User
  sprint_id: UUID FK → Sprint (nullable)
  created_by: UUID FK → User
  created_at: TIMESTAMP
  updated_at: TIMESTAMP

User
  id: UUID PK
  email: VARCHAR(255) UNIQUE NOT NULL
  name: VARCHAR(100) NOT NULL
  role: ENUM('member','admin') DEFAULT 'member'
  api_token: VARCHAR(64) UNIQUE

Sprint
  id: UUID PK
  name: VARCHAR(100) NOT NULL
  start_date: DATE
  end_date: DATE
  status: ENUM('planned','active','completed') DEFAULT 'planned'
```

### API Design
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /auth/token | Get API token | Email+password |
| GET | /tasks | List tasks (filters: status, assignee, sprint) | Token |
| POST | /tasks | Create task | Token |
| GET | /tasks/:id | Get task | Token |
| PATCH | /tasks/:id | Update task | Token |
| DELETE | /tasks/:id | Delete task | Token + owner/admin |
| GET | /sprints | List sprints | Token |
| POST | /sprints | Create sprint | Token + admin |
| PATCH | /sprints/:id | Update sprint | Token + admin |

### Structure projet
```
taskflow-api/
├── src/
│   ├── app.ts           # Fastify instance
│   ├── server.ts        # Entry point
│   ├── config/          # Env, constants
│   ├── middleware/       # Auth, error handler
│   ├── modules/
│   │   ├── tasks/       # tasks.controller, .service, .repository, .schema
│   │   ├── sprints/
│   │   └── users/
│   └── shared/          # Types, utils, errors
├── prisma/
│   └── schema.prisma
├── tests/
│   ├── unit/
│   └── integration/
└── docker-compose.yml
```
```

**Utilisateur :** DESIGN APPROVED ✅

---

# PHASE 3 : BUILD

## Session 3 — LLM : Cursor (reprise via .cursorrules)

**MDAN Core :** `[ACTIVATING: Dev Agent v2.0.0]`  
**Feature :** US-001 — Create Task

**Dev Agent output :**

```typescript
// src/modules/tasks/tasks.schema.ts
import { z } from 'zod'

export const CreateTaskSchema = z.object({
  title: z.string().min(1).max(255),
  description: z.string().optional(),
  priority: z.enum(['low', 'medium', 'high', 'critical']).default('medium'),
  assignee_id: z.string().uuid().optional(),
  sprint_id: z.string().uuid().optional(),
})

export const UpdateTaskSchema = z.object({
  title: z.string().min(1).max(255).optional(),
  description: z.string().optional(),
  status: z.enum(['todo', 'in_progress', 'review', 'done']).optional(),
  priority: z.enum(['low', 'medium', 'high', 'critical']).optional(),
  assignee_id: z.string().uuid().nullable().optional(),
  sprint_id: z.string().uuid().nullable().optional(),
})
```

```typescript
// src/modules/tasks/tasks.service.ts
import { PrismaClient } from '@prisma/client'
import { z } from 'zod'
import { CreateTaskSchema, UpdateTaskSchema } from './tasks.schema'
import { NotFoundError, ForbiddenError } from '../../shared/errors'

export class TasksService {
  constructor(private prisma: PrismaClient) {}

  async create(data: z.infer<typeof CreateTaskSchema>, userId: string) {
    return this.prisma.task.create({
      data: {
        ...data,
        created_by: userId,
      },
      include: { assignee: true, sprint: true },
    })
  }

  async list(filters: { status?: string; assignee_id?: string; sprint_id?: string }) {
    return this.prisma.task.findMany({
      where: {
        ...(filters.status && { status: filters.status as any }),
        ...(filters.assignee_id && { assignee_id: filters.assignee_id }),
        ...(filters.sprint_id && { sprint_id: filters.sprint_id }),
      },
      include: { assignee: true, sprint: true },
      orderBy: { created_at: 'desc' },
    })
  }

  async update(id: string, data: z.infer<typeof UpdateTaskSchema>, userId: string) {
    const task = await this.prisma.task.findUnique({ where: { id } })
    if (!task) throw new NotFoundError('Task not found')
    
    return this.prisma.task.update({
      where: { id },
      data,
      include: { assignee: true, sprint: true },
    })
  }

  async delete(id: string, userId: string, userRole: string) {
    const task = await this.prisma.task.findUnique({ where: { id } })
    if (!task) throw new NotFoundError('Task not found')
    if (task.created_by !== userId && userRole !== 'admin') {
      throw new ForbiddenError('Not authorized to delete this task')
    }
    await this.prisma.task.delete({ where: { id } })
  }
}
```

```typescript
// tests/unit/tasks.service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { TasksService } from '../../src/modules/tasks/tasks.service'

const mockPrisma = {
  task: {
    create: vi.fn(),
    findMany: vi.fn(),
    findUnique: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  },
}

describe('TasksService', () => {
  let service: TasksService

  beforeEach(() => {
    vi.clearAllMocks()
    service = new TasksService(mockPrisma as any)
  })

  describe('create', () => {
    it('creates a task with required fields', async () => {
      const mockTask = { id: 'uuid-1', title: 'Fix bug', status: 'todo' }
      mockPrisma.task.create.mockResolvedValue(mockTask)

      const result = await service.create({ title: 'Fix bug' }, 'user-1')

      expect(mockPrisma.task.create).toHaveBeenCalledWith({
        data: { title: 'Fix bug', created_by: 'user-1' },
        include: { assignee: true, sprint: true },
      })
      expect(result).toEqual(mockTask)
    })

    it('creates a task with all optional fields', async () => {
      const input = {
        title: 'Fix bug',
        description: 'Critical issue',
        priority: 'high' as const,
        assignee_id: 'user-2',
      }
      mockPrisma.task.create.mockResolvedValue({ id: 'uuid-2', ...input })

      await service.create(input, 'user-1')
      expect(mockPrisma.task.create).toHaveBeenCalledWith(
        expect.objectContaining({ data: expect.objectContaining(input) })
      )
    })
  })

  describe('delete', () => {
    it('allows owner to delete their task', async () => {
      mockPrisma.task.findUnique.mockResolvedValue({ id: 't1', created_by: 'user-1' })
      await expect(service.delete('t1', 'user-1', 'member')).resolves.toBeUndefined()
    })

    it('allows admin to delete any task', async () => {
      mockPrisma.task.findUnique.mockResolvedValue({ id: 't1', created_by: 'user-2' })
      await expect(service.delete('t1', 'user-1', 'admin')).resolves.toBeUndefined()
    })

    it('throws ForbiddenError when non-owner non-admin tries to delete', async () => {
      mockPrisma.task.findUnique.mockResolvedValue({ id: 't1', created_by: 'user-2' })
      await expect(service.delete('t1', 'user-1', 'member')).rejects.toThrow('Not authorized')
    })

    it('throws NotFoundError for non-existent task', async () => {
      mockPrisma.task.findUnique.mockResolvedValue(null)
      await expect(service.delete('nonexistent', 'user-1', 'member')).rejects.toThrow('Task not found')
    })
  })
})
```

**MDAN Core :** `[ACTIVATING: Security Agent v2.0.0]` — revue de US-001

**Security Agent :**
```
Security Review — US-001 (Create Task)

FINDINGS:

✅ No CRITICAL issues
✅ No HIGH issues

MEDIUM — VULN-001: Missing rate limiting on POST /tasks
  Impact: A user could spam task creation
  Fix: Add rate limit middleware (100 req/min per token)
  Priority: Fix before VERIFY

LOW — VULN-002: No max length validation on description field
  Impact: Large payloads (DoS potential)
  Fix: Add z.string().max(10000) to description in schema

✅ Auth check present
✅ Owner check on delete
✅ No SQL injection risk (Prisma parameterized)
✅ No sensitive data in error messages
```

**MDAN-STATE.json mis à jour :**
```json
"features": [
  { "id": "US-001", "title": "Create Task", "status": "DONE", "tests": "PASSING", "security_review": "APPROVED (1 medium)" }
]
```

---

# PHASE 4 : VERIFY

**MDAN Core :** `[ACTIVATING: Test Agent v2.0.0]`

**Test Agent — résumé du plan de test :**

```
Test Plan : TaskFlow API

Coverage target : 80%
Tool : Vitest + Supertest

Unit tests     : 24 tests (tasks: 12, sprints: 6, auth: 6)
Integration    : 8 tests (full request cycle avec DB de test)
E2E scenarios  :
  1. ✅ Dev creates task, assigns it, moves through statuses to done
  2. ✅ Admin creates sprint, adds tasks, closes sprint
  3. ✅ Unauthorized user gets 401, wrong owner gets 403

Performance    : p95 < 100ms sous 50 req/s concurrentes (k6)

Results : 32/32 tests PASSING ✅
Coverage : 84% ✅
```

**Utilisateur :** VERIFY APPROVED ✅

---

# PHASE 5 : SHIP

**MDAN Core :** `[ACTIVATING: DevOps Agent v2.0.0]`  
**MDAN Core :** `[ACTIVATING: Doc Agent v2.0.0]`

**DevOps Agent — Dockerfile produit :**

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/prisma ./prisma
EXPOSE 3000
USER node
CMD ["node", "dist/server.js"]
```

**Doc Agent — README extrait :**

```markdown
# TaskFlow API

> API REST légère de gestion de tâches pour équipes techniques.

## Quick Start

```bash
git clone [repo]
cd taskflow-api
cp .env.example .env   # Configurer DATABASE_URL et JWT_SECRET
docker-compose up -d   # Lance PostgreSQL
npm install && npm run db:migrate && npm run dev
```

## Créer votre première tâche

```bash
# 1. Obtenir un token
curl -X POST http://localhost:3000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"email": "you@team.com", "password": "..."}'

# 2. Créer une tâche
curl -X POST http://localhost:3000/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Fix auth bug", "priority": "high"}'
```
```

---

## 🚀 SHIP COMPLETE

**MDAN-STATE.json final :**
```json
{
  "current_phase": "SHIP",
  "phase_history": [
    { "phase": "DISCOVER", "status": "VALIDATED" },
    { "phase": "DESIGN",   "status": "VALIDATED" },
    { "phase": "BUILD",    "status": "VALIDATED" },
    { "phase": "VERIFY",   "status": "VALIDATED" },
    { "phase": "SHIP",     "status": "VALIDATED" }
  ],
  "features": [
    { "id": "US-001", "status": "DONE" },
    { "id": "US-002", "status": "DONE" },
    { "id": "US-003", "status": "DONE" },
    { "id": "US-004", "status": "DONE" },
    { "id": "US-005", "status": "DONE" }
  ]
}
```

**Durée totale :** 3 sessions, 2 LLMs (Claude + Cursor), ~6h de travail effectif  
**Résultat :** API complète, testée, documentée, déployée

---

## Ce que cet exemple démontre

- **Reprise de session** : session 2 et 3 ont repris depuis MDAN-STATE.json sans perte de contexte
- **Multi-LLM** : Claude pour DISCOVER/DESIGN, Cursor pour BUILD — les agents fonctionnent identiquement
- **Sécurité intégrée** : la revue Security Agent sur US-001 a trouvé 2 issues résolues avant VERIFY
- **Profil adaptatif** : UX Agent skippé automatiquement (projet API-only)
- **Versioning** : tous les agents tracés en v2.0.0 dans MDAN-STATE.json
