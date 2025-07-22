# Módulo 4: Automate your builds with GitHub Actions

> **Branch del módulo:** `module-04-cicd`

Aprende a configurar CI/CD usando GitHub Actions para automatizar builds, testing y deployment de aplicaciones Python con Docker.

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, podrás:

- **Configurar pipelines CI/CD completos** con GitHub Actions para automatizar builds, tests y despliegues
- **Implementar estrategias de testing avanzadas** con cobertura de código, quality gates y performance testing
- **Crear workflows sofisticados** con matrix builds, caching, security scanning y optimizaciones
- **Integrar múltiples herramientas** de calidad, seguridad y monitoreo en tus pipelines
- **Configurar container registries** y automated deployments con rollback capabilities
- **Aplicar best practices** de DevOps, Site Reliability Engineering (SRE) y modern deployment strategies

## 📋 Prerequisitos

- Completar [Módulo 1](../../../tree/module-01-containerize), [Módulo 2](../../../tree/module-02-compose) y [Módulo 3](../../../tree/module-03-networking)
- Cuenta de GitHub con acceso a repositorios
- Cuenta de Docker Hub o GitHub Container Registry
- Conocimiento sólido de Git y GitHub
- Familiaridad con conceptos de CI/CD y DevOps
- Comprensión profunda de Docker y containerización

## 📚 Ejemplos Prácticos Completos

### 🔥 Flask CI/CD Pipeline

**Location:** `examples/flask-cicd/`

Pipeline completo para aplicaciones Flask con enfoque tradicional:

- ✅ **Flask Application** con PostgreSQL y Redis
- ✅ **Comprehensive Testing** con pytest, coverage reporting
- ✅ **Code Quality** con Ruff linting y Pyright type checking
- ✅ **Security Scanning** con Safety y Bandit
- ✅ **Multi-stage Docker** builds optimizados para producción
- ✅ **GitHub Actions Pipeline** con 4 jobs completamente integrados
- ✅ **Container Registry** integration con GitHub Packages
- ✅ **Production Deployment** con health checks y monitoring

```bash
cd examples/flask-cicd
docker-compose up --build
# Accede a: http://localhost:5000
```

### 🚀 FastAPI Advanced CI/CD Pipeline

**Location:** `examples/fastapi-cicd/`

Pipeline avanzado para aplicaciones FastAPI modernas:

- ✅ **FastAPI Async** con SQLAlchemy 2.0 y Redis async
- ✅ **Matrix Testing** across Python 3.10, 3.11, 3.12
- ✅ **Performance Testing** con Locust y load analysis
- ✅ **Advanced Security** con Safety, Bandit y Semgrep
- ✅ **Auto-generated Documentation** con OpenAPI/Swagger
- ✅ **Background Tasks** y async patterns
- ✅ **Smoke Tests** y post-deployment verification
- ✅ **Production-ready** deployment con comprehensive monitoring

```bash
cd examples/fastapi-cicd
docker-compose up --build
# Accede a: http://localhost:8000/docs
```

## 📊 Comparison Table

| Feature | Flask CI/CD | FastAPI CI/CD |
|---------|------------|---------------|
| **Application Type** | Traditional sync API | Modern async API |
| **Python Versions** | 3.11 | 3.10, 3.11, 3.12 (matrix) |
| **Testing Strategy** | Standard pytest | Async pytest + performance |
| **Security Scanning** | Safety + Bandit | Safety + Bandit + Semgrep |
| **Documentation** | Manual setup | Auto-generated (OpenAPI) |
| **Performance** | Good | High throughput (async) |
| **Complexity** | Moderate | Advanced |
| **Best for** | Traditional web apps | High-performance APIs |

## 🔧 GitHub Actions Workflows

### Flask Pipeline Features
```yaml
jobs:
  test:        # Pytest + Ruff + Pyright + Coverage
  security:    # Safety + Bandit security scanning  
  build:       # Docker build + GitHub Packages push
  deploy:      # Production deployment + health checks
```

### FastAPI Pipeline Features  
```yaml
jobs:
  test:        # Matrix testing (Python 3.10-3.12)
  performance: # Locust load testing + analysis
  security:    # Safety + Bandit + Semgrep scanning
  build:       # Optimized Docker builds + caching
  deploy:      # Advanced deployment + smoke tests
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

## 🎯 Próximos Pasos

Una vez completado este módulo, continúa con:

**[Módulo 5: Test your deployment](../../../tree/module-05-deployment)** - Aprende sobre Kubernetes, monitoring y production deployment strategies.

---

## 🤝 Contribuciones

¿Tienes sugerencias o mejoras? ¡Contribuye al proyecto!

1. Fork el repositorio
2. Crea tu feature branch (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

---

**📅 Última actualización:** Julio 2025  
**👨‍💻 Mantenido por:** Andrea Carrillo - [GitHub](https://github.com/AndCarrillo)
