# The Product Mindset - AI-Powered Ideation & Design Companion

**The Product Mindset** is an AI-powered agentic workspace that acts as a thinking companion for creators and developers. Built for the AWS & NVIDIA Hackathon, it demonstrates cutting-edge AI integration with a focus on agentic workflows, retrieval-augmented generation, and multi-tool orchestration.

![Screenshot of the application UI](./preview.png)

## 🧠 Architecture — MCP Server Edition

This implementation features a **Model Context Protocol (MCP) Server** that orchestrates multiple AI tools and services, enabling seamless integration across different platforms and providers.

### 🔧 Core Features

- ✅ **MCP Server Orchestration** - Centralized coordination of multiple AI tools
- ✅ **Multi-Tool Integration** - Gemini, Figma, ChatGPT, GitHub, Cursor AI
- ✅ **NVIDIA NIM Integration** - Nemotron Nano 8B + Retrieval Embeddings
- ✅ **AWS Bedrock Support** - Claude 3 Sonnet for enterprise-grade AI
- ✅ **Agentic Workflows** - Parallel, sequential, and hybrid execution strategies
- ✅ **Modern React UI** - Clean, professional interface with tool selection

### 🧩 System Overview & MCP Architecture

```
[ Frontend (React + TypeScript) ]
        ↓
[ MCP Server API (/api/v1/mcp/*) ]
        ↓
[ Orchestration Engine ]
        ↙︎                        ↘︎
[Tool Connectors]              [NVIDIA NIM + AWS Bedrock]
        ↓                               ↓
[External APIs]                [Vector Memory Store]
```

### 🛠️ MCP Server Capabilities

#### **Tool Connectors**
- **Google Gemini** - Text generation and analysis
- **Figma** - Design collaboration and file access  
- **OpenAI ChatGPT** - Conversational AI and code generation
- **GitHub** - Repository access and code search
- **Cursor AI** - Code completion and generation

#### **Orchestration Strategies**
- **Parallel** - Execute multiple tools simultaneously
- **Sequential** - Chain tools with dependencies
- **Hybrid** - Batched parallel execution with configurable limits

