"""
Main orchestrator agent for the Evolution system.

This agent acts as the primary entry point and coordinates
all other specialized agents in the system.
"""

from agents import Agent, WebSearchTool
from tools import execute_sql_query, execute_shell_command, save_memory, recall_memory
from .coding import create_coding_agent
from config import load_instruction_template


def create_main_agent() -> Agent:
    """
    Create and configure the main orchestrator agent.
    
    This agent is responsible for:
    - Understanding user requests
    - Delegating tasks to specialized agents when needed
    - Accessing databases and system resources
    - Web searching for information
    - Coordinating complex multi-step workflows
    
    Args:
        instructions: Custom instructions for the agent
        
    Returns:
        Configured Agent instance ready to handle user requests
        
    Example:
        >>> agent = create_main_agent("You are a helpful assistant")
        >>> result = Runner.run(agent, "Help me with something")
    """
    
    # Create specialized agents that can be used as tools
    coding_agent = create_coding_agent()
    
    # Create the main orchestrator agent with all available tools
    agent = Agent(
        name="main",
        instructions=load_instruction_template("main.jinja2"),
        model="gpt-5-mini",
        # Note: gpt-5-mini doesn't support Reasoning settings (only o1/o3 models do)
        # model_settings=ModelSettings(
        #     reasoning=Reasoning(effort="low", summary="auto")
        # ),
        tools=[
            execute_sql_query,
            execute_shell_command,
            WebSearchTool(),
            coding_agent.as_tool(
                tool_name="coding",
                tool_description="Write application code and test it",
            ),
            recall_memory
        ],
    )
    
    return agent
