// User input form component

import React, { useState } from 'react';
import { Search, Users, Loader2 } from 'lucide-react';
import { UserInputFormProps } from '../types';
import { cn, isValidNumber } from '../utils';

const UserInputForm: React.FC<UserInputFormProps> = ({ onSubmit, loading }) => {
  const [userId, setUserId] = useState('');
  const [error, setError] = useState('');

  const sampleUsers = [1, 5, 10, 15, 20];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!userId.trim()) {
      setError('Please enter a valid user ID');
      return;
    }

    if (!isValidNumber(userId)) {
      setError('Please enter a valid number');
      return;
    }

    const userIdNum = parseInt(userId, 10);
    if (userIdNum < 1 || userIdNum > 50) {
      setError('User ID must be between 1 and 50');
      return;
    }

    setError('');
    onSubmit(userIdNum);
  };

  const handleSampleUserClick = (sampleUserId: number) => {
    setUserId(sampleUserId.toString());
    setError('');
    onSubmit(sampleUserId);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserId(e.target.value);
    if (error) setError('');
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="glass-card rounded-2xl p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-2xl">
              <Search className="h-8 w-8 text-white" />
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Find Recommendations
          </h2>
          <p className="text-gray-600 dark:text-gray-300">
            Enter a user ID to get personalized product recommendations powered by AI
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="userId" className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              User ID
            </label>
            <div className="relative">
              <input
                id="userId"
                type="number"
                value={userId}
                onChange={handleInputChange}
                placeholder="Enter user ID (1-50)"
                min="1"
                max="50"
                disabled={loading}
                className={cn(
                  "input-field pr-12",
                  error && "border-red-500 focus:border-red-500 focus:ring-red-200",
                  loading && "opacity-50 cursor-not-allowed"
                )}
              />
              {loading && (
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <Loader2 className="h-5 w-5 text-primary-500 animate-spin" />
                </div>
              )}
            </div>
            {error && (
              <p className="mt-2 text-sm text-red-600 dark:text-red-400">{error}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading || !userId.trim()}
            className={cn(
              "btn-primary w-full flex items-center justify-center gap-2",
              (loading || !userId.trim()) && "opacity-50 cursor-not-allowed"
            )}
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                Getting Recommendations...
              </>
            ) : (
              <>
                <Search className="h-5 w-5" />
                Get Recommendations
              </>
            )}
          </button>
        </form>

        {/* Sample Users */}
        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
          <div className="text-center">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Quick test with sample users:
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {sampleUsers.map((sampleUserId) => (
                <button
                  key={sampleUserId}
                  onClick={() => handleSampleUserClick(sampleUserId)}
                  disabled={loading}
                  className={cn(
                    "px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200",
                    "bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300",
                    "hover:bg-gray-200 dark:hover:bg-gray-700",
                    "border border-gray-200 dark:border-gray-600",
                    "hover:border-primary-300 dark:hover:border-primary-600",
                    "hover:shadow-md transform hover:-translate-y-0.5",
                    loading && "opacity-50 cursor-not-allowed"
                  )}
                >
                  <Users className="h-4 w-4 inline mr-1" />
                  User {sampleUserId}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserInputForm;

