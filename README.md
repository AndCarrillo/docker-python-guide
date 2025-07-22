# Develop your app

> **Module branch:** `module-02-develop`

Learn how to develop your Python application locally using containers.

## What you'll learn

In this module, you will:

- ✅ Set up local development environment with Docker Compose
- ✅ Configure hot reload and live debugging in containers
- ✅ Manage environment variables and secrets
- ✅ Integrate databases and external services

## Examples

This module includes two progressive examples:

### �️ Flask + PostgreSQL Example

**Location:** `examples/flask-postgres/`

A Flask application with database integration demonstrating local development patterns.

### ⚡ FastAPI + Redis Example

**Location:** `examples/fastapi-redis/`

An advanced FastAPI application with caching layer and async database operations.

## Prerequisites

Before starting this module, make sure you have:

- Completed [Module 1: Containerize your app](../../tree/module-01-containerize)
- Docker Desktop installed and running
- Docker Compose installed (included with Docker Desktop)
- Basic understanding of databases and environment variables

## Getting Started

1. **Clone and switch to this module:**

   ```bash
   git clone https://github.com/AndCarrillo/docker-python-guide.git
   cd docker-python-guide
   git checkout module-02-develop
   ```

2. **Follow the step-by-step guide below** ⬇️

---

## 📚 Step-by-Step Guide

### Step 1: Understanding Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. It uses a YAML file to configure your application's services.

**Key benefits for development:**

- **Multiple services** - Run app, database, cache together
- **Service networking** - Automatic service discovery
- **Volume management** - Persist data and enable hot reload
- **Environment variables** - Easy configuration management

### Step 2: Basic Docker Compose Structure

A typical `docker-compose.yml` for development includes:

```yaml
version: "3.8"

services:
  # Your application
  web:
    build: . # Build from Dockerfile
    ports:
      - "5000:5000" # Port mapping
    environment:
      - ENVIRONMENT=development
    volumes:
      - .:/app # Hot reload
    depends_on:
      - db # Service dependency

  # Database service
  db:
    image: postgres:15-alpine # Use official image
    environment:
      - POSTGRES_DB=devdb
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data: # Named volume
```

### Step 3: Service Communication

Services in Docker Compose can communicate using service names:

```python
# Instead of localhost, use service name
DATABASE_URL = "postgresql://user:pass@db:5432/devdb"
REDIS_HOST = "redis"
```

**Why this works:**

- Docker Compose creates a network automatically
- Services are accessible by their service name
- Internal port is used (not mapped port)

### Step 4: Development Optimizations

**Hot reload with volume mounting:**

```yaml
volumes:
  - .:/app # Mount source code for live changes
```

**Environment variables:**

```yaml
environment:
  - FLASK_DEBUG=1
  - ENVIRONMENT=development
```

**Service dependencies:**

```yaml
depends_on:
  - db # Start database before web app
```

---

## 🧩 Examples

### Flask + PostgreSQL Example

**Purpose:** Learn local development with database integration.

**Key concepts:**

- Docker Compose with multiple services
- Database integration with SQLAlchemy
- Hot reload for development
- Database initialization with sample data

**Files:**

```
examples/flask-postgres/
├── app.py                    # Flask app with database models
├── requirements.txt          # Python dependencies
├── Dockerfile               # Development Dockerfile
├── docker-compose.yml       # Multi-service configuration
├── init.sql                 # Database initialization
├── .dockerignore           # Build optimization
└── README.md               # Example instructions
```

**Try it:**

```bash
cd examples/flask-postgres
docker-compose up --build
# Visit http://localhost:5000
# Database admin: http://localhost:8080
```

### FastAPI + Redis Example

**Purpose:** Advanced development with caching and async patterns.

**Key concepts:**

- Async FastAPI application
- Redis for caching and session storage
- Background tasks and startup events
- Development tools and admin interfaces

**Files:**

```
examples/fastapi-redis/
├── main.py                  # FastAPI app with Redis integration
├── requirements.txt         # Python dependencies
├── Dockerfile              # Development Dockerfile
├── docker-compose.yml      # Multi-service configuration
├── .dockerignore          # Build optimization
└── README.md              # Example instructions
```

**Try it:**

```bash
cd examples/fastapi-redis
docker-compose up --build
# Visit http://localhost:8000/docs
# Redis admin: http://localhost:8081
```

---

## 🔧 Common Docker Compose Commands

### Basic Operations

```bash
# Start all services
docker-compose up

# Start with build
docker-compose up --build

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Development Workflow

```bash
# View logs
docker-compose logs

# Follow logs for specific service
docker-compose logs -f web

# Execute command in running container
docker-compose exec web bash

# Scale services
docker-compose up --scale web=3
```

### Debugging

```bash
# Check service status
docker-compose ps

