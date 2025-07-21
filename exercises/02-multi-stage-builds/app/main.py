"""
Task Manager API - Main application module.

A FastAPI application for managing tasks with CRUD operations.
Demonstrates multi-stage Docker builds and production deployment.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import time
import os

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Task Manager API",
    description="A simple task management API demonstrating Docker best practices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# In-memory storage (in production, use a real database)
tasks = []
task_counter = 0


class Task(BaseModel):
    """Task model for API responses."""
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: float


class TaskCreate(BaseModel):
    """Task creation model for API requests."""
    title: str
    description: str = ""


class TaskUpdate(BaseModel):
    """Task update model for API requests."""
    title: str = None
    description: str = None
    completed: bool = None


@app.get("/",
         summary="Root endpoint",
         description="Welcome message and API information")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health",
         summary="Health check",
         description="Check API health status")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "tasks_count": len(tasks)
    }


@app.get("/tasks",
         response_model=List[Task],
         summary="Get all tasks",
         description="Retrieve all tasks")
async def get_tasks():
    """Get all tasks."""
    logger.info(f"Retrieved {len(tasks)} tasks")
    return tasks


@app.post("/tasks",
          response_model=Task,
          status_code=201,
          summary="Create task",
          description="Create a new task")
async def create_task(task: TaskCreate):
    """Create a new task."""
    global task_counter
    task_counter += 1

    new_task = Task(
        id=task_counter,
        title=task.title,
        description=task.description,
        completed=False,
        created_at=time.time()
    )

    tasks.append(new_task)
    logger.info(f"Created task: {new_task.title} (ID: {new_task.id})")
    return new_task


@app.get("/tasks/{task_id}",
         response_model=Task,
         summary="Get task by ID",
         description="Retrieve a specific task by ID")
async def get_task(task_id: int):
    """Get a specific task by ID."""
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")

    logger.info(f"Retrieved task: {task_id}")
    return task


@app.put("/tasks/{task_id}",
         response_model=Task,
         summary="Update task",
         description="Update an existing task")
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task."""
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        logger.warning(f"Task not found for update: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only provided fields
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed

    logger.info(f"Updated task: {task_id}")
    return task


@app.delete("/tasks/{task_id}",
            summary="Delete task",
            description="Delete a task by ID")
async def delete_task(task_id: int):
    """Delete a task by ID."""
    global tasks
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        logger.warning(f"Task not found for deletion: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")

    tasks = [t for t in tasks if t.id != task_id]
    logger.info(f"Deleted task: {task_id}")
    return {"message": f"Task {task_id} deleted successfully"}


@app.put("/tasks/{task_id}/complete",
         response_model=Task,
         summary="Complete task",
         description="Mark a task as completed")
async def complete_task(task_id: int):
    """Mark a task as completed."""
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        logger.warning(f"Task not found for completion: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    logger.info(f"Completed task: {task_id}")
    return task


@app.put("/tasks/{task_id}/uncomplete",
         response_model=Task,
         summary="Uncomplete task",
         description="Mark a task as not completed")
async def uncomplete_task(task_id: int):
    """Mark a task as not completed."""
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        logger.warning(f"Task not found for uncompletion: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = False
    logger.info(f"Uncompleted task: {task_id}")
    return task


@app.get("/tasks/completed",
         response_model=List[Task],
         summary="Get completed tasks",
         description="Retrieve all completed tasks")
async def get_completed_tasks():
    """Get all completed tasks."""
    completed_tasks = [t for t in tasks if t.completed]
    logger.info(f"Retrieved {len(completed_tasks)} completed tasks")
    return completed_tasks


@app.get("/tasks/pending",
         response_model=List[Task],
         summary="Get pending tasks",
         description="Retrieve all pending tasks")
async def get_pending_tasks():
    """Get all pending tasks."""
    pending_tasks = [t for t in tasks if not t.completed]
    logger.info(f"Retrieved {len(pending_tasks)} pending tasks")
    return pending_tasks

# Startup event


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Task Manager API starting up...")

    # Create some sample tasks for demonstration
    sample_tasks = [
        TaskCreate(title="Welcome to Task Manager",
                   description="This is a sample task"),
        TaskCreate(title="Learn Docker",
                   description="Complete the Docker exercises"),
        TaskCreate(title="Build containers",
                   description="Practice multi-stage builds")
    ]

    for task_data in sample_tasks:
        await create_task(task_data)

    logger.info(f"Application started with {len(tasks)} sample tasks")

# Shutdown event


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Task Manager API shutting down...")

if __name__ == "__main__":
    import uvicorn

    # Configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    logger.info(f"Starting server on {host}:{port} (debug={debug})")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level=log_level.lower()
    )
