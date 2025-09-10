# Income Estimator ML

A production-ready machine learning project for income estimation using modern MLOps practices.

## 🚀 Features

- **Production-Ready API**: FastAPI-based REST API with comprehensive validation and error handling
- **Multiple ML Algorithms**: Support for Random Forest, Gradient Boosting, Logistic Regression, SVM, and Neural Networks
- **Automated Hyperparameter Tuning**: Using Optuna, GridSearch, or RandomSearch
- **Data Validation**: Comprehensive data quality checks and validation
- **Model Registry**: Track and manage multiple model versions
- **Containerized Deployment**: Docker and Docker Compose support
- **Monitoring & Observability**: Prometheus metrics, health checks, and logging
- **Comprehensive Testing**: Unit tests, integration tests, and API tests
- **CLI Interface**: Command-line tools for training, prediction, and model management

## 📁 Project Structure

```
income-estimator-ml/
├── src/
│   └── income_estimator/
│       ├── api/                 # FastAPI application
│       ├── data/                # Data processing modules
│       ├── models/              # Model training and evaluation
│       ├── config.py            # Configuration management
│       ├── logger.py            # Logging utilities
│       └── cli.py               # Command-line interface
├── tests/                       # Test suite
├── data/                        # Data directories
├── models/                      # Trained models
├── config/                      # Configuration files
├── docs/                        # Documentation
├── notebooks/                   # Jupyter notebooks
├── monitoring/                  # Monitoring configuration
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Multi-service setup
├── requirements.txt            # Python dependencies
├── environment.yml             # Conda environment
└── pyproject.toml              # Project configuration
```

## 🛠️ Installation

### Option 1: Using Conda/Mamba (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd income-estimator-ml

# Create conda environment
mamba env create -f environment.yml
# or
conda env create -f environment.yml

# Activate environment
mamba activate income-estimator-ml
# or
conda activate income-estimator-ml

# Install the package
pip install -e .
```

### Option 2: Using pip

```bash
# Clone the repository
git clone <repository-url>
cd income-estimator-ml

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Option 3: Using Docker

```bash
# Clone the repository
git clone <repository-url>
cd income-estimator-ml

# Build and run with Docker Compose
docker-compose up --build
```

## 🚀 Quick Start

### 1. Train a Model

```bash
# Train with sample data
income-estimator train

# Train with your own data
income-estimator train --data-path /path/to/your/data.csv

# Train specific algorithms
income-estimator train --algorithms random_forest --algorithms gradient_boosting

# Train without hyperparameter tuning (faster)
income-estimator train --no-tune
```

### 2. Start the API Server

```bash
# Start the API server
income-estimator serve

# Start with custom host and port
income-estimator serve --host 0.0.0.0 --port 8080

# Start with auto-reload for development
income-estimator serve --reload
```

### 3. Make Predictions

```bash
# Interactive prediction
income-estimator predict

# Predict from JSON file
income-estimator predict --input-file prediction_input.json

# Use specific model
income-estimator predict --model-id model_20240101_120000
```

### 4. List Available Models

```bash
# List all models
income-estimator list-models

# Filter by model name
income-estimator list-models --model-name income_estimator

# Limit results
income-estimator list-models --limit 5
```

## 🌐 API Usage

### Start the API Server

```bash
# Using CLI
income-estimator serve

# Using uvicorn directly
uvicorn income_estimator.api.app:app --host 0.0.0.0 --port 8000

# Using Docker
docker-compose up income-estimator-api
```

### API Endpoints

- **Health Check**: `GET /health`
- **Metrics**: `GET /metrics`
- **Model Info**: `GET /model/info`
- **Single Prediction**: `POST /predict`
- **Batch Prediction**: `POST /predict/batch`
- **API Documentation**: `GET /docs` (Swagger UI)
- **Alternative Docs**: `GET /redoc` (ReDoc)

### Example API Usage

```python
import requests

# Single prediction
response = requests.post("http://localhost:8000/predict", json={
    "age": 35,
    "education_num": 13,
    "hours_per_week": 40,
    "capital_gain": 0,
    "capital_loss": 0,
    "education": "Bachelors",
    "occupation": "Tech-support",
    "marital_status": "Married-civ-spouse",
    "relationship": "Husband",
    "race": "White",
    "sex": "Male",
    "native_country": "United-States"
})

print(response.json())
```

```bash
# Using curl
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "age": 35,
       "education_num": 13,
       "hours_per_week": 40,
       "capital_gain": 0,
       "capital_loss": 0,
       "education": "Bachelors",
       "occupation": "Tech-support",
       "marital_status": "Married-civ-spouse",
       "relationship": "Husband",
       "race": "White",
       "sex": "Male",
       "native_country": "United-States"
     }'
```