#### **Workflow Templates**
- **Ideation Workflow** - Generate ideas using multiple AI models
- **Design & Code Workflow** - Design interfaces and generate code
- **Code Review Workflow** - Review code using multiple perspectives
- **Research Workflow** - Research topics using multiple sources

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**: For the backend API
- **Bun**: For frontend development and package management
- **Podman**: For containerization (Docker alternative)
- **Minikube/k3s**: For local Kubernetes development
- **Helm**: For Kubernetes package management
- **uv**: For Python dependency management
- **NVIDIA API Key**: For AI functionality (get from [NVIDIA NIM](https://build.nvidia.com))

### 🏃‍♂️ Get Started in 3 Steps

1. **Clean Start** (if you have port conflicts):
   ```bash
   make clean-all
   ```

2. **Quick Setup**:
   ```bash
   make quick-start
   ```

3. **Set Your API Keys**:
   ```bash
   # Edit backend/.env and add your API keys
   NIM_API_KEY=your_actual_nvidia_api_key_here
   GEMINI_API_KEY=your_google_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   FIGMA_ACCESS_TOKEN=your_figma_access_token_here
   GITHUB_ACCESS_TOKEN=your_github_access_token_here
   CURSOR_API_KEY=your_cursor_api_key_here
   ```

4. **Start the Application**:
   ```bash
   # Terminal 1: Start backend
   make backend-dev
   
   # Terminal 2: Start frontend
   make dev
   ```

## 🛠️ Makefile Commands

### **Development Commands**
- `make dev` - Start frontend development server
- `make backend-dev` - Start backend development server
- `make clean-all` - Clean everything and fix port conflicts
- `make kill-ports` - Kill processes on development ports

### **Setup Commands**
- `make quick-start` - Quick setup for testing
- `make backend-setup` - Set up backend environment
- `make backend-env` - Create environment variables file

### **Testing Commands**
- `make backend-test` - Test backend endpoints
- `python test_mcp_server.py` - Test MCP server functionality

### **Container Commands**
- `make container-build` - Build container images (uses Podman)
- `make container-run` - Run containers locally
- `make container-stop` - Stop running containers

### **Kubernetes Commands**
- `make k8s` - Manage local Kubernetes cluster (minikube/k3s)
- `make helm-install` - Install Helm chart
- `make helm-upgrade` - Upgrade Helm chart
- `make helm-uninstall` - Uninstall Helm chart

See `make help` for a complete list of available commands.

## 📡 API Endpoints

### **MCP Server Endpoints**
- `GET /api/v1/mcp/tools` - List available tools
- `GET /api/v1/mcp/tools/{tool_id}` - Get tool information
- `POST /api/v1/mcp/tools/execute` - Execute single tool
- `POST /api/v1/mcp/orchestrate` - Multi-tool orchestration
- `GET /api/v1/mcp/workflows` - List workflow templates
- `POST /api/v1/mcp/workflows/{template_id}/execute` - Execute template
- `GET /api/v1/mcp/health` - Check all tool health status

### **Core Application Endpoints**
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)

## 🔧 Configuration

### **Environment Variables**

Create `backend/.env` with the following variables:

```bash
# Database Configuration
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_postgres_password_here
POSTGRES_DB=agentic_app
POSTGRES_PORT=5432

# NVIDIA NIM Configuration
NIM_BASE_URL=https://integrate.api.nvidia.com/v1
NIM_API_KEY=your_nvidia_nim_api_key_here
NIM_MODEL_NAME=nvidia/llama-3_1-nemotron-nano-8b-v1
NIM_EMBEDDING_MODEL=nvidia/nv-embedqa-e5-v5

# MCP Server API Keys (Optional - tools will be disabled if not provided)
GEMINI_API_KEY=your_google_gemini_api_key_here
FIGMA_ACCESS_TOKEN=your_figma_access_token_here
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_ACCESS_TOKEN=your_github_access_token_here
CURSOR_API_KEY=your_cursor_api_key_here

# Security
SECRET_KEY=your_jwt_secret_key_here
API_KEY=your_api_authentication_key_here
```

### **Getting API Keys**

1. **NVIDIA NIM**: Get API key from [NVIDIA NIM](https://build.nvidia.com)
2. **Google Gemini**: Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Figma**: Generate access token from [Figma Account Settings](https://www.figma.com/settings)
4. **OpenAI**: Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
5. **GitHub**: Generate personal access token from [GitHub Settings](https://github.com/settings/tokens)
6. **Cursor**: Get API key from [Cursor AI Platform](https://cursor.sh)

## 🧪 Testing

### **Test MCP Server**
```bash
python test_mcp_server.py
```

### **Test Backend Endpoints**
```bash
make backend-test
```

### **Manual Testing**
1. Start the backend: `make backend-dev`
2. Start the frontend: `make dev`
3. Visit http://localhost:3000 for the UI
4. Visit http://localhost:8000/docs for API documentation

## 🏗️ Architecture Details

### **Frontend (React + TypeScript)**
- Modern React application with Bun
- Tool selection interface
- Real-time orchestration status
- Clean, professional UI matching the intended design

### **Backend (Python + FastAPI)**
- FastAPI application with async support
- MCP server with orchestration engine
- Tool connectors for external APIs
- Health monitoring and error handling

### **MCP Server Components**
- **Orchestration Engine** - Coordinates multiple tools
- **Tool Connectors** - Interface with external APIs
- **Workflow Templates** - Pre-configured workflows
- **Health Monitoring** - Real-time tool status

### **Database & Storage**
- PostgreSQL for application data
- Redis for caching and rate limiting
- Vector storage for embeddings (ChromaDB)

## 🚀 Deployment

### **Local Development (Bun + Podman + Minikube/k3s)**
```bash
make dev-start  # Start all services
make dev-stop   # Stop all services
```

### **Container Deployment (Podman)**
```bash
make container-build  # Build with Podman
make container-run    # Run containers
```

### **Kubernetes Deployment (Minikube/k3s + Helm)**
```bash
make k8s start        # Start local Kubernetes
make helm-install     # Install Helm chart
make deploy-local     # Deploy to local cluster
```

### **AWS Production (GitHub Actions + Terraform Cloud + EKS)**
- **CI/CD**: GitHub Actions with Terraform Cloud integration
- **Container Registry**: Amazon ECR
- **Kubernetes**: Amazon EKS
- **Infrastructure**: Terraform Cloud with environment variables
- **Secrets**: GitHub Secrets for sensitive configuration

## 📚 Documentation

- **[MCP Server Guide](docs/MCP_SERVER_GUIDE.md)** - Comprehensive MCP server documentation
- **[Tech Stack Guide](docs/TECH_STACK.md)** - Complete technology stack overview
- **[CI/CD Pipeline Guide](docs/CI_CD_PIPELINE.md)** - GitHub Actions + Terraform Cloud setup
- **[NIM Integration Guide](docs/NIM_INTEGRATION_GUIDE.md)** - NVIDIA NIM setup and usage
- **[Security Guide](SECURITY_AUDIT_PUBLIC_REPO.md)** - Security best practices
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Testing strategies and examples

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Hackathon Compliance

This implementation meets all AWS & NVIDIA Hackathon requirements:

- ✅ **NVIDIA NIM Integration** - Nemotron Nano 8B for reasoning
- ✅ **Retrieval Embedding NIM** - Semantic search and RAG
- ✅ **Agentic Behavior** - Multi-step reasoning and planning
- ✅ **AWS Bedrock Support** - Enterprise-grade AI capabilities
- ✅ **MCP Server** - Multi-tool orchestration and coordination

## 🆘 Troubleshooting

### **Port Conflicts**
```bash
make clean-all  # Clean everything and kill processes
make kill-ports # Kill processes on development ports
```

### **Backend Issues**
```bash
make backend-setup  # Reinstall dependencies
make backend-test   # Test endpoints
```

### **Frontend Issues**
```bash
rm -rf node_modules/
bun install
make dev
```

### **API Key Issues**
- Check that all required API keys are set in `backend/.env`
- Verify API keys are valid and have proper permissions
- Check tool health status: `GET /api/v1/mcp/health`

---

**Built with ❤️ using React, FastAPI, and MCP Server for the AWS & NVIDIA Hackathon**