"""
Scenario tests for Storyteller Agent (Sophia)
Tests the Master Storyteller's ability to craft compelling narratives
"""

import asyncio
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.cis.agents.storyteller.agent import StorytellerAgent


class TestStorytellerAgent:
    """Test suite for Storyteller Agent scenarios"""

    def __init__(self):
        self.agent = StorytellerAgent()

    async def test_initialization(self):
        """Test 1: Agent initializes correctly"""
        print("Test 1: Agent initialization...")

        try:
            assert self.agent is not None
            assert hasattr(self.agent, "process")
            assert hasattr(self.agent, "name")
            assert self.agent.name == "storyteller"
            print("✓ Agent initializes correctly")
            return True
        except Exception as e:
            print(f"✗ Initialization failed: {e}")
            return False

    async def test_craft_narrative_framework(self):
        """Test 2: Craft narrative using proven frameworks"""
        print("\nTest 2: Craft narrative using frameworks...")

        try:
            input_data = {
                "task": "Craft a compelling narrative",
                "story_type": "brand story",
                "framework": "hero's journey",
                "context": "A sustainable fashion startup",
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            assert "response" in result or "narrative" in result or "story" in result
            print("✓ Narrative crafted successfully")
            return True
        except Exception as e:
            print(f"✗ Narrative crafting failed: {e}")
            return False

    async def test_emotional_psychology_application(self):
        """Test 3: Apply emotional psychology to storytelling"""
        print("\nTest 3: Apply emotional psychology...")

        try:
            input_data = {
                "task": "Create emotionally engaging story",
                "target_emotion": "inspiration",
                "audience": "young professionals",
                "theme": "overcoming challenges",
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            print("✓ Emotional psychology applied successfully")
            return True
        except Exception as e:
            print(f"✗ Emotional psychology application failed: {e}")
            return False

    async def test_audience_engagement_strategy(self):
        """Test 4: Develop audience engagement strategy"""
        print("\nTest 4: Develop audience engagement strategy...")

        try:
            input_data = {
                "task": "Create engagement strategy",
                "audience_segment": "millennials",
                "platform": "social media",
                "story_format": "short-form video",
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            print("✓ Engagement strategy developed successfully")
            return True
        except Exception as e:
            print(f"✗ Engagement strategy development failed: {e}")
            return False

    async def test_vivid_details_creation(self):
        """Test 5: Create vivid details for abstract concepts"""
        print("\nTest 5: Create vivid details...")

        try:
            input_data = {
                "task": "Make abstract concrete",
                "abstract_concept": "innovation",
                "context": "tech company transformation",
                "style": "flowery and whimsical",
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            print("✓ Vivid details created successfully")
            return True
        except Exception as e:
            print(f"✗ Vivid details creation failed: {e}")
            return False

    async def test_screenwriting_techniques(self):
        """Test 6: Apply screenwriting techniques"""
        print("\nTest 6: Apply screenwriting techniques...")

        try:
            input_data = {
                "task": "Use screenwriting techniques",
                "technique": "three-act structure",
                "story_elements": ["protagonist", "conflict", "resolution"],
                "genre": "drama",
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            print("✓ Screenwriting techniques applied successfully")
            return True
        except Exception as e:
            print(f"✗ Screenwriting techniques application failed: {e}")
            return False

    async def test_journalistic_storytelling(self):
        """Test 7: Apply journalistic storytelling approach"""
        print("\nTest 7: Apply journalistic storytelling...")

        try:
            input_data = {
                "task": "Create journalistic narrative",
                "story_angle": "human interest",
                "facts": ["company milestone", "customer impact", "team dedication"],
                "tone": "authentic and compelling",
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            print("✓ Journalistic storytelling applied successfully")
            return True
        except Exception as e:
            print(f"✗ Journalistic storytelling failed: {e}")
            return False

    async def test_brand_narrative_development(self):
        """Test 8: Develop brand narrative"""
        print("\nTest 8: Develop brand narrative...")

        try:
            input_data = {
                "task": "Create brand narrative",
                "brand_values": ["sustainability", "innovation", "quality"],
                "brand_mission": "Make the world better",
                "target_audience": "conscious consumers",
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            print("✓ Brand narrative developed successfully")
            return True
        except Exception as e:
            print(f"✗ Brand narrative development failed: {e}")
            return False

    async def test_story_structure_optimization(self):
        """Test 9: Optimize story structure"""
        print("\nTest 9: Optimize story structure...")

        try:
            input_data = {
                "task": "Optimize story structure",
                "current_story": "A company's journey from startup to success",
                "framework": "monomyth",
                "focus": "emotional arc",
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            print("✓ Story structure optimized successfully")
            return True
        except Exception as e:
            print(f"✗ Story structure optimization failed: {e}")
            return False

    async def test_multichannel_storytelling(self):
        """Test 10: Adapt story for multiple channels"""
        print("\nTest 10: Adapt story for multiple channels...")

        try:
            input_data = {
                "task": "Adapt story for channels",
                "core_story": "A product launch journey",
                "channels": ["blog", "video", "social media", "email"],
                "maintain_consistency": True,
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            print("✓ Multichannel storytelling adapted successfully")
            return True
        except Exception as e:
            print(f"✗ Multichannel storytelling failed: {e}")
            return False

    async def test_story_arc_creation(self):
        """Test 11: Create compelling story arc"""
        print("\nTest 11: Create story arc...")

        try:
            input_data = {
                "task": "Create story arc",
                "protagonist": "founder",
                "goal": "launch innovative product",
                "obstacles": ["funding", "competition", "technical challenges"],
                "theme": "perseverance",
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            print("✓ Story arc created successfully")
            return True
        except Exception as e:
            print(f"✗ Story arc creation failed: {e}")
            return False

    async def test_authentic_story_finding(self):
        """Test 12: Find authentic story elements"""
        print("\nTest 12: Find authentic story elements...")

        try:
            input_data = {
                "task": "Find authentic story",
                "company_context": "family business",
                "values": ["tradition", "quality", "community"],
                "differentiators": ["handmade", "local sourcing", "sustainable"],
            }

            result = await self.agent.process(input_data)

            assert result is not None
            assert isinstance(result, dict)
            print("✓ Authentic story elements found successfully")
            return True
        except Exception as e:
            print(f"✗ Authentic story finding failed: {e}")
            return False


async def run_all_tests():
    """Run all scenario tests for Storyteller Agent"""
    print("=" * 60)
    print("Storyteller Agent (Sophia) - Scenario Tests")
    print("=" * 60)

    test_suite = TestStorytellerAgent()

    tests = [
        test_suite.test_initialization(),
        test_suite.test_craft_narrative_framework(),
        test_suite.test_emotional_psychology_application(),
        test_suite.test_audience_engagement_strategy(),
        test_suite.test_vivid_details_creation(),
        test_suite.test_screenwriting_techniques(),
        test_suite.test_journalistic_storytelling(),
        test_suite.test_brand_narrative_development(),
        test_suite.test_story_structure_optimization(),
        test_suite.test_multichannel_storytelling(),
        test_suite.test_story_arc_creation(),
        test_suite.test_authentic_story_finding(),
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
