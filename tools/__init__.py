"""
Tools package for the Universal System AI Agent.

This package contains all the tools available to the AI agent:
- sql_tool: PostgreSQL database operations
- local_shell_executor: Shell command executor for LocalShellTool

Shell command execution uses the standard LocalShellTool from agents SDK
with a custom Windows-optimized executor.

Each tool is implemented in a separate module for better organization
and maintainability.
"""

from .sql_tool import execute_sql_query
from .local_shell_executor import shell_executor

__all__ = [
    'execute_sql_query',
    'shell_executor'
]
