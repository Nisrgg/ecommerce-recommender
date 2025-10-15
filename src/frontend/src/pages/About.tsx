// About page component

import React from 'react';
import { 
  Brain, 
  Database, 
  Zap, 
  Shield, 
  Code, 
  Users, 
  BarChart3, 
  Globe,
  ArrowRight,
  CheckCircle
} from 'lucide-react';

const About: React.FC = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Explanations',
      description: 'Uses Google Gemini AI to generate natural, friendly explanations for each recommendation.',
    },
    {
      icon: Database,
      title: 'Content-Based Filtering',
      description: 'Analyzes product features using TF-IDF vectorization and cosine similarity.',
    },
    {
      icon: Zap,
      title: 'Real-Time Processing',
      description: 'Fast API responses with intelligent caching for optimal performance.',
    },
    {
      icon: Shield,
      title: 'Robust Error Handling',
      description: 'Graceful fallbacks and comprehensive error management throughout the system.',
    },
    {
      icon: Code,
      title: 'Modern Architecture',
      description: 'Built with FastAPI, React, TypeScript, and Tailwind CSS for maintainability.',
    },
    {
      icon: Users,
      title: 'User-Centric Design',
      description: 'Intuitive interface with responsive design and accessibility features.',
    },
  ];

  const techStack = [
    { name: 'FastAPI', category: 'Backend Framework' },
    { name: 'React 18', category: 'Frontend Framework' },
    { name: 'TypeScript', category: 'Type Safety' },
    { name: 'Tailwind CSS', category: 'Styling' },
    { name: 'SQLite', category: 'Database' },
    { name: 'Scikit-learn', category: 'Machine Learning' },
    { name: 'Google Gemini', category: 'AI Service' },
    { name: 'Pytest', category: 'Testing' },
  ];

  const stats = [
    { label: 'Products', value: '25+' },
    { label: 'Users', value: '50+' },
    { label: 'Interactions', value: '300+' },
    { label: 'Categories', value: '4' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-16">
            <div className="flex justify-center mb-6">
              <div className="flex items-center justify-center w-20 h-20 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-3xl">
                <Brain className="h-10 w-10 text-white" />
              </div>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
              About the E-commerce Recommender
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed">
              A sophisticated recommendation system that combines content-based filtering with AI-generated explanations 
              to provide personalized product recommendations for e-commerce platforms.
            </p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
            {stats.map((stat, index) => (
              <div key={index} className="glass-card rounded-2xl p-6 text-center">
                <div className="text-3xl font-bold text-primary-600 dark:text-primary-400 mb-2">
                  {stat.value}
                </div>
                <div className="text-gray-600 dark:text-gray-300 font-medium">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>

          {/* Features */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
              Key Features
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <div key={index} className="glass-card rounded-2xl p-6 card-hover">
                  <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl mb-4">
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Tech Stack */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
              Technology Stack
            </h2>
            <div className="glass-card rounded-2xl p-8">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                {techStack.map((tech, index) => (
                  <div key={index} className="text-center">
                    <div className="bg-gradient-to-r from-primary-100 to-secondary-100 dark:from-primary-900/20 dark:to-secondary-900/20 rounded-xl p-4 mb-3">
                      <div className="text-lg font-semibold text-gray-900 dark:text-white">
                        {tech.name}
                      </div>
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      {tech.category}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* How It Works */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
              How It Works
            </h2>
            <div className="space-y-8">
              {[
                {
                  step: '1',
                  title: 'User Interaction Analysis',
                  description: 'The system identifies the user\'s most recent product interaction to understand their preferences.',
                  icon: Users,
                },
                {
                  step: '2',
                  title: 'Content-Based Filtering',
                  description: 'Creates text representations from product features and uses TF-IDF vectorization with cosine similarity.',
                  icon: Database,
                },
                {
                  step: '3',
                  title: 'Recommendation Generation',
                  description: 'Finds the most similar products based on content similarity scores.',
                  icon: BarChart3,
                },
                {
                  step: '4',
                  title: 'AI Explanation',
                  description: 'Uses Google Gemini AI to generate friendly, natural explanations for each recommendation.',
                  icon: Brain,
                },
              ].map((step, index) => (
                <div key={index} className="flex items-start space-x-6">
                  <div className="flex-shrink-0">
                    <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl text-white font-bold">
                      {step.step}
                    </div>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <step.icon className="h-6 w-6 text-primary-500" />
                      <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                        {step.title}
                      </h3>
                    </div>
                    <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                      {step.description}
                    </p>
                  </div>
                  {index < 3 && (
                    <div className="hidden md:block">
                      <ArrowRight className="h-6 w-6 text-gray-400" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Benefits */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
              Benefits
            </h2>
            <div className="glass-card rounded-2xl p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                    For Users
                  </h3>
                  <ul className="space-y-3">
                    {[
                      'Personalized product recommendations',
                      'AI-powered explanations for transparency',
                      'Fast and responsive user experience',
                      'Intuitive and accessible interface',
                    ].map((benefit, index) => (
                      <li key={index} className="flex items-center space-x-3">
                        <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                        <span className="text-gray-600 dark:text-gray-300">{benefit}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                    For Businesses
                  </h3>
                  <ul className="space-y-3">
                    {[
                      'Increased customer engagement',
                      'Higher conversion rates',
                      'Scalable recommendation engine',
                      'Modern, maintainable codebase',
                    ].map((benefit, index) => (
                      <li key={index} className="flex items-center space-x-3">
                        <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                        <span className="text-gray-600 dark:text-gray-300">{benefit}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Call to Action */}
          <div className="text-center">
            <div className="glass-card rounded-2xl p-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Ready to Try It Out?
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-6">
                Experience the power of AI-driven recommendations with our intelligent system.
              </p>
              <a
                href="/"
                className="btn-primary inline-flex items-center space-x-2"
              >
                <span>Get Started</span>
                <ArrowRight className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;

