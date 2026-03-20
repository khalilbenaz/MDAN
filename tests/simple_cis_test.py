"""
Simple integration test for all cis module agents
Tests that all agents can be imported and instantiated correctly
"""

import asyncio
import sys
import os
import importlib.util

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def load_agent_from_path(agent_path, agent_class_name):
    """Load an agent class from a file path using importlib"""
    spec = importlib.util.spec_from_file_location("agent_module", agent_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {agent_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, agent_class_name)


async def test_brainstorming_coach():
    """Test Brainstorming Coach Agent"""
    print("Testing Brainstorming Coach Agent (Carson)...")

    try:
        agent_path = os.path.join(
            os.path.dirname(__file__), "../app/cis/agents/brainstorming-coach/agent.py"
        )
        module = importlib.util.spec_from_file_location("agent_module", agent_path)
        if module is None or module.loader is None:
            raise ImportError(f"Could not load spec from {agent_path}")
        agent_module = importlib.util.module_from_spec(module)
        module.loader.exec_module(agent_module)

        BrainstormingCoach = agent_module.BrainstormingCoach
        BrainstormingCoachRequest = agent_module.BrainstormingCoachRequest

        agent = BrainstormingCoach()

        # Test basic processing
        request = BrainstormingCoachRequest(topic="product innovation", participants=5)
        result = await agent.process(request)

        assert result is not None
        assert isinstance(result, dict)
        print("✓ Brainstorming Coach Agent works correctly")
        return True
    except Exception as e:
        print(f"✗ Brainstorming Coach Agent failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_creative_problem_solver():
    """Test Creative Problem Solver Agent"""
    print("\nTesting Creative Problem Solver Agent (Dr. Quinn)...")

    try:
        agent_path = os.path.join(
            os.path.dirname(__file__),
            "../app/cis/agents/creative-problem-solver/agent.py",
        )
        module = importlib.util.spec_from_file_location("agent_module", agent_path)
        if module is None or module.loader is None:
            raise ImportError(f"Could not load spec from {agent_path}")
        agent_module = importlib.util.module_from_spec(module)
        module.loader.exec_module(agent_module)

        CreativeProblemSolver = agent_module.CreativeProblemSolver
        CreativeProblemSolverRequest = agent_module.CreativeProblemSolverRequest

        agent = CreativeProblemSolver()

        # Test basic processing
        request = CreativeProblemSolverRequest(
            problem="declining user engagement", constraints=["budget", "timeline"]
        )
        result = await agent.process(request)

        assert result is not None
        assert isinstance(result, dict)
        print("✓ Creative Problem Solver Agent works correctly")
        return True
    except Exception as e:
        print(f"✗ Creative Problem Solver Agent failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_design_thinking_coach():
    """Test Design Thinking Coach Agent"""
    print("\nTesting Design Thinking Coach Agent (Maya)...")

    try:
        agent_path = os.path.join(
            os.path.dirname(__file__),
            "../app/cis/agents/design-thinking-coach/agent.py",
        )
        module = importlib.util.spec_from_file_location("agent_module", agent_path)
        if module is None or module.loader is None:
            raise ImportError(f"Could not load spec from {agent_path}")
        agent_module = importlib.util.module_from_spec(module)
        module.loader.exec_module(agent_module)

        DesignThinkingCoach = agent_module.DesignThinkingCoach
        DesignThinkingCoachRequest = agent_module.DesignThinkingCoachRequest

        agent = DesignThinkingCoach()

        # Test basic processing
        request = DesignThinkingCoachRequest(
            challenge="improve mobile app UX", phase="empathize"
        )
        result = await agent.process(request)

        assert result is not None
        assert isinstance(result, dict)
        print("✓ Design Thinking Coach Agent works correctly")
        return True
    except Exception as e:
        print(f"✗ Design Thinking Coach Agent failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_innovation_strategist():
    """Test Innovation Strategist Agent"""
    print("\nTesting Innovation Strategist Agent (Victor)...")

    try:
        agent_path = os.path.join(
            os.path.dirname(__file__),
            "../app/cis/agents/innovation-strategist/agent.py",
        )
        module = importlib.util.spec_from_file_location("agent_module", agent_path)
        if module is None or module.loader is None:
            raise ImportError(f"Could not load spec from {agent_path}")
        agent_module = importlib.util.module_from_spec(module)
        module.loader.exec_module(agent_module)

        InnovationStrategist = agent_module.InnovationStrategist
        InnovationStrategistRequest = agent_module.InnovationStrategistRequest

        agent = InnovationStrategist()

        # Test basic processing
        request = InnovationStrategistRequest(
            market_context="fintech", goals=["growth", "differentiation"]
        )
        result = await agent.process(request)

        assert result is not None
        assert isinstance(result, dict)
        print("✓ Innovation Strategist Agent works correctly")
        return True
    except Exception as e:
        print(f"✗ Innovation Strategist Agent failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_presentation_master():
    """Test Presentation Master Agent"""
    print("\nTesting Presentation Master Agent (Caravaggio)...")

    try:
        agent_path = os.path.join(
            os.path.dirname(__file__), "../app/cis/agents/presentation-master/agent.py"
        )
        module = importlib.util.spec_from_file_location("agent_module", agent_path)
        if module is None or module.loader is None:
            raise ImportError(f"Could not load spec from {agent_path}")
        agent_module = importlib.util.module_from_spec(module)
        module.loader.exec_module(agent_module)

        PresentationMaster = agent_module.PresentationMaster
        PresentationMasterRequest = agent_module.PresentationMasterRequest

        agent = PresentationMaster()

        # Test basic processing
        request = PresentationMasterRequest(
            presentation_type="slide-deck",
            topic="quarterly results",
            audience="stakeholders",
            length=30,
        )
        result = await agent.process(request)

        assert result is not None
        assert isinstance(result, dict)
        print("✓ Presentation Master Agent works correctly")
        return True
    except Exception as e:
        print(f"✗ Presentation Master Agent failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_storyteller():
    """Test Storyteller Agent"""
    print("\nTesting Storyteller Agent (Sophia)...")

    try:
        agent_path = os.path.join(
            os.path.dirname(__file__), "../app/cis/agents/storyteller/agent.py"
        )
        module = importlib.util.spec_from_file_location("agent_module", agent_path)
        if module is None or module.loader is None:
            raise ImportError(f"Could not load spec from {agent_path}")
        agent_module = importlib.util.module_from_spec(module)
        module.loader.exec_module(agent_module)

        Storyteller = agent_module.Storyteller
        StorytellerRequest = agent_module.StorytellerRequest

        agent = Storyteller()

        # Test basic processing
        request = StorytellerRequest(
            story_purpose="brand", core_message="company transformation journey"
        )
        result = await agent.process(request)

        assert result is not None
        assert isinstance(result, dict)
        print("✓ Storyteller Agent works correctly")
        return True
    except Exception as e:
        print(f"✗ Storyteller Agent failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all cis module agent tests"""
    print("=" * 60)
    print("CIS Module - Integration Tests")
    print("=" * 60)

    tests = [
        test_brainstorming_coach(),
        test_creative_problem_solver(),
        test_design_thinking_coach(),
        test_innovation_strategist(),
        test_presentation_master(),
        test_storyteller(),
    ]

    results = await asyncio.gather(*tests)

    passed = sum(results)
    total = len(results)

    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} agents passed")
    print("=" * 60)

    if passed == total:
        print("✓ All CIS agents work correctly!")
        return 0
    else:
        print(f"✗ {total - passed} agent(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
