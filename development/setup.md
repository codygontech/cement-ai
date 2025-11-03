# Development Guide

Guide for developers working on the JK Cement AI Optimization System.

---

## Development Environment Setup

### Prerequisites

- **Node.js 18+** with npm/yarn/pnpm
- **Python 3.11+** with pip
- **PostgreSQL 14+**
- **Git**
- **VS Code** (recommended) or your preferred IDE
- **Docker** (optional, for containerized development)
- **Google Cloud SDK** (for cloud services)

### Initial Setup

#### Repository Structure

The project uses a **multi-branch architecture** with separate branches for each component:

- **`frontend`** - Next.js 15 application with React 19
- **`backend`** - FastAPI Python backend with AI agents
- **`docs`** - Documentation site (Docsify)

1. **Clone Repository**
   ```bash
   git clone https://github.com/codygontech/cement-ai.git
   cd cement-ai
   ```

2. **Set Up Backend**
   ```bash
   # Switch to backend branch
   git checkout backend
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set Up Frontend** (in a new terminal/directory)
   ```bash
   # Clone again or use a separate directory
   cd ../cement-ai-frontend
   git clone https://github.com/codygontech/cement-ai.git .
   git checkout frontend
   
   # Install dependencies
   npm install
   ```

4. **Set Up Database**
   ```bash
   # Create database
   createdb jk_cement_plant
   
   # Run migrations (populate sample data)
   cd backend
   python scripts/populate_database.py
   ```

5. **Configure Environment**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env with your settings
   
   # Frontend
   cp .env.example .env.local
   # Edit .env.local with your settings
   ```

---

## Project Structure

### Branch: `backend`

```
cement-ai/ (backend branch)
├── app/
│   ├── agents/          # AI agents (LangGraph)
│   ├── core/            # Configuration, database
│   ├── db/              # Database sessions
│   └── routers/         # API endpoints
├── scripts/             # Utility scripts
├── requirements.txt     # Python dependencies
└── Dockerfile           # Container config
```

### Branch: `frontend`

```
cement-ai/ (frontend branch)
├── src/
│   ├── app/            # App Router pages
│   ├── components/     # React components
│   │   ├── layout/    # Layout components
│   │   ├── modules/   # Feature modules
│   │   └── ui/        # UI components
│   ├── hooks/         # Custom hooks
│   ├── lib/           # Utilities
│   ├── types/         # TypeScript types
│   └── constants/     # Constants
├── public/            # Static assets
└── package.json       # Dependencies
```

### Branch: `docs`

```
cement-ai/ (docs branch)
├── index.html         # Docsify entry point
├── _sidebar.md        # Sidebar navigation
├── _navbar.md         # Top navigation
├── INDEX.md           # Documentation index
├── getting-started/   # Getting started guides
├── backend/           # Backend documentation
├── frontend/          # Frontend documentation
├── deployment/        # Deployment guides
└── reference/         # Reference materials
```

---

## Development Workflow

### Running Development Servers

> **Important**: Since the project uses separate branches, you'll need to work with them in separate directories or use git worktrees.

#### Option 1: Separate Directories (Recommended)

**Terminal 1 - Backend:**
```bash
cd cement-ai-backend  # Your backend directory
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd cement-ai-frontend  # Your frontend directory
npm run dev
```

**Terminal 3 - Documentation (Optional):**
```bash
cd cement-ai-docs  # Your docs directory
docsify serve .
```

#### Option 2: Using Git Worktrees

```bash
# Create worktrees for each branch
cd cement-ai
git worktree add ../cement-ai-backend backend
git worktree add ../cement-ai-frontend frontend
git worktree add ../cement-ai-docs docs

# Now you have three directories, each on its respective branch
```

### Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Code Style Guide

### Python (Backend)

**Style Guide**: PEP 8

