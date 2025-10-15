"""
User-related API endpoints.

This module provides endpoints for retrieving user interaction data
and managing user-related information.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import get_db, get_user_interactions, get_most_recent_interaction
from app.schemas import UserInteractionsResponse, InteractionResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/interactions", response_model=UserInteractionsResponse)
async def get_user_interactions_endpoint(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all interactions for a specific user.
    
    Args:
        user_id: User identifier
        db: Database session dependency
        
    Returns:
        User interactions data
        
    Raises:
        HTTPException: If no interactions found
    """
    logger.info(f"Fetching interactions for user {user_id}")
    
    interactions = get_user_interactions(db, user_id)
    
    if not interactions:
        logger.warning(f"No interactions found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No interactions found for user {user_id}"
        )
    
    return UserInteractionsResponse(
        user_id=user_id,
        interactions=[
            InteractionResponse(
                id=interaction.id,
                user_id=interaction.user_id,
                product_id=interaction.product_id,
                event_type=interaction.event_type,
                timestamp=interaction.timestamp
            )
            for interaction in interactions
        ]
    )


@router.get("/{user_id}/recent-interaction")
async def get_user_recent_interaction(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the most recent interaction for a user.
    
    Args:
        user_id: User identifier
        db: Database session dependency
        
    Returns:
        Most recent interaction or None
        
    Raises:
        HTTPException: If no interactions found
    """
    logger.info(f"Fetching most recent interaction for user {user_id}")
    
    interaction = get_most_recent_interaction(db, user_id)
    
    if not interaction:
        logger.warning(f"No interactions found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No interactions found for user {user_id}"
        )
    
    return InteractionResponse(
        id=interaction.id,
        user_id=interaction.user_id,
        product_id=interaction.product_id,
        event_type=interaction.event_type,
        timestamp=interaction.timestamp
    )


@router.get("/{user_id}/stats")
async def get_user_stats(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get statistics for a specific user.
    
    Args:
        user_id: User identifier
        db: Database session dependency
        
    Returns:
        User interaction statistics
    """
    logger.info(f"Fetching stats for user {user_id}")
    
    interactions = get_user_interactions(db, user_id)
    
    if not interactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No interactions found for user {user_id}"
        )
    
    # Calculate statistics
    total_interactions = len(interactions)
    unique_products = len(set(interaction.product_id for interaction in interactions))
    event_types = {}
    
    for interaction in interactions:
        event_type = interaction.event_type
        event_types[event_type] = event_types.get(event_type, 0) + 1
    
    return {
        "user_id": user_id,
        "total_interactions": total_interactions,
        "unique_products": unique_products,
        "event_types": event_types,
        "first_interaction": min(interaction.timestamp for interaction in interactions),
        "last_interaction": max(interaction.timestamp for interaction in interactions)
    }

