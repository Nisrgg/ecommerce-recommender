// API Response Types
export interface Product {
  product_id: number;
  name: string;
  category: string;
  description: string;
}

export interface Interaction {
  id: number;
  user_id: number;
  product_id: number;
  event_type: string;
  timestamp: string;
}

export interface Recommendation {
  product: Product;
  explanation: string;
}

export interface RecommendationsResponse {
  source_product: Product;
  recommendations: Recommendation[];
  user_id: number;
  generated_at: string;
}

export interface UserInteractionsResponse {
  user_id: number;
  interactions: Interaction[];
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  gemini_available: boolean;
  version: string;
}

export interface StatsResponse {
  total_products: number;
  total_interactions: number;
  unique_users: number;
  unique_products: number;
  categories: string[];
}

// Error Types
export interface ApiError {
  error: string;
  detail: string;
  status_code: number;
  timestamp: string;
}

// Component Props Types
export interface RecommendationCardProps {
  recommendation: Recommendation;
  index: number;
}

export interface UserInputFormProps {
  onSubmit: (userId: number) => void;
  loading: boolean;
}

export interface NavbarProps {
  darkMode: boolean;
  onToggleDarkMode: () => void;
}

// Hook Types
export interface UseRecommendationsReturn {
  recommendations: RecommendationsResponse | null;
  loading: boolean;
  error: string | null;
  fetchRecommendations: (userId: number) => Promise<void>;
  clearError: () => void;
}

export interface UseApiReturn<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

// Theme Types
export type Theme = 'light' | 'dark';

// API Configuration
export interface ApiConfig {
  baseURL: string;
  timeout: number;
}

// Utility Types
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface PaginationParams {
  page: number;
  limit: number;
}

export interface SearchParams {
  query?: string;
  category?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

