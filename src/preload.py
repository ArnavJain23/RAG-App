"""
Preloading module for optimizing startup time
"""
import os
import threading
import logging
from src.config import INDEX_CACHE_DIR
from src.indexing import initialize_models_lazy

logger = logging.getLogger(__name__)

def check_cache_exists():
    """Check if the index cache exists"""
    if not os.path.exists(INDEX_CACHE_DIR):
        return False
    
    # Check for essential files in the cache directory
    required_files = ["docstore.json", "index_store.json"]
    for file in required_files:
        if not os.path.exists(os.path.join(INDEX_CACHE_DIR, file)):
            return False
    
    return True

def preload_resources():
    """Preload resources in background to speed up first query"""
    initialize_models_lazy()
    logger.info("Resources preloaded")
    
def start_background_preload():
    """Start preloading resources in a background thread"""
    logger.info("Starting background preloading")
    thread = threading.Thread(target=preload_resources)
    thread.daemon = True  # Allow the thread to exit when the main program exits
    thread.start()
    return thread
