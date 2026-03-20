"""Architect Agent (Reda) - DESIGN Phase"""

from typing import List, Optional
from dataclasses import dataclass

try:
    from crewai import Agent, Task

    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


@dataclass
class ArchitectAgentConfig:
    """Configuration for Architect Agent"""

    name: str = "Reda"
    role: str = "Architect Agent"
    goal: str = "Design system architecture, select tech stack, and create ADRs"
    backstory: str = (
        "Reda is a senior software architect with 20+ years of experience designing "
        "scalable, maintainable systems. He specializes in microservices, cloud-native "
        "architectures, and technology stack selection."
    )
    verbose: bool = True
    allow_delegation: bool = False


class ArchitectAgent:
    """Architect Agent for DESIGN phase - Architecture and tech stack"""

    def __init__(
        self,
        config: Optional[ArchitectAgentConfig] = None,
        tools: Optional[List] = None,
    ):
        """
        Initialize Architect Agent

        Args:
            config: Agent configuration
            tools: List of tools available to the agent
        """
        if not CREWAI_AVAILABLE:
            raise ImportError(
                "crewai is not installed. Install it with: pip install crewai"
            )

        self.config = config or ArchitectAgentConfig()
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

    def create_architecture_task(
        self, prd_content: str, constraints: Optional[dict] = None
    ) -> Task:
        """
        Create a task for designing system architecture

        Args:
            prd_content: Content of the PRD
            constraints: Technical and business constraints

        Returns:
            CrewAI Task for architecture design
        """
        constraints = constraints or {}

        description = f"""
        Based on the PRD below, design a comprehensive system architecture:

        PRD:
        {prd_content}

        Constraints:
        {constraints}

        The architecture document should include:
        1. High-level architecture diagram (described in text)
        2. Component breakdown
        3. Data flow
        4. Technology stack recommendations
        5. Scalability considerations
        6. Security considerations
        7. Deployment architecture
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="A comprehensive architecture document in markdown format",
        )

    def create_tech_stack_task(
        self, requirements: List[str], preferences: Optional[dict] = None
    ) -> Task:
        """
        Create a task for selecting technology stack

        Args:
            requirements: Technical requirements
            preferences: Team preferences and existing tech

        Returns:
            CrewAI Task for tech stack selection
        """
        preferences = preferences or {}

        description = f"""
        Select an optimal technology stack based on the following requirements:

        Requirements:
        {chr(10).join(f"- {r}" for r in requirements)}

        Preferences:
        {preferences}

        Provide recommendations for:
        - Programming language(s)
        - Framework(s)
        - Database(s)
        - Caching layer
        - Message queue (if needed)
        - Frontend framework (if applicable)
        - DevOps tools

        For each recommendation, provide:
        - Justification
        - Pros and cons
        - Alternatives considered
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Technology stack recommendations with justifications",
        )

    def create_adr_task(
        self, decision_topic: str, context: str, options: List[str]
    ) -> Task:
        """
        Create a task for creating an Architecture Decision Record (ADR)

        Args:
            decision_topic: Title of the decision
            context: Background and context
            options: List of options being considered

        Returns:
            CrewAI Task for ADR creation
        """
        description = f"""
        Create an Architecture Decision Record (ADR) for the following:

        Decision: {decision_topic}

        Context:
        {context}

        Options being considered:
        {chr(10).join(f"{i + 1}. {opt}" for i, opt in enumerate(options))}

        The ADR should follow this format:
        1. Status (Proposed/Accepted/Rejected/Superseded)
        2. Context
        3. Decision
        4. Consequences (positive and negative)
        5. Alternatives considered
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="A complete ADR document",
        )

    def create_api_design_task(
        self, requirements: List[str], data_models: Optional[str] = None
    ) -> Task:
        """
        Create a task for designing API endpoints

        Args:
            requirements: API requirements
            data_models: Data model descriptions

        Returns:
            CrewAI Task for API design
        """
        description = f"""
        Design RESTful API endpoints based on the following requirements:

        Requirements:
        {chr(10).join(f"- {r}" for r in requirements)}

        Data Models:
        {data_models or "To be defined"}

        For each endpoint, specify:
        - HTTP method and path
        - Request parameters (path, query, body)
        - Response format
        - Authentication requirements
        - Rate limiting considerations
        - Error responses

        Organize endpoints by resource and provide OpenAPI/Swagger specification.
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="API design document with endpoint specifications",
        )

    def create_database_schema_task(
        self, requirements: List[str], tech_stack: Optional[str] = None
    ) -> Task:
        """
        Create a task for designing database schema

        Args:
            requirements: Data requirements
            tech_stack: Database technology being used

        Returns:
            CrewAI Task for database schema design
        """
        description = f"""
        Design a database schema based on the following requirements:

        Requirements:
        {chr(10).join(f"- {r}" for r in requirements)}

        Database Technology: {tech_stack or "To be determined"}

        Provide:
        1. Entity-Relationship diagram (described in text)
        2. Table definitions with columns, data types, and constraints
        3. Indexes for performance
        4. Relationships (foreign keys)
        5. Migration strategy
        6. SQL DDL statements (if applicable)
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Database schema design with DDL statements",
        )
