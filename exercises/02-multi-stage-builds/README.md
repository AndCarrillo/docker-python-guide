# 🏗️ Exercise 2: Multi-Stage Docker Builds

Learn how to create optimized, secure, and efficient Docker images using multi-stage builds for a Python web application.

## 🎯 Learning Objectives

By completing this exercise, you will:

- Understand the benefits of multi-stage Docker builds
- Create separate stages for development and production
- Optimize image size and security
- Implement proper dependency management
- Configure different environments in a single Dockerfile

## 📋 Prerequisites

- Completed [Exercise 1: Basic Dockerfile](../01-basic-dockerfile/README.md)
- Docker Desktop installed and running
- Basic understanding of Python web applications
- Text editor or IDE

## 🚀 The Challenge

You'll containerize a Python web API using multi-stage builds to create optimized images for different environments while maintaining security and performance.

## 📁 Project Structure

```
02-multi-stage-builds/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # Data models
│   └── utils.py         # Utility functions
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── Dockerfile          # Your multi-stage Dockerfile (to create)
├── .dockerignore       # Build context optimization (to create)
└── README.md           # This file
```

## 📝 Your Task

### Step 1: Examine the Application

First, let's look at the provided Python application:

**File: `app/main.py`**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Task Manager API", version="1.0.0")

# In-memory storage (in production, use a real database)
tasks = []
task_counter = 0

class Task(BaseModel):
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: float

class TaskCreate(BaseModel):
    title: str
    description: str = ""

@app.get("/")
async def root():
    return {"message": "Task Manager API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    global task_counter
    task_counter += 1

    new_task = Task(
        id=task_counter,
        title=task.title,
        description=task.description,
        completed=False,
        created_at=time.time()
    )

    tasks.append(new_task)
    logger.info(f"Created task: {new_task.title}")
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskCreate):
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_update.title
    task.description = task_update.description
    logger.info(f"Updated task: {task_id}")
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    global tasks
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks = [t for t in tasks if t.id != task_id]
    logger.info(f"Deleted task: {task_id}")
    return {"message": "Task deleted"}

