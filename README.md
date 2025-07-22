# Module 2: Develop your app

> **Module branch:** `module-02-develop`

## Prerequisites

Complete [Module 1: Containerize your app](../../tree/module-01-containerize).

## Overview

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

- Adding a local database and persisting data
- Configuring Compose to automatically update your running Compose services as you edit and save your code
- Managing environment variables and secrets
- Implementing hot reload for development workflow

## 🚀 Choose Your Development Path

This module offers two complete development examples. Choose the one that best fits your needs:

<table>
  <tr>
    <th style="text-align: center;">🌶️ Flask + PostgreSQL</th>
    <th style="text-align: center;">⚡ FastAPI + Redis</th>
  </tr>
  <tr>
    <td>
      <strong>Best for:</strong><br>
      • Traditional web applications<br>
      • Learning SQL databases<br>
      • Simple REST APIs<br>
      • Getting started with Docker
    </td>
    <td>
      <strong>Best for:</strong><br>
      • High-performance APIs<br>
      • Async programming<br>
      • Caching strategies<br>
      • Modern Python development
    </td>
  </tr>
  <tr>
    <td>
      <strong>Technologies:</strong><br>
      • Flask web framework<br>
      • PostgreSQL database<br>
      • SQLAlchemy ORM<br>
      • Adminer (DB admin)
    </td>
    <td>
      <strong>Technologies:</strong><br>
      • FastAPI framework<br>
      • Redis cache/storage<br>
      • Async/await patterns<br>
      • Redis Commander (admin)
    </td>
  </tr>
  <tr>
    <td style="text-align: center;">
      <a href="#option-1-flask--postgresql-example">
        <strong>→ Start with Flask</strong>
      </a>
    </td>
    <td style="text-align: center;">
      <a href="#option-2-fastapi--redis-example">
        <strong>→ Start with FastAPI</strong>
      </a>
    </td>
  </tr>
</table>

> **💡 Tip:** You can follow both examples to compare different development approaches!

## Get the sample application

You already have the containerized application from Module 1. In this module, we'll enhance it with development features.

The applications you containerized in Module 1 are now ready for development enhancements:

- **Flask + PostgreSQL** - Located in `examples/flask-postgres/`
- **FastAPI + Redis** - Located in `examples/fastapi-redis/`

## Add a local database and persist data

You can use containers to set up local services, like a database. In this section, you'll update the compose.yaml file to define a database service and a volume to persist data.

### Option 1: Flask + PostgreSQL Example

Navigate to the Flask example directory:

```bash
cd examples/flask-postgres
```

In the `examples/flask-postgres` directory, open the `compose.yaml` file in an IDE or text editor. The current file from Module 1 needs to be enhanced with database services.

Update your `compose.yaml` file with the following content:

```yaml
services:
  web:
    build:
      context: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/flask_dev
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app
    secrets:
      - db-password
    develop:
      watch:
        - action: rebuild
          path: .

  db:
    image: postgres:15-alpine
    restart: always
    secrets:
      - db-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=flask_dev
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  adminer:
    image: adminer
    restart: always
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgres_data:

secrets:
  db-password:
    file: db/password.txt
```

Before you run the application using Compose, notice that this Compose file specifies a `password.txt` file to hold the database's password. You must create this file as it's not included in the source repository.

In the `examples/flask-postgres` directory, create a new directory named `db` and inside that directory create a file named `password.txt` that contains the password for the database:

```bash
mkdir -p db
echo "mysecretpassword" > db/password.txt
```

You should now have the following contents in your `examples/flask-postgres` directory:

```
examples/flask-postgres/
├── db/
│   └── password.txt
├── app.py
├── requirements.txt
├── .dockerignore
├── compose.yaml
├── Dockerfile
└── README.md
```

Now, run the following docker compose up command to start your application:

```bash
docker compose up --build
```

### Test your application

Now test your API endpoints. Open a new terminal then make requests to the server:

**Create a new task:**

```bash
curl -X 'POST' \
  'http://localhost:5000/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Learn Docker",
  "description": "Complete Module 2 of Docker Python Guide"
}'
```

You should receive a response like:

```json
{
  "id": 1,
  "title": "Learn Docker",
  "description": "Complete Module 2 of Docker Python Guide",
  "completed": false
}
```

**Get all tasks:**

```bash
curl -X 'GET' \
  'http://localhost:5000/tasks' \
  -H 'accept: application/json'
```

**Access database admin interface:**

Open http://localhost:8080 in your browser (Adminer interface):

- System: PostgreSQL
- Server: db
- Username: postgres
- Password: mysecretpassword
- Database: flask_dev

Press `Ctrl+C` in the terminal to stop your application.

---

### 🎯 Flask Example Complete!

**What you accomplished:**
- ✅ Set up Flask with PostgreSQL
- ✅ Configured Docker Compose for development
- ✅ Implemented data persistence
- ✅ Added database administration interface

