# FastAPI + Redis Development Example

This example demonstrates how to set up a FastAPI application with Redis using Docker Compose for development.

## Current Status (Module 1)

This directory contains a basic FastAPI application from Module 1:

- Simple FastAPI app with one endpoint
- Basic Dockerfile for containerization
- Simple compose.yaml with just the API service

## Files Structure

```
examples/fastapi-redis/
├── main.py            # Simple FastAPI application
├── requirements.txt   # FastAPI and Uvicorn only
├── .dockerignore     # Docker ignore file
├── compose.yaml      # Basic compose configuration
├── Dockerfile        # Container definition
└── README.md         # This file
```

## Quick Start (Module 1 state)

1. Start the service:

```bash
docker compose up --build
```

2. Test the application:

```bash
curl http://localhost:8000/
```

You should see: `{"message": "Hello from FastAPI in Docker!", "users_count": 0}`

3. Access API documentation:

```bash
http://localhost:8000/docs
```

## Next Steps

Follow the Module 2 guide to enhance this basic setup with:

- Redis cache integration
- User management endpoints
- Cache statistics
- Redis admin interface
- Development tools and admin interfaces

## Application Overview

This is a user management API built with FastAPI that demonstrates:

- **Async/await patterns** with FastAPI
- **Redis caching** for data storage
- **Automatic API documentation** with OpenAPI
- **Background tasks** and startup initialization
- **Admin interfaces** for development

## Quick Start

### 1. Start the Development Environment

```bash
# Navigate to the example directory
cd examples/fastapi-redis

# Start all services
docker-compose up --build
```

This will start:

- **FastAPI app** on http://localhost:8000
- **Redis cache** on localhost:6379
- **Redis Commander** (admin interface) on http://localhost:8081

### 2. Explore the API

**Interactive Documentation:**

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

**API Endpoints:**

```bash
# Health check
curl http://localhost:8000/health

# Get all users
curl http://localhost:8000/users

# Create a new user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'

# Get specific user
curl http://localhost:8000/users/1

# Get cache statistics
curl http://localhost:8000/cache/stats

# Clear cache (development only)
curl -X DELETE http://localhost:8000/cache/flush
```

### 3. Access Redis Admin

Visit http://localhost:8081 to explore the Redis data structure and monitor cache operations in real-time.

## Docker Compose Breakdown

### Services Configuration

```yaml
services:
  # FastAPI application
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - REDIS_HOST=redis # Service name as hostname
      - REDIS_PORT=6379
    volumes:
      - .:/app # Hot reload enabled
    depends_on:
      - redis

  # Redis cache
  redis:
    image: redis:7.2-alpine
    command: redis-server --appendonly yes # Enable persistence
    volumes:
      - redis_data:/data # Persist Redis data

  # Redis admin interface
  redis-commander:
    image: rediscommander/redis-commander:latest
    environment:
      - REDIS_HOSTS=local:redis:6379
```

### Key Features

**Async Operations:**

- FastAPI handles async/await patterns naturally
- Redis operations are non-blocking
- Background tasks run independently

**Cache Persistence:**

- Redis data survives container restarts
- AOF (Append Only File) persistence enabled
- Named volume for data storage

**Development Tools:**

- Automatic API documentation
- Redis admin interface
- Hot reload for code changes

## Application Architecture

### Data Models

```python
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    created_at: Optional[str] = None

class CacheStats(BaseModel):
    total_keys: int
    memory_usage: str
    connected_clients: int
```

### Redis Integration

**Connection Management:**

```python
def get_redis():
    return redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        decode_responses=True
    )
```

**Data Operations:**

```python
# Store user data
r.set(f"user:{user_id}", json.dumps(user_data.dict()))

# Set expiration
r.expire(f"user:{user_id}", 3600)  # 1 hour

# Retrieve data
user_data = r.get(f"user:{user_id}")
```

### Background Tasks

```python
@app.on_event("startup")
async def startup_event():
    """Initialize sample data on startup"""
    await asyncio.sleep(2)  # Wait for Redis
    # Initialize sample users...
```

## Development Workflow

### Real-time Development

1. **Code Changes:** Modify Python files for instant reload
2. **API Testing:** Use Swagger UI for interactive testing
3. **Cache Monitoring:** Watch Redis operations in real-time
4. **Data Inspection:** Use Redis Commander to view data

### Common Operations

