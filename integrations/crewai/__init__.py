"""CrewAI Integration for MDAN - Multi-Agent Development Agentic Network"""

__version__ = "1.0.0"

from .orchestrator import CrewAIOrchestrator, Phase
from .tools.serper_tool import SerperTool
from .tools.sql_tool import SQLTool
from .tools.file_tool import FileTool
from .flows.auto_flow import AutoFlow
from .flows.discovery_flow import DiscoveryFlow
from .flows.build_flow import BuildFlow
from .flows.debate_flow import DebateFlow
from .skills.skill_router import SkillRouter, Skill

__all__ = [
    "CrewAIOrchestrator",
    "Phase",
    "SerperTool",
    "SQLTool",
    "FileTool",
    "AutoFlow",
    "DiscoveryFlow",
    "BuildFlow",
    "DebateFlow",
    "SkillRouter",
    "Skill",
]
