# 🐳 Docker Python Guide

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-24.0+-blue.svg)](https://docs.docker.com/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.0+-green.svg)](https://fastapi.tiangolo.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-enabled-brightgreen.svg)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Complete Docker guide for Python developers** - Learn to containerize, develop, and deploy Python applications using Docker with hands-on examples.

## 🎯 What You'll Learn

Master Docker for Python development through practical, progressive modules:

- 🐳 **Containerize Python apps** (Flask & FastAPI)
- 🔧 **Set up local development** with Docker Compose
- ✨ **Implement code quality** (linting, formatting, typing)
- 🚀 **Build CI/CD pipelines** with GitHub Actions
- ☸️ **Deploy with Kubernetes** locally

## 📚 Learning Path

| Module | Topic                | Level        | Time | Branch                                                            |
| ------ | -------------------- | ------------ | ---- | ----------------------------------------------------------------- |
| **01** | 🐳 Containerization  | Beginner     | 45m  | [`module-01-containerize`](../../tree/module-01-containerize)     |
| **02** | 🔧 Development Setup | Intermediate | 60m  | [`module-02-develop`](../../tree/module-02-develop)               |
| **03** | ✨ Code Quality      | Intermediate | 45m  | [`module-03-linting-typing`](../../tree/module-03-linting-typing) |
| **04** | 🚀 CI/CD Pipeline    | Advanced     | 90m  | [`module-04-cicd`](../../tree/module-04-cicd)                     |
| **05** | ☸️ Deployment        | Advanced     | 75m  | [`module-05-deployment`](../../tree/module-05-deployment)         |

**🏆 Final Project:** [`project-complete`](../../tree/project-complete) - Complete implementation with all optimizations

## 🚀 Quick Start

### Prerequisites

- 🐳 [Docker Desktop](https://docs.docker.com/get-docker/)
- 🐍 [Python 3.9+](https://www.python.org/downloads/)
- 📂 [Git](https://git-scm.com/downloads)
- 📝 [VS Code](https://code.visualstudio.com/) (recommended)

### Get Started

```bash
# Clone the repository
git clone https://github.com/AndCarrillo/docker-python-guide.git
cd docker-python-guide

# Start with Module 1
git checkout module-01-containerize
# Follow the README instructions in that branch
```

**📖 [View complete workflow guide →](BRANCH-WORKFLOW.md)**

## 🛠️ Examples & Technologies

### Frameworks

| Framework      | Purpose                | Learning Focus                                    |
| -------------- | ---------------------- | ------------------------------------------------- |
| 🌱 **Flask**   | Simple web framework   | Fundamentals, SQL databases, traditional patterns |
| ⚡ **FastAPI** | Modern async framework | Performance, async/await, auto-documentation      |

### Progressive Examples

- **📦 Flask + PostgreSQL** - Traditional web app with relational database
- **⚡ FastAPI + Redis** - Modern API with caching and async operations
- **🔧 Multi-stage builds** - Optimized Docker images
- **🚀 Complete CI/CD** - Automated pipelines with GitHub Actions
- **☸️ Kubernetes deployment** - Local testing and deployment

## 📋 Module Overview

### 📦 [Module 1: Containerize](../../tree/module-01-containerize)

Create optimized Docker images for Python applications.

- Dockerfiles and best practices
- Security and non-root users
- Multi-stage builds
- Health checks

### 🛠️ [Module 2: Develop](../../tree/module-02-develop)

Set up local development environment.

- Docker Compose for development
- Hot reload and debugging
- Environment variables and secrets
- Database integration

### ✨ [Module 3: Code Quality](../../tree/module-03-linting-typing)

Implement linting, formatting, and type checking.

- Ruff for linting and formatting
- mypy for type checking
- Pre-commit hooks
- VS Code integration

### 🚀 [Module 4: CI/CD](../../tree/module-04-cicd)

Automate builds with GitHub Actions.

- Automated testing and building
- Docker image publishing
- Multi-environment deployment
- Security scanning

### ☸️ [Module 5: Deployment](../../tree/module-05-deployment)

Deploy and test with Kubernetes.

- Local Kubernetes setup
- Health checks and monitoring
- Rolling updates and rollbacks
- Debugging containerized apps

## 🎯 Key Features

- ✅ **Step-by-step tutorials** with detailed explanations
- ✅ **Ready-to-use code** in every example
- ✅ **Industry best practices** and patterns
- ✅ **Hands-on exercises** to reinforce learning
- ✅ **Troubleshooting guides** for common issues

## 📚 Resources

- [Docker Documentation](https://docs.docker.com/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🤝 Contributing

Contributions welcome! See [Contributing Guide](CONTRIBUTING.md) for:

- Reporting issues
- Submitting improvements
- Code standards
- Development workflow

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

**📅 Last updated:** July 2025  
**👨‍💻 Maintained by:** [Andrea Carrillo](https://github.com/AndCarrillo)
