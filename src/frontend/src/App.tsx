// Main App component with routing

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import Navbar from './components/Navbar';
import ErrorBoundary from './components/ErrorBoundary';
import Home from './pages/Home';
import About from './pages/About';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    },
  },
});

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <Router basename="/static">
          <div className="min-h-screen transition-colors duration-300">
            <Navbar />
            
            <main className="relative">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
              </Routes>
            </main>
          </div>
        </Router>
      </QueryClientProvider>
    </ErrorBoundary>
  );
};

export default App;

