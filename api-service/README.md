# 🏦 Income Prediction API Service

A production-ready FastAPI service that wraps the existing Caja de Ahorros income prediction ML pipeline to provide REST API endpoints for real-time and batch predictions.

## 🎯 Overview

This API service provides a **zero-modification wrapper** around your existing income prediction pipeline, exposing it as a modern REST API without touching any of your working code.

### Key Features
- **🚀 Production Ready**: FastAPI with automatic documentation, validation, and error handling
- **🔒 Zero Code Modification**: Uses your existing pipeline without any changes
- **📦 Containerized**: Docker support for easy deployment
- **⚡ High Performance**: Async endpoints with batch processing support
- **📊 Monitoring**: Comprehensive health checks and system metrics
- **🛡️ Robust**: Input validation, error handling, and logging

## 📋 Quick Start

### Prerequisites
- Python 3.9+
- Your existing model file: `models/production/final_production_model_nested_cv.pkl`
- Docker (optional, for containerized deployment)

### 1. Local Development Setup

```bash
# Navigate to the API service directory
cd api-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env

# Start the API server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Docker Deployment

```bash
# Build and run with Docker Compose
cd api-service
docker-compose up --build

# Or build and run manually
docker build -t income-prediction-api .
docker run -p 8000:8000 income-prediction-api
```

### 3. Verify Installation

```bash
# Check health
curl http://localhost:8000/health

# View interactive documentation
open http://localhost:8000/docs
```

## 🔧 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and status |
| `/docs` | GET | Interactive API documentation (Swagger UI) |
| `/redoc` | GET | Alternative API documentation (ReDoc) |

### Health & Monitoring

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Basic health check |
| `/health/detailed` | GET | Detailed health with system metrics |
| `/ready` | GET | Readiness check for load balancers |
| `/live` | GET | Liveness check for container orchestration |

### Predictions

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/predict` | POST | Single customer income prediction |
| `/api/v1/predict/batch` | POST | Batch predictions for multiple customers |
| `/api/v1/model/info` | GET | Model information and metadata |

## 📝 Usage Examples

### Single Customer Prediction

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": "CUST001",
    "edad": 35,
    "ocupacion": "Ingeniero",
    "fechaingresoempleo": "2020-01-15",
    "nombreempleadorcliente": "Tech Company SA",
    "cargoempleocliente": "Senior Engineer",
    "saldo": 5000.0,
    "monto_letra": 250.0,
    "fecha_inicio": "2019-06-01"
  }'
```

**Response:**
```json
{
  "customer_id": "CUST001",
  "predicted_income": 1450.75,
  "confidence_score": 0.85,
  "prediction_range": {
    "min": 1200.50,
    "max": 1700.00
  },
  "processing_time_ms": 45.2,
  "timestamp": "2025-09-10T15:30:00Z",
  "model_version": "1.0.0"
}
```

### Batch Prediction

```bash
curl -X POST "http://localhost:8000/api/v1/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "customers": [
      {
        "cliente": "CUST001",
        "edad": 35,
        "ocupacion": "Ingeniero",
        "fechaingresoempleo": "2020-01-15",
        "nombreempleadorcliente": "Tech Company SA",
        "cargoempleocliente": "Senior Engineer",
        "saldo": 5000.0,
        "monto_letra": 250.0,
        "fecha_inicio": "2019-06-01"
      },
      {
        "cliente": "CUST002",
        "edad": 28,
        "ocupacion": "Contador",
        "fechaingresoempleo": "2021-03-10",
        "nombreempleadorcliente": "Finance Corp",
        "cargoempleocliente": "Junior Accountant",
        "saldo": 2500.0,
        "monto_letra": 150.0,
        "fecha_inicio": "2020-08-15"
      }
    ]
  }'
```

### Python Client Example

```python
import requests

# Initialize client
api_url = "http://localhost:8000"

# Single prediction
customer_data = {
    "cliente": "CUST001",
    "edad": 35,
    "ocupacion": "Ingeniero",
    "fechaingresoempleo": "2020-01-15",
    "nombreempleadorcliente": "Tech Company SA",
    "cargoempleocliente": "Senior Engineer",
    "saldo": 5000.0,
    "monto_letra": 250.0,
    "fecha_inicio": "2019-06-01"
}

