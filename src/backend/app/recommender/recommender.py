"""
Content-based recommendation engine for E-commerce Product Recommender.

This module implements a content-based filtering algorithm that recommends products
based on their textual features (name, category, description) using TF-IDF vectorization
and cosine similarity.
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from typing import List, Optional, Tuple
from pathlib import Path

from app.core.config import settings
from app.utils.logger import get_logger
from app.utils.exceptions import RecommendationError

logger = get_logger(__name__)


class ProductRecommender:
    """
    Content-based product recommendation engine using TF-IDF and cosine similarity.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the recommender with database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path or settings.database_url.replace("sqlite:///", "")
        self.engine = create_engine(settings.database_url, echo=False)
        self.products_df = None
        self.tfidf_matrix = None
        self.cosine_sim_matrix = None
        self.tfidf_vectorizer = None
        self.model_cache_path = "recommendation_model.pkl"
        
    def load_data(self) -> pd.DataFrame:
        """
        Load product data from the SQLite database using Pandas and SQLAlchemy.
        
        Returns:
            DataFrame containing product information
            
        Raises:
            RecommendationError: If data loading fails
        """
        try:
            # Load products from database
            query = """
            SELECT product_id, name, category, description 
            FROM products 
            ORDER BY product_id
            """
            
            self.products_df = pd.read_sql_query(query, self.engine)
            logger.info(f"Loaded {len(self.products_df)} products from database")
            
            # Verify required columns exist
            required_columns = ['product_id', 'name', 'category', 'description']
            missing_columns = [col for col in required_columns if col not in self.products_df.columns]
            
            if missing_columns:
                raise RecommendationError(f"Missing required columns: {missing_columns}")
            
            # Handle any missing values
            self.products_df = self.products_df.fillna('')
            
            return self.products_df
            
        except Exception as e:
            logger.error(f"Error loading data from database: {e}")
            raise RecommendationError(f"Failed to load product data: {e}")
    
    def create_text_soup(self, row: pd.Series) -> str:
        """
        Create a text "soup" by combining name, category, and description.
        
        Args:
            row: Pandas Series containing product information
            
        Returns:
            Combined text string
        """
        # Combine name, category, and description
        text_parts = [
            str(row['name']).lower(),
            str(row['category']).lower(),
            str(row['description']).lower()
        ]
        
        # Join with spaces and clean up
        text_soup = ' '.join(text_parts)
        
        # Remove extra whitespace and clean up
        text_soup = ' '.join(text_soup.split())
        
        return text_soup
    
    def prepare_text_data(self) -> List[str]:
        """
        Prepare text data for TF-IDF vectorization by creating text soups.
        
        Returns:
            List of text soups for all products
            
        Raises:
            RecommendationError: If product data is not loaded
        """
        if self.products_df is None:
            raise RecommendationError("Product data not loaded. Call load_data() first.")
        
        text_soups = []
        
        for _, row in self.products_df.iterrows():
            text_soup = self.create_text_soup(row)
            text_soups.append(text_soup)
        
        logger.info(f"Created text soups for {len(text_soups)} products")
        return text_soups
    
    def build_tfidf_matrix(self, text_data: List[str]) -> np.ndarray:
        """
        Build TF-IDF matrix from text data using scikit-learn's TfidfVectorizer.
        
        Args:
            text_data: List of text strings (text soups)
            
        Returns:
            TF-IDF matrix
        """
        # Initialize TF-IDF vectorizer with parameters optimized for product recommendations
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,  # Limit vocabulary size for efficiency
            stop_words='english',  # Remove common English words
            ngram_range=(1, 2),  # Use unigrams and bigrams
            min_df=1,  # Minimum document frequency
            max_df=0.8,  # Maximum document frequency (remove very common words)
            lowercase=True,
            strip_accents='unicode'
        )
        
        # Fit and transform the text data
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(text_data)
        
        logger.info(f"Built TF-IDF matrix with shape: {self.tfidf_matrix.shape}")
        logger.info(f"Vocabulary size: {len(self.tfidf_vectorizer.vocabulary_)}")
        
        return self.tfidf_matrix
    
    def calculate_cosine_similarity(self) -> np.ndarray:
        """
        Calculate cosine similarity matrix between all products.
        
        Returns:
            Cosine similarity matrix
            
        Raises:
            RecommendationError: If TF-IDF matrix is not built
        """
        if self.tfidf_matrix is None:
            raise RecommendationError("TF-IDF matrix not built. Call build_tfidf_matrix() first.")
        
        # Calculate cosine similarity
        self.cosine_sim_matrix = cosine_similarity(self.tfidf_matrix)
        
        logger.info(f"Calculated cosine similarity matrix with shape: {self.cosine_sim_matrix.shape}")
        
        return self.cosine_sim_matrix
    
    def train_model(self) -> None:
        """
        Train the complete recommendation model by loading data and building similarity matrix.
        
        Raises:
            RecommendationError: If model training fails
        """
        logger.info("Starting model training...")
        
        try:
            # Load data
            self.load_data()
            
            # Prepare text data
            text_data = self.prepare_text_data()
            
            # Build TF-IDF matrix
            self.build_tfidf_matrix(text_data)
            
            # Calculate cosine similarity
            self.calculate_cosine_similarity()
            
            # Save model to cache
            self.save_model()
            
            logger.info("Model training completed successfully!")
            
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise RecommendationError(f"Model training failed: {e}")
    
    def save_model(self) -> None:
        """Save the trained model components to disk for faster loading."""
        try:
            model_data = {
                'products_df': self.products_df,
                'tfidf_matrix': self.tfidf_matrix,
                'cosine_sim_matrix': self.cosine_sim_matrix,
                'tfidf_vectorizer': self.tfidf_vectorizer
            }
            
            with open(self.model_cache_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"Model saved to {self.model_cache_path}")
            
        except Exception as e:
            logger.warning(f"Failed to save model: {e}")
    
    def load_model(self) -> bool:
        """
        Load the trained model from disk if available.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.model_cache_path):
                logger.info("No cached model found")
                return False
            
            with open(self.model_cache_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.products_df = model_data['products_df']
            self.tfidf_matrix = model_data['tfidf_matrix']
            self.cosine_sim_matrix = model_data['cosine_sim_matrix']
            self.tfidf_vectorizer = model_data['tfidf_vectorizer']
            
            logger.info("Model loaded from cache successfully")
            return True
            
        except Exception as e:
            logger.warning(f"Failed to load cached model: {e}")
            return False
    
    def get_recommendations(
        self, 
        product_id: int, 
        n_recommendations: Optional[int] = None
    ) -> List[int]:
        """
        Get product recommendations based on content similarity.
        
        Args:
            product_id: ID of the product to find recommendations for
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended product IDs (excluding the input product)
            
        Raises:
            RecommendationError: If model is not trained or product not found
        """
        if self.cosine_sim_matrix is None:
            raise RecommendationError("Model not trained. Call train_model() or load_model() first.")
        
        if self.products_df is None:
            raise RecommendationError("Product data not available.")
        
        n_recommendations = n_recommendations or settings.default_recommendations
        
        # Find the index of the product in the dataframe
        product_indices = self.products_df[self.products_df['product_id'] == product_id].index
        
        if len(product_indices) == 0:
            raise RecommendationError(f"Product with ID {product_id} not found.")
        
        product_idx = product_indices[0]
        
        # Get similarity scores for this product
        similarity_scores = self.cosine_sim_matrix[product_idx]
        
        # Get indices of most similar products (excluding the product itself)
        similar_indices = np.argsort(similarity_scores)[::-1]  # Sort in descending order
        
        # Remove the product itself from recommendations
        similar_indices = similar_indices[similar_indices != product_idx]
        
        # Get the top N recommendations
        top_indices = similar_indices[:n_recommendations]
        
        # Convert indices back to product IDs
        recommended_product_ids = self.products_df.iloc[top_indices]['product_id'].tolist()
        
        logger.info(f"Generated {len(recommended_product_ids)} recommendations for product {product_id}")
        
        return recommended_product_ids
    
    def get_recommendations_with_scores(
        self, 
        product_id: int, 
        n_recommendations: Optional[int] = None
    ) -> List[Tuple[int, float]]:
        """
        Get product recommendations with similarity scores.
        
        Args:
            product_id: ID of the product to find recommendations for
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of tuples (product_id, similarity_score)
            
        Raises:
            RecommendationError: If model is not trained or product not found
        """
        if self.cosine_sim_matrix is None:
            raise RecommendationError("Model not trained. Call train_model() or load_model() first.")
        
        n_recommendations = n_recommendations or settings.default_recommendations
        
        # Find the index of the product
        product_indices = self.products_df[self.products_df['product_id'] == product_id].index
        
        if len(product_indices) == 0:
            raise RecommendationError(f"Product with ID {product_id} not found.")
        
        product_idx = product_indices[0]
        
        # Get similarity scores
        similarity_scores = self.cosine_sim_matrix[product_idx]
        
        # Get indices of most similar products
        similar_indices = np.argsort(similarity_scores)[::-1]
        similar_indices = similar_indices[similar_indices != product_idx]
        
        # Get top N recommendations with scores
        top_indices = similar_indices[:n_recommendations]
        
        recommendations = []
        for idx in top_indices:
            product_id_rec = self.products_df.iloc[idx]['product_id']
            score = similarity_scores[idx]
            recommendations.append((product_id_rec, score))
        
        return recommendations
    
    def get_product_info(self, product_id: int) -> Optional[dict]:
        """
        Get detailed information about a product.
        
        Args:
            product_id: ID of the product
            
        Returns:
            Dictionary with product information or None if not found
        """
        if self.products_df is None:
            return None
        
        product_row = self.products_df[self.products_df['product_id'] == product_id]
        
        if len(product_row) == 0:
            return None
        
        return product_row.iloc[0].to_dict()


# Convenience functions for easy usage
def initialize_recommender(db_path: Optional[str] = None) -> ProductRecommender:
    """
    Initialize and train a ProductRecommender instance.
    
    Args:
        db_path: Path to the SQLite database
        
    Returns:
        Trained ProductRecommender instance
        
    Raises:
        RecommendationError: If initialization fails
    """
    recommender = ProductRecommender(db_path)
    
    # Try to load from cache first
    if not recommender.load_model():
        # If no cache, train the model
        recommender.train_model()
    
    return recommender


def get_recommendations(
    product_id: int, 
    db_path: Optional[str] = None, 
    n_recommendations: Optional[int] = None
) -> List[int]:
    """
    Convenience function to get product recommendations.
    
    Args:
        product_id: ID of the product to find recommendations for
        db_path: Path to the SQLite database
        n_recommendations: Number of recommendations to return
        
    Returns:
        List of recommended product IDs
        
    Raises:
        RecommendationError: If recommendation generation fails
    """
    recommender = initialize_recommender(db_path)
    return recommender.get_recommendations(product_id, n_recommendations)

