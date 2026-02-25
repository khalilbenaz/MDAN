# CrewAI Orchestrator Documentation

## Overview

The CrewAI Orchestrator is a comprehensive integration of CrewAI into MDANV2, providing intelligent multi-agent orchestration, skill routing, and autonomous development capabilities.

## Architecture

```
integrations/crewai/
├── agents/           # CrewAI agents (8 specialized agents)
├── flows/            # CrewAI flows (4 orchestration flows)
├── tools/            # Custom tools (Serper, SQL, File)
├── skills/           # Skill router for intelligent task routing
└── orchestrator.py   # Main orchestrator class
```

## Components

### Agents

Eight specialized CrewAI agents mapped to MDAN phases:

| Agent | Phase | Expertise |
|-------|-------|-----------|
| ProductAgent (Khalil) | DISCOVER | Requirements, PRD, user stories |
| ArchitectAgent (Reda) | DESIGN | Architecture, tech stack, ADR |
| UXAgent (Jihane) | DESIGN | User flows, wireframes, design system |
| DevAgent (Haytame) | BUILD | Implementation, refactoring, debugging |
| TestAgent (Youssef) | VERIFY | Testing strategy, test execution |
| SecurityAgent (Said) | BUILD+VERIFY | Security review, vulnerability assessment |
| DevOpsAgent (Anas) | SHIP | Deployment, CI/CD, infrastructure |
| DocAgent (Amina) | SHIP | Documentation, user guides |

### Flows

Four CrewAI flows for different orchestration patterns:

1. **AutoFlow** - Full autonomous development cycle (8 phases)
2. **DiscoveryFlow** - DISCOVER phase orchestration
3. **BuildFlow** - BUILD phase orchestration
4. **DebateFlow** - Multi-agent debate for consensus

### Tools

Three custom tools for agent capabilities:

1. **SerperTool** - Web search via Serper API
2. **SQLTool** - Async SQL connector (PostgreSQL, MySQL, SQLServer, SQLite)
3. **FileTool** - File operations (read, write, list, copy, move)

### Skill Router

Intelligent skill detection and routing:

- Detects required skills from task descriptions
- Routes tasks to appropriate agents
- Supports 50+ skills across all domains
- Maintains execution history

## Installation

```bash
# Install CrewAI dependencies
pip install -r requirements_crewai.txt

# Set environment variables
export SERPER_API_KEY="your-serper-api-key"
export OPENAI_API_KEY="your-openai-api-key"  # or other LLM provider
```

## Usage

### Basic Usage

```python
import asyncio
from integrations.crewai.orchestrator import CrewAIOrchestrator

async def main():
    # Initialize orchestrator
    orchestrator = CrewAIOrchestrator(
        project_path="/path/to/project",
        llm=your_llm_instance,
        sql_config={
            "db_type": "postgresql",
            "host": "localhost",
            "port": 5432,
            "database": "mydb",
            "user": "user",
            "password": "password"
        },
        serper_api_key="your-serper-api-key"
    )

    # Execute a task
    result = await orchestrator.execute_task(
        "Create a PRD for a todo app"
    )
    print(result)

asyncio.run(main())
```

### Autonomous Mode

```python
# Enable autonomous mode
orchestrator = CrewAIOrchestrator(
    project_path="/path/to/project",
    llm=your_llm_instance,
    auto_mode=True
)

# Run full autonomous development cycle
result = await orchestrator.run_auto_mode(
    "Build a todo app with user authentication"
)
```

### Multi-Agent Debate

```python
# Start a debate on a topic
result = await orchestrator.start_debate(
    "Should we use PostgreSQL or MongoDB for this project?"
)
```

### Skill-Based Execution

```python
from integrations.crewai.skills import SkillRouter

# Initialize skill router
skill_router = SkillRouter(orchestrator)

# Execute based on detected skills
result = await skill_router.execute_skills(
    "Create unit tests for the authentication module"
)
```

### Custom Crew

```python
from crewai import Process

# Create a custom crew with specific agents
crew = orchestrator.create_crew(
    agent_names=["architect", "dev", "test"],
    process=Process.sequential
)

# Execute tasks with the crew
from crewai import Task

tasks = [
    Task(
        description="Design the system architecture",
        agent=orchestrator.agents["architect"].get_agent()
    ),
    Task(
        description="Implement the features",
        agent=orchestrator.agents["dev"].get_agent()
    ),
    Task(
        description="Write tests",
        agent=orchestrator.agents["test"].get_agent()
    )
]

result = await orchestrator.execute_crew(crew, tasks)
```

## Configuration

### SQL Configuration

```python
sql_config = {
    "db_type": "postgresql",  # or "mysql", "sqlserver", "sqlite"
    "host": "localhost",
    "port": 5432,
    "database": "mydb",
    "user": "user",
    "password": "password",
    "pool_size": 10,
    "max_overflow": 20
}
```

### LLM Configuration

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key="your-api-key"
)

