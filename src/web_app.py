"""
Web API for the RAG application
"""
import logging
import time
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from src.application import ApplicationManager

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'rag-application-secret-key'  # Change this to a secure random key in production
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Configure CORS to allow requests from frontend
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "https://rag-app-frontend.vercel.app"])

# Initialize application manager (will be lazy-loaded on first request)
app_manager = None

def get_app_manager():
    """
    Lazy-load the application manager
    
    Returns:
        Initialized ApplicationManager
    """
    global app_manager
    if app_manager is None:
        logger.info("Initializing application manager...")
        app_manager = ApplicationManager()
        app_manager.start()
    return app_manager

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "API is running"})

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Process a chat message
    
    Request JSON format:
    {
        "message": "Your question about the book"
    }
    
    Response JSON format:
    {
        "question": "Original question",
        "answer": "Generated response",
        "sources": [...],
        "processing_time": 1.23
    }
    """
    # Get the application manager
    manager = get_app_manager()
    
    # Get request data
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' field"}), 400
    
    message = data['message']
    logger.info(f"Received chat message: {message}")
    
    # Process the message
    start_time = time.time()
    try:
        result = manager.process_chat_message(message)
        logger.info(f"Chat processed in {time.time() - start_time:.2f} seconds")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        return jsonify({
            "question": message,
            "answer": f"Error processing your request: {str(e)}",
            "sources": [],
            "error": str(e),
            "processing_time": time.time() - start_time
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset the current conversation history"""
    # Get the application manager
    manager = get_app_manager()
    
    # Reset the conversation
    try:
        manager.reset_conversation()
        logger.info("Conversation reset")
        return jsonify({"status": "ok", "message": "Conversation history reset"})
    except Exception as e:
        logger.error(f"Error resetting conversation: {str(e)}")
        return jsonify({
            "error": f"Error resetting conversation: {str(e)}"
        }), 500

def run_app(host='localhost', port=8080, debug=False):
    """
    Run the Flask application
    
    Args:
        host: Host to bind to
        port: Port to listen on
        debug: Whether to run in debug mode
    """
    logger.info(f"Starting web server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_app(debug=True) 