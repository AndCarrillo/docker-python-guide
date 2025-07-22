# FastAPI CI/CD Example

This example demonstrates an advanced CI/CD pipeline for a FastAPI application with comprehensive testing, performance monitoring, and deployment automation.

## 🎯 What You'll Learn

- Building high-performance async APIs with FastAPI
- Advanced CI/CD pipelines with matrix testing and performance benchmarks
- Async database operations with SQLAlchemy
- Redis caching and session management
- Comprehensive testing strategies (unit, integration, performance)
- Advanced security scanning and monitoring
- Production deployment with monitoring and alerting

## 🚀 Key Features

### Application Features
- ✅ **Async FastAPI** with high-performance endpoints
- ✅ **PostgreSQL** with async SQLAlchemy operations
- ✅ **Redis** for caching and session management
- ✅ **Background Tasks** for async processing
- ✅ **Comprehensive API Documentation** (OpenAPI/Swagger)
- ✅ **Advanced Health Checks** with dependency verification
- ✅ **Structured Logging** with JSON format
- ✅ **Type Safety** with Pydantic models and type hints

### CI/CD Features
- ✅ **Matrix Testing** across Python 3.10, 3.11, 3.12
- ✅ **Performance Testing** with Locust
- ✅ **Advanced Security Scanning** (Safety, Bandit, Semgrep)
- ✅ **Multi-stage Docker builds** with optimization
- ✅ **Container Registry** integration with caching
- ✅ **Automated Deployment** with smoke tests
- ✅ **Coverage Reporting** with Codecov integration

## 🏗️ Architecture

```
FastAPI (Async) + PostgreSQL + Redis
           ↓
   Multi-stage Docker Build
           ↓
GitHub Actions (Matrix Testing)
           ↓
   Performance & Security Tests
           ↓
Container Registry (GHCR)
           ↓
Production Deployment + Monitoring
```

## 🚀 Quick Start

### Development with Docker Compose

1. **Start all services:**
   ```bash
   cd examples/fastapi-cicd
   docker-compose up --build
   ```

2. **Access the application:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

### Manual Development Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Set environment variables:**
   ```bash
   export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/fastapicd"
   export REDIS_URL="redis://localhost:6379/0"
   ```

3. **Run the application:**
   ```bash
   uvicorn app:app --reload
   ```

## 🧪 Testing

### Comprehensive Test Suite
```bash
# Run all tests with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test categories
pytest tests/test_app.py::TestAPIEndpoints -v
pytest tests/test_app.py::TestCaching -v
```

### Performance Testing
```bash
# Install performance testing tools
pip install locust

# Run performance tests
locust --headless --users 100 --spawn-rate 10 \
       --run-time 60s --host http://localhost:8000 \
       -f tests/locustfile.py
```

### Code Quality & Security
```bash
# Linting and formatting
ruff check .
ruff format .

# Type checking
pyright .

# Security scanning
safety check -r requirements.txt
bandit -r . -f json
```

## 📊 API Endpoints

### Core API
- `GET /` - API information and navigation
- `GET /docs` - Interactive Swagger documentation
- `GET /redoc` - ReDoc documentation

### Health & Monitoring
- `GET /health` - Basic health check
- `GET /ready` - Comprehensive readiness check

### Items API
- `GET /api/items` - List items (with caching and pagination)
- `POST /api/items` - Create new item (with background tasks)
- `GET /api/items/{id}` - Get specific item (with caching)

### Example Usage

```bash
# API Information
curl http://localhost:8000/

# Create an item
curl -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "FastAPI Example",
    "description": "High-performance async API"
  }'

# Get items with pagination
curl "http://localhost:8000/api/items?skip=0&limit=10"

# Get specific item
curl http://localhost:8000/api/items/1
```

## 🐳 Docker Operations

### Development Build
```bash
docker build --target development -t fastapi-cicd:dev .
docker run -p 8000:8000 \
  -e DATABASE_URL="your-db-url" \
  -e REDIS_URL="your-redis-url" \
  fastapi-cicd:dev
```

### Production Build
```bash
docker build --target production -t fastapi-cicd:prod .
```

### Multi-platform Build
```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  --target production -t fastapi-cicd:prod .
```

## 🔄 Advanced CI/CD Pipeline

### Pipeline Stages

1. **Matrix Testing**
   - Tests across Python 3.10, 3.11, 3.12
   - Parallel execution for faster feedback
   - Full test suite with coverage reporting

2. **Performance Testing**
   - Load testing with Locust
   - Performance regression detection
   - Automated benchmarking

3. **Security Scanning**
   - Dependency vulnerability scanning (Safety)
   - Static security analysis (Bandit)
   - Advanced code scanning (Semgrep)

4. **Build & Push**
   - Multi-stage optimized Docker builds
   - Container registry integration
   - Build caching for efficiency

5. **Deployment**
   - Automated production deployment
   - Post-deployment smoke tests
   - Health check verification

### Environment Configuration

```yaml
# GitHub Environments (configure in repository settings)
production:
  protection_rules:
    - required_reviewers: 1
    - wait_timer: 5 # minutes
  deployment_branch_policy:
    custom_branch_policies: true
    branches: [main]
```

## 📁 Project Structure

```
fastapi-cicd/
├── app.py                    # Main FastAPI application
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Development environment
├── pyproject.toml           # Project configuration
├── tests/
│   ├── test_app.py          # Comprehensive test suite
│   └── locustfile.py        # Performance tests
└── README.md               # This documentation
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |

### Docker Compose Services

- **web**: FastAPI application with hot reload
- **db**: PostgreSQL 15 with Alpine Linux
- **redis**: Redis 7 with persistence

## 🔧 Production Considerations

### Performance Optimizations
- **Async Operations**: Full async/await pattern
- **Connection Pooling**: Optimized database connections
- **Redis Caching**: Intelligent cache invalidation
- **Multi-worker Deployment**: Uvicorn with multiple workers

### Security Features
- **Input Validation**: Comprehensive Pydantic models
- **SQL Injection Protection**: SQLAlchemy ORM
- **CORS Configuration**: Configurable cross-origin requests
- **Security Headers**: Production-ready defaults

### Monitoring & Observability
- **Structured Logging**: JSON format for log aggregation
- **Health Endpoints**: Kubernetes-ready health checks
- **Performance Metrics**: Built-in FastAPI metrics
- **Error Tracking**: Comprehensive error handling

## 🔗 Related Examples

- [Flask CI/CD Example](../flask-cicd/) - Traditional synchronous approach
- [Module 5: Kubernetes](../../README.md#module-5) - Container orchestration

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Async SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Redis with AsyncIO](https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html)
- [GitHub Actions Matrix Strategy](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)
- [Locust Performance Testing](https://locust.io/)

## 🎯 Next Steps

1. **Deploy to Production**: Use the provided workflows for automated deployment
2. **Add Monitoring**: Integrate with Prometheus, Grafana, or similar
3. **Scale Horizontally**: Deploy multiple instances with load balancing
4. **Add Authentication**: Implement JWT or OAuth2 authentication
5. **API Versioning**: Add versioning strategy for backwards compatibility
