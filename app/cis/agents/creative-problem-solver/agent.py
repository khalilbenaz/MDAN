"""
Creative Problem Solver Agent

Systematic problem-solving expert using TRIZ, Theory of Constraints, and Systems Thinking.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class CreativeProblemSolverRequest:
    """Request data structure for the Creative Problem Solver agent."""

    problem: str
    context: Optional[str] = None
    constraints: Optional[str] = None
    methodology: str = "systematic"  # systematic, triz, toc, systems-thinking
    depth: str = "standard"  # quick, standard, deep


class CreativeProblemSolver:
    """
    Master Problem Solver.

    Renowned problem-solver who cracks impossible challenges.
    Expert in TRIZ, Theory of Constraints, Systems Thinking.
    Former aerospace engineer turned puzzle master.

    Capabilities:
    - Apply systematic problem-solving methodologies
    - Use TRIZ (Theory of Inventive Problem Solving)
    - Apply Theory of Constraints
    - Use Systems Thinking approaches
    - Hunt for root causes relentlessly
    - Ask the right questions
    - Find innovative solutions to impossible challenges
    """

    def __init__(self):
        """Initialize the Creative Problem Solver agent."""
        self.name = "Dr. Quinn"
        self.title = "Master Problem Solver"
        self.icon = "🔬"

    async def process(self, request: CreativeProblemSolverRequest) -> Dict[str, Any]:
        """
        Process the problem-solving request and return systematic analysis.

        Args:
            request: The problem-solving request containing problem and parameters

        Returns:
            A dictionary containing the problem analysis and solutions
        """
        # Validate request
        if not request.problem:
            return {"success": False, "error": "Problem description is required"}

        # Analyze the problem
        problem_analysis = self._analyze_problem(request)

        # Apply selected methodology
        methodology_results = self._apply_methodology(request)

        # Generate solutions
        solutions = self._generate_solutions(request, problem_analysis)

        # Create action plan
        action_plan = self._create_action_plan(solutions)

        return {
            "success": True,
            "agent": self.name,
            "title": self.title,
            "problem": request.problem,
            "methodology": request.methodology,
            "depth": request.depth,
            "problem_analysis": problem_analysis,
            "methodology_results": methodology_results,
            "solutions": solutions,
            "action_plan": action_plan,
            "principles": [
                "Every problem is a system revealing weaknesses",
                "Hunt for root causes relentlessly",
                "The right question beats a fast answer",
                "Look for contradictions and trade-offs",
                "Solutions often come from unexpected places",
            ],
        }

    def _analyze_problem(self, request: CreativeProblemSolverRequest) -> Dict[str, Any]:
        """Analyze the problem systematically."""
        return {
            "problem_statement": request.problem,
            "context": request.context or "No additional context provided",
            "constraints": request.constraints or "No specific constraints",
            "system_boundaries": "Identify what's in and out of scope",
            "stakeholders": "Who is affected by this problem?",
            "success_criteria": "What does success look like?",
        }

    def _apply_methodology(
        self, request: CreativeProblemSolverRequest
    ) -> Dict[str, Any]:
        """Apply the selected problem-solving methodology."""
        if request.methodology == "triz":
            return self._apply_triz(request)
        elif request.methodology == "toc":
            return self._apply_toc(request)
        elif request.methodology == "systems-thinking":
            return self._apply_systems_thinking(request)
        else:
            return self._apply_systematic(request)

    def _apply_triz(self, request: CreativeProblemSolverRequest) -> Dict[str, Any]:
        """Apply TRIZ methodology."""
        return {
            "methodology": "TRIZ (Theory of Inventive Problem Solving)",
            "principles": [
                "Segmentation: Divide the problem into parts",
                "Extraction: Remove the interfering part",
                "Local quality: Make each part optimal for its function",
                "Asymmetry: Change from symmetrical to asymmetrical",
                "Combination: Combine similar or neighboring objects",
            ],
            "contradiction_analysis": "Identify technical and physical contradictions",
            "ideality": "Move towards the ideal final result",
        }

    def _apply_toc(self, request: CreativeProblemSolverRequest) -> Dict[str, Any]:
        """Apply Theory of Constraints."""
        return {
            "methodology": "Theory of Constraints",
            "five_focusing_steps": [
                "Identify the constraint",
                "Exploit the constraint",
                "Subordinate everything else to the constraint",
                "Elevate the constraint",
                "Repeat if a new constraint emerges",
            ],
            "thinking_processes": [
                "Current Reality Tree: What's the problem?",
                "Evaporating Cloud: What's the conflict?",
                "Future Reality Tree: What's the solution?",
                "Prerequisite Tree: What obstacles exist?",
                "Transition Tree: How do we implement?",
            ],
        }

    def _apply_systems_thinking(
        self, request: CreativeProblemSolverRequest
    ) -> Dict[str, Any]:
        """Apply Systems Thinking."""
        return {
            "methodology": "Systems Thinking",
            "key_concepts": [
                "Interconnectedness: Everything is connected",
                "Feedback loops: Reinforcing and balancing",
                "Emergence: The whole is greater than the sum of parts",
                "Leverage points: Places to intervene in a system",
            ],
            "tools": [
                "Causal Loop Diagrams",
                "Stock and Flow Diagrams",
                "System Archetypes",
            ],
        }

    def _apply_systematic(
        self, request: CreativeProblemSolverRequest
    ) -> Dict[str, Any]:
        """Apply systematic problem-solving."""
        return {
            "methodology": "Systematic Problem-Solving",
            "steps": [
                "Define the problem clearly",
                "Gather relevant information",
                "Identify root causes",
                "Generate alternative solutions",
                "Evaluate and select solutions",
                "Implement and monitor",
            ],
            "tools": [
                "5 Whys: Ask why five times to find root cause",
                "Fishbone Diagram: Identify cause and effect relationships",
                "Pareto Analysis: Focus on vital few causes",
            ],
        }

    def _generate_solutions(
        self, request: CreativeProblemSolverRequest, analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate potential solutions."""
        return [
            {
                "solution": "Solution 1: Direct approach",
                "description": "Address the problem head-on with straightforward actions",
                "feasibility": "High",
                "impact": "Medium",
                "effort": "Low",
            },
            {
                "solution": "Solution 2: Innovative approach",
                "description": "Apply creative thinking to find novel solutions",
                "feasibility": "Medium",
                "impact": "High",
                "effort": "Medium",
            },
            {
                "solution": "Solution 3: Systemic approach",
                "description": "Address underlying system dynamics",
                "feasibility": "Medium",
                "impact": "High",
                "effort": "High",
            },
        ]

    def _create_action_plan(self, solutions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create an action plan for implementation."""
        return {
            "prioritization": "Rank solutions by impact and feasibility",
            "implementation_steps": [
                "Select best solution",
                "Create detailed implementation plan",
                "Identify resources needed",
                "Set timeline and milestones",
                "Execute and monitor progress",
                "Evaluate results and iterate",
            ],
            "risk_mitigation": "Identify potential risks and mitigation strategies",
            "success_metrics": "Define measurable outcomes",
        }
