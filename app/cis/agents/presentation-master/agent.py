"""
Presentation Master Agent

Visual communication expert specializing in presentation design, visual hierarchy, and information design.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class PresentationMasterRequest:
    """Request data structure for the Presentation Master agent."""

    presentation_type: str  # slide-deck, youtube-explainer, pitch-deck, conference-talk, infographic, visual-metaphor, concept-visual
    topic: str
    audience: Optional[str] = None
    key_messages: Optional[List[str]] = None
    style: str = "professional"  # professional, casual, bold, playful
    length: Optional[int] = None  # number of slides or minutes


class PresentationMaster:
    """
    Visual Communication + Presentation Expert.

    Master presentation designer who's dissected thousands of successful presentations.
    Expert in visual hierarchy, audience psychology, and information design.
    Expert in Excalidraw's frame-based presentation capabilities.

    Capabilities:
    - Create multi-slide presentations with professional layouts
    - Design YouTube/video explainer layouts
    - Craft investor pitch presentations
    - Build conference talk materials
    - Design creative information visualizations
    - Create conceptual illustrations
    - Generate expressive concept visuals
    - Apply visual hierarchy principles
    """

    def __init__(self):
        """Initialize the Presentation Master agent."""
        self.name = "Caravaggio"
        self.title = "Visual Communication + Presentation Expert"
        self.icon = "🎨"

    async def process(self, request: PresentationMasterRequest) -> Dict[str, Any]:
        """
        Process the presentation request and return design guidance.

        Args:
            request: The presentation request containing type and parameters

        Returns:
            A dictionary containing the presentation design and structure
        """
        # Validate request
        if not request.presentation_type:
            return {"success": False, "error": "Presentation type is required"}

        if not request.topic:
            return {"success": False, "error": "Topic is required"}

        # Generate presentation structure
        structure = self._generate_structure(request)

        # Create visual design guidelines
        visual_design = self._create_visual_design(request)

        # Provide content guidance
        content_guidance = self._create_content_guidance(request)

        return {
            "success": True,
            "agent": self.name,
            "title": self.title,
            "presentation_type": request.presentation_type,
            "topic": request.topic,
            "audience": request.audience,
            "style": request.style,
            "structure": structure,
            "visual_design": visual_design,
            "content_guidance": content_guidance,
            "principles": [
                "Know your audience - pitch decks ≠ YouTube thumbnails ≠ conference talks",
                "Visual hierarchy drives attention - design the eye's journey deliberately",
                "Clarity over cleverness - unless cleverness serves the message",
                "Every frame needs a job - inform, persuade, transition, or cut it",
                "Test the 3-second rule - can they grasp the core idea that fast?",
                "White space builds focus - cramming kills comprehension",
                "Consistency signals professionalism - establish and maintain visual language",
                "Story structure applies everywhere - hook, build tension, deliver payoff",
            ],
        }

    def _generate_structure(self, request: PresentationMasterRequest) -> Dict[str, Any]:
        """Generate the presentation structure based on type."""
        structures = {
            "slide-deck": {
                "type": "Multi-slide presentation",
                "recommended_slides": 10 - 20,
                "structure": [
                    {
                        "slide": 1,
                        "purpose": "Title/Hook",
                        "content": "Compelling title and attention-grabbing opening",
                    },
                    {
                        "slide": 2,
                        "purpose": "Agenda",
                        "content": "Clear roadmap of what's coming",
                    },
                    {
                        "slide": 3,
                        "purpose": "Problem",
                        "content": "Define the problem or opportunity",
                    },
                    {
                        "slide": 4,
                        "purpose": "Solution",
                        "content": "Present your solution or approach",
                    },
                    {
                        "slide": 5,
                        "purpose": "Details",
                        "content": "Key details and supporting information",
                    },
                    {
                        "slide": 6,
                        "purpose": "Evidence",
                        "content": "Data, examples, case studies",
                    },
                    {
                        "slide": 7,
                        "purpose": "Benefits",
                        "content": "What's in it for the audience",
                    },
                    {
                        "slide": 8,
                        "purpose": "Implementation",
                        "content": "How to make it happen",
                    },
                    {
                        "slide": 9,
                        "purpose": "Call to Action",
                        "content": "What should they do next",
                    },
                    {
                        "slide": 10,
                        "purpose": "Summary/Contact",
                        "content": "Key takeaways and contact info",
                    },
                ],
            },
            "youtube-explainer": {
                "type": "Video explainer layout",
                "recommended_duration": "5-10 minutes",
                "structure": [
                    {
                        "segment": 1,
                        "purpose": "Hook (0-30s)",
                        "content": "Grab attention immediately",
                    },
                    {
                        "segment": 2,
                        "purpose": "Problem (30s-2m)",
                        "content": "Explain the problem clearly",
                    },
                    {
                        "segment": 3,
                        "purpose": "Solution (2m-5m)",
                        "content": "Present your solution",
                    },
                    {
                        "segment": 4,
                        "purpose": "Proof (5m-7m)",
                        "content": "Show evidence and examples",
                    },
                    {
                        "segment": 5,
                        "purpose": "CTA (7m-end)",
                        "content": "Call to action and subscribe",
                    },
                ],
            },
            "pitch-deck": {
                "type": "Investor pitch presentation",
                "recommended_slides": 10 - 12,
                "structure": [
                    {
                        "slide": 1,
                        "purpose": "Title",
                        "content": "Company name and tagline",
                    },
                    {
                        "slide": 2,
                        "purpose": "Problem",
                        "content": "The problem you're solving",
                    },
                    {"slide": 3, "purpose": "Solution", "content": "Your solution"},
                    {
                        "slide": 4,
                        "purpose": "Market",
                        "content": "Market size and opportunity",
                    },
                    {
                        "slide": 5,
                        "purpose": "Product",
                        "content": "Product demo or screenshots",
                    },
                    {
                        "slide": 6,
                        "purpose": "Traction",
                        "content": "Milestones and metrics",
                    },
                    {
                        "slide": 7,
                        "purpose": "Business Model",
                        "content": "How you make money",
                    },
                    {
                        "slide": 8,
                        "purpose": "Competition",
                        "content": "Competitive landscape",
                    },
                    {
                        "slide": 9,
                        "purpose": "Team",
                        "content": "Founding team and advisors",
                    },
                    {
                        "slide": 10,
                        "purpose": "Financials",
                        "content": "Projections and funding needs",
                    },
                    {
                        "slide": 11,
                        "purpose": "Ask",
                        "content": "What you're asking for",
                    },
                    {
                        "slide": 12,
                        "purpose": "Contact",
                        "content": "Contact information",
                    },
                ],
            },
            "conference-talk": {
                "type": "Conference or workshop presentation",
                "recommended_duration": "20-45 minutes",
                "structure": [
                    {
                        "segment": 1,
                        "purpose": "Opening (5%)",
                        "content": "Hook and introduction",
                    },
                    {
                        "segment": 2,
                        "purpose": "Context (15%)",
                        "content": "Set the stage and context",
                    },
                    {
                        "segment": 3,
                        "purpose": "Main Content (60%)",
                        "content": "Core message with examples",
                    },
                    {
                        "segment": 4,
                        "purpose": "Application (15%)",
                        "content": "Practical applications",
                    },
                    {
                        "segment": 5,
                        "purpose": "Closing (5%)",
                        "content": "Summary and call to action",
                    },
                ],
            },
            "infographic": {
                "type": "Information visualization",
                "structure": [
                    {
                        "section": 1,
                        "purpose": "Header",
                        "content": "Title and subtitle",
                    },
                    {
                        "section": 2,
                        "purpose": "Introduction",
                        "content": "Brief context or hook",
                    },
                    {
                        "section": 3,
                        "purpose": "Data Visualization",
                        "content": "Charts, graphs, or data displays",
                    },
                    {
                        "section": 4,
                        "purpose": "Key Insights",
                        "content": "Main takeaways highlighted",
                    },
                    {
                        "section": 5,
                        "purpose": "Footer",
                        "content": "Sources and credits",
                    },
                ],
            },
            "visual-metaphor": {
                "type": "Conceptual illustration",
                "structure": [
                    {
                        "element": 1,
                        "purpose": "Central Concept",
                        "content": "Main idea or process",
                    },
                    {
                        "element": 2,
                        "purpose": "Supporting Elements",
                        "content": "Related concepts or steps",
                    },
                    {
                        "element": 3,
                        "purpose": "Connections",
                        "content": "Relationships and flows",
                    },
                    {
                        "element": 4,
                        "purpose": "Annotations",
                        "content": "Labels and explanations",
                    },
                ],
            },
            "concept-visual": {
                "type": "Single expressive image",
                "structure": [
                    {
                        "element": 1,
                        "purpose": "Core Message",
                        "content": "Main idea visually represented",
                    },
                    {
                        "element": 2,
                        "purpose": "Supporting Details",
                        "content": "Secondary visual elements",
                    },
                    {
                        "element": 3,
                        "purpose": "Text Overlay",
                        "content": "Minimal text for clarity",
                    },
                ],
            },
        }

        return structures.get(
            request.presentation_type, {"error": "Unknown presentation type"}
        )

    def _create_visual_design(
        self, request: PresentationMasterRequest
    ) -> Dict[str, Any]:
        """Create visual design guidelines."""
        return {
            "visual_hierarchy": [
                "Size matters - larger elements get more attention",
                "Color draws the eye - use strategically",
                "Contrast creates focus - make important elements stand out",
                "White space is your friend - don't cram",
                "Alignment creates order - align elements deliberately",
            ],
            "color_palette": {
                "primary": "Choose 1-2 primary colors for main elements",
                "secondary": "Use 1-2 secondary colors for accents",
                "neutral": "Use neutrals for backgrounds and text",
                "contrast": "Ensure sufficient contrast for readability",
            },
            "typography": {
                "headings": "Bold, larger font for titles and headers",
                "body": "Clean, readable font for main content",
                "accent": "Distinct font for emphasis or quotes",
                "hierarchy": "Establish clear typographic hierarchy",
            },
            "layout_principles": [
                "Grid-based layouts create structure",
                "Rule of thirds for visual balance",
                "F-pattern and Z-pattern for reading flow",
                "Consistent margins and spacing",
                "Visual balance and symmetry",
            ],
        }

    def _create_content_guidance(
        self, request: PresentationMasterRequest
    ) -> Dict[str, Any]:
        """Create content guidance."""
        return {
            "storytelling": [
                "Start with a hook - grab attention immediately",
                "Build tension - create interest and curiosity",
                "Deliver payoff - satisfy the audience's expectations",
                "Use narratives - stories are memorable",
                "Make it relatable - connect to audience experience",
            ],
            "content_principles": [
                "Less is more - one idea per slide/section",
                "Use visuals over text - show, don't tell",
                "Be specific - concrete examples over abstract concepts",
                "Keep it simple - avoid jargon and complexity",
                "Focus on audience - what's in it for them?",
            ],
            "engagement_techniques": [
                "Ask questions - provoke thought",
                "Use humor - when appropriate",
                "Include surprises - break patterns",
                "Create emotional connections - touch on feelings",
                "End strong - memorable closing",
            ],
        }
