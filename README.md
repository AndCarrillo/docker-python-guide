# 🐍 Python Docker Guide - Guía Completa

Una guía completa para containerizar aplicaciones Python usando Docker, desde conceptos básicos hasta deployment en producción.

## 📋 Tabla de Contenidos

### 🎯 Módulos de la Guía

| Módulo                                                                 | Descripción                                   | Branch                     | Estado |
| ---------------------------------------------------------------------- | --------------------------------------------- | -------------------------- | ------ |
| [**1. Containerize your app**](#módulo-1-containerize-your-app)        | Aprende a containerizar una aplicación Python | `module-01-containerize`   | 🚧     |
| [**2. Develop your app**](#módulo-2-develop-your-app)                  | Desarrollo local usando contenedores          | `module-02-develop`        | 🚧     |
| [**3. Linting and typing**](#módulo-3-linting-and-typing)              | Configuración de linting, formato y tipado    | `module-03-linting-typing` | 🚧     |
| [**4. CI/CD with GitHub Actions**](#módulo-4-cicd-with-github-actions) | Automatización con GitHub Actions             | `module-04-cicd`           | 🚧     |
| [**5. Test your deployment**](#módulo-5-test-your-deployment)          | Testing y deployment en Kubernetes            | `module-05-deployment`     | 🚧     |

---

## 🎯 Objetivos de Aprendizaje

Al completar esta guía, serás capaz de:

- ✅ Containerizar aplicaciones Python de manera eficiente
- ✅ Configurar un entorno de desarrollo local con contenedores
- ✅ Implementar mejores prácticas de código (linting, formatting, typing)
- ✅ Configurar pipelines de CI/CD automatizados
- ✅ Desplegar aplicaciones en Kubernetes para testing

---

## 📚 Módulos Detallados

### Módulo 1: Containerize your app

**Branch:** `module-01-containerize`

Aprende los fundamentos de containerización con Docker:

- Creación de Dockerfile optimizado para Python
- Multi-stage builds para reducir tamaño de imagen
- Configuración de dependencias y requirements
- Mejores prácticas de seguridad

**🔗 [Ir al módulo →](../../tree/module-01-containerize)**

---

### Módulo 2: Develop your app

**Branch:** `module-02-develop`

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
