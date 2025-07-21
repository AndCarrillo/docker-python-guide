# 🚀 Setup Script para Docker Python Guide (PowerShell)
# Este script configura el entorno necesario para seguir la guía

param(
    [switch]$SkipPrerequisites,
    [switch]$Verbose
)

# Configuración de colores
$script:Colors = @{
    Red = [System.ConsoleColor]::Red
    Green = [System.ConsoleColor]::Green
    Yellow = [System.ConsoleColor]::Yellow
    Blue = [System.ConsoleColor]::Blue
    White = [System.ConsoleColor]::White
}

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $script:Colors.Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $script:Colors.Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $script:Colors.Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $script:Colors.Red
}

function Test-Prerequisites {
    Write-Status "Verificando prerequisitos..."
    
    $allGood = $true
    
    # Verificar Docker
    try {
        $dockerVersion = docker --version 2>$null
        if ($dockerVersion) {
            $version = $dockerVersion -replace '.*version ([^,]+).*', '$1'
            Write-Success "Docker encontrado: v$version"
        } else {
            throw "Docker no encontrado"
        }
    } catch {
        Write-Error "Docker no está instalado. Descarga Docker Desktop desde https://www.docker.com/products/docker-desktop"
        $allGood = $false
    }
    
    # Verificar Docker Compose
    try {
        $composeVersion = docker compose version 2>$null
        if ($composeVersion) {
            Write-Success "Docker Compose disponible"
        } else {
            docker-compose --version 2>$null | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Docker Compose (legacy) disponible"
            } else {
                Write-Warning "Docker Compose no encontrado explícitamente, pero puede estar incluido en Docker Desktop"
            }
        }
    } catch {
        Write-Warning "Docker Compose no encontrado explícitamente"
    }
    
    # Verificar Python
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion) {
            $version = $pythonVersion -replace 'Python ', ''
            Write-Success "Python encontrado: v$version"
        } else {
            $python3Version = python3 --version 2>$null
            if ($python3Version) {
                $version = $python3Version -replace 'Python ', ''
                Write-Success "Python3 encontrado: v$version"
            } else {
                throw "Python no encontrado"
            }
        }
    } catch {
        Write-Error "Python no está instalado. Descarga Python 3.9+ desde https://www.python.org"
        $allGood = $false
    }
    
    # Verificar Git
    try {
        $gitVersion = git --version 2>$null
        if ($gitVersion) {
            $version = $gitVersion -replace '.*version ([^ ]+).*', '$1'
            Write-Success "Git encontrado: v$version"
        } else {
            throw "Git no encontrado"
        }
    } catch {
        Write-Error "Git no está instalado. Descarga Git desde https://git-scm.com"
        $allGood = $false
    }
    
    if (-not $allGood) {
        Write-Error "Por favor instala los prerequisitos faltantes antes de continuar."
        exit 1
    }
}

function New-DirectoryStructure {
    Write-Status "Creando estructura de directorios..."
    
    $directories = @("docs", "scripts", "examples", "exercises")
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            if ($Verbose) {
                Write-Status "Creado directorio: $dir"
            }
        }
    }
    
    Write-Success "Estructura de directorios creada"
}

function Set-GitHooks {
    if (Test-Path ".git") {
        Write-Status "Configurando Git hooks..."
        
        $hookPath = ".git\hooks\pre-commit"
        $hookContent = @'
#!/bin/sh
# Basic pre-commit hook for Docker Python Guide

echo "🔍 Ejecutando checks básicos..."

# Verificar que no se commiteen archivos sensibles
if git diff --cached --name-only | grep -E "\.(env|key|pem|p12|pfx)$"; then
    echo "❌ Error: Intentando commitear archivos sensibles"
    exit 1
fi

echo "✅ Pre-commit checks completados"
'@
        
        $hookContent | Out-File -FilePath $hookPath -Encoding UTF8
        
        # En Windows, hacer el archivo ejecutable puede requerir permisos adicionales
        try {
            & git update-index --chmod=+x $hookPath 2>$null
        } catch {
            Write-Warning "No se pudo hacer el hook ejecutable automáticamente"
        }
        
        Write-Success "Git hooks configurados"
    }
}

function New-EnvironmentTemplate {
    Write-Status "Creando template de variables de entorno..."
    
    $envTemplate = @'
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
'@
    
    $envTemplate | Out-File -FilePath ".env.template" -Encoding UTF8
    Write-Success "Template .env.template creado"
}

