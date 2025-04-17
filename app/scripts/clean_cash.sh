#!/bin/bash
# From your project root directory

# Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete

# Package files
rm -rf ai_recruitment.egg-info/

# Streamlit cache
rm -rf ~/.streamlit/cache

# Optional: Clear stored resumes
# rm -rf storage/resumes/*

echo "All cache cleared!"