"""
Tests for the user endpoints.

This module contains tests for all user-related API endpoints
including user interactions and statistics.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.tests import client, sample_products, sample_interactions


class TestUserEndpoints:
    """Test cases for user endpoints."""
    
    def test_get_user_interactions_success(self, client: TestClient, sample_products, sample_interactions):
        """Test successful user interactions retrieval."""
        response = client.get("/users/1/interactions")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["user_id"] == 1
        assert len(data["interactions"]) == 3  # User 1 has 3 interactions
        
        # Check interaction structure
        for interaction in data["interactions"]:
            assert "id" in interaction
            assert "user_id" in interaction
            assert "product_id" in interaction
            assert "event_type" in interaction
            assert "timestamp" in interaction
            assert interaction["user_id"] == 1
    
    def test_get_user_interactions_not_found(self, client: TestClient, sample_products):
        """Test user interactions for non-existent user."""
        response = client.get("/users/999/interactions")
        
        assert response.status_code == 404
        data = response.json()
        assert "No interactions found for user 999" in data["detail"]
    
    def test_get_user_interactions_empty(self, client: TestClient, sample_products):
        """Test user interactions for user with no interactions."""
        response = client.get("/users/5/interactions")
        
        assert response.status_code == 404
        data = response.json()
        assert "No interactions found for user 5" in data["detail"]
    
    def test_get_user_recent_interaction_success(self, client: TestClient, sample_products, sample_interactions):
        """Test successful recent interaction retrieval."""
        response = client.get("/users/1/recent-interaction")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["user_id"] == 1
        assert "product_id" in data
        assert "event_type" in data
        assert "timestamp" in data
        assert "id" in data
    
    def test_get_user_recent_interaction_not_found(self, client: TestClient, sample_products):
        """Test recent interaction for non-existent user."""
        response = client.get("/users/999/recent-interaction")
        
        assert response.status_code == 404
        data = response.json()
        assert "No interactions found for user 999" in data["detail"]
    
    def test_get_user_stats_success(self, client: TestClient, sample_products, sample_interactions):
        """Test successful user statistics retrieval."""
        response = client.get("/users/1/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["user_id"] == 1
        assert data["total_interactions"] == 3
        assert data["unique_products"] == 2  # User 1 interacted with products 1 and 3
        assert "event_types" in data
        assert "first_interaction" in data
        assert "last_interaction" in data
        
        # Check event types
        assert data["event_types"]["view"] == 2
        assert data["event_types"]["purchase"] == 1
    
    def test_get_user_stats_not_found(self, client: TestClient, sample_products):
        """Test user statistics for non-existent user."""
        response = client.get("/users/999/stats")
        
        assert response.status_code == 404
        data = response.json()
        assert "No interactions found for user 999" in data["detail"]
    
    def test_user_interactions_response_schema(self, client: TestClient, sample_products, sample_interactions):
        """Test that user interactions response matches expected schema."""
        response = client.get("/users/1/interactions")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check top-level structure
        assert "user_id" in data
        assert "interactions" in data
        assert isinstance(data["interactions"], list)
        
        # Check interaction structure
        if data["interactions"]:
            interaction = data["interactions"][0]
            required_fields = ["id", "user_id", "product_id", "event_type", "timestamp"]
            for field in required_fields:
                assert field in interaction
    
    def test_recent_interaction_response_schema(self, client: TestClient, sample_products, sample_interactions):
        """Test that recent interaction response matches expected schema."""
        response = client.get("/users/1/recent-interaction")
        
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ["id", "user_id", "product_id", "event_type", "timestamp"]
        for field in required_fields:
            assert field in data
        
        # Check data types
        assert isinstance(data["id"], int)
        assert isinstance(data["user_id"], int)
        assert isinstance(data["product_id"], int)
        assert isinstance(data["event_type"], str)
        assert isinstance(data["timestamp"], str)  # ISO format string
    
    def test_user_stats_response_schema(self, client: TestClient, sample_products, sample_interactions):
        """Test that user stats response matches expected schema."""
        response = client.get("/users/1/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        required_fields = [
            "user_id", "total_interactions", "unique_products", 
            "event_types", "first_interaction", "last_interaction"
        ]
        for field in required_fields:
            assert field in data
        
        # Check data types
        assert isinstance(data["user_id"], int)
        assert isinstance(data["total_interactions"], int)
        assert isinstance(data["unique_products"], int)
        assert isinstance(data["event_types"], dict)
        assert isinstance(data["first_interaction"], str)
        assert isinstance(data["last_interaction"], str)
    
    def test_multiple_users_interactions(self, client: TestClient, sample_products, sample_interactions):
        """Test interactions for multiple users."""
        # Test user 1
        response1 = client.get("/users/1/interactions")
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["user_id"] == 1
        assert len(data1["interactions"]) == 3
        
        # Test user 2
        response2 = client.get("/users/2/interactions")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["user_id"] == 2
        assert len(data2["interactions"]) == 2
    
    def test_interaction_timestamps(self, client: TestClient, sample_products, sample_interactions):
        """Test that interaction timestamps are properly formatted."""
        response = client.get("/users/1/interactions")
        
        assert response.status_code == 200
        data = response.json()
        
        for interaction in data["interactions"]:
            timestamp = interaction["timestamp"]
            # Should be ISO format string
            assert isinstance(timestamp, str)
            # Should be parseable as datetime
            parsed_timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            assert isinstance(parsed_timestamp, datetime)

