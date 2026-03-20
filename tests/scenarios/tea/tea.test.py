"""
Scenario tests for TEA Agent (Murat)
Tests the Master Test Architect's ability to provide testing guidance
"""

import asyncio
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.tea.agents.tea.agent import TEA, TEARequest


class TestTEAAgent:
    """Test suite for TEA Agent scenarios"""

    def __init__(self):
        self.agent = TEA()

    async def test_initialization(self):
        """Test 1: Agent initializes correctly"""
        print("Test 1: Agent initialization...")

        try:
            assert self.agent is not None
            assert hasattr(self.agent, "process")
            assert hasattr(self.agent, "name")
            assert self.agent.name == "Murat"
            print("✓ Agent initializes correctly")
            return True
        except Exception as e:
            print(f"✗ Initialization failed: {e}")
            return False

    async def test_teach_me_testing(self):
        """Test 2: Teach testing fundamentals"""
        print("\nTest 2: Teach me testing...")

        try:
            request = TEARequest(
                task="teach-me-testing", context="I want to learn testing from scratch"
            )

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            assert "sessions" in result["guidance"]
            assert len(result["guidance"]["sessions"]) == 7
            print("✓ Teach me testing works correctly")
            return True
        except Exception as e:
            print(f"✗ Teach me testing failed: {e}")
            return False

    async def test_test_framework(self):
        """Test 3: Initialize test framework"""
        print("\nTest 3: Test framework initialization...")

        try:
            request = TEARequest(
                task="test-framework",
                context="Setting up test framework for a web app",
                project_type="web",
                tech_stack=["pytest", "playwright"],
            )

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            assert "architecture" in result["guidance"]
            print("✓ Test framework initialization works correctly")
            return True
        except Exception as e:
            print(f"✗ Test framework initialization failed: {e}")
            return False

    async def test_atdd(self):
        """Test 4: Acceptance Test-Driven Development"""
        print("\nTest 4: ATDD guidance...")

        try:
            request = TEARequest(task="atdd", context="User login feature")

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            assert "acceptance_test_template" in result["guidance"]
            assert "implementation_checklist" in result["guidance"]
            print("✓ ATDD guidance works correctly")
            return True
        except Exception as e:
            print(f"✗ ATDD guidance failed: {e}")
            return False

    async def test_test_automate(self):
        """Test 5: Test automation strategy"""
        print("\nTest 5: Test automation strategy...")

        try:
            request = TEARequest(
                task="test-automate",
                context="Automate tests for payment feature",
                risk_level="high",
                scope="feature",
            )

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            assert "test_prioritization" in result["guidance"]
            assert "definition_of_done" in result["guidance"]
            print("✓ Test automation strategy works correctly")
            return True
        except Exception as e:
            print(f"✗ Test automation strategy failed: {e}")
            return False

    async def test_test_design(self):
        """Test 6: Test design and coverage strategy"""
        print("\nTest 6: Test design strategy...")

        try:
            request = TEARequest(
                task="test-design",
                context="Design test strategy for e-commerce platform",
                risk_level="high",
                scope="epic",
            )

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            assert "risk_assessment" in result["guidance"]
            assert "coverage_strategy" in result["guidance"]
            print("✓ Test design strategy works correctly")
            return True
        except Exception as e:
            print(f"✗ Test design strategy failed: {e}")
            return False

    async def test_test_trace(self):
        """Test 7: Requirements to tests traceability"""
        print("\nTest 7: Test traceability...")

        try:
            request = TEARequest(
                task="test-trace", context="Map requirements to tests for release"
            )

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            assert "phase_1_traceability" in result["guidance"]
            assert "phase_2_quality_gate" in result["guidance"]
            print("✓ Test traceability works correctly")
            return True
        except Exception as e:
            print(f"✗ Test traceability failed: {e}")
            return False

    async def test_nfr_assess(self):
        """Test 8: Non-Functional Requirements assessment"""
        print("\nTest 8: NFR assessment...")

        try:
            request = TEARequest(
                task="nfr-assess", context="Assess NFRs for high-traffic API"
            )

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            assert "nfr_categories" in result["guidance"]
            assert len(result["guidance"]["nfr_categories"]) >= 5
            print("✓ NFR assessment works correctly")
            return True
        except Exception as e:
            print(f"✗ NFR assessment failed: {e}")
            return False

    async def test_continuous_integration(self):
        """Test 9: CI/CD quality pipeline"""
        print("\nTest 9: Continuous integration guidance...")

        try:
            request = TEARequest(
                task="continuous-integration",
                context="Set up CI/CD pipeline for microservices",
                ci_platform="github-actions",
                tech_stack=["pytest", "go-test"],
            )

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            assert "pipeline_stages" in result["guidance"]
            assert "quality_gates" in result["guidance"]
            print("✓ Continuous integration guidance works correctly")
            return True
        except Exception as e:
            print(f"✗ Continuous integration guidance failed: {e}")
            return False

    async def test_test_review(self):
        """Test 10: Test quality review"""
        print("\nTest 10: Test quality review...")

        try:
            request = TEARequest(
                task="test-review", context="Review test suite for quality issues"
            )

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            assert "review_criteria" in result["guidance"]
            assert "common_issues" in result["guidance"]
            print("✓ Test quality review works correctly")
            return True
        except Exception as e:
            print(f"✗ Test quality review failed: {e}")
            return False

    async def test_risk_based_testing(self):
        """Test 11: Risk-based testing approach"""
        print("\nTest 11: Risk-based testing...")

        try:
            request = TEARequest(
                task="test-design",
                context="Apply risk-based testing to critical payment system",
                risk_level="critical",
                scope="system",
            )

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            assert "risk_assessment" in result["guidance"]
            print("✓ Risk-based testing works correctly")
            return True
        except Exception as e:
            print(f"✗ Risk-based testing failed: {e}")
            return False

    async def test_api_testing_focus(self):
        """Test 12: API testing as first-class citizen"""
        print("\nTest 12: API testing focus...")

        try:
            request = TEARequest(
                task="test-automate",
                context="Automate API tests for REST service",
                project_type="api",
                tech_stack=["pytest"],
                risk_level="high",
            )

            result = await self.agent.process(request)

            assert result is not None
            assert isinstance(result, dict)
            assert result["success"] == True
            assert "guidance" in result
            print("✓ API testing focus works correctly")
            return True
        except Exception as e:
            print(f"✗ API testing focus failed: {e}")
            return False


async def run_all_tests():
    """Run all scenario tests for TEA Agent"""
    print("=" * 60)
    print("TEA Agent (Murat) - Scenario Tests")
    print("=" * 60)

    test_suite = TestTEAAgent()

    tests = [
        test_suite.test_initialization(),
        test_suite.test_teach_me_testing(),
        test_suite.test_test_framework(),
        test_suite.test_atdd(),
        test_suite.test_test_automate(),
        test_suite.test_test_design(),
        test_suite.test_test_trace(),
        test_suite.test_nfr_assess(),
        test_suite.test_continuous_integration(),
        test_suite.test_test_review(),
        test_suite.test_risk_based_testing(),
        test_suite.test_api_testing_focus(),
    ]

    results = await asyncio.gather(*tests)

    passed = sum(results)
    total = len(results)

    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} passed")
    print("=" * 60)

    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
