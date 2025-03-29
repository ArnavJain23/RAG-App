from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.storage import StorageContext
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv
import os

from src.config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, INDEX_CACHE_DIR
from src.metadata import create_metadata_extractor

# Load environment variables from .env file
load_dotenv()

def load_documents():
    """Load documents from the data directory with metadata extraction"""
    return SimpleDirectoryReader(
        input_dir=DATA_DIR
        # filename_as_id=True,
        # metadata_extractor=create_metadata_extractor()
    ).load_data()

def create_nodes(documents):
    """Split documents into nodes with appropriate chunking"""
    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.get_nodes_from_documents(documents)

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
    
    # Persist index if requested
    if persist:
        os.makedirs(INDEX_CACHE_DIR, exist_ok=True)
        index.storage_context.persist(persist_dir=INDEX_CACHE_DIR)
    
    return index

def load_index():
    """Load index from disk if it exists, otherwise build it"""
    try:
        # Try to load from disk
        storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore.from_persist_dir(INDEX_CACHE_DIR),
            index_store=SimpleIndexStore.from_persist_dir(INDEX_CACHE_DIR),
        )
        index = VectorStoreIndex.from_storage(storage_context)
        return index
    except:
        # Build from scratch if loading fails
        documents = load_documents()
        nodes = create_nodes(documents)
        return build_index(nodes=nodes) 