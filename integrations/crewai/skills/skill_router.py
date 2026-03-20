"""Skill Router - Intelligent skill detection and execution

Detects required skills for tasks and executes them using appropriate agents.
"""

import re
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Set
from enum import Enum

from .orchestrator import CrewAIOrchestrator


class Skill(Enum):
    """Available skills."""

    # Product skills
    REQUIREMENT_ANALYSIS = "requirement_analysis"
    PRD_CREATION = "prd_creation"
    USER_STORY_WRITING = "user_story_writing"
    PERSONA_CREATION = "persona_creation"
    FEATURE_PRIORITIZATION = "feature_prioritization"
    ACCEPTANCE_CRITERIA = "acceptance_criteria"

    # Architecture skills
    SYSTEM_ARCHITECTURE = "system_architecture"
    TECH_STACK_SELECTION = "tech_stack_selection"
    ADR_DOCUMENTATION = "adr_documentation"
    API_DESIGN = "api_design"
    DATABASE_SCHEMA = "database_schema"

    # UX skills
    USER_FLOW_DESIGN = "user_flow_design"
    WIREFRAME_CREATION = "wireframe_creation"
    DESIGN_SYSTEM = "design_system"
    ACCESSIBILITY = "accessibility"
    PROTOTYPE_CREATION = "prototype_creation"

    # Development skills
    IMPLEMENTATION = "implementation"
    REFACTORING = "refactoring"
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    DEBUGGING = "debugging"

    # Testing skills
    TEST_STRATEGY = "test_strategy"
    UNIT_TESTING = "unit_testing"
    INTEGRATION_TESTING = "integration_testing"
    E2E_TESTING = "e2e_testing"
    TEST_EXECUTION = "test_execution"
    PERFORMANCE_TESTING = "performance_testing"
    SECURITY_TESTING = "security_testing"
    TEST_AUTOMATION = "test_automation"
    QUALITY_GATE = "quality_gate"

    # Security skills
    SECURITY_REVIEW = "security_review"
    VULNERABILITY_SCAN = "vulnerability_scan"
    SECURE_CODING = "secure_coding"
    DEPENDENCY_SECURITY = "dependency_security"
    AUTHENTICATION_SECURITY = "authentication_security"
    DATA_PROTECTION = "data_protection"
    API_SECURITY = "api_security"
    SECURITY_MONITORING = "security_monitoring"
    COMPLIANCE_REVIEW = "compliance_review"

    # DevOps skills
    CI_CD_PIPELINE = "ci_cd_pipeline"
    DOCKER_SETUP = "docker_setup"
    KUBERNETES_SETUP = "kubernetes_setup"
    AZURE_DEPLOYMENT = "azure_deployment"
    MONITORING_SETUP = "monitoring_setup"
    DEPLOYMENT_STRATEGY = "deployment_strategy"
    INFRASTRUCTURE_AS_CODE = "infrastructure_as_code"
    BACKUP_RECOVERY = "backup_recovery"
    SCALING_STRATEGY = "scaling_strategy"
    SECURITY_HARDENING = "security_hardening"

    # Documentation skills
    README_CREATION = "readme_creation"
    API_DOCUMENTATION = "api_documentation"
    USER_GUIDE = "user_guide"
    DEVELOPER_GUIDE = "developer_guide"
    ARCHITECTURE_DOCUMENTATION = "architecture_documentation"
    CHANGELOG = "changelog"
    TROUBLESHOOTING_GUIDE = "troubleshooting_guide"
    MIGRATION_GUIDE = "migration_guide"
    CODE_EXAMPLES = "code_examples"
    RELEASE_NOTES = "release_notes"

    # Tool skills
    WEB_SEARCH = "web_search"
    SQL_QUERY = "sql_query"
    FILE_OPERATION = "file_operation"


