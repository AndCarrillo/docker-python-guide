# Containerize your app

> **Module branch:** `module-01-containerize`

Learn how to containerize a Python application.

## What you'll learn

In this module, you will:

- ✅ Create optimized Dockerfiles for Python applications
- ✅ Implement security best practices and non-root users
- ✅ Use multi-stage builds to reduce image size
- ✅ Configure health checks and monitoring

## Examples

This module includes two progressive examples:

### 🌶️ Flask Basic Example

**Location:** `examples/flask-basic/`

A simple Flask application that demonstrates the fundamental concepts of containerization.

### ⚡ FastAPI Modern Example

**Location:** `examples/fastapi-modern/`

An advanced FastAPI application that showcases multi-stage builds and production optimization.

## Prerequisites

Before starting this module, make sure you have:

- Docker Desktop installed and running
- Python 3.9+ installed
- Basic understanding of Python and web frameworks

## Getting Started

1. **Clone and switch to this module:**

   ```bash
   git clone https://github.com/AndCarrillo/docker-python-guide.git
   cd docker-python-guide
   git checkout module-01-containerize
   ```

2. **Follow the step-by-step guide below** ⬇️

---

## 📚 Step-by-Step Guide

### Step 1: Understanding Python Base Images

Before creating a Dockerfile, you need to choose the right Python base image. Docker offers several options:

- **`python:3.11-slim`** - Recommended for most applications (smaller size)
- **`python:3.11`** - Full featured but larger
- **`python:3.11-alpine`** - Smallest but may have compatibility issues

**Best Practice:** Use `python:3.11-slim` for a good balance of size and compatibility.

### Step 2: Basic Dockerfile Structure

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

# 6. Expose port
EXPOSE 5000

# 7. Define startup command
CMD ["python", "app.py"]
```

### Step 3: Security Best Practices

Always implement these security measures:

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

### Step 4: Multi-stage Builds

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
CMD ["python", "app.py"]
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
