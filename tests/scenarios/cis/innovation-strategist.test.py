"""
Scenario tests for Innovation Strategist agent
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.cis.agents.innovation_strategist import (
    InnovationStrategist,
    InnovationStrategistRequest,
)


async def test_innovation_strategy_basic():
    """Test basic innovation strategy."""
    agent = InnovationStrategist()
    request = InnovationStrategistRequest(
        market_context="E-commerce industry", goals="disruption"
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["agent"] == "Victor"
    assert result["market_context"] == "E-commerce industry"
    assert result["goals"] == "disruption"
    assert "market_analysis" in result
    assert "framework_analysis" in result
    assert "opportunities" in result
    print("✓ test_innovation_strategy_basic passed")


async def test_innovation_strategy_with_offering():
    """Test innovation strategy with current offering."""
    agent = InnovationStrategist()
    request = InnovationStrategistRequest(
        market_context="Food delivery market",
        current_offering="Traditional restaurant delivery service",
        goals="disruption",
        timeframe="medium-term",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["current_offering"] == "Traditional restaurant delivery service"
    assert result["timeframe"] == "medium-term"
    print("✓ test_innovation_strategy_with_offering passed")


async def test_innovation_strategy_short_term():
    """Test innovation strategy with short-term timeframe."""
    agent = InnovationStrategist()
    request = InnovationStrategistRequest(
        market_context="Mobile app market", goals="growth", timeframe="short-term"
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["timeframe"] == "short-term"
    roadmap = result["roadmap"]
    assert "focus" in roadmap
    assert "phases" in roadmap
    print("✓ test_innovation_strategy_short_term passed")


async def test_innovation_strategy_long_term():
    """Test innovation strategy with long-term timeframe."""
    agent = InnovationStrategist()
    request = InnovationStrategistRequest(
        market_context="Automotive industry",
        goals="transformation",
        timeframe="long-term",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["timeframe"] == "long-term"
    roadmap = result["roadmap"]
    assert "focus" in roadmap
    assert "phases" in roadmap
    print("✓ test_innovation_strategy_long_term passed")


async def test_innovation_strategy_with_constraints():
    """Test innovation strategy with constraints."""
    agent = InnovationStrategist()
    request = InnovationStrategistRequest(
        market_context="Healthcare technology",
        current_offering="Basic telemedicine platform",
        goals="disruption",
        constraints="Regulatory compliance required, limited funding",
        timeframe="medium-term",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["constraints"] == "Regulatory compliance required, limited funding"
    print("✓ test_innovation_strategy_with_constraints passed")


async def test_innovation_strategy_frameworks():
    """Test that strategic frameworks are applied."""
    agent = InnovationStrategist()
    request = InnovationStrategistRequest(market_context="SaaS market")
    result = await agent.process(request)
    assert result["success"] == True
    frameworks = result["framework_analysis"]
    assert "jobs_to_be_done" in frameworks
    assert "blue_ocean_strategy" in frameworks
    assert "business_model_innovation" in frameworks
    print("✓ test_innovation_strategy_frameworks passed")


async def test_innovation_strategy_opportunities():
    """Test that innovation opportunities are identified."""
    agent = InnovationStrategist()
    request = InnovationStrategistRequest(market_context="Fintech industry")
    result = await agent.process(request)
    assert result["success"] == True
    opportunities = result["opportunities"]
    assert len(opportunities) > 0
    # Check opportunity structure
    for opportunity in opportunities:
        assert "opportunity" in opportunity
        assert "description" in opportunity
        assert "potential_impact" in opportunity
        assert "feasibility" in opportunity
        assert "time_to_market" in opportunity
    print("✓ test_innovation_strategy_opportunities passed")


async def test_innovation_strategy_roadmap():
    """Test that strategic roadmap is created."""
    agent = InnovationStrategist()
    request = InnovationStrategistRequest(
        market_context="Retail industry", timeframe="medium-term"
    )
    result = await agent.process(request)
    assert result["success"] == True
    roadmap = result["roadmap"]
    assert "focus" in roadmap
    assert "phases" in roadmap
    phases = roadmap["phases"]
    assert len(phases) > 0
    # Check phase structure
    for phase in phases:
        assert "phase" in phase
        assert "activities" in phase
    print("✓ test_innovation_strategy_roadmap passed")


async def test_innovation_strategy_principles():
    """Test that innovation principles are included."""
    agent = InnovationStrategist()
    request = InnovationStrategistRequest(market_context="Technology sector")
    result = await agent.process(request)
    assert result["success"] == True
    principles = result["principles"]
    assert len(principles) > 0
    assert "Markets reward genuine new value" in principles
    print("✓ test_innovation_strategy_principles passed")


async def test_innovation_strategy_missing_context():
    """Test innovation strategy with missing market context."""
    agent = InnovationStrategist()
    request = InnovationStrategistRequest(market_context="")
    result = await agent.process(request)
    assert result["success"] == False
    assert "error" in result
    print("✓ test_innovation_strategy_missing_context passed")


async def main():
    """Run all tests."""
    print("Running Innovation Strategist agent tests...\n")

    await test_innovation_strategy_basic()
    await test_innovation_strategy_with_offering()
    await test_innovation_strategy_short_term()
    await test_innovation_strategy_long_term()
    await test_innovation_strategy_with_constraints()
    await test_innovation_strategy_frameworks()
    await test_innovation_strategy_opportunities()
    await test_innovation_strategy_roadmap()
    await test_innovation_strategy_principles()
    await test_innovation_strategy_missing_context()

    print("\n✅ All Innovation Strategist tests passed!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
