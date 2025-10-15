"""
Tests for the recommendation endpoints.

This module contains comprehensive tests for the recommendation API endpoints
including the main recommendation functionality and AI explanations.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.tests import client, sample_products, sample_interactions, mock_gemini_api


class TestRecommendationEndpoints:
    """Test cases for recommendation endpoints."""
    
    def test_get_recommendations_with_explanations_success(
        self, 
        client: TestClient, 
        sample_products, 
        sample_interactions,
        mock_gemini_api
    ):
        """Test successful recommendation generation with explanations."""
        response = client.get("/recommendations/with-explanations/1")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "source_product" in data
        assert "recommendations" in data
        assert "user_id" in data
        assert "generated_at" in data
        
        # Check source product
        assert data["source_product"]["product_id"] == 1
        assert data["source_product"]["name"] == "Wireless Bluetooth Headphones"
        
        # Check recommendations
        assert len(data["recommendations"]) > 0
        for rec in data["recommendations"]:
            assert "product" in rec
            assert "explanation" in rec
            assert rec["product"]["product_id"] != 1  # Should not recommend the same product
    
    def test_get_recommendations_user_not_found(self, client: TestClient, sample_products):
        """Test recommendation request for non-existent user."""
        response = client.get("/recommendations/with-explanations/999")
        
        assert response.status_code == 404
        data = response.json()
        assert "No interactions found for user 999" in data["error"]
    
    def test_get_recommendations_no_interactions(self, client: TestClient, sample_products):
        """Test recommendation request for user with no interactions."""
        response = client.get("/recommendations/with-explanations/5")
        
        assert response.status_code == 404
        data = response.json()
        assert "No interactions found for user 5" in data["error"]
    
    @patch('app.routers.recommendations.initialize_recommender')
    def test_get_recommendations_recommender_error(self, mock_init, client: TestClient, sample_products, sample_interactions):
        """Test recommendation request when recommender fails."""
        mock_init.side_effect = Exception("Recommender initialization failed")
        
        response = client.get("/recommendations/with-explanations/1")
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to initialize recommendation engine" in data["detail"]
    
    def test_get_product_recommendations_success(self, client: TestClient, sample_products):
        """Test product-specific recommendations."""
        with patch('app.routers.recommendations.initialize_recommender') as mock_init:
            mock_recommender = MagicMock()
            mock_recommender.get_recommendations.return_value = [2, 3, 4]
            mock_init.return_value = mock_recommender
            
            response = client.get("/recommendations/product/1?n_recommendations=3")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["source_product_id"] == 1
            assert data["recommendations"] == [2, 3, 4]
            assert data["count"] == 3
    
    def test_get_product_recommendations_product_not_found(self, client: TestClient):
        """Test product recommendations for non-existent product."""
        with patch('app.routers.recommendations.initialize_recommender') as mock_init:
            mock_recommender = MagicMock()
            mock_init.return_value = mock_recommender
            
            response = client.get("/recommendations/product/999")
            
            assert response.status_code == 404
            data = response.json()
            assert "Product 999 not found" in data["detail"]
    
    def test_get_product_recommendations_max_limit(self, client: TestClient, sample_products):
        """Test product recommendations with max limit exceeded."""
        with patch('app.routers.recommendations.initialize_recommender') as mock_init:
            mock_recommender = MagicMock()
            mock_recommender.get_recommendations.return_value = [2, 3, 4, 5]
            mock_init.return_value = mock_recommender
            
            response = client.get("/recommendations/product/1?n_recommendations=15")
            
            assert response.status_code == 200
            # Should limit to max_recommendations (default 10)
            mock_recommender.get_recommendations.assert_called_once_with(1, n_recommendations=10)
    
    def test_clear_user_cache(self, client: TestClient):
        """Test clearing cache for a specific user."""
        response = client.delete("/recommendations/cache/1")
        
        assert response.status_code == 200
        data = response.json()
        assert "Cache cleared for user 1" in data["message"]
    
    def test_clear_all_cache(self, client: TestClient):
        """Test clearing all recommendation cache."""
        response = client.delete("/recommendations/cache")
        
        assert response.status_code == 200
        data = response.json()
        assert "All recommendation cache cleared" in data["message"]
    
    def test_recommendations_caching(self, client: TestClient, sample_products, sample_interactions, mock_gemini_api):
        """Test that recommendations are cached properly."""
        # First request
        response1 = client.get("/recommendations/with-explanations/1")
        assert response1.status_code == 200
        
        # Second request should use cache
        response2 = client.get("/recommendations/with-explanations/1")
        assert response2.status_code == 200
        
        # Responses should be identical
        assert response1.json() == response2.json()
    
    def test_ai_explanation_fallback(self, client: TestClient, sample_products, sample_interactions):
        """Test fallback explanation when AI service is unavailable."""
        # Mock AI explainer to return fallback
        with patch('app.services.ai_explainer.ai_explainer.is_available', return_value=False):
            response = client.get("/recommendations/with-explanations/1")
            
            assert response.status_code == 200
            data = response.json()
            
            # Check that explanations are present (fallback)
            for rec in data["recommendations"]:
                assert "explanation" in rec
                assert len(rec["explanation"]) > 0
                assert "Because you liked" in rec["explanation"]