@app.put("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    logger.info(f"Completed task: {task_id}")
    return task

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 2: Create the Multi-Stage Dockerfile

Create a `Dockerfile` with the following stages:

#### Stage 1: Base Image

- Use Python 3.11-slim as base
- Set common environment variables
- Create working directory

#### Stage 2: Builder Stage

- Install build dependencies (gcc, etc.)
- Build Python wheels for dependencies
- This stage will be discarded in the final image

#### Stage 3: Development Stage

- Install all dependencies (including dev dependencies)
- Mount source code for live editing
- Use uvicorn with reload
- Include debugging tools

#### Stage 4: Production Stage

- Copy only production dependencies from builder
- Create non-root user
- Copy application code
- Use gunicorn for production
- Implement health checks

### Step 3: Create .dockerignore

Create a `.dockerignore` file to optimize build context:

```dockerignore
# Your .dockerignore content here
# Hint: Exclude development files, git, cache, etc.
```

### Step 4: Build and Test

Build different targets and test them:

```bash
# Build development image
docker build --target development -t task-api:dev .

# Build production image
docker build --target production -t task-api:prod .

# Test development version
docker run -p 8000:8000 task-api:dev

# Test production version
docker run -p 8000:8000 task-api:prod
```

## ✅ Requirements Checklist

Your Dockerfile should include:

### Base Requirements

- [ ] Multi-stage build with at least 3 stages (base, development, production)
- [ ] Use Python 3.11-slim as base image
- [ ] Set appropriate environment variables for Python optimization
- [ ] Create and use non-root user in production

### Builder Stage

- [ ] Install build dependencies (gcc, libc6-dev)
- [ ] Build Python wheels for all dependencies
- [ ] Clean up build dependencies after wheel creation

### Development Stage

- [ ] Install both production and development dependencies
- [ ] Configure for code hot-reloading
- [ ] Use uvicorn with reload flag
- [ ] Include development tools

### Production Stage

- [ ] Copy wheels from builder stage
- [ ] Install only production dependencies
- [ ] Remove build artifacts and cache
- [ ] Configure production WSGI server (gunicorn)
- [ ] Implement health check
- [ ] Use non-root user
- [ ] Expose only necessary port (8000)

### Security & Optimization

- [ ] No secrets or sensitive data in image
- [ ] Minimal attack surface (no unnecessary packages)
- [ ] Proper file permissions
- [ ] Optimized layer ordering for caching

## 🧪 Testing Your Solution

### 1. Build Size Comparison

```bash
# Check image sizes
docker images | grep task-api

# Compare with single-stage build
docker build -f Dockerfile.single-stage -t task-api:single .
docker images | grep task-api
```

Expected results:

- Development image: ~200-300MB
- Production image: ~150-200MB
- Single-stage image: ~400-500MB

### 2. Functionality Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Testing the API"}'

# Get all tasks
curl http://localhost:8000/tasks

# Complete a task
curl -X PUT http://localhost:8000/tasks/1/complete
```

### 3. Security Testing

```bash
# Check if running as non-root user
docker run --rm task-api:prod whoami

# Should output: appuser (not root)
```

### 4. Performance Testing

```bash
# Check startup time
time docker run --rm task-api:prod echo "Container started"

# Load test (if you have ab installed)
ab -n 100 -c 10 http://localhost:8000/health
```

## 🎯 Expected Outcomes

After completing this exercise:

1. **Optimized Images**: Production image significantly smaller than development
2. **Security**: Non-root user, minimal attack surface
3. **Flexibility**: Single Dockerfile for multiple environments
4. **Performance**: Fast build times due to layer caching
5. **Best Practices**: Clean separation of concerns between stages

## 🔍 Troubleshooting

### Common Issues

1. **Build fails at pip install**

   - Check if gcc is installed in builder stage
   - Verify requirements.txt exists and is valid

2. **Permission denied errors**

   - Ensure files are owned by the non-root user
   - Check file permissions (chmod commands)

3. **Large image size**

   - Verify .dockerignore excludes unnecessary files
   - Check if build dependencies are cleaned up
   - Ensure multi-stage build is working correctly

4. **Health check fails**
   - Verify curl is installed in production stage
   - Check if health endpoint responds correctly
   - Ensure port 8000 is accessible

### Debugging Commands

```bash
# Inspect image layers
docker history task-api:prod

# Check image content
docker run --rm -it task-api:prod /bin/bash

# View build logs
docker build --no-cache --progress=plain -t task-api:prod .
```

## 🏆 Bonus Challenges

If you complete the basic requirements, try these advanced features:

### 1. Testing Stage

Add a testing stage that:

- Runs pytest on the application
- Generates coverage reports
- Fails build if tests don't pass

### 2. Multi-Platform Build

Configure for multiple architectures:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t task-api:multi .
```

### 3. Build Arguments

Add build arguments for:

- Python version selection
- Environment-specific configurations
- Feature flags

### 4. Static Analysis

Add a stage that runs:

- Black for code formatting
- Flake8 for linting
- Bandit for security scanning

## 📖 Learning Resources

- [Docker Multi-Stage Builds Documentation](https://docs.docker.com/build/building/multi-stage/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Python Docker Best Practices](https://docs.python.org/3/using/docker.html)

## ✨ Solution Validation

Your solution is complete when:

- [ ] All build targets work correctly
- [ ] Production image is optimized and secure
- [ ] Development workflow supports hot reloading
- [ ] API responds correctly to all endpoints
- [ ] Health checks pass
- [ ] Non-root user is used in production
- [ ] Image size is reasonable for the application

**🎉 Congratulations!** You've mastered multi-stage Docker builds for Python applications. This technique is essential for creating production-ready containers that are both secure and efficient.

**➡️ Next Step**: Proceed to [Exercise 3: Security & Optimization](../03-security-optimization/README.md) to learn advanced security and performance techniques.
