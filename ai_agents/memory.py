"""
Memory agent for vector-based information storage and retrieval.
"""

import os
import uuid
from typing import List, Dict, Any
from agents import Agent
from agents import function_tool
from config import load_instruction_template
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# Collection configuration
COLLECTION_NAME = "memory"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))

# Lazy initialization of clients
_openai_client = None
_qdrant_client = None


def _get_openai_client():
    """Get or create OpenAI client."""
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _openai_client


def _get_qdrant_client():
    """Get or create QDRANT client."""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
    return _qdrant_client


def _ensure_collection_exists():
    """Ensure the memory collection exists in QDRANT."""
    try:
        qdrant_client = _get_qdrant_client()
        # Check if collection exists
        collections = qdrant_client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if COLLECTION_NAME not in collection_names:
            # Create collection with vector parameters
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIM,
                    distance=Distance.COSINE
                )
            )
    except Exception as e:
        print(f"Warning: Could not ensure collection exists: {e}")


def _generate_embedding(text: str) -> List[float]:
    """Generate embeddings for the given text using OpenAI."""
    try:
        openai_client = _get_openai_client()
        response = openai_client.embeddings.create(
            input=text,
            model=EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        raise Exception(f"Failed to generate embedding: {str(e)}")


@function_tool
def save_memory(content: str) -> str:
    """
    Save information to the vector memory database.

    Args:
        content: The text content to store in memory

    Returns:
        Confirmation message with memory ID
    """
    try:
        _ensure_collection_exists()

        # Generate unique ID for this memory
        memory_id = str(uuid.uuid4())

        # Generate embedding for the content
        vector = _generate_embedding(content)

        # Create point with vector and payload
        point = PointStruct(
            id=memory_id,
            vector=vector,
            payload={
                "content": content,
                "timestamp": str(uuid.uuid1().time),  # Time-based UUID for sorting
            }
        )

        # Upsert to QDRANT
        qdrant_client = _get_qdrant_client()
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point]
        )

        return f"Memory saved successfully with ID: {memory_id}"

    except Exception as e:
        return f"Failed to save memory: {str(e)}"


@function_tool
def recall_memory(query: str, limit: int = 5) -> str:
    """
    Search and retrieve relevant information from memory using semantic similarity.

    Args:
        query: The search query to find relevant memories
        limit: Maximum number of results to return (default: 5)

    Returns:
        Formatted string with relevant memories or "No relevant memories found"
    """
    try:
        _ensure_collection_exists()

        # Generate embedding for the query
        query_vector = _generate_embedding(query)

        # Search for similar vectors
        qdrant_client = _get_qdrant_client()
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit
        )

        if not search_results:
            return "No relevant memories found."

        # Format results
        results = []
        for i, result in enumerate(search_results, 1):
            content = result.payload.get("content", "")
            score = result.score
            memory_id = result.id

            results.append(
                f"{i}. [ID: {memory_id}] (Score: {score:.3f})\n"
                f"   {content}\n"
            )

        return "Relevant memories:\n\n" + "\n".join(results)

    except Exception as e:
        return f"Failed to recall memory: {str(e)}"

def create_memory_agent() -> Agent:
    """
    Create and configure the memory agent for vector-based information storage and retrieval.

    Returns:
        Agent: Configured memory agent with save_memory and recall_memory tools
    """

    agent = Agent(
        name="memory",
        instructions=load_instruction_template("memory.jinja2"),
        model="gpt-4o-mini",
        tools=[
            save_memory,
            recall_memory
        ],
    )

    return agent
