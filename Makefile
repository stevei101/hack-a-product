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

# E2E Testing commands
e2e-test: ## Run all E2E tests
	@echo "🧪 Running E2E tests..."
	cd tests/e2e && python3 run_all_tests.py

e2e-test-api-keys: ## Run API key E2E tests
	@echo "🔑 Running API key E2E tests..."
	cd tests/e2e && python3 test_api_keys.py

e2e-test-agents: ## Run agent E2E tests
	@echo "🤖 Running agent E2E tests..."
	cd tests/e2e && python3 test_agents.py

e2e-test-nim: ## Run NVIDIA NIM E2E tests
	@echo "🚀 Running NVIDIA NIM E2E tests..."
	cd tests/e2e && python3 test_nim_integration.py

e2e-setup: ## Set up E2E test environment
	@echo "🔧 Setting up E2E test environment..."
	@echo "📝 Creating test API keys..."
	@echo "ℹ️  Make sure your backend is running with 'make backend-dev'"
	@echo "ℹ️  Set your NVIDIA API key in backend/.env for NIM tests"
	@echo "✅ E2E test environment ready!"

e2e-full: backend-dev e2e-test ## Run full E2E test suite with backend
	@echo "🎉 Full E2E test suite completed!"

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
container-build: ## Build container images for both frontend and backend
	@echo "Building frontend container..."
	docker build -t smithveunsa/react-bun-k8s:frontend .
	@echo "Building backend container..."
	docker build -t smithveunsa/react-bun-k8s:backend ./backend

container-build-registry: ## Build and tag for registry (usage: make container-build-registry REGISTRY=ghcr.io/username)
	@if [ -z "$(REGISTRY)" ]; then \
		echo "❌ Please specify REGISTRY (e.g., make container-build-registry REGISTRY=ghcr.io/username)"; \
		exit 1; \
	fi
	@echo "Building and tagging for registry: $(REGISTRY)"
	docker build -t $(REGISTRY):frontend .
	docker build -t $(REGISTRY):backend ./backend

container-run: ## Run containers locally
	@echo "Starting backend container..."
	docker run -d --name backend -p 8000:8000 smithveunsa/react-bun-k8s:backend
	@echo "Starting frontend container..."
	docker run -d --name frontend -p 3000:80 smithveunsa/react-bun-k8s:frontend
	@echo "✅ Containers started! Backend: http://localhost:8000, Frontend: http://localhost:3000"

container-stop: ## Stop running containers
	docker stop backend frontend || true
	docker rm backend frontend || true

container-push: ## Push containers to registry (usage: make container-push REGISTRY=ghcr.io/username)
	@if [ -z "$(REGISTRY)" ]; then \
		echo "❌ Please specify REGISTRY (e.g., make container-push REGISTRY=ghcr.io/username)"; \
		exit 1; \
	fi
	@echo "Pushing to registry: $(REGISTRY)"
	docker push $(REGISTRY):frontend
	docker push $(REGISTRY):backend

# Docker Hub specific commands (current setup)
dockerhub-build: ## Build for Docker Hub (smithveunsa/react-bun-k8s)
	docker build -t smithveunsa/react-bun-k8s:frontend .
	docker build -t smithveunsa/react-bun-k8s:backend ./backend

dockerhub-push: ## Push to Docker Hub (smithveunsa/react-bun-k8s)
	docker push smithveunsa/react-bun-k8s:frontend
	docker push smithveunsa/react-bun-k8s:backend

# GHCR specific commands (future migration)
ghcr-build: ## Build for GHCR (usage: make ghcr-build USERNAME=your-username)
	@if [ -z "$(USERNAME)" ]; then \
		echo "❌ Please specify USERNAME (e.g., make ghcr-build USERNAME=your-username)"; \
		exit 1; \
	fi
	docker build -t ghcr.io/$(USERNAME)/product-mindset:frontend .
	docker build -t ghcr.io/$(USERNAME)/product-mindset:backend ./backend

ghcr-push: ## Push to GHCR (usage: make ghcr-push USERNAME=your-username)
	@if [ -z "$(USERNAME)" ]; then \
		echo "❌ Please specify USERNAME (e.g., make ghcr-push USERNAME=your-username)"; \
		exit 1; \
	fi
	docker push ghcr.io/$(USERNAME)/product-mindset:frontend
	docker push ghcr.io/$(USERNAME)/product-mindset:backend


# Kubernetes deployment commands
deploy: ## Deploy to Kubernetes using Helm
	./scripts/deploy.sh

deploy-dev: ## Deploy development version
	./scripts/deploy.sh web dev

deploy-prod: ## Deploy production version
	./scripts/deploy.sh web latest

# Utility commands
check-prerequisites: ## Check if all required tools are installed
	./scripts/check-prerequisites.sh

install: ## Install dependencies
	bun install

# Docker-specific commands (if you prefer explicit Docker usage)
docker-build: ## Build with Docker explicitly
	docker build -t react-bun-k8s .

docker-run: ## Run with Docker explicitly
	docker run -p 8080:80 react-bun-k8s

docker-push: ## Push with Docker explicitly
	docker push react-bun-k8s

# Podman-specific commands (if you prefer explicit Podman usage)
podman-build: ## Build with Podman explicitly
	podman build --format=docker -t react-bun-k8s .

podman-run: ## Run with Podman explicitly
	podman run -p 8080:80 react-bun-k8s

podman-push: ## Push with Podman explicitly (usage: make podman-push IMAGE=your/image:tag)
	podman push $(IMAGE)

# Helm commands
helm-install: ## Install Helm chart
	helm install frontend ./charts/frontend --namespace web --create-namespace

helm-upgrade: ## Upgrade Helm chart
	helm upgrade --install frontend ./charts/frontend --namespace web

helm-uninstall: ## Uninstall Helm chart
	helm uninstall frontend --namespace web

# Full workflow commands
# Kubernetes setup commands
k8s-setup: ## Set up local Kubernetes cluster
	./scripts/setup-k8s.sh

k8s-kind: ## Create Kind cluster
	kind create cluster --name react-app
	kubectl cluster-info --context kind-react-app

k8s-minikube: ## Start Minikube with Podman
	minikube start --driver=podman
	kubectl get nodes

k8s-stop: ## Stop Kubernetes cluster
	@if command -v kind &> /dev/null; then \
		kind delete cluster --name react-app; \
	elif command -v minikube &> /dev/null; then \
		minikube stop; \
	else \
		echo "No Kubernetes cluster found to stop"; \
	fi

k8s-status: ## Check Kubernetes cluster status
	kubectl cluster-info
	kubectl get nodes
	kubectl get pods --all-namespaces

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
