#!/bin/bash

# Script de pruebas para la aplicación Flask en Kubernetes
echo "🧪 Iniciando pruebas de la aplicación..."

# Verificar que los pods estén ejecutándose
echo "📊 Verificando estado de los pods..."
kubectl get pods -n python-guide

# Configurar port-forward en segundo plano
echo "🔌 Configurando port-forward..."
kubectl port-forward service/flask-service 8080:80 -n python-guide &
PORT_FORWARD_PID=$!

# Esperar a que el port-forward esté listo
echo "⏳ Esperando a que el port-forward esté listo..."
sleep 5

# Función para limpiar el port-forward al salir
cleanup() {
    echo "🧹 Limpiando port-forward..."
    kill $PORT_FORWARD_PID 2>/dev/null
}
trap cleanup EXIT

# Probar endpoint de salud
echo "🏥 Probando endpoint de salud..."
health_response=$(curl -s http://localhost:8080/health)
echo "Respuesta de salud: $health_response"

# Probar endpoint principal
echo "🏠 Probando endpoint principal..."
home_response=$(curl -s http://localhost:8080/)
echo "Respuesta principal: $home_response"

# Crear un usuario de prueba
echo "👤 Creando usuario de prueba..."
create_response=$(curl -s -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}')
echo "Usuario creado: $create_response"

# Listar usuarios
echo "📋 Listando usuarios..."
users_response=$(curl -s http://localhost:8080/users)
echo "Lista de usuarios: $users_response"

# Obtener usuario específico
echo "🔍 Obteniendo usuario específico (ID: 1)..."
user_response=$(curl -s http://localhost:8080/users/1)
echo "Usuario específico: $user_response"

echo "✅ Pruebas completadas!"
echo "🌐 La aplicación está disponible en: http://localhost:8080"
echo "💡 Presiona Ctrl+C para terminar el port-forward"

# Mantener el port-forward activo
wait $PORT_FORWARD_PID
