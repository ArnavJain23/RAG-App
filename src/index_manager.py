"""
Index management module for building and loading vector indexes
"""
import os
import time
import logging
from typing import List, Optional, Tuple, Any
from functools import lru_cache

from llama_index.core import VectorStoreIndex, Settings, load_index_from_storage
from llama_index.core.schema import Node
from llama_index.core.storage import StorageContext
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from src.config import config
from src.document_processor import DocumentProcessor

logger = logging.getLogger(__name__)

class IndexManager:
    """Manages index operations including building, saving, and loading"""
    
    def __init__(self, config_manager=None, doc_processor=None):
        """
        Initialize index manager
        
        Args:
            config_manager: Configuration manager (uses global instance if None)
            doc_processor: Document processor (creates new instance if None)
        """
        self.config = config_manager or config
        self.index_cache_dir = self.config.index_cache_dir
        self.document_processor = doc_processor or DocumentProcessor(self.config)
        
    def initialize_models(self):
        """
        Initialize necessary models for indexing
        """
        logger.info("Initializing models for indexing")
        
        # Set Claude as LLM
        Settings.llm = Anthropic(
            model=self.config.llm_model, 
            api_key=self.config.anthropic_api_key,
            temperature=0
        )
        
        # Set embedding model
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=self.config.embedding_model
        )
        
        logger.info("Models initialized")
            
    def initialize_models_lazy(self):
        """
        Lazily initialize models only when needed
        """
        logger.info("Setting up lazy model initialization")
        # Only set the model configurations but don't actually load the models
        # They will be loaded on first use
        
        Settings.llm = Anthropic(
            model=self.config.llm_model,
            api_key=self.config.anthropic_api_key,
            temperature=0
        )
        
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=self.config.embedding_model
        )
        
        logger.info("Models initialized lazily")
        
    def build_index(self, nodes: Optional[List[Node]] = None, persist: bool = True) -> VectorStoreIndex:
        """
        Build a vector store index from nodes
        
        Args:
            nodes: Nodes to index (loads and processes documents if None)
            persist: Whether to persist the index to disk
            
        Returns:
            Built VectorStoreIndex
        """
        logger.info("Building index...")
        start_time = time.time()
        
        # Initialize models
        self.initialize_models()
        
        # Get nodes if not provided
        if nodes is None:
            nodes = self.document_processor.process_documents()
        
        # Create the index
        index = VectorStoreIndex(nodes)
        
        elapsed = time.time() - start_time
        logger.info(f"Built index in {elapsed:.2f} seconds")
        
        # Persist index if requested
        if persist:
            self._persist_index(index)
        
        return index
    
    def _persist_index(self, index: VectorStoreIndex):
        """
        Persist index to disk
        
        Args:
            index: Index to persist
        """
        persist_start = time.time()
        logger.info(f"Persisting index to {self.index_cache_dir}")
        
        os.makedirs(self.index_cache_dir, exist_ok=True)
        index.storage_context.persist(persist_dir=self.index_cache_dir)
        
        persist_elapsed = time.time() - persist_start
        logger.info(f"Persisted index in {persist_elapsed:.2f} seconds")
    
    def check_cache_exists(self) -> bool:
        """
        Check if the index cache exists
        
        Returns:
            True if cache exists and appears valid, False otherwise
        """
        if not os.path.exists(self.index_cache_dir):
            return False
        
        # Check for essential files in the cache directory
        required_files = ["docstore.json", "index_store.json"]
        for file in required_files:
            if not os.path.exists(os.path.join(self.index_cache_dir, file)):
                return False
        
        return True
    
    # Add caching decorator to avoid repeated loading
    @lru_cache(maxsize=1)
    def _cached_load_index(self) -> Tuple[Optional[VectorStoreIndex], bool]:
        """
        Internal function to load index with caching
        
        Returns:
            Tuple of (index, success_flag)
        """
        start_time = time.time()
        
        try:
            logger.info(f"Attempting to load index from {self.index_cache_dir}")
            # Only initialize the embeddings model - delay other initializations
            Settings.embed_model = HuggingFaceEmbedding(
                model_name=self.config.embedding_model
            )
            
            # Use optimized storage context loading
            storage_context = StorageContext.from_defaults(
                persist_dir=self.index_cache_dir
            )
            
            # Load the index with minimal initialization
            index = load_index_from_storage(storage_context)
            
            elapsed = time.time() - start_time
            logger.info(f"Loaded index from cache in {elapsed:.2f} seconds")
            return index, True
            
        except Exception as e:
            logger.warning(f"Failed to load index from cache: {str(e)}")
            elapsed = time.time() - start_time
            logger.info(f"Index loading attempt failed after {elapsed:.2f} seconds")
            return None, False
    
    def load_index(self) -> VectorStoreIndex:
        """
        Load index from disk if it exists, otherwise build it
        
        Returns:
            Loaded or newly built VectorStoreIndex
        """
        index, loaded_from_cache = self._cached_load_index()
        
        if loaded_from_cache and index is not None:
            return index
        
        # If we couldn't load from cache, build from scratch
        logger.info("Building new index from documents")
        return self.build_index() 