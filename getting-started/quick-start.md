# Quick Start Guide

Get the JK Cement AI Optimization System running in under 15 minutes.

---

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Node.js 18+** installed ([Download](https://nodejs.org/))
- [ ] **Python 3.11+** installed ([Download](https://www.python.org/))
- [ ] **PostgreSQL 14+** installed ([Download](https://www.postgresql.org/))
- [ ] **Google Cloud Account** with billing enabled
- [ ] **Git** installed
- [ ] **Code editor** (VS Code recommended)

---

## Step 1: Clone the Repository

The project is organized into three separate branches:
- **`frontend`** - Next.js 15 application
- **`backend`** - FastAPI Python backend
- **`docs`** - Documentation (this site)

```bash
# Clone the repository
git clone https://github.com/codygontechadmin/cement-ai.git
cd cement-ai

# For frontend development
git checkout frontend

# For backend development
git checkout backend

# For documentation updates
git checkout docs
```

> **Note**: Each branch contains its respective codebase. Check out the appropriate branch for your work.

---

## Step 2: Set Up Google Cloud

### 2.1 Enable Required APIs

```bash
gcloud services enable \
  aiplatform.googleapis.com \
  sqladmin.googleapis.com \
  storage-api.googleapis.com \
  vision.googleapis.com \
  logging.googleapis.com
```

### 2.2 Create Service Account

```bash
# Create service account
gcloud iam service-accounts create jk-cement-ai \
  --display-name="JK Cement AI Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:jk-cement-ai@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Create and download key
gcloud iam service-accounts keys create credentials.json \
  --iam-account=jk-cement-ai@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 2.3 Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Get API Key"**
3. Copy your API key

---

## Step 3: Configure Environment Variables

### 3.1 Backend Configuration

Create `backend/.env`:

```bash
# Navigate to backend directory
cd backend

# Create .env file
cat > .env << 'EOF'
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
GOOGLE_API_KEY=your-gemini-api-key

# Vertex AI Configuration
VERTEX_AI_LOCATION=asia-south1
VERTEX_AI_MODEL=gemini-2.0-flash-exp

# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/jk_cement_plant

# Cloud Storage
GCS_BUCKET_NAME=jk-cement-plant-data
GCS_IMAGES_BUCKET=jk-cement-plant-images

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Security
SECRET_KEY=your-secret-key-change-in-production

# Logging
ENABLE_CLOUD_LOGGING=False
LOG_LEVEL=INFO
EOF
```

### 3.2 Frontend Configuration

Create `frontend/.env.local`:

```bash
# Navigate to frontend root
cd ..

# Create .env.local file
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
EOF
```

---

## Step 4: Set Up Database

### 4.1 Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE jk_cement_plant;

# Exit psql
\q
```

### 4.2 Populate Sample Data

```bash
cd backend

# Install Python dependencies first (see Step 5)
python scripts/populate_database.py
```

---

## Step 5: Install Backend Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 6: Install Frontend Dependencies

```bash
cd ..  # Back to root

# Install dependencies
npm install
# or
yarn install
# or
pnpm install
```

---

## Step 7: Start the Application

### 7.1 Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # Activate venv if not already active
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 7.2 Start Frontend (Terminal 2)

```bash
# In root directory
npm run dev
# or
yarn dev
# or
pnpm dev
```

You should see:
```
  ▲ Next.js 15.5.2
  - Local:        http://localhost:3000
  - Network:      http://192.168.1.x:3000

 ✓ Ready in 2.5s
```

---

## Step 8: Verify Installation

### 8.1 Check Backend Health

Open browser to: `http://localhost:8000/docs`

You should see the FastAPI interactive documentation (Swagger UI).

### 8.2 Check Frontend

Open browser to: `http://localhost:3000`

You should see the JK Cement AI Optimization dashboard.

### 8.3 Test AI Chat

1. Navigate to the **AI Chat** module
2. Type: "What is the current kiln temperature?"
3. You should receive an AI-generated response with real data

---

## Common Issues & Solutions

### Issue: Database Connection Error

**Error**: `Connection refused` or `Cannot connect to database`

**Solution**:
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Start PostgreSQL if needed
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS

# Verify connection
psql -U postgres -c "SELECT version();"
```

### Issue: Python Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'xxx'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check installation
pip list
```

### Issue: Google Cloud Authentication Error

**Error**: `Could not load the default credentials`

**Solution**:
```bash
# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"

# Verify service account
gcloud auth list

# Login if needed
gcloud auth application-default login
```

### Issue: Frontend Build Errors

**Error**: `Module not found` or `Cannot find module`

**Solution**:
```bash
# Clear cache
rm -rf .next node_modules

# Reinstall dependencies
npm install

# Restart dev server
npm run dev
```

### Issue: Port Already in Use

**Error**: `EADDRINUSE: address already in use :::3000`

**Solution**:
```bash
# Find process using port
lsof -ti:3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
npm run dev -- -p 3001
```

---

## Next Steps

Now that your system is running:

1. **[Explore the Dashboard](../features/monitoring.md)** - Learn about each module
2. **[Try AI Chat](../features/ai-chat.md)** - Interact with the AI agent
3. **[Configure Vision API](../features/vision-api.md)** - Set up quality inspection
4. **[Review API Documentation](../api/rest-endpoints.md)** - Integrate with external systems
5. **[Deploy to Production](../deployment/overview.md)** - Deploy to Google Cloud

---

## Getting Help

- **Documentation**: Browse this wiki
- **API Docs**: `http://localhost:8000/docs`
- **Technical Support**: support@codygon.com
- **Issues**: [GitHub Issues](https://github.com/codygontechadmin/cement-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/codygontechadmin/cement-ai/discussions)

---

**Developed by**: Codygon Technologies Private Limited  
**Support**: support@codygon.com

---

**Congratulations! Your JK Cement AI Optimization System is now running! 🎉**
