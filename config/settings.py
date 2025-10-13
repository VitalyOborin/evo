"""
Application configuration and settings management.

This module handles environment variable loading, validation,
and provides configuration for the AI agent.
"""

import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from dotenv import load_dotenv
from agents import Agent


def load_environment() -> None:
    """Load environment variables from .env file."""
    load_dotenv()


def load_instruction_template(template_name: str, **context) -> str:
    """
    Load and render a Jinja2 instruction template.
    
    Args:
        template_name: Name of the template file (e.g., "main.jinja2")
        **context: Variables to pass to the template for rendering
        
    Returns:
        str: Rendered instruction text
        
    Raises:
        FileNotFoundError: If template file doesn't exist
        Exception: If template rendering fails
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    instructions_dir = project_root / "instructions"
    
    if not instructions_dir.exists():
        raise FileNotFoundError(f"Instructions directory not found: {instructions_dir}")
    
    template_path = instructions_dir / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    
    try:
        # Create Jinja2 environment
        env = Environment(
            loader=FileSystemLoader(instructions_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Load and render template
        template = env.get_template(template_name)
        return template.render(**context)
        
    except Exception as e:
        raise Exception(f"Failed to render template '{template_name}': {str(e)}")


def validate_environment() -> tuple[bool, list[str]]:
    """
    Validate that all required environment variables are set.
    
    Returns:
        tuple: (is_valid, missing_variables)
    """
    required_vars = [
        'OPENAI_API_KEY',
        'DATABASE_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return len(missing_vars) == 0, missing_vars


def get_agent_config() -> dict:
    """
    Get AI agent configuration.
    
    Returns:
        dict: Agent configuration including name, instructions, and capabilities
        
    Raises:
        Exception: If instruction template cannot be loaded
    """
    try:
        # Load instructions from template
        instructions = load_instruction_template("main.jinja2")
        
        return {
            'name': 'Universal System Agent',
            'instructions': instructions
        }
    except Exception as e:
        raise Exception(f"Failed to load agent configuration: {str(e)}")


def get_welcome_message() -> list[str]:
    """
    Get the welcome message lines for the application.
    
    Returns:
        list[str]: List of welcome message lines
    """
    return [
        "[AI] Добро пожаловать! Я - Универсальный Системный ИИ Агент",
    ]
