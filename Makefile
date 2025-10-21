# Makefile for The Product Mindset - Agentic Application
# Provides convenient commands for development, building, and deployment

.PHONY: help dev build test clean container-build container-run container-push deploy check-prerequisites

# Default target
help: ## Show this help message
	@echo "The Product Mindset - Agentic Application"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Frontend Development commands
dev: ## Start frontend development server
	bun run dev

build: ## Build the React application
	bun run build

preview: ## Preview the built application
	bun run preview

test: ## Run tests (placeholder - add your test command here)
	@echo "No tests configured yet. Add your test command to package.json"

# Backend Development commands
backend-dev: ## Start backend development server
	cd backend && source .venv/bin/activate && python3 test_server.py

backend-setup: ## Set up backend environment
	@if [ ! -d "backend/.venv" ]; then \
		cd backend && python3 -m venv .venv; \
	fi
	cd backend && source .venv/bin/activate && pip install uv && uv pip install fastapi uvicorn sqlalchemy asyncpg httpx pydantic pydantic-settings numpy

backend-env: ## Create secure environment variables file
	./setup_env.sh

backend-test: ## Test backend endpoints
	@echo "Testing backend endpoints..."
	@curl -s http://localhost:8000/health | head -5
	@curl -s http://localhost:8000/api/v1/nim/health | head -5

backend-logs: ## View backend logs
	@echo "Backend logs (if running):"
	@ps aux | grep test_server | grep -v grep

# Security commands
security-scan: ## Run security vulnerability scan
	./security_scan.sh

security-report: ## Generate security report
	@echo "🔍 Security Report Generated"
	@echo "📄 Check SECURITY_REPORT.md for detailed findings"
	@echo "🔧 Check SECURITY_FIXES.md for implementation guide"

security-setup: ## Set up secure environment and run security scan
	@echo "🔐 Setting up secure environment..."
	./setup_env.sh
	@echo "🔍 Running security scan..."
	./security_scan.sh

clean: ## Clean build artifacts
	rm -rf dist/
	rm -rf node_modules/

# Container commands (auto-detects Docker/Podman)
CONTAINER_CMD := $(shell command -v podman 2>/dev/null || command -v docker 2>/dev/null || echo "")
COMPOSE_CMD := $(shell command -v podman 2>/dev/null && echo "podman compose" || echo "docker-compose")

container-build: ## Build container images for both frontend and backend
	@if [ -z "$(CONTAINER_CMD)" ]; then \
		echo "❌ Error: Neither podman nor docker found"; \
		echo "   Install podman: https://podman.io"; \
		exit 1; \
	fi
	@echo "🐳 Using: $(CONTAINER_CMD)"
	@echo "Building frontend container..."
	$(CONTAINER_CMD) build -t smithveunsa/react-bun-k8s:frontend .
	@echo "Building backend container..."
	$(CONTAINER_CMD) build -t smithveunsa/react-bun-k8s:backend ./backend

container-build-registry: ## Build and tag for registry (usage: make container-build-registry REGISTRY=ghcr.io/username)
	@if [ -z "$(REGISTRY)" ]; then \
		echo "❌ Please specify REGISTRY (e.g., make container-build-registry REGISTRY=ghcr.io/username)"; \
		exit 1; \
	fi
	@echo "🐳 Using: $(CONTAINER_CMD)"
	@echo "Building and tagging for registry: $(REGISTRY)"
	$(CONTAINER_CMD) build -t $(REGISTRY):frontend .
	$(CONTAINER_CMD) build -t $(REGISTRY):backend ./backend

container-run: ## Run containers locally
	@echo "🐳 Using: $(CONTAINER_CMD)"
	@echo "Starting backend container..."
	$(CONTAINER_CMD) run -d --name backend -p 8000:8000 smithveunsa/react-bun-k8s:backend
	@echo "Starting frontend container..."
	$(CONTAINER_CMD) run -d --name frontend -p 3000:80 smithveunsa/react-bun-k8s:frontend
	@echo "✅ Containers started! Backend: http://localhost:8000, Frontend: http://localhost:3000"

container-stop: ## Stop running containers
	@echo "🛑 Stopping containers..."
	$(CONTAINER_CMD) stop backend frontend || true
	$(CONTAINER_CMD) rm backend frontend || true

container-push: ## Push containers to registry (usage: make container-push REGISTRY=ghcr.io/username)
	@if [ -z "$(REGISTRY)" ]; then \
		echo "❌ Please specify REGISTRY (e.g., make container-push REGISTRY=ghcr.io/username)"; \
		exit 1; \
	fi
	@echo "🐳 Using: $(CONTAINER_CMD)"
	@echo "Pushing to registry: $(REGISTRY)"
	$(CONTAINER_CMD) push $(REGISTRY):frontend
	$(CONTAINER_CMD) push $(REGISTRY):backend

# GitHub Actions Deployment commands
github-secrets: ## Show required GitHub repository secrets
	@echo "🔐 Required GitHub Repository Secrets:"
	@echo "  AWS_ROLE_ARN=arn:aws:iam::YOUR_ACCOUNT:role/product-mindset-github-actions-dev"
	@echo "  AWS_REGION=us-east-1"
	@echo "  NIM_API_KEY=your_nvidia_api_key"
	@echo "  POSTGRES_PASSWORD=your_secure_password"
	@echo ""
	@echo "📝 Add these secrets in GitHub: Settings → Secrets and variables → Actions"

