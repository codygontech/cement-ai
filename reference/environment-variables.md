# Environment Variables Reference

Complete reference for all environment variables used in the JK Cement AI Optimization System.

---

## Backend Environment Variables

### Google Cloud Configuration

#### `GOOGLE_CLOUD_PROJECT`
- **Type**: String
- **Required**: Yes
- **Default**: `jk-cement-ai-optimization`
- **Description**: Your Google Cloud project ID
- **Example**: `my-cement-project-123456`

#### `GOOGLE_APPLICATION_CREDENTIALS`
- **Type**: File Path
- **Required**: Yes (for service account auth)
- **Default**: None
- **Description**: Path to Google Cloud service account JSON key file
- **Example**: `./credentials.json` or `/path/to/service-account-key.json`

#### `GOOGLE_API_KEY`
- **Type**: String
- **Required**: Yes (for Gemini AI)
- **Default**: None
- **Description**: Google AI Studio API key for Gemini 2.0
- **Example**: `AIzaSyD...`
- **Get Key**: [Google AI Studio](https://makersuite.google.com/app/apikey)

---

### Vertex AI Configuration

#### `VERTEX_AI_LOCATION`
- **Type**: String
- **Required**: No
- **Default**: `asia-south1`
- **Description**: Google Cloud region for Vertex AI services
- **Options**: 
  - `asia-south1` (Mumbai, India)
  - `us-central1` (Iowa, USA)
  - `europe-west4` (Netherlands)
  - [All regions](https://cloud.google.com/vertex-ai/docs/general/locations)

#### `VERTEX_AI_MODEL`
- **Type**: String
- **Required**: No
- **Default**: `gemini-2.0-flash-exp`
- **Description**: Gemini model to use
- **Options**:
  - `gemini-2.0-flash-exp` (Latest, experimental)
  - `gemini-1.5-pro`
  - `gemini-1.5-flash`

---

### Database Configuration

#### `DATABASE_URL`
- **Type**: Connection String
- **Required**: Yes
- **Default**: `postgresql+asyncpg://postgres:postgres@localhost:5432/jk_cement_plant`
- **Description**: PostgreSQL database connection URL for SQLAlchemy
- **Format**: `postgresql+asyncpg://user:password@host:port/database`
- **Examples**:
  ```
  # Local PostgreSQL
  postgresql+asyncpg://postgres:mypassword@localhost:5432/cement_db
  
  # Cloud SQL via Proxy
  postgresql+asyncpg://postgres:password@localhost:5432/cement_db
  
  # Cloud SQL Direct (with SSL)
  postgresql+asyncpg://user:pass@10.1.2.3:5432/cement_db
  ```

#### `CLOUD_SQL_CONNECTION_NAME`
- **Type**: String
- **Required**: No (only for Cloud SQL)
- **Default**: None
- **Description**: Cloud SQL connection name for Cloud SQL Proxy
- **Format**: `project:region:instance`
- **Example**: `jk-cement-ai:asia-south1:cement-db-instance`

---

### Cloud Storage Configuration

#### `GCS_BUCKET_NAME`
- **Type**: String
- **Required**: No
- **Default**: `jk-cement-plant-data`
- **Description**: Google Cloud Storage bucket for general data storage
- **Example**: `my-cement-data-bucket`

#### `GCS_IMAGES_BUCKET`
- **Type**: String
- **Required**: No
- **Default**: `jk-cement-plant-images`
- **Description**: GCS bucket specifically for quality inspection images
- **Example**: `cement-quality-images`

---

### API Configuration

#### `API_HOST`
- **Type**: String (IP Address)
- **Required**: No
- **Default**: `0.0.0.0`
- **Description**: Host IP address for FastAPI server
- **Options**:
  - `0.0.0.0` - Listen on all interfaces
  - `127.0.0.1` - Localhost only
  - Specific IP for production

#### `API_PORT`
- **Type**: Integer
- **Required**: No
- **Default**: `8000`
- **Description**: Port number for FastAPI server
- **Range**: 1-65535
- **Common Ports**: 8000, 8080, 3001

#### `DEBUG`
- **Type**: Boolean
- **Required**: No
- **Default**: `True`
- **Description**: Enable debug mode (detailed error messages)
- **Values**: `True`, `False`, `1`, `0`
- **Warning**: Set to `False` in production!

#### `CORS_ORIGINS`
- **Type**: String (comma-separated)
- **Required**: No
- **Default**: `http://localhost:3000,http://localhost:3001`
- **Description**: Allowed CORS origins for API requests
- **Format**: Comma-separated URLs without trailing slashes
- **Examples**:
  ```
  # Development
  http://localhost:3000,http://localhost:3001
  
  # Production
  https://cement.example.com,https://app.example.com
  
  # Mixed
  https://cement.example.com,http://localhost:3000
  ```

---

### Security Configuration

#### `SECRET_KEY`
- **Type**: String
- **Required**: Yes
- **Default**: `change-this-secret-key-in-production`
- **Description**: Secret key for cryptographic operations
- **Generation**:
  ```bash
  # Generate random secret key
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- **Warning**: Change default in production!

---

### WebSocket Configuration

#### `WS_HEARTBEAT_INTERVAL`
- **Type**: Integer (seconds)
- **Required**: No
- **Default**: `30`
- **Description**: Interval for WebSocket heartbeat/ping messages
- **Range**: 10-300 seconds

---

### Logging Configuration

#### `ENABLE_CLOUD_LOGGING`
- **Type**: Boolean
- **Required**: No
- **Default**: `False`
- **Description**: Enable Google Cloud Logging integration
- **Values**: `True`, `False`, `1`, `0`
- **Note**: Requires Google Cloud credentials

#### `LOG_LEVEL`
- **Type**: String
- **Required**: No
- **Default**: `INFO`
- **Description**: Minimum logging level
- **Options**:
  - `DEBUG` - Detailed debugging information
  - `INFO` - General informational messages
  - `WARNING` - Warning messages
  - `ERROR` - Error messages
  - `CRITICAL` - Critical errors only

---

## Frontend Environment Variables

All frontend environment variables must be prefixed with `NEXT_PUBLIC_` to be accessible in the browser.

### API Configuration

#### `NEXT_PUBLIC_API_URL`
- **Type**: String (URL)
- **Required**: Yes
- **Default**: `http://localhost:8000`
- **Description**: Base URL for backend API
- **Examples**:
  ```
  # Development
  http://localhost:8000
  
  # Production
  https://api.cement.example.com
  ```

#### `NEXT_PUBLIC_WS_URL`
- **Type**: String (WebSocket URL)
- **Required**: No
- **Default**: `ws://localhost:8000`
- **Description**: WebSocket endpoint for real-time features
- **Examples**:
  ```
  # Development
  ws://localhost:8000
  
  # Production (secure)
  wss://api.cement.example.com
  ```

---

## Example Configuration Files

### Backend `.env` (Development)

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=jk-cement-ai-dev
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
GOOGLE_API_KEY=AIzaSyD...your-api-key...

# Vertex AI Configuration
VERTEX_AI_LOCATION=asia-south1
VERTEX_AI_MODEL=gemini-2.0-flash-exp

# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/jk_cement_plant

# Cloud Storage
GCS_BUCKET_NAME=jk-cement-plant-data-dev
GCS_IMAGES_BUCKET=jk-cement-plant-images-dev

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Security
SECRET_KEY=dev-secret-key-change-in-production

# WebSocket
WS_HEARTBEAT_INTERVAL=30

# Logging
ENABLE_CLOUD_LOGGING=False
LOG_LEVEL=DEBUG
```

### Backend `.env` (Production)

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=jk-cement-ai-prod
GOOGLE_APPLICATION_CREDENTIALS=/etc/secrets/gcp-credentials.json
GOOGLE_API_KEY=${SECRET_GEMINI_API_KEY}

# Vertex AI Configuration
VERTEX_AI_LOCATION=asia-south1
VERTEX_AI_MODEL=gemini-2.0-flash-exp

# Database Configuration (Cloud SQL)
DATABASE_URL=postgresql+asyncpg://cement_user:${DB_PASSWORD}@localhost:5432/jk_cement_plant
CLOUD_SQL_CONNECTION_NAME=jk-cement-ai-prod:asia-south1:cement-db

# Cloud Storage
GCS_BUCKET_NAME=jk-cement-plant-data-prod
GCS_IMAGES_BUCKET=jk-cement-plant-images-prod

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
DEBUG=False
CORS_ORIGINS=https://cement.jkcement.com,https://app.jkcement.com

# Security
SECRET_KEY=${SECRET_KEY}

# WebSocket
WS_HEARTBEAT_INTERVAL=30

# Logging
ENABLE_CLOUD_LOGGING=True
LOG_LEVEL=INFO
```

### Frontend `.env.local` (Development)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Frontend `.env.production`

```bash
NEXT_PUBLIC_API_URL=https://api.cement.jkcement.com
NEXT_PUBLIC_WS_URL=wss://api.cement.jkcement.com
```

---

## Docker Compose Example

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    environment:
      # Google Cloud
      - GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
      - GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      
      # Vertex AI
      - VERTEX_AI_LOCATION=asia-south1
      - VERTEX_AI_MODEL=gemini-2.0-flash-exp
      
      # Database
      - DATABASE_URL=postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@db:5432/cement
      
      # Cloud Storage
      - GCS_BUCKET_NAME=${GCS_BUCKET_NAME}
      - GCS_IMAGES_BUCKET=${GCS_IMAGES_BUCKET}
      
      # API
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - DEBUG=False
      - CORS_ORIGINS=http://localhost:3000
      
      # Security
      - SECRET_KEY=${SECRET_KEY}
      
      # Logging
      - ENABLE_CLOUD_LOGGING=True
      - LOG_LEVEL=INFO
    volumes:
      - ./credentials.json:/app/credentials.json:ro
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: .
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - NEXT_PUBLIC_WS_URL=ws://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend

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

volumes:
  postgres_data:
```

---

## Environment Variable Loading

### Python (Backend)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_API_KEY: str
    DATABASE_URL: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
```

### Next.js (Frontend)

```typescript
// Access environment variables
const API_URL = process.env.NEXT_PUBLIC_API_URL;
const WS_URL = process.env.NEXT_PUBLIC_WS_URL;

// Validate at build time
if (!API_URL) {
  throw new Error('NEXT_PUBLIC_API_URL is not defined');
}
```

---

## Security Best Practices

### 1. Never Commit `.env` Files

Add to `.gitignore`:
```gitignore
# Environment variables
.env
.env.local
.env.*.local
*.env
credentials.json
*.key.json
```

### 2. Use Secret Management

**Development:**
- Use `.env` files (not committed)
- Store credentials in secure location

**Production:**
- Google Cloud Secret Manager
- Kubernetes Secrets
- AWS Secrets Manager
- HashiCorp Vault

### 3. Rotate Secrets Regularly

- API keys: Every 90 days
- Database passwords: Every 30-60 days
- Service account keys: Every 90 days

### 4. Use Minimal Permissions

Grant only required permissions:
```bash
# Create service account with minimal roles
gcloud iam service-accounts create cement-api \
  --display-name="Cement API Service Account"

# Grant specific roles
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:cement-api@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

---

## Validation & Testing

### Validate Environment Variables

```python
# backend/app/core/config.py

from pydantic import validator

class Settings(BaseSettings):
    DATABASE_URL: str
    
    @validator('DATABASE_URL')
    def validate_database_url(cls, v):
        if not v.startswith('postgresql'):
            raise ValueError('DATABASE_URL must be a PostgreSQL connection string')
        return v
```

### Test Configuration

```python
# backend/tests/test_config.py

def test_settings_loading():
    """Test that settings load correctly."""
    from app.core.config import settings
    
    assert settings.GOOGLE_CLOUD_PROJECT is not None
    assert settings.DATABASE_URL.startswith('postgresql')
    assert settings.API_PORT > 0
```

---

## Troubleshooting

### Issue: Variable Not Loading

**Check:**
1. File named correctly (`.env`)
2. File in correct directory
3. No typos in variable names
4. No quotes around values (unless needed)
5. Application restarted after changes

### Issue: Frontend Variable Undefined

**Solution:**
- Ensure prefixed with `NEXT_PUBLIC_`
- Rebuild application: `npm run build`
- Restart dev server

### Issue: Google Cloud Auth Failing

**Check:**
1. `GOOGLE_APPLICATION_CREDENTIALS` path is correct
2. File exists and is readable
3. Service account has required permissions
4. JSON file is valid

---

## Next Steps

- **[Configuration Guide](../getting-started/configuration.md)** - Detailed setup
- **[Deployment Guide](../deployment/overview.md)** - Production deployment
- **[Google Cloud Setup](../deployment/google-cloud.md)** - GCP configuration
- **[Security Best Practices](../deployment/security.md)** - Security guidelines

---

**Last Updated**: November 2025
