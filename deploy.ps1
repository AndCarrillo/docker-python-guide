# Script de despliegue para Kubernetes (PowerShell)
Write-Host "🚀 Iniciando despliegue en Kubernetes..." -ForegroundColor Green

# 1. Crear namespace
Write-Host "📁 Creando namespace..." -ForegroundColor Yellow
kubectl apply -f k8s/namespace.yaml

# 2. Construir imagen Docker
Write-Host "🔨 Construyendo imagen Docker..." -ForegroundColor Yellow
docker build -t python-k8s-app:latest examples/flask-postgres/

# 3. Desplegar PostgreSQL
Write-Host "🐘 Desplegando PostgreSQL..." -ForegroundColor Yellow
kubectl apply -f k8s/postgres-configmap.yaml
kubectl apply -f k8s/postgres-secret.yaml
kubectl apply -f k8s/postgres-pv.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml

# 4. Esperar a que PostgreSQL esté listo
Write-Host "⏳ Esperando a que PostgreSQL esté listo..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=postgres -n python-guide --timeout=300s

# 5. Desplegar aplicación Flask
Write-Host "🌶️ Desplegando aplicación Flask..." -ForegroundColor Yellow
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml

# 6. Esperar a que la aplicación esté lista
Write-Host "⏳ Esperando a que la aplicación esté lista..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=flask-app -n python-guide --timeout=300s

# 7. Mostrar estado
Write-Host "📊 Estado del despliegue:" -ForegroundColor Yellow
kubectl get pods -n python-guide
kubectl get services -n python-guide

Write-Host "✅ Despliegue completado!" -ForegroundColor Green
Write-Host "🌐 Para acceder a la aplicación:" -ForegroundColor Cyan
Write-Host "   kubectl port-forward service/flask-service 8080:80 -n python-guide" -ForegroundColor White
Write-Host "   Luego visita: http://localhost:8080" -ForegroundColor White