# View service configuration
docker-compose config

# Restart specific service
docker-compose restart web
```

---

## 🔧 Hands-on Exercises

### Exercise 1: Flask + PostgreSQL Setup

1. Navigate to `examples/flask-postgres/`
2. Start the services: `docker-compose up --build`
3. Test the API endpoints:

   ```bash
   # Get all tasks
   curl http://localhost:5000/tasks

   # Create a new task
   curl -X POST http://localhost:5000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "New task", "description": "Test task"}'
   ```

4. Access the database admin at http://localhost:8080

**Questions to explore:**

- How do services communicate with each other?
- What happens when you modify the Python code?
- How is database data persisted?

### Exercise 2: FastAPI + Redis Development

1. Navigate to `examples/fastapi-redis/`
2. Start the services: `docker-compose up --build`
3. Explore the API documentation at http://localhost:8000/docs
4. Test the caching functionality:

   ```bash
   # Create users
   curl -X POST http://localhost:8000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Test User", "email": "test@example.com"}'

   # Get cache statistics
   curl http://localhost:8000/cache/stats
   ```

5. Access Redis admin at http://localhost:8081

**Questions to explore:**

- How does Redis caching improve performance?
- What happens when you restart only the Redis service?
- How do async operations work with external services?

### Exercise 3: Environment Customization

1. Create a `.env` file in either example
2. Override default environment variables
3. Test different configurations (production vs development)
4. Experiment with different service configurations

---

## 🎯 Key Takeaways

After completing this module, you should understand:

1. **Docker Compose Fundamentals** - Multi-container application orchestration
2. **Service Communication** - How containers communicate in development
3. **Volume Management** - Data persistence and hot reload setup
4. **Environment Configuration** - Managing different development configurations
5. **Development Workflow** - Efficient local development with containers

## 🚀 Next Steps

Ready for the next module? Continue with:

**[Module 3: Linting and typing](../../tree/module-03-linting-typing)** - Learn how to set up code quality tools with containers.

---

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Compose Best Practices](https://docs.docker.com/compose/production/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/documentation)

---

## 🤝 Need Help?

- 📖 Check the [main README](../../README.md) for general guidance
- 🐛 [Open an issue](../../issues) if you find problems
- 💬 [Start a discussion](../../discussions) for questions

---

**⬅️ [Back to main guide](../../README.md)**

Configuración de entorno de desarrollo local:

- Docker Compose para desarrollo
- Hot reload y debugging
- Gestión de variables de entorno
- Integración con bases de datos

**🔗 [Ir al módulo →](../../tree/module-02-develop)**

---

### Módulo 3: Linting and typing

**Branch:** `module-03-linting-typing`

Calidad de código y mejores prácticas:

- Configuración de Black, Flake8, isort
- Type checking con mypy
- Pre-commit hooks
- Configuración de VS Code

**🔗 [Ir al módulo →](../../tree/module-03-linting-typing)**

---

### Módulo 4: CI/CD with GitHub Actions

**Branch:** `module-04-cicd`

Automatización del pipeline de desarrollo:

- Workflows de GitHub Actions
- Testing automatizado
- Build y push de imágenes Docker
- Deployment automatizado

**🔗 [Ir al módulo →](../../tree/module-04-cicd)**

---

### Módulo 5: Test your deployment

**Branch:** `module-05-deployment`

Testing y deployment en Kubernetes:

- Configuración local de Kubernetes
- Manifiestos YAML
- Testing de deployment
- Monitoring y debugging

**🔗 [Ir al módulo →](../../tree/module-05-deployment)**

---

## 🚀 Cómo usar esta guía

### Prerequisitos

- Docker Desktop instalado
- Python 3.9+ instalado
- Git configurado
- Editor de código (recomendado: VS Code)

### Navegación

1. **Secuencial**: Sigue los módulos en orden para un aprendizaje progresivo
2. **Por temas**: Ve directamente al módulo que te interese
3. **Práctica**: Cada módulo incluye ejercicios prácticos

### Estructura de branches

```
main/
├── module-01-containerize/     # Containerización básica
├── module-02-develop/          # Desarrollo local
├── module-03-linting-typing/   # Calidad de código
├── module-04-cicd/            # CI/CD Pipeline
└── module-05-deployment/      # Testing y Deployment
```

---

## 📖 Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 🤝 Contribuciones

¿Encontraste un error o tienes una sugerencia? ¡Contribuye!

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🏷️ Tags

`#docker` `#python` `#containerization` `#devops` `#cicd` `#kubernetes` `#github-actions` `#development`

---

**📅 Última actualización:** Julio 2025
**👨‍💻 Mantenido por:** Andrea Carrillo - [GitHub](https://github.com/AndCarrillo)
