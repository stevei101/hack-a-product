# Tech Stack Documentation

## Overview

The Product Mindset uses a modern, cloud-native tech stack optimized for both local development and AWS production deployment.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Local Dev     │    │   CI/CD         │    │   AWS Prod      │
│                 │    │                 │    │                 │
│ Bun + Podman    │───▶│ GitHub Actions  │───▶│ ECR + EKS       │
│ Minikube/k3s    │    │ Terraform Cloud │    │ RDS + ElastiCache│
│ Helm Charts     │    │ Security Scans  │    │ CloudWatch      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🖥️ Frontend Stack

### **Primary Technologies**
- **Bun**: JavaScript runtime and package manager
  - Fast package installation
  - Built-in bundler and test runner
  - Native TypeScript support
  - Compatible with npm ecosystem

- **React 18**: UI framework
  - Functional components with hooks
  - Concurrent features
  - Server-side rendering ready

- **TypeScript**: Type safety
  - Strict type checking
  - Enhanced IDE support
  - Better refactoring capabilities

- **Tailwind CSS**: Utility-first CSS
  - Rapid UI development
  - Responsive design
  - Custom design system

### **Development Tools**
- **Vite**: Build tool and dev server
  - Fast hot module replacement
  - Optimized production builds
  - Plugin ecosystem

- **ESLint**: Code linting
  - Code quality enforcement
  - Custom rules for React/TypeScript
  - Pre-commit hooks

- **Prettier**: Code formatting
  - Consistent code style
  - Automatic formatting
  - Editor integration

## 🐍 Backend Stack

### **Primary Technologies**
- **Python 3.11+**: Programming language
  - Modern Python features
  - Async/await support
  - Type hints

- **uv**: Python package manager
  - Ultra-fast dependency resolution
  - Drop-in pip replacement
  - Lock file support
  - Virtual environment management

- **FastAPI**: Web framework
  - High performance
  - Automatic API documentation
  - Type validation with Pydantic
  - Async support

- **SQLAlchemy**: ORM
  - Database abstraction
  - Migration support
  - Connection pooling

### **Database & Storage**
- **PostgreSQL**: Primary database
  - ACID compliance
  - JSON support
  - Full-text search
  - Connection pooling

- **Redis**: Caching and sessions
  - In-memory storage
  - Pub/sub messaging
  - Rate limiting
  - Session storage

- **ChromaDB**: Vector database
  - Embedding storage
  - Similarity search
  - RAG support

### **AI & ML Integration**
- **NVIDIA NIM**: Inference microservices
  - Nemotron Nano 8B model
  - Retrieval embeddings
  - GPU acceleration

- **AWS Bedrock**: Enterprise AI
  - Claude 3 Sonnet
  - Bedrock Guardrails
  - Managed service

- **MCP Server**: Tool orchestration
  - Multi-tool coordination
  - Workflow management
  - Health monitoring

## 🐳 Containerization

### **Podman (Primary)**
- **Rootless containers**: Enhanced security
- **Docker-compatible**: Easy migration
- **Systemd integration**: Service management
- **BuildKit support**: Advanced builds

### **Container Images**
- **Frontend**: Node.js-based with Bun
- **Backend**: Python-based with uv
- **Multi-stage builds**: Optimized size
- **Security scanning**: Vulnerability detection

### **Container Registry**
- **Local**: Podman local registry
- **Development**: GitHub Container Registry
- **Production**: Amazon ECR

## ☸️ Kubernetes & Orchestration

### **Local Development**
- **Minikube**: Local Kubernetes
  - Single-node cluster
  - Podman driver support
  - Addon ecosystem

- **k3s**: Lightweight Kubernetes
  - Resource efficient
  - Easy setup
  - Production-ready

### **Production (AWS)**
- **Amazon EKS**: Managed Kubernetes
  - High availability
  - Auto-scaling
  - Security integration

### **Package Management**
- **Helm**: Kubernetes package manager
  - Chart templating
  - Release management
  - Dependency resolution

### **Helm Charts**
- **Frontend Chart**: React application
- **Backend Chart**: FastAPI service
- **Database Chart**: PostgreSQL
- **Cache Chart**: Redis

## 🔄 CI/CD Pipeline

### **GitHub Actions**
- **Workflow automation**: Code to deployment
- **Matrix builds**: Multiple environments
- **Security scanning**: Vulnerability detection
- **Artifact management**: Build outputs

### **Terraform Cloud**
- **Infrastructure as Code**: Declarative management
- **State management**: Centralized state
- **Environment variables**: Secure configuration
- **Run triggers**: Automated execution

### **Deployment Strategies**
- **Blue-green**: Zero downtime
- **Rolling updates**: Gradual rollout
- **Canary releases**: Risk mitigation
- **Feature flags**: Controlled rollouts

## ☁️ AWS Services

### **Compute**
- **Amazon EKS**: Kubernetes service
- **EC2**: Virtual machines
- **Fargate**: Serverless containers
- **Lambda**: Serverless functions

