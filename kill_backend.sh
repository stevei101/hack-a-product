#!/bin/bash
# Kill all backend processes

echo "🔪 Killing all backend processes..."

# Kill uvicorn processes
pkill -f "uvicorn agentic_app.main" 2>/dev/null || true
pkill -f "uv run uvicorn" 2>/dev/null || true

# Kill processes on ports 8000, 8001, 8002, 8003
for port in 8000 8001 8002 8003; do
    pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "Killing process $pid on port $port"
        kill -9 $pid 2>/dev/null || true
    fi
done

echo "✅ All backend processes killed!"
