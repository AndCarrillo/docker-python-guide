# Script de pruebas para la aplicación Flask en Kubernetes (PowerShell)
Write-Host "🧪 Iniciando pruebas de la aplicación..." -ForegroundColor Green

# Verificar que los pods estén ejecutándose
Write-Host "📊 Verificando estado de los pods..." -ForegroundColor Yellow
kubectl get pods -n python-guide

# Configurar port-forward en segundo plano
Write-Host "🔌 Configurando port-forward..." -ForegroundColor Yellow
$portForwardJob = Start-Job -ScriptBlock {
    kubectl port-forward service/flask-service 8080:80 -n python-guide
}

# Esperar a que el port-forward esté listo
Write-Host "⏳ Esperando a que el port-forward esté listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    # Probar endpoint de salud
    Write-Host "🏥 Probando endpoint de salud..." -ForegroundColor Yellow
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8080/health" -Method Get
    Write-Host "Respuesta de salud: $($healthResponse | ConvertTo-Json)" -ForegroundColor White

    # Probar endpoint principal
    Write-Host "🏠 Probando endpoint principal..." -ForegroundColor Yellow
    $homeResponse = Invoke-RestMethod -Uri "http://localhost:8080/" -Method Get
    Write-Host "Respuesta principal: $($homeResponse | ConvertTo-Json)" -ForegroundColor White

    # Crear un usuario de prueba
    Write-Host "👤 Creando usuario de prueba..." -ForegroundColor Yellow
    $userData = @{
        name = "Test User"
        email = "test@example.com"
    } | ConvertTo-Json
    
    $createResponse = Invoke-RestMethod -Uri "http://localhost:8080/users" -Method Post -Body $userData -ContentType "application/json"
    Write-Host "Usuario creado: $($createResponse | ConvertTo-Json)" -ForegroundColor White

    # Listar usuarios
    Write-Host "📋 Listando usuarios..." -ForegroundColor Yellow
    $usersResponse = Invoke-RestMethod -Uri "http://localhost:8080/users" -Method Get
    Write-Host "Lista de usuarios: $($usersResponse | ConvertTo-Json)" -ForegroundColor White

    # Obtener usuario específico
    Write-Host "🔍 Obteniendo usuario específico (ID: 1)..." -ForegroundColor Yellow
    $userResponse = Invoke-RestMethod -Uri "http://localhost:8080/users/1" -Method Get
    Write-Host "Usuario específico: $($userResponse | ConvertTo-Json)" -ForegroundColor White

    Write-Host "✅ Pruebas completadas!" -ForegroundColor Green
    Write-Host "🌐 La aplicación está disponible en: http://localhost:8080" -ForegroundColor Cyan
    Write-Host "💡 Presiona Ctrl+C para terminar el port-forward" -ForegroundColor Yellow

    # Mantener el port-forward activo
    Write-Host "⏳ Port-forward activo. Presiona Enter para terminar..." -ForegroundColor Yellow
    Read-Host
}
finally {
    # Limpiar el port-forward
    Write-Host "🧹 Limpiando port-forward..." -ForegroundColor Yellow
    Stop-Job -Job $portForwardJob
    Remove-Job -Job $portForwardJob
}
