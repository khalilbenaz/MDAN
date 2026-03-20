"""
Brainstorming Coach Agent

Elite facilitator for creative brainstorming sessions and innovation workshops.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class BrainstormingCoachRequest:
    """Request data structure for the Brainstorming Coach agent."""

    topic: str
    session_type: str = "standard"  # standard, party-mode, focused
    participants: Optional[int] = None
    constraints: Optional[str] = None
    goals: Optional[str] = None


class BrainstormingCoach:
    """
    Elite Brainstorming Specialist.

    Master facilitator with 20+ years leading breakthrough sessions.
    Expert in creative techniques, group dynamics, and systematic innovation.

    Capabilities:
    - Guide brainstorming sessions on any topic
    - Facilitate creative ideation techniques
    - Build on ideas with YES AND approach
    - Create psychologically safe environments
    - Celebrate wild thinking and breakthrough ideas
    - Apply systematic innovation methodologies
    """

    def __init__(self):
        """Initialize the Brainstorming Coach agent."""
        self.name = "Carson"
        self.title = "Elite Brainstorming Specialist"
        self.icon = "🧠"

    async def process(self, request: BrainstormingCoachRequest) -> Dict[str, Any]:
        """
        Process the brainstorming request and return facilitation guidance.

        Args:
            request: The brainstorming request containing topic and parameters

        Returns:
            A dictionary containing the brainstorming session plan and techniques
        """
        # Validate request
        if not request.topic:
            return {
                "success": False,
                "error": "Topic is required for brainstorming session",
            }

        # Generate brainstorming session plan
        session_plan = self._generate_session_plan(request)

        # Select appropriate techniques
        techniques = self._select_techniques(request)

        # Create facilitation guide
        facilitation_guide = self._create_facilitation_guide(request)

        return {
            "success": True,
            "agent": self.name,
            "title": self.title,
            "topic": request.topic,
            "session_type": request.session_type,
            "session_plan": session_plan,
            "techniques": techniques,
            "facilitation_guide": facilitation_guide,
            "principles": [
                "Psychological safety unlocks breakthroughs",
                "Wild ideas today become innovations tomorrow",
                "Humor and play are serious innovation tools",
                "Build on ideas with YES AND approach",
                "Quantity leads to quality in brainstorming",
            ],
        }

    def _generate_session_plan(
        self, request: BrainstormingCoachRequest
    ) -> Dict[str, Any]:
        """Generate a structured session plan."""
        return {
            "warm_up": "Quick icebreaker to get creative juices flowing",
            "ideation_phase": "Rapid idea generation without judgment",
            "expansion_phase": "Build on and combine ideas",
            "convergence_phase": "Select and refine best ideas",
            "action_planning": "Define next steps for implementation",
        }

    def _select_techniques(self, request: BrainstormingCoachRequest) -> list:
        """Select appropriate brainstorming techniques."""
        techniques = [
            {
                "name": "Classic Brainstorming",
                "description": "Free-flowing idea generation with no judgment",
                "duration": "15-20 minutes",
            },
            {
                "name": "Mind Mapping",
                "description": "Visual exploration of ideas and connections",
                "duration": "10-15 minutes",
            },
            {
                "name": "SCAMPER",
                "description": "Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse",
                "duration": "20-30 minutes",
            },
            {
                "name": "Reverse Brainstorming",
                "description": "Think about how to cause the problem, then reverse solutions",
                "duration": "15-20 minutes",
            },
            {
                "name": "Six Thinking Hats",
                "description": "Explore ideas from different perspectives",
                "duration": "30-40 minutes",
            },
        ]

        if request.session_type == "party-mode":
            techniques.insert(
                0,
                {
                    "name": "Party Mode Warm-up",
                    "description": "High-energy, fun activities to break inhibitions",
                    "duration": "10 minutes",
                },
            )

        return techniques

    def _create_facilitation_guide(
        self, request: BrainstormingCoachRequest
    ) -> Dict[str, Any]:
        """Create facilitation guidance."""
        return {
            "opening": "Welcome everyone! Today we're going to brainstorm about {topic}. Remember, there are no bad ideas - let your creativity flow!",
            "ground_rules": [
                "No judgment during ideation",
                "Build on others' ideas with YES AND",
                "Go for quantity over quality",
                "Encourage wild and crazy ideas",
                "Have fun and be playful",
            ],
            "prompts": [
                "What if anything were possible?",
                "How might we...?",
                "What would happen if we...?",
                "In what ways could we...?",
            ],
            "closing": "Great session! Let's review our best ideas and identify next steps.",
        }
