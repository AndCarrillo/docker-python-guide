# Flask with Quality Tools

This example demonstrates how to integrate code quality tools with a Flask application.

## Current Status (Module 2 Completed)

This directory contains a Flask application that has completed Module 2:

- ✅ Flask application with PostgreSQL integration
- ✅ Task management API endpoints
- ✅ Docker Compose development environment
- ✅ Database persistence and admin interface

## Files Structure

```
examples/flask-quality/
├── app.py                    # Flask app with PostgreSQL (Module 2 completed)
├── requirements.txt          # Runtime dependencies
├── requirements-dev.txt      # Development dependencies (basic)
├── pyproject.toml           # Basic project configuration
├── .pre-commit-config.yaml  # Basic pre-commit setup
├── compose.yaml             # Docker Compose with PostgreSQL
├── Dockerfile               # Development container
└── README.md                # This file
```

## Quick Start (Current State)

1. Start the services:
```bash
docker compose up --build
```

2. Test the application:
```bash
# Home endpoint
curl http://localhost:5000/

# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Testing the API"}'

# Get all tasks
curl http://localhost:5000/tasks
```

3. Access database admin: http://localhost:8080

## Next Steps - Module 3

Follow the Module 3 guide to enhance this application with:

- 🔧 **Ruff** for linting and formatting
- 🔍 **Pyright** for static type checking  
- 🪝 **Pre-commit hooks** for automated quality checks
- 📝 **Type annotations** throughout the codebase
- 🐳 **Container-based quality tools** integration

The current code is intentionally basic and will be enhanced step-by-step following the Module 3 guide.
