"""Scenario tests for Risk Manager agent."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.packs.fintech.agents.risk_manager.agent import RiskManager


def test_market_risk_assessment():
    """Test market risk assessment capability."""
    agent = RiskManager()

    input_data = {
        "task": "Assess market risk for investment portfolio",
        "portfolio": {
            "equities": {"value": "10,000,000", "beta": 1.2},
            "bonds": {"value": "5,000,000", "duration": 6.5},
        },
        "confidence_level": 95,
        "time_horizon": "10 days",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "market_risk" in result.lower() or "market risk" in result.lower()
    assert "var" in result.lower() or "value_at_risk" in result.lower()
    print("✓ Market risk assessment test passed")


def test_credit_risk_assessment():
    """Test credit risk assessment capability."""
    agent = RiskManager()

    input_data = {
        "task": "Assess credit risk for lending portfolio",
        "borrowers": [
            {"name": "Company A", "exposure": "1,000,000", "credit_rating": "A"},
            {"name": "Company B", "exposure": "500,000", "credit_rating": "BBB"},
            {"name": "Company C", "exposure": "2,000,000", "credit_rating": "AA"},
        ],
        "industry_concentration": {
            "Technology": 40,
            "Healthcare": 30,
            "Financials": 30,
        },
    }

    result = agent.process(input_data)

    assert result is not None
    assert "credit_risk" in result.lower() or "credit risk" in result.lower()
    assert "exposure" in result.lower()
    print("✓ Credit risk assessment test passed")


def test_operational_risk():
    """Test operational risk assessment capability."""
    agent = RiskManager()

    input_data = {
        "task": "Assess operational risks",
        "business_processes": ["Trading", "Settlement", "Customer Service"],
        "risk_factors": ["System failures", "Human error", "Fraud", "External events"],
    }

    result = agent.process(input_data)

    assert result is not None
    assert "operational_risk" in result.lower() or "operational risk" in result.lower()
    assert "mitigation" in result.lower() or "controls" in result.lower()
    print("✓ Operational risk test passed")


def test_stress_testing():
    """Test stress testing capability."""
    agent = RiskManager()

    input_data = {
        "task": "Perform stress testing on portfolio",
        "portfolio_value": "15,000,000",
        "scenarios": [
            {"name": "Market crash", "market_decline": "-20%"},
            {"name": "Interest rate spike", "rate_increase": "+200bps"},
            {"name": "Liquidity crisis", "liquidity_impact": "-30%"},
        ],
    }

    result = agent.process(input_data)

    assert result is not None
    assert "stress_test" in result.lower() or "stress test" in result.lower()
    assert "scenario" in result.lower()
    print("✓ Stress testing test passed")


def test_risk_mitigation():
    """Test risk mitigation strategy development capability."""
    agent = RiskManager()

    input_data = {
        "task": "Develop risk mitigation strategies",
        "identified_risks": [
            {"type": "Market risk", "level": "High"},
            {"type": "Credit risk", "level": "Medium"},
            {"type": "Operational risk", "level": "Medium"},
        ],
        "risk_appetite": "Moderate",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "mitigation" in result.lower()
    assert "strategy" in result.lower() or "strategies" in result.lower()
    print("✓ Risk mitigation test passed")


def test_risk_metrics():
    """Test risk metrics development capability."""
    agent = RiskManager()

    input_data = {
        "task": "Develop risk metrics and KPIs",
        "risk_types": ["Market", "Credit", "Operational", "Liquidity"],
        "reporting_frequency": "Monthly",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "metrics" in result.lower() or "kpi" in result.lower()
    assert "monitoring" in result.lower() or "reporting" in result.lower()
    print("✓ Risk metrics test passed")


def test_regulatory_compliance():
    """Test regulatory compliance for risk management capability."""
    agent = RiskManager()

    input_data = {
        "task": "Ensure risk management regulatory compliance",
        "regulations": ["Basel III", "Solvency II", "FRTB"],
        "organization_type": "Bank",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "compliance" in result.lower()
    assert "regulatory" in result.lower()
    print("✓ Regulatory compliance test passed")


if __name__ == "__main__":
    print("Running Risk Manager scenario tests...")
    print()

    test_market_risk_assessment()
    test_credit_risk_assessment()
    test_operational_risk()
    test_stress_testing()
    test_risk_mitigation()
    test_risk_metrics()
    test_regulatory_compliance()

    print()
    print("All Risk Manager tests passed! ✓")
