# 📦 Flask Advanced Example

This example demonstrates a Flask application with SQLite database integration, showcasing:

## Features

- **Database Integration**: SQLite database with user management
- **Data Persistence**: Docker volumes for database storage
- **Multi-stage Build**: Optimized Docker image
- **Health Checks**: Database connectivity monitoring
- **RESTful API**: CRUD operations for users

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check with database status
- `GET /users` - List all users
- `POST /users` - Create a new user
- `GET /users/{id}` - Get specific user

## Running the Application

### Using Docker

```bash
# Build the image
docker build -t flask-advanced .

# Run with volume for data persistence
docker run -d \
  -p 5000:5000 \
  -v flask_data:/app/data \
  --name flask-advanced-app \
  flask-advanced
```

### Testing the API

```bash
# Create a user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'

# Get all users
curl http://localhost:5000/users

# Health check
curl http://localhost:5000/health
```

## Key Docker Concepts Demonstrated

1. **Multi-stage builds** for image optimization
2. **Volume mounts** for data persistence
3. **Health checks** for container monitoring
4. **Non-root user** for security
5. **Build optimization** with wheel caching
