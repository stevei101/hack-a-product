#!/bin/bash
# Quick setup script for development

echo "🚀 Setting up development environment..."

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "uvicorn agentic_app.main" 2>/dev/null || true
pkill -f "bun run dev" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
bun install

# Setup backend
echo "🐍 Setting up backend..."
cd backend && uv sync

echo "✅ Setup complete!"
echo ""
echo "🚀 Now you can run:"
echo "  make backend-dev  # Start backend (in one terminal)"
echo "  make dev         # Start frontend (in another terminal)"
