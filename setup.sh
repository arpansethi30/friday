#!/bin/bash

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create required directories
mkdir -p logs
mkdir -p data
mkdir -p config

# Create empty __init__.py files in module directories
touch modules/__init__.py
touch features/__init__.py

echo "Setup complete!"