class SkillRouter:
    """Intelligent skill router for detecting and executing skills."""

    def __init__(self, orchestrator: CrewAIOrchestrator):
        """Initialize Skill Router.

        Args:
            orchestrator: CrewAI orchestrator instance
        """
        self.orchestrator = orchestrator
        self.skill_patterns = self._initialize_skill_patterns()
        self.skill_execution_history = []

    def _initialize_skill_patterns(self) -> Dict[Skill, List[str]]:
        """Initialize skill detection patterns.

        Returns:
            Dictionary mapping skills to keyword patterns
        """
        return {
            # Product skills
            Skill.REQUIREMENT_ANALYSIS: [
                "requirement",
                "analyze requirement",
                "gather requirement",
            ],
            Skill.PRD_CREATION: ["prd", "product requirement", "requirement document"],
            Skill.USER_STORY_WRITING: [
                "user story",
                "story",
                "as a user",
                "user wants",
            ],
            Skill.PERSONA_CREATION: [
                "persona",
                "user persona",
                "target audience",
                "user profile",
            ],
            Skill.FEATURE_PRIORITIZATION: [
                "prioritize feature",
                "feature priority",
                "rank feature",
                "moscow",
            ],
            Skill.ACCEPTANCE_CRITERIA: [
                "acceptance criteria",
                "definition of done",
                "dod",
            ],
            # Architecture skills
            Skill.SYSTEM_ARCHITECTURE: [
                "architecture",
                "system design",
                "high level design",
            ],
            Skill.TECH_STACK_SELECTION: [
                "tech stack",
                "technology stack",
                "framework",
                "library",
            ],
            Skill.ADR_DOCUMENTATION: [
                "adr",
                "architecture decision",
                "decision record",
            ],
            Skill.API_DESIGN: ["api design", "endpoint", "rest api", "graphql"],
            Skill.DATABASE_SCHEMA: [
                "database schema",
                "data model",
                "entity relationship",
                "er diagram",
            ],
            # UX skills
            Skill.USER_FLOW_DESIGN: ["user flow", "flow", "journey", "workflow"],
            Skill.WIREFRAME_CREATION: ["wireframe", "mockup", "layout"],
            Skill.DESIGN_SYSTEM: ["design system", "component library", "style guide"],
            Skill.ACCESSIBILITY: ["accessibility", "a11y", "wcag", "inclusive design"],
            Skill.PROTOTYPE_CREATION: [
                "prototype",
                "interactive prototype",
                "clickable",
            ],
            # Development skills
            Skill.IMPLEMENTATION: [
                "implement",
                "develop",
                "code",
                "build",
                "create feature",
            ],
            Skill.REFACTORING: [
                "refactor",
                "clean up",
                "improve code",
                "optimize code",
            ],
            Skill.CODE_REVIEW: ["code review", "review code", "peer review"],
            Skill.TESTING: ["write test", "create test", "add test"],
            Skill.DEBUGGING: ["debug", "fix bug", "troubleshoot", "resolve issue"],
            # Testing skills
            Skill.TEST_STRATEGY: ["test strategy", "testing approach", "test plan"],
            Skill.UNIT_TESTING: ["unit test", "unit testing", "test function"],
            Skill.INTEGRATION_TESTING: [
                "integration test",
                "api test",
                "database test",
            ],
            Skill.E2E_TESTING: ["e2e test", "end to end test", "user flow test"],
            Skill.TEST_EXECUTION: ["run test", "execute test", "test execution"],
            Skill.PERFORMANCE_TESTING: ["performance test", "load test", "stress test"],
            Skill.SECURITY_TESTING: [
                "security test",
                "penetration test",
                "vulnerability test",
            ],
            Skill.TEST_AUTOMATION: ["test automation", "automate test", "ci test"],
            Skill.QUALITY_GATE: ["quality gate", "quality check", "acceptance gate"],
            # Security skills
            Skill.SECURITY_REVIEW: [
                "security review",
                "security audit",
                "code security",
            ],
            Skill.VULNERABILITY_SCAN: [
                "vulnerability scan",
                "security scan",
                "dependency scan",
            ],
            Skill.SECURE_CODING: [
                "secure coding",
                "security best practice",
                "secure code",
            ],
            Skill.DEPENDENCY_SECURITY: [
                "dependency security",
                "vulnerable dependency",
                "supply chain",
            ],
            Skill.AUTHENTICATION_SECURITY: [
                "authentication",
                "authorization",
                "auth",
                "oauth",
                "jwt",
            ],
            Skill.DATA_PROTECTION: ["data protection", "encryption", "gdpr", "privacy"],
            Skill.API_SECURITY: ["api security", "rate limiting", "api key"],
            Skill.SECURITY_MONITORING: [
                "security monitoring",
                "security alert",
                "intrusion detection",
            ],
            Skill.COMPLIANCE_REVIEW: ["compliance", "audit", "regulation", "standard"],
            # DevOps skills
            Skill.CI_CD_PIPELINE: [
                "ci/cd",
                "pipeline",
                "continuous integration",
                "continuous deployment",
            ],
            Skill.DOCKER_SETUP: ["docker", "container", "dockerfile", "docker compose"],
            Skill.KUBERNETES_SETUP: [
                "kubernetes",
                "k8s",
                "deployment",
                "pod",
                "service",
            ],
            Skill.AZURE_DEPLOYMENT: ["azure", "cloud deployment", "azure devops"],
            Skill.MONITORING_SETUP: [
                "monitoring",
                "observability",
                "logging",
                "metrics",
            ],
            Skill.DEPLOYMENT_STRATEGY: [
                "deployment strategy",
                "blue green",
                "canary",
                "rolling",
            ],
            Skill.INFRASTRUCTURE_AS_CODE: [
                "infrastructure as code",
                "iac",
                "terraform",
                "bicep",
            ],
            Skill.BACKUP_RECOVERY: ["backup", "disaster recovery", "dr"],
            Skill.SCALING_STRATEGY: [
                "scaling",
                "auto scaling",
                "horizontal scaling",
                "vertical scaling",
            ],
            Skill.SECURITY_HARDENING: [
                "security hardening",
                "infrastructure security",
                "network security",
            ],
            # Documentation skills
            Skill.README_CREATION: ["readme", "read me", "project documentation"],
            Skill.API_DOCUMENTATION: [
                "api documentation",
                "api doc",
                "endpoint documentation",
            ],
            Skill.USER_GUIDE: ["user guide", "user manual", "how to"],
            Skill.DEVELOPER_GUIDE: ["developer guide", "dev guide", "contributing"],
            Skill.ARCHITECTURE_DOCUMENTATION: [
                "architecture documentation",
                "system documentation",
            ],
            Skill.CHANGELOG: ["changelog", "change log", "version history"],
            Skill.TROUBLESHOOTING_GUIDE: ["troubleshooting", "faq", "help", "support"],
            Skill.MIGRATION_GUIDE: ["migration guide", "upgrade guide", "migration"],
            Skill.CODE_EXAMPLES: ["code example", "example", "sample code", "snippet"],
            Skill.RELEASE_NOTES: ["release notes", "release note", "what's new"],
            # Tool skills
            Skill.WEB_SEARCH: ["search", "web search", "google", "find information"],
            Skill.SQL_QUERY: [
                "sql",
                "query",
                "database query",
                "select",
                "insert",
                "update",
                "delete",
            ],
            Skill.FILE_OPERATION: [
                "file",
                "read file",
                "write file",
                "create file",
                "delete file",
            ],
        }

    def detect_skills(self, task_description: str) -> Set[Skill]:
        """Detect required skills from task description.

        Args:
            task_description: Description of the task

        Returns:
            Set of detected skills
        """
        task_lower = task_description.lower()
        detected_skills = set()

        for skill, patterns in self.skill_patterns.items():
            for pattern in patterns:
                if pattern.lower() in task_lower:
                    detected_skills.add(skill)
                    break

        return detected_skills

    def get_agent_for_skill(self, skill: Skill) -> Optional[str]:
        """Get the agent name for a given skill.

        Args:
            skill: Skill to get agent for

        Returns:
            Agent name or None
        """
        skill_to_agent = {
            # Product skills
            Skill.REQUIREMENT_ANALYSIS: "product",
            Skill.PRD_CREATION: "product",
            Skill.USER_STORY_WRITING: "product",
            Skill.PERSONA_CREATION: "product",
            Skill.FEATURE_PRIORITIZATION: "product",
            Skill.ACCEPTANCE_CRITERIA: "product",
            # Architecture skills
            Skill.SYSTEM_ARCHITECTURE: "architect",
            Skill.TECH_STACK_SELECTION: "architect",
            Skill.ADR_DOCUMENTATION: "architect",
            Skill.API_DESIGN: "architect",
            Skill.DATABASE_SCHEMA: "architect",
            # UX skills
            Skill.USER_FLOW_DESIGN: "ux",
            Skill.WIREFRAME_CREATION: "ux",
            Skill.DESIGN_SYSTEM: "ux",
            Skill.ACCESSIBILITY: "ux",
            Skill.PROTOTYPE_CREATION: "ux",
            # Development skills
            Skill.IMPLEMENTATION: "dev",
            Skill.REFACTORING: "dev",
            Skill.CODE_REVIEW: "dev",
            Skill.TESTING: "dev",
            Skill.DEBUGGING: "dev",
            # Testing skills
            Skill.TEST_STRATEGY: "test",
            Skill.UNIT_TESTING: "test",
            Skill.INTEGRATION_TESTING: "test",
            Skill.E2E_TESTING: "test",
            Skill.TEST_EXECUTION: "test",
            Skill.PERFORMANCE_TESTING: "test",
            Skill.SECURITY_TESTING: "test",
            Skill.TEST_AUTOMATION: "test",
            Skill.QUALITY_GATE: "test",
            # Security skills
            Skill.SECURITY_REVIEW: "security",
            Skill.VULNERABILITY_SCAN: "security",
            Skill.SECURE_CODING: "security",
            Skill.DEPENDENCY_SECURITY: "security",
            Skill.AUTHENTICATION_SECURITY: "security",
            Skill.DATA_PROTECTION: "security",
            Skill.API_SECURITY: "security",
            Skill.SECURITY_MONITORING: "security",
            Skill.COMPLIANCE_REVIEW: "security",
            # DevOps skills
            Skill.CI_CD_PIPELINE: "devops",
            Skill.DOCKER_SETUP: "devops",
            Skill.KUBERNETES_SETUP: "devops",
            Skill.AZURE_DEPLOYMENT: "devops",
            Skill.MONITORING_SETUP: "devops",
            Skill.DEPLOYMENT_STRATEGY: "devops",
            Skill.INFRASTRUCTURE_AS_CODE: "devops",
            Skill.BACKUP_RECOVERY: "devops",
            Skill.SCALING_STRATEGY: "devops",
            Skill.SECURITY_HARDENING: "devops",
            # Documentation skills
            Skill.README_CREATION: "doc",
            Skill.API_DOCUMENTATION: "doc",
            Skill.USER_GUIDE: "doc",
            Skill.DEVELOPER_GUIDE: "doc",
            Skill.ARCHITECTURE_DOCUMENTATION: "doc",
            Skill.CHANGELOG: "doc",
            Skill.TROUBLESHOOTING_GUIDE: "doc",
            Skill.MIGRATION_GUIDE: "doc",
            Skill.CODE_EXAMPLES: "doc",
            Skill.RELEASE_NOTES: "doc",
            # Tool skills
            Skill.WEB_SEARCH: "product",
            Skill.SQL_QUERY: "architect",
            Skill.FILE_OPERATION: "dev",
        }

        return skill_to_agent.get(skill)

    async def execute_skills(
        self, task_description: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute detected skills for a task.

        Args:
            task_description: Description of the task
            context: Additional context

        Returns:
            Skill execution results
        """
        # Detect skills
        skills = self.detect_skills(task_description)

        if not skills:
            return {
                "status": "no_skills_detected",
                "message": "No skills detected for the task",
            }

        print(f"🔍 Detected skills: {[s.value for s in skills]}")

        # Group skills by agent
        agent_skills: Dict[str, List[Skill]] = {}
        for skill in skills:
            agent = self.get_agent_for_skill(skill)
            if agent:
                if agent not in agent_skills:
                    agent_skills[agent] = []
                agent_skills[agent].append(skill)

        # Execute skills per agent
        results = {}
        for agent_name, agent_skills_list in agent_skills.items():
            print(
                f"🤖 Executing skills with {agent_name} agent: {[s.value for s in agent_skills_list]}"
            )

            # Create task description with skill context
            skill_context = "\n".join(
                [f"- {skill.value}: Execute this skill" for skill in agent_skills_list]
            )

            enhanced_task = f"""{task_description}

            Required skills to execute:
            {skill_context}

            Execute all required skills and provide comprehensive results.
            """

            # Execute task with agent
            result = await self.orchestrator.execute_task(enhanced_task, context)
            results[agent_name] = result

            # Log execution
            self.skill_execution_history.append(
                {
                    "task": task_description,
                    "skills": [s.value for s in agent_skills_list],
                    "agent": agent_name,
                    "result": result,
                    "timestamp": str(os.times()),
                }
            )

        return {
            "status": "success",
            "detected_skills": [s.value for s in skills],
            "agent_results": results,
        }

    def get_skill_execution_history(self) -> List[Dict[str, Any]]:
        """Get skill execution history.

        Returns:
            List of skill execution records
        """
        return self.skill_execution_history

    def clear_skill_execution_history(self):
        """Clear skill execution history."""
        self.skill_execution_history = []

    def get_all_skills(self) -> List[str]:
        """Get all available skills.

        Returns:
            List of skill names
        """
        return [skill.value for skill in Skill]
