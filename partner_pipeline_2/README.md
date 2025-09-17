# 💰 Income Prediction Pipeline

## 🚀 Quick Start (2 minutes)

### Step 1: Install Python packages
```bash
pip install pandas numpy catboost scikit-learn
```

### Step 2: Run prediction
```bash
python income_prediction_pipeline.py your_data.csv
```

### Step 3: Get results
- View predictions on screen
- Find saved file: `predictions_YYYYMMDD_HHMMSS.csv`

## 📊 Example

```bash
python income_prediction_pipeline.py test_data.csv
```

**Output:**
```
📊 PREDICTION RESULTS:
==================================================
identificador_unico  cliente  predicted_income  income_lower_90  income_upper_90
          9-706-693     3642       1858.930054      1348.000000      2613.949951
          8-904-143    10547       1924.699951      1413.770020      2679.719971

📈 Summary:
   👥 Total customers: 25
   💰 Average income: $1,824.55
   📊 Income range: $1,660.79 - $1,924.70
💾 Saved: predictions_20250916_105000.csv
```

## 📁 Required Data Format

Your CSV file needs these columns:
- `Cliente` - Customer ID
- `Identificador_Unico` - Unique identifier
- `Edad` - Age
- `Ocupacion` - Occupation
- `NombreEmpleadorCliente` - Employer name
- `CargoEmpleoCliente` - Job title
- `FechaIngresoEmpleo` - Employment start date
- `saldo` - Account balance
- `monto_letra` - Monthly payment
- `fecha_inicio` - Account start date

## 🔧 Troubleshooting

**"ModuleNotFoundError"**
```bash
pip install pandas numpy catboost scikit-learn
```

**"File not found"**
- Check CSV file path is correct
- Use full path: `python income_prediction_pipeline.py C:\path\to\data.csv`

**"Model file not found"**
- Ensure all `.pkl` files are in same folder as Python scripts

## 📞 That's it!

Just run: `python income_prediction_pipeline.py your_data.csv`
