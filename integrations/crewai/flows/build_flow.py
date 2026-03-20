"""Build Flow - BUILD phase flow

Orchestrates the BUILD phase: implementation, refactoring, code review, testing, debugging.
"""

from crewai.flow import Flow, listen, start
from typing import Dict, Any, Optional
import asyncio
import json
from pathlib import Path

from ..agents.dev_agent import DevAgent
from ..agents.security_agent import SecurityAgent

from ..tools.sql_tool import SQLTool
from ..tools.serper_tool import SerperTool
from ..tools.file_tool import FileTool


class BuildFlow(Flow):
    """BUILD phase flow for implementation and development."""

    def __init__(
        self,
        project_path: str,
        llm=None,
        sql_config: Optional[Dict[str, Any]] = None,
        serper_api_key: Optional[str] = None,
    ):
        """Initialize Build Flow.

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
        self.dev_agent = DevAgent(
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

        # Flow state
        self.state = {
            "current_step": None,
            "project_context": {},
            "step_results": {},
            "errors": [],
        }

    @start
    async def load_context(self, design_context: str):
        """Load design context and architecture."""
        self.state["current_step"] = "load_context"

        print("📂 Loading design context...")

        # Load project state if exists
        state_file = self.project_path / "MDAN-STATE.json"
        if state_file.exists():
            with open(state_file, "r") as f:
                self.state["project_context"] = json.load(f)
        else:
            self.state["project_context"] = {
                "project_name": self.project_path.name,
                "design_context": design_context,
            }

        self.state["step_results"]["load_context"] = {
            "status": "completed",
            "context": self.state["project_context"],
        }

        return self.state["project_context"]

    @listen(load_context)
    async def implement_features(self, context: Dict[str, Any]):
        """Implement features based on design."""
        self.state["current_step"] = "implement_features"

        print("💻 Implementing features...")

        task = self.dev_agent.create_implementation_task(str(context))

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["implement_features"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ Features implemented successfully")
            return result
        except Exception as e:
            self.state["errors"].append(f"Implementation error: {str(e)}")
            print(f"❌ Error implementing features: {str(e)}")
            return None

    @listen(implement_features)
    async def security_review(self, implementation_result: Any):
        """Conduct security review of implementation."""
        self.state["current_step"] = "security_review"

        print("🔒 Conducting security review...")

        task = self.security_agent.create_security_review_task(
            str(implementation_result)
        )

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["security_review"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ Security review completed")
            return result
        except Exception as e:
            self.state["errors"].append(f"Security review error: {str(e)}")
            print(f"❌ Error in security review: {str(e)}")
            return None

    @listen(security_review)
    async def refactor_code(self, security_result: Any):
        """Refactor code based on feedback."""
        self.state["current_step"] = "refactor_code"

        print("🔧 Refactoring code...")

        task = self.dev_agent.create_refactoring_task(str(security_result))

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["refactor_code"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ Code refactored successfully")
            return result
        except Exception as e:
            self.state["errors"].append(f"Refactoring error: {str(e)}")
            print(f"❌ Error refactoring code: {str(e)}")
            return None

    @listen(refactor_code)
    async def code_review(self, refactor_result: Any):
        """Conduct code review."""
        self.state["current_step"] = "code_review"

        print("👀 Conducting code review...")

        task = self.dev_agent.create_code_review_task(str(refactor_result))

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["code_review"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ Code review completed")
            return result
        except Exception as e:
            self.state["errors"].append(f"Code review error: {str(e)}")
            print(f"❌ Error in code review: {str(e)}")
            return None

    @listen(code_review)
    async def write_tests(self, review_result: Any):
        """Write tests for the implementation."""
        self.state["current_step"] = "write_tests"

        print("🧪 Writing tests...")

        task = self.dev_agent.create_testing_task(str(review_result))

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["write_tests"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ Tests written successfully")
            return result
        except Exception as e:
            self.state["errors"].append(f"Test writing error: {str(e)}")
            print(f"❌ Error writing tests: {str(e)}")
            return None

    @listen(write_tests)
    async def debug_issues(self, test_result: Any):
        """Debug any issues found."""
        self.state["current_step"] = "debug_issues"

        print("🐛 Debugging issues...")

        task = self.dev_agent.create_debugging_task(str(test_result))

        try:
            result = await asyncio.to_thread(task.execute)
            self.state["step_results"]["debug_issues"] = {
                "status": "completed",
                "result": result,
            }
            print("✅ Debugging completed")
            return result
        except Exception as e:
            self.state["errors"].append(f"Debugging error: {str(e)}")
            print(f"❌ Error debugging: {str(e)}")
            return None

    @listen(debug_issues)
    async def finalize_build(self, debug_result: Any):
        """Finalize BUILD phase."""
        print("✨ BUILD phase completed!")

        # Update project state
        self.state["project_context"]["phases_completed"] = self.state[
            "project_context"
        ].get("phases_completed", [])
        if "BUILD" not in self.state["project_context"]["phases_completed"]:
            self.state["project_context"]["phases_completed"].append("BUILD")
        self.state["project_context"]["current_phase"] = "BUILD_COMPLETED"

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
    def load_context(cls, filepath: str, llm=None) -> "BuildFlow":
        """Load flow context from file.

        Args:
            filepath: Path to load context from
            llm: Language model instance

        Returns:
            BuildFlow instance with loaded context
        """
        with open(filepath, "r") as f:
            context = json.load(f)

        flow = cls(project_path=context["project_path"], llm=llm)
        flow.state = context["state"]

        return flow
