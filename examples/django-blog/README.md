# 🚀 Django Blog Containerization Example

A comprehensive Django blog application demonstrating advanced containerization techniques, multi-stage builds, and production deployment with Docker Compose.

## 📋 Features

- **Complete Django Blog**: Posts, categories, tags, comments system
- **Multi-Stage Builds**: Optimized development and production builds
- **Database Integration**: PostgreSQL with Django ORM
- **Static & Media Files**: Proper handling with WhiteNoise and volumes
- **Production Ready**: Nginx, Gunicorn, Redis, and security configurations
- **Environment-Based Config**: 12-factor app principles
- **Health Checks**: Monitoring and readiness probes
- **Admin Interface**: Django admin for content management

## 🏗️ Architecture

```
django-blog/
├── blogproject/                 # Django project
│   ├── blogproject/            # Project settings
│   │   ├── settings.py         # Environment-based configuration
│   │   ├── urls.py             # URL routing with health checks
│   │   └── wsgi.py             # WSGI application
│   └── blog/                   # Blog application
│       ├── models.py           # Post, Category, Tag, Comment models
│       ├── views.py            # Class-based and function views
│       ├── admin.py            # Django admin configuration
│       └── urls.py             # Blog URL patterns
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Multi-stage production build
├── docker-compose.yml          # Full stack with PostgreSQL, Redis, Nginx
├── nginx.conf                  # Production Nginx configuration
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to the Django example
cd examples/django-blog

# Copy environment template
cp .env.example .env

# Edit .env with your settings
```

### 2. Development with Docker Compose

```bash
# Build and start development environment
docker-compose --profile development up --build

# Access the application
# http://localhost:8000
```

### 3. Production Deployment

```bash
# Build and start production environment
docker-compose --profile production up --build

# Access through Nginx
# http://localhost
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `django-insecure...` | Django secret key |
| `DEBUG` | `false` | Debug mode |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Allowed hosts |
| `DB_HOST` | `db` | Database host |
| `DB_NAME` | `blogdb` | Database name |
| `DB_USER` | `bloguser` | Database user |
| `DB_PASSWORD` | `blogpass` | Database password |
| `USE_SQLITE` | `false` | Use SQLite instead of PostgreSQL |

### Docker Compose Profiles

- **development**: Django dev server with hot reload
- **production**: Gunicorn + Nginx + Redis
- **migration**: Run Django migrations only

## 📱 Application Features

### Blog Functionality

- **Posts Management**: Create, edit, delete blog posts
- **Categories & Tags**: Organize content with categories and tags
- **Comments System**: User comments with moderation
- **Search**: Full-text search across posts
- **Admin Interface**: Complete Django admin for content management

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with featured posts |
| GET | `/posts/` | List all published posts |
| GET | `/post/<slug>/` | Individual post detail |
| GET | `/category/<slug>/` | Posts by category |
| GET | `/tag/<slug>/` | Posts by tag |
| GET | `/search/` | Search posts |
| GET | `/api/posts/` | JSON API for posts |
| GET | `/api/categories/` | JSON API for categories |
| GET | `/health/` | Health check |
| GET | `/ready/` | Readiness check |

### Admin Interface

Access Django admin at `/admin/` with superuser credentials:

```bash
# Create superuser (in development)
docker-compose --profile development exec web-dev python blogproject/manage.py createsuperuser
```

## 🐳 Docker Implementation

### Multi-Stage Dockerfile

```dockerfile
# 1. Base stage - Common dependencies
FROM python:3.11-slim as base

# 2. Builder stage - Build dependencies and wheels
FROM base as builder

# 3. Development stage - Hot reload, debugging tools
FROM builder as development

# 4. Production stage - Optimized, security-focused
FROM base as production

# 5. Migration stage - Database operations
FROM production as migration
```

### Django-Specific Optimizations

```dockerfile
# Collect static files during build
RUN python manage.py collectstatic --noinput --clear

# Handle media files with volumes
VOLUME ["/app/media", "/app/logs"]

# Production WSGI server
CMD ["gunicorn", "--chdir", "blogproject", "blogproject.wsgi:application"]
```

## 🏭 Production Deployment

### Full Stack with Docker Compose

```yaml
services:
  db:          # PostgreSQL database
  web-prod:    # Django with Gunicorn
  nginx:       # Static files and reverse proxy
  redis:       # Caching and sessions
  migrate:     # Database migrations
```

### Build and Deploy

```bash
# Production build
docker-compose --profile production build

# Run migrations
docker-compose --profile migration run --rm migrate

# Start production stack
docker-compose --profile production up -d

# Check health
curl http://localhost/health/
```

### Nginx Configuration

- **Static Files**: Served directly by Nginx
- **Media Files**: User uploads served with proper headers
- **Reverse Proxy**: Django application behind Nginx
- **Security Headers**: X-Frame-Options, CSP, etc.

## 🧪 Testing the Application

### Basic Functionality

```bash
# Check health
curl http://localhost:8000/health/

# Get posts via API
curl http://localhost:8000/api/posts/

