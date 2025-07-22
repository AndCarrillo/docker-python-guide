"""
Flask CI/CD Example Application

A production-ready Flask application demonstrating CI/CD best practices.
"""

import logging
import os
from typing import Dict, Any

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://user:password@localhost:5432/flaskcicd'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Redis connection
redis_client = redis.from_url(app.config['REDIS_URL'])


# Models
class Task(db.Model):
    """Task model for demonstration purposes."""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# Routes
@app.route('/health')
def health_check() -> Dict[str, str]:
    """Health check endpoint for load balancers."""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        
        # Check Redis connection
        redis_client.ping()
        
        return jsonify({'status': 'healthy', 'version': '1.0.0'})
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503


@app.route('/api/tasks', methods=['GET'])
def get_tasks() -> Dict[str, Any]:
    """Get all tasks."""
    try:
        tasks = Task.query.all()
        return jsonify({
            'tasks': [task.to_dict() for task in tasks],
            'count': len(tasks)
        })
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        return jsonify({'error': 'Failed to retrieve tasks'}), 500


@app.route('/api/tasks', methods=['POST'])
def create_task() -> Dict[str, Any]:
    """Create a new task."""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        task = Task(
            title=data['title'],
            description=data.get('description', '')
        )
        
        db.session.add(task)
        db.session.commit()
        
        # Cache the task count
        redis_client.set('task_count', Task.query.count())
        
        return jsonify(task.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create task'}), 500


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int) -> Dict[str, Any]:
    """Update a task."""
    try:
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']
        
        db.session.commit()
        
        return jsonify(task.to_dict())
        
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update task'}), 500


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int) -> Dict[str, str]:
    """Delete a task."""
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        
        # Update cached task count
        redis_client.set('task_count', Task.query.count())
        
        return jsonify({'message': 'Task deleted successfully'})
        
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete task'}), 500


@app.route('/api/stats')
def get_stats() -> Dict[str, Any]:
    """Get application statistics."""
    try:
        # Try to get from cache first
        cached_count = redis_client.get('task_count')
        
        if cached_count:
            total_tasks = int(cached_count)
        else:
            total_tasks = Task.query.count()
            redis_client.set('task_count', total_tasks)
        
        completed_tasks = Task.query.filter_by(completed=True).count()
        
        return jsonify({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': total_tasks - completed_tasks,
            'completion_rate': round(completed_tasks / total_tasks * 100, 2) if total_tasks > 0 else 0
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500


if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
