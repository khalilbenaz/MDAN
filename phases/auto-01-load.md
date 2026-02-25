# Auto Phase 1: LOAD

> Load project context and requirements

## Objective

Load and initialize the project context, including requirements, existing code, and configuration.

## Tasks

### 1.1 Load Project Configuration

- Read project configuration file
- Validate configuration
- Load environment variables
- Set up project structure

### 1.2 Load Requirements

- Read requirements document
- Parse user stories
- Identify acceptance criteria
- Load constraints and assumptions

### 1.3 Load Existing Code

- Check for existing codebase
- If exists, analyze structure
- Identify tech stack
- Load dependencies

### 1.4 Initialize Context

- Create initial context state
- Set token tracking
- Initialize logging
- Create output directories

### 1.5 Validate Environment

- Check required tools
- Verify dependencies
- Validate file permissions
- Check disk space

## Output

Generate `docs/load.md`:

```markdown
# Load Phase

## Project Information

**Name**: [Project name]
**Description**: [Project description]
**Version**: [Version]

## Requirements

### User Stories

- [Story 1]
- [Story 2]
- [Story 3]

### Acceptance Criteria

- [Criteria 1]
- [Criteria 2]
- [Criteria 3]

### Constraints

- [Constraint 1]
- [Constraint 2]

## Tech Stack

- **Language**: C#
- **Framework**: .NET 8.0
- **UI**: Blazor Server
- **Database**: SQL Server 2022
- **Cloud**: Azure

## Existing Code

[Analysis of existing code if present]

## Environment

- **Tools**: [List of tools]
- **Dependencies**: [List of dependencies]
- **Status**: Ready/Not Ready

## Next Steps

Proceed to DISCOVER phase.
```

## Quality Gates

- [ ] Project configuration loaded
- [ ] Requirements identified
- [ ] Environment validated
- [ ] Context initialized

## Success Criteria

- All project information loaded
- Requirements clearly defined
- Environment ready for development
- No critical errors

## Error Handling

### Configuration Not Found

- Log error
- Use default configuration
- Continue with warning

### Requirements Not Found

- Log error
- Ask for requirements (if interactive)
- Or use placeholder requirements

### Environment Not Ready

- Log error
- Provide setup instructions
- Abort if critical

## Token Management

Track token usage:
- Initial load: ~1,000 tokens
- Context initialization: ~500 tokens
- Environment validation: ~500 tokens

Total: ~2,000 tokens

## Logging

```
[timestamp] Starting LOAD phase
[timestamp] Loading project configuration...
[timestamp] Loading requirements...
[timestamp] Loading existing code...
[timestamp] Initializing context...
[timestamp] Validating environment...
[timestamp] Token usage: X / 128,000 (X%)
[timestamp] LOAD phase complete
```

## Completion Signal

```
PHASE 1 COMPLETE ✅
```

## Version

MDAN-AUTO Phase 1: LOAD v1.0