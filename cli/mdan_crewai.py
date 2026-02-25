#!/usr/bin/env python3
"""MDAN CrewAI CLI - CrewAI integration commands"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import click
except ImportError:
    print("Error: Click is required. Install with: pip install click")
    sys.exit(1)

# CrewAI imports - will be loaded lazily
CREWAI_AVAILABLE = False
try:
    from integrations.crewai.orchestrator import CrewAIOrchestrator
    from integrations.crewai.skills.skill_router import SkillRouter

    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False

# Colors
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
MAGENTA = "\033[0;35m"
BOLD = "\033[1m"
NC = "\033[0m"


def run_async(coro):
    """Run async coroutine in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@click.group(name="crewai")
def crewai_cli():
    """CrewAI integration commands for MDAN."""
    pass


@crewai_cli.command()
@click.option(
    "--project-path", default=".", help="Project path (default: current directory)"
)
def init(project_path):
    """Initialize CrewAI in a project."""
    project_path = Path(project_path).resolve()

    click.echo(f"{CYAN}🚀 Initializing CrewAI in: {BOLD}{project_path}{NC}")

    # Create crewai_config.yaml if it doesn't exist
    config_file = project_path / "crewai_config.yaml"

    if config_file.exists():
        click.echo(f"{YELLOW}⚠️  CrewAI config already exists at {config_file}{NC}")
        click.echo(f"  {BOLD}Next:{NC} Edit the config file to customize your setup")
        return

    default_config = """# CrewAI Configuration for MDAN
# Copy this file and customize for your project

# LLM Configuration
llm:
  provider: "openai"  # openai, anthropic, local
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 4096

# Database Configuration (optional)
database:
  type: "sqlite"  # postgresql, mysql, sqlserver, sqlite
  host: "localhost"
  port: 5432
  database: "mdan_db"
  username: ""
  password: ""
  
# Serper API Key (for web search)
serper_api_key: "${SERPER_API_KEY}"

# Auto Mode Settings
auto_mode:
  enabled: true
  save_context: true
  context_save_threshold: 0.8  # Save at 80% token usage
  
# Agent Settings
agents:
  product:
    enabled: true
    verbose: true
  architect:
    enabled: true
    verbose: true
  ux:
    enabled: true
    verbose: true
  dev:
    enabled: true
    verbose: true
  test:
    enabled: true
    verbose: true
  security:
    enabled: true
    verbose: true
  devops:
    enabled: true
    verbose: true
  doc:
    enabled: true
    verbose: true

# Flow Settings
flows:
  auto:
    enabled: true
  discovery:
    enabled: true
  build:
    enabled: true
  debate:
    enabled: true
"""

    config_file.write_text(default_config)

    # Create .env.example if it doesn't exist
    env_example = project_path / ".env.example"
    if not env_example.exists():
        env_example.write_text("""# CrewAI Environment Variables
# Copy this to .env and fill in your values

# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# Serper API Key (for web search)
SERPER_API_KEY=your-serper-api-key-here

# Database Configuration (optional)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mdan_db
DB_USER=your-db-user
DB_PASSWORD=your-db-password
""")

    click.echo(f"{GREEN}✅ CrewAI initialized successfully!{NC}")
    click.echo(f"  {BOLD}Config file:{NC} {config_file}")
    click.echo(f"  {BOLD}Env example:{NC} {env_example}")
    click.echo(f"\n  {BOLD}Next:{NC}")
    click.echo(f"  1. Copy .env.example to .env and fill in your API keys")
    click.echo(f"  2. Customize crewai_config.yaml if needed")
    click.echo(f"  3. Run: {CYAN}mdan crewai status{NC}")


