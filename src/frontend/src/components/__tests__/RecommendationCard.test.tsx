// Tests for RecommendationCard component

import React from 'react';
import { render, screen } from '@testing-library/react';
import RecommendationCard from '../RecommendationCard';
import { Recommendation } from '../../types';

const mockRecommendation: Recommendation = {
  product: {
    product_id: 1,
    name: 'Wireless Bluetooth Headphones',
    category: 'Electronics',
    description: 'High-quality wireless headphones with active noise cancellation, 30-hour battery life, and premium sound quality'
  },
  explanation: 'Because you liked Running Shoes, we think you\'ll also enjoy Wireless Bluetooth Headphones as they\'re both premium quality products for active lifestyles.'
};

describe('RecommendationCard', () => {
  it('renders correctly', () => {
    render(<RecommendationCard recommendation={mockRecommendation} index={0} />);
    
    expect(screen.getByText('Wireless Bluetooth Headphones')).toBeInTheDocument();
    expect(screen.getByText('Electronics')).toBeInTheDocument();
    expect(screen.getByText(/High-quality wireless headphones/)).toBeInTheDocument();
    expect(screen.getByText(/Because you liked Running Shoes/)).toBeInTheDocument();
  });

  it('displays correct recommendation number', () => {
    render(<RecommendationCard recommendation={mockRecommendation} index={2} />);
    
    expect(screen.getByText('#3')).toBeInTheDocument();
  });

  it('shows product category', () => {
    render(<RecommendationCard recommendation={mockRecommendation} index={0} />);
    
    expect(screen.getByText('Electronics')).toBeInTheDocument();
  });

  it('displays AI explanation', () => {
    render(<RecommendationCard recommendation={mockRecommendation} index={0} />);
    
    expect(screen.getByText('Why we recommend this:')).toBeInTheDocument();
    expect(screen.getByText(/Because you liked Running Shoes/)).toBeInTheDocument();
  });

  it('shows product ID', () => {
    render(<RecommendationCard recommendation={mockRecommendation} index={0} />);
    
    expect(screen.getByText('Product ID: 1')).toBeInTheDocument();
    expect(screen.getByText('#1')).toBeInTheDocument();
  });

  it('truncates long descriptions', () => {
    const longDescription = 'A'.repeat(200);
    const recommendationWithLongDesc: Recommendation = {
      ...mockRecommendation,
      product: {
        ...mockRecommendation.product,
        description: longDescription
      }
    };
    
    render(<RecommendationCard recommendation={recommendationWithLongDesc} index={0} />);
    
    const descriptionElement = screen.getByText(/A{120}/);
    expect(descriptionElement).toBeInTheDocument();
    expect(descriptionElement.textContent).toContain('...');
  });

  it('has proper accessibility attributes', () => {
    render(<RecommendationCard recommendation={mockRecommendation} index={0} />);
    
    // Check for proper heading structure
    const productName = screen.getByRole('heading', { level: 3 });
    expect(productName).toBeInTheDocument();
    expect(productName).toHaveTextContent('Wireless Bluetooth Headphones');
  });

  it('renders with different index values', () => {
    const { rerender } = render(<RecommendationCard recommendation={mockRecommendation} index={0} />);
    expect(screen.getByText('#1')).toBeInTheDocument();
    
    rerender(<RecommendationCard recommendation={mockRecommendation} index={4} />);
    expect(screen.getByText('#5')).toBeInTheDocument();
  });

  it('handles different product categories', () => {
    const sportsRecommendation: Recommendation = {
      ...mockRecommendation,
      product: {
        ...mockRecommendation.product,
        category: 'Sports',
        name: 'Running Shoes'
      }
    };
    
    render(<RecommendationCard recommendation={sportsRecommendation} index={0} />);
    
    expect(screen.getByText('Running Shoes')).toBeInTheDocument();
    expect(screen.getByText('Sports')).toBeInTheDocument();
  });
});

