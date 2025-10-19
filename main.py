"""
Main entry point for the Evolution AI Agent system.

This module provides the interactive CLI interface for communicating
with the AI agent system.
"""

import asyncio
from agents import Runner
from agents.extensions.memory import SQLAlchemySession


# Import configuration
from config import (
    load_environment, 
    validate_environment, 
    get_agent_config, 
    get_welcome_message, 
    create_session_manager
)

# Import AI agents
from ai_agents import create_main_agent

# Import memory processor for parallel memory operations
from memory_processor import start_memory_processing


async def process_user_input(agent, user_input: str, session: SQLAlchemySession) -> None:
    """
    Process a single user input with the AI agent using streaming.
    
    Args:
        agent: The AI agent instance to process the request
        user_input: User's text input
        session: SQLAlchemy session for context preservation
        
    This function handles streaming of both reasoning process
    and final responses with appropriate formatting.
    After processing, it starts a parallel process for memory operations.
    """
    # ANSI color codes
    GRAY = "\033[90m"
    RESET = "\033[0m"
    
    print("\n[AI] Processing your request...")
    print("=" * 60)
    
    reasoning_started = False
    response_started = False
    agent_response_text = []  # Collect full response for memory processing
    
    try:
        # Use run_streamed with session for context preservation
        result = Runner.run_streamed(agent, user_input, session=session)
        
        # Process streaming events - show reasoning and final answer
        async for event in result.stream_events():
            if hasattr(event, 'type') and event.type == "raw_response_event":
                if hasattr(event, 'data'):
                    # Check if this is a reasoning summary text delta event
                    if event.data.type == "response.reasoning_summary_text.delta":
                        if not reasoning_started:
                            print(f"\n{GRAY}[REASONING] Reasoning Process:")
                            print("-" * 60)
                            reasoning_started = True

                        if hasattr(event.data, 'delta') and event.data.delta:
                            # Stream reasoning text as it comes in gray color
                            print(f"{GRAY}{event.data.delta}{RESET}", end="", flush=True)

                    # Check if this is a ResponseTextDeltaEvent (final answer streaming)
                    elif event.data.__class__.__name__ == 'ResponseTextDeltaEvent':
                        if not response_started:
                            if reasoning_started:
                                print(f"{RESET}\n" + "-" * 60)
                            print("\n[RESPONSE] Agent Response:")
                            print("-" * 60)
                            response_started = True

                        if hasattr(event.data, 'delta') and event.data.delta:
                            # This is the actual final answer text - stream it!
                            delta_text = event.data.delta
                            print(delta_text, end="", flush=True)
                            # Collect the response for memory processing
                            agent_response_text.append(delta_text)
        
        # Print separator after streaming is complete
        print("\n" + "-" * 60)
        
        # Start memory processing in a separate process (non-blocking)
        full_response = "".join(agent_response_text)
        if full_response.strip():  # Only process if we got a response
            start_memory_processing(user_input, full_response)
        
    except Exception as e:
        print(f"\n[ERROR] Streaming error occurred: {str(e)}")
        print("Please check your request and try again.")
        print("-" * 60)


async def main():
    """
    Main function that runs an interactive CLI chat with the AI agent.
    
    This function:
    1. Loads and validates environment configuration
    2. Creates the main orchestrator agent
    3. Initializes session management
    4. Runs an interactive chat loop
    5. Handles cleanup on exit
    """
    
    # Load environment variables
    load_environment()
    
    # Validate environment
    is_valid, missing_vars = validate_environment()
    if not is_valid:
        print("[ERROR] Required environment variables are not set:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file and ensure all required variables are configured.")
        return

    # Create the main orchestrator agent from ai_agents module
    agent = create_main_agent()

    # Initialize session manager
    session_manager = create_session_manager()

    # Create a new session for this conversation
    session = session_manager.create_session(create_tables=True)

    # Display welcome message
    welcome_lines = get_welcome_message()
    for line in welcome_lines:
        print(line)
    print(f"[SESSION] Session ID: {session_manager.get_current_session_id()}")
    print("=" * 80)

    # Interactive chat loop
    while True:
        try:
            # Get user input
            print("\n[USER] You:")
            user_input = input(">>> ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                print("\n[BYE] Goodbye! Thanks for using the AI Assistant!")
                break
            
            # Skip empty inputs
            if not user_input:
                print("Please enter a message or type 'exit' to quit.")
                continue
            
            # Process the user input with session context
            await process_user_input(agent, user_input, session)
            
        except KeyboardInterrupt:
            print("\n\n[INTERRUPT] Chat interrupted. Goodbye!")
            break
        except EOFError:
            print("\n\n[EOF] Chat ended. Goodbye!")
            break
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {str(e)}")
            print("Please try again or type 'exit' to quit.")
    
    # Cleanup resources
    try:
        await session_manager.cleanup()
    except Exception as e:
        print(f"\n[WARNING] Error during cleanup: {str(e)}")


if __name__ == "__main__":
    # Set multiprocessing start method for Windows compatibility
    import multiprocessing
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        # Already set, ignore
        pass
    
    asyncio.run(main())
