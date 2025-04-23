#!/bin/bash

set -e  # exit on first error

echo "📦 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "⬇️ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Running classifier..."
python classifier.py
