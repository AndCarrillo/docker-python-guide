# Multi-stage Dockerfile for FastAPI production deployment
# Demonstrates advanced container optimization techniques

# ===== BUILDER STAGE =====
FROM python:3.11-slim as builder

# Build arguments
ARG BUILD_ENV=production

# Set environment variables for build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Create wheel directory
WORKDIR /wheels

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# ===== PRODUCTION STAGE =====
FROM python:3.11-slim as production

# Metadata
LABEL maintainer="your-email@example.com" \
    description="FastAPI application demonstrating container best practices" \
    version="1.0.0"

# Runtime environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PYTHONOPTIMIZE=1 \
    PATH="/home/appuser/.local/bin:$PATH" \
    HOST=0.0.0.0 \
    PORT=8000

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean

# Create non-root user
RUN groupadd -r appgroup --gid 1000 \
    && useradd -r -g appgroup --uid 1000 --home-dir /app --shell /bin/bash appuser \
    && mkdir -p /app \
    && chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Set working directory
WORKDIR /app

# Install Python dependencies from wheels
COPY --from=builder /wheels /wheels
COPY --chown=appuser:appgroup requirements.txt .
RUN pip install --user --no-cache-dir --no-index --find-links /wheels -r requirements.txt \
    && rm -rf /wheels

# Copy application code
COPY --chown=appuser:appgroup . .

# Create directories for logs and tmp files
RUN mkdir -p logs tmp

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Use Gunicorn for production
CMD ["gunicorn", "app:app", \
    "--bind", "0.0.0.0:8000", \
    "--worker-class", "uvicorn.workers.UvicornWorker", \
    "--workers", "4", \
    "--access-logfile", "-", \
    "--error-logfile", "-", \
    "--log-level", "info"]

# ===== DEVELOPMENT STAGE =====
FROM builder as development

# Install main dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies
COPY requirements-dev.txt* ./
RUN if [ -f requirements-dev.txt ]; then \
    pip install --no-cache-dir -r requirements-dev.txt; \
    fi

# Install application in development mode
WORKDIR /app
COPY . .

# Use uvicorn with auto-reload for development
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
