# Flask Basic Example

This example demonstrates the fundamental concepts of containerizing a simple Flask application.

## What you'll learn

- Basic Dockerfile structure for Python applications
- Security best practices with non-root users
- Health checks implementation
- Environment variables handling
- Docker build optimization

## Application Structure

```
flask-basic/
├── app.py              # Simple Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
├── .dockerignore      # Files to exclude from build
└── README.md          # This file
```

└── README.md # This file

````

## 🚀 Quick Start

### 1. Build the Docker Image

```bash
# Navigate to the example directory
cd examples/flask-basic

# Build the Docker image
docker build -t flask-basic-app .
````

### 2. Run the Container

```bash
# Run the container on port 5000
docker run -p 5000:5000 flask-basic-app
```

### 3. Test the Application

Open your browser or use curl to test:

```bash
# Main endpoint
curl http://localhost:5000

# Health check endpoint
curl http://localhost:5000/health
```

**Expected output:**

```json
{
  "message": "Hello from Dockerized Flask!",
  "environment": "development",
  "version": "1.0.0"
}
```

## 🔍 Understanding the Dockerfile

Let's break down each section of the Dockerfile:

### Base Image Selection

```dockerfile
FROM python:3.11-slim
```

- Uses **Python 3.11 slim** for smaller image size
- Slim images exclude unnecessary packages
- Good balance between functionality and size

### Working Directory

```dockerfile
WORKDIR /app
```

- Sets `/app` as the working directory
- All subsequent commands run from this directory

### Dependency Installation

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

- **Copy requirements first** for better layer caching
- `--no-cache-dir` reduces image size
- If requirements don't change, this layer is cached

### Application Code

```dockerfile
COPY app.py .
```

- Copy application code after dependencies
- Changes to code don't invalidate dependency cache

### Security Configuration

```dockerfile
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser
```

- Creates **non-root user** for security
- Changes ownership of app directory
- Runs container as non-root user

### Port and Health Check

```dockerfile
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1
```

- **Exposes port 5000** for documentation
- **Health check** monitors application status
- Docker can restart unhealthy containers

## 📊 Image Analysis

After building, analyze your image:

```bash
# Check image size
docker images flask-basic-app

# Inspect image layers
docker history flask-basic-app

# Scan for vulnerabilities (if you have docker scan)
docker scan flask-basic-app
```

## 🔧 Customization Options

### Environment Variables

Run with custom environment:

```bash
docker run -p 5000:5000 -e ENVIRONMENT=production flask-basic-app
```

### Development Mode

For development with code mounting:

```bash
# Mount current directory for live editing
docker run -p 5000:5000 -v $(pwd):/app flask-basic-app
```

### Custom Port

Run on a different port:

```bash
docker run -p 8080:5000 flask-basic-app
# Access at http://localhost:8080
```

## 🎯 Learning Points

This example demonstrates:

### ✅ Docker Fundamentals

- **Layer caching** optimization
- **Multi-step builds** basics
- **Port mapping** concepts

### ✅ Security Best Practices

- **Non-root user** execution
- **Minimal base images**
- **Proper file permissions**

### ✅ Python-Specific Patterns

- **Requirements management**
- **Application structure**
- **Environment configuration**

### ✅ Production Readiness

- **Health checks** implementation
- **Proper logging** setup
- **Graceful shutdown** preparation

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check container logs
docker logs <container-id>

# Run interactively for debugging
docker run -it flask-basic-app bash
```

### Port Already in Use

```bash
# Use different port
docker run -p 5001:5000 flask-basic-app
```

### Permission Issues

```bash
# Check if running as non-root
docker exec <container-id> whoami
# Should output: appuser
```

## 📈 Next Steps

After mastering this basic example:

1. **Try the advanced examples:**

   - [FastAPI Advanced](../fastapi-advanced/) - Multi-stage builds
   - [Django Production](../django-production/) - Full production setup

2. **Complete the exercises:**

   - [Exercise 1](../../exercises/01-basic-dockerfile/) - Build your own
   - [Exercise 2](../../exercises/02-multistage-build/) - Optimize further

3. **Explore optimizations:**
   - Reduce image size further
   - Add monitoring capabilities
   - Implement proper logging

## 🔗 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Python Docker Guide](https://docs.docker.com/language/python/)

---

**📊 Image Size:** ~150MB  
**🔧 Build Time:** ~2 minutes  
**🎯 Difficulty:** Beginner
