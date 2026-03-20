"""Documentation Agent (Amina) - SHIP Phase

Responsible for documentation, user guides, and technical writing.
"""

from crewai import Agent, Task
from typing import List, Optional
from ..tools.sql_tool import SQLTool
from ..tools.serper_tool import SerperTool
from ..tools.file_tool import FileTool


class DocAgent:
    """Documentation Agent for SHIP phase - Documentation and technical writing."""

    def __init__(
        self,
        sql_tool: Optional[SQLTool] = None,
        serper_tool: Optional[SerperTool] = None,
        file_tool: Optional[FileTool] = None,
        llm=None,
    ):
        """Initialize Documentation Agent.

        Args:
            sql_tool: SQL connector tool
            serper_tool: Web search tool
            file_tool: File operations tool
            llm: Language model instance
        """
        self.sql_tool = sql_tool
        self.serper_tool = serper_tool
        self.file_tool = file_tool
        self.llm = llm

        tools = []
        if sql_tool:
            tools.append(sql_tool)
        if serper_tool:
            tools.append(serper_tool)
        if file_tool:
            tools.append(file_tool)

        self.agent = Agent(
            role="Technical Writer & Documentation Specialist",
            goal="Create comprehensive, clear, and user-friendly documentation for the project",
            backstory="""You are Amina, an expert Technical Writer with deep knowledge of technical documentation,
            user guides, and developer documentation. You excel at explaining complex concepts clearly, creating
            comprehensive guides, and ensuring documentation is accessible to all users. You are detail-oriented,
            user-focused, and committed to documentation excellence.""",
            verbose=True,
            allow_delegation=False,
            tools=tools,
            llm=llm,
        )

    def create_readme_task(self, project_context: str) -> Task:
        """Create task for writing README documentation.

        Args:
            project_context: Project overview and features

        Returns:
            Task for README documentation
        """
        return Task(
            description=f"""Create comprehensive README documentation.

            Project Context:
            {project_context}

            Your task:
            1. Write clear project description
            2. List key features and capabilities
            3. Provide installation instructions
            4. Include quick start guide
            5. Document configuration options
            6. Provide usage examples
            7. Include contribution guidelines
            8. Add license information
            9. Include badges (build status, coverage, version)
            10. Add links to additional documentation

            Output: Comprehensive README.md file with all sections.
            """,
            agent=self.agent,
            expected_output="Complete README.md with project overview, installation, usage, and contribution guidelines",
        )

    def create_api_documentation_task(self, api_context: str) -> Task:
        """Create task for API documentation.

        Args:
            api_context: API endpoints and specifications

        Returns:
            Task for API documentation
        """
        return Task(
            description=f"""Create comprehensive API documentation.

            API Context:
            {api_context}

            Your task:
            1. Document all API endpoints
            2. Include request/response formats
            3. Document authentication and authorization
            4. Provide code examples for each endpoint
            5. Document error responses
            6. Include rate limiting information
            7. Document query parameters and headers
            8. Create API reference section
            9. Include interactive API examples if possible
            10. Document versioning and deprecation policy

            Output: Complete API documentation with examples and reference.
            """,
            agent=self.agent,
            expected_output="Comprehensive API documentation with endpoints, examples, and reference",
        )

    def create_user_guide_task(self, user_context: str) -> Task:
        """Create task for user guide documentation.

        Args:
            user_context: User workflows and features

        Returns:
            Task for user guide
        """
        return Task(
            description=f"""Create comprehensive user guide.

            User Context:
            {user_context}

            Your task:
            1. Write introduction and overview
            2. Document key features and capabilities
            3. Create step-by-step tutorials
            4. Include screenshots and diagrams
            5. Document common use cases
            6. Provide troubleshooting guide
            7. Include FAQ section
            8. Document best practices
            9. Create getting started guide
            10. Include advanced usage examples

            Output: Complete user guide with tutorials and examples.
            """,
            agent=self.agent,
            expected_output="Comprehensive user guide with tutorials, examples, and troubleshooting",
        )

    def create_developer_guide_task(self, dev_context: str) -> Task:
        """Create task for developer guide documentation.

        Args:
            dev_context: Development setup and architecture

        Returns:
            Task for developer guide
        """
        return Task(
            description=f"""Create comprehensive developer guide.

            Developer Context:
            {dev_context}

            Your task:
            1. Document development environment setup
            2. Explain project architecture
            3. Document code structure and organization
            4. Provide development workflow guide
            5. Document testing procedures
            6. Include code style guidelines
            7. Document contribution process
            8. Provide debugging guide
            9. Document deployment process
            10. Include architecture diagrams

            Output: Complete developer guide with setup, architecture, and contribution guidelines.
            """,
            agent=self.agent,
            expected_output="Comprehensive developer guide with setup, architecture, and contribution process",
        )

    def create_architecture_documentation_task(self, arch_context: str) -> Task:
        """Create task for architecture documentation.

        Args:
            arch_context: System architecture and design decisions

        Returns:
            Task for architecture documentation
        """
        return Task(
            description=f"""Create comprehensive architecture documentation.

            Architecture Context:
            {arch_context}

            Your task:
            1. Document system architecture overview
            2. Explain architectural decisions (ADRs)
            3. Document components and their interactions
            4. Include architecture diagrams
            5. Document data flow
            6. Explain technology choices
            7. Document scalability considerations
            8. Include security architecture
            9. Document deployment architecture
            10. Document future roadmap

            Output: Complete architecture documentation with diagrams and design decisions.
            """,
            agent=self.agent,
            expected_output="Comprehensive architecture documentation with diagrams and design decisions",
        )

    def create_changelog_task(self, changelog_context: str) -> Task:
        """Create task for changelog documentation.

        Args:
            changelog_context: Version history and changes

        Returns:
            Task for changelog
        """
        return Task(
            description=f"""Create comprehensive changelog.

            Changelog Context:
            {changelog_context}

            Your task:
            1. Document all version changes
            2. Categorize changes (Added, Changed, Deprecated, Removed, Fixed, Security)
            3. Include version numbers and dates
            4. Document breaking changes
            5. Include migration guides for breaking changes
            6. Link to relevant issues/PRs
            7. Follow Keep a Changelog format
            8. Document upgrade instructions

            Output: Complete CHANGELOG.md following Keep a Changelog format.
            """,
            agent=self.agent,
            expected_output="Complete CHANGELOG.md with version history and migration guides",
        )

    def create_troubleshooting_guide_task(self, troubleshooting_context: str) -> Task:
        """Create task for troubleshooting guide.

        Args:
            troubleshooting_context: Common issues and solutions

        Returns:
            Task for troubleshooting guide
        """
        return Task(
            description=f"""Create comprehensive troubleshooting guide.

            Troubleshooting Context:
            {troubleshooting_context}

            Your task:
            1. Identify common issues and errors
            2. Provide step-by-step solutions
            3. Include error messages and their meanings
            4. Document diagnostic steps
            5. Provide log analysis guidance
            6. Include debugging tips
            7. Document known issues and workarounds
            8. Provide contact information for support
            9. Include escalation procedures

            Output: Complete troubleshooting guide with common issues and solutions.
            """,
            agent=self.agent,
            expected_output="Comprehensive troubleshooting guide with common issues and solutions",
        )

    def create_migration_guide_task(self, migration_context: str) -> Task:
        """Create task for migration guide.

        Args:
            migration_context: Migration requirements and procedures

        Returns:
            Task for migration guide
        """
        return Task(
            description=f"""Create comprehensive migration guide.

            Migration Context:
            {migration_context}

            Your task:
            1. Document migration prerequisites
            2. Provide step-by-step migration process
            3. Include data migration procedures
            4. Document configuration changes
            5. Provide rollback procedures
            6. Include testing checklist
            7. Document downtime requirements
            8. Provide post-migration verification steps
            9. Include common migration issues and solutions

            Output: Complete migration guide with procedures and rollback steps.
            """,
            agent=self.agent,
            expected_output="Comprehensive migration guide with procedures and rollback steps",
        )

    def create_code_examples_task(self, examples_context: str) -> Task:
        """Create task for code examples documentation.

        Args:
            examples_context: Code usage patterns and examples

        Returns:
            Task for code examples
        """
        return Task(
            description=f"""Create comprehensive code examples documentation.

            Examples Context:
            {examples_context}

            Your task:
            1. Identify common use cases
            2. Create code examples for each use case
            3. Include explanations for each example
            4. Provide complete, runnable examples
            5. Document input/output for each example
            6. Include best practices examples
            7. Document anti-patterns to avoid
            8. Provide advanced usage examples
            9. Include integration examples

            Output: Complete code examples documentation with explanations.
            """,
            agent=self.agent,
            expected_output="Comprehensive code examples documentation with explanations",
        )

    def create_release_notes_task(self, release_context: str) -> Task:
        """Create task for release notes.

        Args:
            release_context: Release details and changes

        Returns:
            Task for release notes
        """
        return Task(
            description=f"""Create comprehensive release notes.

            Release Context:
            {release_context}

            Your task:
            1. Write release summary
            2. List new features
            3. Document improvements and enhancements
            4. List bug fixes
            5. Document breaking changes
            6. Include upgrade instructions
            7. Document known issues
            8. Include acknowledgments
            9. Provide download links
            10. Include compatibility information

            Output: Complete release notes with all relevant information.
            """,
            agent=self.agent,
            expected_output="Comprehensive release notes with features, fixes, and upgrade instructions",
        )

    def get_agent(self) -> Agent:
        """Get the CrewAI Agent instance.

        Returns:
            CrewAI Agent instance
        """
        return self.agent
