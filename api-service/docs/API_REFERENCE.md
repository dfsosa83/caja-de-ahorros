# 📚 API Reference - Income Prediction API

Complete reference documentation for all API endpoints, request/response schemas, and error codes.

## 🌐 Base URL

- **Local Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## 🔐 Authentication

Currently, the API does not require authentication. For production use, consider implementing:
- API Key authentication
- JWT tokens
- OAuth 2.0

## 📋 Common Headers

```http
Content-Type: application/json
Accept: application/json
X-API-Key: your-api-key (if authentication is enabled)
```

## 🏥 Health & Status Endpoints

### GET /health

Basic health check for the API service and ML model.

**Response 200 OK**:
```json
{
  "status": "healthy",
  "model_status": "loaded",
  "version": "1.0.0",
  "uptime_seconds": 3600.5,
  "timestamp": "2025-09-10T15:30:00Z"
}
```

**Response 503 Service Unavailable**:
```json
{
  "status": "unhealthy",
  "model_status": "error",
  "version": "1.0.0",
  "uptime_seconds": 3600.5,
  "timestamp": "2025-09-10T15:30:00Z"
}
```

### GET /health/detailed

Comprehensive health check with system metrics.

**Response 200 OK**:
```json
{
  "service": {
    "status": "healthy",
    "version": "1.0.0",
    "uptime_seconds": 3600.5,
    "uptime_human": "1h 0m"
  },
  "model": {
    "status": "loaded",
    "info": {
      "model_loaded": true,
      "model_version": "1.0.0",
      "feature_count": 10,
      "features": ["ocupacion_consolidated_freq", "edad", ...]
    }
  },
  "system": {
    "cpu_percent": 25.5,
    "memory": {
      "total_gb": 8.0,
      "available_gb": 6.2,
      "percent_used": 22.5
    },
    "disk": {
      "total_gb": 100.0,
      "free_gb": 75.0,
      "percent_used": 25.0
    }
  },
  "timestamp": "2025-09-10T15:30:00Z"
}
```

### GET /ready

Readiness check for load balancers and orchestrators.

**Response 200 OK**:
```json
{
  "status": "ready",
  "timestamp": "2025-09-10T15:30:00Z"
}
```

**Response 503 Service Unavailable**:
```json
{
  "detail": "Service not ready"
}
```

### GET /live

Liveness check for container orchestration.

**Response 200 OK**:
```json
{
  "status": "alive",
  "timestamp": "2025-09-10T15:30:00Z"
}
```

## 🎯 Prediction Endpoints

### POST /api/v1/predict

Make an income prediction for a single customer.

**Request Body**:
```json
{
  "cliente": "CUST001",
  "identificador_unico": "ID001",
  "edad": 35,
  "ocupacion": "Ingeniero",
  "fechaingresoempleo": "2020-01-15",
  "nombreempleadorcliente": "Tech Company SA",
  "cargoempleocliente": "Senior Engineer",
  "saldo": 5000.0,
  "monto_letra": 250.0,
  "fecha_inicio": "2019-06-01",
  "sexo": "M",
  "ciudad": "San José",
  "pais": "Costa Rica",
  "estado_civil": "Casado",
  "productos_activos": 3,
  "letras_mensuales": 12,
  "fecha_vencimiento": "2025-06-01",
  "monto_prestamo": 10000.0,
  "tasa_prestamo": 8.5
}
```

**Required Fields**:
- `cliente` (string): Customer ID
- `edad` (integer): Age (18-100)
- `ocupacion` (string): Occupation
- `fechaingresoempleo` (string): Employment start date (YYYY-MM-DD)
- `nombreempleadorcliente` (string): Employer name
- `cargoempleocliente` (string): Job position
- `saldo` (number): Account balance (≥ 0)
- `fecha_inicio` (string): Account start date (YYYY-MM-DD)

**Optional Fields**:
- `identificador_unico` (string): Unique identifier
- `monto_letra` (number): Monthly payment amount (≥ 0)
- `sexo` (string): Gender
- `ciudad` (string): City
- `pais` (string): Country
- `estado_civil` (string): Marital status
- `productos_activos` (integer): Active products count (≥ 0)
- `letras_mensuales` (integer): Monthly letters count (≥ 0)
- `fecha_vencimiento` (string): Expiration date (YYYY-MM-DD)
- `monto_prestamo` (number): Loan amount (≥ 0)
- `tasa_prestamo` (number): Loan interest rate (0-100)

