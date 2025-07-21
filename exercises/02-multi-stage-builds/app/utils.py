"""
Utility functions for the Task Manager API.

This module contains helper functions and utilities used
throughout the Task Manager API application.
"""

import time
import hashlib
import secrets
import logging
from typing import Dict, Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)


def get_current_timestamp() -> float:
    """Get the current timestamp as a float."""
    return time.time()


def generate_task_id() -> str:
    """Generate a unique task ID using current timestamp and random bytes."""
    timestamp = str(int(time.time() * 1000))  # Milliseconds
    random_bytes = secrets.token_hex(4)  # 8 characters
    return f"{timestamp}-{random_bytes}"


def calculate_completion_rate(total_tasks: int, completed_tasks: int) -> float:
    """Calculate the completion rate as a percentage."""
    if total_tasks == 0:
        return 0.0
    return round((completed_tasks / total_tasks) * 100, 2)


def hash_string(input_string: str) -> str:
    """Generate a SHA-256 hash of the input string."""
    return hashlib.sha256(input_string.encode()).hexdigest()


def format_duration(seconds: float) -> str:
    """Format duration in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def validate_task_data(task_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate task data and return any validation errors.

    Args:
        task_data: Dictionary containing task data

    Returns:
        Dictionary of field names to error messages
    """
    errors = {}

    # Validate title
    title = task_data.get('title', '').strip()
    if not title:
        errors['title'] = 'Title is required and cannot be empty'
    elif len(title) > 200:
        errors['title'] = 'Title cannot exceed 200 characters'

    # Validate description
    description = task_data.get('description', '')
    if description and len(description) > 1000:
        errors['description'] = 'Description cannot exceed 1000 characters'

    # Validate priority
    valid_priorities = ['low', 'medium', 'high', 'urgent']
    priority = task_data.get('priority', 'medium').lower()
    if priority not in valid_priorities:
        errors['priority'] = f'Priority must be one of: {", ".join(valid_priorities)}'

    return errors


def log_request(func):
    """Decorator to log API requests and responses."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()

        # Log request start
        logger.info(f"Starting {func.__name__}")

        try:
            # Execute the function
            result = await func(*args, **kwargs)

            # Log successful completion
            duration = time.time() - start_time
            logger.info(f"Completed {func.__name__} in {duration:.3f}s")

            return result

        except Exception as e:
            # Log error
            duration = time.time() - start_time
            logger.error(
                f"Error in {func.__name__} after {duration:.3f}s: {str(e)}")
            raise

    return wrapper


def sanitize_input(input_string: str) -> str:
    """
    Sanitize input string by removing potentially harmful characters.

    Args:
        input_string: String to sanitize

    Returns:
        Sanitized string
    """
    if not input_string:
        return ""

    # Remove null bytes and control characters
    sanitized = ''.join(char for char in input_string if ord(
        char) >= 32 or char in '\t\n\r')

    # Trim whitespace
    sanitized = sanitized.strip()

    return sanitized


def get_task_summary(tasks: list) -> Dict[str, Any]:
    """
    Generate a summary of tasks.

    Args:
        tasks: List of task objects

    Returns:
        Dictionary containing task statistics
    """
    total = len(tasks)
    completed = sum(1 for task in tasks if task.completed)
    pending = total - completed

    return {
        'total_tasks': total,
        'completed_tasks': completed,
        'pending_tasks': pending,
        'completion_rate': calculate_completion_rate(total, completed),
        'last_updated': get_current_timestamp()
    }


def filter_tasks(tasks: list,
                 completed: Optional[bool] = None,
                 priority: Optional[str] = None,
                 search: Optional[str] = None) -> list:
    """
    Filter tasks based on various criteria.

    Args:
        tasks: List of task objects to filter
        completed: Filter by completion status
        priority: Filter by priority level
        search: Search term to match in title or description

    Returns:
        Filtered list of tasks
    """
    filtered_tasks = tasks.copy()

    # Filter by completion status
    if completed is not None:
        filtered_tasks = [
            task for task in filtered_tasks if task.completed == completed]

    # Filter by priority
    if priority:
        priority_lower = priority.lower()
        filtered_tasks = [task for task in filtered_tasks
                          if hasattr(task, 'priority') and task.priority.lower() == priority_lower]

    # Filter by search term
    if search:
        search_lower = search.lower()
        filtered_tasks = [
            task for task in filtered_tasks
            if search_lower in task.title.lower() or
            (task.description and search_lower in task.description.lower())
        ]

    return filtered_tasks


def paginate_tasks(tasks: list, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """
    Paginate a list of tasks.

    Args:
        tasks: List of tasks to paginate
        page: Page number (1-based)
        per_page: Number of items per page

    Returns:
        Dictionary containing paginated results
    """
    total = len(tasks)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    paginated_tasks = tasks[start_index:end_index]

    return {
        'tasks': paginated_tasks,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page,
        'has_next': end_index < total,
        'has_prev': page > 1
    }


class PerformanceTimer:
    """Context manager for measuring execution time."""

    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.time()
        logger.debug(f"Starting {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time

        if exc_type:
            logger.error(f"{self.name} failed after {duration:.3f}s")
        else:
            logger.debug(f"{self.name} completed in {duration:.3f}s")

    @property
    def duration(self) -> Optional[float]:
        """Get the duration of the operation."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
