# =============================================================================
# Income Prediction API - Production Dockerfile
# =============================================================================
# 
# This Dockerfile creates a production-ready container for the Income Prediction API
# that wraps your existing ML pipeline without modifying any of your code.
#
# Build: docker build -t income-prediction-api .
# Run:   docker run -p 8000:8000 income-prediction-api
# =============================================================================

# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set metadata
LABEL maintainer="Caja de Ahorros ML Team"
LABEL description="Income Prediction API Service"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV API_LOG_LEVEL=INFO

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY api-service/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the API service code
COPY api-service/ ./api-service/

# Copy the models directory (your existing ML pipeline)
COPY models/ ./models/

# Copy the data directory (for any reference data)
COPY data/ ./data/

# Create non-root user for security
RUN groupadd -r apiuser && useradd -r -g apiuser apiuser
RUN chown -R apiuser:apiuser /app
USER apiuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set working directory to api-service
WORKDIR /app/api-service

# Default command
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
