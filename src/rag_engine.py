from llama_index.llms.anthropic import Anthropic
from llama_index.core import VectorStoreIndex
from typing import Dict, Any, List, Optional

from src.config import LLM_MODEL
from src.indexing import load_index

class RAGEngine:
    """Core RAG engine to handle queries and responses"""
    
    def __init__(self, index: Optional[VectorStoreIndex] = None):
        """
        Initialize the RAG engine
        
        Args:
            index: Vector store index (loaded from disk if not provided)
        """
        # Set up the LLM
        self.llm = Anthropic(model=LLM_MODEL)
        
        # Load or use provided index
        self.index = index if index is not None else load_index()
        
        # Create query engine
        self.query_engine = self.index.as_query_engine(llm=self.llm)
    
    def query(self, question: str) -> str:
        """
        Process a query and return the response
        
        Args:
            question: User's question
            
        Returns:
            Response from the RAG system
        """
        response = self.query_engine.query(question)
        return str(response)
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Handle a chat conversation with history
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Response from the RAG system
        """
        # This is a simplified implementation
        # A more sophisticated version would use a chat engine with memory
        
        # Extract the latest user question
        user_question = messages[-1]['content'] if messages[-1]['role'] == 'user' else ""
        
        if not user_question:
            return "I didn't receive a question. How can I help you?"
        
        # Process the question
        return self.query(user_question) 