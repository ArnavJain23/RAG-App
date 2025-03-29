from src.indexing import load_documents, create_nodes, build_index
import os
from src.config import INDEX_CACHE_DIR

def main():
    """Build and save the document index"""
    print("Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")
    
    print("Creating nodes...")
    nodes = create_nodes(documents)
    print(f"Created {len(nodes)} nodes")
    
    print("Building index...")
    index = build_index(nodes=nodes, persist=True)
    print(f"Index built and saved to {INDEX_CACHE_DIR}")

if __name__ == "__main__":
    main()
