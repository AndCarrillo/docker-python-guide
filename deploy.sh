#!/bin/bash

# Script de despliegue para Kubernetes
echo "🚀 Iniciando despliegue en Kubernetes..."

# 1. Crear namespace
echo "📁 Creando namespace..."
kubectl apply -f k8s/namespace.yaml

# 2. Construir imagen Docker
echo "🔨 Construyendo imagen Docker..."
docker build -t python-k8s-app:latest examples/flask-postgres/

# 3. Desplegar PostgreSQL
echo "🐘 Desplegando PostgreSQL..."
kubectl apply -f k8s/postgres-configmap.yaml
kubectl apply -f k8s/postgres-secret.yaml
kubectl apply -f k8s/postgres-pv.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml

# 4. Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a que PostgreSQL esté listo..."
kubectl wait --for=condition=ready pod -l app=postgres -n python-guide --timeout=300s

# 5. Desplegar aplicación Flask
echo "🌶️ Desplegando aplicación Flask..."
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml

# 6. Esperar a que la aplicación esté lista
echo "⏳ Esperando a que la aplicación esté lista..."
kubectl wait --for=condition=ready pod -l app=flask-app -n python-guide --timeout=300s

# 7. Mostrar estado
echo "📊 Estado del despliegue:"
kubectl get pods -n python-guide
kubectl get services -n python-guide

echo "✅ Despliegue completado!"
echo "🌐 Para acceder a la aplicación:"
echo "   kubectl port-forward service/flask-service 8080:80 -n python-guide"
echo "   Luego visita: http://localhost:8080"
