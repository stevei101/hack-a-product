# 🐳 Podman Setup Guide

This project fully supports **Podman** as an alternative to Docker - it auto-detects which you have installed!

---

## ✅ What's Already Set Up

All scripts and commands **automatically detect** whether you're using Podman or Docker:

- ✅ `dev-setup.sh` - Detects and uses `podman compose`
- ✅ `Makefile` - All container commands use the right runtime
- ✅ `docker-compose.yml` - Compatible with both

---

## 🚀 Quick Start with Podman

### **Step 1: Verify Podman is Installed**

```bash
podman --version
# Should show: podman version 5.6.2 (or similar)
```

### **Step 2: Run Setup**

```bash
# Just run it - will auto-detect Podman!
./scripts/dev-setup.sh
```

**Output will show:**
```
✓ podman installed (container runtime)
🐳 [5/5] Starting local services (PostgreSQL & Redis)...
  🚀 Starting PostgreSQL and Redis with podman compose...
```

### **Step 3: Use Make Commands**

```bash
# All commands auto-detect Podman
make dev-start       # Uses podman compose
make container-build # Uses podman build
make container-run   # Uses podman run
```

---

## 🔧 Podman-Specific Commands

### **Check Services**

```bash
# List running containers
podman ps

# View compose services
podman compose ps

# View logs
podman logs product-mindset-postgres
podman logs product-mindset-redis
```

### **Manage Services**

```bash
# Start services
podman compose up -d

# Stop services
podman compose down

# Restart a specific service
podman compose restart postgres

# View logs in real-time
podman compose logs -f
```

### **Build Images**

```bash
# Build both images
make container-build
# Internally runs: podman build -t ...

# Or manually
podman build -t smithveunsa/react-bun-k8s:frontend .
podman build -t smithveunsa/react-bun-k8s:backend ./backend
```

---

## 📊 Podman vs. Docker Comparison

| Feature | Docker | Podman | Winner |
|---------|--------|--------|--------|
| Daemon | Requires dockerd | Daemonless | 🏆 Podman |
| Root Access | Usually needs root | Rootless by default | 🏆 Podman |
| Systemd | Limited | Native integration | 🏆 Podman |
| Compose | docker-compose | podman compose (built-in) | Tie |
| K8s YAML | No | Can generate K8s YAML | 🏆 Podman |
| Drop-in Replacement | N/A | 100% Docker-compatible | 🏆 Podman |
| Ecosystem | Larger | Growing fast | 🏆 Docker |

---

## 🔄 Switching Between Podman and Docker

The project **automatically detects** which runtime you have:

```bash
# Detection order (in Makefile):
CONTAINER_CMD := $(shell command -v podman || command -v docker)
COMPOSE_CMD := $(shell command -v podman && echo "podman compose" || echo "docker-compose")
```

**You can have both installed** - Podman takes priority.

---

## 🐛 Troubleshooting

### **Issue: "Permission Denied" with Volumes**

Podman runs rootless, so you may need to adjust SELinux labels:

```bash
# Add :Z flag to volumes in docker-compose.yml (already done!)
volumes:
  - postgres_data:/var/lib/postgresql/data:Z
```

**Already handled in our `docker-compose.yml`** ✅

### **Issue: "Cannot connect to Podman socket"**

Start the Podman service:

```bash
# macOS
podman machine start

# Linux (if using socket)
systemctl --user start podman.socket
```

### **Issue: "Images not found"**

Podman uses different registries by default. Specify docker.io:

```bash
# docker-compose.yml already specifies full paths:
image: docker.io/library/postgres:15-alpine  # ✅ Correct
```

### **Issue: "Compose command not found"**

If you have Podman < 4.0, install podman-compose:

```bash
# macOS
brew install podman-compose

# Or with pip
pip3 install podman-compose

# Then it will use: podman-compose instead of podman compose
```

---

## 📝 docker-compose.yml Compatibility

Our `docker-compose.yml` is fully compatible with both:

```yaml
services:
  postgres:
    image: docker.io/library/postgres:15-alpine  # Full registry path
    volumes:
      - postgres_data:/var/lib/postgresql/data   # Named volumes work
```

**Key compatibility features:**
- ✅ Full registry paths (`docker.io/library/...`)
- ✅ Named volumes (not host mounts)
- ✅ Standard port mappings
- ✅ Health checks
- ✅ Networks (default bridge network)

---

## 🎯 Podman-Specific Features

### **Generate Kubernetes YAML**

Podman can generate K8s manifests from your compose file!

```bash
# Generate K8s YAML for deployment
podman compose -f docker-compose.yml up --dry-run

# Or for running containers
podman generate kube product-mindset-postgres > k8s-postgres.yaml
```

### **Systemd Integration**

Run containers as systemd services:

```bash
# Generate systemd unit file
podman generate systemd --new --name product-mindset-postgres

# Install and enable
systemctl --user enable --now container-product-mindset-postgres
```

### **Pods (like Kubernetes)**

Group containers in pods:

```bash
# Create a pod
podman pod create --name product-mindset -p 5432:5432 -p 6379:6379

# Run containers in the pod
podman run -d --pod product-mindset postgres:15-alpine
podman run -d --pod product-mindset redis:7-alpine
```

---

## 🚀 Performance Tips

### **Use Podman's Built-in Registry**

```bash
# Pull once, use everywhere
podman pull docker.io/library/postgres:15-alpine
podman pull docker.io/library/redis:7-alpine
```

### **Prune Regularly**

```bash
# Clean up unused images
podman image prune -a

# Clean up volumes
podman volume prune

# Clean up everything
podman system prune -a --volumes
```

### **Use Podman Machine (macOS)**

```bash
# Initialize with more resources
podman machine init --cpus 4 --memory 8192 --disk-size 100

# Start the machine
podman machine start

# Check status
podman machine list
```

---

## 📚 References

- **Podman Docs**: https://docs.podman.io/
- **Compose Support**: https://docs.podman.io/en/latest/markdown/podman-compose.1.html
- **Migration Guide**: https://podman.io/docs/migration
- **Rootless Tutorial**: https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md

---

## ✅ Summary

**Your project is 100% Podman-ready!**

- ✅ Auto-detection in all scripts
- ✅ Compose file compatible
- ✅ Makefile commands work
- ✅ No code changes needed
- ✅ Works with Docker too

**Just use the commands as documented - Podman will be detected and used automatically!** 🚀

