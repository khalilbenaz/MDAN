# MDAN Usage Guide

This guide will help you use MDAN effectively in your development workflow.

## 🚀 Quick Start

### Using MDAN with an AI IDE

MDAN is designed to work seamlessly with AI IDEs like Claude Code and Cursor.

1. **Open your project** in your AI IDE
2. **Select an agent** from the agent selector
3. **Provide your task** to the agent
4. **Review the results** and iterate as needed

### Example: Using the Financial Analyst Agent

```
You: I need to analyze the financial performance of our SaaS product over the last quarter.

Agent (Financial Analyst): I'll help you analyze the financial performance. Please provide:
1. Revenue data for the last quarter
2. Customer acquisition costs
3. Churn rates
4. Any other relevant metrics

[Agent processes the data and provides analysis]
```

## 🤖 Using Agents

### Agent Selection

MDAN provides 23 specialized agents across 4 core modules and 3 specialized packs:

#### Core Module (1 agent)
- **MDAN Master** - Orchestrates all MDAN agents and workflows

#### MMM Module (9 agents)
- **Analyst (Mary)** - Research and analysis
- **Architect (Winston)** - System architecture and design
- **Dev (Amelia)** - Development and implementation
- **PM (John)** - Project management
- **QA (Quinn)** - Quality assurance and testing
- **Quick Flow Solo Dev (Barry)** - Rapid development
- **Scrum Master (Bob)** - Agile facilitation
- **Tech Writer (Paige)** - Technical documentation
- **UX Designer (Sally)** - User experience design

#### MMB Module (3 agents)
- **Agent Builder (Bond)** - Create custom agents
- **Module Builder (Morgan)** - Create custom modules
- **Workflow Builder (Wendy)** - Create custom workflows

#### CIS Module (6 agents)
- **Brainstorming Coach (Carson)** - Facilitate brainstorming sessions
- **Creative Problem Solver (Dr. Quinn)** - Solve complex problems creatively
- **Design Thinking Coach (Maya)** - Guide design thinking processes
- **Innovation Strategist (Victor)** - Develop innovation strategies
- **Presentation Master (Caravaggio)** - Create compelling presentations
- **Storyteller (Sophia)** - Craft engaging narratives

#### TEA Module (1 agent)
- **TEA (Murat)** - Test Engineering & Architecture

#### FinTech Pack (3 agents)
- **Financial Analyst** - Financial modeling and analysis
- **Compliance Officer** - Regulatory compliance
- **Risk Manager** - Risk assessment and management

#### DevOps/Azure Pack (3 agents)
- **DevOps Engineer** - CI/CD and infrastructure
- **Azure Specialist** - Azure cloud services
- **CI/CD Architect** - Pipeline design and automation

#### DB Optimization Pack (3 agents)
- **DB Performance Analyst** - Database performance analysis
- **Query Optimizer** - Query optimization
- **Indexing Specialist** - Index design and tuning

See [AGENTS_LIST.md](./AGENTS_LIST.md) for detailed descriptions of each agent.

### Agent Interaction Patterns

#### 1. Sequential Workflow

Use multiple agents in sequence to complete complex tasks:

```
1. Analyst (Mary) - Research the problem
2. Architect (Winston) - Design the solution
3. Dev (Amelia) - Implement the solution
4. QA (Quinn) - Test the solution
5. Tech Writer (Paige) - Document the solution
```

#### 2. Parallel Collaboration

Use multiple agents simultaneously to work on different aspects:

```
1. UX Designer (Sally) - Design the UI
2. Dev (Amelia) - Implement the backend
3. QA (Quinn) - Write tests
```

#### 3. Specialized Pack Usage

Use specialized pack agents for domain-specific tasks:

```
FinTech Pack:
1. Financial Analyst - Analyze financial data
2. Compliance Officer - Ensure regulatory compliance
3. Risk Manager - Assess and mitigate risks
```

## 🎯 Common Use Cases

### Use Case 1: Building a New Feature

```
1. PM (John) - Define requirements and user stories
2. Analyst (Mary) - Research similar features and best practices
3. Architect (Winston) - Design the architecture
4. UX Designer (Sally) - Design the user interface
5. Dev (Amelia) - Implement the feature
6. QA (Quinn) - Write and execute tests
7. Tech Writer (Paige) - Document the feature
```

### Use Case 2: Database Optimization

```
1. DB Performance Analyst - Analyze database performance
2. Query Optimizer - Optimize slow queries
3. Indexing Specialist - Design optimal indexes
4. Dev (Amelia) - Implement optimizations
5. QA (Quinn) - Verify improvements
```

### Use Case 3: Cloud Migration to Azure

