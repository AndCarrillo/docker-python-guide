# Automate your builds with GitHub Actions

> **Branch del módulo:** `module-04-cicd`

En esta sección aprenderás a configurar GitHub Actions para automatizar builds, testing y deployment de tu aplicación Python con Docker.

## Prerequisites

- Complete all the previous sections of this guide, starting with [Containerize a Python application](../../../tree/module-01-containerize)
- You must have a **GitHub account** and a **Docker account** to complete this section
- If you didn't create a GitHub repository for your project yet, it is time to do it
- After creating the repository, don't forget to add a remote and ensure you can commit and push your code to GitHub

### Setup GitHub Repository Variables and Secrets

1. In your project's GitHub repository, open **Settings**, and go to **Secrets and variables > Actions**

2. Under the **Variables** tab, create a new Repository variable:

   - Name: `DOCKER_USERNAME`
   - Value: Your Docker ID

3. Create a new **Personal Access Token (PAT)** for Docker Hub:

   - Go to Docker Hub → Account Settings → Security
   - Create a new token named `docker-tutorial`
   - Make sure access permissions include **Read and Write**

4. Add the PAT as a Repository secret in your GitHub repository:
   - Name: `DOCKERHUB_TOKEN`
   - Value: Your Personal Access Token

## Overview

**GitHub Actions** is a CI/CD (Continuous Integration and Continuous Deployment) automation tool built into GitHub. It allows you to define custom workflows for building, testing, and deploying your code when specific events occur (e.g., pushing code, creating a pull request, etc.).

A **workflow** is a YAML-based automation script that defines a sequence of steps to be executed when triggered. Workflows are stored in the `.github/workflows/` directory of a repository.

In this section, you'll learn how to set up and use GitHub Actions to:

1. **Run automated tests** with pytest and coverage
2. **Perform code quality checks** with linting and type checking
3. **Build your Docker image** and push it to Docker Hub
4. **Deploy your application** with automated workflows

You will complete the following steps:

