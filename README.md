# Python Docker Guide

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-24.0+-blue.svg)](https://docs.docker.com/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.0+-green.svg)](https://fastapi.tiangolo.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-enabled-brightgreen.svg)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The Python language-specific guide teaches you how to containerize a Python application using Docker. In this guide, you'll learn how to:

- **Containerize and run a Python application**
- **Set up a local environment to develop a Python application using containers**
- **Lint, format, typing and best practices**
- **Configure a CI/CD pipeline for a containerized Python application using GitHub Actions**
- **Deploy your containerized Python application locally to Kubernetes to test and debug your deployment**

Start by containerizing an existing Python application.

## What you'll learn

By completing this guide, you will be able to:

- ✅ Containerize Python applications (Flask & FastAPI)
- ✅ Set up a local development environment with containers
- ✅ Implement code quality best practices (linting, formatting, typing)
- ✅ Configure automated CI/CD pipelines with GitHub Actions
- ✅ Deploy and test applications locally using Kubernetes

## Prerequisites

To complete this guide, you need:

- **Docker Desktop** - [Install Docker Desktop](https://docs.docker.com/get-docker/)
- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Install Git](https://git-scm.com/downloads)
- **Code Editor** - [VS Code](https://code.visualstudio.com/) (recommended)

## How to use this guide

### 🎯 Learning Path

Follow the modules sequentially for the best learning experience:

1. **Start with Module 1** - Learn containerization basics
2. **Progress through each module** - Build on previous knowledge
3. **Complete hands-on examples** - Practice with Flask and FastAPI
4. **Apply to your projects** - Use the patterns in real applications

### 🌿 Branch Structure

Each module has its own branch with complete examples and documentation:

```
main                     # This overview and navigation
├── module-01-containerize   # Dockerfiles and containerization
├── module-02-develop        # Local development setup
├── module-03-linting-typing # Code quality and type safety
├── module-04-cicd          # CI/CD with GitHub Actions
└── module-05-deployment    # Kubernetes and testing
```

### 🚀 Quick Start

Ready to begin? Start with Module 1:

```bash
# Clone the repository
git clone https://github.com/AndCarrillo/docker-python-guide.git
cd docker-python-guide

# Start with Module 1: Containerize your app
git checkout module-01-containerize

# Follow the README instructions in that branch
```

Each module branch contains:

- **📚 README.md** - Complete module guide with step-by-step instructions
- **🧩 Examples** - Flask and FastAPI applications to practice with
- **📖 Documentation** - Additional resources and troubleshooting

## Examples Overview

This guide uses **two progressive examples** throughout all modules:

| Example            | Framework | Purpose            | Key Concepts                                         |
| ------------------ | --------- | ------------------ | ---------------------------------------------------- |
| **Flask Basic**    | Flask     | Learn fundamentals | Simple containerization, health checks, security     |
| **FastAPI Modern** | FastAPI   | Advanced patterns  | Multi-stage builds, async, documentation, production |

Both examples evolve through each module, teaching new Docker and development concepts while maintaining familiar application code.

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## Modules

### 📦 [Containerize your app](../../tree/module-01-containerize)

Learn how to containerize a Python application.

**What you'll learn:**

- Create optimized Dockerfiles for Python applications
- Implement security best practices and non-root users
- Use multi-stage builds to reduce image size
- Configure health checks and monitoring

**Examples:**

- **Flask Basic**: Simple containerization fundamentals
- **FastAPI Modern**: Advanced multi-stage builds with async support

---

### 🛠️ [Develop your app](../../tree/module-02-develop)

Learn how to develop your Python application locally.

**What you'll learn:**

- Set up local development environment with Docker Compose
- Configure hot reload and live debugging in containers
- Manage environment variables and secrets
- Integrate databases and external services

**Examples:**

- **Flask with PostgreSQL**: Database integration and development workflow
- **FastAPI with Redis**: Caching and session management

---

### 🔍 [Code quality and type safety](../../tree/module-03-linting-typing)

Learn how to configure a linter and implement continuous integration.

**What you'll learn:**

- Configure Ruff for linting and formatting
- Set up mypy for static type checking
- Implement pre-commit hooks for automated checks
- Integrate code quality tools with containers

**Examples:**

- **Flask with Quality Tools**: Complete linting and formatting setup
- **FastAPI with Type Safety**: Advanced type checking and validation

---

### 🚀 [Automate your builds with GitHub Actions](../../tree/module-04-cicd)

Learn how to configure CI/CD using GitHub Actions for your Python application.

**What you'll learn:**

- Create automated test and build pipelines
- Configure Docker image building and pushing
- Set up automated deployment workflows
- Implement security scanning and vulnerability checks

**Examples:**

- **Flask CI/CD**: Complete GitHub Actions workflow
- **FastAPI Advanced**: Multi-environment deployment pipeline

---

### 🔧 [Test your deployment](../../tree/module-05-deployment)

Learn how to develop locally using Kubernetes.

**What you'll learn:**

- Deploy applications locally with Kubernetes
- Configure health checks and monitoring
- Implement rolling updates and rollback strategies
- Test and debug containerized applications

**Examples:**

- **Flask on Kubernetes**: Local deployment and testing
- **FastAPI Production**: Advanced Kubernetes configuration

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- How to report issues
- How to submit improvements
- Code standards and guidelines
- Development workflow

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**📅 Last updated:** December 2024  
**👨‍💻 Maintained by:** [Andrea Carrillo](https://github.com/AndCarrillo)
