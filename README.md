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

```bash
python app.py
```
Then open your browser to http://localhost:5000