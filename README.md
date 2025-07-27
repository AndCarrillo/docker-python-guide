# Module 3: Linting and typing

> **Module branch:** `module-03-linting-typing`

## Prerequisites

Complete [Module 2: Develop your app](../../tree/module-02-develop).

## Overview

Learn to set up code quality tools for your Python application:

- Linting and formatting with Ruff
- Static type checking with Pyright
- Pre-commit hooks for automated checks
- Container integration for development

## 🚀 Choose Your Development Path

| Framework                 | Purpose               | Learning Focus                                         | Start Learning                                            |
| ------------------------- | --------------------- | ------------------------------------------------------ | --------------------------------------------------------- |
| 🧪 **Flask + Quality**    | Traditional web apps  | Type hints, linting, SQL app quality                   | [→ Start with Flask](#option-1-flask--quality-tools-example) |
| ⚡ **FastAPI + Advanced**  | High-performance APIs | Strict typing, async patterns, modern quality tools    | [→ Start with FastAPI](#option-2-fastapi--type-safety-example) |

> **New to code quality?** → Choose Flask | **Want advanced typing?** → Choose FastAPI

## Set up code quality tools

In this section, you'll enhance your applications from Module 2 with code quality tools. This includes linting, formatting, type checking, and automated quality checks.

### Option 1: Flask + Quality Tools Example

Navigate to the Flask quality example directory:

```bash
cd examples/flask-quality
```

In the `examples/flask-quality` directory, you'll find your completed Flask application from Module 2. Now you'll enhance it with code quality tools.

#### Step 1: Configure Ruff for linting and formatting

First, update your `pyproject.toml` file with Ruff configuration:

```toml
[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by formatter
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-source-first-line = false
line-ending = "auto"
```

Install the development tools:

```bash
pip install -r requirements-dev.txt
```

Run Ruff to check your code:

```bash
# Check for linting issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Format your code
ruff format .
```

#### Step 2: Add type annotations to your Flask app

Update your `app.py` to include proper type annotations:

```python
from __future__ import annotations

from typing import Any, Dict, List, Optional
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database configuration with type annotations
DATABASE_URL: str = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:mysecretpassword@localhost:5432/flask_dev'
)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models with type annotations
class Task(db.Model):
    __tablename__ = 'task'
    
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(100), nullable=False)
    description: Optional[str] = db.Column(db.Text)
    completed: bool = db.Column(db.Boolean, default=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

# Routes with type annotations
@app.route('/')
def home() -> Response:
    return jsonify({"message": "Hello from Flask in Docker!", "status": "running"})

@app.route('/tasks', methods=['GET'])
def get_tasks() -> Response:
    tasks: List[Task] = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks', methods=['POST'])
def create_task() -> tuple[Response, int] | tuple[Response, int]:
    data: Optional[Dict[str, Any]] = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False)
    )
    
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# Initialize database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### Step 3: Configure Pyright for type checking

Add Pyright configuration to your `pyproject.toml`:

```toml
[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv", "__pycache__"]
reportMissingTypeStubs = false
```

Run type checking:

```bash
pyright
```

#### Step 4: Set up pre-commit hooks

Update your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.2
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

Install and activate pre-commit:

```bash
pre-commit install
```

Now, run the following docker compose up command to start your application:

```bash
docker compose up --build
```

### Option 2: FastAPI + Quality Tools Example

Navigate to the FastAPI quality example directory:

```bash
cd examples/fastapi-quality
```

In the `examples/fastapi-quality` directory, you'll find your completed FastAPI application from Module 2. Now you'll enhance it with code quality tools.

#### Step 1: Configure Ruff for linting and formatting

First, update your `pyproject.toml` file with Ruff configuration:

```toml
[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by formatter
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-source-first-line = false
line-ending = "auto"
```

Install the development tools:

```bash
pip install -r requirements-dev.txt
```

Run Ruff to check your code:

```bash
# Check for linting issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Format your code
ruff format .
```

#### Step 2: Add type annotations to your FastAPI app

Update your `main.py` to include proper type annotations:

```python
from __future__ import annotations

from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import json
import os

app = FastAPI(title="User Management API", version="1.0.0")

# Redis configuration with type annotations
REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_client: redis.Redis[bytes] = redis.from_url(REDIS_URL, decode_responses=False)

# Pydantic models with proper type annotations
class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None

class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

# In-memory storage with type annotations
users_db: Dict[int, User] = {}
next_user_id: int = 1

# Helper functions with type annotations  
def get_user_cache_key(user_id: int) -> str:
    return f"user:{user_id}"

def cache_user(user: User) -> None:
    """Cache user data in Redis"""
    cache_key = get_user_cache_key(user.id)
    user_data = user.model_dump_json()
    redis_client.setex(cache_key, 300, user_data)  # Cache for 5 minutes

def get_cached_user(user_id: int) -> Optional[User]:
    """Get user from Redis cache"""
    cache_key = get_user_cache_key(user_id)
    cached_data = redis_client.get(cache_key)
    if cached_data:
        user_dict = json.loads(cached_data.decode('utf-8'))
        return User(**user_dict)
    return None

def invalidate_user_cache(user_id: int) -> None:
    """Remove user from Redis cache"""
    cache_key = get_user_cache_key(user_id)
    redis_client.delete(cache_key)

# API routes with type annotations
@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello from FastAPI in Docker!", "status": "running"}

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate) -> User:
    global next_user_id
    
    # Check if email already exists
    for existing_user in users_db.values():
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(id=next_user_id, **user.model_dump())
    users_db[next_user_id] = new_user
    cache_user(new_user)
    next_user_id += 1
    return new_user

@app.get("/users/", response_model=List[User])
async def get_users() -> List[User]:
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int) -> User:
    # Try to get from cache first
    cached_user = get_cached_user(user_id)
    if cached_user:
        return cached_user
    
    # If not in cache, get from database
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    cache_user(user)  # Cache the user for next time
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate) -> User:
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Check email uniqueness if email is being updated
    if 'email' in update_data:
        for uid, existing_user in users_db.items():
            if uid != user_id and existing_user.email == update_data['email']:
                raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update user data
    for field, value in update_data.items():
        setattr(user, field, value)
    
    invalidate_user_cache(user_id)  # Remove from cache to force refresh
    cache_user(user)  # Cache updated user
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int) -> Dict[str, str]:
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del users_db[user_id]
    invalidate_user_cache(user_id)
    return {"message": "User deleted successfully"}

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint that includes Redis connectivity"""
    try:
        redis_client.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "redis": redis_status,
        "users_count": len(users_db)
    }
```

#### Step 3: Configure Pyright for type checking

Add Pyright configuration to your `pyproject.toml`:

```toml
[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv", "__pycache__"]
reportMissingTypeStubs = false
```

Run type checking:

```bash
pyright
```

#### Step 4: Set up pre-commit hooks

Update your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.2
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

Install and activate pre-commit:

```bash
pre-commit install
```

Now, run the following docker compose up command to start your application:

```bash
docker compose up --build
```

---

## 🔧 Common Quality Commands

### Ruff Commands

```bash
# Check for linting issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Format your code
ruff format .

# Check specific files
ruff check app.py

# Show configuration
ruff config
```

### Pyright Commands

```bash
# Type check all files
pyright

# Type check specific file
pyright app.py

# Watch mode for continuous checking
pyright --watch

# Generate type coverage report
pyright --stats
```

### Pre-commit Commands

```bash
# Install hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff

# Update hook versions
pre-commit autoupdate
```

---

## 📚 Useful Links

- **Ruff Documentation**: https://docs.astral.sh/ruff/
- **Pyright Documentation**: https://github.com/microsoft/pyright
- **Pre-commit Documentation**: https://pre-commit.com/
- **Type Hints Documentation**: https://docs.python.org/3/library/typing.html
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/

---

## 🎯 Next Steps

You've successfully set up code quality tools for your Python applications! Here's what you can explore next:

1. **Advanced typing patterns** - Generic types, protocols, and type variables
2. **Custom Ruff rules** - Create project-specific linting rules
3. **CI/CD integration** - Automate quality checks in your deployment pipeline
4. **Performance monitoring** - Add profiling and performance analysis tools
5. **Testing strategies** - Integrate quality tools with your testing framework

Continue your journey by exploring advanced Docker concepts or dive deeper into Python development best practices!