github-deploy: ## Trigger GitHub Actions deployment
	@echo "🚀 Triggering GitHub Actions deployment..."
	@echo "📝 Push to 'main' or 'develop' branch to trigger deployment"
	@echo "🔗 Check Actions tab in your GitHub repository"

github-troubleshoot: ## Troubleshoot GitHub Actions AWS OIDC issues
	@echo "🔍 Running AWS OIDC troubleshooting..."
	./scripts/troubleshoot-aws-oidc.sh

github-test-auth: ## Test GitHub Actions AWS authentication
	@echo "🧪 Testing GitHub Actions AWS authentication..."
	@echo "📝 Push to 'develop' branch to trigger AWS auth test"
	@echo "🔗 Check Actions tab for 'Test AWS Authentication' workflow"

github-verify: ## Verify GitHub repository configuration
	@echo "🔍 Verifying GitHub repository setup..."
	./scripts/verify-github-setup.sh

github-config: ## Check GitHub configuration checklist
	@echo "📋 GitHub configuration checklist..."
	./scripts/check-github-config.sh

# Terraform Cloud commands (for infrastructure management)
terraform-validate: ## Validate Terraform configuration locally
	cd terraform && terraform validate

terraform-format: ## Format Terraform files
	cd terraform && terraform fmt -recursive

# Helm commands
helm-install: ## Install Helm chart
	helm install frontend ./charts/frontend --namespace web --create-namespace

helm-upgrade: ## Upgrade Helm chart
	helm upgrade --install frontend ./charts/frontend --namespace web

helm-uninstall: ## Uninstall Helm chart
	helm uninstall frontend --namespace web

# Kubernetes management
k8s: ## Manage local Kubernetes cluster (usage: make k8s command)
	./scripts/k8s-manage.sh $(filter-out $@,$(MAKECMDGOALS))

# Full workflow commands
deploy-local: ## Deploy to local Kubernetes (minikube/kind)
	./scripts/deploy.sh local latest

deploy-staging: ## Deploy to staging environment
	./scripts/deploy.sh staging staging

deploy-production: ## Deploy to production environment
	./scripts/deploy.sh production latest

# Quick start commands
quick-start: backend-env backend-setup ## Quick start for testing
	@echo "🚀 Setting up The Product Mindset for testing..."
	@echo "✅ Backend environment ready!"
	@echo "📝 Next steps:"
	@echo "  1. Edit backend/.env and set your NVIDIA API key"
	@echo "  2. Run 'make backend-dev' to start the backend"
	@echo "  3. Run 'make dev' to start the frontend"
	@echo "  4. Visit http://localhost:3000 for the UI"
	@echo "  5. Visit http://localhost:8000/docs for API docs"

full-start: backend-env backend-setup install ## Complete setup for development
	@echo "🚀 Setting up The Product Mindset for full development..."
	@echo "✅ Frontend and backend environments ready!"
	@echo "📝 Next steps:"
	@echo "  1. Edit backend/.env and set your NVIDIA API key"
	@echo "  2. Run 'make backend-dev' to start the backend"
	@echo "  3. Run 'make dev' to start the frontend"
	@echo "  4. Visit http://localhost:3000 for the UI"
	@echo "  5. Visit http://localhost:8000/docs for API docs"

secure-start: security-setup backend-setup install ## Complete secure setup with security scan
	@echo "🔐 Setting up The Product Mindset with security best practices..."
	@echo "✅ Secure environment ready!"
	@echo "📝 Next steps:"
	@echo "  1. Edit backend/.env and set your NVIDIA API key"
	@echo "  2. Run 'make backend-dev' to start the backend"
	@echo "  3. Run 'make dev' to start the frontend"
	@echo "  4. Review security report in SECURITY_REPORT.md"

# Complete setup commands
full-setup: check-prerequisites install k8s-setup ## Complete setup including Kubernetes
	@echo "🎉 Complete environment ready!"
	@echo "Run 'make deploy' to deploy your app"

# New: Streamlined development commands
dev-setup: ## One-command development setup (recommended for new developers)
	@./scripts/dev-setup.sh

dev-start: ## Start all development services (frontend + backend + databases)
	@echo "🚀 Starting development environment..."
	@echo "🐳 Using: $(COMPOSE_CMD)"
	@$(COMPOSE_CMD) up -d
	@echo "⏳ Waiting for services..."
	@sleep 3
	@echo ""
	@echo "🔧 Starting backend..."
	@cd backend && source .venv/bin/activate && uvicorn agentic_app.main:app --reload --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
	@echo "⚛️  Starting frontend..."
	@bun run dev > logs/frontend.log 2>&1 &
	@sleep 2
	@echo ""
	@echo "✅ Development environment running!"
	@echo "   Frontend: http://localhost:3000"
	@echo "   Backend:  http://localhost:8000/docs"
	@echo "   Logs:     tail -f logs/*.log"
	@echo ""
	@echo "💡 Use 'make dev-stop' to stop all services"

dev-stop: ## Stop all development services
	@echo "🛑 Stopping development environment..."
	@$(COMPOSE_CMD) down 2>/dev/null || true
	@pkill -f "uvicorn agentic_app.main" 2>/dev/null || true
	@pkill -f "bun run dev" 2>/dev/null || true
	@echo "✅ All services stopped!"

dev-logs: ## View development logs
	@echo "📋 Development Logs (Ctrl+C to exit)"
	@tail -f logs/*.log 2>/dev/null || echo "No logs found. Run 'make dev-start' first."

apply-quick-wins: ## Apply quick-win improvements from code review
	@./scripts/apply-quick-wins.sh
