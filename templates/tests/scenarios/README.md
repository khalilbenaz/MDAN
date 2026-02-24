# Test Scenarios Index

> End-to-end conversational tests for MDAN projects

## Overview

Scenarios are conversation-based tests that validate agent behavior in realistic, multi-turn interactions. Unlike unit tests, they simulate how real users interact with your agent.

## Available Scenarios

| Scenario | Description | Agent |
|----------|-------------|-------|
| [basic_authentication.test.md](basic_authentication.test.md) | Login, logout, session management | Dev Agent |
| [user_registration.test.md](user_registration.test.md) | Signup, validation, confirmation | Dev Agent |

## Adding New Scenarios

1. Copy this template:
   ```bash
   cp basic_authentication.test.md my_new_scenario.test.md
   ```

2. Edit the scenario:
   - Update metadata (name, version, framework)
   - Write the conversation script
   - Define success criteria
   - Add security checks if applicable

3. Run the scenario:
   ```bash
   # Python/pytest
   pytest tests/scenarios/my_new_scenario.test.md -v

   # Node/TypeScript
   npm test -- tests/scenarios/my_new_scenario.test.ts
   ```

## Scenario Format

Each scenario includes:
- **Metadata**: version, framework, duration estimate
- **Preconditions**: what must be true before testing
- **Script**: conversation steps with verification points
- **Success Criteria**: checklist of must-pass conditions
- **Security Checks**: validation for security requirements

## Integration with MDAN

Scenarios are automatically generated during the VERIFY phase:
1. Test Agent reviews implemented features
2. Creates relevant scenarios for critical flows
3. Runs scenarios to validate behavior
4. Reports results in quality gate

## Framework Support

| Framework | Command |
|-----------|---------|
| Jest | `jest tests/scenarios/` |
| Pytest | `pytest tests/scenarios/` |
| Playwright | `playwright test tests/scenarios/` |
| Vitest | `vitest run tests/scenarios/` |
