import os
import argparse
import logging
from flow import coding_agent_flow

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('coding_agent.log')
    ]
)

logger = logging.getLogger('main')

def main():
    """
    Run the coding agent to help with code operations
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Coding Agent - AI-powered coding assistant')
    parser.add_argument('--query', '-q', type=str, help='User query to process', required=False)
    parser.add_argument('--working-dir', '-d', type=str, default=os.path.join(os.getcwd(), "project"), 
                        help='Working directory for file operations (default: current directory)')
    args = parser.parse_args()
    
    # Initialize shared memory
    shared = {
        "working_dir": args.working_dir,
        "history": [],
        "response": None
    }
    
    logger.info(f"Working directory: {args.working_dir}")
    
    # If initial query provided via command line, process it
    if args.query:
        shared["user_query"] = args.query
        coding_agent_flow.run(shared)
        print(f"\n{shared.get('response', 'No response generated')}\n")
    
    # Start continuous conversation loop
    print("Coding Agent is ready! Type 'quit' or 'exit' to end the conversation.")
    
    while True:
        try:
            # Get user input
            user_query = input("\nWhat would you like me to help you with? ").strip()
            
            # Check for exit commands
            if user_query.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye! Thanks for using the Coding Agent.")
                break
            
            # Skip empty input
            if not user_query:
                continue
            
            # Update shared memory with new query
            shared["user_query"] = user_query
            
            # Run the flow
            coding_agent_flow.run(shared)
            
            # Display the response
            response = shared.get('response', 'No response generated')
            print(f"\n{response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Thanks for using the Coding Agent.")
            break
        except Exception as e:
            logger.error(f"Error in conversation loop: {e}")
            print(f"\nAn error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()