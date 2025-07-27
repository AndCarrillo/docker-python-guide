# Script de limpieza para Kubernetes (PowerShell)
Write-Host "🧹 Iniciando limpieza del despliegue..." -ForegroundColor Yellow

# Eliminar namespace (esto eliminará todos los recursos)
Write-Host "🗑️ Eliminando namespace python-guide..." -ForegroundColor Red
kubectl delete namespace python-guide

# Verificar que se haya eliminado
Write-Host "✅ Verificando limpieza..." -ForegroundColor Yellow
$namespaceCheck = kubectl get namespaces | Select-String "python-guide"
if (-not $namespaceCheck) {
    Write-Host "Namespace eliminado correctamente" -ForegroundColor Green
}

# Limpiar imagen Docker local (opcional)
$response = Read-Host "¿Deseas eliminar la imagen Docker local python-k8s-app:latest? (y/N)"
if ($response -eq "y" -or $response -eq "Y") {
    Write-Host "🐳 Eliminando imagen Docker..." -ForegroundColor Yellow
    docker rmi python-k8s-app:latest
}

Write-Host "✅ Limpieza completada!" -ForegroundColor Green
