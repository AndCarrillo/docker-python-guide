# 🤝 Contributing Guide

Thank you for your interest in contributing to the **Docker Python Guide**! This guide will help you understand how you can effectively contribute to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Project Structure](#project-structure)
- [Development Process](#development-process)
- [Code Standards](#code-standards)
- [Reporting Issues](#reporting-issues)
- [Pull Requests](#pull-requests)

## 📜 Code of Conduct

This project adheres to a code of conduct that we expect all participants to respect. Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## 🎯 How to Contribute

There are several ways to contribute to this project:

### 📝 Documentation

- Improve module README files
- Fix typos
- Add additional examples
- Translate content
- Improve setup instructions

### 💻 Code

- Create new practical examples
- Improve existing exercises
- Add automation scripts
- Optimize Dockerfiles
- Add tests

### 🐛 Bug Reports

- Find and report errors
- Validate fixes
- Test on different platforms

### 💡 Ideas and Suggestions

- Propose new modules
- Suggest content improvements
- Share best practices

## 🏗️ Project Structure

```
docker-python-guide/
├── README.md              # Main documentation (menu)
├── docs/                  # General documentation
├── scripts/               # Automation scripts
│   ├── setup.sh          # Setup for Linux/Mac
│   └── setup.ps1         # Setup for Windows
├── module-01-containerize/    # Separate branch
├── module-02-develop/         # Separate branch
├── module-03-linting-typing/  # Separate branch
├── module-04-cicd/           # Separate branch
└── module-05-deployment/     # Separate branch
```

### Module Branches

Each module has its own branch with the following structure:

```
module-XX-name/
├── README.md              # Module documentation
├── docs/                  # Specific documentation
├── examples/              # Practical examples
├── exercises/             # Exercises for students
├── src/                   # Source code
└── tests/                # Module tests
```

## 🔄 Development Process

### 1. Fork and Clone

```bash
# Fork the project on GitHub
git clone https://github.com/YOUR-USERNAME/docker-python-guide.git
cd docker-python-guide
```

### 2. Configure Upstream

```bash
git remote add upstream https://github.com/AndCarrillo/docker-python-guide.git
```

### 3. Create Working Branch

```bash
# For general contributions
git checkout -b feature/your-feature-name

# For module-specific contributions
git checkout module-01-containerize
git checkout -b feature/module-01-improvement
```

### 4. Make Changes

- Follow code conventions
- Add tests if applicable
- Update documentation
- Test your changes

### 5. Commit and Push

```bash
git add .
git commit -m "feat: clear description of the change"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

- Clearly describe the changes
- Reference related issues
- Include screenshots if visual

## 📏 Code Standards

### Python

- **Style**: Follow PEP 8
- **Formatting**: Use Black
- **Imports**: Use isort
- **Type hints**: Use when possible
- **Docstrings**: Google style

Example:

```python
def calculate_image_size(base_size: int, layers: int) -> int:
    """Calculate the total size of a Docker image.

    Args:
        base_size: Size of the base image in MB
        layers: Number of additional layers

    Returns:
        Total estimated size in MB

    Raises:
        ValueError: If base_size or layers is negative
    """
    if base_size < 0 or layers < 0:
        raise ValueError("Size and layers must be non-negative")

    return base_size + (layers * 50)  # Estimate 50MB per layer
```

### Docker

- **Multi-stage builds**: When appropriate
- **Command order**: Optimize for cache
- **Security**: Don't use root user
- **Size**: Minimize image size

Example Dockerfile:

```dockerfile
# Multi-stage build example
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim as runner

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

USER appuser
EXPOSE 8000
CMD ["python", "app.py"]
```

### Documentation

- **Markdown**: Use standard syntax
- **Structure**: Consistent headers
- **Examples**: Include executable code
- **Links**: Verify they work

### Commit Messages

Use Conventional Commits format:

```
feat: add FastAPI example with PostgreSQL
fix: correct Dockerfile for Python 3.11
docs: update module 2 README
test: add tests for Docker Compose exercise
chore: update dependencies
```

Valid types:

- `feat`: New functionality
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Add or modify tests
- `chore`: Maintenance tasks
- `refactor`: Code refactoring
- `style`: Format changes

## 🐛 Reporting Issues

### Before Reporting

1. Search existing issues
2. Verify it's not a local problem
3. Test with the latest version

### Issue Template

```markdown
## 🐛 Bug Description

Clear and concise description of the problem.

## 🔄 Steps to Reproduce

1. Go to '...'
2. Run '...'
3. Observe the error

## ✅ Expected Behavior

Description of what should happen.

## 📱 Environment

- OS: [e.g. Windows 11]
- Docker version: [e.g. 24.0.0]
- Python version: [e.g. 3.11]
- Branch/Module: [e.g. module-01-containerize]

## 📎 Additional Information

Logs, screenshots, etc.
```

## 🔀 Pull Requests

### Checklist Before Submitting

- [ ] Code follows established standards
- [ ] Tests pass (if applicable)
- [ ] Documentation updated
- [ ] Commits follow convention
- [ ] Branch updated with upstream
- [ ] PR template completed

### PR Template

```markdown
## 📝 Description

Clear description of the changes made.

## 🎯 Type of Change

- [ ] Bug fix
- [ ] New functionality
- [ ] Breaking change
- [ ] Documentation

## 🧪 Testing

- [ ] Existing tests pass
- [ ] New tests added
- [ ] Manually tested

## 📋 Checklist

- [ ] Code follows project standards
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Commits follow convention

## 🔗 Related Issues

Closes #123
```

## 🏷️ Labels

We use the following labels:

- `bug`: Something doesn't work
- `enhancement`: New functionality
- `documentation`: Documentation improvements
- `good first issue`: Good for beginners
- `help wanted`: Extra help welcome
- `module-01`: Related to module 1
- `module-02`: Related to module 2
- etc.

## 🎉 Recognition

All contributors will be recognized in:

- Main README
- Contributors list
- Release notes

## ❓ Need Help?

- Open an issue with `question` label
- Discuss in GitHub Discussions
- Review existing documentation

Thank you for contributing to the Docker Python Guide! 🚀
