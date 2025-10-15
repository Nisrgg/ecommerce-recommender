"""
Recommendation-related API endpoints.

This module provides the main recommendation endpoints including
the core recommendation functionality with AI explanations.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import get_db, get_product_by_id, get_most_recent_interaction
from app.schemas import RecommendationsResponse, RecommendationResponse, ProductResponse
from app.recommender.recommender import initialize_recommender
from app.services.ai_explainer import ai_explainer
from app.services.cache import cache_service
from app.core.config import settings
from app.utils.logger import get_logger
from app.utils.exceptions import UserNotFoundError, ProductNotFoundError, RecommendationError

logger = get_logger(__name__)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_recommender():
    """
    Dependency to get the initialized recommender.
    Lazy initialization on first use.
    """
    try:
        return initialize_recommender()
    except Exception as e:
        logger.error(f"Failed to initialize recommender: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize recommendation engine"
        )


@router.get(
    "/with-explanations/{user_id}",
    response_model=RecommendationsResponse,
    responses={
        404: {"description": "User not found or no interactions"},
        500: {"description": "Internal server error"}
    }
)
async def get_recommendations_with_explanations(
    user_id: int,
    db: Session = Depends(get_db),
    recommender_instance = Depends(get_recommender)
):
    """
    Get product recommendations with AI-generated explanations for a user.
    
    This endpoint:
    1. Finds the user's most recent product interaction
    2. Gets content-based recommendations for that product
    3. Generates AI explanations for each recommendation
    4. Returns the complete recommendation package
    
    Args:
        user_id: ID of the user to get recommendations for
        db: Database session dependency
        recommender_instance: Recommender instance dependency
        
    Returns:
        Recommendations with explanations
        
    Raises:
        HTTPException: If user not found or recommendation generation fails
    """
    logger.info(f"Getting recommendations for user {user_id}")
    
    # Check cache first
    cache_key = f"recommendations_user_{user_id}"
    cached_result = cache_service.get(cache_key)
    if cached_result:
        logger.info(f"Returning cached recommendations for user {user_id}")
        return cached_result
    
    try:
        # Get the user's most recent interaction
        recent_interaction = get_most_recent_interaction(db, user_id)
        
        if not recent_interaction:
            logger.warning(f"No interactions found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No interactions found for user {user_id}"
            )
        
        # Get the source product
        source_product = get_product_by_id(db, recent_interaction.product_id)
        if not source_product:
            logger.error(f"Product {recent_interaction.product_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {recent_interaction.product_id} not found"
            )
        
        logger.info(f"Getting recommendations based on product {source_product.product_id}")
        
        # Get recommendations from the recommender
        recommended_product_ids = recommender_instance.get_recommendations(
            source_product.product_id, 
            n_recommendations=settings.default_recommendations
        )
        
        if not recommended_product_ids:
            logger.warning(f"No recommendations found for product {source_product.product_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No recommendations found for product {source_product.product_id}"
            )
        
        # Get recommended products from database
        recommended_products = []
        for product_id in recommended_product_ids:
            product = get_product_by_id(db, product_id)
            if product:
                recommended_products.append(product)
        
        if not recommended_products:
            logger.error("No recommended products found in database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No recommended products found in database"
            )
        
        # Generate explanations for each recommendation
        recommendations_with_explanations = []
        
        for recommended_product in recommended_products:
            explanation = await ai_explainer.generate_explanation(source_product, recommended_product)
            
            recommendation = RecommendationResponse(
                product=ProductResponse(
                    product_id=recommended_product.product_id,
                    name=recommended_product.name,
                    category=recommended_product.category,
                    description=recommended_product.description
                ),
                explanation=explanation
            )
            recommendations_with_explanations.append(recommendation)
        
        # Create the response
        response = RecommendationsResponse(
            source_product=ProductResponse(
                product_id=source_product.product_id,
                name=source_product.name,
                category=source_product.category,
                description=source_product.description
            ),
            recommendations=recommendations_with_explanations,
            user_id=user_id,
            generated_at=datetime.utcnow()
        )
        
        # Cache the result
        cache_service.set(cache_key, response, ttl=settings.cache_ttl)
        
        logger.info(f"Successfully generated {len(recommendations_with_explanations)} recommendations for user {user_id}")
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error generating recommendations for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/product/{product_id}")
async def get_product_recommendations(
    product_id: int,
    n_recommendations: int = 3,
    db: Session = Depends(get_db),
    recommender_instance = Depends(get_recommender)
):
    """
    Get recommendations for a specific product.
    
    Args:
        product_id: Product identifier
        n_recommendations: Number of recommendations to return
        db: Database session dependency
        recommender_instance: Recommender instance dependency
        
    Returns:
        List of recommended product IDs
        
    Raises:
        HTTPException: If product not found or recommendation generation fails
    """
    logger.info(f"Getting recommendations for product {product_id}")
    
    # Validate n_recommendations
    if n_recommendations > settings.max_recommendations:
        n_recommendations = settings.max_recommendations
    
    try:
        # Check if product exists
        product = get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {product_id} not found"
            )
        
        # Get recommendations
        recommended_ids = recommender_instance.get_recommendations(
            product_id, 
            n_recommendations=n_recommendations
        )
        
        return {
            "source_product_id": product_id,
            "recommendations": recommended_ids,
            "count": len(recommended_ids)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting recommendations for product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {str(e)}"
        )


@router.delete("/cache/{user_id}")
async def clear_user_recommendations_cache(user_id: int):
    """
    Clear cached recommendations for a specific user.
    
    Args:
        user_id: User identifier
        
    Returns:
        Success message
    """
    cache_key = f"recommendations_user_{user_id}"
    deleted = cache_service.delete(cache_key)
    
    if deleted:
        logger.info(f"Cleared cache for user {user_id}")
        return {"message": f"Cache cleared for user {user_id}"}
    else:
        return {"message": f"No cache found for user {user_id}"}


@router.delete("/cache")
async def clear_all_recommendations_cache():
    """
    Clear all cached recommendations.
    
    Returns:
        Success message
    """
    cache_service.clear()
    logger.info("Cleared all recommendation cache")
    return {"message": "All recommendation cache cleared"}

