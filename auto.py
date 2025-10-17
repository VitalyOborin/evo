import asyncio
from agents import Agent, Runner, WebSearchTool, ItemHelpers
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Literal

async def main():
    load_dotenv()
    agent1 = Agent(
        name="Agent 1",
        instructions="You are an agent that can search the web for information.",
        model="gpt-4o-mini",
        tools=[WebSearchTool()]
    )
    agent2 = Agent(
        name="Agent 2",
        instructions="You are an agent that can search the web for information.",
        model="gpt-4o-mini",
        tools=[WebSearchTool()]
    )

    prompt = "What is the capital of France?"
    result = await Runner.run(agent1, prompt)
    result = await Runner.run(agent2, result.final_output)
    result = await Runner.run(agent1, result.final_output)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
