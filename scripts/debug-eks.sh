#!/bin/bash
# Script to debug EKS deployments

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE="dev"

echo -e "${GREEN}=== EKS Debugging Tool ===${NC}\n"

# Function to check pod status
check_pods() {
    echo -e "${YELLOW}>>> Pod Status${NC}\n"
    kubectl get pods -n $NAMESPACE -o wide
    
    echo -e "\n${YELLOW}>>> Pod Issues${NC}"
    kubectl get pods -n $NAMESPACE | grep -v "Running\|Completed" || echo "All pods are running!"
}

# Function to show pod logs
show_logs() {
    echo -e "\n${YELLOW}>>> Available Pods${NC}\n"
    kubectl get pods -n $NAMESPACE -o name
    
    echo -e "\n${BLUE}Enter pod name (or deployment name like 'frontend'):${NC}"
    read -p "> " pod_name
    
    if [[ $pod_name == deployment/* ]]; then
        kubectl logs -n $NAMESPACE $pod_name --tail=100 -f
    else
        kubectl logs -n $NAMESPACE pod/$pod_name --tail=100 -f
    fi
}

# Function to describe pod
describe_pod() {
    echo -e "\n${YELLOW}>>> Available Pods${NC}\n"
    kubectl get pods -n $NAMESPACE
    
    echo -e "\n${BLUE}Enter pod name:${NC}"
    read -p "> " pod_name
    
    kubectl describe pod -n $NAMESPACE $pod_name
}

# Function to check events
check_events() {
    echo -e "${YELLOW}>>> Recent Events${NC}\n"
    kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' | tail -30
}

# Function to check deployments
check_deployments() {
    echo -e "${YELLOW}>>> Deployments${NC}\n"
    kubectl get deployments -n $NAMESPACE
    
    echo -e "\n${YELLOW}>>> Deployment Details${NC}"
    for deploy in $(kubectl get deployments -n $NAMESPACE -o name); do
        echo -e "\n${BLUE}$deploy${NC}"
        kubectl rollout status -n $NAMESPACE $deploy --timeout=5s || true
    done
}

# Function to check services
check_services() {
    echo -e "${YELLOW}>>> Services${NC}\n"
    kubectl get svc -n $NAMESPACE
    
    echo -e "\n${YELLOW}>>> Service Endpoints${NC}"
    kubectl get endpoints -n $NAMESPACE
}

# Function to shell into pod
exec_pod() {
    echo -e "\n${YELLOW}>>> Running Pods${NC}\n"
    kubectl get pods -n $NAMESPACE | grep Running
    
    echo -e "\n${BLUE}Enter pod name:${NC}"
    read -p "> " pod_name
    
    echo -e "${YELLOW}Opening shell in $pod_name...${NC}"
    kubectl exec -it -n $NAMESPACE $pod_name -- /bin/sh || \
    kubectl exec -it -n $NAMESPACE $pod_name -- /bin/bash
}

# Function to restart deployment
restart_deployment() {
    echo -e "\n${YELLOW}>>> Deployments${NC}\n"
    kubectl get deployments -n $NAMESPACE
    
    echo -e "\n${BLUE}Enter deployment name to restart:${NC}"
    read -p "> " deploy_name
    
    echo -e "${YELLOW}Restarting $deploy_name...${NC}"
    kubectl rollout restart -n $NAMESPACE deployment/$deploy_name
    kubectl rollout status -n $NAMESPACE deployment/$deploy_name
}

# Main menu
while true; do
    echo -e "\n${GREEN}=== Debug Menu ===${NC}"
    echo "1) Check pod status"
    echo "2) View pod logs"
    echo "3) Describe pod (detailed info)"
    echo "4) Check recent events"
    echo "5) Check deployments"
    echo "6) Check services"
    echo "7) Shell into pod"
    echo "8) Restart deployment"
    echo "9) Run all checks"
    echo "0) Exit"
    
    read -p "Enter choice (0-9): " choice
    
    case $choice in
        1) check_pods ;;
        2) show_logs ;;
        3) describe_pod ;;
        4) check_events ;;
        5) check_deployments ;;
        6) check_services ;;
        7) exec_pod ;;
        8) restart_deployment ;;
        9)
            check_pods
            check_deployments
            check_services
            check_events
            ;;
        0)
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
done

