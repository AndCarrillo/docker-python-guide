# Docker Python Guide - Módulo 5: Despliegue con Kubernetes

## Prerrequisitos

- Docker Desktop con Kubernetes habilitado
- kubectl configurado
- Completar módulos anteriores

## Resumen

En este módulo final, aprenderás a desplegar aplicaciones Python en Kubernetes localmente. Implementaremos PostgreSQL y una aplicación web en un clúster local.

## 1. Configuración de Kubernetes

### Habilitar Kubernetes en Docker Desktop

```bash
# Verificar que Kubernetes esté funcionando
kubectl cluster-info
kubectl get nodes
```

### Verificar el contexto

```bash
# Ver contextos disponibles
kubectl config get-contexts

# Usar el contexto de Docker Desktop
kubectl config use-context docker-desktop
```

## 2. Configuración de PostgreSQL

### Crear el namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### Desplegar PostgreSQL

```bash
kubectl apply -f k8s/postgres-configmap.yaml
kubectl apply -f k8s/postgres-secret.yaml
kubectl apply -f k8s/postgres-pv.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
```

## 3. Despliegue de la Aplicación

### Construir la imagen

```bash
docker build -t python-k8s-app:latest examples/flask-postgres/.
```

### Desplegar la aplicación

```bash
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml
```

## 4. Verificación del Despliegue

### Verificar pods

```bash
kubectl get pods -n python-guide
kubectl logs -f deployment/flask-app -n python-guide
```

### Verificar servicios

```bash
kubectl get services -n python-guide
```

### Acceder a la aplicación

```bash
# Port forward para acceso local
kubectl port-forward service/flask-service 8080:80 -n python-guide
```

Accede a http://localhost:8080

## 5. Pruebas de la Aplicación

### Probar endpoints

```bash
# Crear usuario
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'

# Listar usuarios
curl http://localhost:8080/users
```

## 6. Monitoreo y Logs

### Ver logs en tiempo real

```bash
kubectl logs -f deployment/postgres -n python-guide
kubectl logs -f deployment/flask-app -n python-guide
```

### Describir recursos

```bash
kubectl describe deployment flask-app -n python-guide
kubectl describe service flask-service -n python-guide
```

## 7. Limpieza

### Eliminar recursos

```bash
kubectl delete namespace python-guide
```

## Resumen del Módulo

✅ Configuración de Kubernetes local  
✅ Despliegue de PostgreSQL con persistencia  
✅ Despliegue de aplicación Python  
✅ Configuración de servicios y networking  
✅ Verificación y pruebas  
✅ Monitoreo y troubleshooting

## Próximos Pasos

- Explorar Helm para gestión de paquetes
- Implementar Ingress controllers
- Configurar CI/CD con ArgoCD
- Explorar servicios en la nube (EKS, GKE, AKS)
---

**📅 Última actualización:** Julio 2025
**👨‍💻 Mantenido por:** Andrea Carrillo - [GitHub](https://github.com/AndCarrillo)