@crewai_cli.command()
@click.argument("task")
@click.option(
    "--project-path", default=".", help="Project path (default: current directory)"
)
@click.option("--save-context", is_flag=True, help="Save context after execution")
def auto(task, project_path, save_context):
    """Run autonomous mode with a task."""
    if not CREWAI_AVAILABLE:
        click.echo(f"{RED}❌ CrewAI integration not found{NC}")
        click.echo(f"  Install with: {CYAN}pip install -r requirements_crewai.txt{NC}")
        click.echo(
            f"  Note: CrewAI requires Python 3.10-3.13 (current: {sys.version_info.major}.{sys.version_info.minor})"
        )
        sys.exit(1)

    project_path = Path(project_path).resolve()

    # Check for environment variables
    if not os.getenv("OPENAI_API_KEY"):
        click.echo(f"{RED}❌ OPENAI_API_KEY not set{NC}")
        click.echo(f"  Set it with: {CYAN}export OPENAI_API_KEY=your-key{NC}")
        sys.exit(1)

    click.echo(f"{CYAN}🚀 Starting autonomous mode...{NC}")
    click.echo(f"{BOLD}Task:{NC} {task}\n")

    try:
        orchestrator = CrewAIOrchestrator(
            project_path=str(project_path),
            auto_mode=True,
            serper_api_key=os.getenv("SERPER_API_KEY"),
        )

        result = run_async(orchestrator.run_auto_mode(task))

        if result.get("status") == "success":
            click.echo(f"\n{GREEN}✅ Autonomous mode completed successfully!{NC}")

            if save_context:
                state_file = project_path / "mdan_crewai_state.json"
                orchestrator.save_state(str(state_file))
                click.echo(f"  {BOLD}State saved:{NC} {state_file}")

            # Display result summary
            if "result" in result:
                click.echo(f"\n{BOLD}Result:{NC}")
                if isinstance(result["result"], dict):
                    click.echo(json.dumps(result["result"], indent=2))
                else:
                    click.echo(str(result["result"]))
        else:
            click.echo(f"\n{RED}❌ Error:{NC} {result.get('error', 'Unknown error')}")
            sys.exit(1)

    except Exception as e:
        click.echo(f"\n{RED}❌ Error:{NC} {str(e)}")
        sys.exit(1)


@crewai_cli.command()
@click.argument("topic")
@click.option(
    "--project-path", default=".", help="Project path (default: current directory)"
)
@click.option("--rounds", default=3, help="Number of debate rounds (default: 3)")
def debate(topic, project_path, rounds):
    """Start a multi-agent debate on a topic."""
    if not CREWAI_AVAILABLE:
        click.echo(f"{RED}❌ CrewAI integration not found{NC}")
        click.echo(f"  Install with: {CYAN}pip install -r requirements_crewai.txt{NC}")
        click.echo(
            f"  Note: CrewAI requires Python 3.10-3.13 (current: {sys.version_info.major}.{sys.version_info.minor})"
        )
        sys.exit(1)

    project_path = Path(project_path).resolve()

    if not os.getenv("OPENAI_API_KEY"):
        click.echo(f"{RED}❌ OPENAI_API_KEY not set{NC}")
        click.echo(f"  Set it with: {CYAN}export OPENAI_API_KEY=your-key{NC}")
        sys.exit(1)

    click.echo(f"{CYAN}🎯 Starting multi-agent debate...{NC}")
    click.echo(f"{BOLD}Topic:{NC} {topic}")
    click.echo(f"{BOLD}Rounds:{NC} {rounds}\n")

    try:
        orchestrator = CrewAIOrchestrator(
            project_path=str(project_path),
            serper_api_key=os.getenv("SERPER_API_KEY"),
        )

        result = run_async(orchestrator.start_debate(topic))

        if result.get("status") == "success":
            click.echo(f"\n{GREEN}✅ Debate completed!{NC}")

            if "result" in result:
                click.echo(f"\n{BOLD}Debate Summary:{NC}")
                if isinstance(result["result"], dict):
                    click.echo(json.dumps(result["result"], indent=2))
                else:
                    click.echo(str(result["result"]))
        else:
            click.echo(f"\n{RED}❌ Error:{NC} {result.get('error', 'Unknown error')}")
            sys.exit(1)

    except Exception as e:
        click.echo(f"\n{RED}❌ Error:{NC} {str(e)}")
        sys.exit(1)