```python
# Good
async def get_plant_data(
    table_name: str,
    hours_back: int = 24,
    limit: int = 100
) -> Dict[str, Any]:
    """
    Fetch plant data from database.
    
    Args:
        table_name: Name of the table
        hours_back: Hours of historical data
        limit: Maximum records to return
        
    Returns:
        Dictionary containing the data
    """
    async with AsyncSessionLocal() as session:
        # Implementation
        pass

# Use type hints
def calculate_efficiency(
    production: float,
    consumption: float
) -> float:
    """Calculate efficiency percentage."""
    return (production / consumption) * 100

# Constants in UPPER_CASE
MAX_RECORDS = 1000
DEFAULT_TIMEOUT = 30

# Classes in PascalCase
class PlantDataProcessor:
    """Process plant data."""
    pass
```

**Formatting:**
```bash
# Install formatters
pip install black isort flake8

# Format code
black app/
isort app/
flake8 app/
```

### TypeScript/JavaScript (Frontend)

**Style Guide**: Airbnb TypeScript Style Guide

```typescript
// Good
interface PlantData {
  id: number;
  timestamp: string;
  temperature: number;
  production: number;
}

// Use async/await
async function fetchPlantData(): Promise<PlantData[]> {
  const response = await fetch('/api/data');
  return response.json();
}

// Arrow functions for components
export function PlantDashboard() {
  const [data, setData] = useState<PlantData[]>([]);
  
  useEffect(() => {
    fetchPlantData().then(setData);
  }, []);
  
  return <div>{/* Component JSX */}</div>;
}

// Constants in UPPER_SNAKE_CASE
const API_BASE_URL = 'http://localhost:8000';
const MAX_RETRY_ATTEMPTS = 3;

// Types/Interfaces in PascalCase
type ProcessType = 'kiln' | 'grinding' | 'raw_material';
```

**Formatting:**
```bash
# Install ESLint & Prettier
npm install -D eslint prettier

# Format code
npm run lint
npm run lint:fix
```

### React/TSX Components

```tsx
// Component structure
import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { fetchData } from '@/lib/api-client';

interface ComponentProps {
  title: string;
  onUpdate?: (data: Data) => void;
}

export function MyComponent({ title, onUpdate }: ComponentProps) {
  // 1. State declarations
  const [data, setData] = useState<Data | null>(null);
  const [loading, setLoading] = useState(false);
  
  // 2. Effects
  useEffect(() => {
    loadData();
  }, []);
  
  // 3. Event handlers
  const loadData = async () => {
    setLoading(true);
    try {
      const result = await fetchData();
      setData(result);
      onUpdate?.(result);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // 4. Render
  return (
    <Card>
      <h2>{title}</h2>
      {loading ? <LoadingSpinner /> : <DataDisplay data={data} />}
    </Card>
  );
}
```

---

## Git Workflow

### Branch Naming

```
main              # Production-ready code
develop           # Development branch
feature/xxx       # New features
bugfix/xxx        # Bug fixes
hotfix/xxx        # Emergency fixes
docs/xxx          # Documentation updates
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: <type>(<scope>): <subject>

# Examples
git commit -m "feat(ai-chat): add streaming response support"
git commit -m "fix(kiln): correct temperature calculation"
git commit -m "docs(api): update endpoint documentation"
git commit -m "refactor(database): optimize query performance"
git commit -m "test(quality): add quality metrics tests"
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting changes
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make Changes & Commit**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. **Push to Remote**
   ```bash
   git push origin feature/new-feature
   ```

4. **Create Pull Request**
   - Go to GitHub
   - Create PR from feature branch to develop
   - Add description and screenshots
   - Request review

5. **Address Review Comments**
   ```bash
   # Make changes
   git add .
   git commit -m "fix: address review comments"
   git push origin feature/new-feature
   ```

6. **Merge**
   - Squash and merge (for cleaner history)
   - Delete branch after merge

---

## Testing

### Backend Tests

```python
# backend/tests/test_agent.py

import pytest
from app.agents.cement_agent import get_realtime_plant_data

@pytest.mark.asyncio
async def test_get_realtime_data():
    """Test fetching realtime plant data."""
    result = await get_realtime_plant_data(
        table_name="kiln_operations",
        hours_back=1,
        limit=10
    )
    
    assert result is not None
    assert "data" in result
    assert len(result["data"]) <= 10

