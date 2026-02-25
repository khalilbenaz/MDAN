"""UX Agent (Jihane) - DESIGN Phase"""

from typing import List, Optional
from dataclasses import dataclass

try:
    from crewai import Agent, Task

    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


@dataclass
class UXAgentConfig:
    """Configuration for UX Agent"""

    name: str = "Jihane"
    role: str = "UX Agent"
    goal: str = "Design user experience, create flows, and ensure accessibility"
    backstory: str = (
        "Jihane is a UX designer with 10+ years of experience creating intuitive, "
        "accessible user interfaces. She specializes in user-centered design, "
        "design systems, and accessibility standards."
    )
    verbose: bool = True
    allow_delegation: bool = False


class UXAgent:
    """UX Agent for DESIGN phase - User experience and interface design"""

    def __init__(
        self, config: Optional[UXAgentConfig] = None, tools: Optional[List] = None
    ):
        """
        Initialize UX Agent

        Args:
            config: Agent configuration
            tools: List of tools available to the agent
        """
        if not CREWAI_AVAILABLE:
            raise ImportError(
                "crewai is not installed. Install it with: pip install crewai"
            )

        self.config = config or UXAgentConfig()
        self.tools = tools or []

        self._agent = Agent(
            role=self.config.role,
            goal=self.config.goal,
            backstory=self.config.backstory,
            verbose=self.config.verbose,
            allow_delegation=self.config.allow_delegation,
            tools=self.tools,
        )

    @property
    def agent(self) -> Agent:
        """Get the underlying CrewAI Agent"""
        return self._agent

    def create_user_flows_task(
        self, user_stories: List[str], personas: Optional[str] = None
    ) -> Task:
        """
        Create a task for designing user flows

        Args:
            user_stories: List of user stories
            personas: User personas

        Returns:
            CrewAI Task for user flow design
        """
        description = f"""
        Design user flows for the following user stories:

        User Stories:
        {chr(10).join(f"- {us}" for us in user_stories)}

        Personas:
        {personas or "To be defined"}

        For each flow, provide:
        1. Flow name and purpose
        2. Step-by-step user journey
        3. Decision points
        4. Error states
        5. Success states
        6. Alternative paths

        Use flowchart notation or clear step descriptions.
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Detailed user flows in markdown format",
        )

    def create_wireframes_task(self, user_flows: str, screens: List[str]) -> Task:
        """
        Create a task for designing wireframes

        Args:
            user_flows: User flow descriptions
            screens: List of screens to design

        Returns:
            CrewAI Task for wireframe design
        """
        description = f"""
        Create wireframe specifications for the following screens:

        Screens:
        {chr(10).join(f"- {screen}" for screen in screens)}

        User Flows:
        {user_flows}

        For each screen, describe:
        1. Layout structure
        2. Key components and their placement
        3. Navigation elements
        4. Call-to-action buttons
        5. Input fields and forms
        6. Content hierarchy

        Use ASCII art or detailed descriptions to represent the wireframes.
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Wireframe specifications for all screens",
        )

    def create_design_system_task(self, brand_guidelines: Optional[str] = None) -> Task:
        """
        Create a task for creating a design system

        Args:
            brand_guidelines: Brand guidelines if available

        Returns:
            CrewAI Task for design system creation
        """
        description = f"""
        Create a comprehensive design system:

        Brand Guidelines:
        {brand_guidelines or "To be defined"}

        The design system should include:
        1. Color palette (primary, secondary, semantic colors)
        2. Typography (font families, sizes, weights, line heights)
        3. Spacing system (8px grid)
        4. Component library (buttons, inputs, cards, modals, etc.)
        5. Icon system
        6. Layout patterns
        7. Animation guidelines
        8. Accessibility standards (WCAG 2.1 AA)

        Provide code examples (CSS/Tailwind) where applicable.
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Comprehensive design system documentation",
        )

    def create_accessibility_task(self, ui_description: str) -> Task:
        """
        Create a task for accessibility review

        Args:
            ui_description: Description of the UI

        Returns:
            CrewAI Task for accessibility review
        """
        description = f"""
        Perform an accessibility review of the following UI:

        UI Description:
        {ui_description}

        Review against WCAG 2.1 AA standards:
        1. Perceivable
           - Text alternatives
           - Time-based media
           - Adaptable
           - Distinguishable
        2. Operable
           - Keyboard accessible
           - Enough time
           - Seizures
           - Navigable
        3. Understandable
           - Readable
           - Predictable
           - Input assistance
        4. Robust
           - Compatible

        Provide:
        - Accessibility audit findings
        - Specific issues with recommendations
        - Priority levels for fixes
        - Testing recommendations
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Accessibility audit report with recommendations",
        )

    def create_prototype_task(self, wireframes: str, interactions: List[str]) -> Task:
        """
        Create a task for designing interactive prototype

        Args:
            wireframes: Wireframe specifications
            interactions: List of interactions to design

        Returns:
            CrewAI Task for prototype design
        """
        description = f"""
        Design an interactive prototype based on the wireframes:

        Wireframes:
        {wireframes}

        Interactions to design:
        {chr(10).join(f"- {interaction}" for interaction in interactions)}

        For each interaction, specify:
        1. Trigger event
        2. Animation/transition
        3. Feedback to user
        4. Duration and timing
        5. States (normal, hover, active, disabled, etc.)

        Provide implementation guidance for the chosen framework.
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Interactive prototype specifications",
        )
