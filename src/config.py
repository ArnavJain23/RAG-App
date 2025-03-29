import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# LLM Configuration
LLM_MODEL = "claude-3-sonnet-20240229"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = os.environ.get("RAG_DATA_DIR", os.path.join(BASE_DIR, "data"))
INDEX_CACHE_DIR = os.environ.get("RAG_INDEX_CACHE_DIR", os.path.join(BASE_DIR, "index_cache"))

# Chunking parameters
CHUNK_SIZE = int(os.environ.get("RAG_CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.environ.get("RAG_CHUNK_OVERLAP", "50"))

# Performance options
LAZY_LOADING = os.environ.get("RAG_LAZY_LOADING", "true").lower() == "true"
BACKGROUND_PRELOAD = os.environ.get("RAG_BACKGROUND_PRELOAD", "true").lower() == "true"

# Application Settings