# 🔒 Security Audit & Plan for Public Repository

**Repository:** hack-a-product  
**Visibility:** PUBLIC  
**Audit Date:** October 22, 2025  
**Status:** ✅ MOSTLY SECURE (needs improvements)

---

## 📊 Current Security Status

### ✅ What's Already Secure

1. **Environment Files Protected**
   - ✅ `.env*` files in `.gitignore`
   - ✅ `terraform.tfvars` not committed
   - ✅ `.venv/` directories ignored
   - ✅ Only `.example` files committed
   - ✅ No `.tfstate` files in repo

2. **Secrets Management**
   - ✅ GitHub Actions using `${{ secrets.* }}`
   - ✅ AWS OIDC (no hardcoded AWS keys)
   - ✅ Terraform Cloud token in GitHub Secrets
   - ✅ No hardcoded credentials in source code

3. **Git History**
   - ✅ No `.env` files ever committed
   - ✅ No credential files in history

---

## ⚠️ Security Improvements Needed

### 1. **Weak Example Credentials** (Priority: MEDIUM)

**Issue:** `setup_env.sh` contains weak example password

**File:** `setup_env.sh:66`
```bash
POSTGRES_PASSWORD=dev_password_123  # ⚠️ Too weak even for dev
```

**Fix:**
```bash
# Generate secure random password
POSTGRES_PASSWORD=$(openssl rand -base64 24)
```

### 2. **Missing Secret Scanning** (Priority: HIGH)

**Issue:** No automated secret detection

**Install git-secrets:**
```bash
# macOS
brew install git-secrets

# Initialize
git secrets --install
git secrets --register-aws
git secrets --add 'password\s*=\s*.+'
git secrets --add 'api[_-]?key\s*=\s*.+'
git secrets --add '(AWS|NVIDIA|NIM).*[A-Za-z0-9]{20,}'
```

### 3. **No Pre-commit Hooks** (Priority: HIGH)

**Issue:** No automatic checks before commits

**Install:**
```bash
pip install pre-commit
```

**Create:** `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: detect-private-key
      - id: check-yaml
      - id: check-json
      - id: end-of-file-fixer
      - id: trailing-whitespace
      
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package(-lock)?.json|bun.lock
        
  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

**Setup:**
```bash
pre-commit install
pre-commit run --all-files  # Initial scan
```

### 4. **Missing .env.example for Frontend** (Priority: LOW)

**Create:** `.env.example`
```bash
# Frontend Environment Variables (PUBLIC - safe to commit)
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Product Mindset
VITE_ENV=development
```

---

## 🚨 CRITICAL: Files to NEVER Commit

### Add to .gitignore (already there, but verify):
```gitignore
# Secrets
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
secrets.yml
secrets.yaml

# Terraform
terraform.tfvars
*.tfstate
*.tfstate.*
.terraform/

# AWS
.aws/
credentials

# Python
.venv/
venv/
*.pyc
__pycache__/

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
```

---

## 🔍 Sensitive Data Patterns to Watch

### AWS Credentials
```bash
# BAD - Never commit these patterns:
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
aws_access_key_id = AKIA...
```

### API Keys
```bash
# BAD - Never commit:
NIM_API_KEY=nvapi-...
NVIDIA_API_KEY=...
api_key: "sk-..."
token = "ghp_..."
```

### Passwords
```bash
# BAD - Never commit:
POSTGRES_PASSWORD=...
DB_PASSWORD=...
password=actual_password
```

---

## 🛡️ Security Scanning Tools

### 1. **Gitleaks** (Scan for secrets)
```bash
# Install
brew install gitleaks

# Scan repo
gitleaks detect --source . --verbose

# Scan history
gitleaks protect --source . --verbose
```

### 2. **TruffleHog** (Deep history scan)
```bash
# Install
brew install trufflesecurity/trufflehog/trufflehog

# Scan
trufflehog git file://. --only-verified
```

### 3. **detect-secrets** (Python-based)
```bash
# Install
pip install detect-secrets

# Create baseline
detect-secrets scan > .secrets.baseline

