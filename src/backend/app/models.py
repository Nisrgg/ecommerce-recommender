"""
Database models and utilities for the E-commerce Product Recommender.

This module provides SQLAlchemy models and database utilities for managing
products and user interactions in the e-commerce recommendation system.
"""

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List, Optional

from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Database configuration
engine = create_engine(settings.database_url, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Product(Base):
    """Product model representing items in the e-commerce store."""
    
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Product(id={self.product_id}, name='{self.name}', category='{self.category}')>"


class Interaction(Base):
    """Interaction model representing user interactions with products."""
    
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    event_type = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Interaction(user_id={self.user_id}, product_id={self.product_id}, event_type='{self.event_type}')>"


def init_db():
    """
    Initialize the database by creating tables and populating them with data from CSV files.
    
    This function:
    1. Creates all database tables
    2. Reads data from products.csv and interactions.csv
    3. Populates the database with the CSV data
    4. Handles duplicate data gracefully
    """
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_products = db.query(Product).count()
        existing_interactions = db.query(Interaction).count()
        
        if existing_products > 0 or existing_interactions > 0:
            logger.info(f"Database already contains {existing_products} products and {existing_interactions} interactions.")
            logger.info("Skipping data population to avoid duplicates.")
            return
        
        # Read products from CSV
        products_df = pd.read_csv("products.csv")
        logger.info(f"Loading {len(products_df)} products from products.csv...")
        
        # Insert products into database
        for _, row in products_df.iterrows():
            product = Product(
                product_id=row['product_id'],
                name=row['name'],
                category=row['category'],
                description=row['description']
            )
            db.add(product)
        
        # Commit products
        db.commit()
        logger.info(f"Successfully inserted {len(products_df)} products.")
        
        # Read interactions from CSV
        interactions_df = pd.read_csv("interactions.csv")
        logger.info(f"Loading {len(interactions_df)} interactions from interactions.csv...")
        
        # Insert interactions into database
        for _, row in interactions_df.iterrows():
            interaction = Interaction(
                user_id=row['user_id'],
                product_id=row['product_id'],
                event_type=row['event_type']
            )
            db.add(interaction)
        
        # Commit interactions
        db.commit()
        logger.info(f"Successfully inserted {len(interactions_df)} interactions.")
        
        logger.info("Database initialization completed successfully!")
        
    except FileNotFoundError as e:
        logger.error(f"Error: Could not find CSV file - {e}")
        logger.error("Please ensure products.csv and interactions.csv exist in the current directory.")
        
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        db.rollback()
        
    finally:
        db.close()


def get_db():
    """
    Dependency function to get database session.
    Used by FastAPI for dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_product_by_id(db, product_id: int) -> Optional[Product]:
    """Get a product by its ID."""
    return db.query(Product).filter(Product.product_id == product_id).first()


def get_products_by_category(db, category: str) -> List[Product]:
    """Get all products in a specific category."""
    return db.query(Product).filter(Product.category == category).all()


def get_user_interactions(db, user_id: int) -> List[Interaction]:
    """Get all interactions for a specific user."""
    return db.query(Interaction).filter(Interaction.user_id == user_id).all()


def get_product_interactions(db, product_id: int) -> List[Interaction]:
    """Get all interactions for a specific product."""
    return db.query(Interaction).filter(Interaction.product_id == product_id).all()


def get_all_products(db) -> List[Product]:
    """Get all products from the database."""
    return db.query(Product).all()


def get_all_interactions(db) -> List[Interaction]:
    """Get all interactions from the database."""
    return db.query(Interaction).all()


def get_most_recent_interaction(db, user_id: int) -> Optional[Interaction]:
    """Get the most recent interaction for a user."""
    return db.query(Interaction).filter(
        Interaction.user_id == user_id
    ).order_by(desc(Interaction.timestamp)).first()


def add_interaction(db, user_id: int, product_id: int, event_type: str) -> Interaction:
    """Add a new interaction to the database."""
    interaction = Interaction(
        user_id=user_id,
        product_id=product_id,
        event_type=event_type
    )
    db.add(interaction)
    db.commit()
    return interaction


def get_products_by_ids(db, product_ids: List[int]) -> List[Product]:
    """Get multiple products by their IDs."""
    return db.query(Product).filter(Product.product_id.in_(product_ids)).all()


def get_interaction_stats(db) -> dict:
    """Get basic statistics about interactions."""
    total_interactions = db.query(Interaction).count()
    unique_users = db.query(Interaction.user_id).distinct().count()
    unique_products = db.query(Interaction.product_id).distinct().count()
    
    return {
        "total_interactions": total_interactions,
        "unique_users": unique_users,
        "unique_products": unique_products
    }


def get_product_stats(db) -> dict:
    """Get basic statistics about products."""
    total_products = db.query(Product).count()
    categories = db.query(Product.category).distinct().all()
    category_list = [cat[0] for cat in categories]
    
    return {
        "total_products": total_products,
        "categories": category_list,
        "category_count": len(category_list)
    }


if __name__ == "__main__":
    # Run database initialization when script is executed directly
    logger.info("Initializing E-commerce Product Recommender Database...")
    init_db()
    
    # Display some statistics
    db = SessionLocal()
    try:
        product_stats = get_product_stats(db)
        interaction_stats = get_interaction_stats(db)
        
        logger.info("="*50)
        logger.info("DATABASE STATISTICS")
        logger.info("="*50)
        logger.info(f"Total Products: {product_stats['total_products']}")
        logger.info(f"Categories: {', '.join(product_stats['categories'])}")
        logger.info(f"Total Interactions: {interaction_stats['total_interactions']}")
        logger.info(f"Unique Users: {interaction_stats['unique_users']}")
        logger.info(f"Unique Products with Interactions: {interaction_stats['unique_products']}")
        logger.info("="*50)
        
    finally:
        db.close()

