#!/bin/bash

# Task Manager API - Quick Setup Script
# This script sets up the project for local development

set -e  # Exit on error

echo "🚀 Task Manager API - Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "   Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "   ✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "   ✅ Dependencies installed"
echo ""

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v
echo ""

# Success message
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run the application: python app/app.py"
echo "   3. API will be available at: http://localhost:5000"
echo ""
echo "📖 Check README.md for API documentation and usage examples"
echo ""
