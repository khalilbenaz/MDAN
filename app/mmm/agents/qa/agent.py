"""
QA Engineer Agent

A pragmatic test automation engineer focused on rapid test coverage.
Specializes in generating tests quickly for existing features using standard
test framework patterns.
"""

from typing import Any, Dict, List, Optional
import json


class QAAgent:
    """
    QA Engineer Agent - Quinn

    Pragmatic test automation engineer focused on rapid test coverage.
    Specializes in generating tests quickly for existing features using standard
    test framework patterns. Simpler, more direct approach than the advanced
    Test Architect module.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the QA Engineer Agent.

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
        self.name = "Quinn"
        self.title = "QA Engineer"
        self.icon = "🧪"
        self.capabilities = [
            "test automation",
            "API testing",
            "E2E testing",
            "coverage analysis",
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
                "cmd": "QA",
                "label": "Automate - Generate tests",
                "description": "Generate tests for existing features (simplified)",
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
                "response": f"Goodbye {self.user_name}! Tests passing. Coverage good.",
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

        if command == "QA":
            return {
                "response": self._qa_automate(input_text),
                "action": "qa_automate",
                "context": context,
            }
        elif command == "PM":
            return {
                "response": "🎉 Party Mode! All tests passing. Coverage complete.",
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
        menu = f"👋 Hi {self.user_name}! I'm {self.name}, your {self.title} {self.icon}\n\n"
        menu += "Here's what I can help you with:\n\n"

        for i, item in enumerate(self.menu_items, 1):
            menu += f"{i}. [{item['cmd']}] {item['label']}\n"
            menu += f"   {item['description']}\n\n"

        menu += f"\n💡 Tip: You can type `/mmm-help` at any time to get advice on what to do next.\n"

        return menu

    def _process_chat(self, input_text: str) -> str:
        """Process a chat request."""
        text = input_text.lower().replace("ch", "").replace("chat", "").strip()

        if not text:
            return "Ready to generate tests! What would you like me to test?"

        return (
            f"Input: '{text}'\n\n"
            f"**My Approach:**\n"
            f"- Generate API and E2E tests for existing features\n"
            f"- Use standard test framework patterns (simple and maintainable)\n"
            f"- Focus on happy path + critical edge cases\n"
            f"- Get you covered fast without overthinking\n"
            f"- Generate tests only (use Code Review `CR` for review/validation)\n\n"
            f"**When to use me:**\n"
            f"- Quick test coverage for small-medium projects\n"
            f"- Beginner-friendly test automation\n"
            f"- Standard patterns without advanced utilities\n\n"
            f"**Need more advanced testing?**\n"
            f"For comprehensive test strategy, risk-based planning, quality gates, and enterprise features,\n"
            f"install the Test Architect (TEA) module."
        )

    def _qa_automate(self, input_text: str) -> str:
        """Generate tests for existing features."""
        return (
            f"🧪 **Test Generation**\n\n"
            f"I'll generate tests for your existing features using standard test framework patterns.\n\n"
            f"**What I'll Generate:**\n"
            f"- API tests (endpoints, requests, responses)\n"
            f"- E2E tests (user flows, critical paths)\n"
            f"- Unit tests (functions, components)\n"
            f"- Integration tests (component interactions)\n\n"
            f"**My Principles:**\n"
            f"- Never skip running generated tests to verify they pass\n"
            f"- Always use standard test framework APIs (no external utilities)\n"
            f"- Keep tests simple and maintainable\n"
            f"- Focus on realistic user scenarios\n"
            f"- Tests should pass on first run\n\n"
            f"**Test Structure:**\n"
            f"- Arrange-Act-Assert pattern\n"
            f"- Descriptive test names\n"
            f"- Clear setup and teardown\n"
            f"- Proper assertions\n\n"
            f"Provide the code or feature you'd like me to generate tests for!\n\n"
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
