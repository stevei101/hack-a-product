# Using `uv` for Python Development

This project uses [`uv`](https://github.com/astral-sh/uv) for Python package management - it's **10-100x faster** than pip!

---

## 🚀 Quick Start

### **Install uv**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Or with pip (if you must)
pip install uv
```

---

## 📦 Project Setup

### **Option 1: Automated Setup (Recommended)**

```bash
# Run the setup script (uses uv automatically)
./scripts/dev-setup.sh
```

### **Option 2: Manual Setup with uv**

```bash
# Navigate to backend
cd backend

# Create virtual environment (uv auto-selects Python 3.11+)
uv venv

# Activate environment
source .venv/bin/activate

# Install dependencies (super fast!)
uv pip install -e ".[dev]"

# Create environment file
cp env.example .env
```

---

## 💡 Why uv?

| Feature | pip | uv |
|---------|-----|-----|
| Speed | 1x | **10-100x faster** |
| Dependency Resolution | Slow | **Rust-powered** |
| Python Version Selection | Manual | **Automatic** |
| Lock Files | Separate tool | **Built-in** |
| Unified Interface | Multiple tools | **One tool** |

---

## 🔧 Common Commands

### **Install Dependencies**

```bash
# Install from pyproject.toml
uv pip install -e ".[dev]"

# Install single package
uv pip install fastapi

# Install with specific version
uv pip install "fastapi>=0.104.0"
```

### **Update Dependencies**

```bash
# Update all packages
uv pip install --upgrade -e ".[dev]"

# Update specific package
uv pip install --upgrade fastapi
```

### **Create New Project**

```bash
# Create new venv with specific Python version
uv venv --python 3.13

# Or let uv pick the best available version
uv venv --python 3.11
```

### **List Installed Packages**

```bash
uv pip list
```

### **Generate Requirements**

```bash
uv pip freeze > requirements.txt
```

---

## 🐛 Troubleshooting

### **Python Version Issues**

If you see:
```
× No solution found when resolving dependencies
╰─▶ the current Python version (3.10.11) does not satisfy Python>=3.11
```

**Solution:**
```bash
# Remove old venv
rm -rf backend/.venv

# Create new venv with Python 3.11+
cd backend
uv venv --python 3.11

# Install dependencies
uv pip install -e ".[dev]"
```

### **uv Not Found**

If `uv` command is not found after installation:

```bash
# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Or restart your shell
source ~/.zshrc  # or ~/.bashrc
```

### **Virtual Environment Not Activating**

```bash
# Make sure you're in the backend directory
cd backend

# Activate explicitly
source .venv/bin/activate

# Verify Python version
python --version  # Should show 3.11+
```

---

## 📚 Advanced Usage

### **Pin Dependencies**

```bash
# Generate lock file
uv pip compile pyproject.toml -o requirements.lock

# Install from lock file
uv pip sync requirements.lock
```

### **Use Different Python Version**

```bash
# Create venv with specific version
uv venv --python /opt/homebrew/bin/python3.13

# Or use python3.11, python3.12, etc.
uv venv --python python3.13
```

### **Install from GitHub**

```bash
uv pip install git+https://github.com/user/repo.git
```

---

## 🔗 Resources

- **uv Documentation**: https://docs.astral.sh/uv/
- **GitHub**: https://github.com/astral-sh/uv
- **Installation Guide**: https://docs.astral.sh/uv/getting-started/installation/

---

## 🆚 Migration from pip

If you're used to pip, here's the mapping:

| pip | uv |
|-----|-----|
| `pip install package` | `uv pip install package` |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `pip install -e .` | `uv pip install -e .` |
| `pip freeze` | `uv pip freeze` |
| `pip list` | `uv pip list` |
| `python -m venv .venv` | `uv venv` |

**Key difference**: `uv` is just faster - same commands, same workflow! ⚡

---

## ✅ Current Project Status

This project **already uses uv** in:
- ✅ `scripts/dev-setup.sh` - Automatic setup script
- ✅ `backend/pyproject.toml` - Dependency definitions
- ✅ `.gitignore` - Ignores .venv directories

**Just run and enjoy the speed!** 🚀

