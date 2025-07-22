# Module 1: Containerization Fundamentals

> **Module branch:** `module-01-containerize`

Learn how to containerize a simple Python Flask application using Docker. This module focuses on the fundamentals of containerization.

## Prerequisites

Before starting this module, make sure you have:

- ✅ **Docker Desktop** - [Install Docker Desktop](https://docs.docker.com/get-docker/)
- ✅ **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- ✅ **Git client** - Command-line or GUI client
- ✅ **Code Editor** - [VS Code](https://code.visualstudio.com/) (recommended)

## What You'll Learn

In this module, you will:

- 🐳 Create a simple Flask application
- 📦 Write a basic Dockerfile
- �️ Build your first Docker image
- 🚀 Run your containerized application
- 🔍 Understand Docker fundamentals

**Time Required:** ~30 minutes

## Getting Started

Clone the repository and switch to this module:

```bash
git clone https://github.com/AndCarrillo/docker-python-guide.git
cd docker-python-guide
git checkout module-01-containerize
```

---

# 🌱 Flask Containerization Tutorial

### What you'll build

A simple Flask web application that returns "Hello from Docker! 🐳"

### Step 1: Navigate to Flask Example

```bash
cd examples/flask-basic
ls -la
# You'll see: app.py, requirements.txt, Dockerfile
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

**Congratulations! You've successfully containerized your first Python application!**

**What you learned:**
- ✅ Created a simple Flask application
- ✅ Written a basic Dockerfile
- ✅ Built your first Docker image
- ✅ Run a containerized application

**Continue your Docker journey:**

| Next Step           | Description                    | Link                                                       |
| ------------------- | ------------------------------ | ---------------------------------------------------------- |
| 🚀 **Next Module** | Learn development with Docker  | [Module 2: Develop](../../tree/module-02-develop)         |
| 📚 **Resources**    | Docker documentation          | [Docker Docs](https://docs.docker.com)                   |

---

## 📚 Additional Resources

| Type                   | Description                        | Link                                                        |
| ---------------------- | ---------------------------------- | ----------------------------------------------------------- |
| 🐳 **Official Docs**   | Docker Hub Python Images           | [hub.docker.com/\_/python](https://hub.docker.com/_/python) |
| 📘 **References**      | Dockerfile documentation           | [docs.docker.com](https://docs.docker.com)                  |

---

## 🐳 Docker Commands Reference

```bash
# Essential commands used in this module
docker build -t flask-basic .        # Build image
docker run -p 5000:5000 flask-basic  # Run container
docker images                        # List images
docker ps                           # List running containers
docker logs <container-name>        # View logs
docker stop <container-name>        # Stop container
```

---

## 🆘 Troubleshooting

**Common issues and solutions:**

**Port already in use:**
```bash
# Find what's using the port
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # macOS/Linux

# Use a different port
docker run -p 5001:5000 flask-basic
```

**Build fails:**
- Check that Docker Desktop is running
- Ensure `requirements.txt` exists in the same directory
- Verify all file names are correct in the Dockerfile

**Container won't start:**
- Check logs: `docker logs <container-name>`
- Ensure your app runs locally first: `python app.py`

---

## 🚀 Next Module

Ready to set up a development environment with Docker?

**[Module 2: Development Setup](../../tree/module-02-develop)**

Learn how to:
- Use Docker Compose for development
- Set up hot reload
- Work with databases in containers
- Debug containerized applications

---

## 🤝 Need Help?

- 📖 Check the [main README](../../README.md) for general guidance
- 💬 Open an issue if you encounter problems
