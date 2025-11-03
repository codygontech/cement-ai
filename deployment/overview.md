# Deployment Guide

Complete guide for deploying the JK Cement AI Optimization System to production.

---

## Repository Branch Structure

The project uses **separate Git branches** for each component:

- **`frontend`** - Next.js 15 application
- **`backend`** - FastAPI Python backend  
- **`docs`** - Documentation site

Each branch can be deployed independently, allowing for:
- Independent versioning and release cycles
- Separate CI/CD pipelines
- Component-specific deployment strategies
- Better separation of concerns

---

## Deployment Options

### Option 1: Google Cloud Run (Recommended)
- **Best For**: Serverless, auto-scaling applications
- **Pros**: Zero infrastructure management, pay-per-use, auto-scaling
- **Cons**: Cold starts, limited customization

### Option 2: Google Compute Engine
- **Best For**: Full control, consistent workloads
- **Pros**: Full VM control, predictable pricing, no cold starts
- **Cons**: Manual scaling, infrastructure management

### Option 3: Google Kubernetes Engine (GKE)
- **Best For**: Large-scale, complex deployments
- **Pros**: Advanced orchestration, multi-region, flexible
- **Cons**: Complex setup, higher cost, steep learning curve

### Option 4: Traditional VPS/Dedicated Server
- **Best For**: On-premise or non-GCP deployments
- **Pros**: Maximum control, no cloud dependency
- **Cons**: Full infrastructure responsibility

---

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Google Cloud project created
- [ ] APIs enabled
- [ ] Service accounts configured
- [ ] Domain name purchased (if applicable)
- [ ] SSL certificates ready
- [ ] Monitoring configured
- [ ] Backup strategy defined
- [ ] Rollback plan documented

---

## Google Cloud Run Deployment

### 1. Prepare Application

#### Backend Deployment

```bash
# Clone and checkout backend branch
git clone https://github.com/codygontechadmin/cement-ai.git backend-deploy
cd backend-deploy
git checkout backend
```

**Backend Dockerfile** (already exists):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### Frontend Deployment

```bash
# Clone and checkout frontend branch
git clone https://github.com/codygontechadmin/cement-ai.git frontend-deploy
cd frontend-deploy
git checkout frontend
```

**Frontend Dockerfile**:
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000

CMD ["npm", "start"]
```

### 2. Set Up Cloud SQL

```bash
# Create Cloud SQL instance
gcloud sql instances create cement-db \
    --database-version=POSTGRES_14 \
    --tier=db-f1-micro \
    --region=asia-south1 \
    --root-password=YOUR_PASSWORD

# Create database
gcloud sql databases create jk_cement_plant \
    --instance=cement-db

# Create user
gcloud sql users create cement_user \
    --instance=cement-db \
    --password=USER_PASSWORD
```

### 3. Deploy Backend to Cloud Run

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cement-backend ./backend

gcloud run deploy cement-backend \
    --image gcr.io/YOUR_PROJECT_ID/cement-backend \
    --platform managed \
    --region asia-south1 \
    --allow-unauthenticated \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID" \
    --set-env-vars "DATABASE_URL=postgresql+asyncpg://cement_user:PASSWORD@/jk_cement_plant?host=/cloudsql/YOUR_PROJECT_ID:asia-south1:cement-db" \
    --set-env-vars "CORS_ORIGINS=https://your-frontend-url.com" \
    --add-cloudsql-instances YOUR_PROJECT_ID:asia-south1:cement-db \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10
```

### 4. Deploy Frontend to Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cement-frontend .

gcloud run deploy cement-frontend \
    --image gcr.io/YOUR_PROJECT_ID/cement-frontend \
    --platform managed \
    --region asia-south1 \
    --allow-unauthenticated \
    --set-env-vars "NEXT_PUBLIC_API_URL=https://cement-backend-xxx.run.app" \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 5
```

### 5. Configure Custom Domain

```bash
# Map domain to Cloud Run
gcloud run domain-mappings create \
    --service cement-frontend \
    --domain app.yourdomain.com \
    --region asia-south1

