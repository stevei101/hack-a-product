# 🔧 Fix Terraform Local Installation

## 🔍 The Problem

You have **two Terraform installations** conflicting:
- **OLD**: v0.12.16 (from 2019) - executing first ❌
- **NEW**: v1.5.7 in Homebrew - not being used ❌

**Required Version**: 1.1.0+ (preferably 1.13.4)

---

## ✅ Quick Fix (Automated)

Run this script to automatically fix everything:

```bash
./scripts/fix-terraform.sh
```

The script will:
1. Find all Terraform installations
2. Remove old Homebrew terraform
3. Install from HashiCorp official tap
4. Verify the installation

---

## 🛠️ Manual Fix (Step by Step)

If you prefer to do it manually:

### Step 1: Find All Terraform Installations

```bash
which -a terraform
```

This shows ALL terraform binaries in your PATH.

### Step 2: Remove Old Homebrew Terraform

```bash
brew uninstall terraform
```

### Step 3: Install from HashiCorp Official Tap

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

### Step 4: Verify Installation

```bash
terraform version
```

You should see: `Terraform v1.13.4` (or similar 1.x version)

### Step 5: Clean Up Old Binaries (if needed)

If `which -a terraform` still shows multiple locations:

```bash
# Find old binaries
find /usr/local/bin -name "terraform" -type f

# Remove them (be careful!)
sudo rm /usr/local/bin/terraform  # Only if this is the old one
```

---

## 🆘 Troubleshooting

### Still showing v0.12.16?

The old binary is earlier in your PATH. Check:

```bash
echo $PATH
```

Find where the old terraform is:

```bash
/usr/bin/which -a terraform
ls -la $(which terraform)
```

Remove the old one:

```bash
sudo rm $(which terraform)
```

Then verify again:

```bash
terraform version
```

### "command not found" after uninstall?

Restart your terminal or reload your shell:

```bash
source ~/.zshrc
# or
source ~/.bash_profile
```

### Multiple versions still showing?

You might have tfenv or asdf managing Terraform. Check:

```bash
which tfenv
which asdf
```

If you have tfenv:

```bash
tfenv install 1.13.4
tfenv use 1.13.4
```

---

## 📊 Version Requirements

| Tool | Minimum Version | Recommended |
|------|----------------|-------------|
| Terraform | 1.1.0 | 1.13.4 |
| Terraform Cloud | N/A | Latest |

---

## ✅ After Fix - Test It!

### Test 1: Version Check
```bash
terraform version
```

Expected output:
```
Terraform v1.13.4
...
```

### Test 2: Login to Terraform Cloud
```bash
cd terraform
terraform login
```

Follow the prompts to authenticate.

### Test 3: Initialize
```bash
terraform init
```

Should connect to Terraform Cloud successfully.

### Test 4: Plan (Destroy)
```bash
terraform plan -destroy
```

Should show what will be destroyed.

---

## 🎯 Why HashiCorp Tap?

Homebrew deprecated the old `terraform` formula because HashiCorp changed to a Business Source License (BUSL).

The official HashiCorp tap (`hashicorp/tap/terraform`) is:
- ✅ Official and maintained by HashiCorp
- ✅ Always up-to-date
- ✅ Supports latest features
- ✅ Required for Terraform Cloud

---

## 📝 Quick Reference Commands

```bash
# Check version
terraform version

# Check where it's installed
which terraform

# Check all installations
which -a terraform

# Uninstall old Homebrew version
brew uninstall terraform

# Install from HashiCorp tap
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Update to latest
brew upgrade hashicorp/tap/terraform

# Login to Terraform Cloud
terraform login

# Initialize (in terraform directory)
cd terraform && terraform init
```

---

## 🚀 Ready to Use

Once fixed, you can:

1. **Destroy locally**:
   ```bash
   cd terraform
   terraform init
   terraform destroy
   ```

2. **Or use the script**:
   ```bash
   ./scripts/destroy-local.sh
   ```

3. **Or use Terraform Cloud UI** (easiest!):
   https://app.terraform.io/app/disposable-org/workspaces/hack-a-product/settings/destruction

---

## 💡 Pro Tips

1. **Always use HashiCorp tap** for Terraform
2. **Don't mix installation methods** (pick one: brew, tfenv, or direct download)
3. **Restart terminal** after installation
4. **Use Terraform Cloud** for state management (already configured!)

---

## ✅ Success Checklist

- [ ] Run `terraform version` shows 1.13.x
- [ ] Run `which terraform` shows `/opt/homebrew/bin/terraform`
- [ ] Run `which -a terraform` shows only ONE location
- [ ] Run `terraform login` works
- [ ] Run `terraform init` in terraform/ directory works
- [ ] No error messages

---

**Need help?** Run the automated script: `./scripts/fix-terraform.sh` 🚀


