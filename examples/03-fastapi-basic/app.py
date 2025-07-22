"""
Simple FastAPI application demonstrating basic containerization.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
from datetime import datetime

app = FastAPI(
    title="FastAPI Basic Example",
    description="A simple FastAPI application for Docker demonstration",
    version="1.0.0"
)

# In-memory storage for demo purposes
tasks = []


class Task(BaseModel):
    id: str = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = None


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


@app.get("/")
async def root():
    """Welcome endpoint."""
    return {
        "message": "FastAPI Basic Example",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "fastapi-basic-app",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks."""
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task."""
    new_task = Task(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        created_at=datetime.now()
    )
    tasks.append(new_task)
    return new_task


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a specific task."""
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, completed: bool):
    """Update task completion status."""
    for task in tasks:
        if task.id == task_id:
            task.completed = completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task."""
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
