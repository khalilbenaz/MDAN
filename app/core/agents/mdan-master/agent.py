"""
MDAN Master Agent

The primary execution engine for MDAN operations, serving as a master task executor,
knowledge custodian, and workflow orchestrator.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import asyncio


@dataclass
class AgentRequest:
    """Request data structure for the MDAN Master agent."""

    action: str
    context: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None


class MDANMasterAgent:
    """
    MDAN Master Executor, Knowledge Custodian, and Workflow Orchestrator.

    Master-level expert in the MDAN Core Platform and all loaded modules with
    comprehensive knowledge of all resources, tasks, and workflows. Experienced
    in direct task execution and runtime resource management, serving as the
    primary execution engine for MDAN operations.
    """

    def __init__(self):
        """Initialize the MDAN Master agent."""
        self.name = "MDAN Master"
        self.title = (
            "MDAN Master Executor, Knowledge Custodian, and Workflow Orchestrator"
        )
        self.icon = "🧙"
        self.capabilities = [
            "runtime resource management",
            "workflow orchestration",
            "task execution",
            "knowledge custodian",
        ]
        self.role = (
            "Master Task Executor + MDAN Expert + Guiding Facilitator Orchestrator"
        )
        self.identity = (
            "Master-level expert in the MDAN Core Platform and all loaded modules "
            "with comprehensive knowledge of all resources, tasks, and workflows. "
            "Experienced in direct task execution and runtime resource management, "
            "serving as the primary execution engine for MDAN operations."
        )
        self.communication_style = (
            "Direct and comprehensive, refers to himself in the 3rd person. "
            "Expert-level communication focused on efficient task execution, "
            "presenting information systematically using numbered lists with "
            "immediate command response capability."
        )
        self.principles = [
            "Load resources at runtime, never pre-load",
            "Always present numbered lists for choices",
        ]

    async def process(self, request: AgentRequest) -> Dict[str, Any]:
        """
        Process the request and return a response.

        Args:
            request: The request to process

        Returns:
            A dictionary containing the response
        """
        action = request.action.lower()

        if action == "greet":
            return await self._greet(request)
        elif action == "list-tasks":
            return await self._list_tasks(request)
        elif action == "list-workflows":
            return await self._list_workflows(request)
        elif action == "help":
            return await self._help(request)
        else:
            return await self._handle_unknown_action(request)

    async def _greet(self, request: AgentRequest) -> Dict[str, Any]:
        """
        Greet the user and provide initial guidance.

        Args:
            request: The request to process

        Returns:
            A greeting message with menu options
        """
        user_name = (
            request.context.get("user_name", "User") if request.context else "User"
        )
        communication_language = (
            request.context.get("communication_language", "English")
            if request.context
            else "English"
        )

        greeting = {
            "message": f"Welcome {user_name}! MDAN Master is ready to assist you.",
            "agent": self.name,
            "icon": self.icon,
            "capabilities": self.capabilities,
            "menu": [
                {
                    "trigger": "MH or fuzzy match on menu or help",
                    "description": "[MH] Redisplay Menu Help",
                },
                {
                    "trigger": "CH or fuzzy match on chat",
                    "description": "[CH] Chat with the Agent about anything",
                },
                {
                    "trigger": "LT or fuzzy match on list-tasks",
                    "description": "[LT] List Available Tasks",
                },
                {
                    "trigger": "LW or fuzzy match on list-workflows",
                    "description": "[LW] List Workflows",
                },
                {
                    "trigger": "PM or fuzzy match on party-mode",
                    "description": "[PM] Start Party Mode",
                },
                {
                    "trigger": "DA or fuzzy match on exit, leave, goodbye",
                    "description": "[DA] Dismiss Agent",
                },
            ],
            "help_hint": (
                f"You can type `/mmm-help` at any time to get advice on what to do next. "
                f"You can combine that with what you need help with, "
                f"for example: `/mmm-help where should I start with an idea I have that does XYZ`"
            ),
            "language": communication_language,
        }

        return greeting

    async def _list_tasks(self, request: AgentRequest) -> Dict[str, Any]:
        """
        List available tasks.

        Args:
            request: The request to process

        Returns:
            A list of available tasks
        """
        # This would typically load from a task manifest
        # For now, return a placeholder
        tasks = [
            {
                "id": "task-1",
                "name": "Create Product Brief",
                "description": "Create a product brief through collaborative discovery",
                "module": "mmm",
            },
            {
                "id": "task-2",
                "name": "Create PRD",
                "description": "Create a PRD from scratch",
                "module": "mmm",
            },
            {
                "id": "task-3",
                "name": "Create Architecture",
                "description": "Create architecture solution design decisions",
                "module": "mmm",
            },
        ]

        return {"message": "Available Tasks", "tasks": tasks, "count": len(tasks)}

    async def _list_workflows(self, request: AgentRequest) -> Dict[str, Any]:
        """
        List available workflows.

        Args:
            request: The request to process

        Returns:
            A list of available workflows
        """
        # This would typically load from a workflow manifest
        # For now, return a placeholder
        workflows = [
            {
                "id": "workflow-1",
                "name": "brainstorming",
                "description": "Facilitate interactive brainstorming sessions",
                "module": "core",
            },
            {
                "id": "workflow-2",
                "name": "party-mode",
                "description": "Orchestrates group discussions between all installed MDAN agents",
                "module": "core",
            },
            {
                "id": "workflow-3",
                "name": "create-product-brief",
                "description": "Create product brief through collaborative discovery",
                "module": "mmm",
            },
            {
                "id": "workflow-4",
                "name": "financial-analysis",
                "description": "Perform comprehensive financial analysis",
                "module": "packs/fintech",
            },
            {
                "id": "workflow-5",
                "name": "azure-deployment",
                "description": "Deploy application to Azure",
                "module": "packs/devops-azure",
            },
            {
                "id": "workflow-6",
                "name": "query-optimization",
                "description": "Optimize database queries",
                "module": "packs/db-optimization",
            },
        ]

        return {
            "message": "Available Workflows",
            "workflows": workflows,
            "count": len(workflows),
        }

    async def _help(self, request: AgentRequest) -> Dict[str, Any]:
        """
        Provide help information.

        Args:
            request: The request to process

        Returns:
            Help information
        """
        return {
            "message": "MDAN Master Help",
            "agent": self.name,
            "description": self.title,
            "capabilities": self.capabilities,
            "usage": [
                "Use `/mmm-help` to get advice on what to do next",
                "You can combine help with specific topics",
                "Example: `/mmm-help where should I start with an idea I have that does XYZ`",
            ],
            "menu": [
                {"trigger": "MH", "description": "Redisplay Menu Help"},
                {"trigger": "CH", "description": "Chat with the Agent"},
                {"trigger": "LT", "description": "List Available Tasks"},
                {"trigger": "LW", "description": "List Workflows"},
                {"trigger": "PM", "description": "Start Party Mode"},
                {"trigger": "DA", "description": "Dismiss Agent"},
            ],
        }

    async def _handle_unknown_action(self, request: AgentRequest) -> Dict[str, Any]:
        """
        Handle unknown actions.

        Args:
            request: The request to process

        Returns:
            An error message
        """
        return {
            "message": "Action not recognized",
            "action": request.action,
            "suggestion": "Use `/mmm-help` to see available actions",
        }

    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.

        Returns:
            Agent information dictionary
        """
        return {
            "name": self.name,
            "title": self.title,
            "icon": self.icon,
            "capabilities": self.capabilities,
            "role": self.role,
            "identity": self.identity,
            "communication_style": self.communication_style,
            "principles": self.principles,
        }
