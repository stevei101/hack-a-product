#!/bin/bash
# Script to test EKS deployments locally

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
REGION="us-east-1"
CLUSTER_NAME="product-mindset-dev"
NAMESPACE="dev"
ECR_REGISTRY="874834750693.dkr.ecr.us-east-1.amazonaws.com"

echo -e "${GREEN}=== EKS Local Testing Script ===${NC}\n"

# Function to print section headers
print_header() {
    echo -e "\n${YELLOW}>>> $1${NC}\n"
}

# Step 1: Check AWS credentials
print_header "Step 1: Checking AWS credentials"
aws sts get-caller-identity

# Step 2: Configure kubectl
print_header "Step 2: Configuring kubectl for EKS"
aws eks update-kubeconfig --region $REGION --name $CLUSTER_NAME
echo -e "${GREEN}✓ kubectl configured${NC}"

# Step 3: Verify cluster connection
print_header "Step 3: Verifying cluster connection"
kubectl cluster-info
echo ""
kubectl get nodes

# Step 4: Check namespace
print_header "Step 4: Checking namespace"
kubectl get namespace $NAMESPACE || kubectl create namespace $NAMESPACE

# Step 5: View current deployments
print_header "Step 5: Current deployments in $NAMESPACE"
kubectl get all -n $NAMESPACE

# Step 6: List Helm releases
print_header "Step 6: Helm releases"
helm list -n $NAMESPACE

# Step 7: Show pod status
print_header "Step 7: Pod status"
kubectl get pods -n $NAMESPACE -o wide

# Step 8: Show recent events
print_header "Step 8: Recent events"
kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' | tail -20

echo -e "\n${GREEN}=== Testing complete ===${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Deploy frontend: helm upgrade --install frontend ./charts/frontend -n $NAMESPACE --set image.repository=$ECR_REGISTRY/smithveunsa/react-bun-k8s-frontend --set image.tag=latest"
echo "2. Deploy backend:  helm upgrade --install backend ./charts/backend -n $NAMESPACE --set image.repository=$ECR_REGISTRY/smithveunsa/react-bun-k8s-backend --set image.tag=latest"
echo "3. Port forward:    kubectl port-forward -n $NAMESPACE deployment/frontend 8080:80"
echo "4. View logs:       kubectl logs -n $NAMESPACE deployment/frontend --tail=50"

