"""
Document processing module for loading and processing documents
"""
import time
import logging
from typing import List, Optional
from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Node

from src.config import config
from src.metadata import create_metadata_extractor

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document loading and processing"""
    
    def __init__(self, config_manager=None):
        """
        Initialize document processor
        
        Args:
            config_manager: Configuration manager (uses global instance if None)
        """
        self.config = config_manager or config
        self.chunk_size = self.config.chunk_size
        self.chunk_overlap = self.config.chunk_overlap
        self.data_dir = self.config.data_dir
        
    def load_documents(self, directory: Optional[str] = None) -> List[Document]:
        """
        Load documents from directory
        
        Args:
            directory: Directory to load documents from (uses config if None)
            
        Returns:
            List of Document objects
        """
        target_dir = directory or self.data_dir
        logger.info(f"Loading documents from {target_dir}")
        start_time = time.time()
        
        try:
            docs = SimpleDirectoryReader(
                input_dir=target_dir,
                filename_as_id=True,
                metadata_extractor=create_metadata_extractor()
            ).load_data()
            
            elapsed = time.time() - start_time
            logger.info(f"Loaded {len(docs)} documents in {elapsed:.2f} seconds")
            return docs
            
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            raise
    
    def create_nodes(self, documents: List[Document]) -> List[Node]:
        """
        Split documents into nodes with appropriate chunking
        
        Args:
            documents: List of documents to process
            
        Returns:
            List of Node objects
        """
        logger.info(f"Creating nodes with chunk size {self.chunk_size} and overlap {self.chunk_overlap}")
        start_time = time.time()
        
        try:
            splitter = SentenceSplitter(
                chunk_size=self.chunk_size, 
                chunk_overlap=self.chunk_overlap
            )
            nodes = splitter.get_nodes_from_documents(documents)
            
            elapsed = time.time() - start_time
            logger.info(f"Created {len(nodes)} nodes in {elapsed:.2f} seconds")
            return nodes
            
        except Exception as e:
            logger.error(f"Error creating nodes: {str(e)}")
            raise
    
    def process_documents(self, directory: Optional[str] = None) -> List[Node]:
        """
        Load and process documents into nodes
        
        Args:
            directory: Directory to load documents from (uses config if None)
            
        Returns:
            List of processed Node objects
        """
        documents = self.load_documents(directory)
        return self.create_nodes(documents) 