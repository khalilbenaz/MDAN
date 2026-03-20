"""
Workflow Builder Agent

A master workflow architect with expertise in process design, state management, and workflow optimization.
Specializes in creating efficient, scalable workflows that integrate seamlessly with MDAN systems.
"""

from typing import Any, Dict, List, Optional
import json


class WorkflowBuilderAgent:
    """
    Workflow Builder Agent - Wendy

    Master workflow architect with expertise in process design, state management, and workflow
    optimization. Specializes in creating efficient, scalable workflows that integrate seamlessly
    with MDAN systems.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Workflow Builder Agent.

        Args:
            config: Optional configuration dictionary containing:
                - user_name: Name of the user
                - communication_language: Language for communication
                - output_folder: Path for output files
        """
        self.config = config or {}
        self.user_name = self.config.get("user_name", "User")
        self.communication_language = self.config.get(
            "communication_language", "English"
        )
        self.output_folder = self.config.get("output_folder", "./output")

        # Agent metadata
        self.name = "Wendy"
        self.title = "Workflow Building Master"
        self.icon = "🔄"
        self.capabilities = [
            "process design",
            "state management",
            "workflow optimization",
            "error handling",
            "workflow documentation",
        ]

        # Menu items
        self.menu_items = [
            {
                "cmd": "MH",
                "label": "Redisplay Menu Help",
                "description": "Show the main menu with all available options",
            },
            {
                "cmd": "CH",
                "label": "Chat with the Agent",
                "description": "Have a conversation about workflow building topics",
            },
            {
                "cmd": "CW",
                "label": "Create a new MDAN workflow",
                "description": "Create a new BMAD workflow with proper structure and best practices",
            },
            {
                "cmd": "EW",
                "label": "Edit existing MDAN workflows",
                "description": "Edit existing BMAD workflows while maintaining integrity",
            },
            {
                "cmd": "VW",
                "label": "Run validation check",
                "description": "Run validation check on BMAD workflows against best practices",
            },
            {
                "cmd": "MV",
                "label": "Run MAX-PARALLEL validation",
                "description": "Run validation checks in MAX-PARALLEL mode against a workflow",
            },
            {
                "cmd": "RW",
                "label": "Rework to V6 Compliant Version",
                "description": "Rework a Workflow to a V6 Compliant Version",
            },
            {
                "cmd": "DA",
                "label": "Dismiss Agent",
                "description": "Exit the workflow builder",
            },
        ]

    async def process(self, request: str) -> str:
        """
        Process a user request and return a response.

        Args:
            request: The user's request or command

        Returns:
            A response string
        """
        # Parse the request
        request_lower = request.lower().strip()

        # Check for menu commands
        if request_lower in ["mh", "menu", "help"]:
            return self._display_menu()
        elif request_lower in ["ch", "chat"]:
            return self._handle_chat(request)
        elif request_lower in ["cw", "create-workflow"]:
            return self._handle_create_workflow(request)
        elif request_lower in ["ew", "edit-workflow"]:
            return self._handle_edit_workflow(request)
        elif request_lower in ["vw", "validate-workflow"]:
            return self._handle_validate_workflow(request)
        elif request_lower in ["mv", "validate-max-parallel-workflow"]:
            return self._handle_validate_max_parallel(request)
        elif request_lower in ["rw", "convert-or-rework-workflow"]:
            return self._handle_rework_workflow(request)
        elif request_lower in ["da", "exit", "leave", "goodbye", "dismiss"]:
            return self._handle_dismiss()
        else:
            # Try fuzzy matching
            matched = self._fuzzy_match(request_lower)
            if matched:
                return matched
            else:
                return self._handle_general_request(request)

    def _display_menu(self) -> str:
        """Display the main menu."""
        menu = f"\n🔄 **Workflow Builder Menu**\n\n"
        menu += f"Hello {self.user_name}! I'm Wendy, your Workflow Building Master.\n\n"
        menu += "Available commands:\n\n"

        for i, item in enumerate(self.menu_items, 1):
            menu += f"{i}. **[{item['cmd']}]** {item['label']}\n"
            menu += f"   {item['description']}\n\n"

        menu += "Type a command number or use the command shortcut (e.g., 'CW' for Create Workflow).\n"
        menu += "You can also type `/mmm-help` for advice on what to do next.\n"

        return menu

    def _handle_chat(self, request: str) -> str:
        """Handle general chat requests."""
        return f"""
I'm Wendy, your Workflow Building Master. I specialize in:

- Process design and optimization
- State management and transitions
- Workflow architecture and patterns
- Error handling and edge cases
- Workflow documentation

What would you like to know about building workflows?
"""

    def _handle_create_workflow(self, request: str) -> str:
        """Handle create workflow requests."""
        return """
To create a new MDAN workflow, I'll need:

1. **Workflow Purpose**: What is the workflow's goal?
2. **Entry Points**: How does the workflow start?
3. **Exit Points**: What are the possible outcomes?
4. **States and Transitions**: What are the workflow states?
5. **Error Handling**: How should errors be handled?
6. **Data Flow**: What data flows through the workflow?
7. **Integration Points**: How does it integrate with other systems?

Please provide these details, and I'll create a compliant workflow for you.
"""

    def _handle_edit_workflow(self, request: str) -> str:
        """Handle edit workflow requests."""
        return """
To edit an existing MDAN workflow, please specify:

1. **Workflow Name**: Which workflow do you want to edit?
2. **Changes**: What aspects do you want to modify?
   - States and transitions
   - Entry and exit points
   - Error handling
   - Data flow
   - Integration points
   - Documentation
   - Other

I'll help you make the changes while maintaining workflow integrity.
"""

    def _handle_validate_workflow(self, request: str) -> str:
        """Handle validate workflow requests."""
        return """
To validate an MDAN workflow, I'll check for:

✓ **Efficiency**: Workflow is efficient and performant
✓ **Reliability**: Workflow is reliable and consistent
✓ **Maintainability**: Workflow is easy to maintain
✓ **Entry/Exit Points**: Clear entry and exit points
✓ **Error Handling**: Comprehensive error handling and edge cases
✓ **Documentation**: Comprehensive and clear documentation
✓ **Testing**: Workflow has been thoroughly tested
✓ **Performance**: Optimized for performance
✓ **User Experience**: Optimized for user experience

Please specify which workflow you'd like me to validate.
"""

    def _handle_validate_max_parallel(self, request: str) -> str:
        """Handle max-parallel validation requests."""
        return """
To run MAX-PARALLEL validation on a workflow, I'll:

1. **Analyze Parallel Execution**: Identify parallelizable steps
2. **Check Dependencies**: Verify dependency correctness
3. **Validate State Management**: Ensure proper state handling
4. **Test Race Conditions**: Check for race conditions
5. **Verify Resource Usage**: Assess resource utilization
6. **Measure Performance**: Compare parallel vs sequential performance

This requires a tool that supports Parallel Sub-Processes.

Please specify which workflow you'd like me to validate in MAX-PARALLEL mode.
"""

    def _handle_rework_workflow(self, request: str) -> str:
        """Handle rework workflow requests."""
        return """
To rework a workflow to V6 Compliant Version, I'll:

1. **Analyze Current Version**: Review existing workflow structure
2. **Identify V6 Requirements**: Determine V6 compliance requirements
3. **Plan Migration**: Create a migration plan
4. **Update Structure**: Modify workflow structure to V6 standards
5. **Update Documentation**: Update all documentation
6. **Test Changes**: Validate the reworked workflow

Please specify which workflow you'd like me to rework to V6 compliance.
"""

    def _handle_dismiss(self) -> str:
        """Handle dismiss requests."""
        return f"""
Goodbye, {self.user_name}! It was a pleasure helping you with workflow building.

Remember:
- Workflows must be efficient, reliable, and maintainable
- Every workflow should have clear entry and exit points
- Error handling and edge cases are critical for robust workflows
- Workflow documentation must be comprehensive and clear
- Test workflows thoroughly before deployment
- Optimize for both performance and user experience

Feel free to return anytime you need help building workflows! 👋
"""

    def _handle_general_request(self, request: str) -> str:
        """Handle general requests."""
        return f"""
I understand you're asking about: "{request}"

As a Workflow Building Master, I can help you with:
- Creating workflows (use 'CW' or 'create-workflow')
- Editing workflows (use 'EW' or 'edit-workflow')
- Validating workflows (use 'VW' or 'validate-workflow')
- MAX-PARALLEL validation (use 'MV' or 'validate-max-parallel')
- Reworking to V6 compliance (use 'RW' or 'rework-workflow')
- General workflow building questions (use 'CH' or 'chat')

Type 'MH' or 'menu' to see all available commands.
"""

    def _fuzzy_match(self, request: str) -> Optional[str]:
        """Try to fuzzy match the request to a menu item."""
        for item in self.menu_items:
            if item["cmd"].lower() in request or any(
                keyword in request for keyword in item["label"].lower().split()
            ):
                # Call the appropriate handler
                if item["cmd"] == "MH":
                    return self._display_menu()
                elif item["cmd"] == "CH":
                    return self._handle_chat(request)
                elif item["cmd"] == "CW":
                    return self._handle_create_workflow(request)
                elif item["cmd"] == "EW":
                    return self._handle_edit_workflow(request)
                elif item["cmd"] == "VW":
                    return self._handle_validate_workflow(request)
                elif item["cmd"] == "MV":
                    return self._handle_validate_max_parallel(request)
                elif item["cmd"] == "RW":
                    return self._handle_rework_workflow(request)
                elif item["cmd"] == "DA":
                    return self._handle_dismiss()
        return None

    def get_menu_items(self) -> List[Dict[str, str]]:
        """Get the menu items."""
        return self.menu_items

    def get_capabilities(self) -> List[str]:
        """Get the agent's capabilities."""
        return self.capabilities

    def get_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "name": self.name,
            "title": self.title,
            "icon": self.icon,
            "capabilities": self.capabilities,
            "menu_items": self.menu_items,
        }
