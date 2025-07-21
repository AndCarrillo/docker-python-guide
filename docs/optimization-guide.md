# ⚡ Container Optimization Guide

Performance optimization techniques for Python containers in development and production.

## 🎯 Overview

Container optimization focuses on reducing image size, improving build times, and enhancing runtime performance. This guide covers practical optimization strategies for Python applications.

## 📋 Table of Contents

- [Image Size Optimization](#-image-size-optimization)
- [Build Performance](#-build-performance)
- [Runtime Performance](#-runtime-performance)
- [Python-Specific Optimizations](#-python-specific-optimizations)
- [Multi-Stage Builds](#-multi-stage-builds)
- [Caching Strategies](#-caching-strategies)
- [Monitoring & Profiling](#-monitoring--profiling)
- [Optimization Checklist](#-optimization-checklist)

---

## 📦 Image Size Optimization

### Base Image Selection

```dockerfile
# 📊 Image size comparison:
# python:3.11            (~900MB)
# python:3.11-slim       (~120MB)
# python:3.11-alpine     (~50MB)

# ✅ Use slim for most applications
FROM python:3.11-slim

# ✅ Use alpine for size-critical applications
FROM python:3.11-alpine

# ❌ Avoid full images in production
FROM python:3.11  # Too large for production
```

### Layer Optimization

```dockerfile
# ❌ Multiple layers, inefficient
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN rm -rf /var/lib/apt/lists/*

# ✅ Single layer, efficient
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean
```

### Package Management

```dockerfile
# ✅ Install only runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary=all -r requirements.txt

# ✅ Remove build dependencies
FROM python:3.11-slim as builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
```

### File Exclusion

```dockerignore
# .dockerignore - Exclude unnecessary files
**/.git
**/.gitignore
**/README.md
**/Dockerfile*
**/docker-compose*
**/.dockerignore
**/.pytest_cache
**/__pycache__
**/*.pyc
**/*.pyo
**/*.pyd
**/.coverage
**/htmlcov
**/node_modules
**/.vscode
**/.idea
**/tests
**/test_*
**/*_test.py
```

---

## 🚀 Build Performance

### Dependency Caching

```dockerfile
# ✅ Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code after dependencies
COPY . .

# ❌ Poor caching - dependencies reinstall on every code change
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
```

### Build-Time Variables

```dockerfile
# ✅ Use build arguments for flexibility
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ARG BUILD_ENV=production
ENV BUILD_ENV=${BUILD_ENV}

# Conditional installations based on environment
RUN if [ "$BUILD_ENV" = "development" ]; then \
        pip install --no-cache-dir pytest pytest-cov black flake8; \
    fi
```

### Parallel Builds

```bash
# ✅ Use BuildKit for parallel builds
DOCKER_BUILDKIT=1 docker build .

# ✅ Enable experimental features for better performance
export DOCKER_CLI_EXPERIMENTAL=enabled
```

---

## ⚡ Runtime Performance

### Python Runtime Optimization

```dockerfile
# ✅ Python optimization flags
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random
ENV PYTHONOPTIMIZE=1

# ✅ Disable Python development features
ENV PYTHONDEBUG=0
ENV PYTHONPROFILEIMPORTTIME=0
```

### Memory Management

```dockerfile
# ✅ Set memory limits
ENV MALLOC_TRIM_THRESHOLD_=131072
ENV MALLOC_MMAP_THRESHOLD_=131072
ENV MALLOC_MMAP_MAX_=65536

# ✅ Python memory optimization
ENV PYTHONMALLOC=malloc
```

### Process Management

```python
# ✅ Gunicorn production configuration
# gunicorn_config.py
import multiprocessing

# Performance settings
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# Optimization settings
preload_app = True
worker_tmp_dir = "/dev/shm"
keepalive = 5

# Monitoring
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

```dockerfile
# ✅ Use optimized WSGI server
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
```

---

## 🐍 Python-Specific Optimizations

### Import Optimization

```python
# ✅ Optimize imports for faster startup
import sys
import importlib

# Lazy loading for optional dependencies
def get_redis_client():
    """Lazy load Redis client only when needed."""
    if 'redis' not in sys.modules:
        import redis
    return redis.Redis()

# ✅ Use importlib for conditional imports
def load_feature_module(feature_name):
    """Dynamically load feature modules."""
    try:
        return importlib.import_module(f'features.{feature_name}')
    except ImportError:
        return None
```

### Bytecode Compilation

```dockerfile
# ✅ Pre-compile Python bytecode
RUN python -m compileall -f /app

# ✅ Optimize Python bytecode
RUN python -O -m compileall -f /app
```

### Virtual Environment Optimization

```dockerfile
# ✅ Use virtual environment in container
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies in virtual environment
RUN pip install --no-cache-dir -r requirements.txt
```

---

## 🏗️ Multi-Stage Builds

### Development and Production

```dockerfile
# ===== BASE STAGE =====
FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ===== BUILDER STAGE =====
FROM base as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# ===== DEVELOPMENT STAGE =====
FROM builder as development

# Install development dependencies
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Install application in development mode
COPY . .
RUN pip install -e .

CMD ["python", "-m", "flask", "--app", "app", "run", "--host", "0.0.0.0", "--debug"]

# ===== PRODUCTION STAGE =====
FROM base as production

# Create non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser

# Install runtime dependencies only
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links /wheels -r requirements.txt \
    && rm -rf /wheels

# Copy application
COPY --chown=appuser:appuser . .

USER appuser

# Use production WSGI server
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]

# ===== TESTING STAGE =====
FROM development as testing

# Run tests during build
RUN python -m pytest tests/ --cov=app --cov-report=term-missing

# This stage won't be included in final image unless specifically targeted
```

### Build Target Selection

```bash
# ✅ Build specific stages
docker build --target development -t myapp:dev .
docker build --target production -t myapp:prod .
docker build --target testing -t myapp:test .
```

---

## 💾 Caching Strategies

### Docker Layer Caching

```dockerfile
# ✅ Optimize layer order for caching
FROM python:3.11-slim

# System packages (rarely change)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies (change occasionally)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code (changes frequently)
COPY . .
```

### Build Cache Management

```bash
# ✅ Use cache mount for pip (BuildKit)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# ✅ Cache apt packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y curl
```

### Multi-Platform Caching

```dockerfile
# ✅ Platform-specific optimizations
FROM --platform=$BUILDPLATFORM python:3.11-slim

ARG TARGETPLATFORM
RUN echo "Building for $TARGETPLATFORM"

# Use platform-specific optimizations
RUN if [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
        echo "ARM64 optimizations"; \
    elif [ "$TARGETPLATFORM" = "linux/amd64" ]; then \
        echo "AMD64 optimizations"; \
    fi
```

---

## 📊 Monitoring & Profiling

### Performance Metrics

```python
# ✅ Add performance monitoring
import time
import psutil
from flask import Flask, g, request
from prometheus_client import Counter, Histogram, Gauge, start_http_server

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('app_request_duration_seconds', 'Request latency')
MEMORY_USAGE = Gauge('app_memory_usage_bytes', 'Memory usage')
CPU_USAGE = Gauge('app_cpu_usage_percent', 'CPU usage')

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    # Record metrics
    duration = time.time() - g.start_time
    REQUEST_LATENCY.observe(duration)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint,
        status=response.status_code
    ).inc()

    # Update system metrics
    MEMORY_USAGE.set(psutil.virtual_memory().used)
    CPU_USAGE.set(psutil.cpu_percent())

    return response

# Start metrics server
start_http_server(8001)
```

### Health Checks

```python
# ✅ Optimized health check
from flask import jsonify
import time

@app.route('/health')
def health_check():
    """Lightweight health check."""
    return jsonify({
        'status': 'healthy',
        'timestamp': int(time.time())
    }), 200

@app.route('/health/ready')
def readiness_check():
    """Check if application is ready to serve traffic."""
    # Quick dependency checks
    try:
        # Test database connection (with timeout)
        # Test external services (with timeout)
        return jsonify({'status': 'ready'}), 200
    except Exception as e:
        return jsonify({'status': 'not ready', 'error': str(e)}), 503
```

```dockerfile
# ✅ Efficient health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Resource Monitoring

```yaml
# docker-compose.yml - ✅ Resource monitoring
version: "3.8"
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"
        reservations:
          memory: 256M
          cpus: "0.5"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
```

---

## 🧪 Performance Testing

### Load Testing

```python
# ✅ Load testing with locust
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def index_page(self):
        self.client.get("/")

    @task(1)
    def health_check(self):
        self.client.get("/health")

    def on_start(self):
        """Setup for each simulated user."""
        pass
```

### Memory Profiling

```python
# ✅ Memory profiling
import tracemalloc
from memory_profiler import profile

# Enable tracemalloc for production monitoring
tracemalloc.start()

@profile
def memory_intensive_function():
    """Function to profile memory usage."""
    # Your code here
    pass

# Get memory usage snapshots
def get_memory_usage():
    """Get current memory usage."""
    current, peak = tracemalloc.get_traced_memory()
    return {
        'current': current / 1024 / 1024,  # MB
        'peak': peak / 1024 / 1024  # MB
    }
```

---

## 📈 Optimization Checklist

### Image Optimization

- [ ] **Base Image**

  - [ ] Use appropriate base image (slim/alpine)
  - [ ] Pin specific versions
  - [ ] Regular base image updates

- [ ] **Layer Efficiency**

  - [ ] Minimize layer count
  - [ ] Optimize layer order for caching
  - [ ] Remove unnecessary files

- [ ] **Size Reduction**
  - [ ] Use .dockerignore
  - [ ] Remove build dependencies
  - [ ] Use multi-stage builds

### Build Optimization

- [ ] **Caching**

  - [ ] Optimize dependency caching
  - [ ] Use BuildKit features
  - [ ] Implement cache mounts

- [ ] **Build Speed**
  - [ ] Parallel builds when possible
  - [ ] Minimize context size
  - [ ] Use build arguments effectively

### Runtime Optimization

- [ ] **Python Configuration**

  - [ ] Set optimization flags
  - [ ] Configure memory management
  - [ ] Use appropriate WSGI server

- [ ] **Resource Management**

  - [ ] Set resource limits
  - [ ] Configure process management
  - [ ] Implement health checks

- [ ] **Monitoring**
  - [ ] Application metrics
  - [ ] Resource monitoring
  - [ ] Performance profiling

### Production Readiness

- [ ] **Performance**

  - [ ] Load testing completed
  - [ ] Memory profiling done
  - [ ] Resource limits tested

- [ ] **Monitoring**
  - [ ] Metrics collection
  - [ ] Health check endpoints
  - [ ] Logging configuration

---

## 🛠️ Tools & Commands

### Optimization Tools

```bash
# ✅ Analyze image layers
docker history your-app:latest

# ✅ Check image size
docker images your-app

# ✅ Analyze with dive
dive your-app:latest

# ✅ Profile with docker stats
docker stats container-name

# ✅ Memory analysis
docker exec container-name cat /proc/meminfo
```

### Build Performance

```bash
# ✅ Build with cache info
DOCKER_BUILDKIT=1 docker build --progress=plain .

# ✅ Build without cache
docker build --no-cache .

# ✅ Prune build cache
docker builder prune
```

### Runtime Analysis

```bash
# ✅ Check container processes
docker exec container-name ps aux

# ✅ Check resource usage
docker exec container-name cat /proc/cpuinfo
docker exec container-name free -h

# ✅ Profile application
docker exec container-name python -m cProfile app.py
```

---

## 📋 Performance Benchmarks

### Image Size Targets

| Application Type | Target Size | Good Size | Acceptable Size |
| ---------------- | ----------- | --------- | --------------- |
| Microservice     | < 100MB     | < 200MB   | < 500MB         |
| Web Application  | < 200MB     | < 400MB   | < 800MB         |
| Data Processing  | < 300MB     | < 600MB   | < 1GB           |

### Build Time Targets

| Build Stage  | Target Time | Good Time | Review Needed |
| ------------ | ----------- | --------- | ------------- |
| Dependencies | < 2 min     | < 5 min   | > 10 min      |
| Application  | < 30 sec    | < 1 min   | > 3 min       |
| Total Build  | < 3 min     | < 6 min   | > 15 min      |

### Runtime Performance

| Metric        | Target  | Good     | Review Needed |
| ------------- | ------- | -------- | ------------- |
| Startup Time  | < 5 sec | < 10 sec | > 30 sec      |
| Memory Usage  | < 100MB | < 200MB  | > 500MB       |
| Response Time | < 100ms | < 500ms  | > 2s          |

---

**⚡ Remember**: Optimization is about balance. Don't sacrifice maintainability or security for marginal performance gains.

**📖 Next Steps**: Review [Module 1 README](../README.md) to practice these optimizations in the exercises.
