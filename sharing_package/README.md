# 🏦 Caja de Ahorros - Income Prediction Model

A comprehensive machine learning project for predicting customer income using advanced feature engineering, nested cross-validation, and production-ready deployment pipelines.

## 📋 Project Overview

**Objective**: Develop a robust income prediction model for "Caja de Ahorros" customers to enable better financial product recommendations, risk assessment, and customer segmentation.

**Business Value**:
- Optimize financial product offerings
- Improve customer segmentation and retention
- Reduce credit risk through better income assessment
- Enable data-driven decision making

## 🎯 Key Achievements

### Model Performance
- **Best Model**: XGBoost with nested cross-validation
- **R² Score**: 0.497 ± 0.009 (Cross-validation)
- **Test R² Score**: 0.394 (Unbiased estimate)
- **RMSE**: 490.01 ± 3.49 USD (Cross-validation)
- **MAE**: 344.56 ± 3.10 USD (Cross-validation)

### Technical Highlights
- **Nested Cross-Validation**: Rigorous 5-fold outer, 3-fold inner CV with 1,200 model trainings per algorithm
- **Advanced Feature Engineering**: 20+ engineered features including financial ratios and interaction terms
- **Production Pipeline**: Complete end-to-end pipeline from raw data to predictions
- **Data Consolidation**: Merged 42,549 records into 29,319 unique customers with quality assurance

## 📊 Dataset Information

### Data Sources
- **Primary Dataset**: Info_Cliente.csv (19,047 customers)
- **Secondary Dataset**: Info_Clientes_2.csv (23,502 customers)
- **Final Consolidated**: 29,319 unique customers with 24 features

### Key Features
- **Demographics**: Age, gender, city, country, marital status
- **Employment**: Occupation, employer, position, employment start date
- **Financial**: Account balance, monthly payments, loan amounts, interest rates
- **Behavioral**: Product usage, payment history, account tenure

### Target Variable
- **ingresos_reportados**: Customer reported income (USD)
- **Distribution**: Highly skewed (handled through advanced preprocessing)
- **Range**: $100 - $5,000+ USD

## 🔧 Technical Architecture

### Model Comparison Results
| Model | R² Score | RMSE | MAE | Ranking |
|-------|----------|------|-----|---------|
| **XGBoost** | **0.497 ± 0.009** | **490.01 ± 3.49** | **344.56 ± 3.10** | **🥇 Best** |
| Random Forest | 0.463 ± 0.011 | 506.01 ± 3.98 | 359.77 ± 2.71 | 🥈 Second |
| LightGBM | 0.453 ± 0.010 | 510.82 ± 3.21 | 367.64 ± 3.40 | 🥉 Third |

### Feature Engineering Pipeline
1. **Data Cleaning**: Standardization, missing value imputation
2. **Date Features**: Employment years, account tenure, contract duration
3. **Financial Ratios**: Balance-to-payment ratio, debt burden metrics
4. **Categorical Encoding**: Frequency-based encoding for high-cardinality features
5. **Interaction Features**: Location × occupation, payment per age
6. **Professional Stability**: Custom scoring based on employment history

### Top 10 Most Important Features
1. **ocupacion_consolidated_freq** (5,457) - Occupation frequency encoding
2. **nombreempleadorcliente_consolidated_freq** (3,474) - Employer frequency
3. **edad** (2,692) - Customer age
4. **fechaingresoempleo_days** (2,159) - Employment start date
5. **fecha_inicio_days** (2,002) - Account start date
6. **cargoempleocliente_consolidated_freq** (1,880) - Position frequency
7. **balance_to_payment_ratio** (1,845) - Financial health indicator
8. **professional_stability_score** (1,569) - Employment stability
9. **monto_letra** (1,569) - Monthly payment amount
10. **employment_years** (1,478) - Years of employment

## 🚀 Quick Start

### Prerequisites
```bash
# Create environment
conda create -n income-prediction python=3.9
conda activate income-prediction

# Install dependencies
pip install -r requirements_production_pipeline.txt
```

### Production Pipeline
```bash
# Run complete prediction pipeline
python models/production/00_predictions_pipeline.py
```

### Model Training (Development)
```bash
# Open training notebook
jupyter notebook notebooks/02_00_clean_training_nested_version_IC.ipynb
```

## 📁 Project Structure

```
caja-de-ahorros/
├── data/
│   ├── raw/                    # Original datasets
│   ├── processed/              # Cleaned and engineered features
│   └── production/             # Production-ready data
├── models/
│   └── production/             # Production model and pipeline
├── notebooks/
│   ├── 01_exploratory_data_analysis_real.ipynb
│   └── 02_00_clean_training_nested_version_IC.ipynb
├── archive/                    # Previous iterations and documentation
├── requirements_production_pipeline.txt
└── setup_production_env.bat
```

## 🔬 Methodology

### Nested Cross-Validation Strategy
- **Outer Loop**: 5-fold cross-validation for unbiased performance estimation
- **Inner Loop**: 3-fold cross-validation for hyperparameter optimization
- **Hyperparameter Search**: 80 random search iterations per fold
- **Total Training**: 1,200 models per algorithm (5 × 3 × 80)

### Data Preprocessing
1. **Missing Value Handling**: Forward fill for dates, median imputation for numerical
2. **Feature Scaling**: RobustScaler for outlier resistance
3. **Categorical Encoding**: Frequency-based encoding for interpretability
4. **Feature Selection**: Based on business relevance and statistical importance

### Model Selection Criteria
- **Primary Metric**: RMSE (Root Mean Square Error)
- **Secondary Metrics**: R², MAE, MAPE
- **Validation Strategy**: Nested CV with consistent random states
- **Final Selection**: Best performing model on validation set

## 📈 Business Impact

### Financial Insights
- **Income Prediction Accuracy**: ~$490 average error on $1,300 average income
- **Risk Assessment**: Better identification of low-income segments (<$500)
- **Product Targeting**: Improved customer segmentation capabilities

### Operational Benefits
- **Automated Pipeline**: End-to-end processing from raw data to predictions
- **Scalable Architecture**: Handles batch and individual customer predictions
- **Quality Assurance**: Comprehensive data validation and error handling

## 🛠️ Development History

### Major Milestones
1. **Initial Setup** (Sep 2, 2025): Complete ML infrastructure with FastAPI, Docker, MLOps
2. **Feature Engineering** (Sep 3, 2025): Advanced feature engineering with 40+ interpretable features
3. **Production Pipeline** (Sep 10, 2025): Final nested CV model and production deployment

### Key Improvements
- **Code Organization**: Restructured from 1,600+ chaotic lines to modular pipeline
- **Model Performance**: Improved from R² ≈ 0.31 baseline to 0.497
- **Data Quality**: Consolidated datasets with 54% increase in customer base
- **Production Readiness**: Complete deployment pipeline with minimal dependencies

## 📚 Documentation

- **Technical Documentation**: `archive/old_docs/docs/important_docs/`
- **Model Analysis**: `data/processed/nested_cv_comprehensive_results.json`
- **Feature Importance**: `data/processed/final_production_feature_importance.csv`
- **Data Consolidation**: `data/raw/consolidation_summary.txt`

## 🤝 Contributing

This project follows modern ML engineering practices:
- Modular code organization
- Comprehensive testing and validation
- Production-ready deployment
- Detailed documentation and logging

## 📄 License

Internal project for Caja de Ahorros financial institution.

---

**Last Updated**: September 10, 2025  
**Model Version**: Production v1.0  
**Status**: ✅ Production Ready
