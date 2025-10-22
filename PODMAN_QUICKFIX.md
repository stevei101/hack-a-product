# 🚀 Podman Quick Fix (macOS)

## Issue
```
Cannot connect to Podman socket
Error: unable to connect to Podman socket: dial tcp 127.0.0.1:57202: connect: operation not permitted
```

## Solution

On macOS, Podman runs in a VM that needs to be started first.

### **Quick Fix:**

```bash
# Check if machine exists
podman machine list

# If no machine exists, create one:
podman machine init

# Start the machine
podman machine start

# Verify it's running
podman machine list
# Should show "Currently running"
```

### **Then try again:**

```bash
make dev-start
# or
podman compose up -d
```

---

## One-Time Setup

After the first `podman machine start`, the machine will auto-start on login (by default).

**To configure auto-start:**
```bash
# Enable auto-start (default)
podman machine set --rootful=false

# Check settings
podman machine inspect
```

---

## Manual Commands

```bash
# Start
podman machine start

# Stop
podman machine stop

# Status
podman machine list

# SSH into machine (for debugging)
podman machine ssh
```

---

## Alternative: Use Docker Instead

If you prefer, the code works with Docker too:

```bash
# Just install Docker Desktop
# Everything will auto-detect and use Docker instead
```

Both work seamlessly! 🐳

