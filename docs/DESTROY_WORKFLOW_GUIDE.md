# 🧹 Destroy Workflow Guide

## What You'll See When Running the Destroy Workflow

---

## 📋 **Step 1: Workflow Trigger**

When you manually trigger the workflow, GitHub Actions will:
1. Checkout the code
2. Setup Terraform
3. Configure AWS credentials
4. Initialize Terraform

---

## 📊 **Step 2: Destroy Plan Summary** 

You'll see a detailed summary showing:

### Resources to be Destroyed:

| Resource Type | Count |
|--------------|-------|
| S3 Buckets | 1 |
| CloudFront Distributions | 1 |
| ECR Repositories | 2 |
| EKS Cluster | 1 |
| VPC & Networking | Multiple |
| IAM Roles & Policies | Multiple |

### ⚠️ This action will:
- ✅ Delete the S3 static website bucket
- ✅ Delete the CloudFront distribution
- ✅ Delete frontend and backend ECR repositories
- ✅ Delete the EKS cluster and all workloads
- ✅ Delete the VPC, subnets, and networking components
- ✅ Delete IAM roles and policies

### 💰 Cost Impact:
- Monthly savings: ~$100-150/month (EKS cluster)
- All AWS resources will be removed

---

## 🔍 **Step 3: Detailed Resource List**

The workflow will show you each resource that will be destroyed:

```
📋 RESOURCES THAT WILL BE DESTROYED:
====================================

  # aws_s3_bucket.site will be destroyed
  # aws_cloudfront_distribution.s3_distribution will be destroyed
  # aws_ecr_repository.frontend will be destroyed
  # aws_ecr_repository.backend will be destroyed
  # aws_eks_cluster.eks_cluster will be destroyed
  # aws_vpc.eks_vpc will be destroyed
  ...

📊 Summary:
Plan: 0 to add, 0 to change, 25 to destroy.
```

---

## ⏱️ **Step 4: 5-Second Countdown**

Before destroying, you'll see:
```
💥 Destroying infrastructure in 5 seconds...
```

This gives you a final moment to cancel if needed (Ctrl+C in the Actions UI).

---

## 🗑️ **Step 5: Destruction in Progress**

Terraform will destroy resources in reverse dependency order:
1. EKS workloads and node groups
2. EKS cluster
3. CloudFront distribution
4. S3 bucket (after emptying)
5. ECR repositories
6. Networking (subnets, route tables)
7. VPC
8. IAM roles and policies

---

## ✅ **Step 6: Completion Confirmation**

You'll see:

```
✅ Infrastructure Destroyed Successfully!

All AWS resources have been removed.

Next Steps:
1. Verify in AWS Console that resources are gone
2. Check Terraform Cloud state is clean
3. To re-provision: push to develop branch
```

---

## 🎯 **How to Run the Workflow**

### Option 1: Via GitHub UI
1. Go to: https://github.com/YOUR_USERNAME/hack-a-product/actions/workflows/destroy-development-env.yml
2. Click **"Run workflow"**
3. Select branch: **develop**
4. Click **"Run workflow"** button
5. Watch the workflow execute

### Option 2: Via GitHub CLI
```bash
gh workflow run destroy-development-env.yml --ref develop
```

---

## 🛡️ **Safety Features**

1. **Manual Trigger Only**: Workflow only runs when you manually trigger it
2. **Branch Protection**: Only works on `develop` branch
3. **Plan Review**: Shows exactly what will be destroyed before destroying
4. **Summary**: Creates a GitHub Actions summary for audit trail
5. **5-Second Delay**: Gives you time to cancel if you triggered by mistake

---

## 📝 **After Destruction**

### What Stays:
- ✅ GitHub repository and code
- ✅ Terraform Cloud state (empty but preserved)
- ✅ GitHub Actions secrets
- ✅ Container images in local registry (if any)

### What's Gone:
- ❌ All AWS resources
- ❌ S3 bucket and static website
- ❌ CloudFront distribution
- ❌ ECR repositories and images
- ❌ EKS cluster and all deployments
- ❌ VPC and networking

---

## 🔄 **To Re-provision Later**

Just push to the `develop` branch:
```bash
git push origin develop
```

The deploy workflow will recreate everything automatically!

---

## 🆘 **Troubleshooting**

### Workflow fails with "TF_API_TOKEN not found"
- Verify the secret is set: Settings → Secrets → Actions → TF_API_TOKEN

### Workflow fails with "Access Denied"
- Check AWS_ACCOUNT_ID secret is correct
- Verify IAM role trust relationship is set up

### Some resources fail to delete
- CloudFront distribution takes 15-20 minutes to delete
- S3 bucket must be empty first (workflow handles this)
- EKS node groups must drain before cluster deletion

If deletion fails, you can:
1. Re-run the workflow
2. Use Terraform Cloud UI to destroy
3. Manually delete stuck resources in AWS Console

---

## 💡 **Pro Tips**

1. **Check Costs First**: Go to AWS Cost Explorer to see what you're spending
2. **Backup Data**: If you have anything important in S3, download it first
3. **Export Images**: If you want to keep container images, pull them from ECR first
4. **State Backup**: Terraform Cloud keeps your state, so you can always re-provision
5. **Watch the Logs**: GitHub Actions logs show exactly what's happening

---

## 📊 **Estimated Destruction Time**

| Resource | Time |
|----------|------|
| S3 Bucket | 1-2 min |
| CloudFront | 15-20 min |
| ECR Repos | 1 min |
| EKS Cluster | 10-15 min |
| VPC/Networking | 2-3 min |
| **Total** | **~30-40 min** |

The workflow will wait for everything to complete.

---

## ✅ **You're All Set!**

The destroy workflow is now enhanced with:
- ✅ Clear resource listing
- ✅ Cost impact summary
- ✅ Detailed confirmation
- ✅ Safety countdown
- ✅ Completion verification

**Happy destroying!** 🧹 (and easy re-provisioning later! 🚀)

