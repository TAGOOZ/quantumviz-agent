#!/bin/bash
# QuantumViz Agent - Web Interface Startup Script

echo "🌐 Starting QuantumViz Agent Web Interface..."
echo "================================================"

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export FLASK_ENV=development
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Start the web server
cd src
python web/app.py
