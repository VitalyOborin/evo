import asyncio
from agents import Agent, Runner, WebSearchTool, ModelSettings
from openai.types.shared.reasoning import Reasoning
from agents.extensions.memory.sqlalchemy_session import SQLAlchemySession

# Import configuration and tools
from config import load_environment, validate_environment, get_agent_config, get_welcome_message, create_session_manager
from tools import execute_sql_query, execute_shell_command


# All tool functions are now imported from the tools package


async def process_user_input(agent: Agent, user_input: str, session: SQLAlchemySession) -> None:
    """Process a single user input with the AI agent using streaming."""
    # ANSI color codes
    GRAY = "\033[90m"
    RESET = "\033[0m"
    
    print("\n🤖 Processing your request...")
    print("=" * 60)
    
    reasoning_started = False
    response_started = False
    
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
                            print(f"\n{GRAY}🧠 Reasoning Process:")
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
                            print("\n🎯 Agent Response:")
                            print("-" * 60)
                            response_started = True
                        
                        if hasattr(event.data, 'delta') and event.data.delta:
                            # This is the actual final answer text - stream it!
                            print(event.data.delta, end="", flush=True)
        
        # Print separator after streaming is complete
        print("\n" + "-" * 60)
        
    except Exception as e:
        print(f"\n❌ Streaming error occurred: {str(e)}")
        print("Please check your request and try again.")
        print("-" * 60)


async def main():
    """Main function that runs an interactive CLI chat with the AI agent."""
    
    # Load environment variables
    load_environment()
    
    # Validate environment
    is_valid, missing_vars = validate_environment()
    if not is_valid:
        print("❌ Error: Required environment variables are not set:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file and ensure all required variables are configured.")
        return
    
    # Get agent configuration
    config = get_agent_config()
    
    # Create an agent with SQL and system capabilities
    agent = Agent(
        name=config['name'],
        instructions=config['instructions'],
        model="gpt-5-mini",
        model_settings=ModelSettings(reasoning=Reasoning(effort="low", summary="auto")),
        tools=[
            execute_sql_query,
            execute_shell_command,
            WebSearchTool()
        ],
    )
    
    # Initialize session manager
    session_manager = create_session_manager()
    
    # Create a new session for this conversation
    session = session_manager.create_session(create_tables=True)
    
    # Display welcome message
    welcome_lines = get_welcome_message()
    for line in welcome_lines:
        print(line)
    print(f"📋 Session ID: {session_manager.get_current_session_id()}")
    print("=" * 80)
    
    # Interactive chat loop
    while True:
        try:
            # Get user input
            print("\n💭 You:")
            user_input = input(">>> ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                print("\n👋 Goodbye! Thanks for using the AI Assistant!")
                break
            
            # Skip empty inputs
            if not user_input:
                print("Please enter a message or type 'exit' to quit.")
                continue
            
            # Process the user input with session context
            await process_user_input(agent, user_input, session)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Chat ended. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            print("Please try again or type 'exit' to quit.")
    
    # Cleanup resources
    try:
        await session_manager.cleanup()
    except Exception as e:
        print(f"\n⚠️ Warning: Error during cleanup: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
