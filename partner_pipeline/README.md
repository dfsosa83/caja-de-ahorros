# 🚀 Income Prediction Pipeline - Standalone Version

## 📋 Quick Start

### Required Files
Place these files in the same directory:
```
partner_pipeline/
├── income_prediction_pipeline.py           ✅ Main pipeline
├── production_part1_data_cleaning.py       ✅ Data cleaning
├── production_part2_model_inference.py     ✅ Model inference
├── production_model_catboost_all_data.pkl  ✅ Your trained model
├── production_frequency_mappings_catboost.pkl ✅ Your frequency mappings
└── your_data.csv                           ✅ Your customer data
```

### Usage
```bash
python income_prediction_pipeline.py your_data.csv
```

### Example
```bash
python income_prediction_pipeline.py customer_data.csv
```

### Verbose Mode (Optional)
```bash
python income_prediction_pipeline.py customer_data.csv --verbose
```

## 📊 Expected Output

The pipeline will display predictions in this format:
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

## 📁 Input Data Format

Your CSV file should contain these columns:
- `Cliente` or `cliente` - Customer ID
- `Identificador_Unico` - Unique identifier
- `Edad` - Age
- `Ocupacion` - Occupation
- `NombreEmpleadorCliente` - Employer name
- `CargoEmpleoCliente` - Job title
- `FechaIngresoEmpleo` - Employment start date
- `saldo` - Account balance
- `monto_letra` - Monthly payment
- `fecha_inicio` - Account start date

## 🔧 Configuration

To update model file paths, edit `income_prediction_pipeline.py`:
```python
class PipelineConfig:
    MODEL_FILES = {
        "trained_model": "your_model_file.pkl",
        "frequency_mappings": "your_mappings_file.pkl",
    }
```

## 📊 Output Columns

- `identificador_unico` - Customer unique ID
- `cliente` - Customer ID
- `predicted_income` - Predicted monthly income
- `income_lower_90` - Lower bound (90% confidence)
- `income_upper_90` - Upper bound (90% confidence)

## 🚨 Troubleshooting

### "Model file not found"
- Ensure `.pkl` files are in the same directory
- Check file names match exactly

### "Input file not found"
- Verify CSV file path is correct
- Use absolute path if needed

### "Data cleaning failed"
- Check input CSV has required columns
- Verify data format matches expected structure

## 📞 Support

For issues:
1. Check all required files are present
2. Verify input data format
3. Ensure Python environment has required packages:
   - pandas
   - numpy
   - catboost (or xgboost)
   - scikit-learn
