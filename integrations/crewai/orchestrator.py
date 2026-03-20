"""CrewAI Orchestrator - Main orchestrator for CrewAI integration

Intelligent orchestrator that decides which agent/skill to call based on task analysis.
Supports auto-mode management, skill routing, and multi-agent debates.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from enum import Enum

from crewai import Crew, Process, Agent, Task

from .agents.product_agent import ProductAgent
from .agents.architect_agent import ArchitectAgent
from .agents.ux_agent import UXAgent
from .agents.dev_agent import DevAgent
from .agents.test_agent import TestAgent
from .agents.security_agent import SecurityAgent
from .agents.devops_agent import DevOpsAgent
from .agents.doc_agent import DocAgent

from .tools.sql_tool import SQLTool
from .tools.serper_tool import SerperTool
from .tools.file_tool import FileTool

from .flows.auto_flow import AutoFlow
from .flows.discovery_flow import DiscoveryFlow
from .flows.build_flow import BuildFlow
from .flows.debate_flow import DebateFlow


class Phase(Enum):
    """MDAN development phases."""

    LOAD = "LOAD"
    DISCOVER = "DISCOVER"
    PLAN = "PLAN"
    ARCHITECT = "ARCHITECT"
    IMPLEMENT = "IMPLEMENT"
    TEST = "TEST"
    DEPLOY = "DEPLOY"
    DOC = "DOC"


class CrewAIOrchestrator:
    """Main CrewAI orchestrator for MDAN.

    Provides intelligent task routing, agent selection, and auto-mode management.
    """

    def __init__(
        self,
        project_path: str,
        llm=None,
        sql_config: Optional[Dict[str, Any]] = None,
        serper_api_key: Optional[str] = None,
        auto_mode: bool = False,
    ):
        """Initialize CrewAI Orchestrator.

        Args:
            project_path: Path to the project directory
            llm: Language model instance
            sql_config: SQL database configuration
            serper_api_key: Serper API key for web search
            auto_mode: Enable autonomous mode
        """
        self.project_path = Path(project_path)
        self.llm = llm
        self.auto_mode = auto_mode

        # Initialize tools
        self.sql_tool = SQLTool(**sql_config) if sql_config else None
        self.serper_tool = (
            SerperTool(api_key=serper_api_key) if serper_api_key else None
        )
        self.file_tool = FileTool(base_path=project_path)

        # Initialize agents
        self.agents = self._initialize_agents()

        # Initialize flows
        self.flows = self._initialize_flows()

        # Orchestrator state
        self.state = {
            "current_phase": None,
            "active_agents": [],
            "task_history": [],
            "auto_mode_enabled": auto_mode,
        }

    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all CrewAI agents.

        Returns:
            Dictionary of agent instances
        """
        return {
            "product": ProductAgent(
                sql_tool=self.sql_tool,
                serper_tool=self.serper_tool,
                file_tool=self.file_tool,
                llm=self.llm,
            ),
            "architect": ArchitectAgent(
                sql_tool=self.sql_tool,
                serper_tool=self.serper_tool,
                file_tool=self.file_tool,
                llm=self.llm,
            ),
            "ux": UXAgent(
                sql_tool=self.sql_tool,
                serper_tool=self.serper_tool,
                file_tool=self.file_tool,
                llm=self.llm,
            ),
            "dev": DevAgent(
                sql_tool=self.sql_tool,
                serper_tool=self.serper_tool,
                file_tool=self.file_tool,
                llm=self.llm,
            ),
            "test": TestAgent(
                sql_tool=self.sql_tool,
                serper_tool=self.serper_tool,
                file_tool=self.file_tool,
                llm=self.llm,
            ),
            "security": SecurityAgent(
                sql_tool=self.sql_tool,
                serper_tool=self.serper_tool,
                file_tool=self.file_tool,
                llm=self.llm,
            ),
            "devops": DevOpsAgent(
                sql_tool=self.sql_tool,
                serper_tool=self.serper_tool,
                file_tool=self.file_tool,
                llm=self.llm,
            ),
            "doc": DocAgent(
                sql_tool=self.sql_tool,
                serper_tool=self.serper_tool,
                file_tool=self.file_tool,
                llm=self.llm,
            ),
        }

    def _initialize_flows(self) -> Dict[str, Any]:
        """Initialize all CrewAI flows.

        Returns:
            Dictionary of flow instances
        """
        return {
            "auto": AutoFlow(
                project_path=str(self.project_path),
                llm=self.llm,
                sql_config=self.sql_tool.config if self.sql_tool else None,
                serper_api_key=os.getenv("SERPER_API_KEY"),
            ),
            "discovery": DiscoveryFlow(
                project_path=str(self.project_path),
                llm=self.llm,
                sql_config=self.sql_tool.config if self.sql_tool else None,
                serper_api_key=os.getenv("SERPER_API_KEY"),
            ),
            "build": BuildFlow(
                project_path=str(self.project_path),
                llm=self.llm,
                sql_config=self.sql_tool.config if self.sql_tool else None,
                serper_api_key=os.getenv("SERPER_API_KEY"),
            ),
            "debate": DebateFlow(
                project_path=str(self.project_path),
                llm=self.llm,
                sql_config=self.sql_tool.config if self.sql_tool else None,
                serper_api_key=os.getenv("SERPER_API_KEY"),
            ),
        }

    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """Analyze task and determine appropriate agent/flow.

        Args:
            task_description: Description of the task

        Returns:
            Analysis result with recommended agent/flow
        """
        task_lower = task_description.lower()

        # Check for flow-based tasks
        if any(
            keyword in task_lower
            for keyword in ["auto", "autonomous", "full cycle", "complete"]
        ):
            return {
                "type": "flow",
                "flow": "auto",
                "reason": "Task requires autonomous full-cycle development",
            }

        if any(
            keyword in task_lower
            for keyword in ["discover", "requirement", "prd", "user story"]
        ):
            return {
                "type": "flow",
                "flow": "discovery",
                "reason": "Task requires discovery phase execution",
            }

        if any(
            keyword in task_lower
            for keyword in ["build", "implement", "develop", "code"]
        ):
            return {
                "type": "flow",
                "flow": "build",
                "reason": "Task requires build phase execution",
            }

        if any(
            keyword in task_lower
            for keyword in ["debate", "consensus", "discuss", "decide"]
        ):
            return {
                "type": "flow",
                "flow": "debate",
                "reason": "Task requires multi-agent debate",
            }

        # Check for agent-specific tasks
        if any(
            keyword in task_lower
            for keyword in ["prd", "requirement", "user story", "persona", "feature"]
        ):
            return {
                "type": "agent",
                "agent": "product",
                "reason": "Task requires product management expertise",
            }

        if any(
            keyword in task_lower
            for keyword in ["architecture", "tech stack", "design", "api", "schema"]
        ):
            return {
                "type": "agent",
                "agent": "architect",
                "reason": "Task requires architecture expertise",
            }

        if any(
            keyword in task_lower
            for keyword in ["ux", "ui", "user flow", "wireframe", "design system"]
        ):
            return {
                "type": "agent",
                "agent": "ux",
                "reason": "Task requires UX design expertise",
            }

        if any(
            keyword in task_lower
            for keyword in ["implement", "code", "refactor", "debug", "review"]
        ):
            return {
                "type": "agent",
                "agent": "dev",
                "reason": "Task requires development expertise",
            }

        if any(
            keyword in task_lower
            for keyword in ["test", "quality", "verify", "coverage"]
        ):
            return {
                "type": "agent",
                "agent": "test",
                "reason": "Task requires testing expertise",
            }

        if any(
            keyword in task_lower
            for keyword in ["security", "vulnerability", "auth", "encrypt"]
        ):
            return {
                "type": "agent",
                "agent": "security",
                "reason": "Task requires security expertise",
            }

        if any(
            keyword in task_lower
            for keyword in ["deploy", "ci/cd", "infrastructure", "cloud", "azure"]
        ):
            return {
                "type": "agent",
                "agent": "devops",
                "reason": "Task requires DevOps expertise",
            }

        if any(
            keyword in task_lower
            for keyword in ["document", "guide", "readme", "api doc"]
        ):
            return {
                "type": "agent",
                "agent": "doc",
                "reason": "Task requires documentation expertise",
            }

        # Default to product agent for general tasks
        return {
            "type": "agent",
            "agent": "product",
            "reason": "Default agent for general tasks",
        }

    async def execute_task(
        self, task_description: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a task using appropriate agent/flow.

        Args:
            task_description: Description of the task
            context: Additional context for the task

        Returns:
            Task execution result
        """
        # Analyze task
        analysis = self.analyze_task(task_description)

        # Log task
        self.state["task_history"].append(
            {
                "description": task_description,
                "analysis": analysis,
                "context": context,
                "timestamp": str(asyncio.get_event_loop().time()),
            }
        )

        # Execute based on analysis
        if analysis["type"] == "flow":
            return await self._execute_flow(analysis["flow"], task_description, context)
        else:
            return await self._execute_agent_task(
                analysis["agent"], task_description, context
            )

    async def _execute_flow(
        self,
        flow_name: str,
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute a CrewAI flow.

        Args:
            flow_name: Name of the flow to execute
            task_description: Description of the task
            context: Additional context

        Returns:
            Flow execution result
        """
        flow = self.flows.get(flow_name)
        if not flow:
            return {"status": "error", "error": f"Flow '{flow_name}' not found"}

        try:
            if flow_name == "auto":
                result = await flow.kickoff()
            elif flow_name == "discovery":
                result = await flow.kickoff(task_description)
            elif flow_name == "build":
                result = await flow.kickoff(
                    str(context) if context else task_description
                )
            elif flow_name == "debate":
                result = await flow.kickoff(task_description)
            else:
                result = await flow.kickoff()

            return {"status": "success", "flow": flow_name, "result": result}
        except Exception as e:
            return {"status": "error", "flow": flow_name, "error": str(e)}

    async def _execute_agent_task(
        self,
        agent_name: str,
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute a task with a specific agent.

        Args:
            agent_name: Name of the agent
            task_description: Description of the task
            context: Additional context

        Returns:
            Task execution result
        """
        agent_wrapper = self.agents.get(agent_name)
        if not agent_wrapper:
            return {"status": "error", "error": f"Agent '{agent_name}' not found"}

        try:
            # Create task
            task = Task(
                description=task_description,
                agent=agent_wrapper.get_agent(),
                expected_output="Task completion result",
            )

            # Execute task
            result = await asyncio.to_thread(task.execute)

            return {"status": "success", "agent": agent_name, "result": result}
        except Exception as e:
            return {"status": "error", "agent": agent_name, "error": str(e)}

    async def run_auto_mode(self, user_input: str) -> Dict[str, Any]:
        """Run autonomous mode.

        Args:
            user_input: Initial user input for the project

        Returns:
            Auto mode execution result
        """
        if not self.auto_mode:
            return {"status": "error", "error": "Auto mode is not enabled"}

        print("🚀 Starting autonomous mode...")

        try:
            # Execute auto flow
            result = await self.flows["auto"].kickoff()

            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def start_debate(self, topic: str) -> Dict[str, Any]:
        """Start a multi-agent debate.

        Args:
            topic: Topic to debate

        Returns:
            Debate result
        """
        print(f"🎯 Starting debate on: {topic}")

        try:
            result = await self.flows["debate"].kickoff(topic)

            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def create_crew(
        self,
        agent_names: List[str],
        process: Process = Process.sequential,
        verbose: bool = True,
    ) -> Crew:
        """Create a Crew with specified agents.

        Args:
            agent_names: List of agent names to include
            process: Crew process type (sequential or hierarchical)
            verbose: Enable verbose output

        Returns:
            Crew instance
        """
        agents = []
        for name in agent_names:
            agent_wrapper = self.agents.get(name)
            if agent_wrapper:
                agents.append(agent_wrapper.get_agent())

        if not agents:
            raise ValueError(f"No valid agents found in {agent_names}")

        return Crew(agents=agents, process=process, verbose=verbose)

    async def execute_crew(self, crew: Crew, tasks: List[Task]) -> Dict[str, Any]:
        """Execute a Crew with tasks.

        Args:
            crew: Crew instance
            tasks: List of tasks to execute

        Returns:
            Crew execution result
        """
        try:
            result = await asyncio.to_thread(crew.kickoff, tasks)

            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_state(self) -> Dict[str, Any]:
        """Get orchestrator state.

        Returns:
            Current orchestrator state
        """
        return self.state

    def save_state(self, filepath: str):
        """Save orchestrator state to file.

        Args:
            filepath: Path to save state
        """
        with open(filepath, "w") as f:
            json.dump(self.state, f, indent=2)

    def load_state(self, filepath: str):
        """Load orchestrator state from file.

        Args:
            filepath: Path to load state from
        """
        with open(filepath, "r") as f:
            self.state = json.load(f)

    def enable_auto_mode(self):
        """Enable autonomous mode."""
        self.auto_mode = True
        self.state["auto_mode_enabled"] = True

    def disable_auto_mode(self):
        """Disable autonomous mode."""
        self.auto_mode = False
        self.state["auto_mode_enabled"] = False

    def is_auto_mode_enabled(self) -> bool:
        """Check if auto mode is enabled.

        Returns:
            True if auto mode is enabled
        """
        return self.auto_mode
