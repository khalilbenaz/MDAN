"""MMM module agents package."""

import importlib.util
import sys
import os

# Direct imports for agents without hyphens
from .analyst.agent import AnalystAgent
from .architect.agent import ArchitectAgent
from .dev.agent import DevAgent
from .pm.agent import PMAgent
from .qa.agent import QAAgent
from .sm.agent import SMAgent


# Dynamic imports for agents with hyphens in directory names
def load_agent_from_hyphen_dir(agent_name, class_name):
    """Load an agent from a directory with hyphens in its name."""
    spec = importlib.util.spec_from_file_location(
        agent_name,
        os.path.join(
            os.path.dirname(__file__), agent_name.replace("_", "-"), "agent.py"
        ),
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load agent {agent_name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[agent_name] = module
    spec.loader.exec_module(module)
    return getattr(module, class_name)


# Load agents with hyphens
QuickFlowSoloDevAgent = load_agent_from_hyphen_dir(
    "quick_flow_solo_dev", "QuickFlowSoloDevAgent"
)
TechWriterAgent = load_agent_from_hyphen_dir("tech_writer", "TechWriterAgent")

__all__ = [
    "AnalystAgent",
    "ArchitectAgent",
    "DevAgent",
    "PMAgent",
    "QAAgent",
    "QuickFlowSoloDevAgent",
    "SMAgent",
    "TechWriterAgent",
]