**Navigation:**
- 📝 [Continue with FastAPI example](#option-2-fastapi--redis-example) to compare approaches
- 🔄 [Skip to Hot Reload section](#automatically-update-services) if you want to continue with Flask
- 📚 [View both examples side-by-side](#-examples) for comparison

---

### Option 2: FastAPI + Redis Example

Navigate to the FastAPI example directory:

```bash
cd examples/fastapi-redis
```

In the `examples/fastapi-redis` directory, open the `compose.yaml` file. Update it with the following content:

```yaml
services:
  api:
    build:
      context: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=development
    depends_on:
      redis:
        condition: service_healthy
    volumes:
      - .:/app
    develop:
      watch:
        - action: rebuild
          path: .

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data
    expose:
      - 6379
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis-admin:
    image: rediscommander/redis-commander:latest
    restart: always
    ports:
      - "8081:8081"
    environment:
      - REDIS_HOSTS=local:redis:6379
    depends_on:
      - redis

volumes:
  redis_data:
```

Start the services:

```bash
docker compose up --build
```

### Test the FastAPI application

**Create users:**

```bash
curl -X 'POST' \
  'http://localhost:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "John Doe",
  "email": "john@example.com"
}'
```

**Get users (cached):**

```bash
curl -X 'GET' \
  'http://localhost:8000/users' \
  -H 'accept: application/json'
```

**Check cache statistics:**

```bash
curl -X 'GET' \
  'http://localhost:8000/cache/stats' \
  -H 'accept: application/json'
```

**Access interfaces:**

- API Documentation: http://localhost:8000/docs
- Redis Admin: http://localhost:8081

Press `Ctrl+C` to stop the application.

---

### ⚡ FastAPI Example Complete!

**What you accomplished:**
- ✅ Set up FastAPI with Redis
- ✅ Implemented async API endpoints
- ✅ Added caching functionality
- ✅ Configured Redis administration interface

**Navigation:**
- 📝 [Compare with Flask example](#option-1-flask--postgresql-example) to see different approaches
- 🔄 [Continue to Hot Reload section](#automatically-update-services) 
- 📚 [View examples comparison](#-examples) for detailed overview

---

## Automatically update services

Use Compose Watch to automatically update your running Compose services as you edit and save your code. For more details about Compose Watch, see [Use Compose Watch](https://docs.docker.com/compose/file-watch/).

The `compose.yaml` files above already include the Compose Watch instructions in the `develop.watch` section:

```yaml
develop:
  watch:
    - action: rebuild
      path: .
```

### Test hot reload with Flask

Run your Flask application with Compose Watch:

```bash
cd examples/flask-postgres
docker compose watch
```

In a terminal, test the application:

```bash
curl http://localhost:5000/
```

Response: `Hello from Flask in Docker!`

Now open `examples/flask-postgres/app.py` in your IDE and update the home route:

```python
@app.route('/')
def home():
-    return jsonify({"message": "Hello from Flask in Docker!", "status": "running"})
+    return jsonify({"message": "Hello from Flask in Docker!!!", "status": "running"})
```

Save the changes to `app.py` and wait a few seconds for the application to rebuild. Test the application again:

```bash
curl http://localhost:5000/
```

You should see: `Hello from Flask in Docker!!!`

### Test hot reload with FastAPI

Run your FastAPI application with Compose Watch:

```bash
cd examples/fastapi-redis
docker compose watch
```

Open `examples/fastapi-redis/main.py` and update the root endpoint:

```python
@app.get("/")
async def root():
-    return {"message": "Hello from FastAPI in Docker!", "users_count": len(users)}
+    return {"message": "Hello from FastAPI in Docker!!!", "users_count": len(users)}
```

Save the file and test:

```bash
curl http://localhost:8000/
```

The changes will be reflected automatically!

Press `Ctrl+C` in the terminal to stop your application.

## Summary

In this section, you took a look at setting up your Compose file to add local services and persist data. You also learned how to use Compose Watch to automatically rebuild and run your container when you update your code.

**What you accomplished:**

- ✅ **Enhanced applications** with database integration (PostgreSQL/Redis)
- ✅ **Configured multi-service environments** using Docker Compose
- ✅ **Implemented data persistence** with Docker volumes
- ✅ **Set up hot reload** for development workflow
- ✅ **Added admin interfaces** for database management
- ✅ **Learned service communication** between containers

## Key concepts learned

### Service Communication

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

### Development Optimizations

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

## Related information

- [Compose file reference](https://docs.docker.com/compose/compose-file/)
- [Compose file watch](https://docs.docker.com/compose/file-watch/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

## Next steps

In the next section, you'll learn how you can set up linting, formatting and type checking to follow the best practices in Python apps.

**[Module 3: Linting, formatting, and type checking →](../../tree/module-03-linting-typing)**

- ✅ Set up local development environment with Docker Compose
- ✅ Configure hot reload and live debugging in containers
- ✅ Manage environment variables and secrets
- ✅ Integrate databases and external services

## 🧩 Examples

This module includes two progressive examples demonstrating different development approaches:

### Quick Comparison

| Feature | 🌶️ Flask + PostgreSQL | ⚡ FastAPI + Redis |
|---------|----------------------|-------------------|
| **Framework** | Flask (sync) | FastAPI (async) |
| **Database** | PostgreSQL (relational) | Redis (key-value) |
| **Use Case** | Traditional web apps | High-performance APIs |
| **Learning Focus** | SQL, ORM patterns | Async, caching patterns |
| **API Docs** | Manual documentation | Auto-generated (OpenAPI) |
| **Performance** | Standard | High throughput |
| **Port** | 5000 | 8000 |
| **Admin Interface** | Adminer (8080) | Redis Commander (8081) |

### 🌶️ Flask + PostgreSQL Example

**Location:** `examples/flask-postgres/`

**Perfect for learning:**
- Traditional web application patterns
- SQL database integration with SQLAlchemy
- CRUD operations with relational data
- Environment variables and secrets management

**Key Technologies:**
- Flask web framework
- PostgreSQL database
- SQLAlchemy ORM
- Adminer database administration

### ⚡ FastAPI + Redis Example

**Location:** `examples/fastapi-redis/`

**Perfect for learning:**
- Modern async Python development
- High-performance API design
- Caching strategies with Redis
- Auto-generated API documentation

**Key Technologies:**
- FastAPI framework with async/await
- Redis for caching and storage
- Automatic OpenAPI documentation
- Redis Commander administration

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
