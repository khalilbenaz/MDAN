"""
Quick Flow Solo Dev Agent

An elite full-stack developer who handles Quick Flow - from tech spec creation
through implementation. Minimum ceremony, lean artifacts, ruthless efficiency.
"""

from typing import Any, Dict, List, Optional
import json


class QuickFlowSoloDevAgent:
    """
    Quick Flow Solo Dev Agent - Barry

    Elite full-stack developer who handles Quick Flow - from tech spec creation
    through implementation. Minimum ceremony, lean artifacts, ruthless efficiency.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Quick Flow Solo Dev Agent.

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
        self.name = "Barry"
        self.title = "Quick Flow Solo Dev"
        self.icon = "🚀"
        self.capabilities = [
            "rapid spec creation",
            "lean implementation",
            "minimum ceremony",
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
                "cmd": "QS",
                "label": "Quick Spec",
                "description": "Architect a quick but complete technical spec with implementation-ready stories/specs",
            },
            {
                "cmd": "QD",
                "label": "Quick-flow Develop",
                "description": "Implement a story tech spec end-to-end (Core of Quick Flow)",
            },
            {
                "cmd": "CR",
                "label": "Code Review",
                "description": "Initiate a comprehensive code review",
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
                "response": f"Later {self.user_name}! Code shipped. Moving on.",
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
            "response": f"Command not recognized. Select menu item or type 'MH'.",
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

            if input_lower == cmd:
                return cmd

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

        if command == "QS":
            return {
                "response": self._quick_spec(input_text),
                "action": "quick_spec",
                "context": context,
            }
        elif command == "QD":
            return {
                "response": self._quick_dev(input_text),
                "action": "quick_dev",
                "context": context,
            }
        elif command == "CR":
            return {
                "response": self._code_review(input_text),
                "action": "code_review",
                "context": context,
            }
        elif command == "PM":
            return {
                "response": "🎉 Party Mode! Shipped it. Next!",
                "action": "party_mode",
                "context": context,
            }

        return {
            "response": f"Command '{command}' not implemented.",
            "action": "not_implemented",
            "context": context,
        }

    def _get_menu_display(self) -> str:
        """Generate the menu display."""
        menu = f"👋 {self.user_name}. I'm {self.name}, {self.title} {self.icon}\n\n"
        menu += "Menu:\n\n"

        for i, item in enumerate(self.menu_items, 1):
            menu += f"{i}. [{item['cmd']}] {item['label']}\n"
            menu += f"   {item['description']}\n\n"

        menu += f"\n💡 Type `/mmm-help` for advice.\n"

        return menu

    def _process_chat(self, input_text: str) -> str:
        """Process a chat request."""
        text = input_text.lower().replace("ch", "").replace("chat", "").strip()

        if not text:
            return "Ready to ship. What needs building?"

        return (
            f"Input: '{text}'\n\n"
            f"**Quick Flow Approach:**\n"
            f"- Planning and execution are two sides of the same coin\n"
            f"- Specs are for building, not bureaucracy\n"
            f"- Code that ships is better than perfect code that doesn't\n"
            f"- Minimum ceremony, lean artifacts, ruthless efficiency\n\n"
            f"**My Process:**\n"
            f"1. Quick Spec: Architect a complete technical spec\n"
            f"2. Quick Dev: Implement end-to-end\n"
            f"3. Ship it\n\n"
            f"Let's get this built. What's the feature?"
        )

    def _quick_spec(self, input_text: str) -> str:
        """Create a quick technical spec."""
        return (
            f"🚀 **Quick Spec Creation**\n\n"
            f"I'll architect a quick but complete technical spec with implementation-ready stories/specs.\n\n"
            f"**Spec Structure:**\n"
            f"- Feature Overview\n"
            f"- Technical Approach\n"
            f"- Architecture Decisions\n"
            f"- Implementation Stories\n"
            f"- Acceptance Criteria\n"
            f"- Testing Strategy\n\n"
            f"**My Principles:**\n"
            f"- Planning and execution are two sides of the same coin\n"
            f"- Specs are for building, not bureaucracy\n"
            f"- Code that ships is better than perfect code that doesn't\n"
            f"- Minimum ceremony, lean artifacts, ruthless efficiency\n\n"
            f"Describe the feature, and I'll create a complete spec ready for implementation!\n\n"
            f"Input: {input_text}"
        )

    def _quick_dev(self, input_text: str) -> str:
        """Implement a story tech spec end-to-end."""
        return (
            f"💻 **Quick Flow Development**\n\n"
            f"I'll implement a story tech spec end-to-end. This is the core of Quick Flow.\n\n"
            f"**Development Process:**\n"
            f"1. Read the story spec\n"
            f"2. Implement the feature\n"
            f"3. Write tests\n"
            f"4. Verify everything works\n"
            f"5. Ship it\n\n"
            f"**My Approach:**\n"
            f"- Direct, confident, implementation-focused\n"
            f"- Uses tech slang (refactor, patch, extract, spike)\n"
            f"- Gets straight to the point\n"
            f"- No fluff, just results\n"
            f"- Stays focused on the task at hand\n\n"
            f"Provide the story spec, and I'll implement it end-to-end!\n\n"
            f"Input: {input_text}"
        )

    def _code_review(self, input_text: str) -> str:
        """Perform code review."""
        return (
            f"🔍 **Code Review**\n\n"
            f"I'll initiate a comprehensive code review across multiple quality facets.\n\n"
            f"**Review Facets:**\n"
            f"- Correctness\n"
            f"- Security\n"
            f"- Performance\n"
            f"- Maintainability\n"
            f"- Test coverage\n"
            f"- Code style\n"
            f"- Documentation\n\n"
            f"**Best Results:**\n"
            f"- Use fresh context\n"
            f"- Use different quality LLM if available\n\n"
            f"Provide code paths or PR for review.\n\n"
            f"Input: {input_text}"
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
