"""
Tools package for the Universal System AI Agent.

This package contains all the tools available to the AI agent:
- sql_tool: PostgreSQL database operations
- local_shell_executor: Windows system command execution

Each tool is implemented in a separate module for better organization
and maintainability.
"""

from .sql_tool import execute_sql_query
from .local_shell_executor import execute_shell_command

__all__ = [
    'execute_sql_query',
    'execute_shell_command'
]
