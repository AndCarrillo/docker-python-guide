# 🔒 Container Security Basics

Essential security basics for Python containers in Module 1.

## 🎯 Overview

Learn the fundamental security practices every Python container should have. Focus on simple, high-impact security measures for beginners.

## 📋 What You'll Learn

- [Non-root User](#-non-root-user)
- [Base Image Security](#-base-image-security)
- [Basic Environment Security](#-basic-environment-security)
- [Security Checklist](#-security-checklist)

---

## 👤 Non-root User

Always run your application as a non-root user:

```dockerfile
# ✅ Create and use a non-root user
FROM python:3.11-slim

# Create a non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy requirements and install as root (needed for pip)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and change ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Run application
CMD ["python", "app.py"]
```

**Why non-root?**

- Limits damage if container is compromised
- Follows principle of least privilege
- Industry best practice

---

## 🛡️ Base Image Security

Use trusted, official images:

```dockerfile
# ✅ Use official Python images
FROM python:3.11-slim

# ✅ Pin specific versions for consistency
FROM python:3.11.6-slim

# ❌ Avoid unknown or custom images
FROM someuser/python-custom
```

**Security benefits:**

- Official images are regularly updated
- Security patches are applied promptly
- Trusted source reduces supply chain risks

---

## 🔐 Basic Environment Security

### Secure Python Configuration

```dockerfile
# ✅ Python security environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ✅ Disable Python debug mode
ENV PYTHONDEBUG=0
```

### Don't Include Secrets in Images

```dockerfile
# ❌ Never put secrets in Dockerfile
ENV DATABASE_PASSWORD=mysecretpassword

# ✅ Use environment variables at runtime
# docker run -e DATABASE_PASSWORD=secret myapp
```

### Basic .dockerignore

```dockerignore
# Security: exclude sensitive files
**/.env
**/.env.local
**/secrets/
**/*.key
**/*.pem
**/config.ini

# Development files
**/.git
**/venv/
**/__pycache__
```

---

## ✅ Security Checklist for Module 1

### Image Building

- [ ] Use official `python:3.11-slim` base image
- [ ] Create and use non-root user
- [ ] Set secure Python environment variables
- [ ] Use .dockerignore to exclude sensitive files

### Runtime Security

- [ ] Never pass secrets via environment variables in Dockerfile
- [ ] Use environment variables at container runtime instead
- [ ] Run container as non-root user

### Basic Best Practices

- [ ] Pin Python version for consistency
- [ ] Keep base image updated
- [ ] Don't install unnecessary packages

---

## 🎯 Module 1 Focus

For Module 1, these three security practices are essential:

1. **Non-root user** - Prevents privilege escalation
2. **Official base images** - Trusted, maintained source
3. **No secrets in images** - Keep sensitive data secure

These simple practices provide strong foundational security without complexity.

---

## 📖 Next Steps

Advanced security topics covered in later modules:

- **Module 3**: Code scanning and vulnerability detection
- **Module 4**: CI/CD security practices
- **Module 5**: Production security monitoring

---

**🔒 Remember**: Security is about layers. Start with these fundamentals and build upon them as you progress through the modules.
