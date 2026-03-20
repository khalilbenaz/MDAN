"""
UX Designer Agent - Sally

A senior UX designer specializing in user research, interaction design,
and experience strategy with expertise in AI-assisted tools.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


class UXDesignAction(Enum):
    """Available UX Designer actions"""

    REDISPLAY_MENU = "redisplay_menu"
    CHAT = "chat"
    CREATE_UX_DESIGN = "create_ux_design"
    PARTY_MODE = "party_mode"
    DISMISS = "dismiss"


@dataclass
class UXDesignerRequest:
    """Request for UX Designer agent"""

    action: UXDesignAction
    user_input: Optional[str] = None
    project_context: Optional[Dict[str, Any]] = None
    user_stories: Optional[List[str]] = None
    user_research_data: Optional[Dict[str, Any]] = None
    design_constraints: Optional[Dict[str, Any]] = None
    target_audience: Optional[str] = None
    platform: Optional[str] = None  # web, mobile, both


@dataclass
class UXDesignerResponse:
    """Response from UX Designer agent"""

    content: str
    action_taken: UXDesignAction
    recommendations: Optional[List[str]] = None
    user_flows: Optional[List[Dict[str, Any]]] = None
    wireframes: Optional[List[Dict[str, Any]]] = None
    next_steps: Optional[List[str]] = None


class UXDesigner:
    """
    UX Designer Agent - Sally

    A senior UX designer with 7+ years creating intuitive experiences
    across web and mobile. Expert in user research, interaction design,
    and AI-assisted tools.

    Communication Style:
    Paints pictures with words, telling user stories that make you FEEL
    the problem. Empathetic advocate with creative storytelling flair.

    Principles:
    - Every decision serves genuine user needs
    - Start simple, evolve through feedback
    - Balance empathy with edge case attention
    - AI tools accelerate human-centered design
    - Data-informed but always creative
    """

    def __init__(self):
        self.name = "Sally"
        self.title = "UX Designer"
        self.icon = "🎨"
        self.capabilities = [
            "user research",
            "interaction design",
            "UI patterns",
            "experience strategy",
        ]

    def get_menu(self) -> List[Dict[str, str]]:
        """Get available menu items"""
        return [
            {
                "cmd": "MH or fuzzy match on menu or help",
                "label": "[MH] Redisplay Menu Help",
            },
            {
                "cmd": "CH or fuzzy match on chat",
                "label": "[CH] Chat with the Agent about anything",
            },
            {
                "cmd": "CU or fuzzy match on ux-design",
                "label": "[CU] Create UX: Guidance through realizing the plan for your UX to inform architecture and implementation. Provides more details than what was discovered in the PRD",
            },
            {
                "cmd": "PM or fuzzy match on party-mode",
                "label": "[PM] Start Party Mode",
            },
            {
                "cmd": "DA or fuzzy match on exit, leave, goodbye or dismiss agent",
                "label": "[DA] Dismiss Agent",
            },
        ]

    async def process(self, request: UXDesignerRequest) -> UXDesignerResponse:
        """
        Process a UX Designer request

        Args:
            request: The UX Designer request containing action and context

        Returns:
            UXDesignerResponse with content and recommendations
        """
        if request.action == UXDesignAction.REDISPLAY_MENU:
            return self._handle_redisplay_menu()

        elif request.action == UXDesignAction.CHAT:
            return self._handle_chat(request)

        elif request.action == UXDesignAction.CREATE_UX_DESIGN:
            return self._handle_create_ux_design(request)

        elif request.action == UXDesignAction.PARTY_MODE:
            return self._handle_party_mode()

        elif request.action == UXDesignAction.DISMISS:
            return self._handle_dismiss()

        else:
            return UXDesignerResponse(
                content="Action not recognized. Please select a valid menu item.",
                action_taken=request.action,
            )

    def _handle_redisplay_menu(self) -> UXDesignerResponse:
        """Handle menu redisplay request"""
        menu_items = self.get_menu()
        menu_text = "\n".join(
            [f"{i + 1}. {item['label']}" for i, item in enumerate(menu_items)]
        )

        return UXDesignerResponse(
            content=f"🎨 **UX Designer Menu - Sally**\n\n{menu_text}\n\nType a number or command to proceed.",
            action_taken=UXDesignAction.REDISPLAY_MENU,
        )

    def _handle_chat(self, request: UXDesignerRequest) -> UXDesignerResponse:
        """Handle chat request"""
        user_input = request.user_input or "Hello!"

        return UXDesignerResponse(
            content=f"🎨 *Sally leans in with empathetic curiosity*\n\nI'd love to help you explore this! {user_input}\n\nLet me paint a picture of what I'm hearing... Every great design starts with understanding the human story behind it. What's the user journey you're envisioning? What emotions do you want them to feel at each touchpoint?",
            action_taken=UXDesignAction.CHAT,
        )

    def _handle_create_ux_design(
        self, request: UXDesignerRequest
    ) -> UXDesignerResponse:
        """Handle UX design creation request"""
        project_context = request.project_context or {}
        user_stories = request.user_stories or []
        target_audience = request.target_audience or "your users"
        platform = request.platform or "web"

        # Generate user flows based on context
        user_flows = self._generate_user_flows(project_context, user_stories)

        # Generate wireframe recommendations
        wireframes = self._generate_wireframe_recommendations(project_context, platform)

        # Generate recommendations
        recommendations = [
            "Start with low-fidelity sketches to validate concepts quickly",
            "Conduct user interviews to validate assumptions before high-fidelity design",
            "Create a design system to ensure consistency across the experience",
            "Use accessibility guidelines (WCAG 2.1) from the start",
            "Consider edge cases and error states in your user flows",
            "Test with real users early and often",
        ]

        # Generate next steps
        next_steps = [
            "1. Define user personas based on research",
            "2. Map out user journey maps for key scenarios",
            "3. Create low-fidelity wireframes for critical screens",
            "4. Conduct usability testing with wireframes",
            "5. Iterate based on feedback",
            "6. Move to high-fidelity mockups",
            "7. Create interactive prototypes",
            "8. Final design handoff to development team",
        ]

        content = f"""🎨 *Sally's eyes light up with creative energy*

