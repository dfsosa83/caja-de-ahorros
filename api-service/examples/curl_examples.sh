#!/bin/bash

# =============================================================================
# Income Prediction API - cURL Examples
# =============================================================================
# 
# This script demonstrates how to use the Income Prediction API with cURL
# commands for testing and integration purposes.
#
# Usage:
#   chmod +x curl_examples.sh
#   ./curl_examples.sh
# =============================================================================

# API base URL
API_URL="http://localhost:8000"

echo "🏦 Income Prediction API - cURL Examples"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo -e "\n${BLUE}$1${NC}"
    echo "----------------------------------------"
}

# Function to execute curl with error handling
execute_curl() {
    local description="$1"
    local curl_command="$2"
    
    echo -e "${YELLOW}$description${NC}"
    echo "Command: $curl_command"
    echo ""
    
    # Execute the command and capture the response
    response=$(eval "$curl_command" 2>/dev/null)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ Success:${NC}"
        echo "$response" | python -m json.tool 2>/dev/null || echo "$response"
    else
        echo -e "${RED}❌ Failed: Connection error${NC}"
    fi
    echo ""
}

# 1. Health Checks
print_section "1. Health Checks"

execute_curl "Basic Health Check" \
    "curl -s -X GET '$API_URL/health'"

execute_curl "Detailed Health Check" \
    "curl -s -X GET '$API_URL/health/detailed'"

execute_curl "Readiness Check" \
    "curl -s -X GET '$API_URL/ready'"

execute_curl "Liveness Check" \
    "curl -s -X GET '$API_URL/live'"

# 2. API Information
print_section "2. API Information"

execute_curl "Root Endpoint" \
    "curl -s -X GET '$API_URL/'"

execute_curl "Model Information" \
    "curl -s -X GET '$API_URL/api/v1/model/info'"

# 3. Single Prediction
print_section "3. Single Customer Prediction"

# Sample customer data
CUSTOMER_DATA='{
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
  "estado_civil": "Casado"
}'

execute_curl "Single Customer Prediction" \
    "curl -s -X POST '$API_URL/api/v1/predict' \
     -H 'Content-Type: application/json' \
     -d '$CUSTOMER_DATA'"

# 4. Batch Prediction
print_section "4. Batch Prediction"

# Sample batch data
BATCH_DATA='{
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

execute_curl "Batch Prediction" \
    "curl -s -X POST '$API_URL/api/v1/predict/batch' \
     -H 'Content-Type: application/json' \
     -d '$BATCH_DATA'"

# 5. Error Handling Examples
print_section "5. Error Handling Examples"

# Invalid customer data (missing required fields)
INVALID_DATA='{
  "cliente": "INVALID",
  "edad": 150
}'

execute_curl "Invalid Data (Validation Error)" \
    "curl -s -X POST '$API_URL/api/v1/predict' \
     -H 'Content-Type: application/json' \
     -d '$INVALID_DATA'"

# Non-existent endpoint
execute_curl "Non-existent Endpoint (404 Error)" \
    "curl -s -X GET '$API_URL/nonexistent'"

# 6. Performance Testing
print_section "6. Performance Testing"

echo -e "${YELLOW}Performance Test - 10 Sequential Requests${NC}"
echo "Command: Multiple single predictions"
echo ""

start_time=$(date +%s%N)
success_count=0
total_requests=10

for i in $(seq 1 $total_requests); do
    response=$(curl -s -X POST "$API_URL/api/v1/predict" \
        -H 'Content-Type: application/json' \
        -d "$CUSTOMER_DATA" 2>/dev/null)
    
    if echo "$response" | grep -q "predicted_income"; then
        ((success_count++))
    fi
done

end_time=$(date +%s%N)
duration_ms=$(( (end_time - start_time) / 1000000 ))

echo -e "${GREEN}✅ Performance Results:${NC}"
echo "Total Requests: $total_requests"
echo "Successful: $success_count"
echo "Failed: $((total_requests - success_count))"
echo "Total Time: ${duration_ms}ms"
echo "Average Time: $((duration_ms / total_requests))ms per request"
echo ""

# 7. Documentation
print_section "7. API Documentation"

echo -e "${YELLOW}Interactive API Documentation${NC}"
echo "Swagger UI: $API_URL/docs"
echo "ReDoc: $API_URL/redoc"
echo "OpenAPI JSON: $API_URL/openapi.json"
echo ""

echo -e "${GREEN}🎉 All cURL examples completed!${NC}"
echo ""
echo "💡 Tips:"
echo "- Use the interactive docs at $API_URL/docs for easier testing"
echo "- Check health endpoints regularly for monitoring"
echo "- Use batch predictions for better performance with multiple customers"
echo "- Monitor the logs for detailed error information"
