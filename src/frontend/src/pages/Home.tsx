// Home page component

import React from 'react';
import { Clock, Sparkles, TrendingUp } from 'lucide-react';
import UserInputForm from '../components/UserInputForm';
import RecommendationCard from '../components/RecommendationCard';
import { useRecommendations } from '../hooks';
import { cn, formatDate } from '../utils';

const Home: React.FC = () => {
  const { recommendations, loading, error, fetchRecommendations, clearRecommendations } = useRecommendations();

  const handleGetRecommendations = async (userId: number) => {
    await fetchRecommendations(userId);
  };

  const handleClearResults = () => {
    clearRecommendations();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        {/* Main Content */}
        <div className="max-w-6xl mx-auto">
          {/* Input Section */}
          <div className="mb-12">
            <UserInputForm onSubmit={handleGetRecommendations} loading={loading} />
          </div>

          {/* Loading State */}
          {loading && (
            <div className="flex justify-center items-center py-16">
              <div className="glass-card rounded-2xl p-8 text-center">
                <div className="loading-spinner w-12 h-12 mx-auto mb-4"></div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  Analyzing User Preferences
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Finding the best product recommendations for you...
                </p>
                <div className="flex justify-center space-x-1 mt-4">
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="flex justify-center items-center py-16">
              <div className="glass-card rounded-2xl p-8 text-center max-w-md">
                <div className="flex justify-center mb-4">
                  <div className="flex items-center justify-center w-16 h-16 bg-red-100 dark:bg-red-900/20 rounded-2xl">
                    <span className="text-2xl">⚠️</span>
                  </div>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  Oops! Something went wrong
                </h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  {error}
                </p>
                <button
                  onClick={handleClearResults}
                  className="btn-secondary w-full"
                >
                  Try Again
                </button>
              </div>
            </div>
          )}

          {/* Results Section */}
          {recommendations && (
            <div className="space-y-8">
              {/* Results Header */}
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-2xl">
                    <Sparkles className="h-8 w-8 text-white" />
                  </div>
                </div>
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                  Your Personalized Recommendations
                </h2>
                <p className="text-gray-600 dark:text-gray-300">
                  Based on user {recommendations.user_id}'s preferences
                </p>
              </div>

              {/* Source Product */}
              <div className="glass-card rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2 text-primary-500" />
                  Based on Interest In:
                </h3>
                <div className="bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl p-6 text-white">
                  <div className="flex items-start justify-between mb-3">
                    <h4 className="text-xl font-bold">{recommendations.source_product.name}</h4>
                    <span className="bg-white/20 px-3 py-1 rounded-full text-sm font-medium">
                      {recommendations.source_product.category}
                    </span>
                  </div>
                  <p className="text-white/90 leading-relaxed">
                    {recommendations.source_product.description}
                  </p>
                </div>
              </div>

              {/* Recommendations Grid */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6 flex items-center">
                  <Sparkles className="h-5 w-5 mr-2 text-secondary-500" />
                  Recommended Products:
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recommendations.recommendations.map((recommendation, index) => (
                    <RecommendationCard
                      key={recommendation.product.product_id}
                      recommendation={recommendation}
                      index={index}
                    />
                  ))}
                </div>
              </div>

              {/* Metadata */}
              <div className="glass-card rounded-xl p-4 text-center">
                <div className="flex items-center justify-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
                  <Clock className="h-4 w-4" />
                  <span>Generated at {formatDate(recommendations.generated_at)}</span>
                </div>
              </div>

              {/* Clear Button */}
              <div className="text-center">
                <button
                  onClick={handleClearResults}
                  className="btn-secondary"
                >
                  Get New Recommendations
                </button>
              </div>
            </div>
          )}

          {/* Welcome State */}
          {!loading && !error && !recommendations && (
            <div className="flex justify-center items-center py-16">
              <div className="glass-card rounded-2xl p-8 text-center max-w-2xl">
                <div className="flex justify-center mb-6">
                  <div className="flex items-center justify-center w-20 h-20 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-3xl">
                    <span className="text-3xl">👋</span>
                  </div>
                </div>
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                  Welcome to the Product Recommender!
                </h2>
                <p className="text-gray-600 dark:text-gray-300 mb-8 text-lg leading-relaxed">
                  Discover personalized product recommendations powered by AI. 
                  Simply enter a user ID above to get started and see how our intelligent 
                  system finds products you'll love.
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="flex justify-center mb-3">
                      <div className="flex items-center justify-center w-12 h-12 bg-primary-100 dark:bg-primary-900/20 rounded-xl">
                        <span className="text-xl">🎯</span>
                      </div>
                    </div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Personalized</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Recommendations based on user behavior and preferences
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <div className="flex justify-center mb-3">
                      <div className="flex items-center justify-center w-12 h-12 bg-secondary-100 dark:bg-secondary-900/20 rounded-xl">
                        <span className="text-xl">🤖</span>
                      </div>
                    </div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">AI-Powered</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Smart explanations for each recommendation using advanced AI
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <div className="flex justify-center mb-3">
                      <div className="flex items-center justify-center w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-xl">
                        <span className="text-xl">⚡</span>
                      </div>
                    </div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Fast</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Get results in seconds with our optimized recommendation engine
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;

