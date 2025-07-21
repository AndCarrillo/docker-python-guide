# 🐍 Python Docker Guide - Complete Guide

A comprehensive guide to containerize Python applications using Docker, from basic concepts to production deployment.

## 📋 Table of Contents

### 🎯 Guide Modules

| Module                                                                 | Description                                  | Branch                     | Status |
| ---------------------------------------------------------------------- | -------------------------------------------- | -------------------------- | ------ |
| [**1. Containerize your app**](#module-1-containerize-your-app)        | Learn to containerize Python applications    | `module-01-containerize`   | 🚧     |
| [**2. Develop your app**](#module-2-develop-your-app)                  | Local development using containers           | `module-02-develop`        | 🚧     |
| [**3. Linting and typing**](#module-3-linting-and-typing)              | Code quality: linting, formatting and typing | `module-03-linting-typing` | 🚧     |
| [**4. CI/CD with GitHub Actions**](#module-4-cicd-with-github-actions) | Automation with GitHub Actions               | `module-04-cicd`           | 🚧     |
| [**5. Test your deployment**](#module-5-test-your-deployment)          | Testing and deployment in Kubernetes         | `module-05-deployment`     | 🚧     |

---

## 🎯 Learning Objectives

By completing this guide, you will be able to:

- ✅ Containerize Python applications efficiently
- ✅ Set up a local development environment with containers
- ✅ Implement code best practices (linting, formatting, typing)
- ✅ Configure automated CI/CD pipelines
- ✅ Deploy applications to Kubernetes for testing

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

Testing and deployment in Kubernetes:

- Local Kubernetes configuration
- YAML manifests
- Deployment testing
- Monitoring and debugging

**🔗 [Go to module →](../../tree/module-05-deployment)**

---

## 🚀 How to use this guide

### Prerequisites

- Docker Desktop installed
- Python 3.9+ installed
- Git configured
- Code editor (recommended: VS Code)

### 🛠️ Technologies & Tools Covered

| Category | Tools |
|----------|-------|
| **Containerization** | Docker, Docker Compose, Multi-stage builds |
| **Python Frameworks** | Flask, FastAPI, Django |
| **Web Servers** | Gunicorn, Uvicorn, Nginx |
| **Code Quality** | Black, Flake8, isort, mypy, Bandit, Pylint |
| **Testing** | pytest, unittest, coverage |
| **CI/CD** | GitHub Actions, Automated testing, Docker registry |
| **Orchestration** | Kubernetes, kubectl, YAML manifests |
| **Development** | VS Code, Git workflows, Pre-commit hooks |
| **Security** | Non-root users, Secrets management, Vulnerability scanning |

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
- [Kubernetes Documentation](https://kubernetes.io/docs/)
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

### Core Technologies
`#docker` `#python` `#containerization` `#kubernetes` `#docker-compose`

### Development Tools
`#flask` `#fastapi` `#django` `#gunicorn` `#uvicorn` `#nginx`

### Code Quality & Linting
`#black` `#flake8` `#isort` `#mypy` `#bandit` `#pre-commit` `#pylint`

### CI/CD & DevOps
`#github-actions` `#cicd` `#devops` `#automation` `#testing` `#pytest`

### Development Environment
`#vscode` `#git` `#powershell` `#bash` `#cross-platform`

### Security & Best Practices
`#security` `#multistage-builds` `#non-root` `#secrets-management`

---

**📅 Last updated:** July 2025
**👨‍💻 Maintained by:** Andrea Carrillo - [GitHub](https://github.com/AndCarrillo)
