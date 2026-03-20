# MDAN Contribution Guide

This guide will help you contribute to MDAN. We welcome contributions from everyone!

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Pull Request Process](#pull-request-process)
- [Community Guidelines](#community-guidelines)

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Node.js** v20.0.0 or higher
- **npm** v9.0.0 or higher
- **Python** v3.8 or higher
- **Git** installed and configured
- An AI IDE (Claude Code, Cursor, or similar)

### Setting Up Your Development Environment

1. **Fork the repository**

    ```bash
    # Fork the repository on GitHub
    # Clone your fork
    git clone https://github.com/your-username/MDANV2.git
    cd MDANV2
    ```

2. **Install dependencies**

   ```bash
   # Install Node.js dependencies
   npm install

   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env with your configuration
   nano .env
   ```

4. **Run tests to verify setup**

   ```bash
   npm test
   ```

5. **Create a branch for your contribution**

   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## Development Workflow

### 1. Find an Issue

- Browse [GitHub Issues](https://github.com/khalilbenaz/MDANV2/issues) for open issues
- Look for issues labeled `good first issue` if you're new
- Comment on the issue to let others know you're working on it

### 2. Create a Branch

```bash
# Use a descriptive branch name
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Your Changes

- Follow the coding standards below
- Write tests for your changes
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run all tests
npm test

# Run scenario tests
npm run test:scenarios

# Run evaluations
npm run test:evaluations

# Run linting
npm run lint

# Run formatting
npm run format
```

### 5. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add new agent for X"

# Use conventional commit messages:
# feat: new feature
# fix: bug fix
# docs: documentation changes
# style: formatting changes
# refactor: code refactoring
# test: adding or updating tests
# chore: maintenance tasks
```

### 6. Push Your Changes

```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

- Go to the GitHub repository
- Click "New Pull Request"
- Select your branch
- Fill in the PR template
- Submit the PR

---

## Coding Standards

### Python Code

#### Style Guide

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://github.com/psf/black) for formatting (88 character line length)
- Use [isort](https://github.com/PyCQA/isort) for import sorting
- Use [flake8](https://github.com/PyCQA/flake8) or [ruff](https://github.com/charliermarsh/ruff) for linting

#### Type Hints

- Use type hints for all function signatures
- Use `typing` module for complex types
- Use `dataclasses` or `pydantic` for structured data

```python
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

@dataclass
class AgentRequest:
    """Request data structure for the agent."""
    field1: str
    field2: Optional[int] = None
    field3: List[str] = None

class MyAgent:
    """My agent description."""

    async def process(self, request: AgentRequest) -> Dict[str, Any]:
        """Process the request."""
        # Implementation
        pass
```

#### Docstrings

- Use Google or NumPy style docstrings
- Include description, args, returns, raises, examples

```python
def my_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    Brief description of the function.

    Detailed description of what the function does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        A dictionary containing the result

    Raises:
        ValueError: If param1 is invalid

    Examples:
        >>> my_function("test", 42)
        {'result': 'success'}
    """
    # Implementation
    pass
```

#### Function Design

- Keep functions under 50 lines
- Use descriptive variable names
- Extract common logic to helper functions
- Single responsibility principle

### JavaScript/TypeScript Code

#### Style Guide

- Follow [ESLint](https://eslint.org/) rules
- Use [Prettier](https://prettier.io/) for formatting
- Use TypeScript for type safety

#### Type Safety

- Avoid `any` type
- Use proper types
- Enable strict mode in TypeScript

```typescript
interface AgentRequest {
  field1: string;
  field2?: number;
  field3?: string[];
}

class MyAgent {
  async process(request: AgentRequest): Promise<Record<string, unknown>> {
    // Implementation
    return {};
  }
}
```

### YAML Files

#### Prompt Files

- Use consistent indentation (2 spaces)
- Use descriptive names
- Include version and description

```yaml
name: my-agent
version: 1.0.0
description: Brief description of the agent

system_prompt: |
  You are My Agent, a specialist in X.

  Your capabilities:
  - Capability 1
  - Capability 2

user_prompt_template: |
  {template for user prompts}
```

---

## Testing Guidelines

### Test Coverage

- Aim for 80%+ test coverage
- Test all public functions and methods
- Test edge cases and error conditions

### Unit Tests

- Test individual functions and methods in isolation
- Use mocks for external dependencies
- Follow Arrange-Act-Assert pattern

```python
import pytest
from unittest.mock import Mock, patch

def test_my_function():
    """Test my_function."""
    # Arrange
    input_data = "test"
    expected_output = "result"

    # Act
    result = my_function(input_data)

    # Assert
    assert result == expected_output
```

### Integration Tests

- Test agent interactions
- Test workflows
- Test MCP tool integration

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_agent_integration():
    """Test agent integration."""
    agent = MyAgent()
    request = AgentRequest(field1="test")

    result = await agent.process(request)

    assert "expected_key" in result
    assert result["expected_key"] == "expected_value"
```

### Scenario Tests

- Create realistic scenario tests
- Test end-to-end workflows
- Use the Scenario testing framework

```python
from scenario import Scenario, expect

scenario = Scenario("My Agent - Test Description")

@scenario.test
async def test_my_agent_scenario():
    """Test my agent scenario."""
    agent = MyAgent()
    request = AgentRequest(field1="test")

    result = await agent.process(request)

    expect(result).to_have_key("expected_key")
    expect(result["expected_key"]).to_equal("expected_value")
```

### Test Organization

```
tests/
├── scenarios/            # Scenario tests
│   ├── core/
│   ├── mmm/
│   ├── mmb/
│   ├── cis/
│   ├── tea/
│   └── packs/
└── evaluations/          # Evaluation notebooks
    ├── core/
    ├── mmm/
    ├── mmb/
    ├── cis/
    ├── tea/
    └── packs/
```

---

## Documentation Guidelines

### Code Documentation

- Include docstrings for all public functions and classes
- Add comments for complex logic
- Provide usage examples

### Agent Documentation

- Update [AGENTS_LIST.md](./AGENTS_LIST.md) when adding new agents
- Include agent description, capabilities, and usage examples
- Update [AGENTS.md](./AGENTS.md) with agent development guidelines

### README Updates

- Update [README.md](./README.md) for major features
- Update installation instructions if needed
- Update usage examples

### Architecture Documentation

- Update [ARCHITECTURE.md](./ARCHITECTURE.md) for architectural changes
- Document design decisions
- Include diagrams for complex systems

---

## Pull Request Process

### PR Template

When creating a PR, fill in the PR template:

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
```

### PR Review Process

1. **Automated Checks**
   - All tests must pass
   - Code must pass linting
   - Coverage must not decrease

2. **Code Review**
   - At least one maintainer must review
   - Address all review comments
   - Make requested changes

3. **Approval**
   - Get approval from maintainers
   - Resolve all conflicts
   - Squash commits if needed

4. **Merge**
   - Maintainer merges the PR
   - PR is deleted after merge

### PR Best Practices

- Keep PRs focused and small
- Write clear commit messages
- Respond to review comments promptly
- Update PR based on feedback
- Delete your branch after merge

---

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions

### Communication

- Use GitHub issues for bug reports and feature requests
- Use GitHub discussions for questions and ideas
- Be clear and concise in your communication
- Use appropriate labels and milestones

### Recognition

- Credit contributors in release notes
- Highlight significant contributions
- Thank contributors for their work

---

## Getting Help

If you need help:

1. Check the [Documentation](./README.md)
2. Search [GitHub Issues](https://github.com/khalilbenaz/MDANV2/issues)
3. Visit the [Repository](https://github.com/khalilbenaz/MDANV2)
4. Check the [npm Package](https://www.npmjs.com/package/mdan)

---

## Resources

- [Installation Guide](./INSTALL.md)
- [Usage Guide](./USAGE.md)
- [Agent List](./AGENTS_LIST.md)
- [Architecture Documentation](./ARCHITECTURE.md)
- [AGENTS.md](./AGENTS.md) - Agent development guidelines

---

**Last Updated:** 28 February 2026
**Version:** 1.0.0