"""
Core RAG engine that handles queries, chat, and response generation
"""
import time
import logging
from typing import Dict, Any, List, Optional, Union

from llama_index.core import VectorStoreIndex, QueryBundle
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.llms.anthropic import Anthropic

from src.config import config
from src.index_manager import IndexManager

logger = logging.getLogger(__name__)

class Message:
    """Represents a message in a conversation"""
    
    def __init__(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a conversation message
        
        Args:
            role: Role of the message sender (user, assistant, system)
            content: Message content
            metadata: Optional message metadata
        """
        self.role = role
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "role": self.role,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary"""
        msg = cls(
            role=data["role"],
            content=data["content"],
            metadata=data.get("metadata", {})
        )
        msg.timestamp = data.get("timestamp", time.time())
        return msg


class Conversation:
    """Manages a conversation with history"""
    
    def __init__(self, max_history: int = 10):
        """
        Initialize a conversation
        
        Args:
            max_history: Maximum number of messages to keep in history
        """
        self.messages: List[Message] = []
        self.max_history = max_history
    
    def add_message(self, message: Message) -> None:
        """
        Add a message to the conversation
        
        Args:
            message: Message to add
        """
        self.messages.append(message)
        
        # Trim history if needed
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def add_user_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a user message to the conversation
        
        Args:
            content: Message content
            metadata: Optional message metadata
        """
        self.add_message(Message("user", content, metadata))
    
    def add_assistant_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an assistant message to the conversation
        
        Args:
            content: Message content
            metadata: Optional message metadata
        """
        self.add_message(Message("assistant", content, metadata))
    
    def get_messages(self) -> List[Message]:
        """Get all messages in the conversation"""
        return self.messages
    
    def get_chat_history(self) -> str:
        """
        Get formatted chat history as a string
        
        Returns:
            Formatted chat history
        """
        history = []
        for msg in self.messages:
            prefix = "User: " if msg.role == "user" else "Assistant: "
            history.append(f"{prefix}{msg.content}")
        
        return "\n".join(history)
    
    def clear(self) -> None:
        """Clear conversation history"""
        self.messages = []


class RAGEngine:
    """Core RAG engine to handle queries and responses"""
    
    def __init__(self, 
                index: Optional[VectorStoreIndex] = None, 
                config_manager=None,
                index_manager=None):
        """
        Initialize the RAG engine
        
        Args:
            index: Vector store index (loaded from manager if None)
            config_manager: Configuration manager (uses global instance if None)
            index_manager: Index manager (creates new instance if None)
        """
        self.config = config_manager or config
        self.index_manager = index_manager or IndexManager(self.config)
        
        # Load or use provided index
        self.index = index if index is not None else self.index_manager.load_index()
        
        # Set up the LLM
        self.llm = Anthropic(
            model=self.config.llm_model,
            api_key=self.config.anthropic_api_key,
            temperature=0
        )
        
        # Create query engine with the specified configuration
        self.query_engine = self._create_query_engine()
        
        # Initialize conversation
        self.conversation = Conversation()
    
    def _create_query_engine(self) -> BaseQueryEngine:
        """
        Create and configure the query engine
        
        Returns:
            Configured query engine
        """
        query_config = self.config.get_query_config()
        
        return self.index.as_query_engine(
            llm=self.llm,
            similarity_top_k=query_config["similarity_top_k"],
            response_mode=query_config["response_mode"]
        )
    
    def query(self, question: str, include_in_conversation: bool = True) -> Dict[str, Any]:
        """
        Process a query and return the response
        
        Args:
            question: User's question
            include_in_conversation: Whether to include this Q&A in conversation history
            
        Returns:
            Dictionary with response and metadata
        """
        logger.info(f"Processing query: {question}")
        start_time = time.time()
        
        # Add question to conversation history if requested
        if include_in_conversation:
            self.conversation.add_user_message(question)
        
        # Process the query
        response = self.query_engine.query(question)
        
        # Extract source nodes/documents if available
        source_nodes = getattr(response, 'source_nodes', [])
        sources = []
        for node in source_nodes:
            sources.append({
                "text": node.get_content(),
                "metadata": node.metadata
            })
        
        # Create result dictionary
        result = {
            "question": question,
            "answer": str(response),
            "sources": sources,
            "processing_time": time.time() - start_time
        }
        
        # Add to conversation history if requested
        if include_in_conversation:
            self.conversation.add_assistant_message(
                str(response),
                {"sources": sources}
            )
        
        return result
    
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Handle a chat message, incorporating conversation history
        
        Args:
            message: User's message
            
        Returns:
            Dictionary with response and metadata
        """
        # Format query with chat history context if we have prior messages
        if len(self.conversation.messages) > 0:
            history = self.conversation.get_chat_history()
            augmented_query = f"Given the following conversation history:\n{history}\n\nUser's new question: {message}\n\n You are an expert tutor in the field of Data Structures and Algorithms. Respond to the user's most recent question by thoroughly explaining the concept they're referring to."
            
            # Don't include this in conversation yet since we're using a special prompt
            result = self.query(augmented_query, include_in_conversation=False)
            
            # Now add the actual user message and response to the conversation
            self.conversation.add_user_message(message)
            self.conversation.add_assistant_message(result["answer"])
            
            return result
        else:
            # No history yet, just do a regular query
            return self.query(message)
    
    def reset_conversation(self) -> None:
        """Reset the conversation history"""
        self.conversation.clear()
        logger.info("Conversation history has been reset") 