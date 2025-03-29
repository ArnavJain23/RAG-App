from src.rag_engine import RAGEngine

def main():
    """Run the RAG CLI application"""
    print("RAG CLI for Document Q&A - Type 'exit' to quit")
    
    # Initialize the RAG engine
    engine = RAGEngine()
    
    while True:
        query = input("\nEnter your question: ")
        if query.lower() in ('exit', 'quit', 'q'):
            break
        
        # Process the query
        response = engine.query(query)
        print(f"\nAnswer: {response}")

if __name__ == "__main__":
    main() 