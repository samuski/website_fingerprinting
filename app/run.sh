#!/bin/bash

set -e  # exit on first error

source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Exporting stats.csv..."
python export_stats.py
echo "Running classifier..."
python classifier.py
