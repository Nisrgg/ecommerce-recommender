"""
Simple in-memory cache service for recommendations.

This module provides a basic caching mechanism for storing
recommendation results to improve performance.
"""

from typing import Dict, Any, Optional
import time
from threading import Lock

from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CacheService:
    """Simple in-memory cache service."""
    
    def __init__(self):
        """Initialize the cache service."""
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self.enabled = settings.enable_cache
        self.default_ttl = settings.cache_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        if not self.enabled:
            return None
        
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            
            # Check if expired
            if time.time() > entry['expires_at']:
                del self._cache[key]
                logger.debug(f"Cache entry expired for key: {key}")
                return None
            
            logger.debug(f"Cache hit for key: {key}")
            return entry['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (uses default if None)
        """
        if not self.enabled:
            return
        
        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl
        
        with self._lock:
            self._cache[key] = {
                'value': value,
                'expires_at': expires_at
            }
            logger.debug(f"Cached value for key: {key} (TTL: {ttl}s)")
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key was deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                logger.debug(f"Deleted cache entry for key: {key}")
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_entries = len(self._cache)
            expired_entries = sum(
                1 for entry in self._cache.values() 
                if time.time() > entry['expires_at']
            )
            
            return {
                'total_entries': total_entries,
                'expired_entries': expired_entries,
                'active_entries': total_entries - expired_entries,
                'enabled': self.enabled
            }


# Global cache instance
cache_service = CacheService()

