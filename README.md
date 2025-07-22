# Module 1: Containerize your app

> **Module branch:** `module-01-containerize`

Learn how to containerize a Python application using Docker with practical Flask and FastAPI examples.

## Prerequisites

Before starting this module, make sure you have:

- ✅ **Docker Desktop** - [Install Docker Desktop](https://docs.docker.com/get-docker/)
- ✅ **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- ✅ **Git client** - Command-line or GUI client
- ✅ **Code Editor** - [VS Code](https://code.visualstudio.com/) (recommended)

## Overview

This module teaches you containerization fundamentals using **two separate paths**. Choose the one that matches your experience level:

## 🌱 Choose Your Learning Path

### Path A: Flask Basic (Recommended for beginners)
Perfect for learning Docker fundamentals with a simple web framework.

### Path B: FastAPI Modern (For those comfortable with async Python)
Learn advanced containerization patterns with modern async framework.

## What you'll learn

In this module, you will:

- ✅ **Initialize Docker assets** using `docker init` and manual methods
- ✅ **Create optimized Dockerfiles** for Python applications
- ✅ **Implement security best practices** with non-root users
- ✅ **Configure health checks** and monitoring
- ✅ **Run applications** with Docker and Docker Compose

## Getting Started

Clone the repository and switch to this module:

```bash
git clone https://github.com/AndCarrillo/docker-python-guide.git
cd docker-python-guide
git checkout module-01-containerize
```

---

# 🌱 Path A: Flask Basic (Start Here)

**Recommended for**: Docker beginners, those new to containerization

### What you'll build
A simple Flask web application with health checks and basic API endpoints.

### Step 1: Navigate to Flask Example

```bash
cd examples/flask-basic
ls -la
# You'll see: app.py, requirements.txt, Dockerfile, .dockerignore
```

### Step 2: Understand the Application

Let's look at what we're containerizing:

**app.py** - Simple Flask application:
```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Hello from Flask in Docker!",
        "status": "running"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### Step 3A: Create Docker Assets (Automatic)

**Option 1: Use Docker Init** (Recommended for beginners)

```bash
docker init
```

Answer the prompts:
- Platform: **Python**
- Python version: **3.11**
- Port: **5000**
- Run command: **python3 app.py**

### Step 3B: Create Docker Assets (Manual)

**Option 2: Create manually** (Better for learning)

Create these files in the `examples/flask-basic` directory:

**Create a file named `Dockerfile`:**

```dockerfile
FROM python:3.11-slim

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser

# Copy and install dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

**Create a file named `.dockerignore`:**

```dockerignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
venv/

# Development
.git/
.gitignore
*.md
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

### Step 4: Build and Run Flask App

**Build the image:**

```bash
docker build -t flask-basic .
```

**Run the container:**

```bash
docker run -p 5000:5000 flask-basic
```

**Test your application:**
- Open http://localhost:5000 in your browser
- Check health: http://localhost:5000/health

**Stop the container:** Press `Ctrl+C`

### Step 5: Run with Docker Compose (Recommended)

**Create `compose.yaml`:**

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
```

**Run with compose:**

```bash
docker compose up --build
```

### ✅ Flask Path Complete!

You've successfully containerized a Flask application! You learned:

- ✅ Basic Dockerfile structure
- ✅ Security with non-root user  
- ✅ Docker build and run commands
- ✅ Docker Compose basics

**Ready for more?** Continue to [Path B: FastAPI Modern](#-path-b-fastapi-modern-advanced) or jump to [Key Takeaways](#-key-takeaways).

---

# ⚡ Path B: FastAPI Modern (Advanced)

**Recommended for**: Those comfortable with async Python, after completing Path A

### What you'll build
A modern FastAPI application with multi-stage builds, advanced optimization, and production patterns.

### Step 1: Navigate to FastAPI Example

```bash
cd examples/fastapi-modern
ls -la
# You'll see: main.py, requirements.txt, Dockerfile, .dockerignore
```

### Step 2: Understand the Application

**main.py** - FastAPI with async patterns:
```python
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

app = FastAPI(title="Task Manager", version="1.0.0")

# Sample data store
tasks = []

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI in Docker!", "tasks_count": len(tasks)}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "task-manager"}

@app.post("/tasks")
async def create_task(task: dict):
    task_id = len(tasks) + 1
    new_task = {"id": task_id, **task}
    tasks.append(new_task)
    return new_task
```

### Step 3: Create Advanced Docker Assets

**Create `Dockerfile` (Multi-stage):**

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY --chown=appuser:appuser . .

USER appuser
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 4: Build and Run FastAPI App

**Build the image:**

```bash
docker build -t fastapi-modern .
```

**Run the container:**

```bash
docker run -p 8000:8000 fastapi-modern
```

**Test your application:**
- Open http://localhost:8000 in your browser
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Step 5: Advanced Docker Compose

**Create `compose.yaml`:**

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

**Run with compose:**

```bash
docker compose up --build
```

### ✅ FastAPI Path Complete!

You've mastered advanced containerization! You learned:

- ✅ Multi-stage builds for optimization
- ✅ Health checks and monitoring  
- ✅ Production-ready patterns
- ✅ Advanced Docker Compose configurations

---

# 🎯 Key Takeaways

After completing this module, you should understand:

1. **Base Image Selection** - How to choose the right Python base image (`python:3.11-slim`)
2. **Dockerfile Structure** - Layer optimization, security practices, and best patterns
3. **Security Basics** - Running as non-root user and excluding sensitive files
4. **Container Operations** - Building, running, and managing containers
5. **Docker Compose** - Multi-service orchestration and environment management

## 🔍 Understanding Docker Assets

### Essential Files You Created

**Dockerfile** - Instructions for building your container:
- Base image selection
- Dependencies installation  
- Security configuration (non-root user)
- Application setup

**.dockerignore** - Files to exclude from build context:
- Development files (`__pycache__`, `.venv`)
- Version control (`.git`)
- Documentation (`*.md`)

**compose.yaml** - Multi-container orchestration:
- Service definitions
- Port mapping
- Environment variables
- Health checks

### Docker Commands You Learned

```bash
# Build an image
docker build -t my-app .

# Run a container
docker run -p 5000:5000 my-app

# Use Docker Compose (recommended)
docker compose up --build
docker compose up -d          # Run in background
docker compose down           # Stop services

# Useful commands
docker images                 # List images
docker ps                     # List running containers
docker logs <container-name>  # View logs
```

## 📚 Additional Resources

**For deeper learning:**

- 📖 [Dockerfile Best Practices Guide](docs/dockerfile-guide.md) - Advanced Dockerfile patterns
- 🔒 [Container Security Basics](docs/security-guide.md) - Security fundamentals  
- ⚡ [Container Optimization Guide](docs/optimization-guide.md) - Performance tips

**Official Documentation:**
- [Docker Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/best-practices/)

## 🆘 Troubleshooting

**Common issues and solutions:**

**Port already in use:**
```bash
# Find what's using the port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Use a different port
docker run -p 5001:5000 my-app
```

**Permission denied:**
```bash
# Make sure Docker is running
docker version

# On Linux, add user to docker group
sudo usermod -aG docker $USER
```

**Build fails:**
```bash
# Check Dockerfile syntax
# Ensure requirements.txt exists
# Verify file paths in COPY commands
```

## 🚀 Next Steps

Ready for the next module?

**[Module 2: Develop your app](../../tree/module-02-develop)** 
- Development environment with containers
- Code quality and debugging
- Hot reload and development workflows

---

## 🤝 Need Help?

- 📖 Check the [main README](../../README.md) for general guidance
- 🐛 [Open an issue](../../issues) if you find problems
- 💬 [Start a discussion](../../discussions) for questions

---

**⬅️ [Back to main guide](../../README.md)**

### Understanding Docker Assets

#### Dockerfile Structure

A Python Dockerfile typically follows this structure:

```dockerfile
# 1. Choose base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements first (for better caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

# 6. Create non-root user (security)
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# 7. Expose port
EXPOSE 8000

# 8. Define startup command
CMD ["python3", "-m", "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
```

#### Base Image Selection

- **`python:3.11-slim`** - Recommended for most applications (smaller size)
- **`python:3.11`** - Full featured but larger
- **`python:3.11-alpine`** - Smallest but may have compatibility issues

**Best Practice:** Use `python:3.11-slim` for a good balance of size and compatibility.

#### .dockerignore Best Practices

```dockerignore
# Version control
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
.venv/
venv/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Documentation
*.md
!README.md

# Testing
.pytest_cache
.coverage
htmlcov/

# Development
.env.local
.env.development
```

### Security Best Practices

1. **Run as non-root user:**

   ```dockerfile
   RUN adduser --disabled-password --gecos '' appuser
   USER appuser
   ```

2. **Use specific versions:**

   ```dockerfile
   FROM python:3.11-slim
   # Not: FROM python:latest
   ```

3. **Minimize attack surface:**
   ```dockerfile
   RUN apt-get update && apt-get install -y --no-install-recommends \
       && rm -rf /var/lib/apt/lists/*
   ```

### Multi-stage Builds

For production applications, use multi-stage builds to reduce image size:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["python", "main.py"]
```

---

## 🧩 Examples

### Flask Basic Example

**Purpose:** Learn containerization fundamentals with a simple Flask application.

**Key concepts:**

- Basic Dockerfile structure
- Security with non-root user
- Health checks
- Environment variables

**Files:**

```
examples/flask-basic/
├── app.py              # Simple Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Basic containerization
├── .dockerignore      # Files to exclude
└── README.md          # Example instructions
```

**Try it:**

```bash
cd examples/flask-basic
docker build -t flask-basic .
docker run -p 5000:5000 flask-basic
# Visit http://localhost:5000
```

### FastAPI Modern Example

**Purpose:** Advanced containerization with multi-stage builds and production optimization.

**Key concepts:**

- Multi-stage builds
- Production optimizations
- Health checks and monitoring
- Async application patterns

**Files:**

```
examples/fastapi-modern/
├── main.py            # FastAPI application with async endpoints
├── requirements.txt   # Production dependencies
├── Dockerfile        # Multi-stage build
├── .dockerignore     # Optimized exclusions
└── README.md         # Advanced instructions
```

**Try it:**

```bash
cd examples/fastapi-modern
docker build -t fastapi-modern .
docker run -p 8000:8000 fastapi-modern
# Visit http://localhost:8000/docs
```

---

## 🎯 Key Takeaways

After completing this module, you should understand:

1. **Base Image Selection** - How to choose the right Python base image
2. **Dockerfile Best Practices** - Security, optimization, and maintainability
3. **Multi-stage Builds** - Reducing production image size
4. **Security** - Running as non-root, minimal attack surface
5. **Health Checks** - Monitoring container health

## � Next Steps

Ready for the next module? Continue with:

**[Module 2: Develop your app](../../tree/module-02-develop)** - Learn how to set up a local development environment with containers.

---

## 📚 Additional Resources

- [Docker Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/best-practices/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Multi-stage Builds](https://docs.docker.com/develop/dev-best-practices/)

---

## 🤝 Need Help?

- 📖 Check the [main README](../../README.md) for general guidance
- � [Open an issue](../../issues) if you find problems
- � [Start a discussion](../../discussions) for questions

---

**⬅️ [Back to main guide](../../README.md)**
