"""
AI Agents package for the Evolution system.

This package contains all AI agents used in the system:
- main: Main orchestrator agent that coordinates all other agents
- coding: Specialized agent for coding tasks

The agents follow a hierarchical pattern where the main agent
acts as an orchestrator and can delegate tasks to specialized agents.
"""

from .main import create_main_agent
from .coding import create_coding_agent

__all__ = [
    'create_main_agent',
    'create_coding_agent',
]

