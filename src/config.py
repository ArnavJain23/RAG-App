import os
from dotenv import load_dotenv
from pathlib import Path

class ConfigManager:
    """Configuration manager for the RAG application"""
    
    def __init__(self):
        """Initialize configuration with default values and environment variables"""
        # Load environment variables
        load_dotenv()
        
        # Base directories
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = os.environ.get("RAG_DATA_DIR", os.path.join(self.base_dir, "data"))
        self.index_cache_dir = os.environ.get("RAG_INDEX_CACHE_DIR", os.path.join(self.base_dir, "index_cache"))
        
        # LLM Configuration
        self.llm_model = os.environ.get("RAG_LLM_MODEL", "claude-3-sonnet-20240229")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.embedding_model = os.environ.get("RAG_EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
        
        # Chunking parameters
        self.chunk_size = int(os.environ.get("RAG_CHUNK_SIZE", "512"))
        self.chunk_overlap = int(os.environ.get("RAG_CHUNK_OVERLAP", "50"))
        
        # Performance options
        self.lazy_loading = os.environ.get("RAG_LAZY_LOADING", "true").lower() == "true"
        self.background_preload = os.environ.get("RAG_BACKGROUND_PRELOAD", "true").lower() == "true"
        
        # Query parameters
        self.similarity_top_k = int(os.environ.get("RAG_SIMILARITY_TOP_K", "3"))
        self.response_mode = os.environ.get("RAG_RESPONSE_MODE", "compact")
        
    def get_data_dir(self) -> str:
        """Get the data directory path"""
        return self.data_dir
        
    def get_index_cache_dir(self) -> str:
        """Get the index cache directory path"""
        return self.index_cache_dir
        
    def get_llm_config(self) -> dict:
        """Get LLM configuration as a dictionary"""
        return {
            "model": self.llm_model,
            "api_key": self.anthropic_api_key,
            "temperature": 0.0
        }
        
    def get_embedding_config(self) -> dict:
        """Get embedding model configuration"""
        return {
            "model_name": self.embedding_model
        }
        
    def get_chunking_config(self) -> dict:
        """Get text chunking configuration"""
        return {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }
        
    def get_query_config(self) -> dict:
        """Get query engine configuration"""
        return {
            "similarity_top_k": self.similarity_top_k,
            "response_mode": self.response_mode
        }

# Create global config instance for backward compatibility
config = ConfigManager()

# Export configuration variables for backward compatibility
DATA_DIR = config.data_dir
INDEX_CACHE_DIR = config.index_cache_dir
CHUNK_SIZE = config.chunk_size
CHUNK_OVERLAP = config.chunk_overlap
LLM_MODEL = config.llm_model
ANTHROPIC_API_KEY = config.anthropic_api_key
LAZY_LOADING = config.lazy_loading
BACKGROUND_PRELOAD = config.background_preload

# Application Settings