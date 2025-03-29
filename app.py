"""
Main entry point for the RAG web application
"""
import logging
# from dotenv import load_dotenv

# Load environment variables first
# load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import after environment is loaded
from src.web_app import run_app

if __name__ == '__main__':
    # Run the web application
    run_app(host='127.0.0.1', port=8080, debug=True) 