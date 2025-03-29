import os
from typing import Dict, Any, List
from llama_index.core import Document

def extract_metadata(document: Document) -> Dict[str, Any]:
    """
    Extract metadata from documents based on filename, content, etc.
    
    Args:
        document: The document to extract metadata from
    
    Returns:
        Dictionary of metadata attributes
    """
    filename = document.metadata.get('file_name', '')
    
    # Extract basic file metadata
    metadata = {
        'file_name': filename,
        'file_extension': os.path.splitext(filename)[1] if filename else '',
        'character_count': len(document.text),
    }
    
    # You can add more sophisticated metadata extraction here
    # For example, extracting authors, dates, titles, etc.
    
    return metadata

def create_metadata_extractor():
    """
    Creates a metadata extractor function for SimpleDirectoryReader
    
    Returns:
        Metadata extractor function
    """
    def extractor(file_path: str) -> Dict[str, Any]:
        base_metadata = {
            'file_name': os.path.basename(file_path),
            'file_path': file_path,
            'file_type': os.path.splitext(file_path)[1],
            'creation_date': os.path.getctime(file_path),
            'last_modified': os.path.getmtime(file_path),
        }
        return base_metadata
        
    return extractor 