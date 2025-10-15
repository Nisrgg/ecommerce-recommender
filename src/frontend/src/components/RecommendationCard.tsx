// Recommendation card component

import React from 'react';
import { Star, Lightbulb, Tag } from 'lucide-react';
import { RecommendationCardProps } from '../types';
import { cn, truncateText } from '../utils';

const RecommendationCard: React.FC<RecommendationCardProps> = ({ recommendation, index }) => {
  const { product, explanation } = recommendation;

  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
      {/* Card Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg text-white font-bold text-sm">
            #{index + 1}
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <Tag className="h-4 w-4" />
            <span className="font-medium">{product.category}</span>
          </div>
        </div>
        <div className="flex items-center space-x-1 text-yellow-500">
          <Star className="h-4 w-4 fill-current" />
          <span className="text-sm font-medium">Recommended</span>
        </div>
      </div>

      {/* Product Information */}
      <div className="mb-6">
        <h3 className="text-xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition-colors">
          {product.name}
        </h3>
        <p className="text-gray-600 leading-relaxed">
          {truncateText(product.description, 120)}
        </p>
      </div>

      {/* AI Explanation */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-4 border border-blue-200">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <div className="flex items-center justify-center w-8 h-8 bg-blue-500 rounded-lg">
              <Lightbulb className="h-4 w-4 text-white" />
            </div>
          </div>
          <div className="flex-1">
            <h4 className="text-sm font-semibold text-blue-700 mb-2">
              Why we recommend this:
            </h4>
            <p className="text-sm text-gray-700 leading-relaxed italic">
              {explanation}
            </p>
          </div>
        </div>
      </div>

      {/* Product ID Footer */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Product ID: {product.product_id}</span>
          <span className="font-mono bg-gray-100 px-2 py-1 rounded">
            #{product.product_id}
          </span>
        </div>
      </div>
    </div>
  );
};

export default RecommendationCard;

