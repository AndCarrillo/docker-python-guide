# FastAPI Modern Example

> **Part of Module 1: Containerize your app**

This example demonstrates advanced containerization concepts with FastAPI, including multi-stage builds, security best practices, and production optimization.

## What you'll learn

- Multi-stage Docker builds for size optimization
- Security implementation with non-root users
- Health checks and monitoring
- Production-ready FastAPI deployment
- API documentation with OpenAPI/Swagger

## Application Overview

Simple FastAPI application with:

- **Root endpoint** (`/`) - Welcome message with environment info
- **Health check** (`/health`) - Container health monitoring
- **Info endpoint** (`/info`) - Application metadata
- **Auto-generated docs** (`/docs`) - Swagger UI documentation
- **ReDoc documentation** (`/redoc`) - Alternative API docs
  ├── gunicorn_config.py # Production server configuration
  ├── .dockerignore # Build context optimization
  └── README.md # This file

````

## 🚀 Quick Start

### 1. Build the Container

```bash
# Development build
docker build --target development -t fastapi-app:dev .

# Production build
docker build --target production -t fastapi-app:prod .
````

### 2. Run the Application

```bash
# Development mode (with auto-reload)
docker run -p 8000:8000 fastapi-app:dev

# Production mode (with Gunicorn)
docker run -p 8000:8000 fastapi-app:prod
```

### 3. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📖 API Endpoints

### Public Endpoints

| Method | Endpoint        | Description                       |
| ------ | --------------- | --------------------------------- |
| GET    | `/`             | Welcome message and API info      |
| GET    | `/health`       | Health check for monitoring       |
| GET    | `/health/ready` | Readiness check for orchestration |

### Protected Endpoints (Require Authentication)

| Method | Endpoint      | Description       |
| ------ | ------------- | ----------------- |
| GET    | `/users`      | Get all users     |
| POST   | `/users`      | Create a new user |
| GET    | `/users/{id}` | Get user by ID    |
| DELETE | `/users/{id}` | Delete user by ID |

### Testing Endpoints

| Method | Endpoint          | Description                 |
| ------ | ----------------- | --------------------------- |
| GET    | `/simulate-error` | Test error handling         |
| GET    | `/simulate-slow`  | Test performance monitoring |

## 🔐 Authentication

The API uses Bearer token authentication. Include the token in the Authorization header:

```bash
# Using curl
curl -H "Authorization: Bearer valid-token" http://localhost:8000/users

# Using httpie
http GET localhost:8000/users Authorization:"Bearer valid-token"
```

**Note**: For demo purposes, use `valid-token` as the bearer token.

## 🧪 Testing the API

### Create a User

```bash
curl -X POST http://localhost:8000/users \
  -H "Authorization: Bearer valid-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com"
  }'
```

### Get All Users

```bash
curl -H "Authorization: Bearer valid-token" http://localhost:8000/users
```

### Health Check

```bash
curl http://localhost:8000/health
```

## 🏭 Production Deployment

### Environment Variables

| Variable    | Default   | Description   |
| ----------- | --------- | ------------- |
| `HOST`      | `0.0.0.0` | Server host   |
| `PORT`      | `8000`    | Server port   |
| `LOG_LEVEL` | `info`    | Logging level |
| `DEBUG`     | `false`   | Debug mode    |

### Docker Compose Example

```yaml
version: "3.8"
services:
  fastapi-app:
    build:
      context: .
      target: production
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=info
      - DEBUG=false
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    restart: unless-stopped
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
        - name: fastapi-app
          image: fastapi-app:prod
          ports:
            - containerPort: 8000
          env:
            - name: LOG_LEVEL
              value: "info"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              memory: "128Mi"
              cpu: "250m"
            limits:
              memory: "256Mi"
              cpu: "500m"
```

## 🔧 Configuration

### Gunicorn Settings

The application uses Gunicorn with Uvicorn workers for production:

- **Workers**: Auto-calculated based on CPU cores (max 8)
- **Worker Class**: `uvicorn.workers.UvicornWorker`
- **Timeouts**: 30 seconds for all timeout settings
- **Preload**: App preloading enabled for better performance

### Security Features

- **CORS**: Configured for specific origins
- **Trusted Hosts**: Only allows specified hosts
- **Authentication**: Bearer token validation
- **Input Validation**: Pydantic models for request/response
- **Error Handling**: Structured error responses

## 📊 Monitoring

### Health Checks

- **Liveness**: `/health` - Basic app health
- **Readiness**: `/health/ready` - App ready to serve traffic

### Metrics

The application logs important events and can be extended with:

- Prometheus metrics
- Application Performance Monitoring (APM)
- Structured logging with correlation IDs

## 🛠️ Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Development with Docker

```bash
# Build development image
docker build --target development -t fastapi-app:dev .

# Run with volume mount for code changes
docker run -p 8000:8000 -v $(pwd):/app fastapi-app:dev
```

## 🔍 Container Optimizations

This example demonstrates:

- **Multi-stage builds**: Separate build and runtime stages
- **Non-root user**: Security best practice
- **Layer caching**: Optimized Dockerfile layer order
- **Minimal base image**: Using Python slim image
- **Security scanning**: Base image vulnerability awareness
- **Resource limits**: Production-ready resource configuration

## 📚 Learning Objectives

After studying this example, you should understand:

1. **FastAPI Containerization**: How to containerize async Python applications
2. **Multi-stage Builds**: Building efficient production images
3. **Security Practices**: Non-root users, trusted hosts, authentication
4. **Production Configuration**: Gunicorn setup, environment variables
5. **Monitoring Setup**: Health checks and readiness probes
6. **Container Optimization**: Layer caching, minimal images, build context

## 🔗 Related Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## ⭐ Best Practices Demonstrated

- ✅ Multi-stage builds for optimization
- ✅ Non-root user for security
- ✅ Environment-based configuration
- ✅ Comprehensive health checks
- ✅ Production-ready server setup
- ✅ Proper error handling
- ✅ Security middleware
- ✅ Documentation and testing endpoints
