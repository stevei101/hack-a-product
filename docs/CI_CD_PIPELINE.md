# CI/CD Pipeline Documentation

## Overview

This project uses **GitHub Actions** for CI/CD with **Terraform Cloud** for infrastructure management. The pipeline supports both local development (Bun + Podman + Minikube/k3s) and AWS production deployment (ECR + EKS).

## 🏗️ Architecture

### **Local Development Stack**
- **Frontend**: Bun (JavaScript runtime and package manager)
- **Backend**: Python 3.11+ with uv (dependency management)
- **Containers**: Podman (Docker alternative)
- **Kubernetes**: Minikube or k3s (local cluster)
- **Package Management**: Helm (Kubernetes package manager)

### **AWS Production Stack**
- **CI/CD**: GitHub Actions
- **Infrastructure**: Terraform Cloud
- **Container Registry**: Amazon ECR
- **Kubernetes**: Amazon EKS
- **Secrets Management**: GitHub Secrets

## 🔄 CI/CD Pipeline Flow

```
[Developer Push] → [GitHub Actions] → [Terraform Cloud] → [AWS EKS]
       ↓                ↓                    ↓              ↓
   [Code Tests]    [Build Images]    [Infrastructure]  [Deploy App]
       ↓                ↓                    ↓              ↓
   [Security Scan]  [Push to ECR]    [Update Config]   [Health Check]
```

## 📋 Pipeline Stages

### **1. Code Quality & Testing**
- **Linting**: ESLint for frontend, flake8 for backend
- **Type Checking**: TypeScript compilation
- **Security Scanning**: Dependency vulnerability checks
- **Unit Tests**: Jest for frontend, pytest for backend

### **2. Build & Containerization**
- **Frontend Build**: Bun build process
- **Backend Build**: Python with uv dependency management
- **Container Build**: Podman/Docker images
- **Multi-arch Support**: AMD64 and ARM64

### **3. Infrastructure Management**
- **Terraform Cloud**: Infrastructure as Code
- **Environment Variables**: Secure configuration management
- **GitHub Secrets**: Sensitive data handling
- **AWS Resources**: EKS, ECR, RDS, ElastiCache

### **4. Deployment**
- **ECR Push**: Container images to registry
- **EKS Deployment**: Kubernetes cluster updates
- **Helm Charts**: Application deployment
- **Health Checks**: Post-deployment validation

## 🔧 Configuration

### **GitHub Actions Workflows**