1. [Define a basic GitHub Actions workflow](#1-define-a-basic-github-actions-workflow)
2. [Add testing and quality checks](#2-add-testing-and-quality-checks)
3. [Run the workflow](#3-run-the-workflow)
4. [Explore advanced examples](#4-explore-advanced-examples)

## 1. Define a basic GitHub Actions workflow

You can create a GitHub Actions workflow by creating a YAML file in the `.github/workflows/` directory of your repository. Let's start with a simple workflow that builds and pushes your Docker image.

### Option A: Using GitHub Web Interface

1. Go to your repository on GitHub and select the **Actions** tab
2. Select **set up a workflow yourself**
3. Change the default name from `main.yml` to `build.yml`

### Option B: Using Your Text Editor

Create a new file named `build.yml` in the `.github/workflows/` directory of your repository.

Add the following content to the file:

```yaml
name: Build and push Docker image

on:
  push:
    branches:
      - main

jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
```

### Understanding the Workflow

Each GitHub Actions workflow includes one or several **jobs**. Each job consists of **steps**. Each step can either run a set of commands or use already existing actions. The workflow above has four steps:

1. **Checkout code**: Gets your source code from the repository
2. **Login to Docker Hub**: Logs in using your Docker ID and Personal Access Token
3. **Set up Docker Buildx**: Sets up Docker Buildx for advanced build features
4. **Build and push**: Builds your Docker image and pushes it to Docker Hub

## 2. Add testing and quality checks

Now let's enhance our workflow by adding automated testing and code quality checks before building the Docker image:

```yaml
name: Build and push Docker image

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          python -m pytest tests/ -v

      - name: Run linting
        run: |
          ruff check .
          ruff format --check .

      - name: Run type checking
        run: |
          pyright .

  build_and_push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
```

### Key Improvements

- **Separate jobs**: Testing and building are now separate jobs
- **Job dependencies**: `build_and_push` only runs if `test` passes (`needs: test`)
- **Conditional deployment**: Images are only built on `main` branch
- **Pull request support**: Tests run on pull requests for code review

## 3. Run the workflow

Let's commit the changes and push them to the main branch:

```bash
git add .github/workflows/build.yml
git commit -m "Add GitHub Actions workflow for CI/CD"
git push origin main
```

The workflow above is triggered by `push` events on the `main` branch. This means that the workflow will run every time you push changes to the main branch.

### Monitor the Workflow

1. Go to the **Actions** tab of your GitHub repository
2. You'll see your workflow running or completed
3. Click on the workflow to see the breakdown of all steps
4. Each job will show you detailed logs of what happened

### Verify the Results

When the workflow is complete, go to your repositories on **Docker Hub**. If you see the new repository in that list, it means the GitHub Actions workflow successfully pushed the image to Docker Hub.

## 4. Explore advanced examples

Now that you understand the basics, explore these comprehensive examples that demonstrate production-ready CI/CD pipelines:

### 🔥 Flask CI/CD Pipeline

**Location:** `examples/flask-cicd/`

A complete pipeline for Flask applications including:

- Automated testing with pytest and coverage
- Code quality checks with Ruff and Pyright
- Security scanning with Safety and Bandit
- Multi-stage Docker builds
- PostgreSQL and Redis integration

```bash
cd examples/flask-cicd
docker-compose up --build
# Access: http://localhost:5000
```

**Key Features:**

- ✅ Traditional sync API approach
- ✅ Comprehensive test suite
- ✅ Production-ready Docker setup
- ✅ Database and cache integration

### 🚀 FastAPI Advanced CI/CD Pipeline

**Location:** `examples/fastapi-cicd/`

An advanced pipeline for modern FastAPI applications featuring:

- Matrix testing across Python versions (3.10, 3.11, 3.12)
- Performance testing with Locust
- Advanced security scanning
- Async patterns and background tasks
- Auto-generated API documentation

```bash
cd examples/fastapi-cicd
docker-compose up --build
# Access: http://localhost:8000/docs
```

**Key Features:**

- ✅ Modern async API patterns
- ✅ Matrix testing strategy
- ✅ Performance monitoring
- ✅ Advanced security scanning

## Understanding the Examples

### Comparison Between Approaches

| Feature          | Basic Workflow | Flask Example       | FastAPI Example            |
| ---------------- | -------------- | ------------------- | -------------------------- |
| **Complexity**   | Simple         | Moderate            | Advanced                   |
| **Testing**      | Basic          | Comprehensive       | Matrix + Performance       |
| **Security**     | None           | Safety + Bandit     | Safety + Bandit + Semgrep  |
| **Dependencies** | Docker only    | PostgreSQL + Redis  | PostgreSQL + Redis (async) |
| **Best For**     | Learning       | Production web apps | High-performance APIs      |

### Workflow Architecture

#### Flask Pipeline

```yaml
jobs:
  test: # Pytest + Ruff + Pyright + Coverage
  security: # Safety + Bandit security scanning
  build: # Docker build + GitHub Packages push
  deploy: # Production deployment + health checks
```

#### FastAPI Pipeline

```yaml
jobs:
  test: # Matrix testing (Python 3.10-3.12)
  performance: # Locust load testing + analysis
  security: # Safety + Bandit + Semgrep scanning
  build: # Optimized Docker builds + caching
  deploy: # Advanced deployment + smoke tests
```

### Next Steps

Once you've mastered the basic workflow, you can:

1. **Start with Flask example** - Learn comprehensive testing and security scanning
2. **Progress to FastAPI** - Explore async patterns and performance testing
3. **Customize for your project** - Adapt the workflows to your specific needs

## Summary

In this section, you learned how to set up GitHub Actions workflows for your Python application that include:

- **Basic Docker build and push** - Automated image creation and registry upload
- **Automated testing** - Running pytest with proper Python environment setup
- **Code quality checks** - Linting with Ruff and type checking with Pyright
- **Workflow orchestration** - Job dependencies and conditional execution
- **Production examples** - Real-world Flask and FastAPI implementations

### Related Information

- [Introduction to GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions)
- [Docker Build GitHub Actions](https://github.com/docker/build-push-action)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Python testing with pytest](https://docs.pytest.org/)
- [Ruff Python linter](https://docs.astral.sh/ruff/)

---

## 🎯 Next Steps

Once you've completed this module, continue with:

**[Module 5: Test your deployment](../../../tree/module-05-deployment)** - Learn about Kubernetes, monitoring, and production deployment strategies.

```yaml
jobs:
  test: # Matrix testing (Python 3.10-3.12)
  performance: # Locust load testing + analysis
  security: # Safety + Bandit + Semgrep scanning
  build: # Optimized Docker builds + caching
  deploy: # Advanced deployment + smoke tests
```

## 🚀 Quick Start

### 1. Explora los Ejemplos Localmente

```bash
# Flask CI/CD - Traditional approach
cd examples/flask-cicd
docker-compose up --build
curl http://localhost:5000/health
open http://localhost:5000

# FastAPI CI/CD - Modern async approach
cd examples/fastapi-cicd
docker-compose up --build
curl http://localhost:8000/health
open http://localhost:8000/docs
```

### 2. Configura tu Propio Pipeline

```bash
# Fork este repositorio
gh repo fork AndCarrillo/docker-python-guide

# Clona tu fork
git clone https://github.com/YOUR_USERNAME/docker-python-guide.git

# Configura los secrets necesarios en GitHub
# Settings > Secrets and variables > Actions
```

### 3. Adapta los Workflows

- Copia los workflows de `.github/workflows/`
- Modifica las rutas y nombres según tu proyecto
- Configura los environment variables necesarios
- Ajusta los jobs según tus necesidades

## 🎓 Learning Path Recomendado

### Nivel Principiante

1. **Empieza con Flask CI/CD** - Conceptos fundamentales
2. **Explora los workflows** - Entiende cada job y step
3. **Prueba localmente** - Docker compose up y testing

### Nivel Intermedio

4. **Configura tu propio repo** - Fork y adaptación
5. **Modifica los workflows** - Personaliza según tu proyecto
6. **Integra security scanning** - Safety, Bandit, dependency checks

### Nivel Avanzado

7. **FastAPI CI/CD** - Async patterns y performance testing
8. **Matrix testing** - Multiple Python versions
9. **Advanced security** - Semgrep, vulnerability assessment
10. **Production deployment** - Smoke tests, rollback strategies

## 📖 Conceptos Clave

### CI/CD Fundamentals

- **Continuous Integration**: Integración automática de código
- **Continuous Deployment**: Despliegue automático a producción
- **Pipeline Stages**: Test → Build → Deploy
- **Quality Gates**: Puntos de control de calidad

### GitHub Actions

- **Workflows**: Procesos automatizados activados por eventos
- **Jobs**: Conjunto de steps que se ejecutan en paralelo
- **Actions**: Bloques de código reutilizables
- **Runners**: Servidores que ejecutan los workflows

### Docker in CI/CD

- **Multi-stage builds**: Optimización de imágenes
- **Layer caching**: Aceleración de builds
- **Container registries**: Almacenamiento de imágenes
- **Security scanning**: Análisis de vulnerabilidades

## 🔗 Recursos Adicionales

### Documentación Oficial

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Flask Testing](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

### Herramientas y Plugins

- [pytest](https://docs.pytest.org/) - Python testing framework
- [Ruff](https://docs.astral.sh/ruff/) - Fast Python linter
- [Safety](https://safetycli.com/) - Dependency vulnerability scanner
- [Bandit](https://bandit.readthedocs.io/) - Security linter for Python
- [Locust](https://locust.io/) - Performance testing tool

### Community Resources

- [Awesome GitHub Actions](https://github.com/sdras/awesome-actions)
- [Docker Python Guide](https://docs.docker.com/language/python/)
- [CI/CD Best Practices](https://docs.github.com/en/actions/guides)

---

## 🤝 Contributions

Found an error or have a suggestion? Contribute to the project!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**📅 Last updated:** July 2025  
**👨‍💻 Maintained by:** Andrea Carrillo - [GitHub](https://github.com/AndCarrillo)