response = requests.post(f"{api_url}/api/v1/predict", json=customer_data)
prediction = response.json()

print(f"Predicted income: ${prediction['predicted_income']:,.2f}")
```

## 🏗️ Architecture

### Service Structure
```
api-service/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/                # Configuration and utilities
│   ├── models/              # Pydantic schemas
│   ├── routers/             # API endpoints
│   └── services/            # Business logic (wraps your pipeline)
├── tests/                   # Test suite
├── examples/                # Usage examples
├── docs/                    # Documentation
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-service deployment
└── requirements.txt         # Dependencies
```

### How It Works
1. **Zero Modification**: Your existing code in `models/production/` remains untouched
2. **Service Wrapper**: `PredictionService` imports and uses your existing pipeline
3. **API Layer**: FastAPI provides REST endpoints with validation and documentation
4. **Containerization**: Docker ensures consistent deployment across environments

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# Model Configuration
API_MODEL_PATH="../../models/production/final_production_model_nested_cv.pkl"
API_MAX_BATCH_SIZE=1000

# Logging
API_LOG_LEVEL=INFO
```

### Docker Configuration

Customize `docker-compose.yml` for your environment:

```yaml
environment:
  - API_HOST=0.0.0.0
  - API_PORT=8000
  - API_MAX_BATCH_SIZE=1000
  - API_LOG_LEVEL=INFO
```

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Example Scripts
```bash
# Python examples
python examples/example_requests.py

# cURL examples
chmod +x examples/curl_examples.sh
./examples/curl_examples.sh
```

## 🚀 Deployment

### Local Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Compose
```bash
docker-compose up --build
```

### Production Deployment

1. **Cloud Platforms**:
   - AWS ECS/Fargate
   - Google Cloud Run
   - Azure Container Instances
   - DigitalOcean App Platform

2. **Configuration**:
   - Set `API_DEBUG=false`
   - Configure appropriate `API_CORS_ORIGINS`
   - Use environment-specific `.env` files
   - Set up proper logging and monitoring

## 📊 Monitoring

### Health Checks
- **Basic**: `/health` - Service and model status
- **Detailed**: `/health/detailed` - System metrics and resource usage
- **Readiness**: `/ready` - For load balancer health checks
- **Liveness**: `/live` - For container orchestration

### Metrics
- Request processing time (in response headers)
- Model prediction performance
- System resource usage
- Error rates and types

## 🛡️ Security

### Production Considerations
- Configure CORS origins appropriately
- Use HTTPS in production
- Implement API key authentication if needed
- Set up rate limiting
- Monitor and log all requests
- Use non-root user in containers

## 📚 Documentation

- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🤝 Integration

### Client Libraries
The API follows OpenAPI 3.0 standards, so you can generate client libraries for any language:

```bash
# Generate Python client
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o client-python

# Generate JavaScript client
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g javascript -o client-js
```

## 🔍 Troubleshooting

### Common Issues

1. **Model Not Loading**
   - Check model file path in configuration
   - Verify model file exists and is accessible
   - Check logs for detailed error messages

2. **Import Errors**
   - Ensure Python path includes project root
   - Verify all dependencies are installed
   - Check that your existing pipeline code is accessible

3. **Performance Issues**
   - Monitor system resources with `/health/detailed`
   - Consider batch processing for multiple predictions
   - Adjust Docker resource limits if needed

### Logs
```bash
# View container logs
docker-compose logs -f income-prediction-api

# View specific service logs
docker logs income-prediction-api
```

## 🚀 Getting Started Checklist

- [ ] Clone/navigate to the `api-service` directory
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy configuration: `cp .env.example .env`
- [ ] Start the service: `uvicorn app.main:app --reload`
- [ ] Test health: `curl http://localhost:8000/health`
- [ ] View docs: http://localhost:8000/docs
- [ ] Run examples: `python examples/example_requests.py`

## 📞 Support

- **Documentation**: Interactive docs at `/docs` when service is running
- **Examples**: See `examples/` directory for usage patterns
- **Health Monitoring**: Use `/health` endpoints for service monitoring
- **Issues**: Check logs and health endpoints for troubleshooting

## 📄 License

This API service is part of the Caja de Ahorros income prediction project.

---

**🎉 Your ML pipeline is now accessible via REST API!**

Visit http://localhost:8000/docs to explore the interactive documentation and start making predictions.
