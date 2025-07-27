# Choose your Learning Path

Do you want to follow this module using FastAPI or Flask? Select your preferred path:

| Learning Path | Link                                                                |
| ------------- | ------------------------------------------------------------------- |
| 🚀 FastAPI    | [Go to the FastAPI example for this module](../fastapi-deployment/) |
| 🌱 Flask      | [Go to the Flask example for this module](../flask-deployment/)     |

# Flask Deployment Example

This example demonstrates how to set up a Flask application with PostgreSQL using Docker Compose for development.

## Current Status (Module 1)

This directory contains a basic Flask application from Module 1:

- Simple Flask app with one endpoint
- Basic Dockerfile for containerization
- Simple compose.yaml with just the web service

## Files Structure

```
examples/flask-deployment/
├── app.py              # Simple Flask application
├── requirements.txt    # Flask dependency only
├── .dockerignore       # Docker ignore file
├── compose.yaml        # Basic compose configuration
├── Dockerfile          # Container definition
└── README.md           # This file
```

## Quick Start (Module 1 state)

1. Start the service:

```bash
docker compose up --build
```

2. Test the application:

```bash
curl http://localhost:5000/
```

You should see: `{"message": "Hello from Flask in Docker!", "status": "running"}`

## Next Steps

Follow the Module 2 guide to enhance this basic setup with:

- PostgreSQL database integration
- Database secrets management
- Hot reload development
- Admin interface

## What you'll learn

- Setting up multi-service development environment
- Database integration with Flask-SQLAlchemy
- Hot reload development workflow
- Database initialization and administration
- Service networking and communication

## Application Overview

This is a simple task management API built with Flask that demonstrates:

- **CRUD operations** with PostgreSQL database
- **Database migrations** and initialization
- **Environment-based configuration**
- **Health checks** for both app and database
- **Development tools** integration

## Quick Start

### 1. Start the Development Environment

```bash
# Navigate to the example directory
cd examples/flask-postgres

# Start all services
docker-compose up --build
```

This will start:

- **Flask app** on http://localhost:5000
- **PostgreSQL database** on localhost:5432
- **Adminer** (database admin) on http://localhost:8080

### 2. Test the API

```bash
# Health check
curl http://localhost:5000/health

# Get all tasks
curl http://localhost:5000/tasks

# Create a new task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker Compose", "description": "Complete the tutorial"}'

# Update a task
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete a task
curl -X DELETE http://localhost:5000/tasks/1
```

### 3. Access Database Admin

Visit http://localhost:8080 and login with:

- **System:** PostgreSQL
- **Server:** db
- **Username:** user
- **Password:** password
- **Database:** devdb

## Docker Compose Breakdown

### Services Configuration

```yaml
services:
  # Flask application
  web:
    build: . # Build from local Dockerfile
    ports:
      - "5000:5000" # Map host:container ports
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://user:password@db:5432/devdb
    volumes:
      - .:/app # Mount source for hot reload
    depends_on:
      - db # Wait for database

  # PostgreSQL database
  db:
    image: postgres:15-alpine # Official PostgreSQL image
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=devdb
    volumes:
      - postgres_data:/var/lib/postgresql/data # Persist data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql # Initialize
```

### Key Features

**Hot Reload:**

- Source code is mounted as volume (`.:/app`)
- Changes in Python files automatically reload the app
- No need to rebuild containers for code changes

**Database Initialization:**

- `init.sql` runs on first database startup
- Sample data is automatically loaded
- Database schema is created by Flask-SQLAlchemy

**Service Communication:**

- Flask connects to database using service name (`db`)
- Internal networking handles service discovery
- No need for external IP addresses

## Development Workflow

### Making Changes

1. **Edit Python code** - Changes are reflected immediately
2. **Database changes** - Use Flask-SQLAlchemy migrations
3. **Dependencies** - Add to requirements.txt and rebuild
4. **Environment** - Modify docker-compose.yml

### Common Commands

```bash
# View logs
docker-compose logs web
docker-compose logs db

# Execute commands in containers
docker-compose exec web python -c "print('Hello from container')"
docker-compose exec db psql -U user -d devdb

# Restart services
docker-compose restart web

# Rebuild after dependency changes
docker-compose up --build

# Stop and clean up
docker-compose down -v  # Also removes volumes
```

### Database Operations

```bash
# Connect to database
docker-compose exec db psql -U user -d devdb

# View tables
docker-compose exec db psql -U user -d devdb -c "\\dt"

# Reset database (remove volumes)
docker-compose down -v
docker-compose up --build
```

## Troubleshooting

### Common Issues

**Database connection errors:**

```bash
# Check if database is running
docker-compose ps

# View database logs
docker-compose logs db

# Test connection
docker-compose exec web python -c "
from app import db
print('Database connected!' if db.engine else 'Connection failed')
"
```

**Hot reload not working:**

```bash
# Check volume mounting
docker-compose exec web ls -la /app

# Ensure you're in the correct directory
pwd  # Should show .../examples/flask-postgres
```

**Port conflicts:**

```yaml
# Change ports in docker-compose.yml
ports:
  - "5001:5000" # Use 5001 instead of 5000
```

## File Structure

```
flask-postgres/
├── app.py                    # Main Flask application
│   ├── Task model            # SQLAlchemy model
│   ├── CRUD endpoints        # REST API routes
│   └── Health checks         # Monitoring endpoints
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-service setup
├── init.sql                 # Database initialization
├── .dockerignore           # Build optimization
└── README.md               # This file
```

## Key Learning Points

### 1. Service Orchestration

- Multiple services working together
- Dependency management with `depends_on`
- Automatic service discovery

### 2. Development Efficiency

- Hot reload for instant feedback
- Database admin tools
- Consistent environment across team

### 3. Data Persistence

- Named volumes for database data
- Initialization scripts
- Data survives container restarts

### 4. Environment Configuration

- Service-specific environment variables
- Database connection strings
- Development vs production settings

## Exercises

### Exercise 1: Add New Endpoint

1. Add a new route to get completed tasks only
2. Test without rebuilding the container
3. Verify hot reload functionality

### Exercise 2: Database Exploration

1. Use Adminer to explore the database structure
2. Add sample data through the web interface
3. Verify it appears in the API

### Exercise 3: Environment Customization

1. Create a `.env` file with custom variables
2. Override default database credentials
3. Test the application with new settings

## Next Steps

After mastering this example:

1. **Try the FastAPI + Redis example** for async patterns
2. **Experiment with different databases** (MySQL, MongoDB)
3. **Add more services** (nginx, workers, etc.)
4. **Learn production deployment** in later modules

This example provides the foundation for any multi-service Python application development with Docker Compose.

---

**⬅️ [Back to Module 2](../README.md)**
