# ================================================================
# Stage 1: Builder - Build dependencies and wheels
# ================================================================
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create wheels directory
WORKDIR /wheels

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# ================================================================
# Stage 2: Development - Include dev dependencies and tools
# ================================================================
FROM python:3.11-slim AS development

# Copy wheels from builder stage
COPY --from=builder /wheels /wheels

# Install from wheels
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir --find-links /wheels -r requirements.txt && \
    if [ -f requirements-dev.txt ]; then \
    pip install --no-cache-dir -r requirements-dev.txt; \
    fi && \
    rm -rf /wheels

# Create non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser

# Set working directory and copy application
WORKDIR /app
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Command for development
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ================================================================
# Stage 3: Production - Optimized for production deployment
# ================================================================
FROM python:3.11-slim AS production

# Copy wheels from builder stage
COPY --from=builder /wheels /wheels

# Install from wheels (production only)
COPY requirements.txt ./
RUN pip install --no-cache-dir --find-links /wheels -r requirements.txt && \
    rm -rf /wheels

# Create non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser

# Set working directory and copy only application code
WORKDIR /app
COPY app/ ./app/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Command for production
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
