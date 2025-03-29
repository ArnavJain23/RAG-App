# Retrieval Augmented Generation (RAG) Application

A Retrieval Augmented Generation (RAG) application that allows users to ask questions about the book: "Introduction to Algorithms 3rd Edition."

## Overview

This application uses LlamaIndex and Anthropic's Claude to create a question-answering system specifically about "Introduction to Algorithms 3rd Edition." Users can interact with the application through a web interface.

## Features

- **Document Loading and Preprocessing**: Efficiently processes and chunks the book content
- **Vector Indexing and Retrieval**: Creates and manages vector indices for efficient information retrieval
- **Query Processing with Context-aware Responses**: Generates accurate answers based on book content
- **Conversation History Management**: Maintains context across interactions
- **Background Resource Preloading**: Optimizes startup time through preloading models

## Technology Stack

- **Framework**: LlamaIndex for the RAG pipeline
- **LLM**: Anthropic Claude
- **Performance**: Thread-based background loading for optimization

## Technologies Used

### 1. Flask
- **Why Chosen**: Flask is a lightweight and flexible web framework for Python. It is easy to set up and allows for rapid development of web applications. Its simplicity and modularity make it an excellent choice for building RESTful APIs, which is essential for our backend.

### 2. SQLAlchemy
- **Why Chosen**: SQLAlchemy is a powerful ORM (Object-Relational Mapping) library for Python. It provides a high-level abstraction for database interactions, making it easier to manage database schemas and queries. This helps in maintaining clean and efficient code while ensuring database integrity.

### 3. Flask-CORS
- **Why Chosen**: Flask-CORS is an extension that allows Cross-Origin Resource Sharing (CORS) in Flask applications. It is essential for enabling the frontend to communicate with the backend, especially when they are hosted on different domains or ports.

The following features could be added to improve the backend functionality:

1. **Chat Session Management**:
   - Implement a system for managing multiple chat sessions. This would allow users to have concurrent chats without losing context, enhancing the user experience and making the application more versatile.

2. **Multi-Document Support**:
   - Extend the backend to support multiple documents, allowing users to upload and manage various documents simultaneously. This would be particularly useful for applications that require handling large datasets or multiple sources of information.

3. **Faster Indexing**:
   - Optimize the indexing process to ensure that new data can be added quickly and efficiently. This could involve implementing background indexing processes or using more efficient data structures to speed up the retrieval and storage of indexed data.

4. **User Authentication and Authorization**:
   - Implement user authentication and authorization to secure the API endpoints. This would allow for personalized experiences and protect sensitive data.

## Challenges Faced

- **Connecting Frontend and Backend**:
  - Establishing communication between the frontend and backend required the creation of a RESTful API in the backend.
  - The frontend needed to make HTTP requests to these API endpoints to retrieve and send data.
  
- **CORS Issues**:
  - Encountered Cross-Origin Resource Sharing (CORS) issues when the frontend and backend were hosted on different ports. This required configuring Flask-CORS in the backend to allow requests from the frontend.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Anthropic API key

### Installation

1. Clone the repository:
```bash
git clone git@github.com:ArnavJain23/RAG-App.git
cd RAG-App
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

5. Prepare your data:
   - Place the text version of "Introduction to Algorithms 3rd Edition" in the `data/` directory

### Running the Web App

Start the backend server by executing:
```bash
python app.py
```
The backend will be running at `http://127.0.0.1:8080`. You can verify it by visiting this URL in your web browser.
