"""
Tests for the AI explainer service.

This module contains tests for the AI explanation generation
including both successful cases and fallback scenarios.
"""

import pytest
from unittest.mock import patch, MagicMock

from app.services.ai_explainer import AIExplainerService
from app.models import Product


class TestAIExplainerService:
    """Test cases for AI explainer service."""
    
    def test_initialization_with_api_key(self):
        """Test AI explainer initialization with valid API key."""
        with patch('app.services.ai_explainer.genai.configure') as mock_configure, \
             patch('app.services.ai_explainer.genai.GenerativeModel') as mock_model:
            
            mock_client = MagicMock()
            mock_model.return_value = mock_client
            
            with patch('app.config.settings.gemini_api_key', 'valid_api_key'):
                explainer = AIExplainerService()
                
                assert explainer.is_available() is True
                mock_configure.assert_called_once_with(api_key='valid_api_key')
                mock_model.assert_called_once_with('gemini-pro')
    
    def test_initialization_without_api_key(self):
        """Test AI explainer initialization without API key."""
        with patch('app.config.settings.gemini_api_key', None):
            explainer = AIExplainerService()
            
            assert explainer.is_available() is False
    
    def test_initialization_with_placeholder_api_key(self):
        """Test AI explainer initialization with placeholder API key."""
        with patch('app.config.settings.gemini_api_key', 'your_gemini_api_key_here'):
            explainer = AIExplainerService()
            
            assert explainer.is_available() is False
    
    @pytest.mark.asyncio
    async def test_generate_explanation_success(self):
        """Test successful AI explanation generation."""
        # Create mock products
        source_product = Product(
            product_id=1,
            name="Wireless Headphones",
            category="Electronics",
            description="High-quality wireless headphones"
        )
        
        recommended_product = Product(
            product_id=2,
            name="Bluetooth Speaker",
            category="Electronics",
            description="Portable wireless speaker"
        )
        
        # Mock AI response
        mock_response = MagicMock()
        mock_response.text = "Because you liked Wireless Headphones, you'll also enjoy Bluetooth Speaker as they're both wireless audio devices."
        
        mock_client = MagicMock()
        mock_client.generate_content.return_value = mock_response
        
        explainer = AIExplainerService()
        explainer.gemini_client = mock_client
        
        explanation = await explainer.generate_explanation(source_product, recommended_product)
        
        assert explanation == "Because you liked Wireless Headphones, you'll also enjoy Bluetooth Speaker as they're both wireless audio devices."
        mock_client.generate_content.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_explanation_fallback(self):
        """Test fallback explanation when AI is not available."""
        source_product = Product(
            product_id=1,
            name="Running Shoes",
            category="Sports",
            description="Lightweight athletic shoes"
        )
        
        recommended_product = Product(
            product_id=2,
            name="Basketball",
            category="Sports",
            description="Official size basketball"
        )
        
        explainer = AIExplainerService()
        explainer.gemini_client = None  # Simulate unavailable AI
        
        explanation = await explainer.generate_explanation(source_product, recommended_product)
        
        assert "Because you liked Running Shoes" in explanation
        assert "Basketball" in explanation
        assert "Sports category" in explanation
    
    @pytest.mark.asyncio
    async def test_generate_explanation_different_categories(self):
        """Test fallback explanation for products in different categories."""
        source_product = Product(
            product_id=1,
            name="Running Shoes",
            category="Sports",
            description="Lightweight athletic shoes"
        )
        
        recommended_product = Product(
            product_id=2,
            name="Coffee Maker",
            category="Home & Kitchen",
            description="Programmable drip coffee maker"
        )
        
        explainer = AIExplainerService()
        explainer.gemini_client = None  # Simulate unavailable AI
        
        explanation = await explainer.generate_explanation(source_product, recommended_product)
        
        assert "Because you liked Running Shoes" in explanation
        assert "Coffee Maker" in explanation
        assert "similar product features" in explanation
    
    @pytest.mark.asyncio
    async def test_generate_explanation_ai_error(self):
        """Test fallback when AI service throws an error."""
        source_product = Product(
            product_id=1,
            name="Wireless Headphones",
            category="Electronics",
            description="High-quality wireless headphones"
        )
        
        recommended_product = Product(
            product_id=2,
            name="Bluetooth Speaker",
            category="Electronics",
            description="Portable wireless speaker"
        )
        
        # Mock AI client that throws an error
        mock_client = MagicMock()
        mock_client.generate_content.side_effect = Exception("API Error")
        
        explainer = AIExplainerService()
        explainer.gemini_client = mock_client
        
        explanation = await explainer.generate_explanation(source_product, recommended_product)
        
        # Should return fallback explanation
        assert "Because you liked Wireless Headphones" in explanation
        assert "Bluetooth Speaker" in explanation
    
    @pytest.mark.asyncio
    async def test_generate_explanation_missing_prefix(self):
        """Test explanation generation when AI response doesn't start with expected prefix."""
        source_product = Product(
            product_id=1,
            name="Wireless Headphones",
            category="Electronics",
            description="High-quality wireless headphones"
        )
        
        recommended_product = Product(
            product_id=2,
            name="Bluetooth Speaker",
            category="Electronics",
            description="Portable wireless speaker"
        )
        
        # Mock AI response without proper prefix
        mock_response = MagicMock()
        mock_response.text = "This product is similar to what you liked."
        
        mock_client = MagicMock()
        mock_client.generate_content.return_value = mock_response
        
        explainer = AIExplainerService()
        explainer.gemini_client = mock_client
        
        explanation = await explainer.generate_explanation(source_product, recommended_product)
        
        # Should add proper prefix
        assert explanation.startswith("Because you liked Wireless Headphones,")
        assert "this product is similar to what you liked" in explanation.lower()
    
    def test_build_prompt(self):
        """Test prompt building for AI model."""
        source_product = Product(
            product_id=1,
            name="Running Shoes",
            category="Sports",
            description="Lightweight athletic shoes"
        )
        
        recommended_product = Product(
            product_id=2,
            name="Basketball",
            category="Sports",
            description="Official size basketball"
        )
        
        explainer = AIExplainerService()
        prompt = explainer._build_prompt(source_product, recommended_product)
        
        assert "Running Shoes" in prompt
        assert "Sports" in prompt
        assert "Basketball" in prompt
        assert "Because you liked" in prompt
        assert "friendly" in prompt.lower()
    
    def test_get_fallback_explanation_same_category(self):
        """Test fallback explanation for same category products."""
        source_product = Product(
            product_id=1,
            name="Running Shoes",
            category="Sports",
            description="Lightweight athletic shoes"
        )
        
        recommended_product = Product(
            product_id=2,
            name="Basketball",
            category="Sports",
            description="Official size basketball"
        )
        
        explainer = AIExplainerService()
        explanation = explainer._get_fallback_explanation(source_product, recommended_product)
        
        assert "Because you liked Running Shoes" in explanation
        assert "Basketball" in explanation
        assert "Sports category" in explanation
    
    def test_get_fallback_explanation_different_category(self):
        """Test fallback explanation for different category products."""
        source_product = Product(
            product_id=1,
            name="Running Shoes",
            category="Sports",
            description="Lightweight athletic shoes"
        )
        
        recommended_product = Product(
            product_id=2,
            name="Coffee Maker",
            category="Home & Kitchen",
            description="Programmable drip coffee maker"
        )
        
        explainer = AIExplainerService()
        explanation = explainer._get_fallback_explanation(source_product, recommended_product)
        
        assert "Because you liked Running Shoes" in explanation
        assert "Coffee Maker" in explanation
        assert "similar product features" in explanation

