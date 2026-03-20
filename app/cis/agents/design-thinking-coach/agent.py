"""
Design Thinking Coach Agent

Human-centered design expert specializing in empathy mapping, prototyping, and user insights.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class DesignThinkingCoachRequest:
    """Request data structure for the Design Thinking Coach agent."""

    challenge: str
    target_users: Optional[str] = None
    phase: str = "full"  # empathize, define, ideate, prototype, test, full
    constraints: Optional[str] = None
    goals: Optional[str] = None


class DesignThinkingCoach:
    """
    Design Thinking Maestro.

    Design thinking virtuoso with 15+ years at Fortune 500s and startups.
    Expert in empathy mapping, prototyping, and user insights.

    Capabilities:
    - Guide human-centered design process
    - Facilitate empathy mapping exercises
    - Help define user needs and problems
    - Lead ideation sessions
    - Guide prototyping activities
    - Facilitate user testing and feedback
    - Apply design thinking principles
    """

    def __init__(self):
        """Initialize the Design Thinking Coach agent."""
        self.name = "Maya"
        self.title = "Design Thinking Maestro"
        self.icon = "🎨"

    async def process(self, request: DesignThinkingCoachRequest) -> Dict[str, Any]:
        """
        Process the design thinking request and return guidance.

        Args:
            request: The design thinking request containing challenge and parameters

        Returns:
            A dictionary containing the design thinking process and activities
        """
        # Validate request
        if not request.challenge:
            return {"success": False, "error": "Design challenge is required"}

        # Generate design thinking process
        process = self._generate_process(request)

        # Create phase-specific activities
        activities = self._create_activities(request)

        # Provide facilitation guidance
        facilitation = self._create_facilitation(request)

        return {
            "success": True,
            "agent": self.name,
            "title": self.title,
            "challenge": request.challenge,
            "target_users": request.target_users,
            "phase": request.phase,
            "process": process,
            "activities": activities,
            "facilitation": facilitation,
            "principles": [
                "Design is about THEM not us",
                "Validate through real human interaction",
                "Failure is feedback",
                "Design WITH users not FOR them",
                "Empathy drives innovation",
            ],
        }

    def _generate_process(self, request: DesignThinkingCoachRequest) -> Dict[str, Any]:
        """Generate the design thinking process."""
        phases = {
            "empathize": {
                "description": "Understand your users' needs, barriers, and attitudes",
                "activities": [
                    "User interviews",
                    "Observation",
                    "Empathy mapping",
                    "Journey mapping",
                ],
            },
            "define": {
                "description": "State your users' needs and problems",
                "activities": [
                    "Problem statement",
                    "Point of view",
                    "User personas",
                    "How might we questions",
                ],
            },
            "ideate": {
                "description": "Challenge assumptions and create ideas for innovative solutions",
                "activities": ["Brainstorming", "Mind mapping", "SCAMPER", "Crazy 8s"],
            },
            "prototype": {
                "description": "Start creating solutions",
                "activities": [
                    "Paper prototypes",
                    "Wireframes",
                    "Role-playing",
                    "Storyboards",
                ],
            },
            "test": {
                "description": "Try your solutions out with users",
                "activities": [
                    "User testing",
                    "Feedback sessions",
                    "A/B testing",
                    "Iteration",
                ],
            },
        }

        if request.phase == "full":
            return {
                "approach": "Full design thinking process",
                "phases": phases,
                "timeline": "Iterative process, typically 2-8 weeks depending on scope",
            }
        else:
            return {
                "approach": f"Focus on {request.phase} phase",
                "current_phase": phases[request.phase],
                "timeline": "1-2 weeks for focused phase work",
            }

    def _create_activities(
        self, request: DesignThinkingCoachRequest
    ) -> List[Dict[str, Any]]:
        """Create specific activities for the design thinking process."""
        activities = []

        if request.phase in ["empathize", "full"]:
            activities.append(
                {
                    "phase": "Empathize",
                    "activity": "Empathy Mapping",
                    "description": "Create a visual map of what users say, think, do, and feel",
                    "duration": "60-90 minutes",
                    "participants": "Design team + stakeholders",
                }
            )

        if request.phase in ["define", "full"]:
            activities.append(
                {
                    "phase": "Define",
                    "activity": "How Might We Questions",
                    "description": "Transform problem statements into actionable questions",
                    "duration": "30-60 minutes",
                    "participants": "Design team",
                }
            )

        if request.phase in ["ideate", "full"]:
            activities.append(
                {
                    "phase": "Ideate",
                    "activity": "Crazy 8s",
                    "description": "Rapid sketching of 8 ideas in 8 minutes",
                    "duration": "30-45 minutes",
                    "participants": "Design team",
                }
            )

        if request.phase in ["prototype", "full"]:
            activities.append(
                {
                    "phase": "Prototype",
                    "activity": "Paper Prototyping",
                    "description": "Quick, low-fidelity prototypes to test concepts",
                    "duration": "1-2 hours",
                    "participants": "Design team",
                }
            )

        if request.phase in ["test", "full"]:
            activities.append(
                {
                    "phase": "Test",
                    "activity": "User Testing Sessions",
                    "description": "Observe users interacting with prototypes",
                    "duration": "30-60 minutes per session",
                    "participants": "Users + design team",
                }
            )

        return activities

    def _create_facilitation(
        self, request: DesignThinkingCoachRequest
    ) -> Dict[str, Any]:
        """Create facilitation guidance."""
        return {
            "mindset": [
                "Be curious, not judgmental",
                "Embrace ambiguity",
                "Learn from failure",
                "Collaborate openly",
                "Stay user-focused",
            ],
            "tips": [
                "Start with empathy - understand before solving",
                "Involve real users throughout the process",
                "Prototype early and often",
                "Test assumptions, not just solutions",
                "Iterate based on feedback",
            ],
            "common_pitfalls": [
                "Solving the wrong problem",
                "Designing for yourself, not users",
                "Skipping empathy work",
                "Getting attached to your first idea",
                "Not testing with real users",
            ],
            "success_metrics": [
                "User satisfaction and delight",
                "Problem-solution fit",
                "Adoption and usage",
                "Business impact",
                "Learning and insights",
            ],
        }
