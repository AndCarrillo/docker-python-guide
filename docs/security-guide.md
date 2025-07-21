# 🔒 Container Security Best Practices

Essential security considerations for containerizing Python applications.

## 🎯 Overview

Container security is a multi-layered approach that includes secure image building, runtime protection, and ongoing monitoring. This guide focuses on practical security measures for Python containers.

## 📋 Table of Contents

- [Image Security](#-image-security)
- [Runtime Security](#-runtime-security)
- [Access Control](#-access-control)
- [Secrets Management](#-secrets-management)
- [Network Security](#-network-security)
- [Monitoring & Scanning](#-monitoring--scanning)
- [Security Checklist](#-security-checklist)

---

## 🛡️ Image Security

### Base Image Security

```dockerfile
# ✅ Use official, maintained images
FROM python:3.11-slim

# ✅ Pin specific versions
FROM python:3.11.6-slim

# ❌ Avoid unknown or outdated images
FROM someuser/python-custom
FROM python:3.8-slim  # outdated version
```

### Minimal Attack Surface

```dockerfile
# ✅ Install only necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean

# ❌ Avoid development tools in production
RUN apt-get install -y \
    gcc \
    make \
    git \
    vim \
    wget
```

### Package Vulnerability Management

```dockerfile
# ✅ Update packages regularly
RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# ✅ Use specific package versions
RUN apt-get update && apt-get install -y \
    curl=7.74.0-1.3+deb11u7 \
    && rm -rf /var/lib/apt/lists/*
```

---

## 👤 Access Control

### Non-Root User Implementation

```dockerfile
# ✅ Method 1: Simple user creation
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

# ✅ Method 2: Specific UID/GID for consistency
RUN groupadd -r appgroup --gid 1000 \
    && useradd -r -g appgroup --uid 1000 --home-dir /app --shell /bin/bash appuser \
    && chown -R appuser:appgroup /app
USER appuser

# ✅ Method 3: Use existing nobody user
USER nobody

# ❌ Never run as root in production
USER root
```

### File Permissions

```dockerfile
# ✅ Secure file permissions
COPY --chown=appuser:appuser . /app
RUN chmod -R 755 /app \
    && chmod -R 644 /app/*.py \
    && chmod +x /app/entrypoint.sh

# ✅ Remove write permissions where not needed
RUN chmod -R a-w /app/config/
```

### Capability Dropping

```bash
# ✅ Run with minimal capabilities
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE your-app

# ✅ Use security profiles
docker run --security-opt seccomp=default.json your-app
```

---

## 🔐 Secrets Management

### Environment Variables

```dockerfile
# ❌ Never hardcode secrets
ENV SECRET_KEY=mysupersecretkey123
ENV DATABASE_PASSWORD=admin123

# ✅ Use empty defaults
ENV SECRET_KEY=""
ENV DATABASE_PASSWORD=""
```

### Runtime Secret Injection

```bash
# ✅ Use environment files
docker run --env-file .env.production your-app

# ✅ Use Docker secrets (Docker Swarm)
echo "mysecret" | docker secret create db_password -
docker service create --secret db_password your-app

# ✅ Use external secret management
docker run -e SECRET_KEY="$(vault kv get -field=key secret/app)" your-app
```

### Secret Files

```dockerfile
# ✅ Mount secrets at runtime
# Don't copy secrets into image
VOLUME ["/run/secrets"]
```

```bash
# Mount secrets directory
docker run -v /host/secrets:/run/secrets:ro your-app
```

### Python Secret Handling

```python
# ✅ Secure secret loading
import os
from pathlib import Path

def get_secret(secret_name, default=None):
    """Load secret from file or environment variable."""
    # Try file first (Docker secrets)
    secret_file = Path(f"/run/secrets/{secret_name}")
    if secret_file.exists():
        return secret_file.read_text().strip()

    # Fall back to environment variable
    return os.getenv(secret_name, default)

# Usage
SECRET_KEY = get_secret("SECRET_KEY")
DATABASE_PASSWORD = get_secret("DATABASE_PASSWORD")
```

---

## 🌐 Network Security

### Port Exposure

```dockerfile
# ✅ Only expose necessary ports
EXPOSE 8000

# ❌ Don't expose internal services
EXPOSE 5432  # Database port shouldn't be exposed from app container
```

### Network Isolation

```yaml
# docker-compose.yml - ✅ Network isolation
version: "3.8"
services:
  app:
    networks:
      - frontend
      - backend

  database:
    networks:
      - backend # Not accessible from frontend

networks:
  frontend:
  backend:
```

### TLS/SSL Configuration

```python
# ✅ Force HTTPS in production
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

if app.config.get('ENVIRONMENT') == 'production':
    Talisman(app, force_https=True)
```

---

## 🔍 Monitoring & Scanning

### Vulnerability Scanning

```bash
# ✅ Scan images for vulnerabilities
docker scan your-app:latest

# ✅ Use Trivy for comprehensive scanning
trivy image your-app:latest

# ✅ Use Snyk for dependency scanning
snyk test --docker your-app:latest
```

### Runtime Monitoring

```dockerfile
# ✅ Add monitoring capabilities
RUN pip install --no-cache-dir prometheus-client

# In your Python app:
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter('app_requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('app_request_duration_seconds', 'Request latency')
```

### Log Security

```python
# ✅ Secure logging configuration
import logging
import re

class SecurityFilter(logging.Filter):
    """Filter out sensitive information from logs."""

    def filter(self, record):
        # Remove sensitive patterns
        message = record.getMessage()
        # Remove potential passwords, tokens, etc.
        message = re.sub(r'password=[^&\s]+', 'password=***', message, flags=re.IGNORECASE)
        message = re.sub(r'token=[^&\s]+', 'token=***', message, flags=re.IGNORECASE)
        record.msg = message
        return True

# Apply to all loggers
logging.getLogger().addFilter(SecurityFilter())
```

---

## 🔒 Security Hardening

### Read-Only Filesystem

```bash
# ✅ Use read-only root filesystem
docker run --read-only --tmpfs /tmp --tmpfs /var/run your-app
```

```dockerfile
# ✅ Create writable directories for read-only filesystem
RUN mkdir -p /app/tmp /app/logs \
    && chown -R appuser:appuser /app/tmp /app/logs

VOLUME ["/app/tmp", "/app/logs"]
```

### Resource Limits

```bash
# ✅ Set resource limits
docker run \
  --memory=512m \
  --cpus="1.0" \
  --pids-limit=100 \
  your-app
```

```yaml
# docker-compose.yml - ✅ Resource limits
version: "3.8"
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"
        reservations:
          memory: 256M
          cpus: "0.5"
```

### No New Privileges

```bash
# ✅ Prevent privilege escalation
docker run --security-opt no-new-privileges:true your-app
```

---

## 🧪 Security Testing

### Container Security Testing

```bash
# ✅ Test with Docker Bench Security
docker run -it --net host --pid host --userns host --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /etc:/etc:ro \
  -v /usr/bin/containerd:/usr/bin/containerd:ro \
  -v /usr/bin/runc:/usr/bin/runc:ro \
  -v /usr/lib/systemd:/usr/lib/systemd:ro \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --label docker_bench_security \
  docker/docker-bench-security
```

### Penetration Testing

```python
# ✅ Include security headers
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

# Configure security headers
Talisman(app,
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'"
    }
)
```

---

## 📊 Security Checklist

### Build-Time Security

- [ ] **Base Image**

  - [ ] Use official, maintained images
  - [ ] Pin specific versions
  - [ ] Regularly update base images

- [ ] **Dependencies**

  - [ ] Pin all dependency versions
  - [ ] Regularly scan for vulnerabilities
  - [ ] Remove unnecessary packages

- [ ] **Secrets**

  - [ ] No hardcoded secrets in Dockerfile
  - [ ] No secrets in environment variables
  - [ ] Use proper secret management

- [ ] **User Configuration**
  - [ ] Create and use non-root user
  - [ ] Set proper file permissions
  - [ ] Drop unnecessary capabilities

### Runtime Security

- [ ] **Container Configuration**

  - [ ] Run with minimal privileges
  - [ ] Use read-only filesystem when possible
  - [ ] Set resource limits
  - [ ] Enable security profiles

- [ ] **Network Security**

  - [ ] Only expose necessary ports
  - [ ] Use network isolation
  - [ ] Implement TLS/SSL

- [ ] **Monitoring**
  - [ ] Enable security logging
  - [ ] Set up vulnerability scanning
  - [ ] Monitor runtime behavior

### Ongoing Security

- [ ] **Updates**

  - [ ] Regular base image updates
  - [ ] Dependency updates
  - [ ] Security patch management

- [ ] **Scanning**
  - [ ] Automated vulnerability scanning
  - [ ] Security testing in CI/CD
  - [ ] Regular security audits

---

## 🚨 Incident Response

### Security Incident Preparation

```bash
# ✅ Prepare incident response commands
# Stop compromised container
docker stop <container-id>

# Inspect container for forensics
docker diff <container-id>
docker logs <container-id>

# Export container for analysis
docker export <container-id> > compromised-container.tar

# Remove compromised container
docker rm <container-id>

# Scan and rebuild clean image
docker scan your-app:latest
docker build --no-cache -t your-app:latest .
```

### Emergency Security Measures

```python
# ✅ Emergency shutdown endpoint
from flask import Flask, request
import os
import signal

app = Flask(__name__)

@app.route('/emergency-shutdown', methods=['POST'])
def emergency_shutdown():
    """Emergency shutdown endpoint."""
    auth_token = request.headers.get('Authorization')
    if auth_token != f"Bearer {os.getenv('EMERGENCY_TOKEN')}":
        return "Unauthorized", 401

    # Log the shutdown
    app.logger.critical("Emergency shutdown initiated")

    # Graceful shutdown
    os.kill(os.getpid(), signal.SIGTERM)
    return "Shutdown initiated", 200
```

---

## 🔗 Security Tools & Resources

### Scanning Tools

- **Trivy**: Comprehensive vulnerability scanner
- **Snyk**: Dependency vulnerability scanning
- **Clair**: Static analysis of vulnerabilities
- **Docker Scout**: Docker's native security scanning

### Security Frameworks

- **CIS Docker Benchmark**: Security configuration guidelines
- **NIST Container Security**: Comprehensive security guide
- **OWASP Container Security**: Web application security

### Python Security Libraries

```python
# Security libraries for Python applications
pip install flask-talisman      # Security headers
pip install cryptography        # Cryptographic operations
pip install bcrypt              # Password hashing
pip install pyotp               # Two-factor authentication
pip install validators          # Input validation
```

---

**🔒 Remember**: Security is an ongoing process, not a one-time setup. Regularly review and update your security measures as threats evolve.

**📖 Next Steps**: Review [Image Optimization Guide](optimization-guide.md) for performance improvements that don't compromise security.
