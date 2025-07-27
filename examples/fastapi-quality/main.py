from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import redis
import json
import os
from datetime import datetime

app = FastAPI(
    title="FastAPI Redis Development Example",
    description="An example showing local development with FastAPI and Redis",
    version="1.0.0"
)

# Redis connection
def get_redis():
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    return redis.from_url(redis_url, decode_responses=True)

# Pydantic models
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    created_at: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    email: str

# In-memory storage for demo purposes
users = []

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI in Docker!", "users_count": len(users)}

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    redis_client = get_redis()
    
    # Create new user
    new_user = User(
        id=len(users) + 1,
        name=user.name,
        email=user.email,
        created_at=datetime.utcnow().isoformat()
    )
    
    users.append(new_user)
    
    # Cache the user
    redis_client.setex(
        f"user:{new_user.id}",
        300,  # 5 minutes
        json.dumps(new_user.dict())
    )
    
    return new_user

@app.get("/users", response_model=List[User])
async def get_users():
    redis_client = get_redis()
    
    # Try to get from cache
    cached_users = redis_client.get("users:all")
    if cached_users:
        return [User(**user) for user in json.loads(cached_users)]
    
    # Cache the users list
    redis_client.setex(
        "users:all",
        300,  # 5 minutes
        json.dumps([user.dict() for user in users])
    )
    
    return users

@app.get("/cache/stats")
async def get_cache_stats():
    redis_client = get_redis()
    info = redis_client.info()
    
    return {
        "connected_clients": info.get("connected_clients", 0),
        "used_memory": info.get("used_memory_human", "0B"),
        "total_keys": redis_client.dbsize()
    }