# Run tests
pytest backend/tests/
```

### Frontend Tests

```typescript
// src/components/__tests__/PlantDashboard.test.tsx

import { render, screen } from '@testing-library/react';
import { PlantDashboard } from '../PlantDashboard';

describe('PlantDashboard', () => {
  it('renders dashboard title', () => {
    render(<PlantDashboard />);
    expect(screen.getByText('Plant Dashboard')).toBeInTheDocument();
  });
  
  it('loads data on mount', async () => {
    render(<PlantDashboard />);
    const data = await screen.findByTestId('plant-data');
    expect(data).toBeInTheDocument();
  });
});

// Run tests
npm test
```

---

## Debugging

### Backend Debugging (VS Code)

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      },
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

### Frontend Debugging

```typescript
// Use React DevTools
// Install: https://chrome.google.com/webstore/detail/react-developer-tools/

// Console logging
console.log('Data:', data);
console.error('Error:', error);

// Debugger
debugger; // Pauses execution

// VS Code debugging with Chrome
// Add breakpoints in VS Code
```

---

## Performance Optimization

### Backend

```python
# Use async/await for I/O operations
async def fetch_data():
    async with AsyncSessionLocal() as session:
        result = await session.execute(query)
        return result.fetchall()

# Cache frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=128)
def get_config_value(key: str) -> str:
    return config[key]

# Use database indexes
# Add indexes in migration scripts
CREATE INDEX idx_timestamp ON kiln_operations(timestamp DESC);
```

### Frontend

```typescript
// Use React.memo for expensive components
export const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{/* Render data */}</div>;
});

// Use useMemo for expensive calculations
const processedData = useMemo(() => {
  return expensiveCalculation(data);
}, [data]);

// Use useCallback for event handlers
const handleClick = useCallback(() => {
  processData();
}, []);

// Code splitting
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <LoadingSpinner />,
});
```

---

## Database Migrations

### Creating New Tables

```python
# backend/scripts/create_new_table.py

from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS new_table (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            value FLOAT NOT NULL
        );
        
        CREATE INDEX idx_new_table_timestamp 
        ON new_table(timestamp DESC);
    """))
    conn.commit()
```

---

## API Documentation

### Adding New Endpoints

```python
# backend/app/routers/new_endpoint.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/new", tags=["New Feature"])

class NewRequest(BaseModel):
    """Request model."""
    param: str

class NewResponse(BaseModel):
    """Response model."""
    result: str

@router.post("/endpoint", response_model=NewResponse)
async def new_endpoint(request: NewRequest):
    """
    New endpoint description.
    
    - **param**: Parameter description
    
    Returns:
        Result object
    """
    return NewResponse(result="success")
```

---

## Common Tasks

### Adding a New Module

1. Create component file: `src/components/modules/new-module.tsx`
2. Implement module logic
3. Add to sidebar: `src/components/layout/sidebar.tsx`
4. Add icon from `lucide-react`
5. Test functionality

### Adding AI Agent Tool

```python
# backend/app/agents/cement_agent.py

@tool
async def new_tool(param: str) -> Dict[str, Any]:
    """
    Tool description for the AI agent.
    
    Args:
        param: Parameter description
        
    Returns:
        Result dictionary
    """
    # Implementation
    return {"result": "value"}

# Add to tools list
tools = [
    get_realtime_plant_data,
    calculate_efficiency_metrics,
    new_tool,  # Add here
]
```

---

## Troubleshooting

### Common Issues

**Issue**: ModuleNotFoundError
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: Database connection failed
```bash
# Check PostgreSQL is running
pg_isready

# Check connection string
echo $DATABASE_URL
```

**Issue**: Frontend build errors
```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run dev
```

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs
- **LangChain Docs**: https://python.langchain.com/
- **Google Cloud Docs**: https://cloud.google.com/docs

---

## Next Steps

- **[Testing Guide](./testing.md)** - Comprehensive testing
- **[Contributing](./contributing.md)** - Contribution guidelines
- **[API Reference](../backend/api-reference.md)** - API documentation
- **[Architecture](../getting-started/architecture.md)** - System architecture

---

**Last Updated**: November 2025
