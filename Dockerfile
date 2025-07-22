# Basic Dockerfile for CI/CD testing
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Default command for testing
CMD ["python", "-m", "pytest", "tests/", "-v"]
