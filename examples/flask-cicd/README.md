# Flask CI/CD Example

This example demonstrates a complete CI/CD pipeline for a Flask application using GitHub Actions, Docker, and modern Python development practices.

## 🎯 What You'll Learn

- Building production-ready Flask applications
- Setting up comprehensive CI/CD pipelines with GitHub Actions
- Multi-stage Docker builds for development and production
- Automated testing, linting, and security scanning
- Container registry integration and deployment strategies

## 🏗️ Architecture

```
Flask App + PostgreSQL + Redis
        ↓
Multi-stage Docker Build
        ↓
GitHub Actions Pipeline
        ↓
Container Registry (GitHub Packages)
        ↓
Production Deployment
```

## 📋 Features

### Application Features
- ✅ RESTful API with Flask
- ✅ PostgreSQL database integration
- ✅ Redis caching layer
- ✅ Health check endpoints
- ✅ Structured logging
- ✅ Error handling and validation
- ✅ Type hints with Pyright

### CI/CD Features
- ✅ Automated testing with pytest
- ✅ Code quality checks (Ruff, Pyright)
- ✅ Security scanning (Safety, Bandit)
- ✅ Multi-stage Docker builds
- ✅ Container registry integration
- ✅ Coverage reporting
- ✅ Artifact management

## 🚀 Quick Start

### Local Development

1. **Clone and navigate to the example:**
   ```bash
   cd examples/flask-cicd
   ```

2. **Start the development environment:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - API: http://localhost:5000
   - Health check: http://localhost:5000/health
   - Ready check: http://localhost:5000/ready

### Manual Setup (without Docker)

1. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Set up environment variables:**
   ```bash
   export DATABASE_URL="postgresql://postgres:password@localhost:5432/flaskcicd"
   export REDIS_URL="redis://localhost:6379/0"
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ -v --cov=app --cov-report=html
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
```

## 🐳 Docker Commands

### Development Build
```bash
docker build --target development -t flask-cicd:dev .
```

### Production Build
```bash
docker build --target production -t flask-cicd:prod .
```

### Run Production Container
```bash
docker run -p 5000:5000 \
  -e DATABASE_URL="your-db-url" \
  -e REDIS_URL="your-redis-url" \
  flask-cicd:prod
```

## 📊 API Endpoints

### Health & Monitoring
- `GET /health` - Basic health check
- `GET /ready` - Readiness check (includes database and Redis)

### Application API
- `GET /` - API information
- `GET /api/items` - List all items (cached)
- `POST /api/items` - Create a new item

### Example API Usage
```bash
# Get API info
curl http://localhost:5000/

# Create an item
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Example Item", "description": "An example item"}'

# List items
curl http://localhost:5000/api/items
```

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline includes:

### 1. Test Job
- Sets up Python 3.11
- Installs dependencies
- Runs linting (Ruff)
- Performs type checking (Pyright)
- Executes tests with coverage
- Uploads coverage to Codecov

### 2. Security Job
- Scans dependencies for vulnerabilities (Safety)
- Performs static security analysis (Bandit)
- Uploads security scan results

### 3. Build and Push Job
- Builds multi-stage Docker image
- Pushes to GitHub Container Registry
- Uses caching for faster builds
- Tags images appropriately

### 4. Deploy Job
- Runs only on main branch
- Deploys to production environment
- Includes environment protection rules

## 📁 Project Structure

```
flask-cicd/
├── app.py                 # Main Flask application
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Local development environment
├── pyproject.toml        # Python project configuration
├── tests/
│   └── test_app.py       # Comprehensive test suite
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `FLASK_ENV` - Flask environment (development/production)

### Docker Compose Services
- `web` - Flask application
- `db` - PostgreSQL database
- `redis` - Redis cache

## 📈 Production Considerations

### Performance
- Multi-stage Docker builds for smaller production images
- Redis caching for API responses
- Connection pooling for database
- Gunicorn WSGI server for production

### Security
- Dependency vulnerability scanning
- Static security analysis
- Non-root container user
- Health check endpoints for monitoring

### Monitoring
- Structured logging with JSON format
- Health and readiness endpoints
- Error tracking and reporting
- Performance metrics collection

## 🔗 Related Examples

- [FastAPI CI/CD Example](../fastapi-cicd/) - Advanced API with async support
- [Module 5: Kubernetes Deployment](../../README.md#module-5) - Container orchestration

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [PostgreSQL with Python](https://www.psycopg.org/)
- [Redis with Python](https://redis-py.readthedocs.io/)
