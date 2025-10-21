#!/bin/bash
#
# Apply Quick-Win Improvements
# Implements P0 recommendations from CODE_REVIEW_AND_IMPROVEMENTS.md
#
# Run: ./scripts/apply-quick-wins.sh
#

set -e

echo "🚀 Applying Quick-Win Improvements..."
echo "======================================"
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# ============================================================================
# 1. Clean up unused/duplicate files
# ============================================================================

echo "📁 [1/4] Cleaning up unused files and directories..."

# Remove Java code from Python project
if [ -d "backend/src/main/java" ]; then
    echo "  ❌ Removing Java code (backend/src/main/java)..."
    rm -rf backend/src/main/java
fi

# Remove empty Kubernetes manifests directory
if [ -d "kubernetes/manifests" ] && [ -z "$(ls -A kubernetes/manifests)" ]; then
    echo "  ❌ Removing empty directory (kubernetes/manifests)..."
    rm -rf kubernetes/manifests
fi

# Remove design system backup
if [ -d "design-system-backup" ]; then
    echo "  ❌ Removing design-system-backup..."
    rm -rf design-system-backup
fi

# Remove kost directory if it exists
if [ -d "kost" ]; then
    echo "  ❌ Removing kost directory..."
    rm -rf kost
fi

echo "  ✅ Cleanup complete!"
echo ""

# ============================================================================
# 2. Update .gitignore
# ============================================================================

echo "📝 [2/4] Updating .gitignore..."

GITIGNORE=".gitignore"

# Create .gitignore if it doesn't exist
if [ ! -f "$GITIGNORE" ]; then
    touch "$GITIGNORE"
fi

# Add entries if not already present
add_to_gitignore() {
    local entry="$1"
    if ! grep -qF "$entry" "$GITIGNORE"; then
        echo "$entry" >> "$GITIGNORE"
        echo "  ➕ Added: $entry"
    fi
}

add_to_gitignore "# Build artifacts"
add_to_gitignore "dist/"
add_to_gitignore ""
add_to_gitignore "# Python"
add_to_gitignore "backend/__pycache__/"
add_to_gitignore "**/__pycache__/"
add_to_gitignore "*.pyc"
add_to_gitignore "*.pyo"
add_to_gitignore "*.pyd"
add_to_gitignore ".Python"
add_to_gitignore "backend/.venv/"
add_to_gitignore "backend/venv/"
add_to_gitignore ""
add_to_gitignore "# Environment files"
add_to_gitignore ".env"
add_to_gitignore ".env.local"
add_to_gitignore "backend/.env"
add_to_gitignore ""
add_to_gitignore "# IDE"
add_to_gitignore ".vscode/"
add_to_gitignore ".idea/"
add_to_gitignore "*.swp"
add_to_gitignore "*.swo"
add_to_gitignore ""
add_to_gitignore "# OS"
add_to_gitignore ".DS_Store"
add_to_gitignore "Thumbs.db"

echo "  ✅ .gitignore updated!"
echo ""

# ============================================================================
# 3. Clean Terraform variables (remove unused AWS credentials)
# ============================================================================

echo "🏗️  [3/4] Cleaning Terraform variables..."

TERRAFORM_VARS="terraform/variables.tf"

if [ -f "$TERRAFORM_VARS" ]; then
    # Check if the unused variables exist
    if grep -q "AWS_ACCESS_KEY_ID" "$TERRAFORM_VARS"; then
        echo "  🔧 Removing unused AWS credential variables..."
        
        # Create backup
        cp "$TERRAFORM_VARS" "$TERRAFORM_VARS.backup"
        
        # Remove the variables (lines 46-56)
        sed -i.tmp '/variable "AWS_ACCESS_KEY_ID"/,/^}/d' "$TERRAFORM_VARS"
        sed -i.tmp '/variable "AWS_SECRET_ACCESS_KEY"/,/^}/d' "$TERRAFORM_VARS"
        
        # Clean up temp file
        rm -f "$TERRAFORM_VARS.tmp"
        
        echo "  ✅ Cleaned up Terraform variables!"
        echo "  💾 Backup saved to: terraform/variables.tf.backup"
    else
        echo "  ✓ Terraform variables already clean"
    fi
else
    echo "  ⚠️  terraform/variables.tf not found, skipping..."
fi

echo ""

# ============================================================================
# 4. Create docker-compose.yml for local development
# ============================================================================

echo "🐳 [4/4] Creating docker-compose.yml for local development..."

if [ ! -f "docker-compose.yml" ]; then
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: product-mindset-postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: local_dev_password
      POSTGRES_DB: agentic_app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: product-mindset-redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
EOF
    echo "  ✅ Created docker-compose.yml"
else
    echo "  ✓ docker-compose.yml already exists"
fi

echo ""

# ============================================================================
# Summary
# ============================================================================

echo "======================================"
echo "✅ Quick-Win Improvements Applied!"
echo "======================================"
echo ""
echo "📋 Summary:"
echo "  ✓ Removed unused files and directories"
echo "  ✓ Updated .gitignore"
echo "  ✓ Cleaned Terraform variables"
echo "  ✓ Created docker-compose.yml for local dev"
echo ""
echo "📖 Next Steps:"
echo "  1. Review changes: git status"
echo "  2. Test local development: make dev-setup"
echo "  3. See full recommendations: docs/CODE_REVIEW_AND_IMPROVEMENTS.md"
echo ""
echo "💡 Tip: Run 'git add -A && git status' to see what changed"
echo ""

