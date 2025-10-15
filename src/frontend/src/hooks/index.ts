// Custom hooks for the application

import { useState, useCallback } from 'react';
import { RecommendationsResponse, ApiError } from '../types';
import apiService from '../services/api';

/**
 * Hook for managing recommendations
 */
export function useRecommendations() {
  const [recommendations, setRecommendations] = useState<RecommendationsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRecommendations = useCallback(async (userId: number) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getRecommendationsWithExplanations(userId);
      setRecommendations(data);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.detail || 'Failed to fetch recommendations');
    } finally {
      setLoading(false);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const clearRecommendations = useCallback(() => {
    setRecommendations(null);
    setError(null);
  }, []);

  return {
    recommendations,
    loading,
    error,
    fetchRecommendations,
    clearError,
    clearRecommendations,
  };
}

/**
 * Hook for managing API health status
 */
export function useApiHealth() {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [healthData, setHealthData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const checkHealth = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getHealth();
      setHealthData(data);
      setIsHealthy(data.status === 'healthy');
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.detail || 'Health check failed');
      setIsHealthy(false);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    isHealthy,
    healthData,
    loading,
    error,
    checkHealth,
  };
}

/**
 * Hook for managing theme (light/dark mode)
 */
export function useTheme() {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const savedTheme = localStorage.getItem('theme');
    return (savedTheme as 'light' | 'dark') || 'light';
  });

  const toggleTheme = useCallback(() => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update document class for Tailwind dark mode
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  // Initialize theme on mount
  useState(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  });

  return {
    theme,
    toggleTheme,
    isDark: theme === 'dark',
  };
}

/**
 * Hook for managing local storage
 */
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);

  const removeValue = useCallback(() => {
    try {
      window.localStorage.removeItem(key);
      setStoredValue(initialValue);
    } catch (error) {
      console.error(`Error removing localStorage key "${key}":`, error);
    }
  }, [key, initialValue]);

  return [storedValue, setValue, removeValue] as const;
}

/**
 * Hook for debounced input
 */
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useState(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  });

  return debouncedValue;
}

/**
 * Hook for managing loading states
 */
export function useLoadingState() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startLoading = useCallback(() => {
    setLoading(true);
    setError(null);
  }, []);

  const stopLoading = useCallback(() => {
    setLoading(false);
  }, []);

  const setErrorState = useCallback((errorMessage: string) => {
    setError(errorMessage);
    setLoading(false);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    loading,
    error,
    startLoading,
    stopLoading,
    setErrorState,
    clearError,
  };
}

