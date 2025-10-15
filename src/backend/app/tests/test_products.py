"""
Tests for the product endpoints.

This module contains tests for all product-related API endpoints
including product retrieval, category filtering, and statistics.
"""

import pytest
from fastapi.testclient import TestClient

from app.tests import client, sample_products, sample_interactions


class TestProductEndpoints:
    """Test cases for product endpoints."""
    
    def test_get_product_success(self, client: TestClient, sample_products):
        """Test successful product retrieval."""
        response = client.get("/products/1")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["product_id"] == 1
        assert data["name"] == "Wireless Bluetooth Headphones"
        assert data["category"] == "Electronics"
        assert "active noise cancellation" in data["description"]
    
    def test_get_product_not_found(self, client: TestClient):
        """Test product retrieval for non-existent product."""
        response = client.get("/products/999")
        
        assert response.status_code == 404
        data = response.json()
        assert "Product 999 not found" in data["detail"]
    
    def test_get_all_products(self, client: TestClient, sample_products):
        """Test retrieving all products."""
        response = client.get("/products/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 5  # Based on sample_products fixture
        assert all("product_id" in product for product in data)
        assert all("name" in product for product in data)
        assert all("category" in product for product in data)
    
    def test_get_products_by_category_success(self, client: TestClient, sample_products):
        """Test retrieving products by category."""
        response = client.get("/products/category/Electronics")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 1  # Only one Electronics product in sample
        assert data[0]["category"] == "Electronics"
        assert data[0]["product_id"] == 1
    
    def test_get_products_by_category_not_found(self, client: TestClient, sample_products):
        """Test retrieving products by non-existent category."""
        response = client.get("/products/category/NonExistentCategory")
        
        assert response.status_code == 404
        data = response.json()
        assert "No products found in category: NonExistentCategory" in data["detail"]
    
    def test_get_products_by_category_case_sensitive(self, client: TestClient, sample_products):
        """Test that category filtering is case sensitive."""
        response = client.get("/products/category/electronics")  # lowercase
        
        assert response.status_code == 404
        data = response.json()
        assert "No products found in category: electronics" in data["detail"]
    
    def test_get_product_stats(self, client: TestClient, sample_products, sample_interactions):
        """Test product statistics endpoint."""
        response = client.get("/products/stats/overview")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_products"] == 5
        assert data["total_interactions"] == 5
        assert data["unique_users"] == 2
        assert data["unique_products"] == 4
        assert "Electronics" in data["categories"]
        assert "Clothing" in data["categories"]
        assert "Sports" in data["categories"]
        assert "Home & Kitchen" in data["categories"]
    
    def test_product_response_schema(self, client: TestClient, sample_products):
        """Test that product response matches expected schema."""
        response = client.get("/products/1")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields
        required_fields = ["product_id", "name", "category", "description"]
        for field in required_fields:
            assert field in data
        
        # Check data types
        assert isinstance(data["product_id"], int)
        assert isinstance(data["name"], str)
        assert isinstance(data["category"], str)
        assert isinstance(data["description"], str)
    
    def test_all_products_response_schema(self, client: TestClient, sample_products):
        """Test that all products response matches expected schema."""
        response = client.get("/products/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check first product schema
        first_product = data[0]
        required_fields = ["product_id", "name", "category", "description"]
        for field in required_fields:
            assert field in first_product
    
    def test_category_products_response_schema(self, client: TestClient, sample_products):
        """Test that category products response matches expected schema."""
        response = client.get("/products/category/Sports")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 2  # Two Sports products in sample
        
        # Check that all products are in Sports category
        for product in data:
            assert product["category"] == "Sports"
            assert "product_id" in product
            assert "name" in product
            assert "description" in product

