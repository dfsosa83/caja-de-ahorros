# 🚀 SETUP GUIDE - Income Prediction Pipeline

## 📦 Complete Package Contents

Your partner pipeline package contains:

```
partner_pipeline/
├── 📋 DOCUMENTATION
│   ├── README.md                                    ✅ Usage instructions
│   ├── SETUP_GUIDE.md                              ✅ This setup guide
│   └── requirements.txt                            ✅ Python dependencies
│
├── 🐍 PYTHON FILES
│   ├── income_prediction_pipeline.py               ✅ Main pipeline
│   ├── production_part1_data_cleaning.py           ✅ Data cleaning module
│   ├── production_part2_model_inference.py         ✅ Model inference module
│   └── example_usage.py                            ✅ Usage examples
│
├── 🤖 MODEL FILES
│   ├── production_model_catboost_all_data.pkl      ✅ Trained model
│   └── production_frequency_mappings_catboost.pkl  ✅ Frequency mappings
│
└── 📊 TEST DATA
    └── test_data.csv                               ✅ Sample data for testing
```

## ⚡ Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Test the Pipeline
```bash
python income_prediction_pipeline.py test_data.csv
```

### Step 3: Use with Your Data
```bash
python income_prediction_pipeline.py your_data.csv
```

## 📊 Expected Output Format

The pipeline produces predictions in this exact format:
```
📊 PREDICTION RESULTS:
==================================================
identificador_unico  cliente  predicted_income  income_lower_90  income_upper_90
          9-706-693     3642       1858.930054           1348.0      2613.949951
          8-904-143     1234       1245.670000            734.7      2000.669951
          8-398-877     5678       2100.450000           1589.5      2855.449951

📈 Summary:
   👥 Total customers: 3
   💰 Average income: $1,734.68
   📊 Income range: $1,245.67 - $2,100.45

💾 Results saved to: predictions_20250916_102030.csv
```

## 📁 Input Data Requirements

Your CSV file must contain these columns:
- `Cliente` or `cliente` - Customer ID
- `Identificador_Unico` - Unique identifier  
- `Edad` - Age
- `Ocupacion` - Occupation
- `NombreEmpleadorCliente` - Employer name
- `CargoEmpleoCliente` - Job title (can have NULL values)
- `FechaIngresoEmpleo` - Employment start date (can have NULL values)
- `saldo` - Account balance
- `monto_letra` - Monthly payment (can have NULL values)
- `fecha_inicio` - Account start date

## 🔧 Customization

### Update Model Paths
If you have your own model files, edit `income_prediction_pipeline.py`:
```python
class PipelineConfig:
    MODEL_FILES = {
        "trained_model": "your_model_file.pkl",
        "frequency_mappings": "your_mappings_file.pkl",
    }
```

### Confidence Intervals
To adjust confidence intervals, modify:
```python
MODEL_CONFIG = {
    "confidence_level": 0.90,
    "ci_lower_offset": -510.93,  # Adjust these values
    "ci_upper_offset": 755.02,   # based on your model
}
```

## 🚨 Troubleshooting

### Common Issues:

**"ModuleNotFoundError: No module named 'pandas'"**
```bash
pip install pandas numpy catboost scikit-learn
```

**"Model file not found"**
- Ensure `.pkl` files are in the same directory as the Python scripts
- Check file names match exactly

**"Input file not found"**
- Use absolute path: `python income_prediction_pipeline.py C:\path\to\your\data.csv`
- Verify CSV file exists

**"Data cleaning failed"**
- Check your CSV has all required columns
- Verify column names match exactly (case-sensitive)

## 📞 Support

For technical issues:
1. Check all files are in the same directory
2. Verify Python environment has required packages
3. Test with provided `test_data.csv` first
4. Check input data format matches requirements

## 🎯 Success Criteria

Your setup is successful when:
- ✅ Pipeline runs without errors
- ✅ Predictions are displayed in the correct format
- ✅ Output CSV file is created
- ✅ All customers have predicted income values

**🎉 You're ready to predict incomes!**
