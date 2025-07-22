"""
FastAPI CI/CD Demo Application

A production-ready FastAPI application demonstrating:
- Async database operations with SQLAlchemy
- Redis caching and session management
- Background tasks with Celery
- Comprehensive API documentation
- Health checks and monitoring
- Modern Python async patterns
"""
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import List, Optional

import asyncpg
import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, String, Text, select, func
import structlog
import os
from typing import AsyncGenerator
import json

# Logging configuration
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/fastapicd")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Database models


class Base(DeclarativeBase):
    pass


class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

# Pydantic models


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="Item name")
    description: Optional[str] = Field(
        None, max_length=1000, description="Item description")


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"


class ReadinessResponse(BaseModel):
    status: str
    database: str
    redis: str
    timestamp: datetime


# Global variables
engine = None
async_session = None
redis_client = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    global engine, async_session, redis_client

    logger.info("Starting FastAPI application")

    # Initialize database
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_size=10,
        max_overflow=20
    )
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Initialize Redis
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)

    logger.info("Application startup complete")
    yield

    # Cleanup
    logger.info("Shutting down application")
    if redis_client:
        await redis_client.close()
    if engine:
        await engine.dispose()

# FastAPI app
app = FastAPI(
    title="FastAPI CI/CD Demo",
    description="A production-ready FastAPI application with comprehensive CI/CD pipeline",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Background task example


async def log_item_creation(item_name: str) -> None:
    """Background task to log item creation."""
    await asyncio.sleep(1)  # Simulate some processing
    logger.info("Item created in background", item_name=item_name)

# Health check endpoints


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Basic health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow()
    )


@app.get("/ready", response_model=ReadinessResponse, tags=["Health"])
async def readiness_check() -> ReadinessResponse:
    """Readiness check endpoint that verifies all dependencies."""
    db_status = "disconnected"
    redis_status = "disconnected"

    # Check database
    try:
        async with async_session() as session:
            result = await session.execute(select(func.count()).select_from(ItemModel))
            db_status = "connected"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))

    # Check Redis
    try:
        await redis_client.ping()
        redis_status = "connected"
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))

    status_code = "ready" if db_status == "connected" and redis_status == "connected" else "not ready"

    response = ReadinessResponse(
        status=status_code,
        database=db_status,
        redis=redis_status,
        timestamp=datetime.utcnow()
    )

    if status_code == "not ready":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=response.model_dump()
        )

    return response

# API endpoints


@app.get("/", tags=["Root"])
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "message": "FastAPI CI/CD Demo API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "ready": "/ready"
    }


@app.get("/api/items", response_model=List[ItemResponse], tags=["Items"])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
) -> List[ItemResponse]:
    """Get all items with optional pagination and caching."""
    cache_key = f"items:{skip}:{limit}"

    # Try to get from cache
    try:
        cached_items = await redis_client.get(cache_key)
        if cached_items:
            logger.info("Cache hit for items", cache_key=cache_key)
            items_data = json.loads(cached_items)
            return [ItemResponse(**item) for item in items_data]
    except Exception as e:
        logger.warning("Cache get failed", error=str(e))

    # Get from database
    try:
        result = await session.execute(
            select(ItemModel)
            .offset(skip)
            .limit(limit)
            .order_by(ItemModel.created_at.desc())
        )
        items = result.scalars().all()

        # Convert to response models
        response_items = [ItemResponse.model_validate(item) for item in items]

        # Cache the results
        try:
            cache_data = [item.model_dump(mode='json')
                          for item in response_items]
            await redis_client.setex(
                cache_key,
                300,  # 5 minutes
                json.dumps(cache_data, default=str)
            )
            logger.info("Items cached", cache_key=cache_key,
                        count=len(response_items))
        except Exception as e:
            logger.warning("Cache set failed", error=str(e))

        return response_items

    except Exception as e:
        logger.error("Failed to get items", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve items"
        )


@app.post("/api/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(
    item: ItemCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
) -> ItemResponse:
    """Create a new item."""
    try:
        # Create new item
        db_item = ItemModel(
            name=item.name,
            description=item.description
        )
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)

        # Invalidate cache
        try:
            # Find and delete all item cache keys
            keys = await redis_client.keys("items:*")
            if keys:
                await redis_client.delete(*keys)
                logger.info("Cache invalidated after item creation",
                            keys_count=len(keys))
        except Exception as e:
            logger.warning("Cache invalidation failed", error=str(e))

        # Add background task
        background_tasks.add_task(log_item_creation, item.name)

        logger.info("Item created", item_id=db_item.id, item_name=db_item.name)
        return ItemResponse.model_validate(db_item)

    except Exception as e:
        await session.rollback()
        logger.error("Failed to create item", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create item"
        )


@app.get("/api/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def get_item(
    item_id: int,
    session: AsyncSession = Depends(get_session)
) -> ItemResponse:
    """Get a specific item by ID."""
    cache_key = f"item:{item_id}"

    # Try cache first
    try:
        cached_item = await redis_client.get(cache_key)
        if cached_item:
            logger.info("Cache hit for item", item_id=item_id)
            return ItemResponse(**json.loads(cached_item))
    except Exception as e:
        logger.warning("Cache get failed", error=str(e))

    # Get from database
    try:
        result = await session.execute(
            select(ItemModel).where(ItemModel.id == item_id)
        )
        item = result.scalar_one_or_none()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )

        response_item = ItemResponse.model_validate(item)

        # Cache the item
        try:
            await redis_client.setex(
                cache_key,
                600,  # 10 minutes
                json.dumps(response_item.model_dump(mode='json'), default=str)
            )
        except Exception as e:
            logger.warning("Cache set failed", error=str(e))

        return response_item

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get item", item_id=item_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve item"
        )

# Error handlers


@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found",
                 "detail": "The requested resource was not found"}
    )


@app.exception_handler(405)
async def method_not_allowed_handler(request, exc):
    return JSONResponse(
        status_code=405,
        content={"error": "Method not allowed",
                 "detail": "The method is not allowed for this endpoint"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error("Internal server error", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error",
                 "detail": "An internal error occurred"}
    )

if __name__ == "__main__":
    import asyncio

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None  # Use structlog instead
    )
