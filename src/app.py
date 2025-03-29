"""
Main application entry point with optimized startup
"""
import time
import logging
import sys
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from src.application import ApplicationManager

def main():
    """Main application entry point"""
    start_time = time.time()
    # logger.info("Starting application...")
    
    # Initialize application manager
    app_manager = ApplicationManager()
    app_manager.start()
    
    # Report startup time
    startup_time = time.time() - start_time
    logger.info(f"Application ready in {startup_time:.2f} seconds")
    
    # Interactive query loop
    while True:
        try:
            query = input("\nEnter your question (or 'exit' to quit, 'reset' to clear history): ")
            
            if query.lower() in ('exit', 'quit'):
                break
                
            if query.lower() == 'reset':
                app_manager.reset_conversation()
                print("Conversation history has been reset.")
                continue
            
            # Process the query as part of a chat
            result = app_manager.process_chat_message(query)
            
            # Display the response
            print(f"\nResponse: {result['answer']}")
            print(f"Query processed in {result['processing_time']:.2f} seconds")
            
            # Optionally display sources
            if len(result['sources']) > 0 and query.lower().startswith('sources'):
                print("\nSources:")
                for i, source in enumerate(result['sources']):
                    print(f"\n--- Source {i+1} ---")
                    print(source['text'][:200] + "..." if len(source['text']) > 200 else source['text'])
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            print(f"Error: {str(e)}")
    
    app_manager.shutdown()
    logger.info("Application shutting down")

if __name__ == "__main__":
    main() 