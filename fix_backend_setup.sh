#!/bin/bash
# Fix Python environment and setup backend

echo "🔧 Fixing Python environment..."

# Remove broken virtual environment
if [ -d "backend/.venv" ]; then
    echo "🗑️  Removing broken virtual environment..."
    rm -rf backend/.venv
fi

# Create new virtual environment
echo "🐍 Creating new virtual environment..."
cd backend
python3 -m venv .venv

# Activate and upgrade pip
echo "⬆️  Upgrading pip..."
source .venv/bin/activate
python3 -m pip install --upgrade pip

# Install uv
echo "📦 Installing uv..."
python3 -m pip install uv

# Install requirements
echo "📋 Installing requirements..."
uv pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""
echo "🚀 You can now run:"
echo "  make backend-dev  # Start the backend server"
echo "  make dev         # Start the frontend"
