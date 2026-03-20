"""
MDAN - Creative Innovation Strategy (cis) Agents

This module exports all Creative Innovation Strategy agents for brainstorming,
problem-solving, design thinking, innovation strategy, presentations, and storytelling.

Agents:
- BrainstormingCoach: Elite facilitator for creative brainstorming sessions
- CreativeProblemSolver: Systematic problem-solving expert
- DesignThinkingCoach: Human-centered design expert
- InnovationStrategist: Business model innovator and strategic disruption expert
- PresentationMaster: Visual communication and presentation expert
- Storyteller: Expert storytelling guide and narrative strategist
"""

# Import agents from their directories (using direct imports to avoid hyphen issues)
from .brainstorming_coach.agent import BrainstormingCoachAgent
from .creative_problem_solver.agent import CreativeProblemSolverAgent
from .design_thinking_coach.agent import DesignThinkingCoachAgent
from .innovation_strategist.agent import InnovationStrategistAgent
from .presentation_master.agent import PresentationMasterAgent
from .storyteller.agent import StorytellerAgent

__all__ = [
    "BrainstormingCoachAgent",
    "CreativeProblemSolverAgent",
    "DesignThinkingCoachAgent",
    "InnovationStrategistAgent",
    "PresentationMasterAgent",
    "StorytellerAgent",
]
