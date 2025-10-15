// API service for communicating with the backend

import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import { 
  Product, 
  RecommendationsResponse, 
  UserInteractionsResponse, 
  HealthResponse, 
  StatsResponse,
  ApiError 
} from '../types';
import { getApiBaseUrl } from '../utils';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: getApiBaseUrl(),
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
        return config;
      },
      (error) => {
        console.error('Request error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response: AxiosResponse) => {
        console.log(`Response received from ${response.config.url}:`, response.status);
        return response;
      },
      (error: AxiosError) => {
        console.error('Response error:', error.response?.data || error.message);
        return Promise.reject(this.handleError(error));
      }
    );
  }

  private handleError(error: AxiosError): ApiError {
    if (error.response) {
      // Server responded with error status
      const data = error.response.data as any;
      return {
        error: data.error || 'Server Error',
        detail: data.detail || error.message,
        status_code: error.response.status,
        timestamp: new Date().toISOString(),
      };
    } else if (error.request) {
      // Request was made but no response received
      return {
        error: 'Network Error',
        detail: 'Unable to connect to the server. Please check your connection.',
        status_code: 0,
        timestamp: new Date().toISOString(),
      };
    } else {
      // Something else happened
      return {
        error: 'Request Error',
        detail: error.message,
        status_code: 0,
        timestamp: new Date().toISOString(),
      };
    }
  }

  // Health endpoints
  async getHealth(): Promise<HealthResponse> {
    const response = await this.api.get<HealthResponse>('/health');
    return response.data;
  }

  async getDetailedHealth(): Promise<any> {
    const response = await this.api.get('/health/detailed');
    return response.data;
  }

  // Product endpoints
  async getProduct(productId: number): Promise<Product> {
    const response = await this.api.get<Product>(`/products/${productId}`);
    return response.data;
  }

  async getAllProducts(): Promise<Product[]> {
    const response = await this.api.get<Product[]>('/products');
    return response.data;
  }

  async getProductsByCategory(category: string): Promise<Product[]> {
    const response = await this.api.get<Product[]>(`/products/category/${encodeURIComponent(category)}`);
    return response.data;
  }

  async getProductStats(): Promise<StatsResponse> {
    const response = await this.api.get<StatsResponse>('/products/stats/overview');
    return response.data;
  }

  // User endpoints
  async getUserInteractions(userId: number): Promise<UserInteractionsResponse> {
    const response = await this.api.get<UserInteractionsResponse>(`/users/${userId}/interactions`);
    return response.data;
  }

  async getUserRecentInteraction(userId: number): Promise<any> {
    const response = await this.api.get(`/users/${userId}/recent-interaction`);
    return response.data;
  }

  async getUserStats(userId: number): Promise<any> {
    const response = await this.api.get(`/users/${userId}/stats`);
    return response.data;
  }

  // Recommendation endpoints
  async getRecommendationsWithExplanations(userId: number): Promise<RecommendationsResponse> {
    const response = await this.api.get<RecommendationsResponse>(`/recommendations/with-explanations/${userId}`);
    return response.data;
  }

  async getProductRecommendations(productId: number, nRecommendations: number = 3): Promise<any> {
    const response = await this.api.get(`/recommendations/product/${productId}?n_recommendations=${nRecommendations}`);
    return response.data;
  }

  async clearUserRecommendationsCache(userId: number): Promise<any> {
    const response = await this.api.delete(`/recommendations/cache/${userId}`);
    return response.data;
  }

  async clearAllRecommendationsCache(): Promise<any> {
    const response = await this.api.delete('/recommendations/cache');
    return response.data;
  }

  // Utility methods
  async testConnection(): Promise<boolean> {
    try {
      await this.getHealth();
      return true;
    } catch (error) {
      console.error('Connection test failed:', error);
      return false;
    }
  }

  // Get API base URL
  getBaseUrl(): string {
    return this.api.defaults.baseURL || '';
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;

