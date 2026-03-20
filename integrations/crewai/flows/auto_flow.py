"""Auto Flow - Main autonomous flow with 8 phases

Orchestrates the complete autonomous development cycle:
LOAD → DISCOVER → PLAN → ARCHITECT → IMPLEMENT → TEST → DEPLOY → DOC
"""

from crewai.flow import Flow, listen, start
from typing import Dict, Any, Optional
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


class AutoFlow(Flow):
    """Main autonomous flow for full-cycle development."""

    def __init__(
        self,
        project_path: str,
        llm=None,
        sql_config: Optional[Dict[str, Any]] = None,
        serper_api_key: Optional[str] = None,
    ):
        """Initialize Auto Flow.

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

        # Initialize agents
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
            "current_phase": None,
            "project_context": {},
            "phase_results": {},
            "errors": [],
        }

    @start
    async def load_phase(self):
        """LOAD phase: Load project context and state."""
        self.state["current_phase"] = "LOAD"

        print("🔄 LOAD Phase: Loading project context...")

        # Load project state if exists
        state_file = self.project_path / "MDAN-STATE.json"
        if state_file.exists():
            with open(state_file, "r") as f:
                self.state["project_context"] = json.load(f)
            print("✅ Loaded existing project state")
        else:
            self.state["project_context"] = {
                "project_name": self.project_path.name,
                "phases_completed": [],
                "current_phase": "LOAD",
            }
            print("✅ Initialized new project state")

        self.state["phase_results"]["LOAD"] = {
            "status": "completed",
            "context": self.state["project_context"],
        }

        return self.state["project_context"]

    @listen(load_phase)
    async def discover_phase(self, project_context: Dict[str, Any]):
        """DISCOVER phase: Requirements gathering and PRD creation."""
        self.state["current_phase"] = "DISCOVER"

        print("🔍 DISCOVER Phase: Gathering requirements...")

        # Create DISCOVER tasks
        tasks = [
            self.product_agent.create_prd_task(str(project_context)),
            self.product_agent.create_user_stories_task(str(project_context)),
            self.product_agent.create_personas_task(str(project_context)),
            self.product_agent.create_feature_prioritization_task(str(project_context)),
        ]

        # Execute tasks
        results = []
        for task in tasks:
            try:
                result = await asyncio.to_thread(task.execute)
                results.append(result)
                print(f"✅ Completed: {task.description[:50]}...")
            except Exception as e:
                self.state["errors"].append(f"DISCOVER error: {str(e)}")
                print(f"❌ Error in task: {str(e)}")

        self.state["phase_results"]["DISCOVER"] = {
            "status": "completed",
            "results": results,
        }

        return results

    @listen(discover_phase)
    async def plan_phase(self, discover_results: list):
        """PLAN phase: Project planning and task breakdown."""
        self.state["current_phase"] = "PLAN"

        print("📋 PLAN Phase: Creating project plan...")

        # Create planning tasks
        tasks = [
            self.product_agent.create_acceptance_criteria_task(str(discover_results)),
            self.product_agent.create_project_timeline_task(str(discover_results)),
        ]

        # Execute tasks
        results = []
        for task in tasks:
            try:
                result = await asyncio.to_thread(task.execute)
                results.append(result)
                print(f"✅ Completed: {task.description[:50]}...")
            except Exception as e:
                self.state["errors"].append(f"PLAN error: {str(e)}")
                print(f"❌ Error in task: {str(e)}")

        self.state["phase_results"]["PLAN"] = {
            "status": "completed",
            "results": results,
        }

        return results

    @listen(plan_phase)
    async def architect_phase(self, plan_results: list):
        """ARCHITECT phase: System architecture and design."""
        self.state["current_phase"] = "ARCHITECT"

        print("🏗️ ARCHITECT Phase: Designing system architecture...")

        # Create architecture tasks
        tasks = [
            self.architect_agent.create_architecture_task(str(plan_results)),
            self.architect_agent.create_tech_stack_task(str(plan_results)),
            self.architect_agent.create_adr_task(str(plan_results)),
            self.architect_agent.create_api_design_task(str(plan_results)),
            self.architect_agent.create_database_schema_task(str(plan_results)),
        ]

        # Execute tasks
        results = []
        for task in tasks:
            try:
                result = await asyncio.to_thread(task.execute)
                results.append(result)
                print(f"✅ Completed: {task.description[:50]}...")
            except Exception as e:
                self.state["errors"].append(f"ARCHITECT error: {str(e)}")
                print(f"❌ Error in task: {str(e)}")

        self.state["phase_results"]["ARCHITECT"] = {
            "status": "completed",
            "results": results,
        }

        return results

    @listen(architect_phase)
    async def implement_phase(self, architect_results: list):
        """IMPLEMENT phase: Code implementation."""
        self.state["current_phase"] = "IMPLEMENT"

        print("💻 IMPLEMENT Phase: Implementing features...")

        # Create implementation tasks
        tasks = [
            self.dev_agent.create_implementation_task(str(architect_results)),
            self.dev_agent.create_refactoring_task(str(architect_results)),
            self.dev_agent.create_code_review_task(str(architect_results)),
            self.dev_agent.create_testing_task(str(architect_results)),
            self.dev_agent.create_debugging_task(str(architect_results)),
        ]

        # Execute tasks
        results = []
        for task in tasks:
            try:
                result = await asyncio.to_thread(task.execute)
                results.append(result)
                print(f"✅ Completed: {task.description[:50]}...")
            except Exception as e:
                self.state["errors"].append(f"IMPLEMENT error: {str(e)}")
                print(f"❌ Error in task: {str(e)}")

        self.state["phase_results"]["IMPLEMENT"] = {
            "status": "completed",
            "results": results,
        }

        return results

    @listen(implement_phase)
    async def test_phase(self, implement_results: list):
        """TEST phase: Testing and quality assurance."""
        self.state["current_phase"] = "TEST"

        print("🧪 TEST Phase: Running tests...")

        # Create testing tasks
        tasks = [
            self.test_agent.create_test_strategy_task(str(implement_results)),
            self.test_agent.create_unit_tests_task(str(implement_results)),
            self.test_agent.create_integration_tests_task(str(implement_results)),
            self.test_agent.create_e2e_tests_task(str(implement_results)),
            self.test_agent.create_test_execution_task(str(implement_results)),
        ]

        # Execute tasks
        results = []
        for task in tasks:
            try:
                result = await asyncio.to_thread(task.execute)
                results.append(result)
                print(f"✅ Completed: {task.description[:50]}...")
            except Exception as e:
                self.state["errors"].append(f"TEST error: {str(e)}")
                print(f"❌ Error in task: {str(e)}")

        self.state["phase_results"]["TEST"] = {
            "status": "completed",
            "results": results,
        }

        return results

    @listen(test_phase)
    async def deploy_phase(self, test_results: list):
        """DEPLOY phase: Deployment and infrastructure setup."""
        self.state["current_phase"] = "DEPLOY"

        print("🚀 DEPLOY Phase: Setting up deployment...")

        # Create deployment tasks
        tasks = [
            self.devops_agent.create_ci_cd_pipeline_task(str(test_results)),
            self.devops_agent.create_docker_setup_task(str(test_results)),
            self.devops_agent.create_azure_deployment_task(str(test_results)),
            self.devops_agent.create_monitoring_setup_task(str(test_results)),
            self.devops_agent.create_deployment_strategy_task(str(test_results)),
        ]

        # Execute tasks
        results = []
        for task in tasks:
            try:
                result = await asyncio.to_thread(task.execute)
                results.append(result)
                print(f"✅ Completed: {task.description[:50]}...")
            except Exception as e:
                self.state["errors"].append(f"DEPLOY error: {str(e)}")
                print(f"❌ Error in task: {str(e)}")

        self.state["phase_results"]["DEPLOY"] = {
            "status": "completed",
            "results": results,
        }

        return results

    @listen(deploy_phase)
    async def doc_phase(self, deploy_results: list):
        """DOC phase: Documentation creation."""
        self.state["current_phase"] = "DOC"

        print("📚 DOC Phase: Creating documentation...")

        # Create documentation tasks
        tasks = [
            self.doc_agent.create_readme_task(str(deploy_results)),
            self.doc_agent.create_api_documentation_task(str(deploy_results)),
            self.doc_agent.create_user_guide_task(str(deploy_results)),
            self.doc_agent.create_developer_guide_task(str(deploy_results)),
            self.doc_agent.create_architecture_documentation_task(str(deploy_results)),
        ]

        # Execute tasks
        results = []
        for task in tasks:
            try:
                result = await asyncio.to_thread(task.execute)
                results.append(result)
                print(f"✅ Completed: {task.description[:50]}...")
            except Exception as e:
                self.state["errors"].append(f"DOC error: {str(e)}")
                print(f"❌ Error in task: {str(e)}")

        self.state["phase_results"]["DOC"] = {"status": "completed", "results": results}

        return results

    @listen(doc_phase)
    async def finalize(self, doc_results: list):
        """Finalize the autonomous flow."""
        print("✨ Autonomous flow completed!")

        # Update project state
        self.state["project_context"]["phases_completed"] = [
            "LOAD",
            "DISCOVER",
            "PLAN",
            "ARCHITECT",
            "IMPLEMENT",
            "TEST",
            "DEPLOY",
            "DOC",
        ]
        self.state["project_context"]["current_phase"] = "COMPLETED"

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
            "phases": self.state["phase_results"],
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
    def load_context(cls, filepath: str, llm=None) -> "AutoFlow":
        """Load flow context from file.

        Args:
            filepath: Path to load context from
            llm: Language model instance

        Returns:
            AutoFlow instance with loaded context
        """
        with open(filepath, "r") as f:
            context = json.load(f)

        flow = cls(project_path=context["project_path"], llm=llm)
        flow.state = context["state"]

        return flow
