# 📚 Dockerfile Guide for Module 1

Essential Dockerfile practices for Python containerization basics.

## 🎯 Overview

Learn the fundamental Dockerfile patterns you need to containerize Python applications effectively. Focus on simple, proven practices.

## 📋 What You'll Learn

- [Base Image Selection](#-base-image-selection)
- [Basic Structure](#-basic-structure)
- [Dependency Management](#-dependency-management)
- [Essential Best Practices](#-essential-best-practices)

---

## 🐳 Base Image Selection

### Choose the Right Base Image

```dockerfile
# ✅ Recommended: Specific version and slim variant
FROM python:3.11-slim

# ✅ Good: Pin exact version for consistency  
FROM python:3.11.6-slim

# ❌ Avoid: Latest tag (unpredictable)
FROM python:latest

# ❌ Avoid: Full image (too large)
FROM python:3.11
```

### Image Size Comparison

| Base Image           | Size   | Use Case                |
| -------------------- | ------ | ----------------------- |
| `python:3.11-alpine` | ~50MB  | Smallest (compatibility issues) |
| `python:3.11-slim`   | ~120MB | **✅ Recommended for Module 1** |
| `python:3.11`        | ~920MB | Too large              |

**Why `python:3.11-slim`?**
- Good balance of size vs compatibility
- Includes essential libraries
- Works with most Python packages
- 7x smaller than full image

---

## 🏗️ Basic Structure

### Simple Dockerfile Pattern

```dockerfile
# 1. Base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements first (for better caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

# 6. Create non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser
USER appuser

# 7. Expose port
EXPOSE 8000

# 8. Run application
CMD ["python", "app.py"]
```

### Why This Order Matters

1. **Base image first** - Foundation layer
2. **Working directory** - Consistent location
3. **Requirements first** - Better Docker layer caching
4. **Install dependencies** - Heavy operation, cached if requirements don't change
5. **Copy code** - Changes frequently, separate layer
6. **User setup** - Security measure
7. **Expose port** - Documentation + networking
8. **Run command** - Application entrypoint

---

## 📦 Dependency Management

### Python Dependencies

```dockerfile
# ✅ Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Pin exact versions in requirements.txt
# requirements.txt:
# flask==2.3.3
# gunicorn==21.2.0

# ❌ Poor caching - code changes invalidate dependency layer
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
```

### Why Pin Versions?

```txt
# requirements.txt

# ✅ Pinned versions (predictable builds)
flask==2.3.3
requests==2.31.0
gunicorn==21.2.0

# ❌ Loose versions (unpredictable)
flask>=2.0
requests
gunicorn~=21.0
```

---

## 🛠️ Essential Best Practices

### 1. Use .dockerignore

Create `.dockerignore` to exclude unnecessary files:

```dockerignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
.venv/

# Development
.git/
.gitignore
README.md
tests/
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### 2. Environment Variables

```dockerfile
# ✅ Python optimization flags
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ✅ Disable Python debug mode
ENV PYTHONDEBUG=0
```

### 3. Non-root User

```dockerfile
# ✅ Create and use non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser
COPY --chown=appuser:appuser . .
USER appuser
```

### 4. Health Check (Optional)

```dockerfile
# ✅ Simple health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

---

## 📝 Complete Example

Here's a complete, production-ready Dockerfile for Module 1:

```dockerfile
# Use specific Python version with slim variant
FROM python:3.11-slim

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDEBUG=0

# Set working directory
WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser

# Copy and install dependencies (as root for pip permissions)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code with proper ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port (non-privileged port)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run application
CMD ["python", "app.py"]
```

---

## ✅ Module 1 Checklist

When creating your Dockerfile, ensure:

- [ ] Use `python:3.11-slim` base image
- [ ] Set Python environment variables
- [ ] Copy requirements.txt first for caching
- [ ] Use `--no-cache-dir` with pip
- [ ] Create and use non-root user
- [ ] Use .dockerignore file
- [ ] Expose appropriate port
- [ ] Define CMD instruction

---

## 🎯 Module 1 Focus

These Dockerfile patterns will serve you well for basic containerization:

1. **Standard structure** - Consistent, predictable builds
2. **Layer optimization** - Better build performance  
3. **Security basics** - Non-root user, secure defaults
4. **Best practices** - Industry-standard approaches

---

## 📖 Next Steps

Advanced Dockerfile techniques covered in later modules:

- **Module 2**: Development vs production configurations
- **Module 3**: Multi-stage builds and advanced optimization
- **Module 4**: CI/CD integration and automation
- **Module 5**: Production deployment patterns

---

**🐳 Remember**: Master these basics first. Advanced techniques build upon these fundamental patterns.