orchestrator = CrewAIOrchestrator(
    project_path="/path/to/project",
    llm=llm
)
```

## API Reference

### CrewAIOrchestrator

#### Methods

- `analyze_task(task_description: str) -> Dict[str, Any]` - Analyze task and determine agent/flow
- `execute_task(task_description: str, context: Optional[Dict] = None) -> Dict[str, Any]` - Execute a task
- `run_auto_mode(user_input: str) -> Dict[str, Any]` - Run autonomous mode
- `start_debate(topic: str) -> Dict[str, Any]` - Start multi-agent debate
- `create_crew(agent_names: List[str], process: Process, verbose: bool) -> Crew` - Create custom crew
- `execute_crew(crew: Crew, tasks: List[Task]) -> Dict[str, Any]` - Execute crew with tasks
- `get_state() -> Dict[str, Any]` - Get orchestrator state
- `save_state(filepath: str)` - Save state to file
- `load_state(filepath: str)` - Load state from file
- `enable_auto_mode()` - Enable autonomous mode
- `disable_auto_mode()` - Disable autonomous mode
- `is_auto_mode_enabled() -> bool` - Check auto mode status

### SkillRouter

#### Methods

- `detect_skills(task_description: str) -> Set[Skill]` - Detect required skills
- `get_agent_for_skill(skill: Skill) -> Optional[str]` - Get agent for skill
- `execute_skills(task_description: str, context: Optional[Dict] = None) -> Dict[str, Any]` - Execute skills
- `get_skill_execution_history() -> List[Dict]` - Get execution history
- `clear_skill_execution_history()` - Clear history
- `get_all_skills() -> List[str]` - Get all available skills

## Available Skills

### Product Skills
- requirement_analysis
- prd_creation
- user_story_writing
- persona_creation
- feature_prioritization
- acceptance_criteria

### Architecture Skills
- system_architecture
- tech_stack_selection
- adr_documentation
- api_design
- database_schema

### UX Skills
- user_flow_design
- wireframe_creation
- design_system
- accessibility
- prototype_creation

### Development Skills
- implementation
- refactoring
- code_review
- testing
- debugging

### Testing Skills
- test_strategy
- unit_testing
- integration_testing
- e2e_testing
- test_execution
- performance_testing
- security_testing
- test_automation
- quality_gate

### Security Skills
- security_review
- vulnerability_scan
- secure_coding
- dependency_security
- authentication_security
- data_protection
- api_security
- security_monitoring
- compliance_review

### DevOps Skills
- ci_cd_pipeline
- docker_setup
- kubernetes_setup
- azure_deployment
- monitoring_setup
- deployment_strategy
- infrastructure_as_code
- backup_recovery
- scaling_strategy
- security_hardening

### Documentation Skills
- readme_creation
- api_documentation
- user_guide
- developer_guide
- architecture_documentation
- changelog
- troubleshooting_guide
- migration_guide
- code_examples
- release_notes

### Tool Skills
- web_search
- sql_query
- file_operation

## State Management

The orchestrator maintains state that can be saved and loaded:

```python
# Save state
orchestrator.save_state("orchestrator_state.json")

# Load state
orchestrator.load_state("orchestrator_state.json")
```

## Context Save/Load

Flows support context save/load for resuming:

```python
# Save flow context
flow = orchestrator.flows["auto"]
flow.save_context("auto_flow_context.json")

# Load flow context
loaded_flow = AutoFlow.load_context("auto_flow_context.json", llm=your_llm)
```

## Error Handling

All async methods return a result dictionary with status:

```python
result = await orchestrator.execute_task("some task")

if result["status"] == "success":
    print("Task completed:", result["result"])
else:
    print("Task failed:", result["error"])
```

## Best Practices

1. **Use appropriate flows** - Use AutoFlow for full cycles, specific flows for single phases
2. **Enable auto mode carefully** - Auto mode executes all phases without intervention
3. **Monitor execution** - Check state and task history for progress
4. **Save state regularly** - Save state after major milestones
5. **Use skill routing** - Let SkillRouter detect and route skills automatically
6. **Configure tools properly** - Ensure SQL and Serper tools are configured correctly
7. **Handle errors gracefully** - Check result status before proceeding

## Troubleshooting

### Common Issues

1. **CrewAI import errors**
   - Ensure `crewai>=0.80.0` is installed
   - Check Python version (3.9+)

2. **SQL connection errors**
   - Verify database credentials
   - Check database is accessible
   - Ensure correct db_type is specified

3. **Serper API errors**
   - Verify SERPER_API_KEY is set
   - Check API key is valid

4. **LLM errors**
   - Verify API key is set
   - Check model is available
   - Ensure sufficient credits

## Integration with MDAN CLI

The CrewAI orchestrator can be integrated with the existing MDAN CLI:

```python
# In cli/mdan.py
from integrations.crewai.orchestrator import CrewAIOrchestrator

def cmd_auto(args):
    orchestrator = CrewAIOrchestrator(
        project_path=args.project,
        llm=get_llm(),
        auto_mode=True
    )
    result = asyncio.run(orchestrator.run_auto_mode(args.input))
    print(result)
```

## Future Enhancements

- [ ] Add more specialized agents
- [ ] Implement skill caching
- [ ] Add parallel execution support
- [ ] Implement skill composition
- [ ] Add real-time progress monitoring
- [ ] Implement skill learning from execution history
- [ ] Add support for custom skills
- [ ] Implement skill versioning