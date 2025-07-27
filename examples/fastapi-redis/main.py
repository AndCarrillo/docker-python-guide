from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import json
import os
from typing import List, Optional

app = FastAPI(title="FastAPI + Redis Demo", version="1.0.0")

# Redis configuration
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
redis_client = redis.from_url(redis_url, decode_responses=True)

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: str
    name: str
    email: str

@app.on_event("startup")
async def startup_event():
    try:
        redis_client.ping()
        print("Connected to Redis successfully")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")

@app.get("/")
async def root():
    try:
        user_count = redis_client.dbsize()
        return {
            "message": "Hello from FastAPI + Redis!", 
            "status": "running",
            "users_in_cache": user_count
        }
    except Exception as e:
        return {"message": "Hello from FastAPI!", "redis_error": str(e)}

@app.get("/health")
async def health_check():
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "redis_error": str(e)}

@app.get("/users", response_model=List[User])
async def get_users():
    try:
        keys = redis_client.keys("user:*")
        users = []
        for key in keys:
            user_data = redis_client.get(key)
            if user_data:
                user = json.loads(user_data)
                users.append(user)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    try:
        # Generate simple ID
        user_id = str(redis_client.incr("user_counter"))
        
        user_data = {
            "id": user_id,
            "name": user.name,
            "email": user.email
        }
        
        # Store in Redis
        redis_client.set(f"user:{user_id}", json.dumps(user_data))
        
        return User(**user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    try:
        user_data = redis_client.get(f"user:{user_id}")
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = json.loads(user_data)
        return User(**user)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid user data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