# Search functionality
curl "http://localhost:8000/search/?q=django"
```

### Database Operations

```bash
# Run migrations
docker-compose --profile development exec web-dev python blogproject/manage.py migrate

# Create sample data
docker-compose --profile development exec web-dev python blogproject/manage.py loaddata fixtures/sample_data.json

# Create superuser
docker-compose --profile development exec web-dev python blogproject/manage.py createsuperuser
```

### Performance Testing

```bash
# Load test with ab (if available)
ab -n 100 -c 10 http://localhost/

# Check container resources
docker stats
```

## 📊 Monitoring & Logging

### Health Checks

- **Liveness**: `/health/` - Basic application health
- **Readiness**: `/ready/` - Database connectivity check

### Logging Configuration

```python
# Structured logging to stdout
LOGGING = {
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
}
```

### Container Logs

```bash
# View application logs
docker-compose logs web-prod

# Follow logs in real-time
docker-compose logs -f web-prod

# Database logs
docker-compose logs db
```

## 🔐 Security Features

### Django Security

- **Secret Key**: Environment-based configuration
- **HTTPS**: SSL redirect in production
- **Security Headers**: HSTS, XSS protection, frame options
- **CSRF Protection**: Django CSRF middleware
- **Input Validation**: Pydantic-style model validation

### Container Security

- **Non-Root User**: Application runs as `appuser`
- **Minimal Base Image**: Python slim image
- **Read-Only Filesystem**: Where possible
- **Security Scanning**: Regular base image updates

### Database Security

- **Credentials**: Environment variables only
- **Connection Pooling**: PostgreSQL connection management
- **Migrations**: Separate migration container

## 🚀 Performance Optimizations

### Image Size Optimization

```bash
# Check image sizes
docker images | grep django-blog

# Expected results:
# django-blog_web-dev   ~300MB (includes dev tools)
# django-blog_web-prod  ~200MB (production optimized)
```

### Django Optimizations

- **Static Files**: WhiteNoise for efficient serving
- **Database**: Connection pooling and query optimization
- **Caching**: Redis for sessions and page caching
- **Media Files**: Separate volume for user uploads

### Build Optimizations

- **Layer Caching**: Optimized Dockerfile layer order
- **Wheel Building**: Pre-built Python packages
- **Multi-Stage**: Separate build and runtime stages

## 🛠️ Development Workflow

### Local Development

```bash
# Start development environment
docker-compose --profile development up

# Hot reload enabled - edit files locally
# Changes automatically reflected in container

# Run Django commands
docker-compose --profile development exec web-dev python blogproject/manage.py shell
```

### Database Management

```bash
# Create migrations
docker-compose --profile development exec web-dev python blogproject/manage.py makemigrations

# Apply migrations
docker-compose --profile development exec web-dev python blogproject/manage.py migrate

# Database shell
docker-compose --profile development exec db psql -U bloguser -d blogdb
```

### Debugging

```bash
# Container shell access
docker-compose --profile development exec web-dev /bin/bash

# Python shell with Django
docker-compose --profile development exec web-dev python blogproject/manage.py shell

# View container processes
docker-compose --profile development exec web-dev ps aux
```

## 📚 Learning Objectives

After studying this example, you should understand:

1. **Django Containerization**: How to containerize Django applications with proper static/media file handling
2. **Multi-Stage Builds**: Creating optimized images for different environments
3. **Database Integration**: PostgreSQL with Django in containers
4. **Production Deployment**: Full-stack deployment with Nginx and reverse proxy
5. **Environment Configuration**: 12-factor app principles with Django
6. **Security Practices**: Container security, Django security, database security
7. **Performance Optimization**: Caching, static files, database optimization

## 🔗 Related Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PostgreSQL Docker Guide](https://hub.docker.com/_/postgres)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)

## ⭐ Best Practices Demonstrated

- ✅ Multi-stage builds for optimization
- ✅ Environment-based configuration
- ✅ Proper static and media file handling
- ✅ Database migrations in containers
- ✅ Production-ready WSGI configuration
- ✅ Security headers and HTTPS setup
- ✅ Comprehensive health checks
- ✅ Structured logging
- ✅ Non-root user execution
- ✅ Volume management for persistent data

## 🏆 Advanced Features

### Redis Integration

```yaml
# Add to docker-compose.yml
redis:
  image: redis:7-alpine
  volumes:
    - redis_data:/data
```

### Celery Task Queue

```yaml
# Background task processing
celery:
  build:
    context: .
    target: production
  command: celery -A blogproject worker -l info
  depends_on:
    - redis
    - db
```

### SSL/TLS with Let's Encrypt

```yaml
# Production HTTPS setup
certbot:
  image: certbot/certbot
  volumes:
    - ./data/certbot/conf:/etc/letsencrypt
    - ./data/certbot/www:/var/www/certbot
```

**🎉 Congratulations!** You've mastered Django containerization with Docker. This example demonstrates enterprise-grade Django deployment practices with containers.

**📖 Next Steps**: This completes Module 1's comprehensive coverage of Python web framework containerization (Flask, FastAPI, Django).
