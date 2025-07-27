# Flask Minimal App – Module 1: Containerization

This is a minimal Flask application for Module 2 (Development) of the Docker Python Guide. It demonstrates how to containerize and develop a basic Python web app using Flask and Docker Compose with hot reload.

## Features

- Minimal Flask app with a root (`/`) and health check (`/health`) endpoint
- No database, no advanced features
- Ready to build and run with Docker
- Docker Compose for development
- Hot reload support for local development

## Files

- `app.py` – Main Flask application
- `requirements.txt` – Python dependencies (Flask, python-dotenv, debugpy)
- `Dockerfile` – Minimal Dockerfile for Python 3.11
- `.dockerignore` – Ignore Python cache and virtual environment files
- `docker-compose.yml` – Development workflow with hot reload

## Usage

### Development with Docker Compose (hot reload)

```sh
docker compose up --build
```

The app will be available at [http://localhost:5000](http://localhost:5000)

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
docker build -t flask-minimal-app .
docker run -p 5000:5000 flask-minimal-app
```

---

## Integración continua (CI)

Este proyecto incluye un workflow de GitHub Actions en `.github/workflows/ci.yml` que ejecuta automáticamente:
- Instalación de dependencias
- Linting (`flake8`)
- Formateo (`black --check`)
- Type checking (`mypy`)
- Tests (`pytest`)
- Build de la imagen Docker

El workflow se ejecuta en cada push o pull request sobre la carpeta `flask-app`.

---

---

This project is intentionally minimal for learning containerization and development basics. Advanced features are introduced in later modules.
