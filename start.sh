#!/bin/bash
# Start script for production deployment

# Activate virtual environment if available
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set production environment variable
export FLASK_ENV=production

# Start the application with Gunicorn if available
if command -v gunicorn &> /dev/null; then
    echo "Starting with Gunicorn..."
    gunicorn --workers 1 --timeout 120 --bind 0.0.0.0:$PORT "src.web_app:app"
else
    echo "Starting with Flask development server..."
    python3 app.py
fi 