# Security Guidelines for Cement AI Backend

## ⚠️ CRITICAL: Credentials Management

### What Should NEVER Be Committed

1. **Environment Files**
   - `.env` files containing actual credentials
   - Any file with `secret`, `key`, `password`, `token` in plain text

2. **Google Cloud Credentials**
   - Service account JSON files (e.g., `service-account.json`)
   - API keys
   - OAuth client secrets

3. **Database Credentials**
   - Connection strings with passwords
   - Database configuration files with credentials

4. **SSL/TLS Certificates**
   - Private keys (`.key`, `.pem` files)
   - Certificate files with sensitive data

### Proper Credential Management

#### 1. Environment Variables
Always use `.env` files for local development:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual credentials
# NEVER commit .env to git
```

#### 2. Google Cloud Credentials
```bash
# Store service account JSON outside the project directory
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Or use gcloud auth for local development
gcloud auth application-default login
```

#### 3. Generate Strong Secrets
```python
# Generate a secure SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Security Checklist Before Committing

- [ ] No `.env` files with actual credentials
- [ ] No hardcoded API keys, passwords, or secrets in code
- [ ] All service account JSON files are in `.gitignore`
- [ ] `__pycache__` and `.pyc` files are excluded
- [ ] Database connection strings use environment variables
- [ ] SECRET_KEY is loaded from environment, not hardcoded

### Production Deployment

For production deployments, use:

1. **Google Secret Manager** (Recommended)
   ```python
   from google.cloud import secretmanager
   
   def access_secret(project_id, secret_id):
       client = secretmanager.SecretManagerServiceClient()
       name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
       response = client.access_secret_version(request={"name": name})
       return response.payload.data.decode("UTF-8")
   ```

2. **Environment Variables in Cloud Run/App Engine**
   - Set via `gcloud run deploy --set-env-vars`
   - Or use `app.yaml` for App Engine (but don't commit with secrets)

3. **Kubernetes Secrets** (for GKE deployments)
   ```bash
   kubectl create secret generic app-secrets \
     --from-literal=DATABASE_URL=postgresql://... \
     --from-literal=SECRET_KEY=...
   ```

### If You Accidentally Committed Secrets

1. **Immediately rotate all exposed credentials**
   - Revoke the API key in Google Cloud Console
   - Generate new keys
   - Update all services using the old credentials

2. **Remove from Git history**
   ```bash
   # Use BFG Repo-Cleaner or git filter-branch
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force push (coordinate with team first)**
   ```bash
   git push origin --force --all
   ```

### Contact for Security Issues

For security concerns or if you discover exposed credentials:
- Email: security@codygon.com
- Immediately notify the development team lead

---

**Remember: Security is everyone's responsibility!**
