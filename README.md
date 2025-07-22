# Linting and typing

> **Module branch:** `module-03-linting-typing`

Learn how to set up linting, formatting and type checking for your Python application.

## What you'll learn

In this module, you will:

- ✅ Configure Ruff for linting and formatting
- ✅ Set up Pyright for static type checking
- ✅ Implement pre-commit hooks for automated checks
- ✅ Integrate code quality tools with containers

## Prerequisites

Before starting this module, make sure you have completed:

- [Module 2: Develop your app](../../tree/module-02-develop)
- Basic understanding of Python type hints
- Familiarity with code quality concepts

## Examples

This module enhances the examples from previous modules:

### �️ Flask with Quality Tools

**Location:** `examples/flask-quality/`

Flask application with complete linting, formatting, and type checking setup.

### ⚡ FastAPI with Type Safety

**Location:** `examples/fastapi-quality/`

FastAPI application with advanced type checking and validation patterns.

## Getting Started

1. **Clone and switch to this module:**

   ```bash
   git clone https://github.com/AndCarrillo/docker-python-guide.git
   cd docker-python-guide
   git checkout module-03-linting-typing
   ```

2. **Follow the step-by-step guide below** ⬇️

---

## 📚 Step-by-Step Guide

### Overview

In this section, you'll learn how to set up code quality tools for your Python application. This includes:

- **Linting and formatting** with Ruff
- **Static type checking** with Pyright
- **Automating checks** with pre-commit hooks

### Step 1: Linting and formatting with Ruff

Ruff is an extremely fast Python linter and formatter written in Rust. It replaces multiple tools like flake8, isort, and black with a single unified tool.

**Create a `pyproject.toml` file:**

```toml
[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]
```

**Using Ruff:**

Run these commands to check and format your code:

```bash
# Check for errors
ruff check .

# Automatically fix fixable errors
ruff check --fix .

# Format code
ruff format .
```

### Step 2: Type checking with Pyright

Pyright is a fast static type checker for Python that works well with modern Python features.

**Add Pyright configuration in `pyproject.toml`:**

```toml
[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv"]
```

**Running Pyright:**

To check your code for type errors:

```bash
pyright
```

### Step 3: Setting up pre-commit hooks

Pre-commit hooks automatically run checks before each commit. Create a `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.2.2
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

**To install and use:**

```bash
pre-commit install
git commit -m "Test commit"  # Automatically runs checks
```

### Step 4: Integration with Docker

For containerized development, add quality tools to your development Dockerfile:

```dockerfile
# Add development dependencies
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Development tools available in container
CMD ["bash"]
```

---

## 🧩 Examples

### Flask with Quality Tools

**Purpose:** Learn to integrate code quality tools with a Flask application.

**Key concepts:**

- Ruff configuration for web applications
- Type hints for Flask routes and models
- Pre-commit hooks integration
- Container-based quality checks

**Files:**

```
examples/flask-quality/
├── app.py                    # Type-annotated Flask application
├── pyproject.toml           # Ruff and Pyright configuration
├── .pre-commit-config.yaml  # Pre-commit hooks setup
├── requirements.txt         # Runtime dependencies
├── requirements-dev.txt     # Development dependencies
├── Dockerfile              # Development container with tools
├── docker-compose.yml      # Development environment
└── README.md               # Example instructions
```

### FastAPI with Type Safety

**Purpose:** Advanced type checking patterns with FastAPI and Pydantic.

**Key concepts:**

- Strict type checking configuration
- Pydantic model validation
- Advanced type annotations
- Automated quality pipeline

**Files:**

```
examples/fastapi-quality/
├── main.py                  # Fully type-annotated FastAPI app
├── models.py               # Pydantic models with advanced types
├── pyproject.toml          # Strict quality configuration
├── .pre-commit-config.yaml # Comprehensive hooks
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Development dependencies
├── Dockerfile             # Quality-focused development image
├── docker-compose.yml     # Development environment
└── README.md              # Example instructions
```

---

## 🔧 Common Quality Commands

### Daily Development Workflow

```bash
# Check code quality
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Format code
ruff format .

# Type check
pyright

# Run all checks (as pre-commit would)
pre-commit run --all-files
```

### Container-based Quality Checks

```bash
# Run quality checks in container
docker-compose exec web ruff check .
docker-compose exec web pyright

# Format code using container
docker-compose exec web ruff format .

# Install pre-commit in container
docker-compose exec web pre-commit install
```

### CI/CD Integration

```bash
# Commands for CI pipelines
ruff check --output-format=github .
pyright --outputjson
pre-commit run --all-files --show-diff-on-failure
```

---

## 🔧 Hands-on Exercises

### Exercise 1: Flask Quality Setup

1. Navigate to `examples/flask-quality/`
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Run initial quality checks:
   ```bash
   ruff check .
   pyright
   ```
4. Fix any issues found and re-run checks
5. Set up pre-commit hooks: `pre-commit install`

**Questions to explore:**

- What quality issues were found initially?
- How does type checking improve code reliability?
- What happens when you commit code with issues?

### Exercise 2: FastAPI Advanced Types

1. Navigate to `examples/fastapi-quality/`
2. Examine the strict type checking configuration
3. Run comprehensive quality checks:
   ```bash
   ruff check .
   pyright --warnings
   ```
4. Try adding code with type errors and see how they're caught

**Questions to explore:**

- How do Pydantic models help with type safety?
- What advanced type patterns are demonstrated?
- How does strict mode affect development?

### Exercise 3: Container Quality Workflow

1. Use Docker Compose to run quality checks
2. Set up pre-commit hooks inside containers
3. Create a quality-focused development workflow:
   ```bash
   docker-compose up -d
   docker-compose exec web pre-commit install
   # Make code changes and commit
   ```

**Questions to explore:**

- How do containerized quality tools ensure consistency?
- What are the trade-offs of container-based vs local tools?
- How can this be integrated into team workflows?

---

## 🎯 Key Takeaways

After completing this module, you should understand:

1. **Modern Python Tooling** - Ruff as a unified solution for linting and formatting
2. **Type Safety** - Pyright for catching errors before runtime
3. **Automation** - Pre-commit hooks for consistent quality enforcement
4. **Container Integration** - Running quality tools in development containers
5. **Team Workflow** - Establishing quality standards across development teams

## 🚀 Next Steps

Ready for the next module? Continue with:

**[Module 4: CI/CD with GitHub Actions](../../tree/module-04-cicd)** - Learn how to automate quality checks and deployments.

---

## 📚 Additional Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pyright Documentation](https://github.com/microsoft/pyright)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## 🤝 Need Help?

- 📖 Check the [main README](../../README.md) for general guidance
- 🐛 [Open an issue](../../issues) if you find problems
- 💬 [Start a discussion](../../discussions) for questions

---

## Summary

In this section, you learned how to:

- ✅ Configure and use Ruff for linting and formatting
- ✅ Set up Pyright for static type checking
- ✅ Automate checks with pre-commit hooks
- ✅ Integrate quality tools with containerized development

These tools help maintain code quality and catch errors early in development.

---

**⬅️ [Back to main guide](../../README.md)**

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
