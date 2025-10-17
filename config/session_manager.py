"""
Session management for AI agent context preservation.

This module handles session creation, management, and lifecycle
using SQLAlchemy-powered sessions from OpenAI Agents SDK.
"""

import os
import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from agents.extensions.memory import SQLAlchemySession


class SessionManager:
    """
    Manages AI agent sessions with persistent storage.
    
    This class provides session lifecycle management including:
    - Session creation and retrieval
    - Database engine initialization
    - Session persistence using SQLAlchemy
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize the session manager.
        
        Args:
            database_url: Database connection URL. If None, uses DATABASE_URL from env.
            
        Raises:
            ValueError: If database_url is not provided and DATABASE_URL env var is not set
        """
        self._database_url = database_url or os.getenv('DATABASE_URL')
        if not self._database_url:
            raise ValueError(
                "Database URL must be provided either as parameter or via DATABASE_URL env variable"
            )
        
        self._engine: Optional[AsyncEngine] = None
        self._current_session_id: Optional[str] = None
    
    @property
    def engine(self) -> AsyncEngine:
        """
        Get or create the async database engine.
        
        Returns:
            AsyncEngine: SQLAlchemy async engine instance
        """
        if self._engine is None:
            self._engine = create_async_engine(
                self._database_url,
                echo=False,  # Set to True for SQL query logging
                pool_pre_ping=True,  # Verify connections before using
                pool_size=5,
                max_overflow=10
            )
        return self._engine
    
    def generate_session_id(self) -> str:
        """
        Generate a unique session identifier.
        
        Returns:
            str: UUID-based session ID
        """
        return f"session_{uuid.uuid4().hex}"
    
    def create_session(
        self,
        session_id: Optional[str] = None,
        create_tables: bool = True
    ) -> SQLAlchemySession:
        """
        Create a new agent session with persistent storage.
        
        Args:
            session_id: Optional session identifier. If None, generates a new one.
            create_tables: Whether to automatically create database tables if they don't exist.
            
        Returns:
            SQLAlchemySession: Configured session instance
        """
        if session_id is None:
            session_id = self.generate_session_id()
        
        self._current_session_id = session_id
        
        session = SQLAlchemySession(
            session_id=session_id,
            engine=self.engine,
            create_tables=create_tables
        )
        
        return session
    
    def get_current_session_id(self) -> Optional[str]:
        """
        Get the current session identifier.
        
        Returns:
            Optional[str]: Current session ID or None if no session is active
        """
        return self._current_session_id
    
    async def cleanup(self) -> None:
        """
        Clean up resources and close database connections.
        
        This should be called when the application is shutting down.
        """
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None


def create_session_manager(database_url: Optional[str] = None) -> SessionManager:
    """
    Factory function to create a SessionManager instance.
    
    Args:
        database_url: Optional database connection URL
        
    Returns:
        SessionManager: Configured session manager instance
    """
    return SessionManager(database_url=database_url)

