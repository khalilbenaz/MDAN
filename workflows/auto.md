# MDAN-AUTO Workflow

> Autonomous Full-Cycle Development Workflow

## Overview

MDAN-AUTO is an autonomous development mode that executes the complete software development lifecycle without human intervention. It coordinates all phases, manages context, and ensures mission completion.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     MDAN-AUTO v1.0                              │
│                  Autonomous Orchestrator                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. LOAD                                                        │
│  - Load project configuration                                   │
│  - Load requirements                                            │
│  - Load existing code                                           │
│  - Initialize context                                           │
│  - Validate environment                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. DISCOVER                                                    │
│  - Analyze requirements                                         │
│  - Define user stories                                          │
│  - Define acceptance criteria                                   │
│  - Identify dependencies                                        │
│  - Create feature list                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. PLAN                                                        │
│  - Create implementation plan                                   │
│  - Define phase structure (#PHASE1, #PHASE2...)                 │
│  - Create task list                                             │
│  - Define milestones                                            │
│  - Create risk plan                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. ARCHITECT                                                   │
│  - Design system architecture                                   │
│  - Design data models                                           │
│  - Design security architecture                                 │
│  - Design API architecture                                      │
│  - Design deployment architecture                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. IMPLEMENT                                                   │
│  - Execute #PHASE1 tasks                                        │
│  - Execute #PHASE2 tasks                                        │
│  - Execute #PHASE3 tasks                                        │
│  - Execute #PHASE4 tasks                                        │
│  - Execute #PHASE5 tasks                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  6. TEST                                                        │
│  - Run unit tests                                               │
│  - Run integration tests                                        │
│  - Run E2E tests                                                │
│  - Run security tests                                           │
│  - Run performance tests                                        │
│  - Generate test report                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  7. DEPLOY                                                      │
│  - Pre-deployment checks                                        │
│  - Prepare deployment                                           │
│  - Deploy to staging                                            │
│  - Deploy to production                                         │
│  - Post-deployment verification                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  8. DOC                                                         │
│  - Update README                                                │
│  - Generate API documentation                                   │
│  - Create user guide                                            │
│  - Create deployment guide                                      │
│  - Create developer guide                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  MISSION COMPLETE ✅                             │
└─────────────────────────────────────────────────────────────────┘
```

## Phase Details

### Phase 1: LOAD

**Objective**: Load and initialize the project context.

**Tasks**:
- Load project configuration
- Load requirements
- Load existing code
- Initialize context
- Validate environment

**Output**: `docs/load.md`

**Quality Gates**:
- [ ] Project configuration loaded
- [ ] Requirements identified
- [ ] Environment validated
- [ ] Context initialized

**Signal**: `PHASE 1 COMPLETE ✅`

---

### Phase 2: DISCOVER

**Objective**: Analyze requirements and define user stories.

**Tasks**:
- Analyze requirements
- Define user stories
- Define acceptance criteria
- Identify dependencies
- Create feature list

**Output**: `docs/discover.md`

**Quality Gates**:
- [ ] All user stories defined
- [ ] Acceptance criteria clear
- [ ] Dependencies identified
- [ ] MVP scope defined

**Signal**: `PHASE 2 COMPLETE ✅`

---

### Phase 3: PLAN

**Objective**: Create detailed implementation plan.

**Tasks**:
- Create implementation plan
- Define phase structure (#PHASE1, #PHASE2...)
- Create task list
- Define milestones
- Create risk plan

**Output**: `docs/plan.md`

**Quality Gates**:
- [ ] All phases defined
- [ ] Tasks broken down
- [ ] Dependencies mapped
- [ ] Effort estimated

**Signal**: `PHASE 3 COMPLETE ✅`

---

### Phase 4: ARCHITECT

**Objective**: Design system architecture.

**Tasks**:
- Design system architecture
- Design data models
- Design security architecture
- Design API architecture
- Design deployment architecture

**Output**: `docs/architecture.md`

**Quality Gates**:
- [ ] Architecture documented
- [ ] Data models defined
- [ ] Security designed
- [ ] API designed
- [ ] Deployment planned

**Signal**: `PHASE 4 COMPLETE ✅`

---

### Phase 5: IMPLEMENT

**Objective**: Execute implementation tasks.

**Tasks**:
- Execute #PHASE1 tasks (Foundation and Setup)
- Execute #PHASE2 tasks (Core Features)
- Execute #PHASE3 tasks (Advanced Features)
- Execute #PHASE4 tasks (Integration)
- Execute #PHASE5 tasks (Testing and Polish)

**Output**: `docs/implementation.md`

**Quality Gates**:
- [ ] All tasks completed
- [ ] Code compiles
- [ ] No critical errors
- [ ] All acceptance criteria met

**Signal**: `PHASE 5 COMPLETE ✅`

---

### Phase 6: TEST

**Objective**: Run comprehensive tests.

**Tasks**:
- Run unit tests
- Run integration tests
- Run E2E tests
- Run security tests
- Run performance tests
- Generate test report

**Output**: `docs/test-report.md`

**Quality Gates**:
- [ ] All tests pass (or acceptable failure rate)
- [ ] Coverage ≥80%
- [ ] No critical security issues
- [ ] Performance meets requirements

**Signal**: `PHASE 6 COMPLETE ✅`

---

### Phase 7: DEPLOY

**Objective**: Deploy to production.

**Tasks**:
- Pre-deployment checks
- Prepare deployment
- Deploy to staging
- Deploy to production
- Post-deployment verification

**Output**: `docs/deployment.md`

**Quality Gates**:
- [ ] All tests pass
- [ ] Staging deployment successful
- [ ] Production deployment successful
- [ ] Monitoring active
- [ ] Zero downtime

**Signal**: `PHASE 7 COMPLETE ✅`

---

### Phase 8: DOC

**Objective**: Generate documentation.

**Tasks**:
- Update README
- Generate API documentation
- Create user guide
- Create deployment guide
- Create developer guide

**Output**: `docs/documentation.md`

**Quality Gates**:
- [ ] All documentation complete
- [ ] Quality verified
- [ ] Delivered to channels
- [ ] Version controlled

**Signal**: `PHASE 8 COMPLETE ✅`
**Final Signal**: `MISSION COMPLETE ✅`

---

## Context Management

### Token Monitoring

- Track token usage for all LLM calls
- Calculate percentage of context limit
- Default limit: 128,000 tokens (configurable)

### Context Save

When token usage ≥80%:

1. Create save file: `/tmp/mdan-save-[timestamp].json`
2. Save:
   - Current phase
   - All agent outputs
   - Generated artifacts
   - Conversation history
   - Project state
3. Emit signal: `CONTEXT SAVE [file]`
4. Continue execution

### Context Resume

When resuming from save:

1. Load save file
2. Restore conversation history
3. Resume from saved phase
4. Continue execution

## Multi-Agent Debates

### When to Debate

Trigger debate for:
- Architecture decisions
- Technology stack choices
- Security approaches
- Performance optimizations
- Complex implementation strategies

### Debate Process

1. **Select Participants**: Choose relevant agents
2. **Present Question**: Clear, specific question with context
3. **Collect Arguments**: Each agent provides perspective
4. **Score Arguments**: Evaluate based on criteria
5. **Select Winner**: Choose best argument
6. **Document Decision**: Record rationale

### Debate Output

```markdown
## Debate: [Topic]

### Question
[Clear question]

### Participants
- Agent A
- Agent B
- Agent C

### Arguments
[Agent arguments]

### Decision
**Winner**: Agent B

**Rationale**: [Reasoning]

### Implementation
[How decision will be implemented]
```

## Fail-Fast Policy

### Critical Errors

Abort immediately on:
- LLM API failures (after 3 retries)
- File system errors
- Dependency installation failures
- Build failures
- Test failures (if configured as critical)
- Deployment failures

### Error Handling

1. Log error with full context
2. Save current state
3. Emit error signal
4. Exit with non-zero code
5. Provide recovery instructions

## Tech Stack Support

### C#/.NET/Blazor

- Use .NET 8.0 or later
- Blazor Server or WebAssembly
- Entity Framework Core for data access
- ASP.NET Core for APIs

### SQL Server

- Use SQL Server 2022 or Azure SQL Database
- Entity Framework Core migrations
- Stored procedures for complex queries
- Indexes for performance

### Azure Services

- Azure App Service for hosting
- Azure SQL Database for data
- Azure Key Vault for secrets
- Azure DevOps for CI/CD
- Azure Container Registry for Docker

### External Services

- Generic external service integration
- Multiple service support
- Retry logic and circuit breaker
- Rate limiting and caching
- Secure token management

## Output Signals

Emit these signals at key points:

```
PHASE 1 COMPLETE ✅
PHASE 2 COMPLETE ✅
PHASE 3 COMPLETE ✅
PHASE 4 COMPLETE ✅
PHASE 5 COMPLETE ✅
PHASE 6 COMPLETE ✅
PHASE 7 COMPLETE ✅
PHASE 8 COMPLETE ✅
CONTEXT SAVE /tmp/mdan-save-1234567890.json
MISSION COMPLETE ✅
```

## File Structure

Generate outputs in this structure:

```
project/
├── docs/
│   ├── load.md
│   ├── discover.md
│   ├── plan.md
│   ├── architecture.md
│   ├── implementation.md
│   ├── test-report.md
│   ├── deployment.md
│   └── documentation.md
├── src/
│   └── [implementation files]
├── tests/
│   └── [test files]
├── deployment/
│   ├── docker/
│   ├── azure/
│   └── sql/
└── README.md
```

## Configuration

Default configuration (can be overridden):

```yaml
token_limit: 128000
save_threshold: 0.8
output_dir: ./mdan-auto-output
log_level: INFO
fail_fast: true
debate_enabled: true
tech_stack:
  language: csharp
  framework: dotnet
  ui: blazor
  database: sqlserver
  cloud: azure
```

## Logging

Log all actions with timestamps:

```
[2024-01-15 10:00:00] Starting MDAN-AUTO v1.0
[2024-01-15 10:00:01] PHASE 1: LOAD
[2024-01-15 10:00:15] PHASE 1 COMPLETE ✅
[2024-01-15 10:00:16] PHASE 2: DISCOVER
[2024-01-15 10:01:23] PHASE 2 COMPLETE ✅
[2024-01-15 10:01:24] PHASE 3: PLAN
[2024-01-15 10:02:45] PHASE 3 COMPLETE ✅
[2024-01-15 10:02:46] PHASE 4: ARCHITECT
[2024-01-15 10:04:12] PHASE 4 COMPLETE ✅
[2024-01-15 10:04:13] PHASE 5: IMPLEMENT
[2024-01-15 10:15:34] PHASE 5 COMPLETE ✅
[2024-01-15 10:15:35] PHASE 6: TEST
[2024-01-15 10:18:22] PHASE 6 COMPLETE ✅
[2024-01-15 10:18:23] PHASE 7: DEPLOY
[2024-01-15 10:20:45] PHASE 7 COMPLETE ✅
[2024-01-15 10:20:46] PHASE 8: DOC
[2024-01-15 10:22:10] PHASE 8 COMPLETE ✅
[2024-01-15 10:22:11] MISSION COMPLETE ✅
```

## Usage

### Starting Auto Mode

```bash
mdan auto
```

This will:
1. Initialize the Auto Orchestrator
2. Load the auto-orchestrator.md prompt
3. Begin autonomous execution
4. Execute all phases sequentially
5. Save context at 80% token limit
6. Complete mission

### Resuming from Save

```bash
mdan resume /tmp/mdan-save-1234567890.json
```

This will:
1. Load the save file
2. Restore conversation history
3. Resume from saved phase
4. Continue execution

## Best Practices

1. **Always validate** before resuming
2. **Log everything** for debugging
3. **Handle errors gracefully**
4. **Provide clear recovery instructions**
5. **Track resume attempts**
6. **Clean up old saves** after success
7. **Backup saves** before resume
8. **Verify environment** before resume

## Troubleshooting

### Context Save Issues

If context save fails:
- Check disk space
- Verify file permissions
- Check /tmp directory exists
- Review error logs

### Resume Issues

If resume fails:
- Validate save file format
- Check file integrity
- Verify version compatibility
- Review error logs

### Phase Failures

If a phase fails:
- Check error logs
- Review phase output
- Verify quality gates
- Fix issues and retry

## Version

MDAN-AUTO Workflow v1.0