gcloud run domain-mappings create \
    --service cement-backend \
    --domain api.yourdomain.com \
    --region asia-south1
```

---

## Compute Engine Deployment

### 1. Create VM Instance

```bash
# Create VM
gcloud compute instances create cement-server \
    --zone=asia-south1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --tags=http-server,https-server

# Configure firewall
gcloud compute firewall-rules create allow-http \
    --allow tcp:80,tcp:443 \
    --target-tags http-server,https-server
```

### 2. Install Dependencies

```bash
# SSH into VM
gcloud compute ssh cement-server --zone=asia-south1-a

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Nginx
sudo apt install nginx -y

# Install Docker (optional)
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

### 3. Deploy Application

```bash
# Clone repository
git clone https://github.com/codygontechadmin/cement-ai.git
cd cement-ai

# Set up backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up frontend
cd ..
npm install
npm run build

# Configure environment
cp backend/.env.example backend/.env
cp .env.example .env.local
# Edit files with production values
```

### 4. Configure Nginx

```nginx
# /etc/nginx/sites-available/cement

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name app.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Enable configuration
sudo ln -s /etc/nginx/sites-available/cement /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Set Up SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificates
sudo certbot --nginx -d api.yourdomain.com -d app.yourdomain.com

# Auto-renewal is automatic, test with:
sudo certbot renew --dry-run
```

### 6. Create Systemd Services

**Backend Service** (`/etc/systemd/system/cement-backend.service`):
```ini
[Unit]
Description=Cement AI Backend
After=network.target postgresql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/cement-ai/backend
Environment="PATH=/home/ubuntu/cement-ai/backend/venv/bin"
ExecStart=/home/ubuntu/cement-ai/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Frontend Service** (`/etc/systemd/system/cement-frontend.service`):
```ini
[Unit]
Description=Cement AI Frontend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/cement-ai
Environment="NODE_ENV=production"
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and Start Services:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable cement-backend cement-frontend
sudo systemctl start cement-backend cement-frontend
sudo systemctl status cement-backend cement-frontend
```

---

## Docker Compose Deployment

### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    environment:
      - GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
      - GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - DATABASE_URL=postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@db:5432/cement
      - CORS_ORIGINS=http://localhost:3000
    volumes:
      - ./credentials.json:/app/credentials.json:ro
    ports:
      - "8000:8000"
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    build: .
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=cement
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

### Deploy with Docker Compose

```bash
# Create .env file
cat > .env << EOF
GOOGLE_CLOUD_PROJECT=your-project
GOOGLE_API_KEY=your-api-key
POSTGRES_PASSWORD=secure-password
EOF

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Database Migration

```bash
# Backup existing data
pg_dump -h localhost -U postgres jk_cement_plant > backup.sql

# Restore to Cloud SQL (via proxy)
./cloud-sql-proxy YOUR_PROJECT:asia-south1:cement-db &
psql -h localhost -U cement_user jk_cement_plant < backup.sql

# Or use gcloud
gcloud sql import sql cement-db gs://your-bucket/backup.sql \
    --database=jk_cement_plant
```

---

## Monitoring & Logging

### Enable Cloud Logging

```python
# backend/app/core/config.py
ENABLE_CLOUD_LOGGING = True
```

### Set Up Monitoring

```bash
# Create uptime check
gcloud monitoring uptime-check-configs create \
    --display-name="Cement Backend" \
    --resource-type=uptime-url \
    --http-check-path=/health \
    --monitored-resource=https://api.yourdomain.com

# Create alert policy
gcloud alpha monitoring policies create \
    --display-name="High Error Rate" \
    --notification-channels=CHANNEL_ID \
    --condition-display-name="Error rate > 5%" \
    --condition-threshold-value=5.0 \
    --condition-threshold-duration=300s
```

### Application Performance Monitoring

```python
# Install APM (optional)
pip install google-cloud-trace

# Add to application
from google.cloud import trace_v2

trace_client = trace_v2.TraceServiceClient()
```

