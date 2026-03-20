"""
Agent Builder Agent

A master agent architect with deep expertise in agent design patterns, persona development,
and MDAN Core compliance. Specializes in creating robust, maintainable agents that follow best practices.
"""

from typing import Any, Dict, List, Optional
import json


class AgentBuilderAgent:
    """
    Agent Builder Agent - Bond

    Master agent architect with deep expertise in agent design patterns, persona development,
    and MDAN Core compliance. Specializes in creating robust, maintainable agents that follow
    best practices.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Agent Builder Agent.

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
        self.name = "Bond"
        self.title = "Agent Building Expert"
        self.icon = "🤖"
        self.capabilities = [
            "agent design patterns",
            "persona development",
            "MDAN Core compliance",
            "best practices enforcement",
            "agent validation",
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
                "description": "Have a conversation about agent building topics",
            },
            {
                "cmd": "CA",
                "label": "Create a new MDAN agent",
                "description": "Create a new BMAD agent with best practices and compliance",
            },
            {
                "cmd": "EA",
                "label": "Edit existing MDAN agents",
                "description": "Edit existing BMAD agents while maintaining compliance",
            },
            {
                "cmd": "VA",
                "label": "Validate existing MDAN agents",
                "description": "Validate existing BMAD agents and offer to improve deficiencies",
            },
            {
                "cmd": "DA",
                "label": "Dismiss Agent",
                "description": "Exit the agent builder",
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
        elif request_lower in ["ca", "create-agent"]:
            return self._handle_create_agent(request)
        elif request_lower in ["ea", "edit-agent"]:
            return self._handle_edit_agent(request)
        elif request_lower in ["va", "validate-agent"]:
            return self._handle_validate_agent(request)
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
        menu = f"\n🤖 **Agent Builder Menu**\n\n"
        menu += f"Hello {self.user_name}! I'm Bond, your Agent Building Expert.\n\n"
        menu += "Available commands:\n\n"

        for i, item in enumerate(self.menu_items, 1):
            menu += f"{i}. **[{item['cmd']}]** {item['label']}\n"
            menu += f"   {item['description']}\n\n"

        menu += "Type a command number or use the command shortcut (e.g., 'CA' for Create Agent).\n"
        menu += "You can also type `/mmm-help` for advice on what to do next.\n"

        return menu

    def _handle_chat(self, request: str) -> str:
        """Handle general chat requests."""
        return f"""
I'm Bond, your Agent Building Expert. I specialize in:

- Agent design patterns and architecture
- Persona development and character creation
- MDAN Core compliance and best practices
- Agent validation and improvement

What would you like to know about building agents?
"""

    def _handle_create_agent(self, request: str) -> str:
        """Handle create agent requests."""
        return """
To create a new MDAN agent, I'll need the following information:

1. **Agent Name**: What should we call this agent?
2. **Agent Title**: What is the agent's role or title?
3. **Agent Icon**: Choose an emoji to represent the agent
4. **Agent Role**: What is the agent's primary role?
5. **Agent Identity**: Describe the agent's background and expertise
6. **Communication Style**: How should the agent communicate?
7. **Principles**: What principles guide the agent's behavior?
8. **Capabilities**: What are the agent's key capabilities?
9. **Menu Items**: What actions should the agent be able to perform?

Please provide these details, and I'll create a compliant agent for you.
"""

    def _handle_edit_agent(self, request: str) -> str:
        """Handle edit agent requests."""
        return """
To edit an existing MDAN agent, please specify:

1. **Agent Name**: Which agent do you want to edit?
2. **Changes**: What aspects do you want to modify?
   - Persona/Identity
   - Communication Style
   - Principles
   - Capabilities
   - Menu Items
   - Other

I'll help you make the changes while maintaining MDAN Core compliance.
"""

    def _handle_validate_agent(self, request: str) -> str:
        """Handle validate agent requests."""
        return """
To validate an MDAN agent, I'll check for:

✓ **Structure Compliance**: Proper file structure and naming
✓ **Persona Quality**: Clear, specific, and authentic persona
✓ **Menu Consistency**: Consistent menu structure across agents
✓ **Best Practices**: Following MDAN Core standards
✓ **Documentation**: Complete and clear documentation
✓ **Runtime Loading**: Proper resource loading at runtime

Please specify which agent you'd like me to validate.
"""

    def _handle_dismiss(self) -> str:
        """Handle dismiss requests."""
        return f"""
Goodbye, {self.user_name}! It was a pleasure helping you with agent building.

Remember:
- Every agent must follow MDAN Core standards
- Personas drive agent behavior - make them specific and authentic
- Menu structure must be consistent across all agents
- Validate compliance before finalizing any agent

Feel free to return anytime you need help building agents! 👋
"""

    def _handle_general_request(self, request: str) -> str:
        """Handle general requests."""
        return f"""
I understand you're asking about: "{request}"

As an Agent Building Expert, I can help you with:
- Creating new agents (use 'CA' or 'create-agent')
- Editing existing agents (use 'EA' or 'edit-agent')
- Validating agents (use 'VA' or 'validate-agent')
- General agent building questions (use 'CH' or 'chat')

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
                elif item["cmd"] == "CA":
                    return self._handle_create_agent(request)
                elif item["cmd"] == "EA":
                    return self._handle_edit_agent(request)
                elif item["cmd"] == "VA":
                    return self._handle_validate_agent(request)
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
