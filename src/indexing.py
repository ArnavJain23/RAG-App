from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.storage import StorageContext
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv
import os
import time
import logging
from functools import lru_cache

from src.config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, INDEX_CACHE_DIR
from src.metadata import create_metadata_extractor

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_documents():
    """Load documents from the data directory with metadata extraction"""
    logger.info(f"Loading documents from {DATA_DIR}")
    start_time = time.time()
    
    docs = SimpleDirectoryReader(
        input_dir=DATA_DIR
        # filename_as_id=True,
        # metadata_extractor=create_metadata_extractor()
    ).load_data()
    
    elapsed = time.time() - start_time
    logger.info(f"Loaded {len(docs)} documents in {elapsed:.2f} seconds")
    return docs

def create_nodes(documents):
    """Split documents into nodes with appropriate chunking"""
    logger.info(f"Creating nodes with chunk size {CHUNK_SIZE} and overlap {CHUNK_OVERLAP}")
    start_time = time.time()
    
    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    nodes = splitter.get_nodes_from_documents(documents)
    
    elapsed = time.time() - start_time
    logger.info(f"Created {len(nodes)} nodes in {elapsed:.2f} seconds")
    return nodes

def build_index(nodes=None, documents=None, persist=True):
    """
    Build a vector store index from nodes or documents
    
    Args:
        nodes: Pre-processed document nodes (optional)
        documents: Raw documents to process (optional)
        persist: Whether to persist the index to disk
        
    Returns:
        Built VectorStoreIndex
    """
    logger.info("Building index...")
    start_time = time.time()
    
    # Set Claude as LLM and HuggingFace for embeddings
    Settings.llm = Anthropic(model="claude-3-sonnet-20240229")
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    if nodes is None and documents is None:
        documents = load_documents()
        nodes = create_nodes(documents)
    elif nodes is None:
        nodes = create_nodes(documents)
    
    # Create the index
    index = VectorStoreIndex(nodes)
    
    elapsed = time.time() - start_time
    logger.info(f"Built index in {elapsed:.2f} seconds")
    
    # Persist index if requested
    if persist:
        persist_start = time.time()
        logger.info(f"Persisting index to {INDEX_CACHE_DIR}")
        os.makedirs(INDEX_CACHE_DIR, exist_ok=True)
        index.storage_context.persist(persist_dir=INDEX_CACHE_DIR)
        persist_elapsed = time.time() - persist_start
        logger.info(f"Persisted index in {persist_elapsed:.2f} seconds")
    
    return index

# Add caching decorator to avoid repeated loading
@lru_cache(maxsize=1)
def _cached_load_index():
    """Internal function to load index with caching"""
    start_time = time.time()
    
    try:
        logger.info(f"Attempting to load index from {INDEX_CACHE_DIR}")
        # Only initialize the embeddings model - delay other initializations
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        
        # Use optimized storage context loading
        storage_context = StorageContext.from_defaults(
            persist_dir=INDEX_CACHE_DIR
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

def load_index():
    """Load index from disk if it exists, otherwise build it"""
    index, loaded_from_cache = _cached_load_index()
    
    if loaded_from_cache and index is not None:
        return index
    
    # If we couldn't load from cache, build from scratch
    logger.info("Building new index from documents")
    documents = load_documents()
    nodes = create_nodes(documents)
    return build_index(nodes=nodes)

def initialize_models_lazy():
    """Lazily initialize models only when needed"""
    # Only set the model configurations but don't actually load the models
    # They will be loaded on first use
    Settings.llm = Anthropic(model="claude-3-sonnet-20240229", temperature=0)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    logger.info("Models initialized lazily") 