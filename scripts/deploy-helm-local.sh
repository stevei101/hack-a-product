#!/bin/bash
# Script to deploy Helm charts locally to EKS

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
REGION="us-east-1"
NAMESPACE="dev"
ECR_REGISTRY="874834750693.dkr.ecr.us-east-1.amazonaws.com"
IMAGE_TAG="${1:-latest}"  # Use first argument or default to 'latest'

echo -e "${GREEN}=== Helm Deployment Script ===${NC}"
echo -e "Image tag: ${YELLOW}$IMAGE_TAG${NC}\n"

# Function to deploy frontend
deploy_frontend() {
    echo -e "${YELLOW}>>> Deploying Frontend${NC}\n"
    
    helm upgrade --install frontend ./charts/frontend \
        --namespace $NAMESPACE \
        --create-namespace \
        --set image.repository=$ECR_REGISTRY/smithveunsa/react-bun-k8s-frontend \
        --set image.tag=$IMAGE_TAG \
        --wait \
        --timeout 5m
    
    echo -e "${GREEN}✓ Frontend deployed${NC}"
}

# Function to deploy backend
deploy_backend() {
    echo -e "${YELLOW}>>> Deploying Backend${NC}\n"
    
    # Prompt for secrets if not set
    if [ -z "$NIM_API_KEY" ]; then
        read -p "Enter NIM_API_KEY (or press enter to use default): " NIM_API_KEY
        NIM_API_KEY=${NIM_API_KEY:-"changeme-nvidia-api-key"}
    fi
    
    if [ -z "$POSTGRES_PASSWORD" ]; then
        read -sp "Enter POSTGRES_PASSWORD (or press enter to use default): " POSTGRES_PASSWORD
        echo
        POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-"changeme-secure-password"}
    fi
    
    helm upgrade --install backend ./charts/backend \
        --namespace $NAMESPACE \
        --create-namespace \
        --set image.repository=$ECR_REGISTRY/smithveunsa/react-bun-k8s-backend \
        --set image.tag=$IMAGE_TAG \
        --set env.NIM_API_KEY="$NIM_API_KEY" \
        --set env.POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
        --wait \
        --timeout 5m
    
    echo -e "${GREEN}✓ Backend deployed${NC}"
}

# Function to show deployment status
show_status() {
    echo -e "\n${YELLOW}>>> Deployment Status${NC}\n"
    
    echo "Helm Releases:"
    helm list -n $NAMESPACE
    
    echo -e "\nPods:"
    kubectl get pods -n $NAMESPACE
    
    echo -e "\nServices:"
    kubectl get svc -n $NAMESPACE
}

# Main menu
echo "What would you like to deploy?"
echo "1) Frontend only"
echo "2) Backend only"
echo "3) Both (frontend + backend)"
echo "4) Show status only"
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        deploy_frontend
        ;;
    2)
        deploy_backend
        ;;
    3)
        deploy_frontend
        deploy_backend
        ;;
    4)
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

show_status

echo -e "\n${GREEN}=== Deployment Complete ===${NC}"
echo -e "\n${YELLOW}Access your applications:${NC}"
echo "Frontend: kubectl port-forward -n $NAMESPACE deployment/frontend 8080:80"
echo "Backend:  kubectl port-forward -n $NAMESPACE deployment/backend 8000:8000"
echo -e "\n${YELLOW}View logs:${NC}"
echo "kubectl logs -n $NAMESPACE -f deployment/frontend"
echo "kubectl logs -n $NAMESPACE -f deployment/backend"