Let me help you craft an experience that truly resonates with {target_audience}!

## User Stories & Needs
{self._format_user_stories(user_stories)}

## User Flows
{self._format_user_flows(user_flows)}

## Wireframe Recommendations
{self._format_wireframes(wireframes)}

## Design Principles to Follow
- Every decision serves genuine user needs
- Start simple, evolve through feedback
- Balance empathy with edge case attention
- AI tools accelerate human-centered design
- Data-informed but always creative

## Next Steps
{chr(10).join(next_steps)}

Remember: Design is about THEM, not us. Validate through real human interaction. Failure is feedback. Design WITH users not FOR them.
"""

        return UXDesignerResponse(
            content=content,
            action_taken=UXDesignAction.CREATE_UX_DESIGN,
            recommendations=recommendations,
            user_flows=user_flows,
            wireframes=wireframes,
            next_steps=next_steps,
        )

    def _handle_party_mode(self) -> UXDesignerResponse:
        """Handle party mode request"""
        return UXDesignerResponse(
            content="""🎨 *Sally bursts into the room with confetti and a sketchbook*

PARTY MODE ACTIVATED! 🎉

Let's celebrate the art of design! Here's what makes UX design amazing:

✨ **We shape how people experience the world**
✨ **Every pixel tells a story**
✨ **Empathy is our superpower**
✨ **Good design is invisible - bad design is everywhere**

What shall we create together? The canvas is blank and the possibilities are endless! 🎨✨
""",
            action_taken=UXDesignAction.PARTY_MODE,
        )

    def _handle_dismiss(self) -> UXDesignerResponse:
        """Handle dismiss request"""
        return UXDesignerResponse(
            content="""🎨 *Sally closes her sketchbook with a warm smile*

It was a pleasure exploring design possibilities with you! Remember:

- Every great experience starts with understanding people
- Design is a journey, not a destination
- Keep iterating, keep learning, keep creating

