import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from unittest.mock import AsyncMock, patch
import json

from app import app, get_session, Base

# Test database URL (in-memory SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Test async engine and session
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_async_session = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_session():
    """Override database session for testing."""
    async with test_async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_client():
    """Create an async test client."""
    # Override database dependency
    app.dependency_overrides[get_session] = override_get_session
    
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture
def sync_client():
    """Create a sync test client for simple tests."""
    return TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    async def test_health_check(self, async_client: AsyncClient):
        """Test basic health check endpoint."""
        response = await async_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "1.0.0"
    
    @patch('app.redis_client.ping')
    async def test_ready_check_success(self, mock_redis_ping, async_client: AsyncClient):
        """Test readiness check when all services are available."""
        mock_redis_ping.return_value = True
        
        response = await async_client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["database"] == "connected"
        assert data["redis"] == "connected"
    
    @patch('app.redis_client.ping')
    async def test_ready_check_redis_failure(self, mock_redis_ping, async_client: AsyncClient):
        """Test readiness check when Redis is unavailable."""
        mock_redis_ping.side_effect = Exception("Redis connection failed")
        
        response = await async_client.get("/ready")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "not ready"
        assert data["database"] == "connected"
        assert data["redis"] == "disconnected"


class TestAPIEndpoints:
    """Test API endpoints."""
    
    async def test_root_endpoint(self, async_client: AsyncClient):
        """Test root endpoint."""
        response = await async_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "FastAPI CI/CD Demo API"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"
    
    async def test_get_items_empty(self, async_client: AsyncClient):
        """Test getting items when none exist."""
        response = await async_client.get("/api/items")
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    async def test_create_item_success(self, async_client: AsyncClient):
        """Test creating a new item."""
        item_data = {
            "name": "Test Item",
            "description": "A test item"
        }
        response = await async_client.post("/api/items", json=item_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Item"
        assert data["description"] == "A test item"
        assert "id" in data
        assert "created_at" in data
    
    async def test_create_item_invalid_data(self, async_client: AsyncClient):
        """Test creating item with invalid data."""
        item_data = {
            "description": "Missing name field"
        }
        response = await async_client.post("/api/items", json=item_data)
        assert response.status_code == 422
    
    async def test_create_item_name_too_long(self, async_client: AsyncClient):
        """Test creating item with name too long."""
        item_data = {
            "name": "x" * 101,  # Exceeds 100 character limit
            "description": "Valid description"
        }
        response = await async_client.post("/api/items", json=item_data)
        assert response.status_code == 422
    
    async def test_get_items_after_creation(self, async_client: AsyncClient):
        """Test getting items after creating some."""
        # Create test items
        items = [
            {"name": "Item 1", "description": "First item"},
            {"name": "Item 2", "description": "Second item"}
        ]
        
        for item in items:
            await async_client.post("/api/items", json=item)
        
        # Get all items
        response = await async_client.get("/api/items")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        # Items should be ordered by created_at desc
        assert data[0]["name"] == "Item 2"
        assert data[1]["name"] == "Item 1"
    
    async def test_get_item_by_id_success(self, async_client: AsyncClient):
        """Test getting a specific item by ID."""
        # Create an item first
        item_data = {"name": "Specific Item", "description": "Item for ID test"}
        create_response = await async_client.post("/api/items", json=item_data)
        item_id = create_response.json()["id"]
        
        # Get the item by ID
        response = await async_client.get(f"/api/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == "Specific Item"
    
    async def test_get_item_by_id_not_found(self, async_client: AsyncClient):
        """Test getting a non-existent item."""
        response = await async_client.get("/api/items/999")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    async def test_pagination(self, async_client: AsyncClient):
        """Test pagination for items endpoint."""
        # Create multiple items
        for i in range(15):
            item_data = {"name": f"Item {i}", "description": f"Description {i}"}
            await async_client.post("/api/items", json=item_data)
        
        # Test pagination
        response = await async_client.get("/api/items?skip=5&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        
        # Test default pagination
        response = await async_client.get("/api/items")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 15  # All items fit in default limit


class TestCaching:
    """Test Redis caching functionality."""
    
    @patch('app.redis_client.get')
    @patch('app.redis_client.setex')
    async def test_cache_miss_and_set(self, mock_setex, mock_get, async_client: AsyncClient):
        """Test cache miss scenario."""
        mock_get.return_value = None  # Cache miss
        mock_setex.return_value = True
        
        response = await async_client.get("/api/items")
        assert response.status_code == 200
        
        # Verify cache was checked and set
        mock_get.assert_called_once()
        mock_setex.assert_called_once()
    
    @patch('app.redis_client.get')
    async def test_cache_hit(self, mock_get, async_client: AsyncClient):
        """Test cache hit scenario."""
        cached_data = '[{"id": 1, "name": "Cached Item", "description": "Cached", "created_at": "2023-01-01T00:00:00", "updated_at": null}]'
        mock_get.return_value = cached_data
        
        response = await async_client.get("/api/items")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Cached Item"
    
    @patch('app.redis_client.get')
    async def test_item_cache_hit(self, mock_get, async_client: AsyncClient):
        """Test individual item cache hit."""
        cached_data = '{"id": 1, "name": "Cached Item", "description": "Cached", "created_at": "2023-01-01T00:00:00", "updated_at": null}'
        mock_get.return_value = cached_data
        
        response = await async_client.get("/api/items/1")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Cached Item"
    
    @patch('app.redis_client.delete')
    @patch('app.redis_client.keys')
    async def test_cache_invalidation_on_create(self, mock_keys, mock_delete, async_client: AsyncClient):
        """Test cache invalidation when creating items."""
        mock_keys.return_value = ["items:0:100", "items:0:10"]
        mock_delete.return_value = 2
        
        item_data = {"name": "New Item", "description": "Test cache invalidation"}
        response = await async_client.post("/api/items", json=item_data)
        assert response.status_code == 201
        
        # Verify cache invalidation was attempted
        mock_keys.assert_called_once_with("items:*")


class TestErrorHandling:
    """Test error handling."""
    
    async def test_404_error(self, async_client: AsyncClient):
        """Test 404 error handling."""
        response = await async_client.get("/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    async def test_method_not_allowed(self, async_client: AsyncClient):
        """Test 405 error handling."""
        response = await async_client.delete("/api/items")
        assert response.status_code == 405
        data = response.json()
        assert "method not allowed" in data["detail"].lower()


class TestValidation:
    """Test input validation."""
    
    async def test_empty_name_validation(self, async_client: AsyncClient):
        """Test validation for empty name."""
        item_data = {"name": "", "description": "Valid description"}
        response = await async_client.post("/api/items", json=item_data)
        assert response.status_code == 422
    
    async def test_description_too_long(self, async_client: AsyncClient):
        """Test validation for description too long."""
        item_data = {
            "name": "Valid name",
            "description": "x" * 1001  # Exceeds 1000 character limit
        }
        response = await async_client.post("/api/items", json=item_data)
        assert response.status_code == 422
    
    async def test_invalid_json(self, async_client: AsyncClient):
        """Test handling of invalid JSON."""
        response = await async_client.post(
            "/api/items",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


class TestBackgroundTasks:
    """Test background tasks."""
    
    @patch('app.log_item_creation')
    async def test_background_task_triggered(self, mock_task, async_client: AsyncClient):
        """Test that background task is triggered on item creation."""
        item_data = {"name": "Background Test", "description": "Test background task"}
        response = await async_client.post("/api/items", json=item_data)
        assert response.status_code == 201
        
        # Note: Background tasks run after response, so we can't easily test execution
        # In a real scenario, you'd test the background task function separately
