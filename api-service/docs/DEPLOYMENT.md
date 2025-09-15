# 🚀 Deployment Guide - Income Prediction API

This guide covers different deployment strategies for the Income Prediction API service.

## 📋 Prerequisites

- Docker and Docker Compose installed
- Your trained model file: `models/production/final_production_model_nested_cv.pkl`
- Access to your target deployment environment

## 🏠 Local Development

### Quick Start
```bash
cd api-service
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### With Docker
```bash
cd api-service
docker-compose up --build
```

## 🐳 Docker Deployment

### Single Container
```bash
# Build the image
docker build -t income-prediction-api .

# Run the container
docker run -d \
  --name income-prediction-api \
  -p 8000:8000 \
  -v $(pwd)/../models:/app/models:ro \
  -e API_LOG_LEVEL=INFO \
  income-prediction-api
```

### Docker Compose (Recommended)
```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# With custom configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## ☁️ Cloud Deployment

### AWS ECS/Fargate

1. **Build and push image to ECR**:
```bash
# Create ECR repository
aws ecr create-repository --repository-name income-prediction-api

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag image
docker build -t income-prediction-api .
docker tag income-prediction-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/income-prediction-api:latest

# Push image
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/income-prediction-api:latest
```

2. **Create ECS task definition**:
```json
{
  "family": "income-prediction-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "income-prediction-api",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/income-prediction-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "API_LOG_LEVEL", "value": "INFO"},
        {"name": "API_DEBUG", "value": "false"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/income-prediction-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/income-prediction-api

# Deploy to Cloud Run
gcloud run deploy income-prediction-api \
  --image gcr.io/PROJECT-ID/income-prediction-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --memory 2Gi \
  --cpu 1 \
  --set-env-vars API_LOG_LEVEL=INFO,API_DEBUG=false
```

### Azure Container Instances

```bash
# Create resource group
az group create --name income-prediction-rg --location eastus

# Create container instance
az container create \
  --resource-group income-prediction-rg \
  --name income-prediction-api \
  --image income-prediction-api:latest \
  --cpu 1 \
  --memory 2 \
  --ports 8000 \
  --environment-variables API_LOG_LEVEL=INFO API_DEBUG=false \
  --restart-policy Always
```

## 🔧 Configuration

### Environment Variables

**Development**:
```bash
API_DEBUG=true
API_LOG_LEVEL=DEBUG
API_CORS_ORIGINS=["*"]
```

**Production**:
```bash
API_DEBUG=false
API_LOG_LEVEL=INFO
API_CORS_ORIGINS=["https://yourdomain.com"]
API_MAX_BATCH_SIZE=1000
```

### Resource Requirements

**Minimum**:
- CPU: 0.5 cores
- Memory: 1GB
- Storage: 2GB

**Recommended**:
- CPU: 1 core
- Memory: 2GB
- Storage: 5GB

**High Load**:
- CPU: 2+ cores
- Memory: 4GB+
- Storage: 10GB+

## 📊 Monitoring

### Health Checks

Configure your load balancer/orchestrator to use:
- **Health Check**: `GET /health`
- **Readiness**: `GET /ready`
- **Liveness**: `GET /live`

### Logging

The service logs to stdout in JSON format. Configure log aggregation:

**Docker Compose**:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

**Kubernetes**:
```yaml
spec:
  containers:
  - name: income-prediction-api
    image: income-prediction-api:latest
    resources:
      requests:
        memory: "1Gi"
        cpu: "500m"
      limits:
        memory: "2Gi"
        cpu: "1000m"
```

## 🛡️ Security

### Production Security Checklist

- [ ] Use HTTPS/TLS encryption
- [ ] Configure CORS origins appropriately
- [ ] Implement API key authentication
- [ ] Set up rate limiting
- [ ] Use non-root container user
- [ ] Scan images for vulnerabilities
- [ ] Enable audit logging
- [ ] Restrict network access
- [ ] Use secrets management for sensitive data

### Example Nginx Configuration

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name api.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://income-prediction-api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /health {
        proxy_pass http://income-prediction-api:8000/health;
        access_log off;
    }
}
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy Income Prediction API

on:
  push:
    branches: [main]
    paths: ['api-service/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        cd api-service
        docker build -t income-prediction-api:${{ github.sha }} .
    
    - name: Run tests
      run: |
        cd api-service
        docker run --rm income-prediction-api:${{ github.sha }} pytest tests/
    
    - name: Deploy to production
      run: |
        # Add your deployment commands here
        echo "Deploying to production..."
```

## 🚨 Troubleshooting

### Common Issues

1. **Container fails to start**:
   - Check model file path and permissions
   - Verify environment variables
   - Review container logs

2. **High memory usage**:
   - Monitor with `/health/detailed`
   - Consider model optimization
   - Increase container memory limits

3. **Slow predictions**:
   - Use batch endpoints for multiple predictions
   - Check system resources
   - Consider horizontal scaling

### Debugging Commands

```bash
# Check container logs
docker logs income-prediction-api

# Execute shell in container
docker exec -it income-prediction-api /bin/bash

# Check health status
curl http://localhost:8000/health/detailed

# Monitor resource usage
docker stats income-prediction-api
```

## 📈 Scaling

### Horizontal Scaling

**Docker Compose**:
```yaml
services:
  income-prediction-api:
    # ... configuration ...
    deploy:
      replicas: 3
```

**Kubernetes**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: income-prediction-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: income-prediction-api
  template:
    metadata:
      labels:
        app: income-prediction-api
    spec:
      containers:
      - name: income-prediction-api
        image: income-prediction-api:latest
        ports:
        - containerPort: 8000
```

### Load Balancing

Use a load balancer to distribute traffic across multiple instances:
- AWS Application Load Balancer
- Google Cloud Load Balancer
- Azure Load Balancer
- Nginx/HAProxy

---

**🎯 Your API is now ready for production deployment!**

Choose the deployment strategy that best fits your infrastructure and requirements.
