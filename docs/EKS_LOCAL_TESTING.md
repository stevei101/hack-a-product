# Testing Helm Deployments Locally with AWS EKS

This guide explains how to test your Helm charts against the AWS EKS cluster from your local machine.

## Prerequisites

- ✅ kubectl (v1.34.1 or higher)
- ✅ helm (v3.19.0 or higher)
- ✅ aws CLI (v2.31.17 or higher)
- ✅ AWS credentials configured
- ✅ EKS cluster running in AWS

## Quick Start

### 1. Configure kubectl

```bash
aws eks update-kubeconfig --region us-east-1 --name product-mindset-dev
```

### 2. Verify connection

```bash
kubectl cluster-info
kubectl get nodes
```

### 3. Use helper scripts

We've created three helper scripts to make testing easier:

#### **Test EKS Connection**
```bash
./scripts/test-eks-local.sh
```

This script will:
- Verify AWS credentials
- Configure kubectl
- Show cluster status
- List current deployments

#### **Deploy Charts**
```bash
./scripts/deploy-helm-local.sh
```

Interactive menu to:
- Deploy frontend only
- Deploy backend only
- Deploy both
- Show status

#### **Debug Issues**
```bash
./scripts/debug-eks.sh
```

Interactive debugging tool with:
- Pod status checks
- Log viewing
- Event inspection
- Shell access to pods
- Deployment restarts

## Manual Testing Steps

### Step 1: Configure kubectl

```bash
# Update kubeconfig
aws eks update-kubeconfig --region us-east-1 --name product-mindset-dev

# Verify
kubectl config current-context
kubectl cluster-info
```

### Step 2: Check current state

```bash
# View all resources in dev namespace
kubectl get all -n dev

# List Helm releases
helm list -n dev

# Check pods
kubectl get pods -n dev -o wide
```

### Step 3: Test chart rendering (dry run)

```bash
# Test frontend chart
helm template test-frontend ./charts/frontend \
  --namespace dev \
  --set image.tag=latest

# Test backend chart
helm template test-backend ./charts/backend \
  --namespace dev \
  --set image.tag=latest
```

### Step 4: Deploy charts

#### Deploy Frontend

```bash
helm upgrade --install frontend ./charts/frontend \
  --namespace dev \
  --create-namespace \
  --set image.repository=874834750693.dkr.ecr.us-east-1.amazonaws.com/smithveunsa/react-bun-k8s-frontend \
  --set image.tag=latest \
  --wait \
  --debug
```

#### Deploy Backend

```bash
helm upgrade --install backend ./charts/backend \
  --namespace dev \
  --create-namespace \
  --set image.repository=874834750693.dkr.ecr.us-east-1.amazonaws.com/smithveunsa/react-bun-k8s-backend \
  --set image.tag=latest \
  --set env.NIM_API_KEY="your-nvidia-api-key" \
  --set env.POSTGRES_PASSWORD="your-secure-password" \
  --wait \
  --debug
```

### Step 5: Verify deployment

```bash
# Watch pods start
kubectl get pods -n dev -w

# Check deployment status
kubectl rollout status deployment/frontend -n dev
kubectl rollout status deployment/backend -n dev

# View logs
kubectl logs -n dev deployment/frontend --tail=50
kubectl logs -n dev deployment/backend --tail=50
```

### Step 6: Access applications

#### Port Forward

```bash
# Frontend (then visit http://localhost:8080)
kubectl port-forward -n dev deployment/frontend 8080:80

# Backend (then visit http://localhost:8000/docs)
kubectl port-forward -n dev deployment/backend 8000:8000
```

## Common Commands

### Helm Operations

```bash
# List releases
helm list -n dev

# Get release status
helm status frontend -n dev

# Get release history
helm history frontend -n dev

# View values
helm get values frontend -n dev

# Upgrade release
helm upgrade frontend ./charts/frontend -n dev --reuse-values

# Rollback
helm rollback frontend 1 -n dev

# Uninstall
helm uninstall frontend -n dev
```

### kubectl Operations

```bash
# Get resources
kubectl get pods -n dev
kubectl get deployments -n dev
kubectl get services -n dev
kubectl get ingress -n dev

# Describe (detailed info)
kubectl describe pod <pod-name> -n dev
kubectl describe deployment frontend -n dev

# Logs
kubectl logs <pod-name> -n dev
kubectl logs -f deployment/frontend -n dev  # Follow logs
kubectl logs <pod-name> -n dev --previous   # Previous container

# Events
kubectl get events -n dev --sort-by='.lastTimestamp'

# Shell into pod
kubectl exec -it <pod-name> -n dev -- /bin/sh

# Restart deployment
kubectl rollout restart deployment/frontend -n dev

# Scale deployment
kubectl scale deployment/frontend --replicas=3 -n dev
```

## Debugging Tips

### Pod won't start (ImagePullBackOff)

```bash
# Check pod events
kubectl describe pod <pod-name> -n dev

# Verify ECR access
aws ecr get-login-password --region us-east-1

# Check image exists
aws ecr describe-images \
  --repository-name smithveunsa/react-bun-k8s-frontend \
  --region us-east-1
```

### Pod crashes (CrashLoopBackOff)

```bash
# View logs
kubectl logs <pod-name> -n dev
kubectl logs <pod-name> -n dev --previous

# Check events
kubectl describe pod <pod-name> -n dev

# Verify environment variables
kubectl exec <pod-name> -n dev -- env
```

### Can't connect to cluster

```bash
# Verify AWS credentials
aws sts get-caller-identity

# Update kubeconfig
aws eks update-kubeconfig --region us-east-1 --name product-mindset-dev

# Test connection
kubectl cluster-info
kubectl auth can-i get pods -n dev
```

### Helm template errors

```bash
# Lint chart
helm lint ./charts/backend

# Render templates
helm template test ./charts/backend --debug

# Dry run
helm install test ./charts/backend --dry-run --debug -n dev
```

## Environment Variables

Set these for easier commands:

```bash
export AWS_REGION=us-east-1
export EKS_CLUSTER=product-mindset-dev
export K8S_NAMESPACE=dev
export ECR_REGISTRY=874834750693.dkr.ecr.us-east-1.amazonaws.com
```

Then use:
```bash
kubectl get pods -n $K8S_NAMESPACE
helm list -n $K8S_NAMESPACE
```

## Cleanup

### Remove deployments

```bash
# Uninstall Helm releases
helm uninstall frontend -n dev
helm uninstall backend -n dev

# Delete namespace (removes everything)
kubectl delete namespace dev
```

### Reset kubeconfig

```bash
# Remove EKS cluster from kubeconfig
kubectl config delete-context arn:aws:eks:us-east-1:874834750693:cluster/product-mindset-dev
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `error: You must be logged in to the server` | Run `aws eks update-kubeconfig...` |
| `ImagePullBackOff` | Check ECR permissions and image exists |
| `CrashLoopBackOff` | Check application logs with `kubectl logs` |
| `Pending` pods | Check node resources with `kubectl get nodes` |
| Helm template errors | Run `helm lint` and check _helpers.tpl |

## Next Steps

After successful local testing:
1. Commit changes to git
2. Push to `develop` branch
3. GitHub Actions will deploy automatically
4. Monitor deployment in Actions tab

## Useful Links

- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Helm Documentation](https://helm.sh/docs/)
- [AWS EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)

