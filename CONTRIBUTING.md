# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a la **Docker Python Guide**! Esta guía te ayudará a entender cómo puedes contribuir efectivamente a este proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Reporte de Issues](#reporte-de-issues)
- [Pull Requests](#pull-requests)

## 📜 Código de Conducta

Este proyecto adhiere a un código de conducta que esperamos que todos los participantes respeten. Por favor, lee el [Código de Conducta](CODE_OF_CONDUCT.md) antes de participar.

## 🎯 Cómo Contribuir

Hay varias formas de contribuir a este proyecto:

### 📝 Documentación

- Mejorar README files de módulos
- Corregir errores tipográficos
- Agregar ejemplos adicionales
- Traducir contenido
- Mejorar instrucciones de setup

### 💻 Código

- Crear nuevos ejemplos prácticos
- Mejorar ejercicios existentes
- Agregar scripts de automatización
- Optimizar Dockerfiles
- Agregar tests

### 🐛 Reporte de Bugs

- Encontrar y reportar errores
- Validar fixes
- Probar en diferentes plataformas

### 💡 Ideas y Sugerencias

- Proponer nuevos módulos
- Sugerir mejoras en el contenido
- Compartir mejores prácticas

## 🏗️ Estructura del Proyecto

```
docker-python-guide/
├── README.md              # Documentación principal (menú)
├── docs/                  # Documentación general
├── scripts/               # Scripts de automatización
│   ├── setup.sh          # Setup para Linux/Mac
│   └── setup.ps1         # Setup para Windows
├── module-01-containerize/    # Branch separado
├── module-02-develop/         # Branch separado
├── module-03-linting-typing/  # Branch separado
├── module-04-cicd/           # Branch separado
└── module-05-deployment/     # Branch separado
```

### Branches por Módulo

Cada módulo tiene su propio branch con la siguiente estructura:

```
module-XX-name/
├── README.md              # Documentación del módulo
├── docs/                  # Documentación específica
├── examples/              # Ejemplos prácticos
├── exercises/             # Ejercicios para estudiantes
├── src/                   # Código fuente
└── tests/                # Tests del módulo
```

## 🔄 Proceso de Desarrollo

### 1. Fork y Clone

```bash
# Fork el proyecto en GitHub
git clone https://github.com/TU-USERNAME/docker-python-guide.git
cd docker-python-guide
```

### 2. Configurar Upstream

```bash
git remote add upstream https://github.com/AndCarrillo/docker-python-guide.git
```

### 3. Crear Branch de Trabajo

```bash
# Para contribuciones generales
git checkout -b feature/tu-feature-name

# Para módulos específicos
git checkout module-01-containerize
git checkout -b feature/module-01-improvement
```

### 4. Hacer Cambios

- Sigue las convenciones de código
- Agrega tests si es aplicable
- Actualiza documentación
- Prueba tus cambios

### 5. Commit y Push

```bash
git add .
git commit -m "feat: descripción clara del cambio"
git push origin feature/tu-feature-name
```

### 6. Crear Pull Request

- Describe claramente los cambios
- Referencia issues relacionados
- Incluye capturas de pantalla si es visual

## 📏 Estándares de Código

### Python

- **Estilo**: Seguir PEP 8
- **Formatting**: Usar Black
- **Imports**: Usar isort
- **Type hints**: Usar cuando sea posible
- **Docstrings**: Estilo Google

Ejemplo:

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

- **Multi-stage builds**: Cuando sea apropiado
- **Orden de comandos**: Optimizar para cache
- **Security**: No usar root user
- **Size**: Minimizar tamaño de imagen

Ejemplo de Dockerfile:

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

### Documentación

- **Markdown**: Usar sintaxis estándar
- **Estructura**: Headers consistentes
- **Ejemplos**: Incluir código ejecutable
- **Enlaces**: Verificar que funcionen

### Mensajes de Commit

Usar formato Conventional Commits:

```
feat: agregar ejemplo de FastAPI con PostgreSQL
fix: corregir Dockerfile para Python 3.11
docs: actualizar README del módulo 2
test: agregar tests para ejercicio de Docker Compose
chore: actualizar dependencias
```

Tipos válidos:

- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento
- `refactor`: Refactoring de código
- `style`: Cambios de formato

## 🐛 Reporte de Issues

### Antes de Reportar

1. Busca issues existentes
2. Verifica que no sea un problema local
3. Prueba con la última versión

### Template de Issue

```markdown
## 🐛 Descripción del Bug

Descripción clara y concisa del problema.

## 🔄 Pasos para Reproducir

1. Ve a '...'
2. Ejecuta '...'
3. Observa el error

## ✅ Comportamiento Esperado

Descripción de qué debería pasar.

## 📱 Entorno

- OS: [ej. Windows 11]
- Docker version: [ej. 24.0.0]
- Python version: [ej. 3.11]
- Branch/Módulo: [ej. module-01-containerize]

## 📎 Información Adicional

Logs, capturas de pantalla, etc.
```

## 🔀 Pull Requests

### Checklist antes de Enviar

- [ ] Código sigue los estándares establecidos
- [ ] Tests pasan (si aplica)
- [ ] Documentación actualizada
- [ ] Commits siguen convención
- [ ] Branch actualizado con upstream
- [ ] PR template completado

### Template de PR

```markdown
## 📝 Descripción

Descripción clara de los cambios realizados.

## 🎯 Tipo de Cambio

- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Cambio breaking
- [ ] Documentación

## 🧪 Testing

- [ ] Tests existentes pasan
- [ ] Nuevos tests agregados
- [ ] Probado manualmente

## 📋 Checklist

- [ ] Código sigue estándares del proyecto
- [ ] Self-review completado
- [ ] Documentación actualizada
- [ ] Commits siguen convención

## 🔗 Issues Relacionados

Closes #123
```

## 🏷️ Labels

Usamos los siguientes labels:

- `bug`: Algo no funciona
- `enhancement`: Nueva funcionalidad
- `documentation`: Mejoras en documentación
- `good first issue`: Bueno para principiantes
- `help wanted`: Ayuda extra bienvenida
- `module-01`: Relacionado con módulo 1
- `module-02`: Relacionado con módulo 2
- etc.

## 🎉 Reconocimiento

Todos los contribuidores serán reconocidos en:

- README principal
- Lista de contribuidores
- Release notes

## ❓ ¿Necesitas Ayuda?

- Abre un issue con label `question`
- Discute en GitHub Discussions
- Revisa la documentación existente

¡Gracias por contribuir a la Docker Python Guide! 🚀
