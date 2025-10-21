#!/bin/bash
#
# One-Command Development Setup
# Sets up The Product Mindset for local development
#
# Run: ./scripts/dev-setup.sh
#

set -e

echo "🚀 Setting up The Product Mindset for local development..."
echo "=========================================================="
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# ============================================================================
# Check prerequisites
# ============================================================================

echo "📋 [1/5] Checking prerequisites..."

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        echo "  ✓ $1 installed"
        return 0
    else
        echo "  ❌ $1 not installed"
        return 1
    fi
}

MISSING_DEPS=0

check_command "bun" || { echo "     Install from: https://bun.sh"; MISSING_DEPS=1; }
check_command "docker" || { echo "     Install from: https://docker.com"; MISSING_DEPS=1; }
check_command "git" || { echo "     Usually pre-installed"; MISSING_DEPS=1; }

# Check for uv (preferred) or python3
if command -v uv >/dev/null 2>&1; then
    echo "  ✓ uv installed (Python package manager)"
elif command -v python3 >/dev/null 2>&1; then
    echo "  ⚠️  python3 found, but uv is recommended"
    echo "     Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "  ❌ Neither uv nor python3 found"
    echo "     Install from: https://docs.astral.sh/uv/"
    MISSING_DEPS=1
fi

if [ $MISSING_DEPS -eq 1 ]; then
    echo ""
    echo "❌ Missing required dependencies. Please install them and run again."
    exit 1
fi

echo "  ✅ All prerequisites met!"
echo ""

# ============================================================================
# Frontend setup
# ============================================================================

echo "⚛️  [2/5] Setting up frontend..."

if [ ! -d "node_modules" ]; then
    echo "  📦 Installing frontend dependencies..."
    bun install
else
    echo "  ✓ Frontend dependencies already installed"
fi

echo "  ✅ Frontend ready!"
echo ""

# ============================================================================
# Backend setup
# ============================================================================

echo "🐍 [3/5] Setting up backend environment..."

cd backend

# Use uv for Python environment management
if [ ! -d ".venv" ]; then
    echo "  🔨 Creating Python virtual environment with uv..."
    # Use uv to create venv with Python 3.11+ (automatically finds best version)
    uv venv --python 3.11
else
    echo "  ✓ Virtual environment exists"
fi

# Install dependencies using uv (much faster than pip!)
echo "  📦 Installing backend dependencies with uv..."
uv pip install -e ".[dev]"

echo "  ✅ Backend environment ready!"
echo ""

# ============================================================================
# Environment configuration
# ============================================================================

echo "⚙️  [4/5] Configuring environment..."

if [ ! -f ".env" ]; then
    echo "  📝 Creating .env from example..."
    cp env.example .env
    
    # Generate secure keys
    SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo "CHANGE_ME_$(date +%s)")
    API_KEY=$(openssl rand -hex 32 2>/dev/null || echo "CHANGE_ME_$(date +%s)")
    
    # Update .env with generated keys
    if command -v sed >/dev/null 2>&1; then
        sed -i.bak "s/your-secret-key-here/$SECRET_KEY/" .env 2>/dev/null || true
        sed -i.bak "s/your-api-key-here/$API_KEY/" .env 2>/dev/null || true
        rm -f .env.bak
    fi
    
    echo "  ✅ Created .env file"
    echo ""
    echo "  ⚠️  IMPORTANT: Edit backend/.env and add:"
    echo "      NIM_API_KEY=your_nvidia_api_key"
    echo ""
    echo "  💡 Get your NVIDIA API key from: https://build.nvidia.com/explore/discover"
else
    echo "  ✓ .env file already exists"
fi

cd ..

echo "  ✅ Environment configured!"
echo ""

# ============================================================================
# Start local services
# ============================================================================

echo "🐳 [5/5] Starting local services (PostgreSQL & Redis)..."

if command -v docker-compose >/dev/null 2>&1 || command -v docker >/dev/null 2>&1; then
    if [ -f "docker-compose.yml" ]; then
        echo "  🚀 Starting PostgreSQL and Redis with Docker Compose..."
        docker-compose up -d
        
        echo "  ⏳ Waiting for services to be healthy..."
        sleep 5
        
        echo "  ✅ Services started!"
    else
        echo "  ⚠️  docker-compose.yml not found. Services not started."
        echo "      Run ./scripts/apply-quick-wins.sh to create it."
    fi
else
    echo "  ⚠️  Docker not running. Skipping service startup."
fi

echo ""

# ============================================================================
# Summary
# ============================================================================

echo "=========================================================="
echo "✅ Development Environment Ready!"
echo "=========================================================="
echo ""
echo "📋 What's configured:"
echo "  ✓ Frontend dependencies (Bun + React + TypeScript)"
echo "  ✓ Backend environment (Python + FastAPI)"
echo "  ✓ Local databases (PostgreSQL + Redis)"
echo "  ✓ Environment variables (.env)"
echo ""
echo "🚀 Next steps:"
echo ""
echo "  1. Add your NVIDIA API key to backend/.env:"
echo "     NIM_API_KEY=nvapi-..."
echo ""
echo "  2. Start the backend:"
echo "     cd backend && source .venv/bin/activate"
echo "     uvicorn agentic_app.main:app --reload"
echo ""
echo "  3. Start the frontend (in another terminal):"
echo "     bun run dev"
echo ""
echo "  4. Open your browser:"
echo "     Frontend: http://localhost:3000"
echo "     Backend API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Quick commands:"
echo "  make dev-start       - Start all services"
echo "  make dev-stop        - Stop all services"
echo "  make help            - Show all available commands"
echo ""
echo "📖 For more information, see:"
echo "  - README.md"
echo "  - docs/CODE_REVIEW_AND_IMPROVEMENTS.md"
echo ""

