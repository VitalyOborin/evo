"""
Configuration package for the Universal System AI Agent.

This package contains configuration settings, environment variable loading,
and application constants.
"""

from .settings import load_environment, validate_environment, get_agent_config, get_welcome_message

__all__ = [
    'load_environment',
    'validate_environment', 
    'get_agent_config',
    'get_welcome_message'
]
