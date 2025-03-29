import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLM Configuration
LLM_MODEL = "claude-3-sonnet-20240229"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Document Processing
DATA_DIR = "./data/"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# Application Settings
INDEX_CACHE_DIR = "./index_cache/"