### **Storage**
- **Amazon ECR**: Container registry
- **S3**: Object storage
- **EFS**: File system
- **EBS**: Block storage

### **Database**
- **Amazon RDS**: Managed PostgreSQL
- **ElastiCache**: Managed Redis
- **DynamoDB**: NoSQL database
- **RDS Proxy**: Connection pooling

### **Networking**
- **VPC**: Virtual private cloud
- **ALB**: Application load balancer
- **Route 53**: DNS service
- **CloudFront**: CDN

### **Monitoring**
- **CloudWatch**: Monitoring and logging
- **X-Ray**: Distributed tracing
- **CloudTrail**: Audit logging
- **Config**: Configuration management

## 🔒 Security Stack

### **Authentication & Authorization**
- **AWS IAM**: Identity and access management
- **OIDC**: OpenID Connect
- **JWT**: JSON Web Tokens
- **RBAC**: Role-based access control

### **Secrets Management**
- **GitHub Secrets**: CI/CD secrets
- **AWS Secrets Manager**: Application secrets
- **Terraform Cloud**: Infrastructure secrets
- **Vault**: Advanced secret management

### **Security Scanning**
- **Trivy**: Container vulnerability scanning
- **Snyk**: Dependency vulnerability scanning
- **Bandit**: Python security linting
- **ESLint Security**: JavaScript security rules

### **Network Security**
- **VPC**: Network isolation
- **Security Groups**: Firewall rules
- **WAF**: Web application firewall
- **Private Subnets**: Database isolation

## 📊 Monitoring & Observability

### **Application Monitoring**
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Jaeger**: Distributed tracing
- **ELK Stack**: Log aggregation

### **Infrastructure Monitoring**
- **CloudWatch**: AWS metrics
- **Terraform Cloud**: Infrastructure state
- **GitHub Actions**: Pipeline metrics
- **Uptime monitoring**: Service availability

### **Logging**
- **Structured logging**: JSON format
- **Log levels**: DEBUG, INFO, WARN, ERROR
- **Correlation IDs**: Request tracing
- **Centralized collection**: ELK stack

## 🛠️ Development Tools

### **IDE & Editors**
- **VS Code**: Primary editor
- **Cursor**: AI-powered editor
- **Vim/Neovim**: Terminal editing
- **IntelliJ**: Full IDE

### **Version Control**
- **Git**: Source control
- **GitHub**: Repository hosting
- **GitHub Actions**: CI/CD
- **GitHub Packages**: Artifact storage

### **Testing**
- **Jest**: Frontend testing
- **pytest**: Backend testing
- **Playwright**: E2E testing
- **Cypress**: UI testing

### **Code Quality**
- **Pre-commit hooks**: Quality gates
- **Code reviews**: Peer review
- **Automated testing**: CI integration
- **Security scanning**: Vulnerability detection

## 📈 Performance Optimization

### **Frontend Optimization**
- **Code splitting**: Lazy loading
- **Tree shaking**: Dead code elimination
- **Bundle optimization**: Size reduction
- **CDN**: Content delivery

### **Backend Optimization**
- **Async/await**: Non-blocking I/O
- **Connection pooling**: Database efficiency
- **Caching**: Redis integration
- **Load balancing**: Traffic distribution

### **Database Optimization**
- **Indexing**: Query performance
- **Connection pooling**: Resource efficiency
- **Read replicas**: Read scaling
- **Partitioning**: Data organization

## 🔄 Migration & Compatibility

### **Docker to Podman**
- **Command compatibility**: Drop-in replacement
- **Image compatibility**: Same format
- **Registry compatibility**: Same protocols
- **Build compatibility**: Same Dockerfiles

### **Local to Cloud**
- **Environment parity**: Consistent behavior
- **Configuration management**: Environment variables
- **Secrets management**: Secure handling
- **Monitoring**: Consistent observability

## 📚 Learning Resources

### **Bun**
- [Official Documentation](https://bun.sh/docs)
- [Migration Guide](https://bun.sh/docs/installation)
- [Performance Comparison](https://bun.sh/docs/benchmarks)

### **Podman**
- [Official Documentation](https://podman.io/docs)
- [Docker Migration](https://podman.io/getting-started/migration)
- [Rootless Containers](https://podman.io/getting-started/rootless)

### **uv**
- [Official Documentation](https://docs.astral.sh/uv/)
- [Migration from pip](https://docs.astral.sh/uv/pip/)
- [Performance Benefits](https://docs.astral.sh/uv/benchmarks/)

### **Terraform Cloud**
- [Official Documentation](https://developer.hashicorp.com/terraform/cloud-docs)
- [GitHub Integration](https://developer.hashicorp.com/terraform/cloud-docs/run/run-triggers)
- [Environment Variables](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/variables)

---

**This tech stack provides a modern, scalable, and maintainable foundation for The Product Mindset application.**
