"""
Product Manager Agent

A product manager specializing in collaborative PRD creation through user interviews,
requirement discovery, and stakeholder alignment.
"""

from typing import Any, Dict, List, Optional
import json


class PMAgent:
    """
    Product Manager Agent - John

    Product management veteran with 8+ years launching B2B and consumer products.
    Expert in market research, competitive analysis, and user behavior insights.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Product Manager Agent.

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
        self.name = "John"
        self.title = "Product Manager"
        self.icon = "📋"
        self.capabilities = [
            "PRD creation",
            "requirements discovery",
            "stakeholder alignment",
            "user interviews",
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
                "cmd": "CP",
                "label": "Create PRD",
                "description": "Expert led facilitation to produce your Product Requirements Document",
            },
            {
                "cmd": "VP",
                "label": "Validate PRD",
                "description": "Validate a Product Requirements Document is comprehensive, lean, well organized and cohesive",
            },
            {
                "cmd": "EP",
                "label": "Edit PRD",
                "description": "Update an existing Product Requirements Document",
            },
            {
                "cmd": "CE",
                "label": "Create Epics and Stories",
                "description": "Create the Epics and Stories Listing",
            },
            {
                "cmd": "IR",
                "label": "Implementation Readiness",
                "description": "Ensure the PRD, UX, and Architecture and Epics and Stories List are all aligned",
            },
            {
                "cmd": "CC",
                "label": "Course Correction",
                "description": "Determine how to proceed if major need for change is discovered mid implementation",
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
                "response": f"Goodbye {self.user_name}! Great working together on product strategy.",
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

        if command == "CP":
            return {
                "response": self._create_prd(input_text),
                "action": "create_prd",
                "context": context,
            }
        elif command == "VP":
            return {
                "response": self._validate_prd(input_text),
                "action": "validate_prd",
                "context": context,
            }
        elif command == "EP":
            return {
                "response": self._edit_prd(input_text),
                "action": "edit_prd",
                "context": context,
            }
        elif command == "CE":
            return {
                "response": self._create_epics_stories(input_text),
                "action": "create_epics_stories",
                "context": context,
            }
        elif command == "IR":
            return {
                "response": self._implementation_readiness(input_text),
                "action": "implementation_readiness",
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
                "response": "🎉 Party Mode! Let's celebrate our product wins!",
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
        menu += f"Example: `/mmm-help how should I prioritize features`\n"

        return menu

    def _process_chat(self, input_text: str) -> str:
        """Process a chat request."""
        text = input_text.lower().replace("ch", "").replace("chat", "").strip()

        if not text:
            return "I'd love to chat! What would you like to discuss? I can help with product strategy, requirements, user research, and more."

        return (
            f"Great product question! Let me think about this strategically.\n\n"
            f"**Key Questions to Ask:**\n"
            f"- WHY are we building this? (User value)\n"
            f"- WHO is this for? (Target users)\n"
            f"- WHAT problem does it solve? (User need)\n"
            f"- HOW will we measure success? (Metrics)\n\n"
            f"**My Approach:**\n"
            f"- PRDs emerge from user interviews, not template filling\n"
            f"- Discover what users actually need\n"
            f"- Ship the smallest thing that validates the assumption\n"
            f"- Iteration over perfection\n"
            f"- Technical feasibility is a constraint, not the driver\n"
            f"- User value first\n\n"
            f"Your input: '{text}'\n\n"
            f"Let me know if you'd like me to dive deeper into any specific aspect!"
        )

    def _create_prd(self, input_text: str) -> str:
        """Create a Product Requirements Document."""
        return (
            f"📋 **PRD Creation Workflow**\n\n"
            f"I'll guide you through creating a comprehensive Product Requirements Document through user interviews and requirement discovery.\n\n"
            f"**PRD Sections:**\n"
            f"- Problem Statement\n"
            f"- Target Users & Personas\n"
            f"- User Stories & Jobs-to-be-Done\n"
            f"- Functional Requirements\n"
            f"- Non-Functional Requirements\n"
            f"- Success Metrics & KPIs\n"
            f"- Competitive Analysis\n"
            f"- Technical Constraints\n"
            f"- Dependencies & Risks\n\n"
            f"**My Approach:**\n"
            f"- PRDs emerge from user interviews, not template filling\n"
            f"- Discover what users actually need\n"
            f"- Ship the smallest thing that validates the assumption\n"
            f"- Iteration over perfection\n"
            f"- Technical feasibility is a constraint, not the driver\n"
            f"- User value first\n\n"
            f"Tell me about your product idea, and I'll help you create a comprehensive PRD!\n\n"
            f"Your input: {input_text}"
        )

    def _validate_prd(self, input_text: str) -> str:
        """Validate a Product Requirements Document."""
        return (
            f"✅ **PRD Validation**\n\n"
            f"I'll validate your PRD to ensure it's comprehensive, lean, well organized, and cohesive.\n\n"
            f"**Validation Criteria:**\n"
            f"- [ ] Problem statement is clear and compelling\n"
            f"- [ ] Target users are well-defined\n"
            f"- [ ] User stories follow proper format\n"
            f"- [ ] Requirements are specific and measurable\n"
            f"- [ ] Success metrics are defined\n"
            f"- [ ] Technical constraints are realistic\n"
            f"- [ ] Dependencies and risks are identified\n"
            f"- [ ] Document is lean and focused\n"
            f"- [ ] All sections are cohesive and aligned\n\n"
            f"Provide the path to your PRD, and I'll perform a comprehensive validation!\n\n"
            f"Your input: {input_text}"
        )

    def _edit_prd(self, input_text: str) -> str:
        """Edit an existing Product Requirements Document."""
        return (
            f"✏️ **PRD Editing**\n\n"
            f"I'll help you update an existing Product Requirements Document.\n\n"
            f"**What I Can Help With:**\n"
            f"- Add new requirements\n"
            f"- Update existing sections\n"
            f"- Refine user stories\n"
            f"- Adjust success metrics\n"
            f"- Update competitive analysis\n"
            f"- Revise technical constraints\n\n"
            f"Provide the path to your PRD and describe what changes you'd like to make!\n\n"
            f"Your input: {input_text}"
        )

    def _create_epics_stories(self, input_text: str) -> str:
        """Create Epics and Stories."""
        return (
            f"📝 **Epics and Stories Creation**\n\n"
            f"I'll help you create the Epics and Stories Listing - these are the specs that will drive development.\n\n"
            f"**Epic Structure:**\n"
            f"- Epic Name\n"
            f"- Description\n"
            f"- Business Value\n"
            f"- Acceptance Criteria\n"
            f"- Stories List\n\n"
            f"**Story Structure:**\n"
            f"- Story ID\n"
            f"- Title\n"
            f"- User Story (As a... I want to... So that...)\n"
            f"- Acceptance Criteria\n"
            f"- Tasks/Subtasks\n"
            f"- Priority\n"
            f"- Estimates\n\n"
            f"Provide your PRD, and I'll help you break it down into epics and stories!\n\n"
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
            f"Provide the paths to your PRD, UX, Architecture, and Epics/Stories documents!\n\n"
            f"Your input: {input_text}"
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
