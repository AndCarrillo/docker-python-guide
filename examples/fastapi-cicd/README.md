# FastAPI CI/CD Example

This example demonstrates an advanced CI/CD pipeline for a FastAPI application with async capabilities, comprehensive testing, performance monitoring, and modern Python development practices.

## 🎯 What You'll Learn

- Building production-ready async FastAPI applications
- Advanced CI/CD pipelines with matrix testing and performance testing
- Async database operations with SQLAlchemy 2.0
- Redis caching and session management
- Background tasks and async patterns
- Security scanning and performance monitoring
- Container optimization for async workloads

## 🏗️ Architecture

```
FastAPI (Async) + PostgreSQL + Redis
        ↓
Multi-stage Docker Build
        ↓
Advanced GitHub Actions Pipeline
├── Matrix Testing (Python 3.10, 3.11, 3.12)
├── Performance Testing (Locust)
├── Security Scanning (Multiple tools)
└── Container Registry & Deployment
```

## 📋 Features

### Application Features

- ✅ Async FastAPI with SQLAlchemy 2.0
- ✅ PostgreSQL with async drivers (asyncpg)
- ✅ Redis async client for caching
- ✅ Background tasks with FastAPI
- ✅ Comprehensive API documentation (OpenAPI/Swagger)
- ✅ Health and readiness checks
- ✅ Structured logging with JSON output
- ✅ Type hints and Pydantic models
- ✅ CORS middleware
- ✅ Error handling and validation

### CI/CD Features

- ✅ Matrix testing across Python versions
- ✅ Performance testing with Locust
- ✅ Advanced security scanning (Safety, Bandit, Semgrep)
- ✅ Async-optimized testing with pytest-asyncio
- ✅ Coverage reporting and analysis
- ✅ Multi-stage Docker builds
- ✅ Container registry integration
- ✅ Smoke tests for production deployment

## 🚀 Quick Start

### Local Development

1. **Clone and navigate to the example:**

   ```bash
   cd examples/fastapi-cicd
   ```

2. **Start the development environment:**

   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health
   - Ready check: http://localhost:8000/ready

### Manual Setup (without Docker)

1. **Install dependencies:**

   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Set up environment variables:**

   ```bash
   export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/fastapicd"
   export REDIS_URL="redis://localhost:6379/0"
   ```

3. **Run the application:**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Async Tests with Coverage

```bash
pytest tests/ -v --cov=app --cov-report=html
```

### Performance Testing

```bash
# Install Locust
pip install locust

# Run performance tests
locust --headless --users 100 --spawn-rate 10 --run-time 60s --host http://localhost:8000 -f tests/locustfile.py
```

### Code Quality Checks

```bash
# Linting and formatting
ruff check .
ruff format .

# Type checking
pyright .
```

### Security Scanning

```bash
# Dependency vulnerability scanning
safety check -r requirements.txt

# Static security analysis
bandit -r . -f json

# Advanced security scanning
semgrep --config=auto .
```

## 🐳 Docker Commands

### Development Build

```bash
docker build --target development -t fastapi-cicd:dev .
```

### Production Build

```bash
docker build --target production -t fastapi-cicd:prod .
```

### Run Production Container

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://your-db-url" \
  -e REDIS_URL="redis://your-redis-url" \
  fastapi-cicd:prod
```

## 📊 API Endpoints

### Health & Monitoring

- `GET /health` - Basic health check with version info
- `GET /ready` - Comprehensive readiness check (database + Redis)

### Application API

- `GET /` - API information and navigation
- `GET /api/items` - List all items with pagination (cached)
- `POST /api/items` - Create a new item (with background task)
- `GET /api/items/{item_id}` - Get specific item (cached)

### Documentation

- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Example API Usage

```bash
# Get API info
curl http://localhost:8000/

# Create an item
curl -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "FastAPI Item", "description": "An async example item"}'

# List items with pagination
curl "http://localhost:8000/api/items?skip=0&limit=10"

# Get specific item
curl http://localhost:8000/api/items/1

# Access interactive docs
open http://localhost:8000/docs
```

## 🔄 Advanced CI/CD Pipeline

### 1. Matrix Testing Job

- Tests across Python 3.10, 3.11, and 3.12
- Async test execution with pytest-asyncio
- Comprehensive coverage reporting
- Type checking and linting

### 2. Performance Testing Job

- Load testing with Locust
- Configurable user load and duration
- Performance regression detection
- Response time analysis

### 3. Security Scanning Job

- Dependency vulnerability scanning (Safety)
- Static security analysis (Bandit)
- Advanced security patterns (Semgrep)
- Security report artifacts

### 4. Build and Push Job

- Multi-stage Docker builds
- Container registry integration
- Build caching optimization
- Image vulnerability scanning

### 5. Deployment Job

- Production environment deployment
- Post-deployment smoke tests
- Health check verification
- Rollback capabilities

## 📁 Project Structure

```
fastapi-cicd/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Local development environment
├── pyproject.toml        # Python project configuration
├── tests/
│   ├── test_app.py       # Comprehensive async test suite
│   └── locustfile.py     # Performance testing scenarios
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

- `DATABASE_URL` - PostgreSQL async connection string
- `REDIS_URL` - Redis connection string
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

### Docker Compose Services

- `web` - FastAPI application (port 8000)
- `db` - PostgreSQL database (port 5433)
- `redis` - Redis cache (port 6380)

## 📈 Production Considerations

### Performance

- Async/await patterns for non-blocking operations
- Connection pooling for database and Redis
- Response caching with TTL
- Background task processing
- Uvicorn with multiple workers

### Security

- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- CORS configuration
- Security headers middleware
- Dependency vulnerability monitoring

### Monitoring

- Structured JSON logging
- Health and readiness endpoints
- Performance metrics collection
- Error tracking integration
- APM (Application Performance Monitoring) ready

### Scalability

- Horizontal scaling with multiple workers
- Database connection pooling
- Redis clustering support
- Container orchestration ready
- Load balancer friendly

## 🆚 FastAPI vs Flask Comparison

| Feature               | FastAPI (This Example)      | Flask (Previous Example) |
| --------------------- | --------------------------- | ------------------------ |
| **Async Support**     | ✅ Native async/await       | ❌ Sync only             |
| **API Documentation** | ✅ Auto-generated (OpenAPI) | ❌ Manual setup          |
| **Type Hints**        | ✅ Pydantic integration     | ⚠️ Manual validation     |
| **Performance**       | ✅ Higher throughput        | ⚠️ Good but sync         |
| **Learning Curve**    | ⚠️ Steeper                  | ✅ Gentler               |
| **Ecosystem**         | ⚠️ Newer                    | ✅ Mature                |

## 🔗 Related Examples

- [Flask CI/CD Example](../flask-cicd/) - Traditional sync API approach
- [Module 5: Kubernetes Deployment](../../README.md#module-5) - Container orchestration

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Redis Async Python](https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html)
- [Pydantic Models](https://docs.pydantic.dev/)
- [Locust Performance Testing](https://locust.io/)
- [Python Async Patterns](https://realpython.com/async-io-python/)
