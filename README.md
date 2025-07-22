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

This section walks you through containerizing and running Python applications using two complementary examples:

- **Flask Basic**: Simple containerization fundamentals
- **FastAPI Modern**: Advanced patterns with multi-stage builds

## What you'll learn

In this module, you will:

- ✅ **Initialize Docker assets** using `docker init` and manual methods
- ✅ **Create optimized Dockerfiles** for Python applications
- ✅ **Implement security best practices** with non-root users
- ✅ **Use multi-stage builds** to reduce image size
- ✅ **Configure health checks** and monitoring
- ✅ **Run applications** with Docker Compose

## Getting Started

Clone the repository and switch to this module:

```bash
git clone https://github.com/AndCarrillo/docker-python-guide.git
cd docker-python-guide
git checkout module-01-containerize
```

---

##  Step-by-Step Guide

### Step 1: Get the Sample Applications

We provide two complementary examples that demonstrate different containerization approaches:

#### Option A: Flask Basic Example

```bash
cd examples/flask-basic
ls -la
# You'll see: app.py, requirements.txt, Dockerfile, .dockerignore
```

#### Option B: FastAPI Modern Example

```bash
cd examples/fastapi-modern
ls -la
# You'll see: main.py, requirements.txt, Dockerfile, .dockerignore
```

### Step 2: Initialize Docker Assets

You have two approaches to create Docker assets:

#### 🔧 Use Docker Init (Recommended for beginners)

Inside either example directory, run:

```bash
docker init
```

Docker Init will ask you:

```
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

? What application platform does your project use? Python
? What version of Python do you want to use? 3.11
? What port do you want your app to listen on? 8000 (FastAPI) or 5000 (Flask)
? What is the command to run your app?
  # FastAPI: python3 -m uvicorn main:app --host=0.0.0.0 --port=8000
  # Flask: python3 app.py
```

#### ⚙️ Manually Create Assets (Recommended for learning)

If you don't have Docker Desktop installed or prefer creating the assets manually, you can create the following files in your project directory.

**Create a file named `Dockerfile` with the following contents:**

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["python3", "-m", "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
```

**Create a file named `compose.yaml` with the following contents:**

```yaml
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000
```

**Create a file named `.dockerignore` with the following contents:**

```dockerignore
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

**/.DS_Store
**/__pycache__
**/.venv
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/bin
**/charts
**/docker-compose*
**/compose.y*ml
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
LICENSE
README.md
```

**Create a file named `.gitignore` with the following contents:**

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

**Understanding the files:**

Our examples already include manually crafted Docker assets that demonstrate both basic and advanced approaches. Study them to understand the differences.

### Step 3: Build and Run

#### Using Docker Compose (Recommended)

For **Flask Basic** example:

```bash
cd examples/flask-basic
docker compose up --build
# Visit http://localhost:5000
```

For **FastAPI Modern** example:

```bash
cd examples/fastapi-modern
docker compose up --build
# Visit http://localhost:8000
# API docs: http://localhost:8000/docs
```

#### Using Docker Build + Run

Alternative approach:

```bash
# Build
docker build -t my-python-app .

# Run
docker run -p 8000:8000 my-python-app
```

### Step 4: Run in Background

Run the application detached from terminal:

```bash
docker compose up --build -d
```

To stop:

```bash
docker compose down
```

### Step 5: Understanding the Structure

After running docker init or examining our examples, you should have:

```
examples/flask-basic/          # or fastapi-modern/
├── app.py (main.py)          # Application code
├── requirements.txt          # Python dependencies
├── .dockerignore            # Files to exclude from build
├── .gitignore              # Git exclusions
├── Dockerfile              # Container instructions
├── compose.yaml            # Multi-container orchestration
└── README.md               # Example-specific guide
```

---

## 🔍 Technical Deep Dive

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

## � Hands-on Exercises

### Exercise 1: Basic Flask Container

1. Navigate to `examples/flask-basic/`
2. Examine the Dockerfile and understand each instruction
3. Build the image: `docker build -t my-flask-app .`
4. Run the container: `docker run -p 5000:5000 my-flask-app`
5. Test the application at http://localhost:5000

**Questions to explore:**

- What base image is used and why?
- How is the non-root user implemented?
- What files are excluded by .dockerignore?

### Exercise 2: FastAPI Multi-stage Build

1. Navigate to `examples/fastapi-modern/`
2. Study the multi-stage Dockerfile
3. Build the image: `docker build -t my-fastapi-app .`
4. Run the container: `docker run -p 8000:8000 my-fastapi-app`
5. Explore the automatic API docs at http://localhost:8000/docs

**Questions to explore:**

- How does the multi-stage build reduce image size?
- What production optimizations are implemented?
- How do health checks work?

### Exercise 3: Optimization Challenge

1. Compare the image sizes:
   ```bash
   docker images | grep flask-basic
   docker images | grep fastapi-modern
   ```
2. Try building without multi-stage build
3. Measure the difference in size and build time

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
