# FastAPI Minimal App – Module 1: Containerization

This is a minimal FastAPI application for Module 2 (Development) of the Docker Python Guide. It demonstrates how to containerize and develop a basic Python web app using FastAPI and Docker Compose with hot reload.

## Features

- Minimal FastAPI app with a root (`/`) and health check (`/health`) endpoint
- No database, no advanced features
- Ready to build and run with Docker
- Docker Compose for development
- Hot reload support for local development

## Files

- `main.py` – Main FastAPI application
- `requirements.txt` – Python dependencies (FastAPI, Uvicorn, watchfiles, debugpy)
- `Dockerfile` – Minimal Dockerfile for Python 3.11
- `.dockerignore` – Ignore Python cache and virtual environment files
- `docker-compose.yml` – Development workflow with hot reload

## Usage

### Development with Docker Compose (hot reload)

```sh
docker compose up --build
```

The app will be available at [http://localhost:8000](http://localhost:8000)

---

## Testing

This project uses [pytest](https://docs.pytest.org/) for testing.

### Run tests

```sh
pytest
```

All tests are in the `tests/` directory.

---

## Code Quality: Linting, Formatting, and Type Checking

This project uses [pre-commit](https://pre-commit.com/) to automate code quality checks:

- **Black**: Code formatter
- **Flake8**: Linting
- **Mypy**: Type checking

### Setup pre-commit hooks

Install pre-commit and set up the hooks:

```sh
pip install pre-commit
pre-commit install
```

You can also run all checks manually:

```sh
pre-commit run --all-files
```

---

### Build and Run Standalone Docker Image

```sh
docker build -t fastapi-minimal-app .
docker run -p 8000:8000 fastapi-minimal-app
```

---

---

This project is intentionally minimal for learning containerization and development basics. Advanced features are introduced in later modules.