@crewai_cli.command()
@click.argument("agent_name")
@click.argument("task")
@click.option(
    "--project-path", default=".", help="Project path (default: current directory)"
)
def agent(agent_name, task, project_path):
    """Execute a task with a specific agent."""
    if not CREWAI_AVAILABLE:
        click.echo(f"{RED}❌ CrewAI integration not found{NC}")
        click.echo(f"  Install with: {CYAN}pip install -r requirements_crewai.txt{NC}")
        click.echo(
            f"  Note: CrewAI requires Python 3.10-3.13 (current: {sys.version_info.major}.{sys.version_info.minor})"
        )
        sys.exit(1)

    project_path = Path(project_path).resolve()

    valid_agents = [
        "product",
        "architect",
        "ux",
        "dev",
        "test",
        "security",
        "devops",
        "doc",
    ]

    if agent_name not in valid_agents:
        click.echo(f"{RED}❌ Invalid agent: {agent_name}{NC}")
        click.echo(f"  Valid agents: {', '.join(valid_agents)}")
        sys.exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        click.echo(f"{RED}❌ OPENAI_API_KEY not set{NC}")
        click.echo(f"  Set it with: {CYAN}export OPENAI_API_KEY=your-key{NC}")
        sys.exit(1)

    click.echo(f"{CYAN}🤖 Executing task with {BOLD}{agent_name}{NC} agent...")
    click.echo(f"{BOLD}Task:{NC} {task}\n")

    try:
        orchestrator = CrewAIOrchestrator(
            project_path=str(project_path),
            serper_api_key=os.getenv("SERPER_API_KEY"),
        )

        result = run_async(orchestrator.execute_task(task))

        if result.get("status") == "success":
            click.echo(f"\n{GREEN}✅ Task completed!{NC}")

            if "result" in result:
                click.echo(f"\n{BOLD}Result:{NC}")
                if isinstance(result["result"], dict):
                    click.echo(json.dumps(result["result"], indent=2))
                else:
                    click.echo(str(result["result"]))
        else:
            click.echo(f"\n{RED}❌ Error:{NC} {result.get('error', 'Unknown error')}")
            sys.exit(1)

    except Exception as e:
        click.echo(f"\n{RED}❌ Error:{NC} {str(e)}")
        sys.exit(1)


@crewai_cli.command()
@click.argument("flow_name")
@click.argument("task")
@click.option(
    "--project-path", default=".", help="Project path (default: current directory)"
)
def flow(flow_name, task, project_path):
    """Execute a specific flow."""
    if not CREWAI_AVAILABLE:
        click.echo(f"{RED}❌ CrewAI integration not found{NC}")
        click.echo(f"  Install with: {CYAN}pip install -r requirements_crewai.txt{NC}")
        click.echo(
            f"  Note: CrewAI requires Python 3.10-3.13 (current: {sys.version_info.major}.{sys.version_info.minor})"
        )
        sys.exit(1)

    project_path = Path(project_path).resolve()

    valid_flows = ["auto", "discovery", "build", "debate"]

    if flow_name not in valid_flows:
        click.echo(f"{RED}❌ Invalid flow: {flow_name}{NC}")
        click.echo(f"  Valid flows: {', '.join(valid_flows)}")
        sys.exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        click.echo(f"{RED}❌ OPENAI_API_KEY not set{NC}")
        click.echo(f"  Set it with: {CYAN}export OPENAI_API_KEY=your-key{NC}")
        sys.exit(1)

    click.echo(f"{CYAN}🔄 Executing {BOLD}{flow_name}{NC} flow...")
    click.echo(f"{BOLD}Task:{NC} {task}\n")

    try:
        orchestrator = CrewAIOrchestrator(
            project_path=str(project_path),
            serper_api_key=os.getenv("SERPER_API_KEY"),
        )

        result = run_async(orchestrator.execute_task(task))

        if result.get("status") == "success":
            click.echo(f"\n{GREEN}✅ Flow completed!{NC}")

            if "result" in result:
                click.echo(f"\n{BOLD}Result:{NC}")
                if isinstance(result["result"], dict):
                    click.echo(json.dumps(result["result"], indent=2))
                else:
                    click.echo(str(result["result"]))
        else:
            click.echo(f"\n{RED}❌ Error:{NC} {result.get('error', 'Unknown error')}")
            sys.exit(1)

    except Exception as e:
        click.echo(f"\n{RED}❌ Error:{NC} {str(e)}")
        sys.exit(1)


