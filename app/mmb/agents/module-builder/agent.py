"""
Module Builder Agent

An expert module architect with comprehensive knowledge of MDAN Core systems, integration patterns,
and end-to-end module development. Specializes in creating cohesive, scalable modules that deliver
complete functionality.
"""

from typing import Any, Dict, List, Optional
import json


class ModuleBuilderAgent:
    """
    Module Builder Agent - Morgan

    Expert module architect with comprehensive knowledge of MDAN Core systems, integration patterns,
    and end-to-end module development. Specializes in creating cohesive, scalable modules that
    deliver complete functionality.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Module Builder Agent.

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
        self.name = "Morgan"
        self.title = "Module Creation Master"
        self.icon = "🏗️"
        self.capabilities = [
            "module architecture",
            "integration patterns",
            "end-to-end module development",
            "modularity and reusability",
            "system-wide impact analysis",
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
                "description": "Have a conversation about module building topics",
            },
            {
                "cmd": "PB",
                "label": "Create product brief",
                "description": "Create product brief for MDAN module development",
            },
            {
                "cmd": "CM",
                "label": "Create a complete MDAN module",
                "description": "Create a complete MDAN module with agents, workflows, and infrastructure",
            },
            {
                "cmd": "EM",
                "label": "Edit existing MDAN modules",
                "description": "Edit existing MDAN modules while maintaining coherence",
            },
            {
                "cmd": "VM",
                "label": "Run compliance check",
                "description": "Run compliance check on MDAN modules against best practices",
            },
            {
                "cmd": "DA",
                "label": "Dismiss Agent",
                "description": "Exit the module builder",
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
        elif request_lower in ["pb", "product-brief"]:
            return self._handle_product_brief(request)
        elif request_lower in ["cm", "create-module"]:
            return self._handle_create_module(request)
        elif request_lower in ["em", "edit-module"]:
            return self._handle_edit_module(request)
        elif request_lower in ["vm", "validate-module"]:
            return self._handle_validate_module(request)
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
        menu = f"\n🏗️ **Module Builder Menu**\n\n"
        menu += f"Hello {self.user_name}! I'm Morgan, your Module Creation Master.\n\n"
        menu += "Available commands:\n\n"

        for i, item in enumerate(self.menu_items, 1):
            menu += f"{i}. **[{item['cmd']}]** {item['label']}\n"
            menu += f"   {item['description']}\n\n"

        menu += "Type a command number or use the command shortcut (e.g., 'CM' for Create Module).\n"
        menu += "You can also type `/mmm-help` for advice on what to do next.\n"

        return menu

    def _handle_chat(self, request: str) -> str:
        """Handle general chat requests."""
        return f"""
I'm Morgan, your Module Creation Master. I specialize in:

- Module architecture and design
- Integration patterns and dependencies
- End-to-end module development
- Modularity and reusability
- System-wide impact analysis

What would you like to know about building modules?
"""

    def _handle_product_brief(self, request: str) -> str:
        """Handle product brief requests."""
        return """
To create a product brief for a new MDAN module, I'll need:

1. **Module Name**: What should we call this module?
2. **Module Purpose**: What problem does this module solve?
3. **Target Users**: Who will use this module?
4. **Key Features**: What are the main features?
5. **Integration Points**: How does this integrate with existing systems?
6. **Success Metrics**: How do we measure success?

Please provide these details, and I'll create a comprehensive product brief.
"""

    def _handle_create_module(self, request: str) -> str:
        """Handle create module requests."""
        return """
To create a complete MDAN module, I'll need:

1. **Module Structure**:
   - Module name and directory structure
   - Agents to include
   - Workflows to implement
   - Infrastructure requirements

2. **Module Components**:
   - Agent definitions and personas
   - Workflow definitions and state machines
   - Integration points and APIs
   - Data models and schemas

3. **Documentation**:
   - Module README
   - API documentation
   - Usage examples
   - Integration guides

Please provide the module requirements, and I'll create a complete, compliant module.
"""

    def _handle_edit_module(self, request: str) -> str:
        """Handle edit module requests."""
        return """
To edit an existing MDAN module, please specify:

1. **Module Name**: Which module do you want to edit?
2. **Changes**: What aspects do you want to modify?
   - Module structure
   - Agent definitions
   - Workflow definitions
   - Integration points
   - Documentation
   - Other

I'll help you make the changes while maintaining module coherence and compliance.
"""

    def _handle_validate_module(self, request: str) -> str:
        """Handle validate module requests."""
        return """
To validate an MDAN module, I'll check for:

✓ **Module Structure**: Proper directory structure and organization
✓ **Self-Containment**: Module is self-contained yet integrates seamlessly
✓ **Business Value**: Module solves specific business problems effectively
✓ **Documentation**: Complete documentation and examples
✓ **Scalability**: Module plans for growth and evolution
✓ **Best Practices**: Follows proven patterns and standards
✓ **Lifecycle**: Considers entire module lifecycle from creation to maintenance

Please specify which module you'd like me to validate.
"""

    def _handle_dismiss(self) -> str:
        """Handle dismiss requests."""
        return f"""
Goodbye, {self.user_name}! It was a pleasure helping you with module building.

Remember:
- Modules must be self-contained yet integrate seamlessly
- Every module should solve specific business problems effectively
- Documentation and examples are as important as code
- Plan for growth and evolution from day one
- Balance innovation with proven patterns
- Consider the entire module lifecycle from creation to maintenance

Feel free to return anytime you need help building modules! 👋
"""

    def _handle_general_request(self, request: str) -> str:
        """Handle general requests."""
        return f"""
I understand you're asking about: "{request}"

As a Module Creation Master, I can help you with:
- Creating product briefs (use 'PB' or 'product-brief')
- Creating complete modules (use 'CM' or 'create-module')
- Editing existing modules (use 'EM' or 'edit-module')
- Validating modules (use 'VM' or 'validate-module')
- General module building questions (use 'CH' or 'chat')

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
                elif item["cmd"] == "PB":
                    return self._handle_product_brief(request)
                elif item["cmd"] == "CM":
                    return self._handle_create_module(request)
                elif item["cmd"] == "EM":
                    return self._handle_edit_module(request)
                elif item["cmd"] == "VM":
                    return self._handle_validate_module(request)
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