```bash
# View application logs
docker-compose logs api

# Monitor Redis operations
docker-compose logs redis

# Execute Redis commands
docker-compose exec redis redis-cli

# Test Redis connection
docker-compose exec redis redis-cli ping

# Check cache keys
docker-compose exec redis redis-cli keys "*"

# Monitor Redis in real-time
docker-compose exec redis redis-cli monitor
```

### Performance Testing

```bash
# Install httpie for better testing
pip install httpie

# Create multiple users quickly
for i in {1..10}; do
  http POST localhost:8000/users name="User $i" email="user$i@example.com"
done

# Test cache performance
time curl http://localhost:8000/users
time curl http://localhost:8000/cache/stats
```

## Advanced Features

### Cache Strategies

**User Storage:**

```python
# Store with expiration
r.set(f"user:{user_id}", json.dumps(user_data.dict()))
r.expire(f"user:{user_id}", 3600)  # 1 hour TTL
```

**Statistics Tracking:**

```python
# Increment counters
r.incr("user_counter")
r.incr("api_calls")

# Store metrics
r.hset("metrics", "total_users", user_count)
```

### Error Handling

```python
try:
    user_data = r.get(f"user:{user_id}")
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
except redis.ConnectionError:
    raise HTTPException(status_code=503, detail="Cache unavailable")
```

### Environment Specific Features

```python
# Development-only endpoints
@app.delete("/cache/flush")
async def flush_cache():
    if os.getenv("ENVIRONMENT") != "development":
        raise HTTPException(status_code=403, detail="Not allowed in production")
```

## Troubleshooting

### Redis Connection Issues

```bash
# Check Redis service status
docker-compose ps redis

# Test Redis connectivity
docker-compose exec api python -c "
import redis
r = redis.Redis(host='redis', port=6379)
print('Connected!' if r.ping() else 'Failed!')
"

# View Redis logs
docker-compose logs redis
```

### Performance Issues

```bash
# Monitor Redis memory usage
docker-compose exec redis redis-cli info memory

# Check slow queries
docker-compose exec redis redis-cli slowlog get 10

# Monitor commands in real-time
docker-compose exec redis redis-cli monitor
```

### Data Issues

```bash
# Clear all Redis data
docker-compose exec redis redis-cli flushall

# Or use the API endpoint
curl -X DELETE http://localhost:8000/cache/flush

# Restart with fresh data
docker-compose down -v
docker-compose up --build
```

## File Structure

```
fastapi-redis/
├── main.py                   # Main FastAPI application
│   ├── User models           # Pydantic models
│   ├── Redis integration     # Cache operations
│   ├── API endpoints         # REST routes
│   ├── Background tasks      # Startup events
│   └── Error handling        # Exception management
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-service setup
├── .dockerignore           # Build optimization
└── README.md               # This file
```

## Key Learning Points

### 1. Async Development

- Non-blocking I/O operations
- Background task management
- Concurrent request handling

### 2. Caching Strategies

- Data storage patterns
- TTL (Time To Live) management
- Cache invalidation strategies

### 3. API Design

- Automatic documentation
- Request/response models
- Error handling patterns

### 4. Development Tools

- Interactive API documentation
- Real-time cache monitoring
- Hot reload capabilities

## Exercises

### Exercise 1: Custom Cache Operations

1. Add a new endpoint to search users by name
2. Implement cache-aside pattern
3. Test performance with and without caching

### Exercise 2: Background Tasks

1. Add a background task to clean expired data
2. Implement periodic cache statistics collection
3. Monitor task execution

### Exercise 3: Advanced Redis Features

1. Use Redis Sets for user categories
2. Implement pub/sub for real-time notifications
3. Add Redis transactions for data consistency

## Performance Considerations

### Cache Optimization

- Use appropriate data structures (Hash, Set, List)
- Implement cache warming strategies
- Monitor memory usage and eviction

### Connection Management

- Connection pooling for production
- Timeout configuration
- Retry mechanisms

### Data Modeling

- Efficient key naming conventions
- Appropriate data serialization
- TTL strategies based on use case

## Next Steps

After mastering this example:

1. **Explore Redis advanced features** (Streams, Modules)
2. **Add authentication and authorization**
3. **Implement rate limiting with Redis**
4. **Learn production deployment** in later modules

This example provides advanced patterns for building high-performance, scalable Python applications with caching.

---

**⬅️ [Back to Module 2](../README.md)**
