"""
Scrum Master Agent

A technical Scrum Master with deep technical background. Expert in agile ceremonies,
story preparation, and creating clear actionable user stories.
"""

from typing import Any, Dict, List, Optional
import json


class SMAgent:
    """
    Scrum Master Agent - Bob

    Certified Scrum Master with deep technical background. Expert in agile ceremonies,
    story preparation, and creating clear actionable user stories.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Scrum Master Agent.

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
        self.name = "Bob"
        self.title = "Scrum Master"
        self.icon = "🏃"
        self.capabilities = [
            "sprint planning",
            "story preparation",
            "agile ceremonies",
            "backlog management",
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
                "cmd": "SP",
                "label": "Sprint Planning",
                "description": "Generate or update the record that will sequence the tasks",
            },
            {
                "cmd": "CS",
                "label": "Context Story",
                "description": "Prepare a story with all required context for implementation",
            },
            {
                "cmd": "ER",
                "label": "Epic Retrospective",
                "description": "Party Mode review of all work completed across an epic",
            },
            {
                "cmd": "CC",
                "label": "Course Correction",
                "description": "Determine how to proceed if major need for change is discovered",
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
                "response": f"Goodbye {self.user_name}! Great sprint. Let's keep the momentum going!",
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

        if command == "SP":
            return {
                "response": self._sprint_planning(input_text),
                "action": "sprint_planning",
                "context": context,
            }
        elif command == "CS":
            return {
                "response": self._create_story(input_text),
                "action": "create_story",
                "context": context,
            }
        elif command == "ER":
            return {
                "response": self._epic_retrospective(input_text),
                "action": "epic_retrospective",
                "context": context,
            }
        elif command == "CC":
            return {
                "response": self._course_correction(input_text),
                "action": "course_correction",
                "context": context,
            }
        elif command == "PM":
            return {
                "response": "🎉 Party Mode! Great sprint everyone! Let's celebrate our wins!",
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
        menu += f"Example: `/mmm-help how should I plan this sprint`\n"

        return menu

    def _process_chat(self, input_text: str) -> str:
        """Process a chat request."""
        text = input_text.lower().replace("ch", "").replace("chat", "").strip()

        if not text:
            return "I'd love to chat! What would you like to discuss? I can help with agile ceremonies, sprint planning, story preparation, and more."

        return (
            f"Great agile question! Let me think about this systematically.\n\n"
            f"**My Approach:**\n"
            f"- Crisp and checklist-driven\n"
            f"- Every word has a purpose\n"
            f"- Every requirement crystal clear\n"
            f"- Zero tolerance for ambiguity\n\n"
            f"**My Principles:**\n"
            f"- I strive to be a servant leader and conduct myself accordingly\n"
            f"- I help with any task and offer suggestions\n"
            f"- I love to talk about Agile process and theory whenever anyone wants to\n\n"
            f"Your input: '{text}'\n\n"
            f"Let me know if you'd like me to dive deeper into any specific aspect!"
        )

    def _sprint_planning(self, input_text: str) -> str:
        """Generate or update sprint planning record."""
        return (
            f"🏃 **Sprint Planning**\n\n"
            f"I'll generate or update the record that will sequence the tasks to complete the full project that the dev agent will follow.\n\n"
            f"**Sprint Planning Record:**\n"
            f"- Sprint Goal\n"
            f"- Sprint Backlog\n"
            f"- Task Breakdown\n"
            f"- Task Sequence\n"
            f"- Estimates\n"
            f"- Dependencies\n"
            f"- Risks\n\n"
            f"**My Approach:**\n"
            f"- Crisp and checklist-driven\n"
            f"- Every word has a purpose\n"
            f"- Every requirement crystal clear\n"
            f"- Zero tolerance for ambiguity\n\n"
            f"Provide the epics and stories, and I'll create a comprehensive sprint plan!\n\n"
            f"Input: {input_text}"
        )

    def _create_story(self, input_text: str) -> str:
        """Prepare a story with all required context."""
        return (
            f"📝 **Story Preparation**\n\n"
            f"I'll prepare a story with all required context for implementation for the developer agent.\n\n"
            f"**Story Context:**\n"
            f"- Story ID and Title\n"
            f"- User Story\n"
            f"- Acceptance Criteria\n"
            f"- Tasks/Subtasks\n"
            f"- Technical Context\n"
            f"- Dependencies\n"
            f"- Definition of Done\n"
            f"- Testing Requirements\n\n"
            f"**My Approach:**\n"
            f"- Crisp and checklist-driven\n"
            f"- Every word has a purpose\n"
            f"- Every requirement crystal clear\n"
            f"- Zero tolerance for ambiguity\n\n"
            f"Provide the story details, and I'll prepare it for implementation!\n\n"
            f"Input: {input_text}"
        )

    def _epic_retrospective(self, input_text: str) -> str:
        """Conduct epic retrospective."""
        return (
            f"🎉 **Epic Retrospective**\n\n"
            f"I'll conduct a Party Mode review of all work completed across an epic.\n\n"
            f"**Retrospective Agenda:**\n"
            f"- What went well?\n"
            f"- What didn't go well?\n"
            f"- What did we learn?\n"
            f"- What should we do differently?\n"
            f"- Action items\n\n"
            f"**Review Areas:**\n"
            f"- Process\n"
            f"- Communication\n"
            f"- Technical decisions\n"
            f"- Team collaboration\n"
            f"- Deliverables\n\n"
            f"Let's celebrate our wins and learn from our challenges!\n\n"
            f"Input: {input_text}"
        )

    def _course_correction(self, input_text: str) -> str:
        """Determine course correction strategy."""
        return (
            f"🔄 **Course Correction**\n\n"
            f"I'll help you determine how to proceed if a major need for change is discovered mid-implementation.\n\n"
            f"**Course Correction Process:**\n"
            f"1. Assess the change impact\n"
            f"2. Evaluate options (pivot, adjust, continue)\n"
            f"3. Update affected artifacts\n"
            f"4. Communicate changes to team\n"
            f"5. Adjust timeline and estimates\n"
            f"6. Document decision rationale\n\n"
            f"**Options to Consider:**\n"
            f"- **Pivot**: Major direction change\n"
            f"- **Adjust**: Modify scope or approach\n"
            f"- **Continue**: Defer change to next iteration\n\n"
            f"Describe the change that's needed, and I'll help you determine the best course of action!\n\n"
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
