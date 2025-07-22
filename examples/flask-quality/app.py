"""
Flask application with comprehensive type annotations and quality tools.

This module demonstrates best practices for:
- Type annotations with Flask
- SQLAlchemy model typing
- Error handling with proper types
- Code quality integration
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database configuration with type annotations
DATABASE_URL: str = os.getenv(
    'DATABASE_URL', 
    'postgresql://user:password@localhost:5432/devdb'
)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Type aliases for better readability
JsonResponse = Dict[str, Any]
TaskDict = Dict[str, Union[int, str, bool]]


class Task(db.Model):  # type: ignore[name-defined]
    """Task model with comprehensive type annotations."""
    
    __tablename__ = 'tasks'
    
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(100), nullable=False)
    description: Optional[str] = db.Column(db.Text, nullable=True)
    completed: bool = db.Column(db.Boolean, default=False, nullable=False)
    created_at: datetime = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        nullable=False
    )
    
    def to_dict(self) -> TaskDict:
        """Convert task instance to dictionary with proper typing."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description or '',
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self) -> str:
        """String representation of the task."""
        return f'<Task {self.id}: {self.title}>'


# Route handlers with proper type annotations
@app.route('/')
def home() -> Response:
    """Home endpoint with environment information."""
    response_data: JsonResponse = {
        "message": "Flask Quality Example - Type-safe and well-formatted",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "Connected" if _check_db_connection() else "Not connected",
        "version": "1.0.0"
    }
    return jsonify(response_data)


@app.route('/health')
def health() -> Response:
    """Health check endpoint with comprehensive status."""
    try:
        db_status = "healthy" if _check_db_connection() else "unhealthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = f"unhealthy: {str(e)}"
    
    health_data: JsonResponse = {
        "status": "healthy",
        "service": "flask-quality-app",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }
    return jsonify(health_data)


@app.route('/tasks', methods=['GET'])
def get_tasks() -> Response:
    """Get all tasks with proper error handling."""
    try:
        tasks: List[Task] = Task.query.all()
        task_list: List[TaskDict] = [task.to_dict() for task in tasks]
        
        logger.info(f"Retrieved {len(task_list)} tasks")
        return jsonify(task_list)
    
    except Exception as e:
        logger.error(f"Error retrieving tasks: {e}")
        error_response: JsonResponse = {
            "error": "Failed to retrieve tasks",
            "details": str(e)
        }
        return jsonify(error_response), 500


@app.route('/tasks', methods=['POST'])
def create_task() -> Response:
    """Create a new task with input validation."""
    try:
        data: Optional[Dict[str, Any]] = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if 'title' not in data or not data['title'].strip():
            return jsonify({"error": "Title is required and cannot be empty"}), 400
        
        # Create task with validated data
        task = Task(
            title=str(data['title']).strip(),
            description=data.get('description', '').strip() or None
        )
        
        db.session.add(task)
        db.session.commit()
        
        logger.info(f"Created task: {task.title}")
        return jsonify(task.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating task: {e}")
        error_response: JsonResponse = {
            "error": "Failed to create task",
            "details": str(e)
        }
        return jsonify(error_response), 500


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int) -> Response:
    """Get a specific task by ID."""
    try:
        task: Optional[Task] = Task.query.get(task_id)
        
        if not task:
            return jsonify({"error": f"Task {task_id} not found"}), 404
        
        logger.info(f"Retrieved task: {task.title}")
        return jsonify(task.to_dict())
    
    except Exception as e:
        logger.error(f"Error retrieving task {task_id}: {e}")
        error_response: JsonResponse = {
            "error": f"Failed to retrieve task {task_id}",
            "details": str(e)
        }
        return jsonify(error_response), 500


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int) -> Response:
    """Update an existing task with validation."""
    try:
        task: Optional[Task] = Task.query.get(task_id)
        
        if not task:
            return jsonify({"error": f"Task {task_id} not found"}), 404
        
        data: Optional[Dict[str, Any]] = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Update fields if provided
        if 'title' in data:
            title = str(data['title']).strip()
            if not title:
                return jsonify({"error": "Title cannot be empty"}), 400
            task.title = title
        
        if 'description' in data:
            task.description = str(data['description']).strip() or None
        
        if 'completed' in data:
            task.completed = bool(data['completed'])
        
        db.session.commit()
        
        logger.info(f"Updated task: {task.title}")
        return jsonify(task.to_dict())
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating task {task_id}: {e}")
        error_response: JsonResponse = {
            "error": f"Failed to update task {task_id}",
            "details": str(e)
        }
        return jsonify(error_response), 500


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int) -> Response:
    """Delete a task by ID."""
    try:
        task: Optional[Task] = Task.query.get(task_id)
        
        if not task:
            return jsonify({"error": f"Task {task_id} not found"}), 404
        
        task_title = task.title
        db.session.delete(task)
        db.session.commit()
        
        logger.info(f"Deleted task: {task_title}")
        return '', 204
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting task {task_id}: {e}")
        error_response: JsonResponse = {
            "error": f"Failed to delete task {task_id}",
            "details": str(e)
        }
        return jsonify(error_response), 500


def _check_db_connection() -> bool:
    """Check if database connection is working."""
    try:
        db.session.execute('SELECT 1')
        return True
    except Exception:
        return False


# Database initialization
@app.before_first_request
def create_tables() -> None:
    """Create database tables on first request."""
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
