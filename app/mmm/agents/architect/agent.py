"""
Architect Agent

A system architect specializing in distributed systems, cloud infrastructure,
and API design. Focuses on scalable patterns and technology selection.
"""

from typing import Any, Dict, List, Optional
import json


class ArchitectAgent:
    """
    Architect Agent - Winston

    Senior architect with expertise in distributed systems, cloud infrastructure,
    and API design. Specializes in scalable patterns and technology selection.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Architect Agent.

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
        self.name = "Winston"
        self.title = "Architect"
        self.icon = "🏗️"
        self.capabilities = [
            "distributed systems",
            "cloud infrastructure",
            "API design",
            "scalable patterns",
        ]

        # Menu items
        self.menu_items = [
            {
                "cmd": "MH",
                "label": "Redisplay Menu Help",
                "description": "Show this menu",
            },
            {
                "cmd": "CH",
                "label": "Chat with the Agent",
                "description": "Chat about anything",
            },
            {
                "cmd": "CA",
                "label": "Create Architecture",
                "description": "Guided workflow to document technical decisions",
            },
            {
                "cmd": "IR",
                "label": "Implementation Readiness",
                "description": "Ensure PRD, UX, Architecture and Epics/Stories are aligned",
            },
            {
                "cmd": "PM",
                "label": "Start Party Mode",
                "description": "Start party mode",
            },
            {"cmd": "DA", "label": "Dismiss Agent", "description": "Exit the agent"},
        ]

    async def process(
        self, input_text: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user input and generate a response.

        Args:
            input_text: The user's input text
            context: Optional context dictionary with additional information

        Returns:
            Dictionary containing:
                - response: The agent's response text
                - action: Any action to be taken
                - context: Updated context
        """
        context = context or {}

        # Check for menu display request
        if self._is_menu_request(input_text):
            return {
                "response": self._get_menu_display(),
                "action": "display_menu",
                "context": context,
            }

        # Check for exit request
        if self._is_exit_request(input_text):
            return {
                "response": f"Goodbye {self.user_name}! It was a pleasure working with you on architecture decisions.",
                "action": "exit",
                "context": context,
            }

        # Check for chat request
        if self._is_chat_request(input_text):
            return {
                "response": self._process_chat(input_text),
                "action": "chat",
                "context": context,
            }

        # Check for specific menu item commands
        menu_action = self._parse_menu_command(input_text)
        if menu_action:
            return await self._execute_menu_item(menu_action, input_text, context)

        # Default: unrecognized command
        return {
            "response": f"I didn't recognize that command. Please select a menu item or type 'MH' to see the menu.",
            "action": "unrecognized",
            "context": context,
        }

    def _is_menu_request(self, input_text: str) -> bool:
        """Check if input is a menu display request."""
        menu_triggers = ["mh", "menu", "help"]
        return any(trigger in input_text.lower() for trigger in menu_triggers)

    def _is_exit_request(self, input_text: str) -> bool:
        """Check if input is an exit request."""
        exit_triggers = ["da", "exit", "leave", "goodbye", "dismiss", "quit"]
        return any(trigger in input_text.lower() for trigger in exit_triggers)

    def _is_chat_request(self, input_text: str) -> bool:
        """Check if input is a chat request."""
        chat_triggers = ["ch", "chat"]
        return any(trigger in input_text.lower() for trigger in chat_triggers)

    def _parse_menu_command(self, input_text: str) -> Optional[str]:
        """Parse menu command from input text."""
        input_lower = input_text.lower().strip()

        for item in self.menu_items:
            cmd = item["cmd"].lower()
            label = item["label"].lower()

            # Check for exact command match
            if input_lower == cmd:
                return cmd

            # Check for fuzzy match on label
            if cmd in input_lower or any(
                word in label for word in input_lower.split() if len(word) > 2
            ):
                return cmd

        return None

    async def _execute_menu_item(
        self, command: str, input_text: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a menu item action."""
        command = command.upper()

        if command == "CA":
            return {
                "response": self._create_architecture(input_text),
                "action": "create_architecture",
                "context": context,
            }
        elif command == "IR":
            return {
                "response": self._implementation_readiness(input_text),
                "action": "implementation_readiness",
                "context": context,
            }
        elif command == "PM":
            return {
                "response": "🎉 Party Mode activated! Let's celebrate our architectural achievements!",
                "action": "party_mode",
                "context": context,
            }

        return {
            "response": f"Command '{command}' recognized but not yet implemented.",
            "action": "not_implemented",
            "context": context,
        }

    def _get_menu_display(self) -> str:
        """Generate the menu display."""
        menu = f"👋 Hello {self.user_name}! I'm {self.name}, your {self.title} {self.icon}\n\n"
        menu += "Here's what I can help you with:\n\n"

        for i, item in enumerate(self.menu_items, 1):
            menu += f"{i}. [{item['cmd']}] {item['label']}\n"
            menu += f"   {item['description']}\n\n"

        menu += f"\n💡 Tip: You can type `/mmm-help` at any time to get advice on what to do next.\n"
        menu += f"Example: `/mmm-help how should I architect this system`\n"

        return menu

    def _process_chat(self, input_text: str) -> str:
        """Process a chat request."""
        # Remove chat command if present
        text = input_text.lower().replace("ch", "").replace("chat", "").strip()

        if not text:
            return "I'd love to chat! What would you like to discuss? I can help with system architecture, distributed systems, cloud infrastructure, API design, and more."

        # Simulate a response based on the input
        return (
            f"Great architectural question! Let me think about this pragmatically.\n\n"
            f"**Key Considerations:**\n"
            f"1. **Scalability**: How will this system grow?\n"
            f"2. **Reliability**: What happens when things fail?\n"
            f"3. **Maintainability**: Can we evolve this over time?\n"
            f"4. **Simplicity**: Are we over-engineering?\n\n"
            f"**My Approach:**\n"
            f"- Start with boring, proven technology\n"
            f"- Design for the current scale, not hypothetical future scale\n"
            f"- Connect every decision to business value\n"
            f"- User journeys should drive technical decisions\n\n"
            f"Your input: '{text}'\n\n"
            f"Let me know if you'd like me to dive deeper into any specific aspect!"
        )

    def _create_architecture(self, input_text: str) -> str:
        """Create architecture documentation."""
        return (
            f"🏗️ **Architecture Creation Workflow**\n\n"
            f"I'll guide you through documenting technical decisions to keep implementation on track.\n\n"
            f"**Architecture Documentation Sections:**\n"
            f"- System Overview\n"
            f"- Architecture Patterns\n"
            f"- Technology Stack\n"
            f"- Component Design\n"
            f"- Data Architecture\n"
            f"- Security Considerations\n"
            f"- Scalability Strategy\n"
            f"- Deployment Architecture\n\n"
            f"**Principles I Follow:**\n"
            f"- Embrace boring technology for stability\n"
            f"- Design simple solutions that scale when needed\n"
            f"- Developer productivity is architecture\n"
            f"- Connect every decision to business value\n"
            f"- User journeys drive technical decisions\n\n"
            f"Tell me about the system you're architecting, and I'll help you create comprehensive documentation!\n\n"
            f"Your input: {input_text}"
        )

    def _implementation_readiness(self, input_text: str) -> str:
        """Check implementation readiness."""
        return (
            f"✅ **Implementation Readiness Check**\n\n"
            f"I'll ensure your PRD, UX, Architecture, and Epics/Stories are all aligned before development begins.\n\n"
            f"**Readiness Checklist:**\n"
            f"- [ ] PRD is complete and approved\n"
            f"- [ ] UX designs are finalized\n"
            f"- [ ] Architecture decisions are documented\n"
            f"- [ ] Epics and Stories are created\n"
            f"- [ ] All artifacts are consistent and aligned\n"
            f"- [ ] Dependencies are identified\n"
            f"- [ ] Risks are documented\n\n"
            f"**What I'll Check:**\n"
            f"- Consistency across all documents\n"
            f"- Completeness of requirements\n"
            f"- Clarity of implementation guidance\n"
            f"- Alignment between business and technical specs\n\n"
            f"Provide the paths to your PRD, UX, Architecture, and Epics/Stories documents, and I'll perform a comprehensive alignment check!\n\n"
            f"Your input: {input_text}"
        )

    def get_greeting(self) -> str:
        """Get the agent's greeting message."""
        return self._get_menu_display()

    def get_capabilities(self) -> List[str]:
        """Get the agent's capabilities."""
        return self.capabilities

    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary representation."""
        return {
            "name": self.name,
            "title": self.title,
            "icon": self.icon,
            "capabilities": self.capabilities,
            "config": self.config,
            "menu_items": self.menu_items,
        }
