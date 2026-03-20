# MDAN - Agent Development Guidelines

This document provides guidelines for developing agents in the MDAN project, following the Better Agents framework standards.

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Agent Development](#agent-development)
- [Testing](#testing)
- [Prompt Management](#prompt-management)
- [Best Practices](#best-practices)

---

## 🏗️ Project Structure

```
MDAN/
├── app/                      # Agent code
│   ├── core/                 # Core agents
│   │   └── agents/
│   ├── mmm/                  # Main module (Business Model & Management)
│   │   └── agents/
│   ├── mmb/                  # Module Builder
│   │   └── agents/
│   ├── cis/                  # Creative Innovation Strategy
│   │   └── agents/
│   ├── tea/                  # Test Engineering & Architecture
│   │   └── agents/
│   └── packs/                # Specialized packs
│       ├── fintech/
│       │   └── agents/
│       ├── devops-azure/
│       │   └── agents/
│       └── db-optimization/
│           └── agents/
├── tests/
│   ├── scenarios/            # End-to-end scenario tests
│   │   ├── core/
│   │   ├── mmm/
│   │   ├── mmb/
│   │   ├── cis/
│   │   ├── tea/
│   │   └── packs/
│   └── evaluations/          # Jupyter notebooks for evaluations
│       ├── core/
│       ├── mmm/
│       ├── mmb/
│       ├── cis/
│       ├── tea/
│       └── packs/
├── prompts/                  # Versioned prompts
│   ├── core/
│   ├── mmm/
│   ├── mmb/
│   ├── cis/
│   ├── tea/
│   └── packs/
├── prompts.json              # Prompt registry
├── .mcp.json                 # MCP server configuration
├── AGENTS.md                 # This file
├── CLAUDE.md                 # Claude Code compatibility
└── .env                      # Environment variables
```

---

## 🤖 Agent Development

### Agent Structure

Each agent should have the following structure:

```
app/{module}/agents/{agent-name}/
├── agent.py                  # Agent implementation
└── prompt.yaml               # Versioned prompt
```

### Agent Implementation (agent.py)

```python
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class AgentRequest:
    """Request data structure for the agent."""
    # Define your request fields here
    pass

class {AgentName}Agent:
    """
    Brief description of the agent.

    Detailed description of what the agent does,
    its capabilities, and its role in the system.
    """

    def __init__(self):
        """Initialize the agent."""
        self.name = "{Agent Name}"
        self.title = "{Agent Title}"
        self.icon = "{emoji}"

    async def process(self, request: AgentRequest) -> Dict[str, Any]:
        """
        Process the request and return a response.

        Args:
            request: The request to process

        Returns:
            A dictionary containing the response
        """
        # Implementation here
        pass
```

### Prompt Definition (prompt.yaml)

```yaml
name: {agent-name}
version: 1.0.0
description: Brief description of the agent

system_prompt: |
  You are {Agent Name}, a {Agent Title}.

  Your capabilities:
  - Capability 1
  - Capability 2
  - Capability 3

  Your communication style:
  - Style characteristic 1
  - Style characteristic 2

  Your principles:
  - Principle 1
  - Principle 2
  - Principle 3

user_prompt_template: |
  {template for user prompts}
```

---

## 🧪 Testing

### Scenario Tests

Every agent must have at least one scenario test in `tests/scenarios/{module}/{agent-name}.test.py`.

```python
from scenario import Scenario, expect

scenario = Scenario("{Agent Name} - Test Description")

@scenario.test
async def test_{test_name}():
    """
    Test description.
    """
    agent = {AgentName}Agent()

    request = AgentRequest(
        # Set request fields
    )

    result = await agent.process(request)

    # Assertions
    expect(result).to_have_key("expected_key")
    expect(result["expected_key"]).to_equal("expected_value")
```

### Evaluations

For agents with probabilistic components (RAG, classification, etc.), create evaluation notebooks in `tests/evaluations/{module}/{agent-name}.ipynb`.

---

## 📝 Prompt Management

### Versioning

All prompts must be versioned in YAML files in the `prompts/` directory.

### Prompt Registry

Update `prompts.json` when adding or modifying prompts:

```json
{
  "prompts": [
    {
      "name": "{agent-name}",
      "version": "1.0.0",
      "path": "prompts/{module}/{agent-name}.yaml",
      "description": "Brief description"
    }
  ]
}
```

---

## ✅ Best Practices

### 1. Agent Design

- **Single Responsibility**: Each agent should have a clear, focused purpose
- **Type Hints**: Use type hints for all function signatures
- **Async/Await**: Use async functions for I/O operations
- **Error Handling**: Implement proper error handling with specific exceptions

### 2. Prompt Design

- **Clear Instructions**: Provide clear, specific instructions
- **Examples**: Include examples in prompts when helpful
- **Constraints**: Specify constraints and boundaries
- **Tone**: Define the communication style and tone

### 3. Testing

- **Test Coverage**: Aim for high test coverage
- **Edge Cases**: Test edge cases and error conditions
- **Scenarios**: Create realistic scenario tests
- **Evaluations**: Use evaluations for probabilistic components

### 4. Documentation

- **Docstrings**: Include docstrings for all public functions
- **Comments**: Add comments for complex logic
- **Examples**: Provide usage examples
- **README**: Update module READMEs when adding agents

### 5. Code Quality

- **PEP 8**: Follow PEP 8 style guidelines
- **Linting**: Use linters to catch issues
- **Formatting**: Use consistent code formatting
- **Reviews**: Get code reviews before merging

---

## 🚀 Getting Started

### Creating a New Agent

1. Create the agent directory:
   ```bash
   mkdir -p app/{module}/agents/{agent-name}
   ```

2. Create `agent.py` with the agent implementation

3. Create `prompt.yaml` with the prompt definition

4. Create scenario test in `tests/scenarios/{module}/{agent-name}.test.py`

5. Update `prompts.json` with the new prompt

6. Run tests to verify:
   ```bash
   npm test
   ```

### Running Tests

```bash
# Run all tests
npm test

# Run scenario tests
npm run test:scenarios

# Run evaluations
npm run test:evaluations
```

---

## 📚 Resources

- [Better Agents Documentation](https://github.com/langwatch/better-agents)
- [Scenario Testing](https://github.com/langwatch/scenario)
- [LangWatch Documentation](https://docs.langwatch.ai)
- [MCP Protocol](https://modelcontextprotocol.io)

---

## 🤝 Contributing

When contributing to MDAN:

1. Follow the agent structure defined above
2. Include tests for all new agents
3. Update documentation
4. Follow code quality standards
5. Get code review before merging

---

**Last Updated:** 28 February 2026
**Version:** 1.0.0