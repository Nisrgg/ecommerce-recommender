"""
Product-related API endpoints.

This module provides endpoints for retrieving product information
and managing product data.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import get_db, get_product_by_id, get_products_by_category, get_all_products
from app.schemas import ProductResponse, StatsResponse
from app.utils.logger import get_logger
from app.utils.exceptions import ProductNotFoundError

logger = get_logger(__name__)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific product by ID.
    
    Args:
        product_id: Product identifier
        db: Database session dependency
        
    Returns:
        Product information
        
    Raises:
        HTTPException: If product not found
    """
    logger.info(f"Fetching product {product_id}")
    
    product = get_product_by_id(db, product_id)
    if not product:
        logger.warning(f"Product {product_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found"
        )
    
    return ProductResponse(
        product_id=product.product_id,
        name=product.name,
        category=product.category,
        description=product.description
    )


@router.get("/", response_model=List[ProductResponse])
async def get_all_products_endpoint(db: Session = Depends(get_db)):
    """
    Get all products from the database.
    
    Args:
        db: Database session dependency
        
    Returns:
        List of all products
    """
    logger.info("Fetching all products")
    
    products = get_all_products(db)
    
    return [
        ProductResponse(
            product_id=product.product_id,
            name=product.name,
            category=product.category,
            description=product.description
        )
        for product in products
    ]


@router.get("/category/{category}", response_model=List[ProductResponse])
async def get_products_by_category_endpoint(
    category: str,
    db: Session = Depends(get_db)
):
    """
    Get all products in a specific category.
    
    Args:
        category: Product category
        db: Database session dependency
        
    Returns:
        List of products in the category
    """
    logger.info(f"Fetching products in category: {category}")
    
    products = get_products_by_category(db, category)
    
    if not products:
        logger.warning(f"No products found in category: {category}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No products found in category: {category}"
        )
    
    return [
        ProductResponse(
            product_id=product.product_id,
            name=product.name,
            category=product.category,
            description=product.description
        )
        for product in products
    ]


@router.get("/stats/overview", response_model=StatsResponse)
async def get_product_stats(db: Session = Depends(get_db)):
    """
    Get product and interaction statistics.
    
    Args:
        db: Database session dependency
        
    Returns:
        Statistics about products and interactions
    """
    logger.info("Fetching product statistics")
    
    from app.models import get_product_stats, get_interaction_stats
    
    product_stats = get_product_stats(db)
    interaction_stats = get_interaction_stats(db)
    
    return StatsResponse(
        total_products=product_stats['total_products'],
        total_interactions=interaction_stats['total_interactions'],
        unique_users=interaction_stats['unique_users'],
        unique_products=interaction_stats['unique_products'],
        categories=product_stats['categories']
    )

