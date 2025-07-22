from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import redis
import json
import os
import asyncio
from datetime import datetime

app = FastAPI(
    title="FastAPI + Redis Development Example",
    description="An example showing local development with FastAPI and Redis",
    version="1.0.0"
)

# Redis connection


def get_redis():
    return redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        decode_responses=True
    )

# Pydantic models


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    created_at: Optional[str] = None


class UserCreate(BaseModel):
    name: str
    email: str


class CacheStats(BaseModel):
    total_keys: int
    memory_usage: str
    connected_clients: int

# Routes


@app.get("/")
async def root():
    return {
        "message": "FastAPI + Redis Development Example",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "docs": "/docs",
        "cache": "Redis connected" if check_redis_connection() else "Redis disconnected"
    }


@app.get("/health")
async def health():
    redis_status = "healthy" if check_redis_connection() else "unhealthy"

    return {
        "status": "healthy",
        "service": "fastapi-redis-app",
        "cache": redis_status,
        "timestamp": datetime.utcnow().isoformat()
    }


def check_redis_connection():
    try:
        r = get_redis()
        r.ping()
        return True
    except:
        return False


@app.get("/users", response_model=List[User])
async def get_users():
    """Get all users from cache"""
    r = get_redis()

    try:
        # Get all user keys
        user_keys = r.keys("user:*")
        users = []

        for key in user_keys:
            user_data = r.get(key)
            if user_data:
                user = json.loads(user_data)
                users.append(User(**user))

        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache error: {str(e)}")


@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user and store in cache"""
    r = get_redis()

    try:
        # Generate simple ID
        user_id = r.incr("user_counter")

        # Create user with timestamp
        user_data = User(
            id=user_id,
            name=user.name,
            email=user.email,
            created_at=datetime.utcnow().isoformat()
        )

        # Store in Redis
        r.set(f"user:{user_id}", json.dumps(user_data.dict()))

        # Set expiration (optional - for demo purposes)
        r.expire(f"user:{user_id}", 3600)  # 1 hour

        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache error: {str(e)}")


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user from cache"""
    r = get_redis()

    try:
        user_data = r.get(f"user:{user_id}")
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        user = json.loads(user_data)
        return User(**user)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="Invalid user data in cache")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache error: {str(e)}")


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Delete a user from cache"""
    r = get_redis()

    try:
        deleted = r.delete(f"user:{user_id}")
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": f"User {user_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache error: {str(e)}")


@app.get("/cache/stats", response_model=CacheStats)
async def get_cache_stats():
    """Get Redis cache statistics"""
    r = get_redis()

    try:
        info = r.info()

        return CacheStats(
            total_keys=info['db0']['keys'] if 'db0' in info else 0,
            memory_usage=f"{info['used_memory_human']}",
            connected_clients=info['connected_clients']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache error: {str(e)}")


@app.delete("/cache/flush")
async def flush_cache():
    """Clear all cache data (development only)"""
    if os.getenv("ENVIRONMENT") != "development":
        raise HTTPException(
            status_code=403, detail="Cache flush only allowed in development")

    r = get_redis()

    try:
        r.flushdb()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache error: {str(e)}")

# Async background task example


@app.on_event("startup")
async def startup_event():
    """Initialize some sample data on startup"""
    await asyncio.sleep(2)  # Wait for Redis to be ready

    try:
        r = get_redis()

        # Add some sample users if none exist
        if not r.exists("user_counter"):
            sample_users = [
                {"name": "Alice Johnson", "email": "alice@example.com"},
                {"name": "Bob Smith", "email": "bob@example.com"},
                {"name": "Charlie Brown", "email": "charlie@example.com"}
            ]

            for user_data in sample_users:
                user_id = r.incr("user_counter")
                user = User(
                    id=user_id,
                    name=user_data["name"],
                    email=user_data["email"],
                    created_at=datetime.utcnow().isoformat()
                )
                r.set(f"user:{user_id}", json.dumps(user.dict()))

    except Exception as e:
        print(f"Startup error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
