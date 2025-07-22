"""
Simple FastAPI application for containerization learning.

This example demonstrates:
- Basic FastAPI setup
- Health checks
- Environment configuration
- API documentation
"""

from fastapi import FastAPI
from pydantic import BaseModel
import os
from datetime import datetime
from typing import Dict

# Create FastAPI app
app = FastAPI(
    title="Python Docker Guide - FastAPI",
    description="A sample FastAPI application for learning containerization",
    version="1.0.0"
)

# Pydantic models


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    environment: str
    version: str


class MessageResponse(BaseModel):
    message: str
    framework: str
    environment: str
    timestamp: datetime

# Routes


@app.get("/", response_model=MessageResponse)
async def root():
    """Root endpoint returning welcome message."""
    return MessageResponse(
        message="Hello from Dockerized FastAPI!",
        framework="FastAPI",
        environment=os.getenv("ENVIRONMENT", "development"),
        timestamp=datetime.now()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        environment=os.getenv("ENVIRONMENT", "development"),
        version="1.0.0"
    )


@app.get("/info")
async def info() -> Dict[str, str]:
    """Application information endpoint."""
    return {
        "app_name": "FastAPI Docker Example",
        "framework": "FastAPI",
        "python_version": os.getenv("PYTHON_VERSION", "3.11"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
