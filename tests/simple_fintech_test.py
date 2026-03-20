"""Simple test script for FinTech pack agents."""

import sys
import os
import asyncio

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Import agents directly from their modules
import importlib.util


def load_agent(module_path, class_name):
    """Load an agent class from a file path."""
    spec = importlib.util.spec_from_file_location("agent_module", module_path)
    if spec is None:
        raise ImportError(f"Could not load spec from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


# Load agents
FinancialAnalystAgent = load_agent(
    os.path.join(
        os.path.dirname(__file__),
        "../app/packs/fintech/agents/financial-analyst/agent.py",
    ),
    "FinancialAnalystAgent",
)
ComplianceOfficerAgent = load_agent(
    os.path.join(
        os.path.dirname(__file__),
        "../app/packs/fintech/agents/compliance-officer/agent.py",
    ),
    "ComplianceOfficerAgent",
)
RiskManagerAgent = load_agent(
    os.path.join(
        os.path.dirname(__file__), "../app/packs/fintech/agents/risk-manager/agent.py"
    ),
    "RiskManagerAgent",
)


async def test_financial_analyst():
    """Test Financial Analyst agent."""
    print("Testing Financial Analyst agent...")
    agent = FinancialAnalystAgent()

    # Test get_info method
    info = agent.get_info()
    assert info is not None
    assert "name" in info
    assert info["name"] == "Financial Analyst"
    assert "capabilities" in info
    assert len(info["capabilities"]) > 0

    # Test process method with a simple request
    from dataclasses import dataclass

    @dataclass
    class FinancialAnalysisRequest:
        action: str
        financial_data: dict = None
        analysis_type: str = None
        time_period: str = None
        metrics: list = None

    request = FinancialAnalysisRequest(
        action="analyze",
        financial_data={"revenue": "5,000,000"},
        analysis_type="performance",
    )

    result = await agent.process(request)
    assert result is not None
    assert len(result) > 0
    print("✓ Financial Analyst agent test passed")
    return True


async def test_compliance_officer():
    """Test Compliance Officer agent."""
    print("Testing Compliance Officer agent...")
    agent = ComplianceOfficerAgent()

    # Test get_info method
    info = agent.get_info()
    assert info is not None
    assert "name" in info
    assert info["name"] == "Compliance Officer"
    assert "capabilities" in info
    assert len(info["capabilities"]) > 0

    # Test process method with a simple request
    from dataclasses import dataclass

    @dataclass
    class ComplianceRequest:
        action: str
        compliance_area: str = None
        jurisdiction: str = None
        data: dict = None
        requirements: list = None

    request = ComplianceRequest(
        action="assess", compliance_area="data_protection", jurisdiction="EU"
    )

    result = await agent.process(request)
    assert result is not None
    assert len(result) > 0
    print("✓ Compliance Officer agent test passed")
    return True


async def test_risk_manager():
    """Test Risk Manager agent."""
    print("Testing Risk Manager agent...")
    agent = RiskManagerAgent()

    # Test get_info method
    info = agent.get_info()
    assert info is not None
    assert "name" in info
    assert info["name"] == "Risk Manager"
    assert "capabilities" in info
    assert len(info["capabilities"]) > 0

    # Test process method with a simple request
    from dataclasses import dataclass

    @dataclass
    class RiskManagementRequest:
        action: str
        risk_category: str = None
        risk_data: dict = None
        time_horizon: str = None
        tolerance_level: str = None

    request = RiskManagementRequest(action="identify", risk_category="market")

    result = await agent.process(request)
    assert result is not None
    assert len(result) > 0
    print("✓ Risk Manager agent test passed")
    return True


async def main():
    """Run all tests."""
    print("=" * 60)
    print("FinTech Pack - Simple Agent Tests")
    print("=" * 60)
    print()

    all_passed = True

    try:
        all_passed &= await test_financial_analyst()
    except Exception as e:
        print(f"✗ Financial Analyst agent test failed: {e}")
        import traceback

        traceback.print_exc()
        all_passed = False

    print()

    try:
        all_passed &= await test_compliance_officer()
    except Exception as e:
        print(f"✗ Compliance Officer agent test failed: {e}")
        import traceback

        traceback.print_exc()
        all_passed = False

    print()

    try:
        all_passed &= await test_risk_manager()
    except Exception as e:
        print(f"✗ Risk Manager agent test failed: {e}")
        import traceback

        traceback.print_exc()
        all_passed = False

    print()
    print("=" * 60)
    if all_passed:
        print("All FinTech pack tests passed! ✓")
    else:
        print("Some tests failed! ✗")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    all_passed = asyncio.run(main())
    sys.exit(0 if all_passed else 1)
