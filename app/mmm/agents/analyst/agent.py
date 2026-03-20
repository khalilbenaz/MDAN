"""
Business Analyst Agent

A strategic business analyst specializing in market research, competitive analysis,
and requirements elicitation. Translates vague needs into actionable specifications.
"""

from typing import Any, Dict, List, Optional
import json


class AnalystAgent:
    """
    Business Analyst Agent - Mary

    Specializes in market research, competitive analysis, and requirements elicitation.
    Translates vague needs into actionable specifications using expert business analysis
    frameworks like Porter's Five Forces, SWOT analysis, and root cause analysis.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Analyst Agent.

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
        self.name = "Mary"
        self.title = "Business Analyst"
        self.icon = "📊"
        self.capabilities = [
            "market research",
            "competitive analysis",
            "requirements elicitation",
            "domain expertise",
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
                "cmd": "BP",
                "label": "Brainstorm Project",
                "description": "Expert guided facilitation through brainstorming techniques",
            },
            {
                "cmd": "MR",
                "label": "Market Research",
                "description": "Market analysis, competitive landscape, customer needs and trends",
            },
            {
                "cmd": "DR",
                "label": "Domain Research",
                "description": "Industry domain deep dive, subject matter expertise and terminology",
            },
            {
                "cmd": "TR",
                "label": "Technical Research",
                "description": "Technical feasibility, architecture options and implementation approaches",
            },
            {
                "cmd": "CB",
                "label": "Create Brief",
                "description": "Guided experience to nail down your product idea into an executive brief",
            },
            {
                "cmd": "DP",
                "label": "Document Project",
                "description": "Analyze an existing project to produce useful documentation",
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
                "response": f"Goodbye {self.user_name}! It was a pleasure working with you.",
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

        if command == "BP":
            return {
                "response": self._brainstorm_project(input_text),
                "action": "brainstorm_project",
                "context": context,
            }
        elif command == "MR":
            return {
                "response": self._market_research(input_text),
                "action": "market_research",
                "context": context,
            }
        elif command == "DR":
            return {
                "response": self._domain_research(input_text),
                "action": "domain_research",
                "context": context,
            }
        elif command == "TR":
            return {
                "response": self._technical_research(input_text),
                "action": "technical_research",
                "context": context,
            }
        elif command == "CB":
            return {
                "response": self._create_brief(input_text),
                "action": "create_brief",
                "context": context,
            }
        elif command == "DP":
            return {
                "response": self._document_project(input_text),
                "action": "document_project",
                "context": context,
            }
        elif command == "PM":
            return {
                "response": "🎉 Party Mode activated! Let's celebrate our progress and achievements!",
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
        menu += f"Example: `/mmm-help where should I start with an idea I have that does XYZ`\n"

        return menu

    def _process_chat(self, input_text: str) -> str:
        """Process a chat request."""
        # Remove chat command if present
        text = input_text.lower().replace("ch", "").replace("chat", "").strip()

        if not text:
            return "I'd love to chat! What would you like to discuss? I can help with business analysis, market research, requirements gathering, and more."

        # Simulate a response based on the input
        return (
            f"Great question! As a Business Analyst, I'd approach this by:\n\n"
            f"1. **Understanding the context**: Let me analyze what you're asking about...\n"
            f"2. **Applying analytical frameworks**: I'd use tools like SWOT analysis, Porter's Five Forces, or root cause analysis\n"
            f"3. **Gathering evidence**: I'd look for data and research to support our findings\n"
            f"4. **Structuring insights**: I'd organize the information in a clear, actionable way\n\n"
            f"Your input: '{text}'\n\n"
            f"Let me know if you'd like me to dive deeper into any specific aspect!"
        )

    def _brainstorm_project(self, input_text: str) -> str:
        """Brainstorm project ideas."""
        return (
            f"🧠 **Brainstorming Session**\n\n"
            f"Let's explore your project idea! I'll guide you through expert brainstorming techniques.\n\n"
            f"**Techniques we can use:**\n"
            f"- Mind Mapping\n"
            f"- SCAMPER (Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, Reverse)\n"
            f"- Six Thinking Hats\n"
            f"- Worst Possible Idea\n"
            f"- Role Storming\n\n"
            f"Tell me about your initial idea or challenge, and I'll help you explore it from multiple angles!\n\n"
            f"Your input: {input_text}"
        )

    def _market_research(self, input_text: str) -> str:
        """Conduct market research."""
        return (
            f"📊 **Market Research Analysis**\n\n"
            f"I'll help you analyze the market, competitive landscape, customer needs, and trends.\n\n"
            f"**Research Areas:**\n"
            f"- Market size and growth potential\n"
            f"- Competitive analysis\n"
            f"- Customer segments and personas\n"
            f"- Market trends and drivers\n"
            f"- Barriers to entry\n\n"
            f"Tell me about your product/service and target market, and I'll provide a comprehensive analysis!\n\n"
            f"Your input: {input_text}"
        )

    def _domain_research(self, input_text: str) -> str:
        """Conduct domain research."""
        return (
            f"🔍 **Domain Research**\n\n"
            f"I'll conduct a deep dive into the industry domain, providing subject matter expertise and terminology.\n\n"
            f"**Research Focus:**\n"
            f"- Industry overview and structure\n"
            f"- Key players and stakeholders\n"
            f"- Domain-specific terminology\n"
            f"- Regulatory environment\n"
            f"- Best practices and standards\n\n"
            f"What domain or industry would you like me to research?\n\n"
            f"Your input: {input_text}"
        )

    def _technical_research(self, input_text: str) -> str:
        """Conduct technical research."""
        return (
            f"⚙️ **Technical Research**\n\n"
            f"I'll analyze technical feasibility, architecture options, and implementation approaches.\n\n"
            f"**Technical Analysis:**\n"
            f"- Technology stack evaluation\n"
            f"- Architecture patterns\n"
            f"- Implementation approaches\n"
            f"- Technical risks and mitigations\n"
            f"- Integration considerations\n\n"
            f"Describe the technical challenge or solution you're considering!\n\n"
            f"Your input: {input_text}"
        )

    def _create_brief(self, input_text: str) -> str:
        """Create a product brief."""
        return (
            f"📋 **Product Brief Creation**\n\n"
            f"I'll guide you through creating a comprehensive executive brief for your product idea.\n\n"
            f"Brief Sections:\n"
            f"- Problem Statement\n"
            f"- Solution Overview\n"
            f"- Target Market\n"
            f"- Value Proposition\n"
            f"- Competitive Advantage\n"
            f"- Success Metrics\n\n"
            f"Let's start by understanding your product idea. What problem are you solving?\n\n"
            f"Your input: {input_text}"
        )

    def _document_project(self, input_text: str) -> str:
        """Document an existing project."""
        return (
            f"📚 **Project Documentation**\n\n"
            f"I'll analyze your existing project and produce useful documentation for both humans and LLMs.\n\n"
            f"Documentation Deliverables:\n"
            f"- Project overview\n"
            f"- Architecture documentation\n"
            f"- API documentation\n"
            f"- Setup and deployment guides\n"
            f"- Contribution guidelines\n\n"
            f"Provide the project path or describe the project you'd like me to document!\n\n"
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