## 🐳 Docker Deployment

### Production Deployment

```bash
# Build and start production services
docker-compose up -d income-estimator-api

# Check logs
docker-compose logs -f income-estimator-api

# Scale the service
docker-compose up -d --scale income-estimator-api=3
```

### Development Environment

```bash
# Start development environment with hot reload
docker-compose --profile dev up -d

# Start with Jupyter notebook
docker-compose --profile dev up -d jupyter

# Access Jupyter at http://localhost:8888
```

### Monitoring Stack

```bash
# Start monitoring services
docker-compose --profile monitoring up -d

# Access Prometheus at http://localhost:9090
# Access Grafana at http://localhost:3000 (admin/admin)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest tests/unit/          # Unit tests only
pytest tests/api/           # API tests only
pytest -m "not slow"        # Skip slow tests

# Run tests in Docker
docker-compose run --rm income-estimator-api pytest
```

## 📊 Monitoring and Observability

### Metrics

The API exposes Prometheus metrics at `/metrics`:

- `predictions_total`: Total number of predictions made
- `prediction_duration_seconds`: Prediction processing time
- `errors_total`: Total number of errors by type

### Health Checks

Health check endpoint at `/health` provides:

- Service status
- Model loading status
- Uptime information
- Version information

### Logging

Structured logging with:

- Request/response logging
- Error tracking
- Performance metrics
- Configurable log levels

## ⚙️ Configuration

Configuration is managed through:

1. **YAML files**: `config/config.yml`
2. **Environment variables**: `.env` file
3. **Command-line arguments**: CLI overrides

### Key Configuration Sections

- **Data**: Paths, validation rules, preprocessing options
- **Model**: Algorithms, hyperparameters, evaluation metrics
- **API**: Server settings, CORS, rate limiting
- **Logging**: Levels, formats, output destinations
- **Monitoring**: MLflow, metrics, health checks

## 🔧 Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run code formatting
black src/ tests/
isort src/ tests/

# Run type checking
mypy src/

# Run linting
flake8 src/ tests/
```

### Adding New Features

1. Create feature branch
2. Add tests for new functionality
3. Implement the feature
4. Update documentation
5. Run full test suite
6. Submit pull request

## 📚 Documentation

- **API Documentation**: Available at `/docs` when server is running
- **Code Documentation**: Inline docstrings and type hints
- **Architecture Guide**: See `docs/architecture.md`
- **Deployment Guide**: See `docs/deployment.md`
- **Contributing Guide**: See `docs/contributing.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: `/docs` endpoint when API is running
- **Examples**: See `notebooks/` directory

## 🔄 Version History

- **v0.1.0**: Initial release with basic ML pipeline and API

---

## 📋 Data Format

### Input Features

The model expects the following features:

#### Numerical Features
- `age`: Age of the person (16-100)
- `education_num`: Number of years of education (1-16)
- `hours_per_week`: Hours worked per week (1-100)
- `capital_gain`: Capital gains (≥0)
- `capital_loss`: Capital losses (≥0)

#### Categorical Features
- `education`: Education level (e.g., 'Bachelors', 'HS-grad', 'Masters')
- `occupation`: Occupation (e.g., 'Tech-support', 'Sales', 'Exec-managerial')
- `marital_status`: Marital status (e.g., 'Married-civ-spouse', 'Never-married')
- `relationship`: Relationship status (e.g., 'Husband', 'Wife', 'Not-in-family')
- `race`: Race (e.g., 'White', 'Black', 'Asian-Pac-Islander')
- `sex`: Gender ('Male' or 'Female')
- `native_country`: Native country (e.g., 'United-States', 'Canada')

### Output

The model predicts income class:
- `<=50K`: Income less than or equal to $50,000
- `>50K`: Income greater than $50,000

## 🚨 Troubleshooting

### Common Issues

1. **Model not found error**
   ```bash
   # Train a model first
   income-estimator train
   ```

2. **Permission denied in Docker**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

3. **Port already in use**
   ```bash
   # Use different port
   income-estimator serve --port 8001
   ```

4. **Memory issues during training**
   ```bash
   # Reduce dataset size or use simpler algorithms
   income-estimator train --algorithms logistic_regression
   ```

### Getting Help

- Check the logs: `tail -f logs/app.log`
- Validate your data: The validator will show specific issues
- Use health check: `curl http://localhost:8000/health`
- Check API docs: Visit `http://localhost:8000/docs`
