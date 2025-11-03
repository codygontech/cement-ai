# Quick Start Script for Cement Plant AI Backend

Write-Host "🏭 Cement Plant AI Backend - Quick Start" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check if .env exists
if (!(Test-Path ".env")) {
    Write-Host "`nCreating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created" -ForegroundColor Green
    Write-Host "⚠️  Please edit .env and add your GOOGLE_API_KEY" -ForegroundColor Yellow
    Write-Host "   Get your key from: https://aistudio.google.com/app/apikey`n" -ForegroundColor Cyan
    
    # Open .env in default editor
    if ($env:EDITOR) {
        & $env:EDITOR .env
    } elseif (Get-Command code -ErrorAction SilentlyContinue) {
        code .env
    } else {
        notepad .env
    }
    
    Read-Host "Press Enter after you've added your GOOGLE_API_KEY"
}

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -e . 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check database connection
Write-Host "`nChecking database connection..." -ForegroundColor Yellow
$dbCheck = python -c "import asyncio; from app.db.session import engine; asyncio.run(engine.dispose())" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database connection OK" -ForegroundColor Green
} else {
    Write-Host "⚠️  Database connection failed. Using local PostgreSQL?" -ForegroundColor Yellow
    Write-Host "   Make sure PostgreSQL is running and DATABASE_URL in .env is correct`n" -ForegroundColor Cyan
}

# Initialize database
Write-Host "`nInitializing database tables..." -ForegroundColor Yellow
python -c "from app.db.session import init_db; import asyncio; asyncio.run(init_db())" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database initialized" -ForegroundColor Green
} else {
    Write-Host "⚠️  Database initialization had warnings (this might be OK if tables already exist)" -ForegroundColor Yellow
}

# Ask about sample data
Write-Host ""
$loadData = Read-Host "Do you want to load sample data? (y/n)"
if ($loadData -eq "y" -or $loadData -eq "Y") {
    Write-Host "`nGenerating sample data..." -ForegroundColor Yellow
    python scripts/generate_sample_data.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Sample data loaded" -ForegroundColor Green
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✓ Backend setup complete!" -ForegroundColor Green
Write-Host "`nTo start the backend server, run:" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor White
Write-Host "`nAPI will be available at:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000" -ForegroundColor White
Write-Host "  http://localhost:8000/docs (API documentation)" -ForegroundColor White
Write-Host "`nDon't forget to start the frontend in another terminal!" -ForegroundColor Yellow
Write-Host "  cd .. && npm run dev`n" -ForegroundColor White

# Offer to start the server
$startServer = Read-Host "Start the backend server now? (y/n)"
if ($startServer -eq "y" -or $startServer -eq "Y") {
    Write-Host "`nStarting backend server..." -ForegroundColor Cyan
    python main.py
}
