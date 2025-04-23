#!/bin/bash

set -e  # exit on first error

source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Running classifier..."
python export_stats.py

python classifier.py
