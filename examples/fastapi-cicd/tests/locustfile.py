from locust import HttpUser, task, between


class FastAPIUser(HttpUser):
    """Locust user for performance testing FastAPI application."""

    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        """Called when a user starts."""
        # Create some test data
        self.item_ids = []
        for i in range(5):
            response = self.client.post("/api/items", json={
                "name": f"Performance Test Item {i}",
                "description": f"Description for item {i}"
            })
            if response.status_code == 201:
                self.item_ids.append(response.json()["id"])

    @task(3)
    def get_health(self):
        """Health check endpoint - most frequent."""
        self.client.get("/health")

    @task(2)
    def get_ready(self):
        """Readiness check endpoint."""
        self.client.get("/ready")

    @task(5)
    def get_root(self):
        """Root endpoint."""
        self.client.get("/")

    @task(10)
    def get_all_items(self):
        """Get all items - frequently accessed."""
        self.client.get("/api/items")

    @task(8)
    def get_items_paginated(self):
        """Get items with pagination."""
        self.client.get("/api/items?skip=0&limit=10")

    @task(5)
    def get_specific_item(self):
        """Get a specific item by ID."""
        if self.item_ids:
            item_id = self.item_ids[0]  # Always get the first item
            self.client.get(f"/api/items/{item_id}")

    @task(2)
    def create_item(self):
        """Create a new item - less frequent due to write operations."""
        import random
        item_num = random.randint(1000, 9999)
        response = self.client.post("/api/items", json={
            "name": f"Load Test Item {item_num}",
            "description": f"Created during load test - {item_num}"
        })
        if response.status_code == 201:
            self.item_ids.append(response.json()["id"])

    @task(1)
    def get_nonexistent_item(self):
        """Test 404 handling."""
        self.client.get("/api/items/999999")

    @task(1)
    def get_docs(self):
        """Access API documentation."""
        self.client.get("/docs")


class HighLoadUser(HttpUser):
    """High-load user for stress testing."""

    wait_time = between(0.1, 0.5)  # Very short wait times

    @task
    def rapid_health_checks(self):
        """Rapid health check requests."""
        self.client.get("/health")

    @task
    def rapid_item_requests(self):
        """Rapid item list requests."""
        self.client.get("/api/items")
