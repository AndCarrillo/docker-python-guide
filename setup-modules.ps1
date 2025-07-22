# Script to set up module structure across all branches
# This script creates the basic structure for each module

Write-Host "🚀 Setting up Python Docker Guide modules..." -ForegroundColor Green

# Define modules configuration
$modules = @{
    "module-01-containerize" = @{
        "title" = "Containerize your app"
        "description" = "Learn how to containerize a Python application"
        "goals" = @(
            "Create optimized Dockerfiles for Python applications",
            "Implement security best practices and non-root users", 
            "Use multi-stage builds to reduce image size",
            "Configure health checks and monitoring"
        )
    }
    "module-02-develop" = @{
        "title" = "Develop your app"
        "description" = "Learn how to develop your Python application locally"
        "goals" = @(
            "Set up local development environment with Docker Compose",
            "Configure hot reload and live debugging in containers",
            "Manage environment variables and secrets",
            "Integrate databases and external services"
        )
    }
    "module-03-linting-typing" = @{
        "title" = "Linting and typing"
        "description" = "Learn how to set up linting, formatting and type checking"
        "goals" = @(
            "Configure Black, Flake8, and isort for code quality",
            "Set up mypy for static type checking",
            "Implement pre-commit hooks for automated checks",
            "Integrate code quality tools with containers"
        )
    }
    "module-04-cicd" = @{
        "title" = "Automate your builds with GitHub Actions"
        "description" = "Learn how to configure CI/CD using GitHub Actions"
        "goals" = @(
            "Create automated test and build pipelines",
            "Configure Docker image building and pushing",
            "Set up automated deployment workflows",
            "Implement security scanning and vulnerability checks"
        )
    }
    "module-05-deployment" = @{
        "title" = "Test your deployment"
        "description" = "Learn how to develop locally using Kubernetes"
        "goals" = @(
            "Deploy applications locally with Kubernetes",
            "Configure health checks and monitoring",
            "Implement rolling updates and rollback strategies",
            "Test and debug containerized applications"
        )
    }
}

# Store current branch
$currentBranch = git branch --show-current

Write-Host "📋 Current branch: $currentBranch" -ForegroundColor Yellow

foreach ($module in $modules.GetEnumerator()) {
    $branchName = $module.Key
    $config = $module.Value
    
    Write-Host "`n🌿 Setting up branch: $branchName" -ForegroundColor Cyan
    
    # Switch to module branch
    git checkout $branchName
    
    # Create module README template
    $readmeContent = @"
# $($config.title)

> **Module branch:** ``$branchName``

$($config.description).

## What you'll learn

In this module, you will:

$($config.goals | ForEach-Object { "- ✅ $_" } | Out-String)

## Examples

This module includes two progressive examples:

### 🌶️ Flask Basic Example
**Location:** ``examples/flask-basic/``

A simple Flask application that demonstrates the fundamental concepts of this module.

### ⚡ FastAPI Modern Example  
**Location:** ``examples/fastapi-modern/``

An advanced FastAPI application that showcases more sophisticated patterns and practices.

## Prerequisites

Before starting this module, make sure you have completed:
- Previous modules (if applicable)
- Have Docker Desktop installed and running
- Basic understanding of Python and web frameworks

## Getting Started

1. **Clone and switch to this module:**
   ``````bash
   git clone https://github.com/AndCarrillo/docker-python-guide.git
   cd docker-python-guide
   git checkout $branchName
   ``````

2. **Follow the step-by-step guide below** ⬇️

---

## 📚 Step-by-Step Guide

> **🚧 Under Construction**  
> This module is currently being developed. Check back soon for complete instructions!

### Step 1: [Coming Soon]
### Step 2: [Coming Soon] 
### Step 3: [Coming Soon]

---

## 🧩 Examples

### Flask Basic Example

**Purpose:** [Description coming soon]

**Key concepts:**
- [Concept 1]
- [Concept 2]
- [Concept 3]

**Files:**
``````
examples/flask-basic/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
└── README.md          # Example-specific instructions
``````

### FastAPI Modern Example

**Purpose:** [Description coming soon]

**Key concepts:**
- [Concept 1]
- [Concept 2] 
- [Concept 3]

**Files:**
``````
examples/fastapi-modern/
├── main.py            # Main FastAPI application
├── requirements.txt   # Python dependencies
├── Dockerfile        # Docker configuration
└── README.md         # Example-specific instructions
``````

---

## 🎯 Next Steps

After completing this module:

1. **Test your understanding** - Try the exercises in each example
2. **Experiment** - Modify the examples to see how they work
3. **Move to the next module** - Continue with the next module in the series

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## 🤝 Need Help?

- 📖 Check the [main README](../../README.md) for general guidance
- 🐛 [Open an issue](../../issues) if you find problems
- 💬 [Start a discussion](../../discussions) for questions

---

**⬅️ [Back to main guide](../../README.md)**
"@

    # Write README for the module
    $readmeContent | Out-File -FilePath "README.md" -Encoding UTF8
    
    Write-Host "   ✅ Created README.md for $branchName" -ForegroundColor Green
}

# Return to original branch
Write-Host "`n🔄 Returning to branch: $currentBranch" -ForegroundColor Yellow
git checkout $currentBranch

Write-Host "`n🎉 Module setup complete!" -ForegroundColor Green
Write-Host "📝 Each module branch now has a basic README template" -ForegroundColor White
Write-Host "🚀 You can now switch to any module branch and start developing the content" -ForegroundColor White
