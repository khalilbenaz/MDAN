"""
Scenario tests for MDAN Master agent.
"""

from scenario import Scenario, expect
import sys
import os

# Add the app directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "app")
)

from core.agents.mdan_master.agent import MDANMasterAgent, AgentRequest


scenario = Scenario("MDAN Master - Core Functionality")


@scenario.test
async def test_agent_initialization():
    """
    Test that the MDAN Master agent initializes correctly.
    """
    agent = MDANMasterAgent()

    expect(agent.name).to_equal("MDAN Master")
    expect(agent.title).to_equal(
        "MDAN Master Executor, Knowledge Custodian, and Workflow Orchestrator"
    )
    expect(agent.icon).to_equal("🧙")
    expect(len(agent.capabilities)).to_equal(4)
    expect("runtime resource management" in agent.capabilities).to_be_true()
    expect("workflow orchestration" in agent.capabilities).to_be_true()
    expect("task execution" in agent.capabilities).to_be_true()
    expect("knowledge custodian" in agent.capabilities).to_be_true()


@scenario.test
async def test_greet_action():
    """
    Test that the greet action returns a proper greeting with menu.
    """
    agent = MDANMasterAgent()

    request = AgentRequest(
        action="greet",
        context={
            "user_name": "Alice",
            "communication_language": "English",
            "output_folder": "/output",
        },
    )

    result = await agent.process(request)

    expect(result).to_have_key("message")
    expect(result).to_have_key("agent")
    expect(result).to_have_key("icon")
    expect(result).to_have_key("capabilities")
    expect(result).to_have_key("menu")
    expect(result).to_have_key("help_hint")
    expect(result).to_have_key("language")

    expect(result["message"]).to_contain("Alice")
    expect(result["agent"]).to_equal("MDAN Master")
    expect(result["icon"]).to_equal("🧙")
    expect(result["language"]).to_equal("English")
    expect(len(result["menu"])).to_equal(6)


@scenario.test
async def test_greet_action_without_context():
    """
    Test that the greet action works without context (uses defaults).
    """
    agent = MDANMasterAgent()

    request = AgentRequest(action="greet")

    result = await agent.process(request)

    expect(result["message"]).to_contain("User")
    expect(result["language"]).to_equal("English")


@scenario.test
async def test_list_tasks_action():
    """
    Test that the list-tasks action returns available tasks.
    """
    agent = MDANMasterAgent()

    request = AgentRequest(action="list-tasks")

    result = await agent.process(request)

    expect(result).to_have_key("message")
    expect(result).to_have_key("tasks")
    expect(result).to_have_key("count")

    expect(result["message"]).to_equal("Available Tasks")
    expect(len(result["tasks"])).to_be_greater_than(0)
    expect(result["count"]).to_equal(len(result["tasks"]))


@scenario.test
async def test_list_workflows_action():
    """
    Test that the list-workflows action returns available workflows.
    """
    agent = MDANMasterAgent()

    request = AgentRequest(action="list-workflows")

    result = await agent.process(request)

    expect(result).to_have_key("message")
    expect(result).to_have_key("workflows")
    expect(result).to_have_key("count")

    expect(result["message"]).to_equal("Available Workflows")
    expect(len(result["workflows"])).to_be_greater_than(0)
    expect(result["count"]).to_equal(len(result["workflows"]))

    # Check that workflows from different modules are present
    workflow_ids = [w["id"] for w in result["workflows"]]
    expect("workflow-1" in workflow_ids).to_be_true()
    expect("workflow-4" in workflow_ids).to_be_true()  # FinTech workflow
    expect("workflow-5" in workflow_ids).to_be_true()  # DevOps/Azure workflow
    expect("workflow-6" in workflow_ids).to_be_true()  # DB Optimization workflow


@scenario.test
async def test_help_action():
    """
    Test that the help action returns help information.
    """
    agent = MDANMasterAgent()

    request = AgentRequest(action="help")

    result = await agent.process(request)

    expect(result).to_have_key("message")
    expect(result).to_have_key("agent")
    expect(result).to_have_key("description")
    expect(result).to_have_key("capabilities")
    expect(result).to_have_key("usage")
    expect(result).to_have_key("menu")

    expect(result["message"]).to_equal("MDAN Master Help")
    expect(result["agent"]).to_equal("MDAN Master")
    expect(len(result["usage"])).to_be_greater_than(0)
    expect(len(result["menu"])).to_equal(6)


@scenario.test
async def test_unknown_action():
    """
    Test that unknown actions return an appropriate error message.
    """
    agent = MDANMasterAgent()

    request = AgentRequest(action="unknown-action")

    result = await agent.process(request)

    expect(result).to_have_key("message")
    expect(result).to_have_key("action")
    expect(result).to_have_key("suggestion")

    expect(result["message"]).to_equal("Action not recognized")
    expect(result["action"]).to_equal("unknown-action")
    expect(result["suggestion"]).to_contain("/mmm-help")


@scenario.test
async def test_get_info():
    """
    Test that get_info returns complete agent information.
    """
    agent = MDANMasterAgent()

    info = agent.get_info()

    expect(info).to_have_key("name")
    expect(info).to_have_key("title")
    expect(info).to_have_key("icon")
    expect(info).to_have_key("capabilities")
    expect(info).to_have_key("role")
    expect(info).to_have_key("identity")
    expect(info).to_have_key("communication_style")
    expect(info).to_have_key("principles")

    expect(info["name"]).to_equal("MDAN Master")
    expect(info["icon"]).to_equal("🧙")
    expect(len(info["principles"])).to_equal(2)


@scenario.test
async def test_menu_structure():
    """
    Test that the menu has the correct structure and all required items.
    """
    agent = MDANMasterAgent()

    request = AgentRequest(action="greet")
    result = await agent.process(request)

    menu = result["menu"]

    # Check that all menu items are present
    menu_descriptions = [item["description"] for item in menu]

    expect("[MH] Redisplay Menu Help" in menu_descriptions).to_be_true()
    expect("[CH] Chat with the Agent about anything" in menu_descriptions).to_be_true()
    expect("[LT] List Available Tasks" in menu_descriptions).to_be_true()
    expect("[LW] List Workflows" in menu_descriptions).to_be_true()
    expect("[PM] Start Party Mode" in menu_descriptions).to_be_true()
    expect("[DA] Dismiss Agent" in menu_descriptions).to_be_true()

    # Check that each menu item has a trigger
    for item in menu:
        expect(item).to_have_key("trigger")
        expect(item).to_have_key("description")


@scenario.test
async def test_help_hint_format():
    """
    Test that the help hint is properly formatted.
    """
    agent = MDANMasterAgent()

    request = AgentRequest(action="greet")
    result = await agent.process(request)

    help_hint = result["help_hint"]

    expect(help_hint).to_contain("/mmm-help")
    expect(help_hint).to_contain("advice")
    expect(help_hint).to_contain("combine")


@scenario.test
async def test_communication_language_support():
    """
    Test that different communication languages are supported.
    """
    agent = MDANMasterAgent()

    # Test with Spanish
    request = AgentRequest(
        action="greet",
        context={
            "user_name": "Carlos",
            "communication_language": "Spanish",
            "output_folder": "/output",
        },
    )

    result = await agent.process(request)

    expect(result["language"]).to_equal("Spanish")
    expect(result["message"]).to_contain("Carlos")

    # Test with French
    request = AgentRequest(
        action="greet",
        context={
            "user_name": "Marie",
            "communication_language": "French",
            "output_folder": "/output",
        },
    )

    result = await agent.process(request)

    expect(result["language"]).to_equal("French")
    expect(result["message"]).to_contain("Marie")
