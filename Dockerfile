FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and README (needed by hatchling build)
COPY pyproject.toml README.md ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY app ./app
COPY main.py ./

# Expose port (Cloud Run will override with PORT env var)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV API_HOST=0.0.0.0

# Run the application
CMD ["python", "main.py"]
