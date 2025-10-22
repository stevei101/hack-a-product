#!/bin/bash

set -e

echo "🧹 Terraform Local Destroy Script"
echo "=================================="
echo ""

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not found. Installing..."
    brew tap hashicorp/tap
    brew install hashicorp/tap/terraform
fi

# Check Terraform version
echo "📦 Terraform version:"
terraform version
echo ""

# Navigate to terraform directory
cd "$(dirname "$0")/../terraform"

echo "🔐 Logging in to Terraform Cloud..."
echo "You'll need to generate a token at: https://app.terraform.io/app/settings/tokens"
echo ""
terraform login

echo ""
echo "🔧 Initializing Terraform..."
terraform init

echo ""
echo "📋 Creating destroy plan..."
terraform plan -destroy -out=destroy.tfplan

echo ""
echo "⚠️  WARNING: This will DESTROY all AWS resources!"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" == "yes" ]; then
    echo ""
    echo "💥 Destroying infrastructure..."
    terraform apply destroy.tfplan
    rm -f destroy.tfplan
    echo ""
    echo "✅ Infrastructure destroyed successfully!"
else
    echo "❌ Destroy cancelled."
    rm -f destroy.tfplan
    exit 1
fi

