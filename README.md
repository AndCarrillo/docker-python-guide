# 🐳 Docker Python Guide - PROJECT COMPLETE 🎯

> **📍 Esta es la rama `project-complete`** - Contiene el proyecto final con todas las configuraciones Docker avanzadas y optimizaciones

Learn how to containerize a Python application using Docker with practical Flask and FastAPI examples.

## 🏆 Proyecto Completo

¡Felicitaciones! Has llegado a la rama del **proyecto completo**. Aquí encontrarás:

### ✅ Configuraciones Incluidas
- ✅ **Dockerfiles optimizados** para producción
- ✅ **Docker Compose** con servicios completos
- ✅ **Optimizaciones de seguridad** implementadas
- ✅ **Multi-stage builds** configurados
- ✅ **Redes Docker** para microservicios
- ✅ **Volúmenes persistentes** configurados
- ✅ **Variables de entorno** organizadas
- ✅ **Documentación completa** de mejores prácticas

### 🚀 Estado del Proyecto
Este proyecto incluye **todas las configuraciones Docker** desde básicas hasta avanzadas, listo para usar en:
- 🧪 **Desarrollo local**
- 🧪 **Testing automatizado**
- 🚀 **Despliegue en producción**

## Prerequisites

Before starting this module, make sure you have:

- ✅ **Docker Desktop** - [Install Docker Desktop](https://docs.docker.com/get-docker/)
- ✅ **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- ✅ **Git client** - Command-line or GUI client
- ✅ **Code Editor** - [VS Code](https://code.visualstudio.com/) (recommended)

## 🚀 Choose Your Framework

| Framework      | Description                                          | Difficulty   | Time    | Start Learning                                 |
| -------------- | ---------------------------------------------------- | ------------ | ------- | ---------------------------------------------- |
| 🌱 **Flask**   | Simple web framework, perfect for Docker beginners   | **Beginner** | ~30 min | [→ Start Flask Tutorial](#-flask-tutorial)     |
| ⚡ **FastAPI** | Modern async framework with advanced Docker patterns | **Advanced** | ~45 min | [→ Start FastAPI Tutorial](#-fastapi-tutorial) |

> **New to Docker?** → Choose Flask | **Have Docker experience?** → Choose FastAPI

## Getting Started

Clone the repository and switch to this module:

```bash
git clone https://github.com/AndCarrillo/docker-python-guide.git
cd docker-python-guide
git checkout module-01-containerize
```

---

# 🌱 Flask Tutorial

**Step-by-step containerization with Flask**

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

```bash
# Build and run
docker build -t flask-basic .
docker run -p 5000:5000 flask-basic

# Or use Docker Compose (recommended)
docker compose up --build
```

**Test your application:**

- Open http://localhost:5000 in your browser
- Check health: http://localhost:5000/health
- Stop: Press `Ctrl+C`

### ✅ Flask Tutorial Complete!

You've successfully containerized a Flask application!

**What you learned:**

- ✅ Basic Dockerfile structure and best practices
- ✅ Security with non-root user configuration
- ✅ Docker build and run commands
- ✅ Docker Compose for development

---

### 🎯 Next Steps

| Option             | Description               | Link                                                       |
| ------------------ | ------------------------- | ---------------------------------------------------------- |
| ⚡ **Try FastAPI** | Learn advanced patterns   | [→ FastAPI Tutorial](#-fastapi-tutorial)                   |
| 📚 **Deep Dive**   | Explore advanced concepts | [→ Additional Resources](#-additional-resources)           |
| 🚀 **Next Module** | Continue learning         | [Module 2: Develop your app](../../tree/module-02-develop) |

---

# ⚡ FastAPI Tutorial

**Advanced containerization with FastAPI**

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

```bash
# Build and run
docker build -t fastapi-modern .
docker run -p 8000:8000 fastapi-modern

# Or use Docker Compose (recommended)
docker compose up --build
```

**Test your application:**

- Open http://localhost:8000 in your browser
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Stop: Press `Ctrl+C`

### ✅ FastAPI Tutorial Complete!

You've mastered advanced containerization with FastAPI!

**What you learned:**

- ✅ Multi-stage builds for optimization and security
- ✅ Health checks and container monitoring
- ✅ Production-ready patterns and configurations
- ✅ Advanced Docker Compose with health checks

---

### 🎯 Next Steps

| Option             | Description               | Link                                                       |
| ------------------ | ------------------------- | ---------------------------------------------------------- |
| 🌱 **Try Flask**   | Learn the basics first    | [→ Flask Tutorial](#-flask-tutorial)                       |
| 📚 **Deep Dive**   | Explore advanced concepts | [→ Additional Resources](#-additional-resources)           |
| 🚀 **Next Module** | Continue learning         | [Module 2: Develop your app](../../tree/module-02-develop) |

---

## 📚 Additional Resources

| Type                   | Description                        | Link                                                        |
| ---------------------- | ---------------------------------- | ----------------------------------------------------------- |
| 📖 **Advanced Guides** | Dockerfile, Security, Optimization | [docs/](docs/)                                              |
| 🐳 **Official Docs**   | Docker Hub Python Images           | [hub.docker.com/\_/python](https://hub.docker.com/_/python) |
| 📘 **References**      | Dockerfile & Compose docs          | [docs.docker.com](https://docs.docker.com)                  |

---

## 🐳 Docker Commands Reference

```bash
# Build and run
docker build -t my-app .
docker run -p 5000:5000 my-app

# Docker Compose (recommended)
docker compose up --build
docker compose up -d          # Run in background
docker compose down           # Stop services

# Useful commands
docker images                 # List images
docker ps                     # List running containers
docker logs <container-name>  # View logs
```

---

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

---

## 🚀 Next Module

Ready to continue your Docker journey?

**[Module 2: Develop your app](../../tree/module-02-develop)**

- Development environment with containers
- Code quality and debugging
- Hot reload and development workflows

---

## 🤝 Need Help?

- 📖 Check the [main README](../../README.md) for general guidance
