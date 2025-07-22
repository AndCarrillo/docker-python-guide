"""
FastAPI application demonstrating containerization best practices.

This example shows a complete FastAPI application with:
- Async endpoints
- Database integration
- Authentication
- Monitoring
- Documentation
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import asyncio
import time
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# App configuration
app = FastAPI(
    title="Python Containerization API",
    description="A sample FastAPI application demonstrating Docker best practices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
    uptime: float


# In-memory database (in production, use real database)
users_db = []
app_start_time = time.time()

# Dependency for authentication


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify authentication token."""
    token = credentials.credentials
    # In production, verify JWT token here
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

# Routes


@app.get("/",
         summary="Root endpoint",
         description="Welcome message and API information")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Python Containerization API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health",
         response_model=HealthCheck,
         summary="Health check",
         description="Check API health and status")
async def health_check():
    """Health check endpoint for monitoring."""
    uptime = time.time() - app_start_time
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        uptime=uptime
    )


@app.get("/health/ready",
         summary="Readiness check",
         description="Check if API is ready to serve requests")
async def readiness_check():
    """Readiness check for container orchestration."""
    try:
        # Check database connection (simulated)
        await asyncio.sleep(0.01)  # Simulate DB check
        return {"status": "ready", "timestamp": datetime.now()}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not ready"
        )


@app.get("/users",
         response_model=List[User],
         dependencies=[Depends(verify_token)],
         summary="Get all users",
         description="Retrieve all users (requires authentication)")
async def get_users():
    """Get all users with authentication."""
    logger.info("Fetching all users")
    return users_db


@app.post("/users",
          response_model=User,
          status_code=status.HTTP_201_CREATED,
          dependencies=[Depends(verify_token)],
          summary="Create user",
          description="Create a new user (requires authentication)")
async def create_user(user: UserCreate):
    """Create a new user."""
    # Simulate async database operation
    await asyncio.sleep(0.1)

    # Check if user already exists
    if any(u.email == user.email for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    new_user = User(
        id=len(users_db) + 1,
        name=user.name,
        email=user.email,
        created_at=datetime.now()
    )

    users_db.append(new_user)
    logger.info(f"Created user: {new_user.email}")

    return new_user


@app.get("/users/{user_id}",
         response_model=User,
         dependencies=[Depends(verify_token)],
         summary="Get user by ID",
         description="Retrieve a specific user by ID (requires authentication)")
async def get_user(user_id: int):
    """Get a specific user by ID."""
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@app.delete("/users/{user_id}",
            dependencies=[Depends(verify_token)],
            summary="Delete user",
            description="Delete a user by ID (requires authentication)")
async def delete_user(user_id: int):
    """Delete a user by ID."""
    global users_db
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    users_db = [u for u in users_db if u.id != user_id]
    logger.info(f"Deleted user: {user_id}")

    return {"message": "User deleted successfully"}


@app.get("/simulate-error",
         summary="Simulate error",
         description="Endpoint to test error handling")
async def simulate_error():
    """Simulate an error for testing."""
    logger.error("Simulated error triggered")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="This is a simulated error"
    )


@app.get("/simulate-slow",
         summary="Simulate slow endpoint",
         description="Endpoint to test performance monitoring")
async def simulate_slow():
    """Simulate a slow endpoint for testing."""
    logger.info("Slow endpoint called")
    await asyncio.sleep(2)  # Simulate slow processing
    return {"message": "This endpoint was intentionally slow"}

# Startup event


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("FastAPI application starting up...")

    # Create sample data
    sample_users = [
        UserCreate(name="John Doe", email="john@example.com"),
        UserCreate(name="Jane Smith", email="jane@example.com")
    ]

    for user_data in sample_users:
        new_user = User(
            id=len(users_db) + 1,
            name=user_data.name,
            email=user_data.email,
            created_at=datetime.now()
        )
        users_db.append(new_user)

    logger.info(f"Created {len(sample_users)} sample users")

# Shutdown event


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("FastAPI application shutting down...")
    # Cleanup resources here

if __name__ == "__main__":
    import uvicorn

    # Configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
