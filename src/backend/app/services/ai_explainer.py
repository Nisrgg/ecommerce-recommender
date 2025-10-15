"""
AI Explanation Service using Google Gemini API.

This module handles the generation of user-friendly explanations
for product recommendations using Google's Gemini AI.
"""

from typing import Optional
import google.generativeai as genai
from app.core.config import settings
from app.utils.logger import get_logger
from app.utils.exceptions import AIExplanationError
from app.models import Product

logger = get_logger(__name__)


class AIExplainerService:
    """Service for generating AI-powered explanations for recommendations."""
    
    def __init__(self):
        """Initialize the AI explainer service."""
        self.gemini_client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize the Gemini client."""
        if not settings.gemini_api_key or settings.gemini_api_key == "your_gemini_api_key_here":
            logger.warning("GEMINI_API_KEY not found in environment variables. AI explanations will be disabled.")
            return
        
        try:
            genai.configure(api_key=settings.gemini_api_key)
            self.gemini_client = genai.GenerativeModel(settings.gemini_model)
            logger.info("Gemini AI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.gemini_client = None
    
    def is_available(self) -> bool:
        """Check if the AI service is available."""
        return self.gemini_client is not None
    
    async def generate_explanation(
        self, 
        source_product: Product, 
        recommended_product: Product
    ) -> str:
        """
        Generate a user-friendly explanation for why a product is recommended.
        
        Args:
            source_product: The product the user was interested in
            recommended_product: The product being recommended
            
        Returns:
            A friendly explanation string
            
        Raises:
            AIExplanationError: If explanation generation fails
        """
        if not self.is_available():
            return self._get_fallback_explanation(source_product, recommended_product)
        
        try:
            prompt = self._build_prompt(source_product, recommended_product)
            response = self.gemini_client.generate_content(prompt)
            explanation = response.text.strip()
            
            # Ensure the explanation starts with "Because you liked"
            if not explanation.lower().startswith("because you liked"):
                explanation = f"Because you liked {source_product.name}, {explanation.lower()}"
            
            logger.debug(f"Generated AI explanation for {recommended_product.name}")
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating AI explanation: {e}")
            return self._get_fallback_explanation(source_product, recommended_product)
    
    def _build_prompt(self, source_product: Product, recommended_product: Product) -> str:
        """Build the prompt for the AI model."""
        return f"""You are a helpful e-commerce assistant that explains product recommendations in a friendly, conversational tone.

A user was interested in '{source_product.name}' (Category: {source_product.category}). 
We are now recommending '{recommended_product.name}' (Category: {recommended_product.category}).

In a single, friendly sentence, explain why this is a good recommendation. Start with 'Because you liked...' and make it sound natural and helpful."""

    def _get_fallback_explanation(self, source_product: Product, recommended_product: Product) -> str:
        """Get a fallback explanation when AI is not available."""
        if source_product.category == recommended_product.category:
            return f"Because you liked {source_product.name}, we think you'll also enjoy {recommended_product.name} as they're both in the {recommended_product.category} category."
        else:
            return f"Because you liked {source_product.name}, we think you'll also enjoy {recommended_product.name} based on similar product features and user preferences."


# Global instance
ai_explainer = AIExplainerService()

