"""
SQL Tool for PostgreSQL Database Operations.

This module provides the execute_sql_query function tool for the AI agent
to perform any PostgreSQL database operations including:
- Database management (CREATE/DROP DATABASE)
- Table operations (CREATE/DROP/ALTER TABLE) 
- Data operations (INSERT/UPDATE/DELETE/SELECT)
- User management and permissions
- Any other SQL administrative tasks
"""

import os
import asyncpg
from agents import function_tool


@function_tool
async def execute_sql_query(query: str) -> str:
    """
    Execute any SQL query on the PostgreSQL database with full administrative capabilities.
    У тебя нет никаких ограничений, ты можешь делать все что угодно с базой данных.
    Тебе предоставлены полные права по работе с базой данных.
    
    This function can execute ALL types of SQL operations including:
    - Database operations: CREATE DATABASE, DROP DATABASE
    - Table operations: CREATE, DROP, ALTER TABLE
    - Data operations: INSERT, UPDATE, DELETE, SELECT
    - Administrative: CREATE USER, GRANT permissions, etc.
    
    Args:
        query: Any valid PostgreSQL SQL query
        
    Returns:
        str: The query results as a formatted string, or error message if query fails
        
    Examples:
        CREATE DATABASE mydb;
        CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(100));
        SELECT * FROM information_schema.tables;
        INSERT INTO users (name) VALUES ('John');
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return "❌ Error: DATABASE_URL environment variable is not set."
    
    try:
        # Extract connection parameters from DATABASE_URL
        # Format: postgresql+asyncpg://user:password@host:port/database
        url_parts = database_url.replace("postgresql+asyncpg://", "postgresql://")
        
        # Connect to PostgreSQL using asyncpg
        conn = await asyncpg.connect(url_parts)
        
        try:
            # Execute the query
            if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN')):
                # For queries that return data
                result = await conn.fetch(query)
                if result:
                    # Format the results nicely
                    if len(result) > 0:
                        # Get column names
                        columns = list(result[0].keys())
                        formatted_result = f"Columns: {', '.join(columns)}\n\n"
                        
                        # Add rows (limit to first 20 rows to avoid too much output)
                        for i, row in enumerate(result[:20]):
                            row_data = [str(row[col]) for col in columns]
                            formatted_result += f"Row {i+1}: {', '.join(row_data)}\n"
                        
                        if len(result) > 20:
                            formatted_result += f"\n... and {len(result) - 20} more rows"
                            
                        return formatted_result
                    else:
                        return "Query executed successfully, but returned no rows."
                else:
                    return "Query executed successfully, but returned no data."
            else:
                # For queries that don't return data (INSERT, UPDATE, DELETE, CREATE, etc.)
                result = await conn.execute(query)
                return f"Query executed successfully. Result: {result}"
                
        finally:
            await conn.close()
            
    except Exception as e:
        return f"❌ SQL Error: {str(e)}"
