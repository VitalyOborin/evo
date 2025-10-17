"""
Specialized coding agent for the Evolution system.

This agent handles all programming-related tasks including:
- Code generation and refactoring
- Architecture design
- Bug fixing and debugging
- Code review and optimization
- Python code execution via code interpreter

The agent uses CodeInterpreterTool to execute Python code in a secure
sandbox environment, allowing it to test code, perform calculations,
data analysis, and verify implementations.
"""

from agents import Agent, CodeInterpreterTool
from config import load_instruction_template


def create_coding_agent() -> Agent:
    """
    Create and configure a specialized coding agent.
    
    This agent is optimized for programming tasks and follows
    best practices for software development including:
    - Clean code principles
    - SOLID principles
    - DRY and KISS
    - Design patterns
    - Security best practices
    
    The agent's instructions are loaded from the coding.jinja2 template,
    which can be customized without modifying code.
    
    Returns:
        Configured Agent instance specialized for coding tasks
        
    Example:
        >>> coding_agent = create_coding_agent()
        >>> # Use as a tool in another agent or standalone
        
    Raises:
        Exception: If instruction template cannot be loaded
    """
    
    agent = Agent(
        name="coding",
        instructions=load_instruction_template("coding.jinja2"),
        model="gpt-5-codex",
        # Note: gpt-5-codex doesn't support Reasoning settings (only o1/o3 models do)
        # model_settings=ModelSettings(
        #     reasoning=Reasoning(effort="medium", summary="auto")
        # ),
        #tools=[
        #    CodeInterpreterTool(
        #        tool_config={"type": "code_interpreter", "container": {"type": "auto"}}
        #    )
        #],
    )
    
    return agent
