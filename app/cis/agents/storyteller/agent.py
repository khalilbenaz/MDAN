"""
Storyteller Agent

Expert storytelling guide specializing in narrative strategy, emotional psychology, and audience engagement.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class StorytellerRequest:
    """Request data structure for the Storyteller agent."""

    story_purpose: str  # brand, product, educational, inspirational, entertainment
    core_message: str
    audience: Optional[str] = None
    tone: str = "engaging"  # engaging, emotional, humorous, dramatic, inspirational
    format: str = "narrative"  # narrative, script, blog, social, presentation
    length: Optional[str] = None  # short, medium, long


class Storyteller:
    """
    Master Storyteller.

    Master storyteller with 50+ years across journalism, screenwriting, and brand narratives.
    Expert in emotional psychology and audience engagement.

    Capabilities:
    - Craft compelling narratives using proven frameworks
    - Apply storytelling principles across formats
    - Create emotional connections with audiences
    - Structure stories for maximum impact
    - Use vivid details and sensory language
    - Adapt stories for different contexts
    - Leverage timeless human truths
    """

    def __init__(self):
        """Initialize the Storyteller agent."""
        self.name = "Sophia"
        self.title = "Master Storyteller"
        self.icon = "📖"

    async def process(self, request: StorytellerRequest) -> Dict[str, Any]:
        """
        Process the storytelling request and return narrative guidance.

        Args:
            request: The storytelling request containing purpose and parameters

        Returns:
            A dictionary containing the story structure and guidance
        """
        # Validate request
        if not request.story_purpose:
            return {"success": False, "error": "Story purpose is required"}

        if not request.core_message:
            return {"success": False, "error": "Core message is required"}

        # Generate story structure
        structure = self._generate_structure(request)

        # Create narrative framework
        framework = self._create_framework(request)

        # Provide storytelling guidance
        guidance = self._create_guidance(request)

        return {
            "success": True,
            "agent": self.name,
            "title": self.title,
            "story_purpose": request.story_purpose,
            "core_message": request.core_message,
            "audience": request.audience,
            "tone": request.tone,
            "format": request.format,
            "structure": structure,
            "framework": framework,
            "guidance": guidance,
            "principles": [
                "Powerful narratives leverage timeless human truths",
                "Find the authentic story",
                "Make the abstract concrete through vivid details",
                "Emotion drives engagement",
                "Conflict creates interest",
                "Transformation resonates",
                "Specificity creates universality",
            ],
        }

    def _generate_structure(self, request: StorytellerRequest) -> Dict[str, Any]:
        """Generate the story structure."""
        return {
            "classic_structure": {
                "name": "Three-Act Structure",
                "acts": [
                    {
                        "act": 1,
                        "name": "Setup",
                        "purpose": "Establish the world, characters, and status quo",
                        "elements": [
                            "Introduction to protagonist",
                            "Establish the ordinary world",
                            "Inciting incident that disrupts status quo",
                        ],
                    },
                    {
                        "act": 2,
                        "name": "Confrontation",
                        "purpose": "Protagonist faces challenges and obstacles",
                        "elements": [
                            "Rising action and complications",
                            "Midpoint - shift in direction",
                            "All is lost moment - lowest point",
                        ],
                    },
                    {
                        "act": 3,
                        "name": "Resolution",
                        "purpose": "Protagonist overcomes and transforms",
                        "elements": [
                            "Climax - final confrontation",
                            "Falling action - consequences",
                            "Resolution - new normal",
                        ],
                    },
                ],
            },
            "alternative_structures": [
                {
                    "name": "Hero's Journey",
                    "description": "Monomyth structure with 12 stages",
                    "best_for": "Epic narratives, transformation stories",
                },
                {
                    "name": "In Media Res",
                    "description": "Start in the middle of the action",
                    "best_for": "Grabbing attention immediately",
                },
                {
                    "name": "Non-linear",
                    "description": "Jump between time periods",
                    "best_for": "Mystery, revealing information gradually",
                },
                {
                    "name": "Circular",
                    "description": "End where you began",
                    "best_for": "Showing transformation, coming full circle",
                },
            ],
        }

    def _create_framework(self, request: StorytellerRequest) -> Dict[str, Any]:
        """Create the narrative framework."""
        frameworks = {
            "brand": {
                "framework": "Brand Story Framework",
                "elements": [
                    {"element": "Origin", "description": "Why does this brand exist?"},
                    {
                        "element": "Mission",
                        "description": "What problem does it solve?",
                    },
                    {"element": "Values", "description": "What does it stand for?"},
                    {"element": "Impact", "description": "How does it change lives?"},
                    {"element": "Vision", "description": "Where is it going?"},
                ],
            },
            "product": {
                "framework": "Product Story Framework",
                "elements": [
                    {"element": "Problem", "description": "What pain point exists?"},
                    {
                        "element": "Discovery",
                        "description": "How was the solution found?",
                    },
                    {"element": "Solution", "description": "What does the product do?"},
                    {"element": "Benefit", "description": "How does it help?"},
                    {
                        "element": "Transformation",
                        "description": "What changes for the user?",
                    },
                ],
            },
            "educational": {
                "framework": "Educational Story Framework",
                "elements": [
                    {"element": "Hook", "description": "Grab attention with curiosity"},
                    {
                        "element": "Context",
                        "description": "Provide necessary background",
                    },
                    {
                        "element": "Journey",
                        "description": "Guide through learning process",
                    },
                    {"element": "Insight", "description": "Reveal key understanding"},
                    {"element": "Application", "description": "Show how to use it"},
                ],
            },
            "inspirational": {
                "framework": "Inspirational Story Framework",
                "elements": [
                    {"element": "Struggle", "description": "Show the challenge"},
                    {"element": "Persistence", "description": "Demonstrate resilience"},
                    {"element": "Breakthrough", "description": "Moment of success"},
                    {"element": "Lesson", "description": "What was learned"},
                    {"element": "Call to Action", "description": "Inspire others"},
                ],
            },
            "entertainment": {
                "framework": "Entertainment Story Framework",
                "elements": [
                    {
                        "element": "Setup",
                        "description": "Establish interesting situation",
                    },
                    {"element": "Complication", "description": "Introduce conflict"},
                    {"element": "Escalation", "description": "Raise the stakes"},
                    {"element": "Climax", "description": "Peak excitement"},
                    {"element": "Resolution", "description": "Satisfying conclusion"},
                ],
            },
        }

        return frameworks.get(request.story_purpose, frameworks["entertainment"])

    def _create_guidance(self, request: StorytellerRequest) -> Dict[str, Any]:
        """Create storytelling guidance."""
        return {
            "narrative_techniques": [
                {
                    "technique": "Show, Don't Tell",
                    "description": "Use actions and details to reveal information",
                    "example": "Instead of saying he was nervous, describe his trembling hands",
                },
                {
                    "technique": "Sensory Details",
                    "description": "Engage all five senses",
                    "example": "The smell of rain, the sound of distant thunder",
                },
                {
                    "technique": "Active Voice",
                    "description": "Make subjects do actions",
                    "example": "She opened the door vs The door was opened by her",
                },
                {
                    "technique": "Specific Details",
                    "description": "Use concrete, specific language",
                    "example": "A 1967 Mustang vs an old car",
                },
                {
                    "technique": "Pacing",
                    "description": "Vary sentence length for rhythm",
                    "example": "Short sentences for action, longer for reflection",
                },
            ],
            "emotional_arcs": [
                {
                    "arc": "Rags to Riches",
                    "pattern": "Rise from nothing to everything",
                    "emotion": "Hope, triumph",
                },
                {
                    "arc": "Overcoming the Monster",
                    "pattern": "Face and defeat a great evil",
                    "emotion": "Courage, victory",
                },
                {
                    "arc": "The Quest",
                    "pattern": "Journey to achieve a goal",
                    "emotion": "Determination, achievement",
                },
                {
                    "arc": "Voyage and Return",
                    "pattern": "Go to strange world, return changed",
                    "emotion": "Wonder, growth",
                },
                {
                    "arc": "Tragedy",
                    "pattern": "Fall from grace due to flaw",
                    "emotion": "Pity, fear, catharsis",
                },
                {
                    "arc": "Rebirth",
                    "pattern": "Redemption through transformation",
                    "emotion": "Hope, renewal",
                },
            ],
            "engagement_tips": [
                "Start with a hook that grabs attention",
                "Create relatable characters",
                "Build tension through conflict",
                "Use dialogue to reveal character",
                "End with a satisfying resolution",
                "Leave room for interpretation",
                "Make every word earn its place",
            ],
        }
