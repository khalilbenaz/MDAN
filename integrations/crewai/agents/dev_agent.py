"""Dev Agent (Haytame) - BUILD Phase"""

from typing import List, Optional
from dataclasses import dataclass

try:
    from crewai import Agent, Task

    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


@dataclass
class DevAgentConfig:
    """Configuration for Dev Agent"""

    name: str = "Haytame"
    role: str = "Dev Agent"
    goal: str = "Implement features, write clean code, and ensure quality"
    backstory: str = (
        "Haytame is a senior software engineer with 12+ years of experience in "
        "full-stack development. He writes clean, maintainable code and follows "
        "best practices for testing, documentation, and code review."
    )
    verbose: bool = True
    allow_delegation: bool = False


class DevAgent:
    """Dev Agent for BUILD phase - Implementation and coding"""

    def __init__(
        self, config: Optional[DevAgentConfig] = None, tools: Optional[List] = None
    ):
        """
        Initialize Dev Agent

        Args:
            config: Agent configuration
            tools: List of tools available to the agent
        """
        if not CREWAI_AVAILABLE:
            raise ImportError(
                "crewai is not installed. Install it with: pip install crewai"
            )

        self.config = config or DevAgentConfig()
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

    def create_implementation_task(
        self,
        user_story: str,
        acceptance_criteria: List[str],
        tech_stack: Optional[dict] = None,
    ) -> Task:
        """
        Create a task for implementing a user story

        Args:
            user_story: User story to implement
            acceptance_criteria: List of acceptance criteria
            tech_stack: Technology stack being used

        Returns:
            CrewAI Task for implementation
        """
        tech_stack = tech_stack or {}

        description = f"""
        Implement the following user story:

        User Story: {user_story}

        Acceptance Criteria:
        {chr(10).join(f"- {ac}" for ac in acceptance_criteria)}

        Technology Stack:
        {tech_stack}

        Provide:
        1. Implementation plan
        2. Code for the feature (following best practices)
        3. Unit tests
        4. Integration points
        5. Any configuration changes needed

        Ensure code is:
        - Clean and readable
        - Well-documented
        - Following SOLID principles
        - Type-hinted (if applicable)
        - Error-handled appropriately
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Complete implementation with code and tests",
        )

    def create_refactoring_task(self, code_content: str, issues: List[str]) -> Task:
        """
        Create a task for refactoring code

        Args:
            code_content: Code to refactor
            issues: List of issues to address

        Returns:
            CrewAI Task for refactoring
        """
        description = f"""
        Refactor the following code to address these issues:

        Issues to address:
        {chr(10).join(f"- {issue}" for issue in issues)}

        Code:
        {code_content}

        Provide:
        1. Refactored code
        2. Explanation of changes
        3. Tests to verify the refactoring
        4. Any performance improvements
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Refactored code with explanations",
        )

    def create_code_review_task(
        self, code_content: str, context: Optional[str] = None
    ) -> Task:
        """
        Create a task for code review

        Args:
            code_content: Code to review
            context: Context about the code

        Returns:
            CrewAI Task for code review
        """
        description = f"""
        Perform a thorough code review:

        Context:
        {context or "No additional context provided"}

        Code:
        {code_content}

        Review for:
        1. Code quality and readability
        2. Potential bugs
        3. Security vulnerabilities
        4. Performance issues
        5. Best practices adherence
        6. Test coverage
        7. Documentation

        Provide:
        - Overall assessment
        - Specific issues found (with line references if possible)
        - Suggestions for improvement
        - Approval status (Approved/Request Changes)
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Detailed code review with findings and recommendations",
        )

    def create_test_task(self, code_content: str, requirements: List[str]) -> Task:
        """
        Create a task for writing tests

        Args:
            code_content: Code to test
            requirements: Test requirements

        Returns:
            CrewAI Task for test writing
        """
        description = f"""
        Write comprehensive tests for the following code:

        Code:
        {code_content}

        Test Requirements:
        {chr(10).join(f"- {req}" for req in requirements)}

        Provide:
        1. Unit tests
        2. Integration tests (if applicable)
        3. Edge case tests
        4. Mock implementations (if needed)
        5. Test documentation

        Ensure tests are:
        - Clear and maintainable
        - Following Arrange-Act-Assert pattern
        - Well-named and descriptive
        - Independent of each other
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Comprehensive test suite",
        )

    def create_debugging_task(
        self, error_message: str, code_content: str, context: Optional[str] = None
    ) -> Task:
        """
        Create a task for debugging

        Args:
            error_message: Error message or stack trace
            code_content: Code with the bug
            context: Additional context

        Returns:
            CrewAI Task for debugging
        """
        description = f"""
        Debug the following issue:

        Error:
        {error_message}

        Context:
        {context or "No additional context provided"}

        Code:
        {code_content}

        Provide:
        1. Root cause analysis
        2. Fixed code
        3. Explanation of the fix
        4. Tests to prevent regression
        5. Suggestions for preventing similar issues
        """

        return Task(
            description=description,
            agent=self._agent,
            expected_output="Bug fix with explanation and tests",
        )
