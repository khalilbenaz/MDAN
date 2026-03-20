# Multi-Agent Debate Protocol

> MDAN-AUTO v1.0 Decision-Making Through Agent Collaboration

## Overview

The debate protocol enables multiple MDAN agents to collaborate on complex decisions, providing diverse perspectives and ensuring well-considered choices.

## When to Trigger a Debate

Trigger a debate for:

- **Architecture Decisions**
  - Monolith vs microservices
  - Design patterns
  - Technology stack choices
  - System boundaries

- **Security Decisions**
  - Authentication methods
  - Authorization models
  - Encryption strategies
  - Security controls

- **Performance Decisions**
  - Caching strategies
  - Database optimization
  - Scaling approaches
  - Resource allocation

- **Implementation Decisions**
  - Code organization
  - Library choices
  - Testing strategies
  - Error handling

- **DevOps Decisions**
  - Deployment strategies
  - CI/CD pipelines
  - Infrastructure choices
  - Monitoring approaches

## Debate Participants

### Core Agents

| Agent | Expertise | Debate Topics |
|-------|-----------|---------------|
| Product | Requirements, user needs | Feature decisions, UX choices |
| Architect | System design, patterns | Architecture, technology stack |
| Dev | Implementation, code quality | Implementation approaches, libraries |
| Security | Security, compliance | Security controls, authentication |
| Test | Testing, quality | Testing strategies, quality gates |
| DevOps | Deployment, infrastructure | Deployment, CI/CD, infrastructure |
| Doc | Documentation | Documentation approaches |

### Participant Selection

Select participants based on topic:

**Architecture Decisions:**
- Architect (lead)
- Dev
- DevOps
- Security

**Security Decisions:**
- Security (lead)
- Architect
- Dev
- DevOps

**Performance Decisions:**
- Dev (lead)
- Architect
- DevOps

**Implementation Decisions:**
- Dev (lead)
- Architect
- Test

**DevOps Decisions:**
- DevOps (lead)
- Architect
- Security

**Feature Decisions:**
- Product (lead)
- Architect
- Doc

## Debate Process

### Step 1: Define Question

Create a clear, specific question:

```
❌ Bad: "How should we do authentication?"

✅ Good: "Should we use JWT tokens or session-based authentication
for a Blazor Server application with Azure AD integration?"
```

Include:
- Context
- Constraints
- Requirements
- Trade-offs

### Step 2: Select Participants

Choose relevant agents:
- Lead agent (primary expertise)
- Supporting agents (related expertise)
- 3-5 agents maximum

### Step 3: Present Question

Send question to all participants with:
- Clear question
- Context
- Constraints
- Requirements
- Deadline (optional)

### Step 4: Collect Arguments

Each participant provides:

1. **Recommendation**: Clear choice
2. **Rationale**: Why this choice
3. **Pros**: Benefits of choice
4. **Cons**: Drawbacks of choice
5. **Evidence**: Supporting facts/experience
6. **Alternatives**: Other options considered

### Step 5: Score Arguments

Score each argument on:

| Criteria | Weight | Description |
|----------|--------|-------------|
| Technical Merit | 30% | Technical soundness |
| Alignment | 25% | Alignment with requirements |
| Security | 20% | Security implications |
| Maintainability | 15% | Long-term maintainability |
| Feasibility | 10% | Implementation feasibility |

Total score: 0-100

### Step 6: Select Winner

Choose argument with highest score.

If scores are close (<5% difference):
- Consider hybrid approach
- Or defer to lead agent

### Step 7: Document Decision

Record:
- Question
- Participants
- Arguments
- Scores
- Winner
- Rationale
- Implementation plan

### Step 8: Implement

Apply decision to implementation.

## Debate Output Format

```markdown
## Debate: [Topic]

### Question
[Clear, specific question with context]

### Context
- Project: [Project name]
- Phase: [Current phase]
- Requirements: [Key requirements]
- Constraints: [Constraints]

### Participants
- **Lead**: [Agent name] - [Role]
- [Agent name] - [Role]
- [Agent name] - [Role]

### Arguments

#### [Agent Name]
**Recommendation**: [Choice]

**Rationale**: [Why this choice]

**Pros**:
- [Benefit 1]
- [Benefit 2]

**Cons**:
- [Drawback 1]
- [Drawback 2]

**Evidence**: [Supporting facts]

**Alternatives Considered**:
- [Alternative 1] - [Why rejected]
- [Alternative 2] - [Why rejected]

**Score**: [0-100]

---

#### [Agent Name]
[Same structure]

---

### Scoring Summary

| Agent | Technical | Alignment | Security | Maintainability | Feasibility | Total |
|-------|-----------|-----------|----------|-----------------|-------------|-------|
| Agent A | 25 | 20 | 15 | 12 | 8 | 80 |
| Agent B | 28 | 23 | 18 | 14 | 9 | 92 |
| Agent C | 22 | 18 | 16 | 11 | 7 | 74 |

### Decision
**Winner**: [Agent name]

**Rationale**: [Why this argument won]

**Score**: [Winning score]

### Implementation
[How decision will be implemented]

### Next Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Timestamp
[ISO 8601 timestamp]
```

