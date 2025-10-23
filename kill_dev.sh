#!/bin/bash
# Kill all development processes

echo "🧹 Killing all development processes..."

# Kill backend processes
pkill -f "uvicorn agentic_app.main" 2>/dev/null || true
pkill -f "uv run uvicorn" 2>/dev/null || true

# Kill frontend processes  
pkill -f "bun run dev" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

# Kill any processes on ports 8000 and 3000
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

echo "✅ All processes killed!"
echo "🚀 You can now run:"
echo "  make backend-dev  # Start backend"
echo "  make dev         # Start frontend"
