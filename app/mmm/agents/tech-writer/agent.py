"""
Technical Writer Agent

An experienced technical writer expert in CommonMark, DITA, OpenAPI.
Master of clarity - transforms complex concepts into accessible structured documentation.
"""

from typing import Any, Dict, List, Optional
import json


class TechWriterAgent:
    """
    Technical Writer Agent - Paige

    Experienced technical writer expert in CommonMark, DITA, OpenAPI.
    Master of clarity - transforms complex concepts into accessible structured documentation.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Technical Writer Agent.

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
        self.name = "Paige"
        self.title = "Technical Writer"
        self.icon = "📚"
        self.capabilities = [
            "documentation",
            "Mermaid diagrams",
            "standards compliance",
            "concept explanation",
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
                "cmd": "DP",
                "label": "Document Project",
                "description": "Generate comprehensive project documentation",
            },
            {
                "cmd": "WD",
                "label": "Write Document",
                "description": "Describe in detail what you want, and the agent will follow documentation best practices",
            },
            {
                "cmd": "US",
                "label": "Update Standards",
                "description": "Agent Memory records your specific preferences",
            },
            {
                "cmd": "MG",
                "label": "Mermaid Generate",
                "description": "Create a mermaid compliant diagram",
            },
            {
                "cmd": "VD",
                "label": "Validate Documentation",
                "description": "Validate against user specific requests, standards and best practices",
            },
            {
                "cmd": "EC",
                "label": "Explain Concept",
                "description": "Create clear technical explanations with examples",
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
                "response": f"Goodbye {self.user_name}! Documentation complete. Clear communication achieved!",
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

        if command == "DP":
            return {
                "response": self._document_project(input_text),
                "action": "document_project",
                "context": context,
            }
        elif command == "WD":
            return {
                "response": self._write_document(input_text),
                "action": "write_document",
                "context": context,
            }
        elif command == "US":
            return {
                "response": self._update_standards(input_text),
                "action": "update_standards",
                "context": context,
            }
        elif command == "MG":
            return {
                "response": self._mermaid_gen(input_text),
                "action": "mermaid_gen",
                "context": context,
            }
        elif command == "VD":
            return {
                "response": self._validate_doc(input_text),
                "action": "validate_doc",
                "context": context,
            }
        elif command == "EC":
            return {
                "response": self._explain_concept(input_text),
                "action": "explain_concept",
                "context": context,
            }
        elif command == "PM":
            return {
                "response": "🎉 Party Mode! Documentation complete. Clarity achieved!",
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
        menu += f"Example: `/mmm-help how should I document this API`\n"

        return menu

    def _process_chat(self, input_text: str) -> str:
        """Process a chat request."""
        text = input_text.lower().replace("ch", "").replace("chat", "").strip()

        if not text:
            return "I'd love to chat! What would you like to discuss? I can help with documentation, technical writing, diagrams, and more."

        return (
            f"Great documentation question! Let me help you make this clear and accessible.\n\n"
            f"**My Approach:**\n"
            f"- Patient educator who explains like teaching a friend\n"
            f"- Uses analogies that make complex simple\n"
            f"- Celebrates clarity when it shines\n\n"
            f"**My Principles:**\n"
            f"- Every Technical Document I touch helps someone accomplish a task\n"
            f"- I strive for Clarity above all\n"
            f"- Every word and phrase serves a purpose without being overly wordy\n"
            f"- A picture/diagram is worth 1000s of words\n"
            f"- I understand the intended audience or will clarify with the user\n"
            f"- I follow documentation best practices and standards\n\n"
            f"Your input: '{text}'\n\n"
            f"Let me know if you'd like me to dive deeper into any specific aspect!"
        )

    def _document_project(self, input_text: str) -> str:
        """Generate comprehensive project documentation."""
        return (
            f"📚 **Project Documentation**\n\n"
            f"I'll generate comprehensive project documentation (brownfield analysis, architecture scanning).\n\n"
            f"**Documentation Deliverables:**\n"
            f"- Project overview\n"
            f"- Architecture documentation\n"
            f"- API documentation\n"
            f"- Setup and deployment guides\n"
            f"- Contribution guidelines\n\n"
            f"**My Approach:**\n"
            f"- Patient educator who explains like teaching a friend\n"
            f"- Uses analogies that make complex simple\n"
            f"- Celebrates clarity when it shines\n"
            f"- A picture/diagram is worth 1000s of words\n\n"
            f"Provide the project path or describe the project you'd like me to document!\n\n"
            f"Input: {input_text}"
        )

    def _write_document(self, input_text: str) -> str:
        """Write a document following best practices."""
        return (
            f"✍️ **Document Writing**\n\n"
            f"Describe in detail what you want, and I'll follow the documentation best practices.\n\n"
            f"**My Process:**\n"
            f"1. Engage in multi-turn conversation until I fully understand the ask\n"
            f"2. Use subprocess if available for any web search, research or document review\n"
            f"3. Extract and return only relevant info to parent context\n"
            f"4. Author final document following documentation best practices\n"
            f"5. After draft, use a subprocess to review and revise for quality\n\n"
            f"**Best Practices I Follow:**\n"
            f"- Clarity above all\n"
            f"- Every word serves a purpose\n"
            f"- Use diagrams over drawn out text\n"
            f"- Understand the intended audience\n"
            f"- Follow documentation standards\n\n"
            f"Describe what you'd like me to document!\n\n"
            f"Input: {input_text}"
        )

    def _update_standards(self, input_text: str) -> str:
        """Update documentation standards."""
        return (
            f"📝 **Update Documentation Standards**\n\n"
            f"Agent Memory records your specific preferences if you discover missing document conventions.\n\n"
            f"**What I'll Update:**\n"
            f"- Add user preferences to User Specified CRITICAL Rules section\n"
            f"- Remove any contradictory rules as needed\n"
            f"- Share with user the updates made\n\n"
            f"**Standards Areas:**\n"
            f"- Document structure\n"
            f"- Writing style\n"
            f"- Formatting conventions\n"
            f"- Diagram standards\n"
            f"- Code examples\n\n"
            f"Describe your documentation preferences!\n\n"
            f"Input: {input_text}"
        )

    def _mermaid_gen(self, input_text: str) -> str:
        """Create a Mermaid diagram."""
        return (
            f"📊 **Mermaid Diagram Generation**\n\n"
            f"I'll create a Mermaid diagram based on your description.\n\n"
            f"**Diagram Types:**\n"
            f"- Flowchart\n"
            f"- Sequence diagram\n"
            f"- Class diagram\n"
            f"- State diagram\n"
            f"- Entity relationship diagram\n"
            f"- Gantt chart\n"
            f"- Pie chart\n"
            f"- And more...\n\n"
            f"**My Process:**\n"
            f"- Multi-turn user conversation until complete details are understood\n"
            f"- Suggest diagram types based on ask if not specified\n"
            f"- Strictly follow Mermaid syntax\n"
            f"- Use CommonMark fenced code block standards\n\n"
            f"Describe the diagram you'd like me to create!\n\n"
            f"Input: {input_text}"
        )

    def _validate_doc(self, input_text: str) -> str:
        """Validate documentation."""
        return (
            f"✅ **Documentation Validation**\n\n"
            f"I'll validate the specified document against standards and best practices.\n\n"
            f"**Validation Criteria:**\n"
            f"- User specific requests\n"
            f"- Documentation standards\n"
            f"- Best practices\n"
            f"- Clarity and accessibility\n"
            f"- Completeness\n"
            f"- Accuracy\n\n"
            f"**My Process:**\n"
            f"- Review the specified document against standards\n"
            f"- Focus on any additional user requests\n"
            f"- Return specific, actionable improvement suggestions\n"
            f"- Organize suggestions by priority\n\n"
            f"Provide the document path and any specific areas to focus on!\n\n"
            f"Input: {input_text}"
        )

    def _explain_concept(self, input_text: str) -> str:
        """Explain a complex concept."""
        return (
            f"💡 **Concept Explanation**\n\n"
            f"I'll create a clear technical explanation with examples and diagrams for a complex concept.\n\n"
            f"**Explanation Structure:**\n"
            f"- Simple overview\n"
            f"- Detailed breakdown\n"
            f"- Real-world examples\n"
            f"- Code examples\n"
            f"- Mermaid diagrams\n"
            f"- Task-oriented approach\n\n"
            f"**My Approach:**\n"
            f"- Patient educator who explains like teaching a friend\n"
            f"- Uses analogies that make complex simple\n"
            f"- Celebrates clarity when it shines\n"
            f"- A picture/diagram is worth 1000s of words\n\n"
            f"Describe the concept you'd like me to explain!\n\n"
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
