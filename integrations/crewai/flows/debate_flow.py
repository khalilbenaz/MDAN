"""Debate Flow - Multi-agent debate flow

Orchestrates debates between multiple agents to reach consensus on complex decisions.
"""

from crewai.flow import Flow, listen, start
from typing import Dict, Any, Optional, List
import asyncio
import json
from pathlib import Path

from ..agents.product_agent import ProductAgent
from ..agents.architect_agent import ArchitectAgent
from ..agents.ux_agent import UXAgent
from ..agents.dev_agent import DevAgent
from ..agents.test_agent import TestAgent
from ..agents.security_agent import SecurityAgent
from ..agents.devops_agent import DevOpsAgent
from ..agents.doc_agent import DocAgent

from ..tools.sql_tool import SQLTool
from ..tools.serper_tool import SerperTool
from ..tools.file_tool import FileTool


class DebateFlow(Flow):
    """Multi-agent debate flow for reaching consensus on complex decisions."""

    def __init__(
        self,
        project_path: str,
        llm=None,
        sql_config: Optional[Dict[str, Any]] = None,
        serper_api_key: Optional[str] = None,
    ):
        """Initialize Debate Flow.

        Args:
            project_path: Path to the project directory
            llm: Language model instance
            sql_config: SQL database configuration
            serper_api_key: Serper API key for web search
        """
        super().__init__()
        self.project_path = Path(project_path)
        self.llm = llm

        # Initialize tools
        self.sql_tool = SQLTool(**sql_config) if sql_config else None
        self.serper_tool = (
            SerperTool(api_key=serper_api_key) if serper_api_key else None
        )
        self.file_tool = FileTool(base_path=project_path)

        # Initialize all agents
        self.product_agent = ProductAgent(
            sql_tool=self.sql_tool,
            serper_tool=self.serper_tool,
            file_tool=self.file_tool,
            llm=llm,
        )

        self.architect_agent = ArchitectAgent(
            sql_tool=self.sql_tool,
            serper_tool=self.serper_tool,
            file_tool=self.file_tool,
            llm=llm,
        )

        self.ux_agent = UXAgent(
            sql_tool=self.sql_tool,
            serper_tool=self.serper_tool,
            file_tool=self.file_tool,
            llm=llm,
        )

        self.dev_agent = DevAgent(
            sql_tool=self.sql_tool,
            serper_tool=self.serper_tool,
            file_tool=self.file_tool,
            llm=llm,
        )

        self.test_agent = TestAgent(
            sql_tool=self.sql_tool,
            serper_tool=self.serper_tool,
            file_tool=self.file_tool,
            llm=llm,
        )

        self.security_agent = SecurityAgent(
            sql_tool=self.sql_tool,
            serper_tool=self.serper_tool,
            file_tool=self.file_tool,
            llm=llm,
        )

        self.devops_agent = DevOpsAgent(
            sql_tool=self.sql_tool,
            serper_tool=self.serper_tool,
            file_tool=self.file_tool,
            llm=llm,
        )

        self.doc_agent = DocAgent(
            sql_tool=self.sql_tool,
            serper_tool=self.serper_tool,
            file_tool=self.file_tool,
            llm=llm,
        )

        # Flow state
        self.state = {
            "current_round": 0,
            "max_rounds": 3,
            "topic": None,
            "arguments": [],
            "consensus": None,
            "errors": [],
        }

    @start
    async def initialize_debate(self, topic: str):
        """Initialize debate with topic and context."""
        self.state["topic"] = topic
        self.state["current_round"] = 1

        print(f"🎯 Initializing debate on topic: {topic}")
        print(f"📊 Max rounds: {self.state['max_rounds']}")

        return topic

    @listen(initialize_debate)
    async def round1_initial_positions(self, topic: str):
        """Round 1: Agents present initial positions."""
        print(f"\n🗣️ Round 1: Initial positions")

        # Select relevant agents based on topic
        agents = self._select_agents_for_topic(topic)

        arguments = []
        for agent_name, agent in agents.items():
            try:
                # Create a debate task for each agent
                from crewai import Task

                task = Task(
                    description=f"""Present your initial position on the following topic:

                    Topic: {topic}

                    Your task:
                    1. Analyze the topic from your perspective
                    2. Present your initial position
                    3. Provide supporting arguments
                    4. Identify potential concerns

                    Be concise but thorough in your response.
                    """,
                    agent=agent.get_agent(),
                    expected_output="Initial position with supporting arguments",
                )

                result = await asyncio.to_thread(task.execute)
                arguments.append({"round": 1, "agent": agent_name, "position": result})
                print(f"  ✅ {agent_name}: Position presented")
            except Exception as e:
                self.state["errors"].append(f"{agent_name} error: {str(e)}")
                print(f"  ❌ {agent_name}: Error - {str(e)}")

        self.state["arguments"].extend(arguments)
        return arguments

    @listen(round1_initial_positions)
    async def round2_counterarguments(self, round1_args: List[Dict]):
        """Round 2: Agents present counterarguments."""
        self.state["current_round"] = 2
        print(f"\n🔄 Round 2: Counterarguments")

        # Select relevant agents
        agents = self._select_agents_for_topic(self.state["topic"])

        # Create summary of round 1 for context
        round1_summary = "\n".join(
            [f"{arg['agent']}: {arg['position'][:200]}..." for arg in round1_args]
        )

        arguments = []
        for agent_name, agent in agents.items():
            try:
                from crewai import Task

                task = Task(
                    description=f"""Present counterarguments to the following positions:

                    Topic: {self.state["topic"]}

                    Previous positions:
                    {round1_summary}

                    Your task:
                    1. Review other agents' positions
                    2. Present counterarguments where you disagree
                    3. Acknowledge valid points from others
                    4. Refine your position based on new insights

                    Be constructive and respectful in your counterarguments.
                    """,
                    agent=agent.get_agent(),
                    expected_output="Counterarguments with refined position",
                )

                result = await asyncio.to_thread(task.execute)
                arguments.append({"round": 2, "agent": agent_name, "position": result})
                print(f"  ✅ {agent_name}: Counterarguments presented")
            except Exception as e:
                self.state["errors"].append(f"{agent_name} error: {str(e)}")
                print(f"  ❌ {agent_name}: Error - {str(e)}")

        self.state["arguments"].extend(arguments)
        return arguments

    @listen(round2_counterarguments)
    async def round3_consensus_building(self, round2_args: List[Dict]):
        """Round 3: Build consensus."""
        self.state["current_round"] = 3
        print(f"\n🤝 Round 3: Consensus building")

        # Select relevant agents
        agents = self._select_agents_for_topic(self.state["topic"])

        # Create summary of all previous rounds
        all_args_summary = "\n".join(
            [
                f"Round {arg['round']} - {arg['agent']}: {arg['position'][:200]}..."
                for arg in self.state["arguments"]
            ]
        )

        arguments = []
        for agent_name, agent in agents.items():
            try:
                from crewai import Task

                task = Task(
                    description=f"""Work towards consensus on the following topic:

                    Topic: {self.state["topic"]}

                    All previous arguments:
                    {all_args_summary}

                    Your task:
                    1. Review all arguments from previous rounds
                    2. Identify areas of agreement
                    3. Propose compromises where there's disagreement
                    4. Suggest a consensus position
                    5. Highlight any remaining concerns

                    Focus on finding common ground and practical solutions.
                    """,
                    agent=agent.get_agent(),
                    expected_output="Consensus proposal with compromises",
                )

                result = await asyncio.to_thread(task.execute)
                arguments.append({"round": 3, "agent": agent_name, "position": result})
                print(f"  ✅ {agent_name}: Consensus proposal presented")
            except Exception as e:
                self.state["errors"].append(f"{agent_name} error: {str(e)}")
                print(f"  ❌ {agent_name}: Error - {str(e)}")

        self.state["arguments"].extend(arguments)
        return arguments

    @listen(round3_consensus_building)
    async def finalize_consensus(self, round3_args: List[Dict]):
        """Finalize consensus and generate summary."""
        print(f"\n✨ Finalizing consensus...")

        # Use Product Agent to synthesize final consensus
        try:
            from crewai import Task

            task = Task(
                description=f"""Synthesize the final consensus from all debate rounds.

                Topic: {self.state["topic"]}

                All arguments:
                {json.dumps(self.state["arguments"], indent=2)}

                Your task:
                1. Analyze all arguments from all rounds
                2. Identify the consensus position
                3. Document areas of agreement
                4. Document areas of disagreement
                5. Provide final recommendation
                6. List any action items or next steps

                Generate a comprehensive consensus report.
                """,
                agent=self.product_agent.get_agent(),
                expected_output="Comprehensive consensus report",
            )

            consensus = await asyncio.to_thread(task.execute)
            self.state["consensus"] = consensus

            print("✅ Consensus reached!")
            print(f"\n📋 Consensus Summary:\n{consensus[:500]}...")

        except Exception as e:
            self.state["errors"].append(f"Consensus synthesis error: {str(e)}")
            print(f"❌ Error synthesizing consensus: {str(e)}")
            self.state["consensus"] = "Unable to reach consensus due to errors"

        # Save debate results
        debate_file = self.project_path / "debate_results.json"
        with open(debate_file, "w") as f:
            json.dump(self.state, f, indent=2)

        print(f"\n💾 Debate results saved to {debate_file}")

        if self.state["errors"]:
            print(f"\n⚠️ Errors encountered: {len(self.state['errors'])}")
            for error in self.state["errors"]:
                print(f"  - {error}")

        return {
            "topic": self.state["topic"],
            "consensus": self.state["consensus"],
            "arguments": self.state["arguments"],
            "errors": self.state["errors"],
        }

    def _select_agents_for_topic(self, topic: str) -> Dict[str, Any]:
        """Select relevant agents based on topic keywords.

        Args:
            topic: Debate topic

        Returns:
            Dictionary of relevant agents
        """
        topic_lower = topic.lower()

        # Default agents for most topics
        agents = {
            "product": self.product_agent,
            "architect": self.architect_agent,
            "dev": self.dev_agent,
        }

        # Add agents based on topic keywords
        if any(
            keyword in topic_lower
            for keyword in ["user", "ux", "ui", "design", "interface"]
        ):
            agents["ux"] = self.ux_agent

        if any(
            keyword in topic_lower for keyword in ["test", "quality", "verify", "bug"]
        ):
            agents["test"] = self.test_agent

        if any(
            keyword in topic_lower
            for keyword in ["security", "vulnerability", "auth", "encrypt"]
        ):
            agents["security"] = self.security_agent

        if any(
            keyword in topic_lower
            for keyword in ["deploy", "ci/cd", "infrastructure", "cloud", "azure"]
        ):
            agents["devops"] = self.devops_agent

        if any(
            keyword in topic_lower
            for keyword in ["document", "guide", "readme", "api doc"]
        ):
            agents["doc"] = self.doc_agent

        return agents

    def get_state(self) -> Dict[str, Any]:
        """Get current flow state.

        Returns:
            Current flow state
        """
        return self.state

    def save_context(self, filepath: str):
        """Save flow context to file.

        Args:
            filepath: Path to save context
        """
        context = {"state": self.state, "project_path": str(self.project_path)}
        with open(filepath, "w") as f:
            json.dump(context, f, indent=2)

    @classmethod
    def load_context(cls, filepath: str, llm=None) -> "DebateFlow":
        """Load flow context from file.

        Args:
            filepath: Path to load context from
            llm: Language model instance

        Returns:
            DebateFlow instance with loaded context
        """
        with open(filepath, "r") as f:
            context = json.load(f)

        flow = cls(project_path=context["project_path"], llm=llm)
        flow.state = context["state"]

        return flow
