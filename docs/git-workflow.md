# 🚀 Comandos de Git para Docker Python Guide

> **💡 Nota importante**: Los comandos en esta guía están optimizados para diferentes shells. Si usas Windows PowerShell, revisa la sección [Comandos para PowerShell](#comandos-para-powershell).

## 📋 Configuración Inicial

### Bash/Zsh (Linux/Mac/Git Bash):
```bash
# Clonar el repositorio
git clone https://github.com/USERNAME/docker-python-guide.git
cd docker-python-guide

# Configurar upstream (si es fork)
git remote add upstream https://github.com/AndCarrillo/docker-python-guide.git

# Verificar remotes
git remote -v
```

### PowerShell (Windows):
```powershell
# Clonar el repositorio
git clone https://github.com/USERNAME/docker-python-guide.git
Set-Location docker-python-guide

# Configurar upstream (si es fork)
git remote add upstream https://github.com/AndCarrillo/docker-python-guide.git

# Verificar remotes
git remote -v
```

## 🌿 Trabajo con Branches de Módulos

### Listar Módulos Disponibles

```bash
# Ver todos los branches de módulos
git branch -r | grep "module-"

# Ver solo nombres de módulos
git branch -r | grep "module-" | sed 's/.*origin\///' | sort
```

### Cambiar a un Módulo Específico

```bash
# Cambiar al módulo 1
git checkout module-01-containerize

# Cambiar al módulo 2
git checkout module-02-develop

# Volver al branch principal
git checkout main
```

### Crear Branch de Trabajo desde un Módulo

```bash
# Trabajar en mejoras del módulo 1
git checkout module-01-containerize
git checkout -b feature/module-01-improvements

# Trabajar en nuevo ejemplo para módulo 2
git checkout module-02-develop
git checkout -b feature/module-02-flask-example
```

## 🔄 Sincronización

### Actualizar desde Upstream

```bash
# Actualizar main
git checkout main
git pull upstream main

# Actualizar módulo específico
git checkout module-01-containerize
git pull upstream module-01-containerize
```

### Sincronizar Fork

```bash
# Actualizar todos los branches principales
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Actualizar módulos
for module in $(git branch -r | grep "upstream/module-" | sed 's/.*upstream\///'); do
    git checkout $module 2>/dev/null || git checkout -b $module upstream/$module
    git pull upstream $module
    git push origin $module
done
```

## 📤 Contribuciones

### Crear Feature Branch

```bash
# Para mejoras generales
git checkout main
git checkout -b feature/improve-documentation

# Para módulo específico
git checkout module-01-containerize
git checkout -b feature/add-fastapi-example
```

### Commit y Push

```bash
# Agregar cambios
git add .

# Commit con mensaje descriptivo
git commit -m "feat: agregar ejemplo de FastAPI con Docker"

# Push al fork
git push origin feature/add-fastapi-example
```

### Mantener Branch Actualizado

```bash
# Rebase con upstream
git fetch upstream
git rebase upstream/module-01-containerize

# O merge si prefieres
git merge upstream/module-01-containerize
```

## 🏷️ Tags y Releases

### Crear Tags

```bash
# Tag para version completa
git tag -a v1.0.0 -m "Primera versión completa de la guía"

# Tag para módulo específico
git tag -a module-01-v1.0 -m "Módulo 1 completado"

# Push tags
git push origin --tags
```

### Listar Tags

```bash
# Ver todos los tags
git tag -l

# Ver tags de módulos específicos
git tag -l "module-*"
```

## 🔍 Navegación y Búsqueda

### Buscar en el Historial

```bash
# Buscar commits por mensaje
git log --grep="docker"

# Buscar cambios en archivos específicos
git log --follow -- README.md

# Ver cambios entre branches
git diff main..module-01-containerize
```

### Buscar Archivos

```bash
# Buscar archivos por nombre
git ls-files | grep -i dockerfile

# Buscar contenido en archivos
git grep -n "docker-compose" -- "*.md"
```

## 🛠️ Utilidades

### Aliases Útiles

```bash
# Configurar aliases útiles
git config alias.co checkout
git config alias.br branch
git config alias.ci commit
git config alias.st status
git config alias.unstage 'reset HEAD --'
git config alias.last 'log -1 HEAD'
git config alias.visual '!gitk'

# Alias específicos para este proyecto
git config alias.modules 'branch -r | grep module-'
git config alias.switch-module '!f() { git checkout module-$1-*; }; f'
```

### Scripts de Automatización

#### Cambiar a Módulo (Función Bash)

```bash
# Agregar a ~/.bashrc o ~/.zshrc
switch_module() {
    if [ -z "$1" ]; then
        echo "Uso: switch_module <numero>"
        echo "Ejemplo: switch_module 01"
        return 1
    fi

    module_branch=$(git branch -r | grep "module-$1" | head -1 | sed 's/.*origin\///')
    if [ -n "$module_branch" ]; then
        git checkout $module_branch
        echo "Cambiado a: $module_branch"
    else
        echo "Módulo $1 no encontrado"
    fi
}
```

#### PowerShell Function

```powershell
# Agregar a $PROFILE
function Switch-Module {
    param([string]$ModuleNumber)

    if (-not $ModuleNumber) {
        Write-Host "Uso: Switch-Module <numero>"
        Write-Host "Ejemplo: Switch-Module 01"
        return
    }

    $branches = git branch -r | Where-Object { $_ -match "module-$ModuleNumber" }
    if ($branches) {
        $branch = ($branches[0] -replace '.*origin/', '').Trim()
        git checkout $branch
        Write-Host "Cambiado a: $branch"
    } else {
        Write-Host "Módulo $ModuleNumber no encontrado"
    }
}
```

## 📊 Status y Información

### Ver Estado del Proyecto

```bash
# Estado actual
echo "Branch actual: $(git branch --show-current)"
echo "Último commit: $(git log -1 --oneline)"
echo "Archivos modificados: $(git status --porcelain | wc -l)"

# Módulos disponibles
echo "Módulos disponibles:"
git branch -r | grep "module-" | sed 's/.*origin\//  - /'
```

### Estadísticas

```bash
# Número de commits por módulo
for module in $(git branch -r | grep "module-" | sed 's/.*origin\///'); do
    count=$(git rev-list --count $module)
    echo "$module: $count commits"
done

# Contribuidores por módulo
git shortlog -sn --all | head -10
```

## 🚨 Solución de Problemas

### Branch no Actualizado

```bash
# Si el branch local está desactualizado
git fetch origin
git reset --hard origin/$(git branch --show-current)
```

### Conflictos de Merge

```bash
# Ver archivos con conflictos
git status

# Resolver y continuar
git add .
git commit -m "resolve merge conflicts"
```

### Limpiar Branches Locales

```bash
# Eliminar branches mergeados
git branch --merged | grep -v "\*\|main\|module-" | xargs -n 1 git branch -d

# Limpiar branches remotos eliminados
git remote prune origin
```

## 🎯 Mejores Prácticas

1. **Siempre actualizar antes de trabajar**

   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Commits pequeños y frecuentes**

   ```bash
   git add file1.py
   git commit -m "feat: add function X"
   git add file2.py
   git commit -m "docs: update README for function X"
   ```

3. **Mensajes de commit descriptivos**

   ```bash
   # ❌ Malo
   git commit -m "fix stuff"

   # ✅ Bueno
   git commit -m "fix: resolve Docker build issue with Python 3.11"
   ```

4. **Revisar cambios antes de commit**
   ```bash
   git diff --staged
   git status
   ```

---

## 💻 Comandos para PowerShell

### Comandos Básicos Adaptados

```powershell
# Listar módulos disponibles
git branch -r | Where-Object { $_ -match "module-" }

# Cambiar a un módulo específico
git checkout module-01-containerize

# Actualizar desde upstream (comandos separados)
git fetch upstream
git checkout main
git merge upstream/main
```

### Función Helper para PowerShell

Agrega esta función a tu `$PROFILE`:

```powershell
function Switch-Module {
    param([string]$ModuleNumber)
    
    if (-not $ModuleNumber) {
        Write-Host "Uso: Switch-Module <numero>"
        Write-Host "Ejemplo: Switch-Module 01"
        return
    }
    
    $branches = git branch -r | Where-Object { $_ -match "module-$ModuleNumber" }
    if ($branches) {
        $branch = ($branches[0] -replace '.*origin/', '').Trim()
        git checkout $branch
        Write-Host "Cambiado a: $branch" -ForegroundColor Green
    } else {
        Write-Host "Módulo $ModuleNumber no encontrado" -ForegroundColor Red
    }
}

function Update-FromUpstream {
    Write-Host "Actualizando desde upstream..." -ForegroundColor Blue
    git fetch upstream
    git checkout main
    git merge upstream/main
    git push origin main
    Write-Host "Actualización completada" -ForegroundColor Green
}

function Show-ModuleStatus {
    Write-Host "📚 Módulos disponibles:" -ForegroundColor Green
    git branch -r | Where-Object { $_ -match "module-" } | ForEach-Object {
        $branch = ($_ -replace '.*origin/', '').Trim()
        $current = if ((git branch --show-current) -eq $branch) { " (actual)" } else { "" }
        Write-Host "  $branch$current" -ForegroundColor Yellow
    }
}
```

### Operadores de PowerShell vs Bash

| Bash | PowerShell | Descripción |
|------|------------|-------------|
| `&&` | `;` o nueva línea | Ejecutar comandos secuencialmente |
| `\|` | `\|` | Pipe (funciona igual) |
| `grep` | `Where-Object` o `Select-String` | Filtrar texto |
| `cd` | `Set-Location` o `cd` | Cambiar directorio |
| `ls` | `Get-ChildItem` o `ls` | Listar archivos |

### Ejemplos de Conversión

```bash
# Bash
git branch -r | grep "module-" | sed 's/.*origin\///'
```

```powershell
# PowerShell
git branch -r | Where-Object { $_ -match "module-" } | ForEach-Object { $_ -replace '.*origin/', '' }
```
