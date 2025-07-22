# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install dependencies (none in this case, but good practice)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY calculator.py .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Run the calculator
CMD ["python", "calculator.py"]
