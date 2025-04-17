#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/.." || exit

# Install package in editable mode
pip install -e .

# Add project root to Python path
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Run the Streamlit app
streamlit run app/main.py