---

## Security Hardening

### 1. Update Environment Variables

```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set in production
export SECRET_KEY="generated-secure-key"
export DEBUG=False
```

### 2. Configure Firewall

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 3. Set Up VPC

```bash
# Create VPC network
gcloud compute networks create cement-vpc \
    --subnet-mode=custom

# Create subnet
gcloud compute networks subnets create cement-subnet \
    --network=cement-vpc \
    --region=asia-south1 \
    --range=10.0.0.0/24
```

### 4. Enable Cloud Armor

```bash
# Create security policy
gcloud compute security-policies create cement-security-policy

# Add rate limiting rule
gcloud compute security-policies rules create 1000 \
    --security-policy cement-security-policy \
    --expression "true" \
    --action "rate-based-ban" \
    --rate-limit-threshold-count 100 \
    --rate-limit-threshold-interval-sec 60 \
    --ban-duration-sec 600
```

---

## Backup Strategy

### Automated Database Backups

```bash
# Enable automatic backups for Cloud SQL
gcloud sql instances patch cement-db \
    --backup-start-time=02:00 \
    --enable-bin-log

# Manual backup
gcloud sql backups create \
    --instance=cement-db \
    --description="Manual backup before update"
```

### Application Backups

```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
gsutil cp -r /app gs://cement-backups/app-$DATE/
pg_dump -h localhost -U postgres jk_cement_plant | \
    gzip | \
    gsutil cp - gs://cement-backups/db-$DATE.sql.gz
```

---

## Rollback Procedures

### Cloud Run Rollback

```bash
# List revisions
gcloud run revisions list --service cement-backend

# Rollback to previous revision
gcloud run services update-traffic cement-backend \
    --to-revisions REVISION_NAME=100
```

### Compute Engine Rollback

```bash
# Keep previous version
mv cement-ai cement-ai.backup
git clone https://github.com/...  # Clone working version
# Restore configuration
cp cement-ai.backup/backend/.env cement-ai/backend/.env
# Restart services
sudo systemctl restart cement-backend cement-frontend
```

---

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_kiln_timestamp ON kiln_operations(timestamp DESC);
CREATE INDEX idx_quality_sample ON quality_metrics(sample_id);

-- Analyze tables
ANALYZE kiln_operations;
ANALYZE quality_metrics;
```

### CDN Configuration

```bash
# Set up Cloud CDN
gcloud compute backend-services create cement-backend-service \
    --global \
    --enable-cdn

gcloud compute backend-services add-backend cement-backend-service \
    --global \
    --instance-group=cement-ig \
    --instance-group-zone=asia-south1-a
```

---

## Post-Deployment Checklist

- [ ] All services running
- [ ] Health checks passing
- [ ] SSL certificates active
- [ ] Database connected
- [ ] Monitoring configured
- [ ] Logs being collected
- [ ] Backups scheduled
- [ ] Domain DNS configured
- [ ] Performance tested
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] Team notified

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u cement-backend -n 50 --no-pager
docker-compose logs backend

# Check ports
sudo netstat -tulpn | grep :8000

# Check environment
printenv | grep GOOGLE
```

### Database Connection Issues

```bash
# Test connection
psql -h localhost -U cement_user -d jk_cement_plant

# Check Cloud SQL Proxy
./cloud-sql-proxy PROJECT:REGION:INSTANCE &
```

### High Memory Usage

```bash
# Check memory
free -h
docker stats

# Optimize configuration
# Reduce workers, limit connections
```

---

## Next Steps

- **[Cost Analysis](./cost-analysis.md)** - Monthly cost breakdown and optimization
- **[Monitoring Guide](./monitoring.md)** - Set up monitoring
- **[Google Cloud Setup](./google-cloud.md)** - Detailed GCP configuration
- **[Security Best Practices](./security.md)** - Security hardening
- **[Scaling Guide](./scaling.md)** - Handle increased load

---

**Last Updated**: November 2025
