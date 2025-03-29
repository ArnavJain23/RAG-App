"""
Main application entry point with optimized startup
"""
import time
import logging
import sys
from dotenv import load_dotenv

# Import optimized modules (lazy imports to speed up initial startup)
from src.config import BACKGROUND_PRELOAD
from src.preload import check_cache_exists, start_background_preload
from src.indexing import load_index

# Load environment variables first
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    start_time = time.time()
    logger.info("Starting application...")
    
    
    # Check if we can use cached index
    has_cache = check_cache_exists()
    
    # Start background preloading if enabled
    preload_thread = None
    if BACKGROUND_PRELOAD and has_cache:
        preload_thread = start_background_preload()
    
    # Load the index (this will use cache if available)
    index = load_index()
    
    # Create query engine
    query_engine = index.as_query_engine()
    
    # Report startup time
    startup_time = time.time() - start_time
    logger.info(f"Application ready in {startup_time:.2f} seconds")
    
    # Interactive query loop
    while True:
        try:
            query = input("\nEnter your question (or 'exit' to quit): ")
            if query.lower() in ('exit', 'quit'):
                break
                
            query_start = time.time()
            response = query_engine.query(query)
            query_time = time.time() - query_start
            
            print(f"\nResponse: {response}")
            print(f"Query processed in {query_time:.2f} seconds")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            print(f"Error: {str(e)}")
    
    logger.info("Application shutting down")

if __name__ == "__main__":
    main() 