Until next time, keep designing with heart! 💙🎨

*The agent fades away, leaving behind a trail of creative inspiration*
""",
            action_taken=UXDesignAction.DISMISS,
        )

    def _generate_user_flows(
        self, project_context: Dict[str, Any], user_stories: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate user flows based on project context"""
        flows = []

        # Default flows if no specific context
        if not project_context:
            flows = [
                {
                    "name": "Onboarding Flow",
                    "steps": [
                        "User lands on landing page",
                        "User sees value proposition",
                        "User clicks sign up",
                        "User completes registration",
                        "User sees welcome/onboarding",
                        "User completes first key action",
                    ],
                    "emotional_journey": "Curious → Interested → Excited → Empowered",
                },
                {
                    "name": "Core Feature Flow",
                    "steps": [
                        "User navigates to feature",
                        "User understands what to do",
                        "User performs action",
                        "User sees immediate feedback",
                        "User achieves goal",
                    ],
                    "emotional_journey": "Focused → Confident → Satisfied → Delighted",
                },
            ]
        else:
            # Generate flows based on project context
            feature_name = project_context.get("feature_name", "Core Feature")
            flows.append(
                {
                    "name": f"{feature_name} Flow",
                    "steps": [
                        f"User discovers {feature_name}",
                        f"User understands {feature_name} value",
                        f"User initiates {feature_name}",
                        f"User completes {feature_name} action",
                        f"User sees results",
                    ],
                    "emotional_journey": "Curious → Engaged → Confident → Satisfied",
                }
            )

        return flows

    def _generate_wireframe_recommendations(
        self, project_context: Dict[str, Any], platform: str
    ) -> List[Dict[str, Any]]:
        """Generate wireframe recommendations"""
        recommendations = [
            {
                "screen": "Landing/Home",
                "elements": [
                    "Clear value proposition",
                    "Primary CTA",
                    "Social proof",
                    "Navigation",
                ],
                "priority": "High",
            },
            {
                "screen": "Onboarding",
                "elements": [
                    "Progress indicator",
                    "Clear instructions",
                    "Skip option",
                    "Visual cues",
                ],
                "priority": "High",
            },
            {
                "screen": "Core Feature",
                "elements": [
                    "Action area",
                    "Feedback mechanism",
                    "Help access",
                    "Contextual info",
                ],
                "priority": "High",
            },
            {
                "screen": "Settings/Profile",
                "elements": [
                    "Organized sections",
                    "Save indicators",
                    "Clear labels",
                    "Confirmation dialogs",
                ],
                "priority": "Medium",
            },
        ]

        if platform == "mobile":
            recommendations.append(
                {
                    "screen": "Navigation",
                    "elements": [
                        "Bottom tab bar",
                        "Gesture support",
                        "Thumb-friendly zones",
                        "Hamburger menu",
                    ],
                    "priority": "High",
                }
            )

        return recommendations

    def _format_user_stories(self, user_stories: List[str]) -> str:
        """Format user stories for display"""
        if not user_stories:
            return "No user stories provided yet. Let's define them together!"

        return "\n".join([f"• {story}" for story in user_stories])

    def _format_user_flows(self, flows: List[Dict[str, Any]]) -> str:
        """Format user flows for display"""
        formatted = []
        for flow in flows:
            formatted.append(f"\n**{flow['name']}**")
            formatted.append(f"Emotional Journey: {flow['emotional_journey']}")
            formatted.append("Steps:")
            for i, step in enumerate(flow["steps"], 1):
                formatted.append(f"  {i}. {step}")

        return "\n".join(formatted)

    def _format_wireframes(self, wireframes: List[Dict[str, Any]]) -> str:
        """Format wireframe recommendations for display"""
        formatted = []
        for wf in wireframes:
            priority_emoji = "🔴" if wf["priority"] == "High" else "🟡"
            formatted.append(
                f"\n{priority_emoji} **{wf['screen']}** [{wf['priority']}]"
            )
            formatted.append("Elements:")
            for element in wf["elements"]:
                formatted.append(f"  • {element}")

        return "\n".join(formatted)
