# 🚀 FastAPI Basic Example

This example demonstrates a simple FastAPI application with basic containerization concepts.

## Features

- **RESTful API**: Task management with CRUD operations
- **Async Support**: Async endpoints for better performance
- **Auto Documentation**: Interactive API docs at `/docs`
- **Data Validation**: Pydantic models for request/response validation
- **Health Checks**: Built-in health monitoring

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /tasks` - List all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task completion
- `DELETE /tasks/{id}` - Delete task

## Running the Application

### Using Docker

```bash
# Build the image
docker build -t fastapi-basic .

# Run the container
docker run -d -p 8000:8000 --name fastapi-basic-app fastapi-basic
```

### Testing the API

```bash
# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker", "description": "Containerize FastAPI app"}'

# Get all tasks
curl http://localhost:8000/tasks

# Check health
curl http://localhost:8000/health
```

### Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI or `http://localhost:8000/redoc` for ReDoc.

## Key Docker Concepts Demonstrated

1. **Simple Dockerfile** structure
2. **Dependency caching** with requirements.txt
3. **Non-root user** for security
4. **Health checks** for monitoring
5. **Environment variables** configuration
