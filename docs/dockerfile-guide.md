# 📚 Dockerfile Best Practices Guide

A comprehensive guide to writing optimal Dockerfiles for Python applications.

## 🎯 Overview

This guide covers essential best practices for creating efficient, secure, and maintainable Dockerfiles specifically for Python applications.

## 📋 Table of Contents

- [Base Image Selection](#-base-image-selection)
- [Layer Optimization](#-layer-optimization)
- [Dependency Management](#-dependency-management)
- [Security Practices](#-security-practices)
- [Performance Optimization](#-performance-optimization)
- [Production Readiness](#-production-readiness)
- [Common Pitfalls](#-common-pitfalls)

---

## 🐳 Base Image Selection

### Choose the Right Base Image

```dockerfile
# ✅ Good: Specific version and slim variant
FROM python:3.11-slim

# ❌ Avoid: Latest tag (unpredictable)
FROM python:latest

# ❌ Avoid: Full image (unnecessarily large)
FROM python:3.11
```

### Image Size Comparison

| Base Image           | Size   | Use Case                          |
| -------------------- | ------ | --------------------------------- |
| `python:3.11-alpine` | ~50MB  | Minimal size, basic dependencies  |
| `python:3.11-slim`   | ~120MB | **Recommended** - Good balance    |
| `python:3.11`        | ~920MB | Full features, heavy dependencies |

### When to Use Each

**Alpine (`python:3.11-alpine`)**

- ✅ Smallest size
- ✅ Good for microservices
- ❌ Compilation issues with some packages
- ❌ Different package manager (apk)

**Slim (`python:3.11-slim`)** - **Recommended**

- ✅ Good size/functionality balance
- ✅ Compatible with most Python packages
- ✅ Debian-based (familiar package manager)

**Full (`python:3.11`)**

- ✅ All development tools included
- ❌ Very large size
- ❌ Security surface area

---

## 🔄 Layer Optimization

### Order Instructions by Change Frequency

```dockerfile
# ✅ Optimal order
FROM python:3.11-slim

# 1. System dependencies (change rarely)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements first (change less often)
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code (changes most often)
COPY . .

# 6. Runtime configuration
USER appuser
EXPOSE 8000
CMD ["python", "app.py"]
```

### Layer Caching Benefits

**Good caching strategy:**

- Requirements change → Only rebuild from step 4
- Code change → Only rebuild from step 5
- Base image update → Rebuild everything (expected)

### Combine RUN Instructions

```dockerfile
# ✅ Good: Single layer
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ❌ Bad: Multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get clean
```

---

## 📦 Dependency Management

### Requirements Files Strategy

```dockerfile
# ✅ Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ For Poetry users
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# ✅ For multiple requirement files
COPY requirements/ ./requirements/
RUN pip install --no-cache-dir \
    -r requirements/base.txt \
    -r requirements/production.txt
```

### Pip Installation Best Practices

```dockerfile
# ✅ Optimal pip install
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Key flags:
# --no-cache-dir: Reduces image size
# --upgrade pip: Ensures latest pip version
# --no-deps: Skip dependency checks (if needed)
```

### Version Pinning

```txt
# requirements.txt - ✅ Good versioning
Flask==3.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.7

# ❌ Avoid unpinned versions
Flask
gunicorn>=20.0
psycopg2-binary~=2.9
```

---

## 🔒 Security Practices

### Non-Root User Configuration

```dockerfile
# ✅ Create and use non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# ✅ Alternative with specific UID/GID
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -s /bin/bash appuser
USER appuser
```

### File Permissions

```dockerfile
# ✅ Proper ownership and permissions
COPY --chown=appuser:appuser . /app
RUN chmod +x /app/entrypoint.sh

# ✅ Secure file permissions
RUN find /app -type f -exec chmod 644 {} \; && \
    find /app -type d -exec chmod 755 {} \;
```

### Secrets Management

```dockerfile
# ❌ Never do this
ENV SECRET_KEY=mysecretkey123

# ✅ Use runtime environment variables
ENV SECRET_KEY=""

# ✅ Use Docker secrets (in docker-compose or swarm)
# Or mount secrets at runtime
```

### Minimal Attack Surface

```dockerfile
# ✅ Remove unnecessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        && rm -rf /var/lib/apt/lists/* \
        && apt-get autoremove -y
```

---

## ⚡ Performance Optimization

### Multi-stage Builds

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Copy only installed packages
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

CMD ["python", "app.py"]
```

### Python Optimizations

```dockerfile
# ✅ Python performance flags
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# PYTHONUNBUFFERED: Real-time logging
# PYTHONDONTWRITEBYTECODE: Smaller images
# PYTHONPATH: Module resolution
```

### Build Context Optimization

```dockerignore
# .dockerignore - Exclude unnecessary files
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.pytest_cache/
.coverage
.venv/
venv/
.git/
.gitignore
README.md
Dockerfile
.dockerignore
.vscode/
.idea/
tests/
docs/
*.log
```

---

## 🚀 Production Readiness

### Health Checks

```dockerfile
# ✅ HTTP health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ✅ Custom health check script
COPY healthcheck.py .
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python healthcheck.py || exit 1
```

### Signal Handling

```dockerfile
# ✅ Use exec form for proper signal handling
CMD ["python", "app.py"]

# ❌ Shell form doesn't handle signals properly
CMD python app.py
```

### Logging Configuration

```dockerfile
# ✅ Configure proper logging
ENV PYTHONUNBUFFERED=1

# In your Python app:
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Environment Configuration

```dockerfile
# ✅ Environment-specific settings
ENV ENVIRONMENT=production \
    DEBUG=False \
    LOG_LEVEL=INFO

# ✅ Use .env files in development
# Mount them at runtime, don't copy into image
```

---

## ⚠️ Common Pitfalls

### Avoid These Mistakes

```dockerfile
# ❌ Running as root
USER root
CMD ["python", "app.py"]

# ❌ Installing unnecessary dependencies
RUN apt-get install -y build-essential git vim curl wget

# ❌ Not cleaning package cache
RUN apt-get update && apt-get install -y curl

# ❌ Copying everything before dependencies
COPY . .
RUN pip install -r requirements.txt

# ❌ Using ADD instead of COPY
ADD . /app

# ❌ Not using .dockerignore
# (Results in large build context)

# ❌ Hardcoding values
EXPOSE 8000
ENV DATABASE_URL=postgresql://localhost/mydb
```

### Debug Large Images

```bash
# Analyze image layers
docker history your-image:tag

# Check image size
docker images your-image:tag

# Inspect what's taking space
docker run --rm -it your-image:tag du -sh /*
```

---

## 📊 Dockerfile Template Checklist

Use this checklist for every Dockerfile:

### 🔍 Base Configuration

- [ ] Specific base image version (no `latest`)
- [ ] Appropriate image variant (`slim` recommended)
- [ ] Set `WORKDIR`

### 📦 Dependencies

- [ ] Copy requirements files first
- [ ] Use `--no-cache-dir` with pip
- [ ] Pin dependency versions
- [ ] Clean package cache after installation

### 🔒 Security

- [ ] Create and use non-root user
- [ ] Set proper file permissions
- [ ] No secrets in environment variables
- [ ] Minimal package installation

### ⚡ Performance

- [ ] Optimal layer ordering
- [ ] Combined RUN instructions
- [ ] Proper `.dockerignore`
- [ ] Consider multi-stage builds

### 🚀 Production

- [ ] Add health checks
- [ ] Use exec form for CMD
- [ ] Configure environment variables
- [ ] Set up proper logging

---

## 📖 Example: Complete Production Dockerfile

```dockerfile
# Multi-stage build for production Flask app
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Update PATH for user packages
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "app.py"]
```

---

## 🔗 Next Steps

- Review [Security Considerations](security-guide.md)
- Learn about [Image Optimization](optimization-guide.md)
- Practice with [Examples](../examples/)
- Complete [Exercises](../exercises/)

---

**📚 Additional Resources:**

- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Python Docker Official Guide](https://docs.docker.com/language/python/)
- [Security Scanning Tools](https://docs.docker.com/engine/scan/)
