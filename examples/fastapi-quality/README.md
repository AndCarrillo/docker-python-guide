# FastAPI with Type Safety

This example demonstrates how to integrate advanced type checking and quality tools with a FastAPI application.

## Current Status (Module 2 Completed)

This directory contains a FastAPI application that has completed Module 2:

- ✅ FastAPI application with Redis integration
- ✅ User management API endpoints with caching
- ✅ Docker Compose development environment
- ✅ Redis persistence and admin interface

## Files Structure

```
examples/fastapi-quality/
├── main.py                  # FastAPI app with Redis (Module 2 completed)
├── requirements.txt         # Runtime dependencies
├── requirements-dev.txt     # Development dependencies (basic)
├── pyproject.toml          # Basic project configuration
├── .pre-commit-config.yaml # Basic pre-commit setup
├── compose.yaml            # Docker Compose with Redis
├── Dockerfile              # Development container
└── README.md               # This file
```

## Quick Start (Current State)

1. Start the services:
```bash
docker compose up --build
```

2. Test the application:
```bash
# Home endpoint
curl http://localhost:8000/

# Create a user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'

# Get all users (cached)
curl http://localhost:8000/users

# Check cache statistics
curl http://localhost:8000/cache/stats
```

3. Access interfaces:
   - API Documentation: http://localhost:8000/docs
   - Redis Admin: http://localhost:8081

## Next Steps - Module 3

Follow the Module 3 guide to enhance this application with:

- 🔧 **Ruff** for linting and formatting
- 🔍 **Pyright** for strict static type checking
- 🪝 **Pre-commit hooks** for automated quality checks
- 📝 **Advanced type annotations** with Pydantic
- 🐳 **Container-based quality tools** integration
- ⚡ **Async typing patterns** and best practices

The current code is intentionally basic and will be enhanced step-by-step following the Module 3 guide.
