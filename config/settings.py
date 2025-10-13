"""
Application configuration and settings management.

This module handles environment variable loading, validation,
and provides configuration for the AI agent.
"""

import os
from dotenv import load_dotenv
from agents import Agent


def load_environment() -> None:
    """Load environment variables from .env file."""
    load_dotenv()


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
    """
    return {
        'name': 'Universal System Agent',
        'instructions': (
            "Ты - мощный универсальный ИИ агент с полным доступом к системе. "
            "У тебя есть два основных инструмента:\n\n"
            "1. execute_sql_query - для работы с базой данных PostgreSQL:\n"
            "   - Создание/удаление баз данных и таблиц\n"
            "   - Любые SQL операции (SELECT, INSERT, UPDATE, DELETE)\n"
            "   - Управление пользователями и правами доступа\n\n"
            "2. execute_shell_command - для выполнения команд в системе Windows:\n"
            "   - Файловые операции (dir, copy, move, del)\n"
            "   - Системная информация (systeminfo, tasklist)\n"
            "   - Сетевые операции (ping, curl, netstat)\n"
            "   - Управление пакетами (pip, npm, choco)\n"
            "   - Git операции (git status, commit, push)\n"
            "   - Любые другие системные команды\n\n"
            "ВАЖНО: Выполняй запросы пользователя уверенно, используя подходящие инструменты. "
            "Если пользователь просит что-то связанное с базой данных - используй execute_sql_query. "
            "Если просит системную операцию - используй execute_shell_command. "
            "Ты можешь также отвечать на обычные вопросы и вести диалог."
        )
    }


def get_welcome_message() -> list[str]:
    """
    Get the welcome message lines for the application.
    
    Returns:
        list[str]: List of welcome message lines
    """
    return [
        "🤖 Добро пожаловать! Я - Универсальный Системный ИИ Агент",
        "🗄️ База данных: PostgreSQL (полный административный доступ)",
        "💻 Система: Windows (полный доступ к командной строке)",
        "✨ Ответы транслируются в реальном времени!",
        "",
        "🛠️ Мои возможности:",
        "  📊 БАЗА ДАННЫХ:",
        "    - CREATE/DROP DATABASE myapp",
        "    - SELECT * FROM users WHERE age > 25",
        "    - CREATE TABLE products (id SERIAL, name VARCHAR(100))",
        "",
        "  💻 СИСТЕМА:",
        "    - dir                    (просмотр файлов)",
        "    - systeminfo            (информация о системе)",  
        "    - pip list              (установленные пакеты)",
        "    - git status            (статус репозитория)",
        "    - netstat -an           (сетевые соединения)",
        "",
        "  💬 ОБЩЕНИЕ:",
        "    - Расскажи анекдот про программистов",
        "    - Объясни, как работает искусственный интеллект",
        "",
        "🚪 Для выхода введите: exit, quit, bye"
    ]
