"""
Агент для работы с памятью в асинхронном режиме
"""

from agents import Agent
from config import load_instruction_template
from tools import recall_memory, save_memory

def create_memory_agent() -> Agent:
    agent = Agent(
        name="memory",
        instructions=load_instruction_template("memory.jinja2"),
        model="gpt-5-mini",
        # Note: gpt-5-codex doesn't support Reasoning settings (only o1/o3 models do)
        # model_settings=ModelSettings(
        #     reasoning=Reasoning(effort="medium", summary="auto")
        # ),
        tools=[
            recall_memory,
            save_memory,
        ]
    )
    
    return agent