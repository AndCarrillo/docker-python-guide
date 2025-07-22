# Automate your builds with GitHub Actions

> **Module branch:** `module-04-cicd`

Learn how to configure CI/CD using GitHub Actions for your Python application.

## What you'll learn

In this module, you will:

- ✅ Create automated test and build pipelines
- ✅ Configure Docker image building and pushing to registries
- ✅ Set up automated deployment workflows
- ✅ Implement security scanning and vulnerability checks
- ✅ Configure multi-environment deployments (dev, staging, prod)
- ✅ Set up automated code quality checks

## Prerequisites

Before starting this module, make sure you have completed:

- [Module 3: Linting and typing](../../tree/module-03-linting-typing)
- GitHub account with repository access
- Docker Hub or GitHub Container Registry account
- Basic understanding of GitHub Actions concepts

## Examples

This module includes comprehensive CI/CD setups:

### �️ Flask CI/CD Pipeline

**Location:** `examples/flask-cicd/`

A complete GitHub Actions workflow for Flask applications including:
- Automated testing with pytest
- Code quality checks with Ruff and Pyright
- Docker image building and pushing
- Multi-environment deployment

### ⚡ FastAPI Advanced Pipeline

**Location:** `examples/fastapi-cicd/`

An advanced FastAPI CI/CD setup featuring:
- Matrix testing across Python versions
- Security scanning with Trivy
- Automated API documentation deployment
- Blue-green deployment strategies

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
