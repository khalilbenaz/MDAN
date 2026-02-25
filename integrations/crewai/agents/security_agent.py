"""Security Agent (Said) - BUILD+VERIFY Phases

Responsible for security review, vulnerability assessment, and secure coding practices.
"""

from crewai import Agent, Task
from typing import List, Optional
from ..tools.sql_tool import SQLTool
from ..tools.serper_tool import SerperTool
from ..tools.file_tool import FileTool


class SecurityAgent:
    """Security Agent for BUILD+VERIFY phases - Security review and vulnerability assessment."""

    def __init__(
        self,
        sql_tool: Optional[SQLTool] = None,
        serper_tool: Optional[SerperTool] = None,
        file_tool: Optional[FileTool] = None,
        llm=None,
    ):
        """Initialize Security Agent.

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
            role="Security Engineer & Vulnerability Specialist",
            goal="Ensure software security through comprehensive security reviews and vulnerability assessments",
            backstory="""You are Said, an expert Security Engineer with deep knowledge of cybersecurity,
            vulnerability assessment, and secure coding practices. You excel at identifying security vulnerabilities,
            conducting security reviews, and implementing security best practices. You are thorough, security-conscious,
            and focused on preventing security breaches before they happen.""",
            verbose=True,
            allow_delegation=False,
            tools=tools,
            llm=llm,
        )

    def create_security_review_task(self, codebase_context: str) -> Task:
        """Create task for conducting security code review.

        Args:
            codebase_context: Codebase structure and implementation details

        Returns:
            Task for security code review
        """
        return Task(
            description=f"""Conduct a comprehensive security code review.

            Codebase Context:
            {codebase_context}

            Your task:
            1. Review codebase for security vulnerabilities
            2. Check for OWASP Top 10 vulnerabilities:
               - Injection (SQL, NoSQL, OS command, LDAP)
               - Broken Authentication
               - Sensitive Data Exposure
               - XML External Entities (XXE)
               - Broken Access Control
               - Security Misconfiguration
               - Cross-Site Scripting (XSS)
               - Insecure Deserialization
               - Using Components with Known Vulnerabilities
               - Insufficient Logging & Monitoring
            3. Review authentication and authorization implementation
            4. Check input validation and sanitization
            5. Review error handling for information disclosure
            6. Check for hardcoded secrets or credentials
            7. Review encryption and data protection
            8. Generate security review report with findings and recommendations

            Output: Comprehensive security review report with vulnerability findings and remediation plan.
            """,
            agent=self.agent,
            expected_output="Security review report with vulnerability findings, risk assessment, and remediation plan",
        )

    def create_vulnerability_scan_task(self, scan_context: str) -> Task:
        """Create task for vulnerability scanning.

        Args:
            scan_context: Application and infrastructure context

        Returns:
            Task for vulnerability scanning
        """
        return Task(
            description=f"""Perform vulnerability scanning on the application.

            Scan Context:
            {scan_context}

            Your task:
            1. Configure and run vulnerability scanning tools
            2. Scan for known vulnerabilities in dependencies
            3. Scan for configuration vulnerabilities
            4. Scan for infrastructure vulnerabilities
            5. Analyze scan results and prioritize findings
            6. Generate vulnerability report with:
               - Vulnerability list with severity (Critical, High, Medium, Low)
               - Affected components
               - Exploitability assessment
               - Business impact analysis
               - Remediation recommendations
            7. Create remediation timeline
            8. Document false positives

            Output: Vulnerability scan report with prioritized findings and remediation plan.
            """,
            agent=self.agent,
            expected_output="Vulnerability scan report with severity ratings and remediation timeline",
        )

    def create_secure_coding_task(self, coding_guidelines: str) -> Task:
        """Create task for establishing secure coding guidelines.

        Args:
            coding_guidelines: Existing coding standards and practices

        Returns:
            Task for secure coding guidelines
        """
        return Task(
            description=f"""Establish secure coding guidelines for the project.

            Existing Guidelines:
            {coding_guidelines}

            Your task:
            1. Define secure coding principles
            2. Create guidelines for:
               - Input validation and sanitization
               - Output encoding
               - Authentication and authorization
               - Session management
               - Cryptography usage
               - Error handling and logging
               - Data protection
               - API security
            3. Provide code examples for each guideline
            4. Define security checklists for developers
            5. Create security review checklist
            6. Document common security pitfalls and how to avoid them
            7. Integrate guidelines into development workflow

            Output: Comprehensive secure coding guidelines with examples and checklists.
            """,
            agent=self.agent,
            expected_output="Secure coding guidelines document with examples and developer checklists",
        )

    def create_dependency_security_task(self, dependency_context: str) -> Task:
        """Create task for dependency security review.

        Args:
            dependency_context: List of dependencies and versions

        Returns:
            Task for dependency security review
        """
        return Task(
            description=f"""Review security of project dependencies.

            Dependency Context:
            {dependency_context}

            Your task:
            1. List all project dependencies
            2. Check for known vulnerabilities in each dependency
            3. Review dependency update history
            4. Identify outdated dependencies with security fixes
            5. Assess risk of vulnerable dependencies
            6. Recommend updates or replacements
            7. Create dependency security policy
            8. Set up automated dependency scanning
            9. Document dependency maintenance process

            Output: Dependency security report with update recommendations and maintenance policy.
            """,
            agent=self.agent,
            expected_output="Dependency security report with vulnerability assessment and update recommendations",
        )

    def create_authentication_security_task(self, auth_context: str) -> Task:
        """Create task for authentication security review.

        Args:
            auth_context: Authentication implementation details

        Returns:
            Task for authentication security review
        """
        return Task(
            description=f"""Review and strengthen authentication security.

            Authentication Context:
            {auth_context}

            Your task:
            1. Review authentication implementation
            2. Check for:
               - Strong password policies
               - Multi-factor authentication (MFA)
               - Secure session management
               - Proper token handling (JWT, OAuth)
               - Account lockout mechanisms
               - Password reset security
               - Session timeout configuration
            3. Test authentication flows for vulnerabilities
            4. Review authorization implementation
            5. Check for privilege escalation vulnerabilities
            6. Test role-based access control (RBAC)
            7. Generate authentication security report with recommendations

            Output: Authentication security report with findings and hardening recommendations.
            """,
            agent=self.agent,
            expected_output="Authentication security report with vulnerability findings and hardening plan",
        )

    def create_data_protection_task(self, data_context: str) -> Task:
        """Create task for data protection review.

        Args:
            data_context: Data handling and storage details

        Returns:
            Task for data protection review
        """
        return Task(
            description=f"""Review data protection and privacy measures.

            Data Context:
            {data_context}

            Your task:
            1. Identify sensitive data types (PII, financial, health, etc.)
            2. Review data encryption at rest
            3. Review data encryption in transit
            4. Check data masking and anonymization
            5. Review data retention policies
            6. Check data backup security
            7. Review GDPR/privacy compliance
            8. Check data access controls
            9. Review data logging and audit trails
            10. Generate data protection report with recommendations

            Output: Data protection report with compliance assessment and recommendations.
            """,
            agent=self.agent,
            expected_output="Data protection report with compliance assessment and security recommendations",
        )

    def create_api_security_task(self, api_context: str) -> Task:
        """Create task for API security review.

        Args:
            api_context: API endpoints and implementation details

        Returns:
            Task for API security review
        """
        return Task(
            description=f"""Review API security implementation.

            API Context:
            {api_context}

            Your task:
            1. Review all API endpoints for security
            2. Check for:
               - Proper authentication and authorization
               - Rate limiting and throttling
               - Input validation
               - Output encoding
               - CORS configuration
               - API versioning security
               - Error message information disclosure
               - API key management
            3. Test for common API vulnerabilities
            4. Review API documentation for security guidance
            5. Check for sensitive data in API responses
            6. Review API logging and monitoring
            7. Generate API security report with recommendations

            Output: API security report with vulnerability findings and hardening recommendations.
            """,
            agent=self.agent,
            expected_output="API security report with vulnerability assessment and hardening plan",
        )

    def create_security_monitoring_task(self, monitoring_context: str) -> Task:
        """Create task for security monitoring setup.

        Args:
            monitoring_context: Application and infrastructure context

        Returns:
            Task for security monitoring setup
        """
        return Task(
            description=f"""Set up security monitoring and alerting.

            Monitoring Context:
            {monitoring_context}

            Your task:
            1. Define security monitoring requirements
            2. Set up logging for security events:
               - Authentication failures
               - Authorization failures
               - Suspicious activities
               - Data access
               - Configuration changes
            3. Configure security alerts and notifications
            4. Set up intrusion detection
            5. Configure security dashboards
            6. Define incident response procedures
            7. Set up security audit trails
            8. Document monitoring setup and procedures

            Output: Security monitoring setup with alerting and incident response procedures.
            """,
            agent=self.agent,
            expected_output="Security monitoring infrastructure with alerting and incident response documentation",
        )

    def create_compliance_review_task(self, compliance_context: str) -> Task:
        """Create task for compliance review.

        Args:
            compliance_context: Compliance requirements and standards

        Returns:
            Task for compliance review
        """
        return Task(
            description=f"""Review compliance with security standards and regulations.

            Compliance Context:
            {compliance_context}

            Your task:
            1. Identify applicable compliance standards (GDPR, HIPAA, PCI-DSS, SOC2, etc.)
            2. Review current implementation against requirements
            3. Identify compliance gaps
            4. Assess risk of non-compliance
            5. Create remediation plan for gaps
            6. Document compliance controls
            7. Set up compliance monitoring
            8. Prepare compliance documentation
            9. Generate compliance report with findings and recommendations

            Output: Compliance review report with gap analysis and remediation plan.
            """,
            agent=self.agent,
            expected_output="Compliance review report with gap analysis and remediation recommendations",
        )

    def get_agent(self) -> Agent:
        """Get the CrewAI Agent instance.

        Returns:
            CrewAI Agent instance
        """
        return self.agent
