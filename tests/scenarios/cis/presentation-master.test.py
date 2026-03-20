"""
Scenario tests for Presentation Master agent
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.cis.agents.presentation_master import (
    PresentationMaster,
    PresentationMasterRequest,
)


async def test_presentation_slide_deck():
    """Test slide deck presentation."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(
        presentation_type="slide-deck",
        topic="Company quarterly review",
        audience="Board of directors",
        style="professional",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["agent"] == "Caravaggio"
    assert result["presentation_type"] == "slide-deck"
    assert result["topic"] == "Company quarterly review"
    assert result["audience"] == "Board of directors"
    assert "structure" in result
    assert "visual_design" in result
    print("✓ test_presentation_slide_deck passed")


async def test_presentation_youtube_explainer():
    """Test YouTube explainer presentation."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(
        presentation_type="youtube-explainer",
        topic="How blockchain works",
        audience="General public",
        style="engaging",
        length=8,
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["presentation_type"] == "youtube-explainer"
    assert result["length"] == 8
    structure = result["structure"]
    assert structure["type"] == "Video explainer layout"
    print("✓ test_presentation_youtube_explainer passed")


async def test_presentation_pitch_deck():
    """Test pitch deck presentation."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(
        presentation_type="pitch-deck",
        topic="AI-powered health monitoring app",
        audience="Venture capitalists",
        style="bold",
        key_messages=[
            "Revolutionary technology",
            "Large market opportunity",
            "Strong team",
        ],
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["presentation_type"] == "pitch-deck"
    assert result["key_messages"] == [
        "Revolutionary technology",
        "Large market opportunity",
        "Strong team",
    ]
    structure = result["structure"]
    assert structure["type"] == "Investor pitch presentation"
    print("✓ test_presentation_pitch_deck passed")


async def test_presentation_conference_talk():
    """Test conference talk presentation."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(
        presentation_type="conference-talk",
        topic="The future of remote work",
        audience="HR professionals",
        style="professional",
        length=30,
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["presentation_type"] == "conference-talk"
    assert result["length"] == 30
    structure = result["structure"]
    assert structure["type"] == "Conference or workshop presentation"
    print("✓ test_presentation_conference_talk passed")


async def test_presentation_infographic():
    """Test infographic presentation."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(
        presentation_type="infographic",
        topic="Climate change statistics",
        audience="General public",
        style="bold",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["presentation_type"] == "infographic"
    structure = result["structure"]
    assert structure["type"] == "Information visualization"
    print("✓ test_presentation_infographic passed")


async def test_presentation_visual_metaphor():
    """Test visual metaphor presentation."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(
        presentation_type="visual-metaphor",
        topic="Software development process",
        audience="New developers",
        style="playful",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["presentation_type"] == "visual-metaphor"
    structure = result["structure"]
    assert structure["type"] == "Conceptual illustration"
    print("✓ test_presentation_visual_metaphor passed")


async def test_presentation_concept_visual():
    """Test concept visual presentation."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(
        presentation_type="concept-visual",
        topic="Team collaboration",
        audience="Company employees",
        style="engaging",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["presentation_type"] == "concept-visual"
    structure = result["structure"]
    assert structure["type"] == "Single expressive image"
    print("✓ test_presentation_concept_visual passed")


async def test_presentation_visual_design():
    """Test that visual design guidelines are provided."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(
        presentation_type="slide-deck", topic="Product launch"
    )
    result = await agent.process(request)
    assert result["success"] == True
    visual_design = result["visual_design"]
    assert "visual_hierarchy" in visual_design
    assert "color_palette" in visual_design
    assert "typography" in visual_design
    assert "layout_principles" in visual_design
    print("✓ test_presentation_visual_design passed")


async def test_presentation_content_guidance():
    """Test that content guidance is provided."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(
        presentation_type="slide-deck", topic="Marketing strategy"
    )
    result = await agent.process(request)
    assert result["success"] == True
    content_guidance = result["content_guidance"]
    assert "storytelling" in content_guidance
    assert "content_principles" in content_guidance
    assert "engagement_techniques" in content_guidance
    print("✓ test_presentation_content_guidance passed")


async def test_presentation_principles():
    """Test that presentation principles are included."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(
        presentation_type="slide-deck", topic="Annual report"
    )
    result = await agent.process(request)
    assert result["success"] == True
    principles = result["principles"]
    assert len(principles) > 0
    assert "Know your audience" in principles[0]
    print("✓ test_presentation_principles passed")


async def test_presentation_missing_type():
    """Test presentation with missing type."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(presentation_type="", topic="Some topic")
    result = await agent.process(request)
    assert result["success"] == False
    assert "error" in result
    print("✓ test_presentation_missing_type passed")


async def test_presentation_missing_topic():
    """Test presentation with missing topic."""
    agent = PresentationMaster()
    request = PresentationMasterRequest(presentation_type="slide-deck", topic="")
    result = await agent.process(request)
    assert result["success"] == False
    assert "error" in result
    print("✓ test_presentation_missing_topic passed")


async def main():
    """Run all tests."""
    print("Running Presentation Master agent tests...\n")

    await test_presentation_slide_deck()
    await test_presentation_youtube_explainer()
    await test_presentation_pitch_deck()
    await test_presentation_conference_talk()
    await test_presentation_infographic()
    await test_presentation_visual_metaphor()
    await test_presentation_concept_visual()
    await test_presentation_visual_design()
    await test_presentation_content_guidance()
    await test_presentation_principles()
    await test_presentation_missing_type()
    await test_presentation_missing_topic()

    print("\n✅ All Presentation Master tests passed!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
