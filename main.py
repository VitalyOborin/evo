import asyncio
from agents import Agent, Runner, WebSearchTool

# Import configuration and tools
from config import load_environment, validate_environment, get_agent_config, get_welcome_message
from tools import execute_sql_query, execute_shell_command


# All tool functions are now imported from the tools package


async def process_user_input(agent: Agent, user_input: str) -> None:
    """Process a single user input with the AI agent using streaming."""
    print("\n🤖 Processing your request...")
    print("=" * 60)
    
    try:
        # Use run_streamed for proper streaming
        result = Runner.run_streamed(agent, user_input)
        
        print("\n🎯 Agent Response:")
        print("-" * 60)
        
        # Process streaming events - show ONLY final answer text
        async for event in result.stream_events():
            if hasattr(event, 'type') and event.type == "raw_response_event":
                if hasattr(event, 'data'):
                    # Check if this is a ResponseTextDeltaEvent (final answer streaming)
                    if event.data.__class__.__name__ == 'ResponseTextDeltaEvent':
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
        tools=[execute_sql_query, execute_shell_command, WebSearchTool()]
    )
    
    # Display welcome message
    welcome_lines = get_welcome_message()
    for line in welcome_lines:
        print(line)
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
            
            # Process the user input
            await process_user_input(agent, user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Chat ended. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            print("Please try again or type 'exit' to quit.")


if __name__ == "__main__":
    asyncio.run(main())
