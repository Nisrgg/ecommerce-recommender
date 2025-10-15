// Navigation bar component

import React from 'react';
import { ShoppingBag, Github, Heart } from 'lucide-react';
import { cn } from '../utils';

const Navbar: React.FC = () => {
  return (
    <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200/20 dark:border-gray-700/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl">
              <ShoppingBag className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">
                E-commerce Recommender
              </h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                AI-Powered Product Recommendations
              </p>
            </div>
          </div>

          {/* Navigation Items */}
          <div className="flex items-center space-x-4">
            {/* GitHub Link */}
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className={cn(
                "p-2 rounded-lg transition-all duration-200",
                "hover:bg-gray-100 dark:hover:bg-gray-800",
                "text-gray-600 dark:text-gray-300"
              )}
              aria-label="View on GitHub"
            >
              <Github className="h-5 w-5" />
            </a>

            {/* Made with Love */}
            <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
              <span>Made with</span>
              <Heart className="h-4 w-4 text-red-500 fill-current" />
              <span>for better shopping</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

