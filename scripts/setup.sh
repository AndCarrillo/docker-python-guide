#!/bin/bash

# 🚀 Setup Script para Docker Python Guide
# Este script configura el entorno necesario para seguir la guía

set -e

echo "🐍 Docker Python Guide - Setup Script"
echo "======================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes de estado
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar prerequisitos
check_prerequisites() {
    print_status "Verificando prerequisitos..."
    
    # Verificar Docker
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        print_success "Docker encontrado: v$DOCKER_VERSION"
    else
        print_error "Docker no está instalado. Por favor instala Docker Desktop desde https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    
    # Verificar Docker Compose
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        print_success "Docker Compose disponible"
    else
        print_warning "Docker Compose no encontrado. Se instalará automáticamente con Docker Desktop moderno."
    fi
    
    # Verificar Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python3 encontrado: v$PYTHON_VERSION"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version | cut -d' ' -f2)
        print_success "Python encontrado: v$PYTHON_VERSION"
    else
        print_error "Python no está instalado. Por favor instala Python 3.9+ desde https://www.python.org"
        exit 1
    fi
    
    # Verificar Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        print_success "Git encontrado: v$GIT_VERSION"
    else
        print_error "Git no está instalado. Por favor instala Git desde https://git-scm.com"
        exit 1
    fi
}

# Crear estructura de directorios
create_directories() {
    print_status "Creando estructura de directorios..."
    
    mkdir -p {docs,scripts,examples,exercises}
    
    print_success "Estructura de directorios creada"
}

# Configurar Git hooks (si se está en un repo git)
setup_git_hooks() {
    if [ -d ".git" ]; then
        print_status "Configurando Git hooks..."
        
        # Crear pre-commit hook básico
        cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
# Basic pre-commit hook for Docker Python Guide

echo "🔍 Ejecutando checks básicos..."

# Verificar que no se commiteen archivos sensibles
if git diff --cached --name-only | grep -E "\.(env|key|pem|p12|pfx)$"; then
    echo "❌ Error: Intentando commitear archivos sensibles"
    exit 1
fi

echo "✅ Pre-commit checks completados"
EOF
        
        chmod +x .git/hooks/pre-commit
        print_success "Git hooks configurados"
    fi
}

# Crear archivo de configuración del entorno
create_env_template() {
    print_status "Creando template de variables de entorno..."
    
    cat > .env.template << 'EOF'
# 🔧 Variables de Entorno - Docker Python Guide
# Copia este archivo a .env y configura los valores según tu entorno

# Configuración de la aplicación
APP_NAME=docker-python-guide
APP_VERSION=1.0.0
APP_PORT=8000

# Configuración de Python
PYTHON_VERSION=3.11
PYTHONPATH=/app

# Configuración de base de datos (para módulos avanzados)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=appdb
DB_USER=appuser
DB_PASSWORD=changeme

# Configuración de Redis (para módulos avanzados)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Configuración de desarrollo
DEBUG=true
LOG_LEVEL=INFO

# Configuración de Docker
DOCKER_REGISTRY=docker.io
DOCKER_NAMESPACE=dockerpythonguide
EOF
    
    print_success "Template .env.template creado"
}

# Crear Makefile para comandos comunes
create_makefile() {
    print_status "Creando Makefile con comandos útiles..."
    
    cat > Makefile << 'EOF'
.PHONY: help setup clean docker-build docker-run test lint format

# 🎯 Docker Python Guide - Comandos Útiles
help: ## Mostrar esta ayuda
	@echo "Docker Python Guide - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Configurar entorno inicial
	@echo "🚀 Configurando entorno..."
	@./scripts/setup.sh

clean: ## Limpiar archivos temporales y contenedores
	@echo "🧹 Limpiando..."
	@docker system prune -f
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete

docker-build: ## Construir imagen Docker
	@echo "🐳 Construyendo imagen Docker..."
	@docker build -t docker-python-guide .

docker-run: ## Ejecutar contenedor
	@echo "🚀 Ejecutando contenedor..."
	@docker run -p 8000:8000 docker-python-guide

test: ## Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	@python -m pytest tests/ -v

lint: ## Ejecutar linting
	@echo "🔍 Ejecutando linting..."
	@flake8 src/
	@mypy src/

format: ## Formatear código
	@echo "✨ Formateando código..."
	@black src/
	@isort src/

check-modules: ## Verificar disponibilidad de módulos
	@echo "📚 Verificando módulos disponibles..."
	@git branch -r | grep "module-" | sed 's/origin\///' | sort

switch-module: ## Cambiar a un módulo específico (uso: make switch-module MODULE=01)
	@echo "🔄 Cambiando a módulo $(MODULE)..."
	@git checkout module-$(MODULE)-*

status: ## Mostrar estado del proyecto
	@echo "📊 Estado del proyecto:"
	@echo "Branch actual: $$(git branch --show-current)"
	@echo "Último commit: $$(git log -1 --oneline)"
	@echo "Archivos modificados: $$(git status --porcelain | wc -l)"
EOF
    
    print_success "Makefile creado"
}

# Función principal
main() {
    echo ""
    print_status "Iniciando configuración del entorno..."
    echo ""
    
    check_prerequisites
    echo ""
    
    create_directories
    create_env_template
    create_makefile
    setup_git_hooks
    
    echo ""
    print_success "¡Configuración completada exitosamente! 🎉"
    echo ""
    print_status "Próximos pasos:"
    echo "  1. Revisa el README.md para entender la estructura de la guía"
    echo "  2. Ejecuta 'make help' para ver comandos disponibles"
    echo "  3. Comienza con el Módulo 1: 'make switch-module MODULE=01'"
    echo "  4. Copia .env.template a .env y configura según necesites"
    echo ""
    print_status "¡Happy coding! 🐍🐳"
}

# Ejecutar función principal
main
