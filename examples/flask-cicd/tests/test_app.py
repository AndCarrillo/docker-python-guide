import pytest
import os
from app import create_app, db
from unittest.mock import patch


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Set test configuration
    test_config = {
        'TESTING': True,
        'DATABASE_URL': 'sqlite:///:memory:',
        'REDIS_URL': 'redis://localhost:6379/1'
    }

    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_check(self, client):
        """Test basic health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data

    @patch('app.db.engine.execute')
    @patch('app.redis_client.ping')
    def test_ready_check_success(self, mock_redis_ping, mock_db_execute, client):
        """Test readiness check when all services are available."""
        mock_redis_ping.return_value = True
        mock_db_execute.return_value = None

        response = client.get('/ready')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ready'
        assert data['database'] == 'connected'
        assert data['redis'] == 'connected'

    @patch('app.db.engine.execute')
    @patch('app.redis_client.ping')
    def test_ready_check_failure(self, mock_redis_ping, mock_db_execute, client):
        """Test readiness check when services are unavailable."""
        mock_redis_ping.side_effect = Exception("Redis connection failed")
        mock_db_execute.side_effect = Exception("Database connection failed")

        response = client.get('/ready')
        assert response.status_code == 503
        data = response.get_json()
        assert data['status'] == 'not ready'
        assert data['database'] == 'disconnected'
        assert data['redis'] == 'disconnected'


class TestAPIEndpoints:
    """Test API endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Flask CI/CD Demo API'
        assert data['version'] == '1.0.0'

    def test_items_get_empty(self, client):
        """Test getting items when none exist."""
        response = client.get('/api/items')
        assert response.status_code == 200
        data = response.get_json()
        assert data == []

    def test_items_post_success(self, client):
        """Test creating a new item."""
        item_data = {
            'name': 'Test Item',
            'description': 'A test item'
        }
        response = client.post('/api/items', json=item_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'Test Item'
        assert data['description'] == 'A test item'
        assert 'id' in data
        assert 'created_at' in data

    def test_items_post_invalid_data(self, client):
        """Test creating item with invalid data."""
        item_data = {
            'description': 'Missing name field'
        }
        response = client.post('/api/items', json=item_data)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_items_get_after_creation(self, client):
        """Test getting items after creating some."""
        # Create test items
        items = [
            {'name': 'Item 1', 'description': 'First item'},
            {'name': 'Item 2', 'description': 'Second item'}
        ]

        for item in items:
            client.post('/api/items', json=item)

        # Get all items
        response = client.get('/api/items')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['name'] == 'Item 1'
        assert data[1]['name'] == 'Item 2'


class TestCaching:
    """Test Redis caching functionality."""

    @patch('app.redis_client.get')
    @patch('app.redis_client.setex')
    def test_cache_miss_and_set(self, mock_setex, mock_get, client):
        """Test cache miss scenario."""
        mock_get.return_value = None  # Cache miss
        mock_setex.return_value = True

        response = client.get('/api/items')
        assert response.status_code == 200

        # Verify cache was checked and set
        mock_get.assert_called_once()
        mock_setex.assert_called_once()

    @patch('app.redis_client.get')
    def test_cache_hit(self, mock_get, client):
        """Test cache hit scenario."""
        cached_data = '[{"id": 1, "name": "Cached Item"}]'
        mock_get.return_value = cached_data.encode('utf-8')

        response = client.get('/api/items')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['name'] == 'Cached Item'


class TestErrorHandling:
    """Test error handling."""

    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Not found'

    def test_method_not_allowed(self, client):
        """Test 405 error handling."""
        response = client.delete('/api/items')
        assert response.status_code == 405
        data = response.get_json()
        assert data['error'] == 'Method not allowed'

    @patch('app.db.session.commit')
    def test_database_error_handling(self, mock_commit, client):
        """Test database error handling."""
        mock_commit.side_effect = Exception("Database error")

        item_data = {'name': 'Test Item', 'description': 'Test'}
        response = client.post('/api/items', json=item_data)
        assert response.status_code == 500
        data = response.get_json()
        assert data['error'] == 'Internal server error'
