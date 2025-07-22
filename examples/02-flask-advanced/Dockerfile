# Multi-stage Dockerfile for Flask with database
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
WORKDIR /wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies from wheels
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --find-links /wheels -r requirements.txt \
    && rm -rf /wheels requirements.txt

# Copy application code
COPY app.py .

# Create non-root user and directories
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

USER appuser

# Create volume for database
VOLUME ["/app/data"]

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "app.py"]
