"""
Scenario tests for Creative Problem Solver agent
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.cis.agents.creative_problem_solver import (
    CreativeProblemSolver,
    CreativeProblemSolverRequest,
)


async def test_problem_solving_basic():
    """Test basic problem solving."""
    agent = CreativeProblemSolver()
    request = CreativeProblemSolverRequest(
        problem="Customer retention is declining", methodology="systematic"
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["agent"] == "Dr. Quinn"
    assert result["problem"] == "Customer retention is declining"
    assert "problem_analysis" in result
    assert "methodology_results" in result
    assert "solutions" in result
    print("✓ test_problem_solving_basic passed")


async def test_problem_solving_triz():
    """Test problem solving with TRIZ methodology."""
    agent = CreativeProblemSolver()
    request = CreativeProblemSolverRequest(
        problem="Product is too expensive to manufacture", methodology="triz"
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["methodology"] == "triz"
    methodology = result["methodology_results"]
    assert methodology["methodology"] == "TRIZ (Theory of Inventive Problem Solving)"
    assert "principles" in methodology
    print("✓ test_problem_solving_triz passed")


async def test_problem_solving_toc():
    """Test problem solving with Theory of Constraints."""
    agent = CreativeProblemSolver()
    request = CreativeProblemSolverRequest(
        problem="Production bottleneck", methodology="toc"
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["methodology"] == "toc"
    methodology = result["methodology_results"]
    assert methodology["methodology"] == "Theory of Constraints"
    assert "five_focusing_steps" in methodology
    print("✓ test_problem_solving_toc passed")


async def test_problem_solving_systems_thinking():
    """Test problem solving with Systems Thinking."""
    agent = CreativeProblemSolver()
    request = CreativeProblemSolverRequest(
        problem="Organizational communication issues", methodology="systems-thinking"
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["methodology"] == "systems-thinking"
    methodology = result["methodology_results"]
    assert methodology["methodology"] == "Systems Thinking"
    assert "key_concepts" in methodology
    print("✓ test_problem_solving_systems_thinking passed")


async def test_problem_solving_with_context():
    """Test problem solving with context."""
    agent = CreativeProblemSolver()
    request = CreativeProblemSolverRequest(
        problem="Low user engagement",
        context="Mobile app for fitness tracking",
        constraints="Limited development resources",
        methodology="systematic",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["context"] == "Mobile app for fitness tracking"
    assert result["constraints"] == "Limited development resources"
    print("✓ test_problem_solving_with_context passed")


async def test_problem_solving_solutions():
    """Test that solutions are generated."""
    agent = CreativeProblemSolver()
    request = CreativeProblemSolverRequest(problem="High customer churn rate")
    result = await agent.process(request)
    assert result["success"] == True
    solutions = result["solutions"]
    assert len(solutions) > 0
    # Check solution structure
    for solution in solutions:
        assert "solution" in solution
        assert "description" in solution
        assert "feasibility" in solution
        assert "impact" in solution
        assert "effort" in solution
    print("✓ test_problem_solving_solutions passed")


async def test_problem_solving_action_plan():
    """Test that action plan is created."""
    agent = CreativeProblemSolver()
    request = CreativeProblemSolverRequest(problem="Inefficient workflow")
    result = await agent.process(request)
    assert result["success"] == True
    action_plan = result["action_plan"]
    assert "prioritization" in action_plan
    assert "implementation_steps" in action_plan
    assert "risk_mitigation" in action_plan
    assert "success_metrics" in action_plan
    print("✓ test_problem_solving_action_plan passed")


async def test_problem_solving_principles():
    """Test that problem-solving principles are included."""
    agent = CreativeProblemSolver()
    request = CreativeProblemSolverRequest(problem="Quality issues")
    result = await agent.process(request)
    assert result["success"] == True
    principles = result["principles"]
    assert len(principles) > 0
    assert "Every problem is a system revealing weaknesses" in principles
    print("✓ test_problem_solving_principles passed")


async def test_problem_solving_missing_problem():
    """Test problem solving with missing problem."""
    agent = CreativeProblemSolver()
    request = CreativeProblemSolverRequest(problem="")
    result = await agent.process(request)
    assert result["success"] == False
    assert "error" in result
    print("✓ test_problem_solving_missing_problem passed")


async def main():
    """Run all tests."""
    print("Running Creative Problem Solver agent tests...\n")

    await test_problem_solving_basic()
    await test_problem_solving_triz()
    await test_problem_solving_toc()
    await test_problem_solving_systems_thinking()
    await test_problem_solving_with_context()
    await test_problem_solving_solutions()
    await test_problem_solving_action_plan()
    await test_problem_solving_principles()
    await test_problem_solving_missing_problem()

    print("\n✅ All Creative Problem Solver tests passed!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
