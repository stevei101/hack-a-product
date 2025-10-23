#!/bin/bash

set -e

echo "🔧 Terraform Installation Fix"
echo "=============================="
echo ""

# Step 1: Find all terraform binaries
echo "📍 Step 1: Finding all Terraform installations..."
echo "Looking for terraform in PATH:"
which -a terraform || echo "  None found in PATH"

echo ""
echo "Looking in common locations:"
find /usr/local/bin /opt/homebrew/bin -name "terraform" -type f 2>/dev/null || true

echo ""
echo "Checking versions:"
for tf in $(which -a terraform 2>/dev/null); do
    echo "  $tf -> $($tf version -json 2>/dev/null | grep terraform_version || echo 'unknown')"
done

echo ""
read -p "Press Enter to continue to removal..."

# Step 2: Uninstall old Homebrew terraform
echo ""
echo "🗑️  Step 2: Removing old Homebrew terraform..."
brew uninstall terraform 2>/dev/null || echo "  Already uninstalled"

# Step 3: Install from HashiCorp tap
echo ""
echo "📦 Step 3: Installing Terraform from HashiCorp official tap..."
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Step 4: Verify
echo ""
echo "✅ Step 4: Verifying installation..."
echo ""
which terraform
echo ""
terraform version
echo ""

# Check if there are still old versions
OLD_TF=$(find /usr/local/bin -name "terraform" -type f 2>/dev/null || true)
if [ -n "$OLD_TF" ]; then
    echo ""
    echo "⚠️  WARNING: Found old terraform binary at: $OLD_TF"
    echo "You may want to remove it manually:"
    echo "  sudo rm $OLD_TF"
fi

echo ""
echo "🎉 Terraform installation complete!"
echo ""
echo "Current version:"
terraform version | head -1
echo ""
echo "You can now use Terraform locally!"


