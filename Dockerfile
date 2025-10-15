# Multi-stage Dockerfile for E-commerce Product Recommender
# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY src/frontend/package*.json ./
RUN npm install
COPY src/frontend/ .
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npx vite build

# Stage 2: Backend + Frontend
FROM python:3.12-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY src/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY src/backend/ ./

# Copy CSV data files
COPY data/*.csv ./

# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./static

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting E-commerce Product Recommender..."\n\
echo "Backend: http://localhost:8000"\n\
echo "Frontend: http://localhost:8000/static"\n\
echo "API Docs: http://localhost:8000/docs"\n\
echo ""\n\
# Start FastAPI with static file serving\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 &\n\
\n\
# Wait for backend to start\n\
sleep 5\n\
\n\
# Test backend health\n\
echo "Testing backend health..."\n\
curl -f http://localhost:8000/health/ || echo "Backend health check failed"\n\
\n\
# Test frontend\n\
echo "Testing frontend..."\n\
curl -f http://localhost:8000/static/ || echo "Frontend test failed"\n\
\n\
echo "Application is ready!"\n\
echo "Visit: http://localhost:8000/static"\n\
\n\
# Keep container running\n\
wait' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Start the application
CMD ["/app/start.sh"]
