"""
Configuration package for the Universal System AI Agent.

This package contains configuration settings, environment variable loading,
session management, and application constants.
"""

from .settings import load_environment, validate_environment, get_agent_config, get_welcome_message
from .session_manager import SessionManager, create_session_manager

__all__ = [
    'load_environment',
    'validate_environment', 
    'get_agent_config',
    'get_welcome_message',
    'SessionManager',
    'create_session_manager'
]