#### **Main Workflow** (`.github/workflows/main.yml`)
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install uv
        run: pip install uv
      - name: Run tests
        run: |
          bun test
          cd backend && uv pip install -r requirements.txt && pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Podman
        uses: containers/setup-podman@v2
      - name: Build images
        run: make container-build-registry REGISTRY=${{ secrets.ECR_REGISTRY }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to AWS
        run: |
          # Terraform Cloud integration
          # EKS deployment
```

### **Terraform Cloud Configuration**

#### **Environment Variables**
Set these in Terraform Cloud workspace:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=123456789012

# EKS Configuration
EKS_CLUSTER_NAME=product-mindset
EKS_NODE_GROUP_NAME=main-nodes
EKS_NODE_INSTANCE_TYPE=t3.medium

# Database Configuration
RDS_INSTANCE_CLASS=db.t3.micro
RDS_ALLOCATED_STORAGE=20

# Redis Configuration
REDIS_NODE_TYPE=cache.t3.micro
```

#### **GitHub Secrets**
Configure these in GitHub repository settings:

```bash
# AWS Authentication
AWS_ROLE_ARN=arn:aws:iam::123456789012:role/github-actions-role
AWS_REGION=us-east-1

# Container Registry
ECR_REGISTRY=123456789012.dkr.ecr.us-east-1.amazonaws.com
ECR_REPOSITORY_FRONTEND=product-mindset/frontend
ECR_REPOSITORY_BACKEND=product-mindset/backend

# Application Secrets
NIM_API_KEY=your_nvidia_api_key
GEMINI_API_KEY=your_google_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
FIGMA_ACCESS_TOKEN=your_figma_access_token
GITHUB_ACCESS_TOKEN=your_github_access_token
CURSOR_API_KEY=your_cursor_api_key

# Database
POSTGRES_PASSWORD=your_secure_postgres_password
REDIS_PASSWORD=your_secure_redis_password

# Terraform Cloud
TF_CLOUD_TOKEN=your_terraform_cloud_token
TF_CLOUD_ORGANIZATION=your_organization
TF_CLOUD_WORKSPACE=product-mindset-prod
```

## 🚀 Local Development Setup

### **Prerequisites Installation**

#### **macOS (using Homebrew)**
```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Install Podman
brew install podman

# Install Minikube
brew install minikube

# Install Helm
brew install helm

# Install uv
pip install uv
```

#### **Ubuntu/Debian**
```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Install Podman
sudo apt-get update
sudo apt-get install podman

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install uv
pip install uv
```

### **Development Commands**

```bash
# Start local development
make dev-start

# Build containers with Podman
make container-build

# Start local Kubernetes
make k8s start

# Deploy to local cluster
make deploy-local

# Stop everything
make dev-stop
```

## 🔒 Security Considerations

### **Secrets Management**
- **GitHub Secrets**: Store sensitive configuration
- **Terraform Cloud**: Environment-specific variables
- **AWS IAM**: Least privilege access
- **Container Scanning**: Vulnerability detection

### **Network Security**
- **VPC**: Isolated network environment
- **Security Groups**: Restrictive firewall rules
- **Private Subnets**: Database and cache isolation
- **Load Balancer**: SSL termination and routing

### **Compliance**
- **SOC 2**: Security controls
- **GDPR**: Data protection
- **HIPAA**: Healthcare compliance (if applicable)

## 📊 Monitoring & Observability

### **Application Monitoring**
- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **Jaeger**: Distributed tracing
- **ELK Stack**: Log aggregation

### **Infrastructure Monitoring**
- **AWS CloudWatch**: System metrics
- **Terraform Cloud**: Infrastructure state
- **GitHub Actions**: Pipeline metrics
- **Security Scanning**: Vulnerability reports

## 🛠️ Troubleshooting

### **Common Issues**

#### **Podman Issues**
```bash
# Initialize Podman machine
podman machine init
podman machine start

# Check Podman status
podman info
```

#### **Minikube Issues**
```bash
# Start Minikube
minikube start --driver=podman

# Check cluster status
kubectl cluster-info
```

#### **Terraform Cloud Issues**
```bash
# Check workspace status
terraform workspace show

# Validate configuration
terraform validate

# Plan changes
terraform plan
```

### **Debug Commands**
```bash
# Check GitHub Actions logs
gh run list
gh run view <run-id>

# Check Terraform Cloud runs
terraform cloud runs list

# Check AWS resources
aws eks describe-cluster --name product-mindset
aws ecr describe-repositories
```

## 📈 Performance Optimization

### **Build Optimization**
- **Multi-stage Dockerfiles**: Smaller images
- **Layer caching**: Faster builds
- **Parallel builds**: Concurrent processing
- **Dependency caching**: Reduced install time

### **Deployment Optimization**
- **Blue-green deployments**: Zero downtime
- **Rolling updates**: Gradual rollout
- **Health checks**: Automatic rollback
- **Resource limits**: Optimal resource usage

## 🔄 Maintenance

### **Regular Tasks**
- **Dependency updates**: Security patches
- **Image scanning**: Vulnerability detection
- **Backup verification**: Data integrity
- **Performance monitoring**: Optimization opportunities

### **Update Procedures**
1. **Test locally**: `make dev-start`
2. **Run tests**: `make test`
3. **Security scan**: `make security-scan`
4. **Deploy to staging**: GitHub Actions
5. **Deploy to production**: Manual approval

---

**This CI/CD pipeline provides a robust, secure, and scalable deployment process for The Product Mindset application.**
