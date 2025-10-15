<p align="center">
  <img src="https://img.shields.io/badge/Built%20With-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Dockerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" />
</p>

# E-commerce Product Recommender

A production-grade AI-powered recommendation system built with FastAPI, React, and Docker, featuring intelligent collaborative filtering and Gemini AI-generated explanations.

## Overview

The E-commerce Product Recommender solves the critical challenge of personalized product discovery by implementing sophisticated collaborative filtering algorithms combined with AI-powered recommendation explanations. It provides a seamless full-stack experience with a modern React frontend consuming RESTful APIs from a FastAPI backend, all containerized for easy deployment and scaling.

## Features

### Core Functionality
- **Intelligent Recommendation Engine**: Collaborative filtering algorithms with TF-IDF vectorization and cosine similarity
- **AI-Powered Explanations**: Google Gemini AI generates human-readable explanations for each recommendation
- **Real-time User Analysis**: Dynamic user preference analysis based on interaction history
- **Product Catalog Management**: Comprehensive product database with categories and metadata
- **User Interaction Tracking**: Persistent user behavior analysis for improved recommendations

### AI Features
- **Smart Explanations**: Context-aware AI explanations for recommendation reasoning
- **Content-Based Filtering**: Advanced text analysis using scikit-learn TF-IDF
- **Hybrid Recommendation**: Combines collaborative and content-based approaches
- **Dynamic Scoring**: Real-time recommendation scoring and ranking

### Infrastructure
- **Dockerized Deployment**: Complete containerization with multi-stage builds
- **RESTful API**: Comprehensive FastAPI backend with automatic OpenAPI documentation
- **Modern Frontend**: React with TypeScript, Tailwind CSS, and responsive design
- **Database Integration**: SQLAlchemy ORM with SQLite for data persistence
- **Health Monitoring**: Built-in health checks and system monitoring

### Testing and Quality
- **Comprehensive Testing**: Unit tests for both backend (pytest) and frontend (Jest)
- **Type Safety**: Full TypeScript implementation with strict type checking
- **Code Quality**: ESLint, Prettier, and PEP 8 compliance
- **Error Handling**: Robust error boundaries and exception management

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React         │    │   FastAPI      │    │   SQLite       │
│   Frontend      │◄──►│   Backend      │◄──►│   Database     │
│   (TypeScript)  │    │   (Python)     │    │   (SQLAlchemy) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │   Gemini AI    │              │
         └─────────────►│   Explanations │◄─────────────┘
                        │   (Google)     │
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │   Scikit-learn  │
                        │   ML Engine     │
                        │   (TF-IDF)      │
                        └─────────────────┘
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nisrgg/ecommerce-recommender.git
   cd ecommerce-recommender
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the services**
   - **Frontend**: http://localhost:8000/static/
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health/

## API Endpoints

### Core Endpoints
- `GET /health/` - System health status and configuration
- `GET /products` - Retrieve all products in catalog
- `GET /products/{product_id}` - Get specific product details
- `GET /recommendations/with-explanations/{user_id}` - Get AI-powered recommendations
- `GET /users/{user_id}/interactions` - Get user interaction history

### Admin Endpoints
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Example Usage
```bash
# Get recommendations for user 1
curl -X GET "http://localhost:8000/recommendations/with-explanations/1"

# Check system health
curl -X GET "http://localhost:8000/health/"

# Get product details
curl -X GET "http://localhost:8000/products/1"
```

## Frontend Overview

The React frontend provides an intuitive interface for testing and demonstrating the recommendation system:

### Key Features
- **User Input Form**: Enter user IDs to generate personalized recommendations
- **Sample User Buttons**: Quick access to test with predefined users
- **Recommendation Cards**: Beautiful display of recommended products with AI explanations
- **Real-time Updates**: Dynamic loading states and error handling
- **Responsive Design**: Optimized for desktop and mobile devices

### Development Mode
```bash
cd src/frontend
npm install
npm run dev
```

## Project Structure

