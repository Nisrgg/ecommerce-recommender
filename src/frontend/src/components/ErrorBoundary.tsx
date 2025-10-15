// Error Boundary component for handling React errors

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({ error, errorInfo });
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-orange-50">
          <div className="max-w-md w-full mx-4">
            <div className="glass-card rounded-2xl p-8 text-center">
              <div className="flex justify-center mb-6">
                <AlertTriangle className="h-16 w-16 text-red-500" />
              </div>
              
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Oops! Something went wrong
              </h2>
              
              <p className="text-gray-600 mb-6">
                We're sorry, but something unexpected happened. Please try refreshing the page.
              </p>
              
              {this.state.error && (
                <details className="text-left mb-6 p-4 bg-gray-50 rounded-lg">
                  <summary className="cursor-pointer font-medium text-gray-700 mb-2">
                    Error Details
                  </summary>
                  <pre className="text-xs text-gray-600 overflow-auto">
                    {this.state.error.toString()}
                  </pre>
                </details>
              )}
              
              <button
                onClick={this.handleRetry}
                className="btn-primary w-full flex items-center justify-center gap-2"
              >
                <RefreshCw className="h-4 w-4" />
                Try Again
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