function New-PowerShellHelper {
    Write-Status "Creando helper de PowerShell..."
    
    $helperContent = @'
# 🎯 Docker Python Guide - PowerShell Helper
# Funciones útiles para trabajar con la guía

function Show-DockerPythonGuideHelp {
    Write-Host "🐍 Docker Python Guide - Comandos PowerShell" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Comandos disponibles:" -ForegroundColor Yellow
    Write-Host "  Build-DockerImage          - Construir imagen Docker"
    Write-Host "  Start-DockerContainer      - Iniciar contenedor"
    Write-Host "  Test-Application          - Ejecutar tests"
    Write-Host "  Format-Code               - Formatear código Python"
    Write-Host "  Switch-Module <number>    - Cambiar a módulo específico"
    Write-Host "  Show-ModuleStatus         - Mostrar estado de módulos"
    Write-Host "  Clean-Environment         - Limpiar archivos temporales"
    Write-Host ""
    Write-Host "Ejemplos:" -ForegroundColor Cyan
    Write-Host "  Switch-Module 1           - Cambiar al módulo 1"
    Write-Host "  Build-DockerImage         - Construir imagen"
    Write-Host "  Start-DockerContainer     - Ejecutar contenedor"
}

function Build-DockerImage {
    param([string]$Tag = "docker-python-guide")
    Write-Host "🐳 Construyendo imagen Docker..." -ForegroundColor Blue
    docker build -t $Tag .
}

function Start-DockerContainer {
    param(
        [string]$Image = "docker-python-guide",
        [int]$Port = 8000
    )
    Write-Host "🚀 Ejecutando contenedor..." -ForegroundColor Blue
    docker run -p "${Port}:${Port}" $Image
}

function Test-Application {
    Write-Host "🧪 Ejecutando tests..." -ForegroundColor Blue
    if (Test-Path "tests") {
        python -m pytest tests/ -v
    } else {
        Write-Warning "Directorio tests/ no encontrado"
    }
}

function Format-Code {
    Write-Host "✨ Formateando código..." -ForegroundColor Blue
    if (Test-Path "src") {
        black src/
        isort src/
    } else {
        Write-Warning "Directorio src/ no encontrado"
    }
}

function Switch-Module {
    param([int]$ModuleNumber)
    
    if (-not $ModuleNumber) {
        Write-Error "Especifica el número de módulo (ej: Switch-Module 1)"
        return
    }
    
    $moduleNumber = $ModuleNumber.ToString("00")
    $branches = git branch -r | Where-Object { $_ -match "module-$moduleNumber" }
    
    if ($branches) {
        $branch = ($branches[0] -replace '.*origin/', '').Trim()
        Write-Host "🔄 Cambiando a módulo $ModuleNumber..." -ForegroundColor Blue
        git checkout $branch
    } else {
        Write-Error "Módulo $ModuleNumber no encontrado"
    }
}

function Show-ModuleStatus {
    Write-Host "📚 Módulos disponibles:" -ForegroundColor Green
    git branch -r | Where-Object { $_ -match "module-" } | ForEach-Object {
        $branch = ($_ -replace '.*origin/', '').Trim()
        $current = if ((git branch --show-current) -eq $branch) { " (actual)" } else { "" }
        Write-Host "  $branch$current" -ForegroundColor Yellow
    }
}

function Clean-Environment {
    Write-Host "🧹 Limpiando entorno..." -ForegroundColor Blue
    
    # Limpiar Docker
    docker system prune -f
    
    # Limpiar archivos Python
    Get-ChildItem -Recurse -Name "*.pyc" | Remove-Item -Force
    Get-ChildItem -Recurse -Name "__pycache__" -Directory | Remove-Item -Recurse -Force
    
    Write-Success "Entorno limpiado"
}

# Alias para compatibilidad
Set-Alias -Name "docker-guide-help" -Value Show-DockerPythonGuideHelp
Set-Alias -Name "dghelp" -Value Show-DockerPythonGuideHelp

Write-Host "🎯 PowerShell Helper cargado. Ejecuta 'Show-DockerPythonGuideHelp' para ver comandos disponibles." -ForegroundColor Green
'@
    
    $helperContent | Out-File -FilePath "scripts\PowerShellHelper.ps1" -Encoding UTF8
    Write-Success "PowerShell helper creado en scripts\PowerShellHelper.ps1"
}

function Show-CompletionMessage {
    Write-Host ""
    Write-Success "¡Configuración completada exitosamente! 🎉"
    Write-Host ""
    Write-Status "Próximos pasos:"
    Write-Host "  1. Revisa el README.md para entender la estructura de la guía"
    Write-Host "  2. Carga el helper de PowerShell: . .\scripts\PowerShellHelper.ps1"
    Write-Host "  3. Ejecuta 'Show-DockerPythonGuideHelp' para ver comandos disponibles"
    Write-Host "  4. Comienza con el Módulo 1: 'Switch-Module 1'"
    Write-Host "  5. Copia .env.template a .env y configura según necesites"
    Write-Host ""
    Write-Status "¡Happy coding! 🐍🐳"
}

# Función principal
function Main {
    Write-Host "🐍 Docker Python Guide - Setup Script (PowerShell)" -ForegroundColor Green
    Write-Host "====================================================" -ForegroundColor Green
    Write-Host ""
    
    if (-not $SkipPrerequisites) {
        Test-Prerequisites
        Write-Host ""
    }
    
    New-DirectoryStructure
    New-EnvironmentTemplate
    New-PowerShellHelper
    Set-GitHooks
    
    Show-CompletionMessage
}

# Ejecutar función principal
Main
