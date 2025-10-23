# 🧹 Destroy AWS Infrastructure

You have **3 options** to destroy your AWS infrastructure. Choose the one that works best for you.

---

## ✅ **Option 1: GitHub Actions (Recommended - No Local Setup)**

**Pros:** No local setup needed, uses the workflow we already fixed  
**Cons:** Requires GitHub access

### Steps:
1. Push your latest changes (including the workflow fix):
   ```bash
   git add .
   git commit -m "fix: add TF_API_TOKEN to destroy workflow"
   git push origin develop
   ```

2. Go to: https://github.com/YOUR_USERNAME/hack-a-product/actions/workflows/destroy-development-env.yml

3. Click **"Run workflow"** dropdown (top right)

4. Select branch: **develop**

5. Click **"Run workflow"** button

6. Watch the workflow run and destroy all resources

---

## ✅ **Option 2: Terraform Cloud UI (Easy)**

**Pros:** Visual interface, no command line needed  
**Cons:** Need to navigate to find workspace

### Steps:
1. Go to: https://app.terraform.io/app

2. Login and find your organization (likely "disposable-org")

3. Click on the organization

4. Find workspace: **"hack-a-product"**

5. Click **"Settings"** (in the left sidebar)

6. Scroll to **"Destruction and Deletion"** section

7. Click **"Queue destroy plan"**

8. Review the plan

9. Click **"Confirm & Apply"**

10. Wait for the destroy to complete

**Tip**: If you see "Not Found" error, the organization or workspace name might be different. Check your Terraform Cloud dashboard for the actual names.

---

## ✅ **Option 3: Local Terraform (If You Want Local Control)**

**Pros:** Full control, can see everything locally  
**Cons:** Requires local Terraform setup

### Quick Method (Use the Script):
```bash
./scripts/destroy-local.sh
```

The script will:
- Install Terraform if needed
- Log you into Terraform Cloud
- Initialize Terraform
- Create and show a destroy plan
- Ask for confirmation
- Destroy all resources

### Manual Method:
```bash
cd terraform

# Login to Terraform Cloud
terraform login

# Initialize
terraform init

# Preview what will be destroyed
terraform plan -destroy

# Destroy (will ask for confirmation)
terraform destroy
```

---

## 📊 **What Gets Destroyed:**

All of these methods will destroy:
- ✅ S3 bucket (static website)
- ✅ CloudFront distribution
- ✅ ECR repositories (frontend & backend)
- ✅ EKS cluster
- ✅ VPC and networking
- ✅ IAM roles and policies
- ✅ All related AWS resources

---

## ⚠️ **Important Notes:**

1. **Backup First**: If you have any important data in S3 or container images in ECR, back them up first!

2. **Cost Savings**: Destroying the infrastructure will stop all AWS charges.

3. **Re-provision Later**: You can always re-provision by:
   - Pushing to `develop` branch (triggers deploy workflow)
   - Running `terraform apply` locally
   - Running apply in Terraform Cloud UI

4. **State Remains**: Your Terraform state stays in Terraform Cloud, so you can re-provision with the same configuration.

---

## 🎯 **My Recommendation:**

Use **Option 2 (Terraform Cloud UI)** - it's the simplest and most reliable!

Just visit: https://app.terraform.io/app/disposable-org/workspaces/hack-a-product/settings/destruction

---

## 🆘 **Troubleshooting:**

### "Terraform login failed"
Get a token manually:
1. Go to: https://app.terraform.io/app/settings/tokens
2. Generate a new token
3. Save it to `~/.terraform.d/credentials.tfrc.json`:
   ```json
   {
     "credentials": {
       "app.terraform.io": {
         "token": "YOUR_TOKEN_HERE"
       }
     }
   }
   ```

### "Permission denied" on destroy
Make sure your AWS credentials are set up (only needed for local destroy):
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
```

But honestly, just use **Terraform Cloud UI** to avoid all this! 😊

