# Docker Deployment Guide

This guide explains how to build and run the Coding Interview Platform using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional but recommended)

## Building the Docker Image

From the `02-coding-interview` directory, run:

```bash
docker build -t coding-interview-platform:latest .
```

## Running with Docker

### Using Docker directly:

```bash
docker run -p 8000:8000 coding-interview-platform:latest
```

The application will be available at `http://localhost:8000`

### Using Docker Compose:

```bash
docker-compose up -d
```

To stop the container:

```bash
docker-compose down
```

## Image Details

### Multi-stage Build

The Dockerfile uses a multi-stage build process:

1. **Frontend Builder Stage**: 
   - Uses `node:18-alpine` to build the React/TypeScript frontend
   - Outputs built files to `dist/` directory

2. **Backend Stage**:
   - Uses `python:3.11-slim` for the final image
   - Installs Python dependencies from `requirements.txt`
   - Copies built frontend static files
   - Runs the FastAPI backend on port 8000
   - Serves both API endpoints and frontend files

### Final Image Size

- Optimized to ~500MB (slim Python image + built frontend)

## Architecture

```
Docker Container
├── Python 3.11
├── FastAPI Backend (port 8000)
├── Frontend Static Files (served by FastAPI)
└── Health Check Endpoint
```

## Environment Variables

You can customize the build and runtime by setting environment variables:

```bash
docker run -e PYTHONUNBUFFERED=1 -p 8000:8000 coding-interview-platform:latest
```

## Accessing the Application

- **Frontend**: `http://localhost:8000`
- **API**: `http://localhost:8000/api`
- **Health Check**: `http://localhost:8000/api/health`

## Development with Docker

For development with hot reload, you can mount volumes:

```bash
docker run -v $(pwd)/backend:/app/backend -p 8000:8000 coding-interview-platform:latest
```

## Troubleshooting

### Container won't start

Check logs:
```bash
docker logs <container-id>
```

### Port already in use

Use a different host port:
```bash
docker run -p 9000:8000 coding-interview-platform:latest
```

### Slow initial startup

The frontend build during image creation can take 2-3 minutes. This is normal.

## Production Deployment

For production, consider:

1. Using a reverse proxy (nginx)
2. Setting environment variables for production
3. Using a more specific Python base image
4. Implementing proper logging and monitoring

Example nginx reverse proxy configuration can be added if needed.
