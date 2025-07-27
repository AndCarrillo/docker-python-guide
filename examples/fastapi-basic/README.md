# FastAPI Basic Example

This is a basic FastAPI application demonstrating containerization with Docker.

## Features

- Simple FastAPI application with two endpoints
- Health check endpoint
- Optimized Docker configuration
- Non-root user for security

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

Visit: http://localhost:8000

### Docker

```bash
# Build the image
docker build -t fastapi-basic .

# Run the container
docker run -p 8000:8000 fastapi-basic
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation
