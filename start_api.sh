#!/bin/bash
# QuantumViz Agent - API Server Startup Script

echo "🚀 Starting QuantumViz Agent API Server..."
echo "================================================"

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export FLASK_ENV=development
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Start the API server
cd src
python api/quantum_api.py
