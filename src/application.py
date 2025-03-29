"""
Application manager for the RAG system
"""
import time
import logging
import threading
from typing import Optional, Dict, Any

from src.config import config
from src.document_processor import DocumentProcessor
from src.index_manager import IndexManager
from src.rag_engine import RAGEngine

logger = logging.getLogger(__name__)

class ApplicationManager:
    """Manages the RAG application lifecycle and components"""
    
    def __init__(self):
        """
        Initialize the application manager
        
        Args:
            config_manager: Configuration manager (uses global instance if None)
        """
        logger.info("Initializing application manager...")
        
        # Initialize configuration
        self.config = config
        
        # Initialize components
        self.document_processor = DocumentProcessor(self.config)
        self.index_manager = IndexManager(self.config, self.document_processor)
        self.rag_engine = None
        self.preload_thread = None
            
    def start(self):
        """
        Start the application
        
        Args:
            preload_in_background: Whether to preload resources in background
            
        Returns:
            Initialized RAG engine
        """
        start_time = time.time()
        logger.info("Starting application...")
        
        # Check if we can use cached index
        has_cache = self.index_manager.check_cache_exists()
        
        # Start background preloading if enabled
        if self.config.background_preload and has_cache:
            self.preload_thread = self._start_background_preload()
        
        # Initialize RAG engine (this will load the index)
        self.rag_engine = RAGEngine(
            config_manager=self.config,
            index_manager=self.index_manager
        )
        
        logger.info(f"Application started in {time.time() - start_time:.2f} seconds")
    
    def _start_background_preload(self) -> threading.Thread:
        """
        Start preloading resources in a background thread
        
        Returns:
            Background thread
        """
        logger.info("Starting background preloading")
        thread = threading.Thread(target=self._preload_resources)
        thread.daemon = True  # Allow the thread to exit when the main program exits
        thread.start()
        return thread
    
    def _preload_resources(self):
        """Preload resources in background to speed up first query"""
        try:
            self.index_manager.initialize_models_lazy()
            logger.info("Resources preloaded")
        except Exception as e:
            logger.error(f"Error during background preloading: {str(e)}")
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query
        
        Args:
            query: User's query
            
        Returns:
            Response dictionary
        """
        if self.rag_engine is None:
            # Start the application if not already started
            self.start()
        
        try:
            query_start = time.time()
            response = self.rag_engine.query(query)
            query_time = time.time() - query_start
            
            logger.info(f"Query processed in {query_time:.2f} seconds")
            response["processing_time"] = query_time
            
            return response
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "question": query,
                "answer": f"Error: {str(e)}",
                "sources": [],
                "error": str(e)
            }
    
    def process_chat_message(self, message: str) -> Dict[str, Any]:
        """
        Process a chat message with conversation history
        
        Args:
            message: User's message
            
        Returns:
            Response dictionary
        """
        if self.rag_engine is None:
            # Start the application if not already started
            self.start()
        
        try:
            chat_start = time.time()
            response = self.rag_engine.chat(message)
            chat_time = time.time() - chat_start
            
            logger.info(f"Chat message processed in {chat_time:.2f} seconds")
            response["processing_time"] = chat_time
            
            return response
        except Exception as e:
            logger.error(f"Error processing chat message: {str(e)}")
            return {
                "question": message,
                "answer": f"Error: {str(e)}",
                "sources": [],
                "error": str(e)
            }
    
    def reset_conversation(self):
        """Reset the conversation history"""
        if self.rag_engine is not None:
            self.rag_engine.reset_conversation()
    
    def shutdown(self):
        """Shut down the application and clean up resources"""
        logger.info("Shutting down application...")
        
        # Any cleanup logic would go here
        
        logger.info("Application shutdown complete") 