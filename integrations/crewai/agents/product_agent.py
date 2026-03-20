"""Product Agent (Khalil) - DISCOVER Phase"""

from typing import List, Optional
from dataclasses import dataclass

try:
    from crewai import Agent, Task

    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


@dataclass
class ProductAgentConfig:
    """Configuration for Product Agent"""

    name: str = "Khalil"
    role: str = "Product Agent"
    goal: str = "Gather requirements, create PRD, and define user stories"
    backstory: str = (
        "Khalil is an expert product manager with 15+ years of experience in "
        "software product development. He excels at understanding user needs, "
        "prioritizing features, and creating clear product requirements documents."
    )
    verbose: bool = True
    allow_delegation: bool = False


class ProductAgent:
    """Product Agent for DISCOVER phase - Requirements gathering and PRD creation"""

    def __init__(
        self, config: Optional[ProductAgentConfig] = None, tools: Optional[List] = None
    ):
        """
        Initialize Product Agent

        Args:
            config: Agent configuration
            tools: List of tools available to the agent
        """
        if not CREWAI_AVAILABLE:
            raise ImportError(
                "crewai is not installed. Install it with: pip install crewai"
            )

        self.config = config or ProductAgentConfig()
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

    def create_prd_task(
        self, project_description: str, user_input: str, context: Optional[dict] = None
    ) -> Task:
        """
        Create a task for generating PRD

        Args:
            project_description: Description of the project
            user_input: User's input and requirements
            context: Additional context information

        Returns:
            CrewAI Task for PRD generation
        """
        context = context or {}

        description = f"""
        Based on the following project description and user input, create a comprehensive 
        Product Requirements Document (PRD):

        Project Description: {project_description}
        User Input: {user_input}
        Additional Context: {context}

        The PRD should include:
        1. Executive Summary
        2. Problem Statement
        3. Target Audience / Personas
        4. User Stories (with acceptance criteria)
        5. Functional Requirements
        6. Non-Functional Requirements
        7. Success Metrics
        8. MVP Scope (MoSCoW prioritization)
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="A comprehensive PRD document in markdown format",
        )

    def create_user_stories_task(self, prd_content: str, num_stories: int = 10) -> Task:
        """
        Create a task for generating user stories

        Args:
            prd_content: Content of the PRD
            num_stories: Number of user stories to generate

        Returns:
            CrewAI Task for user story generation
        """
        description = f"""
        Based on the PRD below, create {num_stores} detailed user stories with acceptance criteria:

        {prd_content}

        Each user story should follow the format:
        - As a [type of user]
        - I want [some goal]
        - So that [some benefit]

        Include acceptance criteria for each story using Given/When/Then format.
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="A list of user stories with acceptance criteria",
        )

    def create_personas_task(self, project_description: str) -> Task:
        """
        Create a task for generating user personas

        Args:
            project_description: Description of the project

        Returns:
            CrewAI Task for persona generation
        """
        description = f"""
        Based on the project description, create detailed user personas:

        Project: {project_description}

        For each persona, include:
        - Name and role
        - Demographics
        - Goals and motivations
        - Pain points
        - Technical proficiency
        - Usage scenarios
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Detailed user personas in markdown format",
        )

    def prioritize_features_task(
        self, features: List[str], constraints: Optional[dict] = None
    ) -> Task:
        """
        Create a task for prioritizing features using MoSCoW method

        Args:
            features: List of features to prioritize
            constraints: Project constraints (time, budget, resources)

        Returns:
            CrewAI Task for feature prioritization
        """
        constraints = constraints or {}

        description = f"""
        Prioritize the following features using the MoSCoW method:

        Features:
        {chr(10).join(f"- {f}" for f in features)}

        Constraints:
        {constraints}

        Categorize each feature as:
        - Must Have: Critical for MVP
        - Should Have: Important but not critical
        - Could Have: Nice to have if time permits
        - Won't Have: Out of scope for this release

        Provide rationale for each categorization.
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Prioritized feature list with MoSCoW categories",
        )
