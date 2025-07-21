# Multi-stage Dockerfile for Django production deployment
# Demonstrates Django-specific containerization techniques

# ===== BASE STAGE =====
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONHASHSEED=random

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean

WORKDIR /app

# ===== BUILDER STAGE =====
FROM base as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# ===== DEVELOPMENT STAGE =====
FROM builder as development

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from wheels
RUN pip install --no-cache-dir --find-links /wheels -r requirements.txt

# Create development user
RUN adduser --disabled-password --gecos '' --shell /bin/bash devuser \
    && chown -R devuser:devuser /app

# Copy project files
COPY --chown=devuser:devuser . .

# Create directories for static and media files
RUN mkdir -p static staticfiles media logs \
    && chown -R devuser:devuser static staticfiles media logs

USER devuser

# Expose port
EXPOSE 8000

# Development command with auto-reload
CMD ["python", "blogproject/manage.py", "runserver", "0.0.0.0:8000"]

# ===== PRODUCTION STAGE =====
FROM base as production

# Metadata
LABEL maintainer="your-email@example.com" \
      description="Django blog application demonstrating container best practices" \
      version="1.0.0"

# Production environment variables
ENV DJANGO_SETTINGS_MODULE=blogproject.settings \
    PYTHONOPTIMIZE=1

# Install runtime dependencies only
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links /wheels -r requirements.txt \
    && rm -rf /wheels requirements.txt

# Create non-root user for production
RUN groupadd -r appgroup --gid 1000 \
    && useradd -r -g appgroup --uid 1000 --home-dir /app --shell /bin/bash appuser \
    && chown -R appuser:appgroup /app

# Copy application code
COPY --chown=appuser:appgroup . .

# Create directories with proper permissions
RUN mkdir -p staticfiles media logs \
    && chown -R appuser:appgroup staticfiles media logs \
    && chmod 755 staticfiles media logs

# Switch to non-root user
USER appuser

# Collect static files (Django-specific)
RUN cd blogproject && python manage.py collectstatic --noinput --clear

# Create volume mount points
VOLUME ["/app/media", "/app/logs"]

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Production command using Gunicorn
CMD ["gunicorn", \
     "--chdir", "blogproject", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--preload", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "blogproject.wsgi:application"]

# ===== MIGRATION STAGE =====
FROM production as migration

# Special stage for running Django migrations
USER root

# Install PostgreSQL client for database operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

USER appuser

# Migration command
CMD ["python", "blogproject/manage.py", "migrate"]
