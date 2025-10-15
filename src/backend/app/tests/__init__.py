"""
Test configuration and utilities for the E-commerce Recommender backend.

This module provides test fixtures and utilities for testing the API endpoints
and recommendation engine.
"""

import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base, get_db
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Test database URL
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session() -> Generator:
    """
    Create a fresh database session for each test.
    
    Yields:
        Database session for testing
    """
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """
    Create a test client with database dependency override.
    
    Args:
        db_session: Database session fixture
        
    Yields:
        FastAPI test client
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_products(db_session):
    """
    Create sample products for testing.
    
    Args:
        db_session: Database session fixture
        
    Returns:
        List of created product objects
    """
    from app.models import Product
    
    products = [
        Product(
            product_id=1,
            name="Wireless Bluetooth Headphones",
            category="Electronics",
            description="High-quality wireless headphones with active noise cancellation"
        ),
        Product(
            product_id=2,
            name="Organic Cotton T-Shirt",
            category="Clothing",
            description="Comfortable 100% organic cotton t-shirt"
        ),
        Product(
            product_id=3,
            name="Running Shoes",
            category="Sports",
            description="Lightweight athletic shoes with advanced cushioning"
        ),
        Product(
            product_id=4,
            name="Coffee Maker",
            category="Home & Kitchen",
            description="Programmable drip coffee maker with thermal carafe"
        ),
        Product(
            product_id=5,
            name="Yoga Mat",
            category="Sports",
            description="Non-slip premium yoga mat with carrying strap"
        )
    ]
    
    for product in products:
        db_session.add(product)
    db_session.commit()
    
    return products


@pytest.fixture(scope="function")
def sample_interactions(db_session, sample_products):
    """
    Create sample interactions for testing.
    
    Args:
        db_session: Database session fixture
        sample_products: Sample products fixture
        
    Returns:
        List of created interaction objects
    """
    from app.models import Interaction
    from datetime import datetime
    
    interactions = [
        Interaction(
            user_id=1,
            product_id=1,
            event_type="view",
            timestamp=datetime.utcnow()
        ),
        Interaction(
            user_id=1,
            product_id=1,
            event_type="purchase",
            timestamp=datetime.utcnow()
        ),
        Interaction(
            user_id=1,
            product_id=3,
            event_type="view",
            timestamp=datetime.utcnow()
        ),
        Interaction(
            user_id=2,
            product_id=2,
            event_type="view",
            timestamp=datetime.utcnow()
        ),
        Interaction(
            user_id=2,
            product_id=4,
            event_type="purchase",
            timestamp=datetime.utcnow()
        )
    ]
    
    for interaction in interactions:
        db_session.add(interaction)
    db_session.commit()
    
    return interactions


@pytest.fixture(scope="function")
def mock_gemini_api(monkeypatch):
    """
    Mock the Gemini API for testing.
    
    Args:
        monkeypatch: pytest monkeypatch fixture
    """
    class MockGeminiResponse:
        def __init__(self, text):
            self.text = text
    
    class MockGeminiClient:
        def generate_content(self, prompt):
            return MockGeminiResponse("Because you liked the source product, we recommend this similar item.")
    
    def mock_configure(api_key):
        pass
    
    def mock_generative_model(model_name):
        return MockGeminiClient()
    
    monkeypatch.setattr("google.generativeai.configure", mock_configure)
    monkeypatch.setattr("google.generativeai.GenerativeModel", mock_generative_model)

