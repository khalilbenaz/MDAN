"""Test Agent (Youssef) - VERIFY Phase

Responsible for testing strategy, test execution, and quality assurance.
"""

from crewai import Agent, Task
from typing import List, Optional
from ..tools.sql_tool import SQLTool
from ..tools.serper_tool import SerperTool
from ..tools.file_tool import FileTool


class TestAgent:
    """Test Agent for VERIFY phase - Testing strategy and execution."""

    def __init__(
        self,
        sql_tool: Optional[SQLTool] = None,
        serper_tool: Optional[SerperTool] = None,
        file_tool: Optional[FileTool] = None,
        llm=None,
    ):
        """Initialize Test Agent.

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
            role="Test Engineer & QA Specialist",
            goal="Ensure software quality through comprehensive testing strategies and execution",
            backstory="""You are Youssef, an expert Test Engineer with deep knowledge of testing methodologies,
            test automation, and quality assurance. You excel at designing test strategies, writing test cases,
            and ensuring software meets quality standards. You are thorough, detail-oriented, and focused on
            preventing bugs before they reach production.""",
            verbose=True,
            allow_delegation=False,
            tools=tools,
            llm=llm,
        )

    def create_test_strategy_task(self, project_context: str) -> Task:
        """Create task for developing test strategy.

        Args:
            project_context: Project requirements and context

        Returns:
            Task for test strategy development
        """
        return Task(
            description=f"""Develop a comprehensive test strategy for the project.

            Project Context:
            {project_context}

            Your task:
            1. Analyze project requirements and identify testing needs
            2. Define test scope and objectives
            3. Identify test types needed (unit, integration, E2E, performance, security)
            4. Define test coverage targets (aim for 80%+)
            5. Identify test data requirements
            6. Define test environment setup
            7. Create test schedule and milestones
            8. Identify testing tools and frameworks needed

            Output: Complete test strategy document with all sections defined.
            """,
            agent=self.agent,
            expected_output="Comprehensive test strategy document covering scope, types, coverage, tools, and schedule",
        )

    def create_unit_tests_task(self, codebase_context: str) -> Task:
        """Create task for writing unit tests.

        Args:
            codebase_context: Codebase structure and implementation details

        Returns:
            Task for unit test development
        """
        return Task(
            description=f"""Write comprehensive unit tests for the codebase.

            Codebase Context:
            {codebase_context}

            Your task:
            1. Analyze codebase structure and identify components to test
            2. Write unit tests for all business logic functions
            3. Ensure tests follow Arrange-Act-Assert pattern
            4. Use descriptive test names (test_function_scenario_expected_result)
            5. Test edge cases and error conditions
            6. Mock external dependencies appropriately
            7. Achieve 80%+ code coverage
            8. Use appropriate testing framework (pytest, unittest, etc.)

            Output: Complete unit test suite with high coverage.
            """,
            agent=self.agent,
            expected_output="Comprehensive unit test suite with 80%+ code coverage",
        )

    def create_integration_tests_task(self, api_context: str) -> Task:
        """Create task for writing integration tests.

        Args:
            api_context: API endpoints and integration points

        Returns:
            Task for integration test development
        """
        return Task(
            description=f"""Write integration tests for API and database interactions.

            API Context:
            {api_context}

            Your task:
            1. Identify all API endpoints to test
            2. Write tests for database operations
            3. Test external service integrations
            4. Test authentication and authorization
            5. Test error handling and edge cases
            6. Use test databases/fixtures
            7. Test data validation
            8. Ensure tests are independent and repeatable

            Output: Complete integration test suite covering all critical paths.
            """,
            agent=self.agent,
            expected_output="Integration test suite covering all API endpoints and database operations",
        )

    def create_e2e_tests_task(self, user_flows: str) -> Task:
        """Create task for writing E2E tests.

        Args:
            user_flows: User journey and flow descriptions

        Returns:
            Task for E2E test development
        """
        return Task(
            description=f"""Write end-to-end tests for critical user flows.

            User Flows:
            {user_flows}

            Your task:
            1. Identify critical user journeys
            2. Write E2E tests for each flow
            3. Test complete user workflows from start to finish
            4. Include happy path and error scenarios
            5. Test cross-browser compatibility if applicable
            6. Use appropriate E2E testing framework (Playwright, Cypress, Selenium)
            7. Ensure tests are maintainable and reliable
            8. Document test scenarios

            Output: E2E test suite covering all critical user flows.
            """,
            agent=self.agent,
            expected_output="E2E test suite covering all critical user journeys",
        )

    def create_test_execution_task(self, test_suite: str) -> Task:
        """Create task for executing tests and reporting results.

        Args:
            test_suite: Test suite to execute

        Returns:
            Task for test execution
        """
        return Task(
            description=f"""Execute the test suite and generate comprehensive test report.

            Test Suite:
            {test_suite}

            Your task:
            1. Execute all tests in the suite
            2. Collect test results and metrics
            3. Calculate code coverage
            4. Identify failing tests and root causes
            5. Generate test report with:
               - Test summary (total, passed, failed, skipped)
               - Coverage metrics
               - Performance metrics
               - Failed test details with stack traces
               - Recommendations for fixes
            6. Identify quality trends and patterns
            7. Document any blockers or issues

            Output: Comprehensive test report with all metrics and recommendations.
            """,
            agent=self.agent,
            expected_output="Detailed test report with coverage metrics, failure analysis, and recommendations",
        )

    def create_performance_tests_task(self, performance_requirements: str) -> Task:
        """Create task for performance testing.

        Args:
            performance_requirements: Performance criteria and requirements

        Returns:
            Task for performance test development
        """
        return Task(
            description=f"""Design and execute performance tests.

            Performance Requirements:
            {performance_requirements}

            Your task:
            1. Identify performance-critical components
            2. Define performance metrics (response time, throughput, latency)
            3. Create load tests for expected traffic
            4. Create stress tests for peak conditions
            5. Test database query performance
            6. Identify performance bottlenecks
            7. Generate performance report with:
               - Baseline metrics
               - Test results
               - Bottleneck analysis
               - Optimization recommendations
            8. Set up performance monitoring

            Output: Performance test suite and report with optimization recommendations.
            """,
            agent=self.agent,
            expected_output="Performance test suite and report with bottleneck analysis",
        )

    def create_security_tests_task(self, security_context: str) -> Task:
        """Create task for security testing.

        Args:
            security_context: Security requirements and context

        Returns:
            Task for security test development
        """
        return Task(
            description=f"""Design and execute security tests.

            Security Context:
            {security_context}

            Your task:
            1. Identify security vulnerabilities to test for
            2. Test for common vulnerabilities (OWASP Top 10)
            3. Test authentication and authorization
            4. Test input validation and sanitization
            5. Test for SQL injection, XSS, CSRF
            6. Test API security (rate limiting, authentication)
            7. Test data encryption and secure storage
            8. Generate security report with:
               - Vulnerability findings
               - Risk assessment
               - Remediation recommendations
            9. Verify security best practices

            Output: Security test report with vulnerability findings and remediation plan.
            """,
            agent=self.agent,
            expected_output="Security test report with vulnerability assessment and remediation plan",
        )

    def create_test_automation_task(self, automation_context: str) -> Task:
        """Create task for test automation setup.

        Args:
            automation_context: Test automation requirements

        Returns:
            Task for test automation setup
        """
        return Task(
            description=f"""Set up test automation infrastructure.

            Automation Context:
            {automation_context}

            Your task:
            1. Select appropriate testing frameworks and tools
            2. Set up test automation pipeline
            3. Configure CI/CD integration for automated tests
            4. Create test data management strategy
            5. Set up test reporting and notifications
            6. Configure test environment provisioning
            7. Document automation setup and maintenance
            8. Create guidelines for writing automated tests

            Output: Complete test automation setup with documentation.
            """,
            agent=self.agent,
            expected_output="Test automation infrastructure setup with CI/CD integration",
        )

    def create_quality_gate_task(self, quality_criteria: str) -> Task:
        """Create task for defining quality gates.

        Args:
            quality_criteria: Quality criteria and thresholds

        Returns:
            Task for quality gate definition
        """
        return Task(
            description=f"""Define quality gates for the project.

            Quality Criteria:
            {quality_criteria}

            Your task:
            1. Define quality gate criteria for each phase
            2. Set thresholds for:
               - Code coverage (minimum 80%)
               - Test pass rate (100% for critical paths)
               - Performance metrics
               - Security scan results
               - Code quality metrics
            3. Define gate approval process
            4. Create gate check automation
            5. Document gate criteria and process
            6. Define exception handling for gate failures
            7. Set up gate monitoring and reporting

            Output: Quality gate definitions with automated checks and documentation.
            """,
            agent=self.agent,
            expected_output="Quality gate definitions with automated checks and approval process",
        )

    def get_agent(self) -> Agent:
        """Get the CrewAI Agent instance.

        Returns:
            CrewAI Agent instance
        """
        return self.agent
