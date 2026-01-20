# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY frontend/src ./src
COPY frontend/public ./public
COPY frontend/*.config.* ./
COPY frontend/*.json ./
COPY frontend/*.ts ./

# Build frontend
RUN npm run build

# Stage 2: Setup backend with built frontend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY backend ./backend

# Copy built frontend to backend static directory
RUN mkdir -p backend/app/static
COPY --from=frontend-builder /app/frontend/dist ./backend/app/static

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run the backend server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