# Check for new secrets
detect-secrets scan --baseline .secrets.baseline
```

---

## ✅ Security Checklist

### Before EVERY Commit:
- [ ] Run `git diff` and review changes
- [ ] No `.env` files
- [ ] No `terraform.tfvars`
- [ ] No API keys in code
- [ ] No passwords in config
- [ ] No AWS credentials
- [ ] No private keys (.pem, .key)

### Monthly:
- [ ] Rotate API keys
- [ ] Review GitHub Secrets
- [ ] Update dependencies
- [ ] Scan with gitleaks
- [ ] Review access logs

### Before Making Repo Public:
- [ ] Scan entire history with gitleaks
- [ ] Review all `.example` files
- [ ] Check GitHub Secrets are set
- [ ] Verify .gitignore coverage
- [ ] Remove any hardcoded values
- [ ] Audit all documentation

---

## 🔧 Quick Fixes (Do Now!)

### 1. Update .gitignore (add these)
```bash
cat >> .gitignore << 'EOF'

# Additional security patterns
**/secrets/
**/credentials/
**/.credentials/
*.backup
*.bak
.env.backup
.env.bak
.secrets
terraform.tfstate.d/
.terraform.lock.hcl
EOF
```

### 2. Install Security Tools
```bash
# Install pre-commit hooks
pip install pre-commit detect-secrets

# Install git-secrets
brew install git-secrets gitleaks

# Setup
git secrets --install
pre-commit install
```

### 3. Create Security Policy
**Create:** `SECURITY.md`
```markdown
# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please email: 
security@yourproject.com

Do NOT create a public GitHub issue.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| develop | :white_check_mark: |
| main    | :white_check_mark: |

## Security Measures

- All secrets managed via GitHub Secrets
- AWS access via OIDC (no long-term credentials)
- Pre-commit hooks scan for secrets
- Dependencies scanned with Dependabot
```

### 4. Enable GitHub Security Features

**Go to:** `Settings → Security → Code security and analysis`

Enable:
- ✅ Dependency graph
- ✅ Dependabot alerts
- ✅ Dependabot security updates
- ✅ Secret scanning
- ✅ Push protection

---

## 📝 Safe Documentation Practices

### ✅ DO:
```markdown
# Safe examples
NIM_API_KEY=your_nvidia_api_key_here
AWS_ACCESS_KEY_ID=AKIA<redacted>
password=<your-secure-password>
```

### ❌ DON'T:
```markdown
# Never include real values
NIM_API_KEY=nvapi-abc123real456key789
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
password=MyRealPassword123
```

---

## 🚀 GitHub Actions Security

### Current Status: ✅ SECURE

Your workflows properly use:
- `${{ secrets.AWS_ROLE_ARN }}`
- `${{ secrets.TF_API_TOKEN }}`
- `${{ secrets.NIM_API_KEY }}`
- `${{ secrets.POSTGRES_PASSWORD }}`

### Best Practices:
1. ✅ Never echo secrets
2. ✅ Use environment-specific secrets
3. ✅ Rotate tokens quarterly
4. ✅ Use OIDC instead of long-term credentials
5. ✅ Limit secret access to specific branches

---

## 🎯 Action Plan (Priority Order)

### High Priority (Do Today)
1. ✅ Install pre-commit hooks
2. ✅ Run gitleaks scan
3. ✅ Enable GitHub secret scanning
4. ✅ Fix weak password in setup_env.sh

### Medium Priority (This Week)
5. Create SECURITY.md
6. Add .env.example for frontend
7. Document secret rotation policy
8. Train team on security practices

### Low Priority (This Month)
9. Setup automated security scans in CI
10. Create security incident response plan
11. Regular security audits
12. Dependency vulnerability scanning

---

## 📞 Emergency Response

### If Secrets Are Exposed:

**Immediate Actions:**
1. **STOP** - Don't commit anything else
2. **Rotate** all exposed credentials immediately
3. **Revoke** the exposed secrets
4. **Scan** git history: `gitleaks detect --source . --log-level=debug`
5. **Remove** from history (if needed):
   ```bash
   # Use BFG Repo Cleaner (safer than git filter-branch)
   brew install bfg
   bfg --delete-files .env
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   ```
6. **Force push** (coordinate with team!)
7. **Notify** affected services
8. **Update** documentation

---

## 📚 Resources

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Git-secrets](https://github.com/awslabs/git-secrets)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [Pre-commit](https://pre-commit.com/)

---

## ✅ Summary

**Current Status:** Your repo is **mostly secure** for public use.

**Required Actions:**
1. Install pre-commit hooks (5 min)
2. Run security scan (2 min)
3. Enable GitHub features (3 min)
4. Fix weak passwords (2 min)

**Total Time:** ~15 minutes to production-ready security!

---

**Last Updated:** October 22, 2025  
**Next Audit:** November 22, 2025

