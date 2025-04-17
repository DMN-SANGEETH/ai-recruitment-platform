#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/.." || exit

# Add project root to Python path
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Activate conda environment if running locally
if command -v conda &> /dev/null; then
    conda activate gemini
fi

# Clean pycache files
#find . -type d -name "__pycache__" -exec rm -r {} +

# Load environment variables from .env if it exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Run the Streamlit app
streamlit run app/main.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --logger.level=${LOG_LEVEL:-INFO}