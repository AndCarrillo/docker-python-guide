#!/bin/bash

# Script de limpieza para Kubernetes
echo "🧹 Iniciando limpieza del despliegue..."

# Eliminar namespace (esto eliminará todos los recursos)
echo "🗑️ Eliminando namespace python-guide..."
kubectl delete namespace python-guide

# Verificar que se haya eliminado
echo "✅ Verificando limpieza..."
kubectl get namespaces | grep python-guide || echo "Namespace eliminado correctamente"

# Limpiar imagen Docker local (opcional)
read -p "¿Deseas eliminar la imagen Docker local python-k8s-app:latest? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🐳 Eliminando imagen Docker..."
    docker rmi python-k8s-app:latest
fi

echo "✅ Limpieza completada!"
