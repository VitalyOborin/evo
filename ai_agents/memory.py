"""
Memory agent
"""

from agents import Agent
from config import load_instruction_template
from agents import function_tool

@function_tool
def recall_memory(query: str) -> str:
    """
    Recall and retrieve information from the memory.
    """
    return "I don't know"

@function_tool
def save_memory(memory: str) -> bool:
    """
    Save new information to the memory.
    """
    return True

def create_coding_agent() -> Agent:
    """
    Search and retrieve information from the memory.
    """
    
    agent = Agent(
        name="memory",
        instructions=load_instruction_template("memory.jinja2"),
        model="gpt-5-mini",
        tools=[
            "recall_memory",
            "save_memory"
        ],
    )
    
    return agent
