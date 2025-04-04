'''#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/.." || exit

# Add project root to Python path
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Activate conda environment
conda activate gemini
find . -type d -name "__pycache__" -exec rm -r {} +

# Load environment variables
set -a
source .env
set +a

# Run the Streamlit app
streamlit run app/main.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --logger.level=${LOG_LEVEL}

'''
#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/.." || exit

# Install package in editable mode
pip install -e .

# Run the Streamlit app
streamlit run app/main.py \