## Debate Example

```markdown
## Debate: Authentication Strategy

### Question
Should we use JWT tokens or session-based authentication for a Blazor Server
application with Azure AD integration?

### Context
- Project: External Service Integration
- Phase: ARCHITECT
- Requirements: Secure authentication, Azure AD integration, session management
- Constraints: Must support multiple external service APIs

### Participants
- **Lead**: Security - Security expertise
- Architect - System design
- Dev - Implementation

### Arguments

#### Security
**Recommendation**: JWT tokens with Azure AD

**Rationale**: JWT provides stateless authentication, works well with Azure AD,
and is industry standard for modern applications.

**Pros**:
- Stateless, no server-side session storage
- Works seamlessly with Azure AD
- Industry standard
- Easy to scale
- Built-in expiration and refresh

**Cons**:
- Token revocation is complex
- Larger payload size
- Requires careful token validation

**Evidence**: OWASP recommends JWT for stateless authentication. Azure AD
natively issues JWT tokens.

**Alternatives Considered**:
- Session-based - Rejected due to scaling concerns
- Hybrid - Rejected due to complexity

**Score**: 92

---

#### Architect
**Recommendation**: Session-based authentication

**Rationale**: Blazor Server maintains server-side state, session-based auth
aligns better with the architecture.

**Pros**:
- Natural fit for Blazor Server
- Easy to implement
- Built-in session management
- Simple revocation

**Cons**:
- Requires server-side storage
- Harder to scale
- Session affinity required
- More complex with Azure AD

**Evidence**: Blazor Server documentation recommends session-based auth for
server-side rendering.

**Alternatives Considered**:
- JWT - Rejected due to Blazor Server architecture
- Hybrid - Rejected due to complexity

**Score**: 78

---

#### Dev
**Recommendation**: JWT tokens with Azure AD

**Rationale**: JWT is easier to implement with Azure AD and provides better
separation of concerns.

**Pros**:
- Easy Azure AD integration
- Standard libraries available
- Clear separation of auth logic
- Better for API calls

**Cons**:
- Token management complexity
- Refresh token handling

**Evidence**: Microsoft.Identity.Web library provides excellent JWT support
for Azure AD.

**Alternatives Considered**:
- Session-based - Rejected due to Azure AD complexity

**Score**: 88

---

### Scoring Summary

| Agent | Technical | Alignment | Security | Maintainability | Feasibility | Total |
|-------|-----------|-----------|----------|-----------------|-------------|-------|
| Security | 28 | 23 | 18 | 14 | 9 | 92 |
| Architect | 22 | 20 | 14 | 12 | 10 | 78 |
| Dev | 26 | 22 | 16 | 13 | 11 | 88 |

### Decision
**Winner**: Security

**Rationale**: JWT with Azure AD provides the best security posture, aligns
with industry standards, and has excellent Azure integration. The slight
complexity is outweighed by security benefits and scalability.

**Score**: 92

### Implementation
1. Configure Azure AD app registration
2. Implement JWT token validation middleware
3. Use Microsoft.Identity.Web library
4. Implement token refresh logic
5. Add token validation to API endpoints

### Next Steps
1. Create Azure AD app registration
2. Implement authentication middleware
3. Update Blazor Server configuration
4. Test authentication flow
5. Document authentication approach

### Timestamp
2024-01-15T10:15:00Z
```

## Debate Timeout

Set timeout for debates:
- Default: 5 minutes per agent
- Maximum: 30 minutes total
- If timeout, use available arguments

## Debate Cancellation

Cancel debate if:
- Question is unclear
- Insufficient context
- Emergency situation
- User intervention

## Debate Storage

Store debates in:
- `context.debates` array in save file
- Separate debate log file
- Decision history

## Debate Quality

Ensure debate quality:
- Clear questions
- Relevant participants
- Well-reasoned arguments
- Evidence-based decisions
- Proper documentation

## Debate Automation

Automate debate triggering:
- Detect complex decisions
- Select participants automatically
- Collect arguments
- Score and decide
- Document and implement

## Debate Review

Review debates periodically:
- Check decision quality
- Validate implementation
- Learn from outcomes
- Improve process

## Best Practices

1. **Clear Questions**: Be specific and provide context
2. **Right Participants**: Choose agents with relevant expertise
3. **Evidence-Based**: Use facts and experience
4. **Fair Scoring**: Use consistent criteria
5. **Document Everything**: Record full debate
6. **Implement Decisions**: Apply decisions consistently
7. **Review Outcomes**: Learn from results
8. **Time-Boxed**: Set reasonable timeouts

## Version

MDAN-AUTO Debate Protocol v1.0