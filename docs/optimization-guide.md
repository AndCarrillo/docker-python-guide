# ⚡ Container Optimization Basics

Essential optimization techniques for Python containers in Module 1.

## 🎯 Overview

This guide covers the fundamental optimization strategies you'll need for containerizing Python applications effectively. Focus on the basics that provide the most impact.

## 📋 What You'll Learn

- [Base Image Selection](#-base-image-selection)
- [Image Size Optimization](#-image-size-optimization)
- [Build Performance](#-build-performance)
- [Basic Security](#-basic-security)
- [Quick Wins Checklist](#-quick-wins-checklist)

---

## 📦 Base Image Selection

Choose the right Python base image for your needs:

```dockerfile
# 📊 Image size comparison:
# python:3.11            (~900MB) - Full development environment
# python:3.11-slim       (~120MB) - ✅ Recommended for most apps
# python:3.11-alpine     (~50MB)  - Smallest, but potential compatibility issues

# ✅ Best choice for learning and production
FROM python:3.11-slim

# ❌ Avoid in production (too large)
FROM python:3.11
```

**Why slim?**

- 7x smaller than full image
- Includes essential libraries
- Good compatibility with most packages
- Faster downloads and deployments

---

## 🗜️ Image Size Optimization

### 1. Use .dockerignore

Create a `.dockerignore` file to exclude unnecessary files:

```dockerignore
# Development files
.git
.gitignore
README.md
*.md
.vscode/
.idea/

# Python cache
__pycache__/
*.pyc
*.pyo
.pytest_cache/

# Virtual environments
.venv/
venv/
env/

# OS files
.DS_Store
Thumbs.db
```

### 2. Optimize RUN Instructions

```dockerfile
# ❌ Multiple layers (inefficient)
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# ✅ Single layer (efficient)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
```

### 3. Copy Files Strategically

```dockerfile
# ✅ Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code last (changes most frequently)
COPY app.py .
```

---

## 🚀 Build Performance

### Layer Caching

Order your Dockerfile instructions from least to most frequently changed:

```dockerfile
FROM python:3.11-slim

# 1. System packages (rarely change)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Python dependencies (change occasionally)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Application code (changes frequently)
COPY . .
```

### Pip Optimizations

```dockerfile
# ✅ Optimize pip installations
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
```

Benefits:

- `--no-cache-dir`: Reduces image size
- `--upgrade pip`: Uses latest pip features
- Single RUN command: Reduces layers

---

## 🔒 Basic Security

### Non-Root User

Always run your application as a non-root user:

```dockerfile
# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

# Switch to non-root user
USER appuser

# Set working directory with proper permissions
WORKDIR /app
COPY --chown=appuser:appuser . .
```

### Environment Variables

```dockerfile
# Python optimizations
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
```

- `PYTHONUNBUFFERED=1`: Shows logs immediately
- `PYTHONDONTWRITEBYTECODE=1`: Prevents .pyc files

---

## ✅ Quick Wins Checklist

### Image Size

- [ ] Use `python:3.11-slim` base image
- [ ] Create comprehensive `.dockerignore`
- [ ] Combine RUN commands
- [ ] Remove package manager cache

### Build Performance

- [ ] Copy requirements.txt first
- [ ] Use `--no-cache-dir` with pip
- [ ] Order instructions by change frequency

### Security

- [ ] Create and use non-root user
- [ ] Set proper file permissions
- [ ] Use specific image tags (not `latest`)

### Python Optimization

- [ ] Set `PYTHONUNBUFFERED=1`
- [ ] Set `PYTHONDONTWRITEBYTECODE=1`
- [ ] Pin dependency versions

---

## 📏 Size Comparison

Here's what you can expect with these optimizations:

| Approach                       | Estimated Size | Use Case              |
| ------------------------------ | -------------- | --------------------- |
| `python:3.11` + basic app      | ~950MB         | ❌ Not recommended    |
| `python:3.11-slim` + basic app | ~130MB         | ✅ Good for most apps |
| Optimized slim + multi-stage   | ~100MB         | ✅ Production ready   |

---

## 🛠️ Testing Your Optimizations

### Check Image Size

```bash
# Build your image
docker build -t my-app .

# Check the size
docker images my-app

# See layer details
docker history my-app
```

### Measure Build Time

```bash
# Time your build
time docker build -t my-app .

# Build without cache to test from scratch
docker build --no-cache -t my-app .
```

---

## 🎯 Module 1 Focus

For Module 1, focus on these high-impact optimizations:

1. **Use `python:3.11-slim`** - Instant 7x size reduction
2. **Create .dockerignore** - Exclude unnecessary files
3. **Proper layering** - Copy requirements first
4. **Non-root user** - Basic security
5. **Environment variables** - Python optimization

These simple changes will give you 80% of the optimization benefits with minimal complexity.

---

## 📖 Next Steps

Once you've mastered these basics in Module 1:

- **Module 2**: Development environment optimization
- **Module 3**: Code quality and linting in containers
- **Module 4**: CI/CD pipeline optimization
- **Module 5**: Production deployment optimization

---

**💡 Remember**: Start with these fundamentals. Advanced optimizations like multi-stage builds are covered in later modules when you have more context.
