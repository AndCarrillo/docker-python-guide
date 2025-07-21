"""
Data models for the Task Manager API.

This module defines Pydantic models used for data validation
and serialization in the Task Manager API.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(BaseModel):
    """Base task model with common fields."""
    title: str = Field(..., min_length=1, max_length=200,
                       description="Task title")
    description: Optional[str] = Field(
        None, max_length=1000, description="Task description")
    priority: TaskPriority = Field(
        TaskPriority.MEDIUM, description="Task priority")

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()


class TaskCreate(TaskBase):
    """Model for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Model for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    completed: Optional[bool] = None

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip() if v else v


class Task(TaskBase):
    """Full task model for API responses."""
    id: int = Field(..., description="Unique task identifier")
    status: TaskStatus = Field(
        TaskStatus.PENDING, description="Current task status")
    completed: bool = Field(False, description="Whether the task is completed")
    created_at: float = Field(..., description="Task creation timestamp")
    updated_at: Optional[float] = Field(
        None, description="Last update timestamp")

    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete Docker exercise",
                "description": "Finish the multi-stage builds exercise",
                "priority": "medium",
                "status": "pending",
                "completed": False,
                "created_at": 1640995200.0,
                "updated_at": None
            }
        }


class TaskList(BaseModel):
    """Model for paginated task lists."""
    tasks: List[Task] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    page: int = Field(1, description="Current page number")
    per_page: int = Field(10, description="Tasks per page")

    class Config:
        schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": 1,
                        "title": "Sample task",
                        "description": "This is a sample task",
                        "priority": "medium",
                        "status": "pending",
                        "completed": False,
                        "created_at": 1640995200.0,
                        "updated_at": None
                    }
                ],
                "total": 1,
                "page": 1,
                "per_page": 10
            }
        }


class TaskStats(BaseModel):
    """Model for task statistics."""
    total_tasks: int = Field(..., description="Total number of tasks")
    completed_tasks: int = Field(..., description="Number of completed tasks")
    pending_tasks: int = Field(..., description="Number of pending tasks")
    in_progress_tasks: int = Field(...,
                                   description="Number of in-progress tasks")
    cancelled_tasks: int = Field(..., description="Number of cancelled tasks")
    completion_rate: float = Field(...,
                                   description="Task completion rate as percentage")

    class Config:
        schema_extra = {
            "example": {
                "total_tasks": 10,
                "completed_tasks": 6,
                "pending_tasks": 3,
                "in_progress_tasks": 1,
                "cancelled_tasks": 0,
                "completion_rate": 60.0
            }
        }


class HealthCheck(BaseModel):
    """Model for health check responses."""
    status: str = Field(..., description="Service health status")
    timestamp: float = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    uptime: Optional[float] = Field(
        None, description="Service uptime in seconds")

    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": 1640995200.0,
                "version": "1.0.0",
                "uptime": 3600.0
            }
        }


class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(
        None, description="Additional error details")

    class Config:
        schema_extra = {
            "example": {
                "error": "NotFound",
                "message": "Task not found",
                "details": {"task_id": 123}
            }
        }
