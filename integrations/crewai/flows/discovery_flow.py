"""Discovery Flow - DISCOVER phase flow

Orchestrates the DISCOVER phase: requirements gathering, PRD creation, user stories, personas.
"""

from crewai.flow import Flow, listen, start
from typing import Dict, Any, Optional
import asyncio
import json
from pathlib import Path

from ..agents.product_agent import ProductAgent

from ..tools.sql_tool import SQLTool
from ..tools.serper_tool import SerperTool
from ..tools.file_tool import FileTool


class DiscoveryFlow(Flow):
    """DISCOVER phase flow for requirements gathering."""

    def __init__(
        self,
        project_path: str,
        llm=None,
        sql_config: Optional[Dict[str, Any]] = None,
        serper_api_key: Optional[str] = None,
    ):
        """Initialize Discovery Flow.

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

        # Initialize agent
        self.product_agent = ProductAgent(
            sql_tool=self.sql_tool,
            serper_tool=self.serper_tool,
            file_tool=self.file_tool,
            llm=llm,
        )

        # Flow state
        self.state = {
            "current_step": None,
            "project_context": {},
            "step_results": {},
            "errors": [],
        }

    @start
    async def load_context(self, user_input: str):
        """Load project context and user input."""
        self.state["current_step"] = "load_context"

        print("📂 Loading project context...")

        # Load project state if exists
        state_file = self.project_path / "MDAN-STATE.json"
        if state_file.exists():
            with open(state_file, "r") as f:
                self.state["project_context"] = json.load(f)
        else:
            self.state["project_context"] = {
                "project_name": self.project_path.name,
                "user_input": user_input,
            }

        self.state["step_results"]["load_context"] = {
            "status": "completed",
            "context": self.state["project_context"],
        }

        return self.state["project_context"]

    @listen(load_context)
    async def create_prd(self, context: Dict[str, Any]):
        """Create Product Requirements Document."""
        self.state["current_step"] = "create_prd"

        print("📝 Creating Product Requirements Document...")

        task = self.product_agent.create_prd_task(str(context))

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["create_prd"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ PRD created successfully")
            return result
        except Exception as e:
            self.state["errors"].append(f"PRD creation error: {str(e)}")
            print(f"❌ Error creating PRD: {str(e)}")
            return None

    @listen(create_prd)
    async def create_user_stories(self, prd_result: Any):
        """Create user stories."""
        self.state["current_step"] = "create_user_stories"

        print("📋 Creating user stories...")

        task = self.product_agent.create_user_stories_task(str(prd_result))

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["create_user_stories"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ User stories created successfully")
            return result
        except Exception as e:
            self.state["errors"].append(f"User stories creation error: {str(e)}")
            print(f"❌ Error creating user stories: {str(e)}")
            return None

    @listen(create_user_stories)
    async def create_personas(self, user_stories_result: Any):
        """Create user personas."""
        self.state["current_step"] = "create_personas"

        print("👥 Creating user personas...")

        task = self.product_agent.create_personas_task(str(user_stories_result))

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["create_personas"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ User personas created successfully")
            return result
        except Exception as e:
            self.state["errors"].append(f"Personas creation error: {str(e)}")
            print(f"❌ Error creating personas: {str(e)}")
            return None

    @listen(create_personas)
    async def prioritize_features(self, personas_result: Any):
        """Prioritize features."""
        self.state["current_step"] = "prioritize_features"

        print("🎯 Prioritizing features...")

        task = self.product_agent.create_feature_prioritization_task(
            str(personas_result)
        )

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["prioritize_features"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ Features prioritized successfully")
            return result
        except Exception as e:
            self.state["errors"].append(f"Feature prioritization error: {str(e)}")
            print(f"❌ Error prioritizing features: {str(e)}")
            return None

    @listen(prioritize_features)
    async def create_acceptance_criteria(self, features_result: Any):
        """Create acceptance criteria."""
        self.state["current_step"] = "create_acceptance_criteria"

        print("✅ Creating acceptance criteria...")

        task = self.product_agent.create_acceptance_criteria_task(str(features_result))

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["create_acceptance_criteria"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ Acceptance criteria created successfully")
            return result
        except Exception as e:
            self.state["errors"].append(f"Acceptance criteria creation error: {str(e)}")
            print(f"❌ Error creating acceptance criteria: {str(e)}")
            return None

    @listen(create_acceptance_criteria)
    async def finalize_discovery(self, acceptance_criteria_result: Any):
        """Finalize DISCOVER phase."""
        print("✨ DISCOVER phase completed!")

        # Update project state
        self.state["project_context"]["phases_completed"] = self.state[
            "project_context"
        ].get("phases_completed", [])
        if "DISCOVER" not in self.state["project_context"]["phases_completed"]:
            self.state["project_context"]["phases_completed"].append("DISCOVER")
        self.state["project_context"]["current_phase"] = "DISCOVER_COMPLETED"

        # Save state
        state_file = self.project_path / "MDAN-STATE.json"
        with open(state_file, "w") as f:
            json.dump(self.state["project_context"], f, indent=2)

        print(f"✅ Project state saved to {state_file}")

        if self.state["errors"]:
            print(f"\n⚠️ Errors encountered: {len(self.state['errors'])}")
            for error in self.state["errors"]:
                print(f"  - {error}")

        return {
            "status": "completed",
            "steps": self.state["step_results"],
            "errors": self.state["errors"],
        }

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
    def load_context(cls, filepath: str, llm=None) -> "DiscoveryFlow":
        """Load flow context from file.

        Args:
            filepath: Path to load context from
            llm: Language model instance

        Returns:
            DiscoveryFlow instance with loaded context
        """
        with open(filepath, "r") as f:
            context = json.load(f)

        flow = cls(project_path=context["project_path"], llm=llm)
        flow.state = context["state"]

        return flow
