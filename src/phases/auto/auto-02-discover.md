# Auto Phase 2: DISCOVER

> Analyze requirements and define user stories

## Objective

Analyze requirements, define user stories, and create acceptance criteria for the project.

## Tasks

### 2.1 Analyze Requirements

- Review loaded requirements
- Identify key features
- Prioritize features
- Define MVP scope

### 2.2 Define User Stories

- Create user stories for each feature
- Format: "As a [role], I want [feature], so that [benefit]"
- Assign priority (Must Have, Should Have, Could Have, Won't Have)
- Estimate complexity

### 2.3 Define Acceptance Criteria

- Create acceptance criteria for each user story
- Define measurable outcomes
- Identify edge cases
- Specify constraints

### 2.4 Identify Dependencies

- Map dependencies between stories
- Identify external dependencies
- Define integration points
- Note blocking issues

### 2.5 Create Feature List

- Compile all features
- Organize by priority
- Group by functionality
- Estimate effort

## Output

Generate `docs/discover.md`:

```markdown
# Discover Phase

## Project Overview

[Project description and goals]

## Features

### Must Have (MVP)

#### Feature 1: [Feature Name]

**User Story**:
As a [role], I want [feature], so that [benefit].

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Priority**: Must Have
**Complexity**: [Low/Medium/High]
**Dependencies**: [None/Feature X]

---

#### Feature 2: [Feature Name]

[Same structure]

---

### Should Have

[Features for v1.1]

### Could Have

[Features for future versions]

### Won't Have

[Features explicitly out of scope]

## Dependencies

### Internal Dependencies

- Feature A depends on Feature B
- Feature C depends on Feature D

### External Dependencies

- [External service 1]
- [External service 2]

## Integration Points

- [Integration point 1]
- [Integration point 2]

## Technical Considerations

- [Consideration 1]
- [Consideration 2]

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [High/Medium/Low] | [Mitigation] |
| [Risk 2] | [High/Medium/Low] | [Mitigation] |

## MVP Scope

**Included**:
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Excluded**:
- [Feature 4]
- [Feature 5]

## Next Steps

Proceed to PLAN phase.
```

## Quality Gates

- [ ] All user stories defined
- [ ] Acceptance criteria clear
- [ ] Dependencies identified
- [ ] MVP scope defined

## Success Criteria

- User stories cover all requirements
- Acceptance criteria are measurable
- Dependencies are mapped
- MVP scope is realistic

## Error Handling

### Unclear Requirements

- Log warning
- Make reasonable assumptions
- Document assumptions
- Continue with note

### Conflicting Requirements

- Trigger debate
- Resolve conflict
- Document decision
- Continue

### Missing Information

- Log warning
- Use defaults
- Document gaps
- Continue

## Token Management

Track token usage:
- Requirements analysis: ~2,000 tokens
- User story creation: ~3,000 tokens
- Acceptance criteria: ~2,000 tokens
- Dependencies: ~1,000 tokens

Total: ~8,000 tokens

## Logging

```
[timestamp] Starting DISCOVER phase
[timestamp] Analyzing requirements...
[timestamp] Defining user stories...
[timestamp] Creating acceptance criteria...
[timestamp] Identifying dependencies...
[timestamp] Token usage: X / 128,000 (X%)
[timestamp] DISCOVER phase complete
```

## Completion Signal

```
PHASE 2 COMPLETE ✅
```

## Version

MDAN-AUTO Phase 2: DISCOVER v1.0