```
1. Azure Specialist - Assess current infrastructure
2. DevOps Engineer - Plan migration strategy
3. CI/CD Architect - Design deployment pipelines
4. Dev (Amelia) - Implement migration
5. QA (Quinn) - Test migrated system
```

### Use Case 4: Innovation Workshop

```
1. Brainstorming Coach (Carson) - Facilitate brainstorming
2. Creative Problem Solver (Dr. Quinn) - Generate creative solutions
3. Design Thinking Coach (Maya) - Apply design thinking
4. Innovation Strategist (Victor) - Develop strategy
5. Presentation Master (Caravaggio) - Create presentation
```

## 🛠️ Advanced Usage

### Custom Agent Creation

Use the Agent Builder to create custom agents:

```
You: I need an agent specialized in React Native development.

Agent (Agent Builder): I'll help you create a React Native specialist agent.
Please provide:
1. Agent name and title
2. Key capabilities
3. Communication style
4. Specific knowledge areas

[Agent creates the custom agent]
```

### Custom Workflow Creation

Use the Workflow Builder to create custom workflows:

```
You: I need a workflow for code review.

Agent (Workflow Builder): I'll help you create a code review workflow.
Please provide:
1. Workflow steps
2. Agents involved in each step
3. Success criteria
4. Output format

[Agent creates the custom workflow]
```

### Integration with MCP Tools

MDAN agents can use MCP tools for enhanced capabilities:

- **Filesystem** - Read and write files
- **Brave Search** - Search the web
- **Git** - Perform Git operations
- **GitHub** - Interact with GitHub

Example:
```
You: Search for best practices for React hooks and create a summary document.

Agent (Analyst): I'll search for best practices and create a summary.
[Uses Brave Search MCP tool]
[Uses Filesystem MCP tool to create document]
```

## 📊 Monitoring and Observability

### Agent Activity Logs

MDAN logs all agent activities for monitoring and debugging:

```bash
# View agent logs
tail -f logs/mdan.log

# Filter by agent
grep "Financial Analyst" logs/mdan.log

# Filter by date
grep "2026-02-28" logs/mdan.log
```

### Performance Metrics

Track agent performance metrics:

```bash
# View performance metrics
npm run metrics

# Export metrics to CSV
npm run metrics:export
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
npm test

# Run scenario tests
npm run test:scenarios

# Run evaluations
npm run test:evaluations

# Run tests for a specific module
npm test -- --module mmm
```

### Writing Tests

Create scenario tests for custom agents:

```python
from scenario import Scenario, expect

scenario = Scenario("Custom Agent - Test Description")

@scenario.test
async def test_custom_agent():
    """Test custom agent functionality."""
    agent = CustomAgent()
    request = CustomRequest(field1="value1")
    result = await agent.process(request)
    expect(result).to_have_key("expected_key")
```

## 🎓 Best Practices

### 1. Choose the Right Agent

- Use **Analyst** for research and analysis
- Use **Architect** for system design
- Use **Dev** for implementation
- Use **QA** for testing
- Use **PM** for project management
- Use specialized pack agents for domain-specific tasks

### 2. Provide Clear Context

Give agents clear, specific context:
- ✅ "Analyze the performance of our PostgreSQL database with 1M records"
- ❌ "Analyze the database"

### 3. Iterate and Refine

Work iteratively with agents:
1. Provide initial request
2. Review results
3. Provide feedback
4. Refine and iterate

### 4. Use Workflows for Complex Tasks

For complex tasks, use multiple agents in a workflow:
- Define clear steps
- Assign appropriate agents to each step
- Review outputs at each step

### 5. Document Your Work

Use the Tech Writer agent to document:
- Architecture decisions
- Implementation details
- Testing procedures
- Deployment guides

## 🔧 Configuration

### Agent Configuration

Configure agent behavior in `.env`:

```env
# Agent Configuration
MDAN_LOG_LEVEL=info
MDAN_MAX_CONCURRENT_AGENTS=5
MDAN_DEFAULT_TIMEOUT=300
MDAN_ENABLE_CACHING=true
```

### MCP Tool Configuration

Configure MCP tools in `.mcp.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
    }
  }
}
```

## 📚 Additional Resources

- [Installation Guide](./INSTALL.md)
- [Agent List](./AGENTS_LIST.md)
- [Architecture Documentation](./ARCHITECTURE.md)
- [Contribution Guide](./CONTRIBUTING.md)
- [AGENTS.md](./AGENTS.md) - Agent development guidelines

## 🤝 Getting Help

- Check the [Documentation](./README.md)
- Search [GitHub Issues](https://github.com/khalilbenaz/MDANV2/issues)
- Visit the [Repository](https://github.com/khalilbenaz/MDANV2)
- Check the [npm Package](https://www.npmjs.com/package/mdan)

---

**Last Updated:** 28 February 2026
**Version:** 1.0.0