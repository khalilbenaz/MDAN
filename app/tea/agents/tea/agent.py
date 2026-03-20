"""
TEA Agent

Master Test Architect and Quality Advisor specializing in risk-based testing,
fixture architecture, ATDD, API testing, backend services, UI automation,
CI/CD governance, and scalable quality gates.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class TEARequest:
    """Request data structure for the TEA agent."""

    task: str  # teach-me-testing, test-framework, atdd, test-automate, test-design, test-trace, nfr-assess, continuous-integration, test-review
    context: str
    project_type: Optional[str] = None  # web, mobile, api, microservices
    tech_stack: Optional[List[str]] = (
        None  # playwright, cypress, pytest, junit, go-test, pact
    )
    ci_platform: Optional[str] = (
        None  # github-actions, gitlab-ci, jenkins, azure-devops, harness
    )
    risk_level: Optional[str] = "medium"  # low, medium, high, critical
    scope: Optional[str] = None  # story, feature, epic, system


class TEA:
    """
    Master Test Architect and Quality Advisor.

    Test architect specializing in risk-based testing, fixture architecture,
    ATDD, API testing, backend services, UI automation, CI/CD governance,
    and scalable quality gates. Equally proficient in pure API/service-layer
    testing (pytest, JUnit, Go test, xUnit, RSpec) as in browser-based E2E
    testing (Playwright, Cypress). Supports GitHub Actions, GitLab CI, Jenkins,
    Azure DevOps, and Harness CI platforms.

    Capabilities:
    - Teach testing fundamentals through advanced practices
    - Initialize production-ready test framework architecture
    - Generate failing acceptance tests plus implementation checklist (ATDD)
    - Generate prioritized API/E2E tests, fixtures, and DoD summary
    - Risk assessment plus coverage strategy for system or epic scope
    - Map requirements to tests and make quality gate decisions
    - Assess NFRs and recommend actions
    - Recommend and scaffold CI/CD quality pipeline
    - Perform quality checks against written tests
    """

    def __init__(self):
        """Initialize the TEA agent."""
        self.name = "Murat"
        self.title = "Master Test Architect and Quality Advisor"
        self.icon = "🧪"

    async def process(self, request: TEARequest) -> Dict[str, Any]:
        """
        Process the testing request and return expert guidance.

        Args:
            request: The testing request containing task and parameters

        Returns:
            A dictionary containing the testing guidance and recommendations
        """
        # Validate request
        if not request.task:
            return {
                "success": False,
                "error": "Task is required for testing guidance",
            }

        # Route to appropriate handler based on task
        task_handlers = {
            "teach-me-testing": self._handle_teach_me_testing,
            "test-framework": self._handle_test_framework,
            "atdd": self._handle_atdd,
            "test-automate": self._handle_test_automate,
            "test-design": self._handle_test_design,
            "test-trace": self._handle_test_trace,
            "nfr-assess": self._handle_nfr_assess,
            "continuous-integration": self._handle_continuous_integration,
            "test-review": self._handle_test_review,
        }

        handler = task_handlers.get(request.task)
        if not handler:
            return {
                "success": False,
                "error": f"Unknown task: {request.task}",
            }

        return await handler(request)

    async def _handle_teach_me_testing(self, request: TEARequest) -> Dict[str, Any]:
        """Handle teach-me-testing task."""
        return {
            "success": True,
            "task": "teach-me-testing",
            "guidance": {
                "title": "Interactive Learning Companion - Testing Fundamentals",
                "description": "7 progressive sessions teaching testing fundamentals through advanced practices",
                "sessions": [
                    {
                        "session": 1,
                        "title": "Testing Fundamentals",
                        "topics": [
                            "Why test? Risk and value",
                            "Test pyramid: unit > integration > E2E",
                            "Testing terminology and concepts",
                            "Writing your first test",
                        ],
                    },
                    {
                        "session": 2,
                        "title": "Test Design Principles",
                        "topics": [
                            "AAA pattern (Arrange-Act-Assert)",
                            "Test isolation and independence",
                            "Descriptive test names",
                            "One assertion per test",
                        ],
                    },
                    {
                        "session": 3,
                        "title": "API Testing",
                        "topics": [
                            "API testing vs UI testing",
                            "RESTful API testing with pytest",
                            "Contract testing with Pact",
                            "API test fixtures and data management",
                        ],
                    },
                    {
                        "session": 4,
                        "title": "UI Automation",
                        "topics": [
                            "Playwright vs Cypress comparison",
                            "Page Object Model",
                            "Handling async and waiting",
                            "Visual regression testing",
                        ],
                    },
                    {
                        "session": 5,
                        "title": "Test Architecture",
                        "topics": [
                            "Fixture design patterns",
                            "Test data management",
                            "Test organization and structure",
                            "Reusable test utilities",
                        ],
                    },
                    {
                        "session": 6,
                        "title": "ATDD and TDD",
                        "topics": [
                            "Acceptance Test-Driven Development",
                            "Test-Driven Development workflow",
                            "Writing failing tests first",
                            "Red-Green-Refactor cycle",
                        ],
                    },
                    {
                        "session": 7,
                        "title": "CI/CD and Quality Gates",
                        "topics": [
                            "Integrating tests into CI/CD",
                            "Quality gate strategies",
                            "Test reporting and metrics",
                            "Flakiness detection and prevention",
                        ],
                    },
                ],
                "recommendations": [
                    "Start with session 1 and progress sequentially",
                    "Practice each concept with hands-on exercises",
                    "Apply learnings to your current project",
                    "Review official documentation for your chosen tools",
                ],
            },
        }

    async def _handle_test_framework(self, request: TEARequest) -> Dict[str, Any]:
        """Handle test-framework task."""
        tech_stack = request.tech_stack or ["pytest"]
        project_type = request.project_type or "web"

        return {
            "success": True,
            "task": "test-framework",
            "guidance": {
                "title": "Production-Ready Test Framework Architecture",
                "project_type": project_type,
                "tech_stack": tech_stack,
                "architecture": {
                    "structure": {
                        "tests/": "Root test directory",
                        "tests/unit/": "Unit tests",
                        "tests/integration/": "Integration tests",
                        "tests/e2e/": "End-to-end tests",
                        "tests/fixtures/": "Test fixtures and data",
                        "tests/utils/": "Reusable test utilities",
                        "tests/config/": "Test configuration",
                    },
                    "core_components": [
                        "Test runner configuration",
                        "Fixture management system",
                        "Test data factories",
                        "Assertion libraries",
                        "Mock/stub utilities",
                        "Test reporters",
                    ],
                },
                "recommendations": [
                    f"Use {tech_stack[0]} as primary test framework",
                    "Implement Page Object Model for UI tests",
                    "Create reusable fixtures for common test scenarios",
                    "Set up test data factories for consistent test data",
                    "Configure test reporters for CI/CD integration",
                ],
            },
        }

    async def _handle_atdd(self, request: TEARequest) -> Dict[str, Any]:
        """Handle ATDD task."""
        return {
            "success": True,
            "task": "atdd",
            "guidance": {
                "title": "Acceptance Test-Driven Development",
                "description": "Generate failing acceptance tests plus implementation checklist",
                "process": [
                    "1. Collaborate with stakeholders to define acceptance criteria",
                    "2. Write failing acceptance tests before implementation",
                    "3. Create implementation checklist from test requirements",
                    "4. Implement features to make tests pass",
                    "5. Refactor and optimize implementation",
                ],
                "acceptance_test_template": {
                    "given": "Preconditions and initial state",
                    "when": "Action or event being tested",
                    "then": "Expected outcome and assertions",
                },
                "implementation_checklist": [
                    "Review acceptance criteria",
                    "Identify required components and dependencies",
                    "Plan data model changes",
                    "Design API endpoints (if applicable)",
                    "Plan UI changes (if applicable)",
                    "Identify edge cases and error handling",
                    "Plan integration points",
                ],
                "best_practices": [
                    "Write tests in business language (Gherkin)",
                    "Keep tests independent and isolated",
                    "Use descriptive test names",
                    "Test one behavior per test",
                    "Include edge cases and error scenarios",
                ],
            },
        }

    async def _handle_test_automate(self, request: TEARequest) -> Dict[str, Any]:
        """Handle test-automate task."""
        risk_level = request.risk_level or "medium"
        scope = request.scope or "feature"

        return {
            "success": True,
            "task": "test-automate",
            "guidance": {
                "title": "Test Automation Strategy",
                "risk_level": risk_level,
                "scope": scope,
                "test_prioritization": {
                    "high_priority": [
                        "Critical user flows",
                        "Core business logic",
                        "API endpoints with high traffic",
                        "Security and authentication",
                        "Payment and financial transactions",
                    ],
                    "medium_priority": [
                        "Secondary user flows",
                        "Data validation",
                        "Error handling",
                        "Integration points",
                    ],
                    "low_priority": [
                        "UI edge cases",
                        "Non-critical features",
                        "Cosmetic elements",
                    ],
                },
                "test_types": [
                    {
                        "type": "API Tests",
                        "description": "Service-layer testing for business logic",
                        "tools": ["pytest", "JUnit", "Go test", "RSpec"],
                        "priority": "high",
                    },
                    {
                        "type": "E2E Tests",
                        "description": "Full user journey testing",
                        "tools": ["Playwright", "Cypress"],
                        "priority": "medium",
                    },
                    {
                        "type": "Integration Tests",
                        "description": "Component interaction testing",
                        "tools": ["pytest", "JUnit"],
                        "priority": "high",
                    },
                ],
                "definition_of_done": [
                    "All acceptance criteria covered by tests",
                    "Critical paths have automated tests",
                    "Edge cases identified and tested",
                    "Tests are stable and non-flaky",
                    "Tests integrated into CI/CD pipeline",
                    "Test coverage meets minimum threshold",
                ],
            },
        }

    async def _handle_test_design(self, request: TEARequest) -> Dict[str, Any]:
        """Handle test-design task."""
        risk_level = request.risk_level or "medium"
        scope = request.scope or "epic"

        return {
            "success": True,
            "task": "test-design",
            "guidance": {
                "title": "Test Design and Coverage Strategy",
                "risk_level": risk_level,
                "scope": scope,
                "risk_assessment": {
                    "impact_factors": [
                        "User impact and frequency",
                        "Business criticality",
                        "Data sensitivity",
                        "Complexity and dependencies",
                        "Failure cost and recovery time",
                    ],
                    "risk_matrix": {
                        "high_impact_high_frequency": "Comprehensive testing (unit + integration + E2E)",
                        "high_impact_low_frequency": "Focused testing (unit + integration)",
                        "low_impact_high_frequency": "Standard testing (unit + integration)",
                        "low_impact_low_frequency": "Basic testing (unit)",
                    },
                },
                "coverage_strategy": {
                    "unit_tests": {
                        "target": "80%+ coverage",
                        "focus": "Business logic, algorithms, data transformations",
                    },
                    "integration_tests": {
                        "target": "Critical paths covered",
                        "focus": "API endpoints, database interactions, external services",
                    },
                    "e2e_tests": {
                        "target": "Key user journeys",
                        "focus": "Happy paths, critical workflows, cross-feature scenarios",
                    },
                },
                "test_categories": [
                    "Functional testing",
                    "Performance testing",
                    "Security testing",
                    "Usability testing",
                    "Compatibility testing",
                    "Regression testing",
                ],
            },
        }

    async def _handle_test_trace(self, request: TEARequest) -> Dict[str, Any]:
        """Handle test-trace task."""
        return {
            "success": True,
            "task": "test-trace",
            "guidance": {
                "title": "Requirements to Tests Traceability",
                "description": "Map requirements to tests and make quality gate decisions",
                "phase_1_traceability": {
                    "steps": [
                        "1. Identify all requirements (user stories, acceptance criteria)",
                        "2. Create requirement-to-test mapping matrix",
                        "3. Tag tests with requirement IDs",
                        "4. Identify orphan requirements (no tests)",
                        "5. Identify orphan tests (no requirements)",
                        "6. Calculate coverage metrics",
                    ],
                    "traceability_matrix": {
                        "requirement_id": "Unique identifier",
                        "requirement_description": "Brief description",
                        "test_ids": "List of test IDs covering this requirement",
                        "coverage_status": "covered / partial / not-covered",
                        "risk_level": "critical / high / medium / low",
                    },
                },
                "phase_2_quality_gate": {
                    "decision_criteria": [
                        "All critical requirements have tests",
                        "Coverage threshold met (e.g., 80%)",
                        "No high-risk requirements untested",
                        "All tests passing",
                        "No flaky tests in critical paths",
                    ],
                    "gate_outcomes": {
                        "pass": "All criteria met - ready for release",
                        "conditional": "Minor gaps - document and proceed with monitoring",
                        "fail": "Critical gaps - block release until addressed",
                    },
                },
                "recommendations": [
                    "Maintain traceability throughout development",
                    "Update traceability matrix as requirements change",
                    "Use automated tools for traceability reporting",
                    "Review traceability in sprint reviews",
                ],
            },
        }

    async def _handle_nfr_assess(self, request: TEARequest) -> Dict[str, Any]:
        """Handle nfr-assess task."""
        return {
            "success": True,
            "task": "nfr-assess",
            "guidance": {
                "title": "Non-Functional Requirements Assessment",
                "description": "Assess NFRs and recommend testing actions",
                "nfr_categories": [
                    {
                        "category": "Performance",
                        "metrics": [
                            "Response time",
                            "Throughput",
                            "Resource utilization",
                        ],
                        "testing": ["Load testing", "Stress testing", "Spike testing"],
                        "tools": ["k6", "JMeter", "Locust"],
                    },
                    {
                        "category": "Security",
                        "metrics": ["Vulnerability count", "Compliance score"],
                        "testing": [
                            "Penetration testing",
                            "Security scanning",
                            "Auth testing",
                        ],
                        "tools": ["OWASP ZAP", "Burp Suite", "Snyk"],
                    },
                    {
                        "category": "Reliability",
                        "metrics": ["Uptime", "MTBF", "MTTR"],
                        "testing": [
                            "Chaos engineering",
                            "Failover testing",
                            "Recovery testing",
                        ],
                        "tools": ["Chaos Monkey", "Gremlin", "Pumba"],
                    },
                    {
                        "category": "Scalability",
                        "metrics": [
                            "Concurrent users",
                            "Data volume",
                            "Transaction rate",
                        ],
                        "testing": ["Capacity planning", "Horizontal scaling tests"],
                        "tools": ["Kubernetes", "Docker Swarm", "AWS Auto Scaling"],
                    },
                    {
                        "category": "Usability",
                        "metrics": [
                            "Task completion rate",
                            "User satisfaction",
                            "Error rate",
                        ],
                        "testing": [
                            "Usability testing",
                            "A/B testing",
                            "Accessibility testing",
                        ],
                        "tools": ["UserTesting", "Hotjar", "axe DevTools"],
                    },
                ],
                "assessment_process": [
                    "1. Identify relevant NFRs for the system",
                    "2. Define measurable acceptance criteria",
                    "3. Design tests for each NFR",
                    "4. Establish baseline metrics",
                    "5. Run tests and collect data",
                    "6. Compare against acceptance criteria",
                    "7. Document findings and recommendations",
                ],
                "recommendations": [
                    "Define NFRs early in the project",
                    "Make NFRs testable and measurable",
                    "Include NFR testing in CI/CD pipeline",
                    "Monitor NFRs in production",
                ],
            },
        }

    async def _handle_continuous_integration(
        self, request: TEARequest
    ) -> Dict[str, Any]:
        """Handle continuous-integration task."""
        ci_platform = request.ci_platform or "github-actions"
        tech_stack = request.tech_stack or ["pytest"]

        return {
            "success": True,
            "task": "continuous-integration",
            "guidance": {
                "title": "CI/CD Quality Pipeline",
                "ci_platform": ci_platform,
                "tech_stack": tech_stack,
                "pipeline_stages": [
                    {
                        "stage": "Lint & Format",
                        "tools": ["ESLint", "Prettier", "Black", "Flake8"],
                        "purpose": "Code quality and consistency",
                    },
                    {
                        "stage": "Unit Tests",
                        "tools": tech_stack,
                        "purpose": "Verify business logic",
                        "threshold": "80% coverage",
                    },
                    {
                        "stage": "Integration Tests",
                        "tools": tech_stack,
                        "purpose": "Verify component interactions",
                    },
                    {
                        "stage": "Build",
                        "tools": ["Docker", "Webpack", "Vite"],
                        "purpose": "Package application",
                    },
                    {
                        "stage": "E2E Tests",
                        "tools": ["Playwright", "Cypress"],
                        "purpose": "Verify critical user journeys",
                    },
                    {
                        "stage": "Security Scan",
                        "tools": ["Snyk", "OWASP Dependency-Check"],
                        "purpose": "Identify vulnerabilities",
                    },
                    {
                        "stage": "Deploy",
                        "tools": [ci_platform],
                        "purpose": "Deploy to staging/production",
                    },
                ],
                "quality_gates": [
                    "All tests must pass",
                    "Coverage threshold must be met",
                    "No critical security vulnerabilities",
                    "No flaky tests allowed",
                    "Build time within acceptable limits",
                ],
                "best_practices": [
                    "Run fast tests first (unit > integration > E2E)",
                    "Parallelize test execution",
                    "Cache dependencies to speed up builds",
                    "Use test result artifacts for debugging",
                    "Set up notifications for build failures",
                    "Monitor build metrics and trends",
                ],
            },
        }

    async def _handle_test_review(self, request: TEARequest) -> Dict[str, Any]:
        """Handle test-review task."""
        return {
            "success": True,
            "task": "test-review",
            "guidance": {
                "title": "Test Quality Review",
                "description": "Perform quality check against written tests",
                "review_criteria": {
                    "test_structure": [
                        "Tests follow AAA pattern (Arrange-Act-Assert)",
                        "Descriptive test names",
                        "Single responsibility per test",
                        "Proper test organization",
                    ],
                    "test_isolation": [
                        "Tests are independent",
                        "No shared state between tests",
                        "Proper setup and teardown",
                        "Test data isolation",
                    ],
                    "assertions": [
                        "Clear and meaningful assertions",
                        "Appropriate assertion methods",
                        "Testing behavior not implementation",
                        "Edge cases covered",
                    ],
                    "maintainability": [
                        "DRY principle followed",
                        "Reusable fixtures and utilities",
                        "Clear test documentation",
                        "Easy to understand and modify",
                    ],
                    "performance": [
                        "Tests run efficiently",
                        "No unnecessary waits or sleeps",
                        "Proper mocking of external dependencies",
                        "Parallel execution support",
                    ],
                },
                "common_issues": [
                    "Flaky tests (intermittent failures)",
                    "Brittle tests (break with minor changes)",
                    "Slow tests (poor performance)",
                    "Over-mocking (testing nothing)",
                    "Testing implementation details",
                    "Missing edge cases",
                    "Poor test data management",
                ],
                "recommendations": [
                    "Review tests as part of code review process",
                    "Use static analysis tools for test quality",
                    "Monitor test flakiness metrics",
                    "Refactor tests regularly",
                    "Keep test code quality as high as production code",
                ],
            },
        }

    def _calculate_risk_score(self, impact: str, frequency: str) -> str:
        """Calculate risk score based on impact and frequency."""
        risk_matrix = {
            ("high", "high"): "critical",
            ("high", "medium"): "high",
            ("high", "low"): "medium",
            ("medium", "high"): "high",
            ("medium", "medium"): "medium",
            ("medium", "low"): "low",
            ("low", "high"): "medium",
            ("low", "medium"): "low",
            ("low", "low"): "low",
        }
        return risk_matrix.get((impact, frequency), "medium")

    def _get_test_recommendations(
        self, risk_level: str, project_type: str
    ) -> List[str]:
        """Get test recommendations based on risk level and project type."""
        recommendations = []

        if risk_level in ["high", "critical"]:
            recommendations.extend(
                [
                    "Comprehensive test coverage required",
                    "Include performance and security testing",
                    "Implement chaos engineering for reliability",
                    "Continuous monitoring in production",
                ]
            )

        if project_type == "api":
            recommendations.extend(
                [
                    "Focus on API contract testing",
                    "Use Pact for consumer-driven contracts",
                    "Test all endpoints with various inputs",
                ]
            )
        elif project_type == "web":
            recommendations.extend(
                [
                    "Implement E2E tests for critical user flows",
                    "Use Playwright or Cypress for UI automation",
                    "Include visual regression testing",
                ]
            )

        return recommendations
