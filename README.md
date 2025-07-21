# 🐍 Python Docker Guide

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-24.0+-blue.svg)](https://docs.docker.com/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.0+-green.svg)](https://fastapi.tiangolo.com)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-enabled-brightgreen.svg)](https://github.com/features/actions)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-registry-blue.svg)](https://hub.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

A comprehensive guide to containerize Python applications using Docker, from basic concepts to production deployment.

## 📋 Table of Contents

### 🎯 Guide Modules

| Module                                                                 | Description                                  | Branch                     | Status |
| ---------------------------------------------------------------------- | -------------------------------------------- | -------------------------- | ------ |
| [**1. Containerize your app**](#module-1-containerize-your-app)        | Learn to containerize Python applications    | `module-01-containerize`   | 🚧     |
| [**2. Develop your app**](#module-2-develop-your-app)                  | Local development using containers           | `module-02-develop`        | 🚧     |
| [**3. Linting and typing**](#module-3-linting-and-typing)              | Code quality: linting, formatting and typing | `module-03-linting-typing` | 🚧     |
| [**4. CI/CD with GitHub Actions**](#module-4-cicd-with-github-actions) | Automation with GitHub Actions               | `module-04-cicd`           | 🚧     |
| [**5. Test your deployment**](#module-5-test-your-deployment)          | Testing and deployment strategies            | `module-05-deployment`     | 🚧     |

---

## 🎯 Learning Objectives

By completing this guide, you will be able to:

- ✅ Containerize Python applications efficiently
- ✅ Set up a local development environment with containers
- ✅ Implement code best practices (linting, formatting, typing)
- ✅ Configure automated CI/CD pipelines
- ✅ Deploy applications with best practices and monitoring

---

## 📚 Detailed Modules

### Module 1: Containerize your app

**Branch:** `module-01-containerize`

Learn the fundamentals of containerization with Docker:

- Creating optimized Dockerfiles for Python
- Multi-stage builds to reduce image size
- Dependencies and requirements configuration
- Security best practices

**🔗 [Go to module →](../../tree/module-01-containerize)**

---

### Module 2: Develop your app

**Branch:** `module-02-develop`

Local development environment setup:

- Docker Compose for development
- Hot reload and debugging
- Environment variables management
- Database integration

**🔗 [Go to module →](../../tree/module-02-develop)**

---

### Module 3: Linting and typing

**Branch:** `module-03-linting-typing`

Code quality and best practices:

- Configuration of Black, Flake8, isort
- Type checking with mypy
- Pre-commit hooks
- VS Code configuration

**🔗 [Go to module →](../../tree/module-03-linting-typing)**

---

### Module 4: CI/CD with GitHub Actions

**Branch:** `module-04-cicd`

Development pipeline automation:

- GitHub Actions workflows
- Automated testing
- Docker image build and push
- Automated deployment

**🔗 [Go to module →](../../tree/module-04-cicd)**

---

### Module 5: Test your deployment

**Branch:** `module-05-deployment`

Testing and deployment strategies:

- Local deployment testing
- Container orchestration basics
- Health checks and monitoring
- Production deployment considerations

**🔗 [Go to module →](../../tree/module-05-deployment)**

---

## 🚀 How to use this guide

### Prerequisites

- Docker Desktop installed
- Python 3.9+ installed
- Git configured
- Code editor (recommended: VS Code)

### Navigation

1. **Sequential**: Follow modules in order for progressive learning
2. **By topics**: Go directly to the module that interests you
3. **Practical**: Each module includes hands-on exercises

### Branch structure

```
main/
├── module-01-containerize/     # Basic containerization
├── module-02-develop/          # Local development
├── module-03-linting-typing/   # Code quality
├── module-04-cicd/            # CI/CD Pipeline
└── module-05-deployment/      # Testing and Deployment
```

---

## 📖 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 🤝 Contributing

Found an error or have a suggestion? Contribute!

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## 📝 License

This project is under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🏷️ Tags

`#docker` `#python` `#containerization` `#devops` `#cicd` `#github-actions` `#development`

---

**📅 Last updated:** July 2025  
**👨‍💻 Maintained by:** Andrea Carrillo - [GitHub](https://github.com/AndCarrillo)
