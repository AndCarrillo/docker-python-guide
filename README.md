# 📦 Module 1: Containerize your app

Learn the fundamentals of containerizing Python applications with Docker, from basic concepts to production-ready containers.

## 🎯 Learning Objectives

By completing this module, you will be able to:

- ✅ Write optimized Dockerfiles for Python applications
- ✅ Implement multi-stage builds to reduce image size
- ✅ Apply security best practices for containers
- ✅ Optimize container images for production use
- ✅ Configure proper Python dependency management in containers

## 📋 Module Contents

### 📚 Documentation

- [**Dockerfile Best Practices**](docs/dockerfile-guide.md) - Complete guide to writing optimal Dockerfiles (400+ lines)
- [**Security Considerations**](docs/security-guide.md) - Container security best practices and implementation
- [**Image Optimization**](docs/optimization-guide.md) - Techniques to reduce image size and improve performance

### 💡 Practical Examples

- [**Flask Basic**](examples/flask-basic/) - Simple Flask application with health checks and security
- [**FastAPI API**](examples/fastapi-api/) - Production-ready API with authentication and monitoring
- [**Django Blog**](examples/django-blog/) - Full-stack blog with PostgreSQL, static files, and Nginx

### 🎓 Hands-on Exercises

- [**Exercise 1: Basic Dockerfile**](exercises/01-basic-dockerfile/) - Create your first Python container
- [**Exercise 2: Multi-stage Builds**](exercises/02-multi-stage-builds/) - Optimize with multi-stage builds

### 🔧 Templates

- [**Dockerfile Templates**](templates/) - Ready-to-use Dockerfile templates for different scenarios

---

## 🚀 Getting Started

### Prerequisites

Before starting this module, ensure you have:

- ✅ Docker Desktop installed and running
- ✅ Python 3.9+ installed
- ✅ Basic understanding of Python applications
- ✅ Text editor or IDE (VS Code recommended)

### Quick Start

1. **Clone and navigate to this module:**

   ```bash
   git clone https://github.com/AndCarrillo/docker-python-guide.git
   cd docker-python-guide
   git checkout module-01-containerize
   ```

2. **Start with the Flask example:**

   ```bash
   cd examples/flask-basic
   # Follow the README instructions in that folder
   ```

3. **Or jump to exercises:**
   ```bash
   cd exercises/01-basic-dockerfile
   # Follow the exercise instructions
   ```

---

## 📖 Study Path

### 🎯 Recommended Learning Sequence

1. **📚 Read Documentation First**

   - Start with [Dockerfile Best Practices](docs/dockerfile-guide.md)
   - Review [Security Considerations](docs/security-guide.md)

2. **💡 Explore Examples**

   - Begin with [Flask Basic Example](examples/flask-basic/)
   - Progress to [FastAPI Advanced](examples/fastapi-advanced/)
   - Study [Django Production](examples/django-production/)

3. **🎓 Complete Exercises**

   - Exercise 1: [Basic Dockerfile](exercises/01-basic-dockerfile/)
   - Exercise 2: [Multi-stage Build](exercises/02-multistage-build/)
   - Exercise 3: [Optimization](exercises/03-optimization/)

4. **🔧 Use Templates**
   - Apply [templates](templates/) to your own projects

---

## 🏗️ What You'll Build

Throughout this module, you'll containerize three different types of Python applications:

### 🌐 Flask Web Application

- **Basic containerization** with essential dependencies
- **Environment configuration** and best practices
- **Health checks** and proper logging

### ⚡ FastAPI API Server

- **Multi-stage build** for optimized production image
- **Advanced dependency management** with Poetry
- **Security scanning** and vulnerability testing

### 🎨 Django Full Application

- **Production-ready** configuration
- **Static files** handling
- **Database integration** preparation
- **Comprehensive optimization** techniques

---

## 🔍 Key Concepts Covered

### 🐳 Docker Fundamentals

- **Image layers** and caching strategies
- **Build context** optimization
- **Registry best practices**

### 🐍 Python-Specific Optimizations

- **Requirements management** (pip, Poetry, pipenv)
- **Virtual environments** in containers
- **Bytecode compilation** strategies
- **Package installation** optimization

### 🔒 Security & Production

- **Non-root users** configuration
- **Secrets management** basics
- **Image scanning** integration
- **Runtime security** considerations

---

## 📊 Module Progress Tracker

Track your progress through the module:

- [ ] **Documentation Review** (Estimated: 45 minutes)

  - [ ] Dockerfile Best Practices
  - [ ] Security Considerations
  - [ ] Image Optimization

- [ ] **Examples Study** (Estimated: 90 minutes)

  - [ ] Flask Basic Example
  - [ ] FastAPI Advanced Example
  - [ ] Django Production Example

- [ ] **Hands-on Exercises** (Estimated: 120 minutes)

  - [ ] Exercise 1: Basic Dockerfile
  - [ ] Exercise 2: Multi-stage Build
  - [ ] Exercise 3: Security & Optimization

- [ ] **Template Application** (Estimated: 30 minutes)
  - [ ] Apply templates to personal project

**Total Estimated Time: ~5 hours**

---

## 🎯 Learning Outcomes Validation

After completing this module, you should be able to:

### ✅ Technical Skills

- [ ] Write a Dockerfile from scratch for any Python application
- [ ] Implement multi-stage builds to reduce image size by 50%+
- [ ] Configure non-root users for security
- [ ] Optimize image layers for faster builds
- [ ] Handle Python dependencies efficiently in containers

### ✅ Best Practices Knowledge

- [ ] Explain why certain Dockerfile instructions are preferred
- [ ] Identify security vulnerabilities in container configurations
- [ ] Choose appropriate base images for different use cases
- [ ] Implement proper logging and health checks

### ✅ Production Readiness

- [ ] Create production-ready container images
- [ ] Configure proper environment variable handling
- [ ] Implement basic security scanning
- [ ] Optimize for container registry efficiency

---

## 🔗 Next Steps

After mastering this module, you'll be ready for:

- **[Module 2: Develop your app](../module-02-develop/)** - Local development with Docker Compose
- Apply containerization to your own Python projects
- Explore advanced Docker features and optimization techniques

---

## 🤝 Need Help?

- 📖 Review the [documentation](docs/) for detailed explanations
- 💡 Check the [examples](examples/) for working code
- 🎓 Practice with the [exercises](exercises/) for hands-on learning
- 🔧 Use [templates](templates/) as starting points

---

**📅 Module Duration:** ~5 hours  
**🎯 Difficulty Level:** Beginner to Intermediate  
**📋 Prerequisites:** Basic Python knowledge, Docker installed
