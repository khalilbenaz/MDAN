# MDAN Architecture Documentation

This document provides a comprehensive overview of the MDAN architecture, including system design, component interactions, and technical decisions.

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Design Patterns](#design-patterns)
- [Security Considerations](#security-considerations)
- [Scalability](#scalability)
- [Performance](#performance)

---

## Overview

MDAN is an AI-driven development platform built on the Better Agents framework. It provides specialized agents for various domains including FinTech, DevOps/Azure, and Database Optimization.

### Key Architectural Principles

1. **Modularity** - Each agent is a self-contained module
2. **Extensibility** - Easy to add new agents and packs
3. **Testability** - Comprehensive testing framework
4. **Observability** - Full tracing and monitoring
5. **Interoperability** - MCP integration for tool access

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         AI IDE Layer                         │
│  (Claude Code, Cursor, or other AI-enabled IDEs)            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      MDAN Core Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Agent        │  │ Workflow     │  │ Prompt       │      │
│  │ Orchestrator │  │ Engine       │  │ Manager      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Agent Modules                           │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │ Core │ │ MMM  │ │ MMB  │ │ CIS  │ │ TEA  │ │Packs │   │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      MCP Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Filesystem   │  │ Brave Search │  │ Git/GitHub   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      External Services                       │
│  (OpenAI, Anthropic, GitHub, Brave Search, etc.)            │
└─────────────────────────────────────────────────────────────┘
```

---

## System Architecture

### Core Components

#### 1. Agent Orchestrator

The Agent Orchestrator is responsible for:
- Agent selection and instantiation
- Workflow coordination
- Task delegation
- Result aggregation
- Error handling and recovery

**Location:** `app/core/agents/mdan-master/`

**Key Responsibilities:**
- Parse user requests
- Select appropriate agents
- Coordinate multi-agent workflows
- Manage agent lifecycle
- Handle errors and retries

#### 2. Workflow Engine

The Workflow Engine manages:
- Workflow definition and execution
- Agent sequencing
- Parallel execution
- State management
- Workflow persistence

**Location:** `app/core/workflows/`

**Key Responsibilities:**
- Parse workflow definitions
- Execute workflow steps
- Manage workflow state
- Handle workflow errors
- Provide workflow metrics

#### 3. Prompt Manager

The Prompt Manager handles:
- Prompt versioning
- Prompt storage and retrieval
- Prompt validation
- Prompt updates

**Location:** `prompts/` and `prompts.json`

**Key Responsibilities:**
- Store versioned prompts
- Retrieve prompts by version
- Validate prompt structure
- Update prompts
- Track prompt changes

### Agent Modules

#### Core Module

**Purpose:** Provides core orchestration and coordination

**Components:**
- MDAN Master agent

**Location:** `app/core/agents/`

#### MMM Module

**Purpose:** Business Model & Management

**Components:**
- Analyst (Mary)
- Architect (Winston)
- Dev (Amelia)
- PM (John)
- QA (Quinn)
- Quick Flow Solo Dev (Barry)
- Scrum Master (Bob)
- Tech Writer (Paige)
- UX Designer (Sally)

**Location:** `app/mmm/agents/`

#### MMB Module

**Purpose:** Module Builder

**Components:**
- Agent Builder (Bond)
- Module Builder (Morgan)
- Workflow Builder (Wendy)

**Location:** `app/mmb/agents/`

#### CIS Module

**Purpose:** Creative Innovation Strategy

**Components:**
- Brainstorming Coach (Carson)
- Creative Problem Solver (Dr. Quinn)
- Design Thinking Coach (Maya)
- Innovation Strategist (Victor)
- Presentation Master (Caravaggio)
- Storyteller (Sophia)

**Location:** `app/cis/agents/`

#### TEA Module

**Purpose:** Test Engineering & Architecture

**Components:**
- TEA (Murat)

**Location:** `app/tea/agents/`

#### Packs

**Purpose:** Specialized domain-specific agents

**Components:**
- FinTech Pack (3 agents)
- DevOps/Azure Pack (3 agents)
- DB Optimization Pack (3 agents)

**Location:** `app/packs/`

---

## Component Architecture

### Agent Structure

Each agent follows a consistent structure:

```
app/{module}/agents/{agent-name}/
├── __init__.py           # Agent exports
├── agent.py              # Agent implementation
└── prompt.yaml           # Versioned prompt
```

#### Agent Implementation (agent.py)

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

#### Prompt Definition (prompt.yaml)

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

### Testing Structure

```
tests/
├── scenarios/            # End-to-end scenario tests
│   ├── core/
│   ├── mmm/
│   ├── mmb/
│   ├── cis/
│   ├── tea/
│   └── packs/
└── evaluations/          # Jupyter notebooks for evaluations
    ├── core/
    ├── mmm/
    ├── mmb/
    ├── cis/
    ├── tea/
    └── packs/
```

#### Scenario Tests

Scenario tests use the Scenario testing framework:

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

---

## Data Flow

### Request Flow

```
1. User submits request to AI IDE
   ↓
2. AI IDE forwards request to MDAN Core
   ↓
3. Agent Orchestrator parses request
   ↓
4. Agent Orchestrator selects appropriate agent(s)
   ↓
5. Prompt Manager retrieves agent prompt
   ↓
6. Agent processes request with LLM
   ↓
7. Agent may use MCP tools for additional capabilities
   ↓
8. Agent returns result to Agent Orchestrator
   ↓
9. Agent Orchestrator aggregates results (if multi-agent)
   ↓
10. Result returned to AI IDE
   ↓
11. AI IDE displays result to user
```

### Multi-Agent Workflow Flow

```
1. User submits complex request
   ↓
2. Agent Orchestrator identifies need for multi-agent workflow
   ↓
3. Workflow Engine loads workflow definition
   ↓
4. Workflow Engine executes workflow steps:
   a. Step 1: Agent A processes task
   b. Step 2: Agent B processes task (may depend on A)
   c. Step 3: Agent C processes task (may depend on B)
   ↓
5. Workflow Engine aggregates results
   ↓
6. Workflow Engine returns final result
   ↓
7. Result returned to user
```

---

## Technology Stack

### Core Technologies

- **Node.js** v20+ - Runtime environment
- **Python** v3.8+ - Agent implementation
- **TypeScript** - Type-safe development
- **YAML** - Prompt configuration

### Frameworks and Libraries

- **Better Agents** - Agent development framework
- **Scenario** - Agent testing framework
- **MCP (Model Context Protocol)** - Tool integration
- **Pydantic** - Data validation

### AI/ML

- **OpenAI API** - GPT models
- **Anthropic API** - Claude models

### Development Tools

- **npm** - Package management
- **Git** - Version control
- **ESLint** - Linting
- **Prettier** - Code formatting

---

## Design Patterns

### 1. Agent Pattern

Each agent is a self-contained module with:
- Clear responsibilities
- Defined interface
- Independent testing

### 2. Orchestrator Pattern

The Agent Orchestrator coordinates multiple agents:
- Selects appropriate agents
- Manages agent lifecycle
- Aggregates results

### 3. Strategy Pattern

Different agents implement different strategies for:
- Problem-solving
- Communication
- Task execution

### 4. Factory Pattern

Agent creation uses factory methods:
- Dynamic agent instantiation
- Configuration-based creation
- Extensible agent types

### 5. Observer Pattern

Workflow execution uses observers for:
- Progress tracking
- Event handling
- State updates

---

## Security Considerations

### API Key Management

- API keys stored in environment variables
- Never committed to version control
- Rotated regularly
- Access restricted to necessary services

### Input Validation

- All user inputs validated
- Sanitized before processing
- Type-checked with Pydantic
- Length limits enforced

### Output Sanitization

- Agent outputs sanitized
- Sensitive data redacted
- HTML/JS escaped
- File paths validated

### MCP Tool Security

- MCP tools run in isolated environments
- File system access restricted to project directory
- Git operations require authentication
- GitHub tokens scoped appropriately

### Logging and Auditing

- All agent activities logged
- Sensitive data not logged
- Audit trail maintained
- Logs rotated and archived

---

## Scalability

### Horizontal Scaling

- Stateless agent design
- Distributed execution possible
- Load balancing support
- Container-ready architecture

### Vertical Scaling

- Efficient resource usage
- Async/await for I/O operations
- Connection pooling
- Caching strategies

### Performance Optimization

- Lazy loading of agents
- Prompt caching
- Result caching
- Parallel execution where possible

---

## Performance

### Response Time Targets

- Simple agent requests: < 5 seconds
- Multi-agent workflows: < 30 seconds
- Complex workflows: < 2 minutes

### Optimization Strategies

1. **Prompt Optimization**
   - Concise prompts
   - Clear instructions
   - Minimal context

2. **Caching**
   - Prompt caching
   - Result caching
   - Agent instance caching

3. **Parallel Execution**
   - Independent agents run in parallel
   - Concurrent MCP tool calls
   - Async I/O operations

4. **Resource Management**
   - Connection pooling
   - Memory management
   - Efficient data structures

### Monitoring

- Response time tracking
- Agent performance metrics
- Error rate monitoring
- Resource usage monitoring

---

## Future Enhancements

### Planned Features

1. **Agent Marketplace**
   - Community-contributed agents
   - Agent ratings and reviews
   - Easy agent installation

2. **Advanced Workflows**
   - Conditional workflows
   - Loop workflows
   - Event-driven workflows

3. **Enhanced Testing**
   - Automated test generation
   - Performance testing
   - Load testing

4. **Improved Observability**
   - Distributed tracing
   - Real-time monitoring
   - Alerting

5. **Multi-Model Support**
   - Support for more LLM providers
   - Model routing
   - Cost optimization

---

**Last Updated:** 28 February 2026
**Version:** 1.0.0