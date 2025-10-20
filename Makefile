# Makefile for React + Bun + Kubernetes project
# Provides convenient commands for development, building, and deployment

.PHONY: help dev build test clean container-build container-run container-push deploy check-prerequisites

# Default target
help: ## Show this help message
	@echo "React + Bun + Kubernetes Project"
	@echo "================================="
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development commands
dev: ## Start development server
	bun run dev

build: ## Build the React application
	bun run build

preview: ## Preview the built application
	bun run preview

test: ## Run tests (placeholder - add your test command here)
	@echo "No tests configured yet. Add your test command to package.json"

clean: ## Clean build artifacts
	rm -rf dist/
	rm -rf node_modules/

# Container commands (auto-detects Docker/Podman)
container-build: ## Build container image (auto-detects Docker/Podman)
	./scripts/build.sh

container-run: ## Run container locally
	@if command -v podman &> /dev/null; then \
		podman run -p 8080:80 react-bun-k8s; \
	elif command -v docker &> /dev/null; then \
		docker run -p 8080:80 react-bun-k8s; \
	else \
		echo "❌ No container runtime found. Install Docker or Podman."; \
		exit 1; \
	fi

container-push: ## Push container to registry (usage: make container-push REGISTRY=docker.io/username)
	./scripts/push.sh $(REGISTRY)

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

# Complete setup commands
full-setup: check-prerequisites install k8s-setup ## Complete setup including Kubernetes
	@echo "🎉 Complete environment ready!"
	@echo "Run 'make deploy' to deploy your app"
