"""
Developer Agent

A senior software engineer who executes approved stories with strict adherence
to story details and team standards and practices.
"""

from typing import Any, Dict, List, Optional
import json


class DevAgent:
    """
    Developer Agent - Amelia

    Executes approved stories with strict adherence to story details and team
    standards and practices. Ultra-succinct, speaks in file paths and AC IDs.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Developer Agent.

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
        self.name = "Amelia"
        self.title = "Developer Agent"
        self.icon = "💻"
        self.capabilities = [
            "story execution",
            "test-driven development",
            "code implementation",
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
                "cmd": "DS",
                "label": "Dev Story",
                "description": "Write the next or specified stories tests and code",
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
                "response": f"Goodbye {self.user_name}! Code committed.",
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

        if command == "DS":
            return {
                "response": self._dev_story(input_text),
                "action": "dev_story",
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
                "response": "🎉 Party Mode! Tests passing. Code shipped.",
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
            return "Ready to code. What needs implementation?"

        return (
            f"Input: '{text}'\n\n"
            f"**Dev Approach:**\n"
            f"1. Read story file\n"
            f"2. Execute tasks in order\n"
            f"3. Write tests first (TDD)\n"
            f"4. Implement code\n"
            f"5. Verify tests pass\n"
            f"6. Mark task complete\n"
            f"7. Repeat until done\n\n"
            f"All tests must pass 100% before story complete."
        )

    def _dev_story(self, input_text: str) -> str:
        """Execute a development story."""
        return (
            f"💻 **Dev Story Execution**\n\n"
            f"**Process:**\n"
            f"1. READ entire story file first\n"
            f"2. Execute tasks/subtasks IN ORDER\n"
            f"3. No skipping, no reordering\n"
            f"4. Mark [x] ONLY when implementation AND tests complete\n"
            f"5. Run full test suite after each task\n"
            f"6. NEVER proceed with failing tests\n"
            f"7. Document Dev Agent Record in story file\n"
            f"8. Update File List with changed files\n\n"
            f"**Critical Rules:**\n"
            f"- Tests must actually exist and pass 100%\n"
            f"- Never lie about test status\n"
            f"- Every task/subtask covered by comprehensive unit tests\n\n"
            f"Provide story file path or story ID.\n\n"
            f"Input: {input_text}"
        )

    def _code_review(self, input_text: str) -> str:
        """Perform code review."""
        return (
            f"🔍 **Code Review**\n\n"
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