**Response 200 OK**:
```json
{
  "customer_id": "CUST001",
  "predicted_income": 1450.75,
  "confidence_score": 0.85,
  "prediction_range": {
    "min": 1200.50,
    "max": 1700.00
  },
  "top_factors": [
    {
      "feature": "ocupacion",
      "impact": "high",
      "value": "Ingeniero"
    },
    {
      "feature": "edad",
      "impact": "medium",
      "value": 35
    }
  ],
  "processing_time_ms": 45.2,
  "timestamp": "2025-09-10T15:30:00Z",
  "model_version": "1.0.0"
}
```

### POST /api/v1/predict/batch

Make income predictions for multiple customers in a single request.

**Request Body**:
```json
{
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
}
```

**Constraints**:
- Maximum batch size: 1000 customers
- Minimum batch size: 1 customer

**Response 200 OK**:
```json
{
  "predictions": [
    {
      "customer_id": "CUST001",
      "predicted_income": 1450.75,
      "confidence_score": 0.85,
      "prediction_range": {
        "min": 1200.50,
        "max": 1700.00
      },
      "top_factors": [
        {
          "feature": "ocupacion",
          "impact": "high",
          "value": "Ingeniero"
        }
      ],
      "processing_time_ms": 45.2,
      "timestamp": "2025-09-10T15:30:00Z",
      "model_version": "1.0.0"
    },
    {
      "customer_id": "CUST002",
      "predicted_income": 980.25,
      "confidence_score": 0.78,
      "prediction_range": {
        "min": 800.00,
        "max": 1200.00
      },
      "top_factors": [
        {
          "feature": "edad",
          "impact": "medium",
          "value": 28
        }
      ],
      "processing_time_ms": 38.7,
      "timestamp": "2025-09-10T15:30:01Z",
      "model_version": "1.0.0"
    }
  ],
  "batch_summary": {
    "total_customers": 2,
    "successful_predictions": 2,
    "failed_predictions": 0,
    "average_income": 1215.50,
    "success_rate": 1.0
  },
  "total_processing_time_ms": 83.9
}
```

### GET /api/v1/model/info

Get information about the loaded ML model and its capabilities.

**Response 200 OK**:
```json
{
  "model_info": {
    "model_loaded": true,
    "model_version": "1.0.0",
    "feature_count": 10,
    "features": [
      "ocupacion_consolidated_freq",
      "nombreempleadorcliente_consolidated_freq",
      "edad",
      "fechaingresoempleo_days",
      "cargoempleocliente_consolidated_freq",
      "fecha_inicio_days",
      "balance_to_payment_ratio",
      "professional_stability_score",
      "saldo",
      "employment_years"
    ]
  },
  "api_version": "1.0.0",
  "max_batch_size": 1000,
  "timestamp": 1694358600.123
}
```

## ❌ Error Responses

### 400 Bad Request
Invalid request format or missing required parameters.

```json
{
  "error": "BadRequest",
  "message": "Invalid request format",
  "details": {
    "field": "edad",
    "issue": "Field is required"
  },
  "timestamp": "2025-09-10T15:30:00Z"
}
```

### 422 Validation Error
Input data validation failed.

```json
{
  "error": "ValidationError",
  "message": "Input validation failed",
  "details": {
    "field": "edad",
    "issue": "Age must be between 18 and 100"
  },
  "timestamp": "2025-09-10T15:30:00Z"
}
```

### 500 Internal Server Error
Unexpected server error during processing.

```json
{
  "error": "InternalServerError",
  "message": "An unexpected error occurred",
  "details": {
    "path": "/api/v1/predict"
  },
  "timestamp": "2025-09-10T15:30:00Z"
}
```

### 503 Service Unavailable
Service or model is not available.

```json
{
  "error": "ServiceUnavailable",
  "message": "Prediction service is not available",
  "timestamp": "2025-09-10T15:30:00Z"
}
```

## 📊 Response Headers

All responses include these headers:
- `X-Process-Time`: Request processing time in seconds
- `Content-Type`: `application/json`

## 🔄 Rate Limiting

Currently no rate limiting is implemented. For production use, consider:
- Requests per minute limits
- Concurrent request limits
- IP-based throttling

## 📝 OpenAPI Specification

The complete OpenAPI 3.0 specification is available at:
- **JSON**: `GET /openapi.json`
- **Interactive Docs**: `GET /docs`
- **Alternative Docs**: `GET /redoc`

---

**💡 Tip**: Use the interactive documentation at `/docs` for easy API exploration and testing!
