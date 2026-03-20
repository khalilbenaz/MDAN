"""DevOps Agent (Anas) - SHIP Phase

Responsible for deployment, CI/CD, infrastructure, and cloud operations.
"""

from crewai import Agent, Task
from typing import List, Optional
from ..tools.sql_tool import SQLTool
from ..tools.serper_tool import SerperTool
from ..tools.file_tool import FileTool


class DevOpsAgent:
    """DevOps Agent for SHIP phase - Deployment, CI/CD, and infrastructure management."""

    def __init__(
        self,
        sql_tool: Optional[SQLTool] = None,
        serper_tool: Optional[SerperTool] = None,
        file_tool: Optional[FileTool] = None,
        llm=None,
    ):
        """Initialize DevOps Agent.

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
            role="DevOps Engineer & Cloud Specialist",
            goal="Ensure reliable deployment and infrastructure management through CI/CD and cloud operations",
            backstory="""You are Anas, an expert DevOps Engineer with deep knowledge of cloud infrastructure,
            CI/CD pipelines, containerization, and infrastructure as code. You excel at designing robust deployment
            strategies, automating operations, and ensuring high availability. You are automation-focused,
            reliability-conscious, and committed to operational excellence.""",
            verbose=True,
            allow_delegation=False,
            tools=tools,
            llm=llm,
        )

    def create_ci_cd_pipeline_task(self, project_context: str) -> Task:
        """Create task for setting up CI/CD pipeline.

        Args:
            project_context: Project structure and requirements

        Returns:
            Task for CI/CD pipeline setup
        """
        return Task(
            description=f"""Design and implement CI/CD pipeline.

            Project Context:
            {project_context}

            Your task:
            1. Analyze project structure and requirements
            2. Design CI/CD pipeline stages:
               - Build
               - Test (unit, integration, E2E)
               - Code quality checks (linting, type checking)
               - Security scanning
               - Build artifacts
               - Deploy to staging
               - Integration tests
               - Deploy to production
            3. Select CI/CD platform (GitHub Actions, GitLab CI, Azure DevOps, etc.)
            4. Configure pipeline triggers (push, PR, schedule)
            5. Set up environment-specific configurations
            6. Configure secrets management
            7. Set up notifications and approvals
            8. Document pipeline configuration

            Output: Complete CI/CD pipeline configuration with documentation.
            """,
            agent=self.agent,
            expected_output="CI/CD pipeline configuration with all stages and documentation",
        )

    def create_docker_setup_task(self, application_context: str) -> Task:
        """Create task for Docker containerization.

        Args:
            application_context: Application details and dependencies

        Returns:
            Task for Docker setup
        """
        return Task(
            description=f
            < arg_value
            > """Set up Docker containerization for the application.

            Application Context:
            {application_context}

            Your task:
            1. Create optimized Dockerfile for the application
            2. Use multi-stage builds for smaller images
            3. Configure health checks
            4. Set up proper environment variables
            5. Create docker-compose for local development
            6. Configure volume mounts for development
            7. Set up networking between services
            8. Document Docker setup and usage
            9. Create .dockerignore file

            Output: Complete Docker setup with Dockerfile, docker-compose, and documentation.
            """,
            agent=self.agent,
            expected_output="Docker setup with Dockerfile, docker-compose, and usage documentation",
        )

    def create_kubernetes_setup_task(self, k8s_context: str) -> Task:
        """Create task for Kubernetes deployment.

        Args:
            k8s_context: Application and infrastructure requirements

        Returns:
            Task for Kubernetes setup
        """
        return Task(
            description=f"""Set up Kubernetes deployment configuration.

            Kubernetes Context:
            {k8s_context}

            Your task:
            1. Design Kubernetes architecture
            2. Create deployment manifests:
               - Deployment
               - Service
               - ConfigMap
               - Secret
               - Ingress
               - HorizontalPodAutoscaler
            3. Configure resource limits and requests
            4. Set up liveness and readiness probes
            5. Configure persistent volumes if needed
            6. Set up namespace isolation
            7. Create Helm chart if applicable
            8. Document Kubernetes setup and deployment process

            Output: Complete Kubernetes manifests with deployment documentation.
            """,
            agent=self.agent,
            expected_output="Kubernetes deployment manifests with setup documentation",
        )

    def create_azure_deployment_task(self, azure_context: str) -> Task:
        """Create task for Azure cloud deployment.

        Args:
            azure_context: Azure requirements and configuration

        Returns:
            Task for Azure deployment
        """
        return Task(
            description=f"""Set up Azure cloud deployment infrastructure.

            Azure Context:
            {azure_context}

            Your task:
            1. Design Azure architecture
            2. Set up Azure resources:
               - Resource Group
               - App Service / Container Apps / AKS
               - Azure SQL / PostgreSQL
               - Azure Storage
               - Azure Key Vault
               - Application Insights
               - Azure CDN (if needed)
            3. Configure networking (VNet, subnets, NSG)
            4. Set up identity and access management
            5. Configure backup and disaster recovery
            6. Set up monitoring and alerting
            7. Create Infrastructure as Code (Terraform/Bicep)
            8. Document Azure setup and deployment process

            Output: Complete Azure infrastructure setup with IaC and documentation.
            """,
            agent=self.agent,
            expected_output="Azure infrastructure setup with IaC and deployment documentation",
        )

    def create_monitoring_setup_task(self, monitoring_context: str) -> Task:
        """Create task for monitoring and observability.

        Args:
            monitoring_context: Application and infrastructure context

        Returns:
            Task for monitoring setup
        """
        return Task(
            description=f"""Set up comprehensive monitoring and observability.

            Monitoring Context:
            {monitoring_context}

            Your task:
            1. Define monitoring requirements and metrics
            2. Set up application monitoring:
               - Performance metrics (latency, throughput, error rate)
               - Business metrics
               - Custom metrics
            3. Set up infrastructure monitoring:
               - CPU, memory, disk, network
               - Container metrics
               - Database metrics
            4. Configure logging:
               - Application logs
               - Access logs
               - Error logs
               - Structured logging
            5. Set up distributed tracing
            6. Configure dashboards and visualizations
            7. Set up alerts and notifications
            8. Document monitoring setup and alert thresholds

            Output: Complete monitoring setup with dashboards and alerting.
            """,
            agent=self.agent,
            expected_output="Monitoring infrastructure with dashboards and alerting configuration",
        )

    def create_deployment_strategy_task(self, deployment_context: str) -> Task:
        """Create task for deployment strategy.

        Args:
            deployment_context: Application and business requirements

        Returns:
            Task for deployment strategy
        """
        return Task(
            description=f"""Design deployment strategy for the application.

            Deployment Context:
            {deployment_context}

            Your task:
            1. Analyze application and business requirements
            2. Select deployment strategy:
               - Blue-Green deployment
               - Canary deployment
               - Rolling update
               - Feature flags
            3. Design deployment pipeline stages
            4. Configure rollback procedures
            5. Set up health checks and smoke tests
            6. Configure traffic shifting
            7. Set up deployment approvals
            8. Document deployment strategy and procedures

            Output: Deployment strategy document with implementation details.
            """,
            agent=self.agent,
            expected_output="Deployment strategy document with implementation procedures",
        )

    def create_infrastructure_as_code_task(self, iac_context: str) -> Task:
        """Create task for Infrastructure as Code.

        Args:
            iac_context: Infrastructure requirements

        Returns:
            Task for IaC setup
        """
        return Task(
            description=f"""Set up Infrastructure as Code.

            IaC Context:
            {iac_context}

            Your task:
            1. Select IaC tool (Terraform, Bicep, Pulumi, etc.)
            2. Design infrastructure modules
            3. Create reusable infrastructure components
            4. Configure state management
            5. Set up environment-specific configurations
            6. Configure secrets management
            7. Set up infrastructure testing
            8. Document IaC structure and usage
            9. Create infrastructure validation

            Output: Complete IaC setup with modules and documentation.
            """,
            agent=self.agent,
            expected_output="Infrastructure as Code setup with modules and documentation",
        )

    def create_backup_recovery_task(self, backup_context: str) -> Task:
        """Create task for backup and disaster recovery.

        Args:
            backup_context: Data and infrastructure context

        Returns:
            Task for backup and recovery setup
        """
        return Task(
            description=f"""Set up backup and disaster recovery strategy.

            Backup Context:
            {backup_context}

            Your task:
            1. Identify critical data and infrastructure
            2. Define backup requirements (RPO, RTO)
            3. Set up automated backups:
               - Database backups
               - Application data backups
               - Configuration backups
            4. Configure backup retention policies
            5. Set up backup monitoring and alerts
            6. Design disaster recovery procedures
            7. Test backup and recovery procedures
            8. Document backup and recovery processes

            Output: Backup and disaster recovery setup with documentation.
            """,
            agent=self.agent,
            expected_output="Backup and disaster recovery setup with procedures documentation",
        )

    def create_scaling_strategy_task(self, scaling_context: str) -> Task:
        """Create task for scaling strategy.

        Args:
            scaling_context: Application and traffic patterns

        Returns:
            Task for scaling strategy
        """
        return Task(
            description=f"""Design scaling strategy for the application.

            Scaling Context:
            {scaling_context}

            Your task:
            1. Analyze traffic patterns and load requirements
            2. Design scaling strategy:
               - Horizontal scaling
               - Vertical scaling
               - Auto-scaling policies
            3. Configure load balancing
            4. Set up caching strategy
            5. Configure database scaling
            6. Set up CDN for static assets
            7. Configure auto-scaling rules and thresholds
            8. Document scaling strategy and procedures

            Output: Scaling strategy document with implementation details.
            """,
            agent=self.agent,
            expected_output="Scaling strategy document with auto-scaling configuration",
        )

    def create_security_hardening_task(self, security_context: str) -> Task:
        """Create task for infrastructure security hardening.

        Args:
            security_context: Infrastructure and security requirements

        Returns:
            Task for security hardening
        """
        return Task(
            description=f"""Implement infrastructure security hardening.

            Security Context:
            {security_context}

            Your task:
            1. Review infrastructure security posture
            2. Implement network security:
               - VNet isolation
               - Network security groups
               - Private endpoints
            3. Configure identity and access management
            4. Set up secrets management
            5. Configure SSL/TLS certificates
            6. Implement security monitoring
            7. Configure firewall rules
            8. Document security hardening measures

            Output: Infrastructure security hardening implementation with documentation.
            """,
            agent=self.agent,
            expected_output="Infrastructure security hardening with documentation",
        )

    def get_agent(self) -> Agent:
        """Get the CrewAI Agent instance.

        Returns:
            CrewAI Agent instance
        """
        return self.agent