```
ecommerce-recommender/
├── src/                          # Source code
│   ├── backend/                  # FastAPI backend
│   │   └── app/
│   │       ├── api/               # API route handlers
│   │       │   ├── health.py
│   │       │   ├── products.py
│   │       │   ├── recommendations.py
│   │       │   └── users.py
│   │       ├── core/              # Core configuration
│   │       │   └── config.py
│   │       ├── models/            # Database models
│   │       ├── recommender/       # ML algorithms
│   │       │   ├── hybrid.py
│   │       │   └── recommender.py
│   │       ├── services/          # Business logic
│   │       │   ├── ai_explainer.py
│   │       │   └── cache.py
│   │       ├── tests/             # Backend tests
│   │       ├── utils/             # Utilities
│   │       ├── main.py            # FastAPI app
│   │       ├── models.py          # SQLAlchemy models
│   │       └── schemas.py         # Pydantic schemas
│   └── frontend/                  # React frontend
│       ├── src/
│       │   ├── components/        # React components
│       │   ├── pages/             # Page components
│       │   ├── hooks/             # Custom hooks
│       │   ├── services/          # API services
│       │   ├── types/             # TypeScript types
│       │   └── utils/             # Utilities
│       ├── public/                # Static assets
│       └── package.json           # Frontend dependencies
├── data/                          # Data files
│   ├── products.csv
│   ├── interactions.csv
│   └── ecommerce.db
├── docs/                          # Documentation
├── docker-compose.yml             # Service orchestration
├── Dockerfile                     # Multi-stage container
├── .env.example                   # Environment template
└── README.md                      # This file
```

## Tech Stack

### Backend
- **Python 3.12**: Core programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **Pydantic**: Data validation and settings management
- **Scikit-learn**: Machine learning library for recommendation algorithms
- **Google Generative AI**: AI service for generating recommendation explanations

### Frontend
- **React 18**: JavaScript library for building user interfaces
- **TypeScript**: Typed superset of JavaScript
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API requests
- **React Query**: Data fetching and caching library

### Infrastructure
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container application definition
- **SQLite**: Lightweight database engine
- **Uvicorn**: ASGI server for running FastAPI applications

## Configuration

### Environment Variables
- `GEMINI_API_KEY` - Google Gemini AI API key for explanations
- `DATABASE_URL` - Database connection string (default: sqlite:///./ecommerce.db)
- `DEBUG` - Enable debug mode (default: true)
- `LOG_LEVEL` - Logging level (default: INFO)
- `CORS_ORIGINS` - Allowed CORS origins
- `VITE_API_BASE_URL` - Frontend API base URL

### Docker Services
- **ecommerce-recommender**: Main application server (FastAPI + React)
- **Database**: SQLite database with persistent storage
- **Static Files**: Frontend assets served by FastAPI

## Testing

### Backend Testing
```bash
cd src/backend
pip install -r requirements.txt
pytest
```

### Frontend Testing
```bash
cd src/frontend
npm install
npm test
```

### Integration Testing
```bash
# Start the application
docker-compose up --build

# Test API endpoints
curl -X GET "http://localhost:8000/health/"
curl -X GET "http://localhost:8000/recommendations/with-explanations/1"
```

## Deployment

### Docker Deployment
```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f
```

### Production Considerations
- Configure proper environment variables
- Set up reverse proxy (Nginx) for production
- Implement proper logging and monitoring
- Consider database migration strategies
- Set up CI/CD pipelines for automated deployment

## Performance and Security

### Performance Optimizations
- **Caching**: Recommendation results cached for improved response times
- **Database Indexing**: Optimized queries with proper indexing
- **Efficient Algorithms**: TF-IDF vectorization with cosine similarity
- **Container Optimization**: Multi-stage Docker builds for smaller images

### Security Features
- **Input Validation**: Pydantic models for request/response validation
- **CORS Configuration**: Properly configured cross-origin resource sharing
- **Environment Variables**: Sensitive configuration stored securely
- **SQL Injection Prevention**: SQLAlchemy ORM provides protection
- **Error Handling**: Comprehensive error boundaries and exception management

## License

This project is licensed under the [MIT License](LICENSE).

## Author

**Nisarg Gajjar** — Developer & System Architect

---

*Built with modern technologies and best practices for scalable, maintainable software development.*