@crewai_cli.command()
def skills():
    """List available skills."""
    if not CREWAI_AVAILABLE:
        click.echo(f"{RED}❌ CrewAI integration not found{NC}")
        click.echo(f"  Install with: {CYAN}pip install -r requirements_crewai.txt{NC}")
        click.echo(
            f"  Note: CrewAI requires Python 3.10-3.13 (current: {sys.version_info.major}.{sys.version_info.minor})"
        )
        sys.exit(1)

    click.echo(f"{CYAN}📚 Available Skills:{NC}\n")

    try:
        router = SkillRouter()
        all_skills = router.get_all_skills()

        # Group by category
        categories = {}
        for skill_name, skill_info in all_skills.items():
            category = skill_info.get("category", "General")
            if category not in categories:
                categories[category] = []
            categories[category].append((skill_name, skill_info))

        for category, skills in sorted(categories.items()):
            click.echo(f"{BOLD}{category}:{NC}")
            for skill_name, skill_info in skills:
                description = skill_info.get("description", "No description")
                click.echo(f"  • {skill_name}: {description}")
            click.echo()

    except Exception as e:
        click.echo(f"{RED}❌ Error loading skills: {str(e)}{NC}")
        sys.exit(1)


@crewai_cli.command()
@click.option(
    "--project-path", default=".", help="Project path (default: current directory)"
)
def status(project_path):
    """Show CrewAI status."""
    project_path = Path(project_path).resolve()

    click.echo(f"{CYAN}📊 CrewAI Status{NC}\n")

    # Check if CrewAI is available
    if not CREWAI_AVAILABLE:
        click.echo(f"{RED}❌ CrewAI integration not found{NC}")
        click.echo(f"  Install with: {CYAN}pip install -r requirements_crewai.txt{NC}")
        click.echo(
            f"  Note: CrewAI requires Python 3.10-3.13 (current: {sys.version_info.major}.{sys.version_info.minor})"
        )
        return

    # Check config file
    config_file = project_path / "crewai_config.yaml"
    if config_file.exists():
        click.echo(f"{GREEN}✅ Config file:{NC} {config_file}")
    else:
        click.echo(f"{YELLOW}⚠️  Config file not found{NC}")
        click.echo(f"  Run: {CYAN}mdan crewai init{NC}")
        return

    # Check environment variables
    click.echo(f"\n{BOLD}Environment Variables:{NC}")

    if os.getenv("OPENAI_API_KEY"):
        click.echo(f"  {GREEN}✅{NC} OPENAI_API_KEY: Set")
    else:
        click.echo(f"  {RED}❌{NC} OPENAI_API_KEY: Not set")

    if os.getenv("SERPER_API_KEY"):
        click.echo(f"  {GREEN}✅{NC} SERPER_API_KEY: Set")
    else:
        click.echo(f"  {YELLOW}⚠️{NC} SERPER_API_KEY: Not set (optional)")

    # Check state file
    state_file = project_path / "mdan_crewai_state.json"
    if state_file.exists():
        click.echo(f"\n{GREEN}✅ State file:{NC} {state_file}")
        try:
            with open(state_file) as f:
                state = json.load(f)
            click.echo(
                f"  {BOLD}Current Phase:{NC} {state.get('current_phase', 'N/A')}"
            )
            click.echo(
                f"  {BOLD}Auto Mode:{NC} {state.get('auto_mode_enabled', False)}"
            )
            click.echo(
                f"  {BOLD}Tasks Completed:{NC} {len(state.get('task_history', []))}"
            )
        except Exception:
            click.echo(f"  {YELLOW}⚠️  Could not read state file{NC}")

    # Check integrations
    click.echo(f"\n{BOLD}Integrations:{NC}")

    import importlib.util

    if importlib.util.find_spec("integrations.crewai.tools.serper_tool") is not None:
        click.echo(f"  {GREEN}✅{NC} Serper Tool: Available")
    else:
        click.echo(f"  {RED}❌{NC} Serper Tool: Not available")

    if importlib.util.find_spec("integrations.crewai.tools.sql_tool") is not None:
        click.echo(f"  {GREEN}✅{NC} SQL Tool: Available")
    else:
        click.echo(f"  {RED}❌{NC} SQL Tool: Not available")

    if importlib.util.find_spec("integrations.crewai.tools.file_tool") is not None:
        click.echo(f"  {GREEN}✅{NC} File Tool: Available")
    else:
        click.echo(f"  {RED}❌{NC} File Tool: Not available")

    # List agents
    click.echo(f"\n{BOLD}Available Agents:{NC}")
    agents = ["product", "architect", "ux", "dev", "test", "security", "devops", "doc"]
    for agent in agents:
        click.echo(f"  • {agent}")

    # List flows
    click.echo(f"\n{BOLD}Available Flows:{NC}")
    flows = ["auto", "discovery", "build", "debate"]
    for flow in flows:
        click.echo(f"  • {flow}")


if __name__ == "__main__":
    crewai_cli()
