# 📊 Data Formats Guide

## 🎯 Supported Input Formats

The Income Prediction Pipeline supports **2 input formats**:

### 1. 📄 CSV Format
- **File extension**: `.csv`
- **Encoding**: UTF-8
- **Separator**: Comma (`,`)
- **Example**: `customer_data.csv`

### 2. 📄 JSON Format  
- **File extension**: `.json`
- **Encoding**: UTF-8
- **Structure**: Array of objects
- **Example**: `customer_data.json`

---

## 📋 Required Data Fields

Your input file **must contain** these 10 columns:

| **Field Name** | **Type** | **Description** | **Example** |
|----------------|----------|-----------------|-------------|
| `Cliente` | Integer | Customer ID | `3642` |
| `Identificador_Unico` | String | Unique identifier | `"9-706-693"` |
| `Edad` | Integer | Customer age (18-85) | `67` |
| `Ocupacion` | String | Job category | `"JUBILADO"` |
| `NombreEmpleadorCliente` | String | Employer name | `"CAJA DE SEGURO SOCIAL"` |
| `CargoEmpleoCliente` | String | Job position | `"JUBILADO"` |
| `FechaIngresoEmpleo` | String | Employment start date | `"2010-05-15"` |
| `saldo` | Float | Account balance | `15000.50` |
| `monto_letra` | Float | Monthly payment (can be null) | `450.75` |
| `fecha_inicio` | String | Account start date | `"2020-01-10"` |

---

## 📅 Date Format Support

The pipeline supports **multiple date formats**:

- **ISO Format**: `"2010-05-15"` (YYYY-MM-DD) ✅ **Recommended**
- **European Format**: `"15/05/2010"` (DD/MM/YYYY) ✅
- **Auto-detect**: Most common formats ✅

---

## 💡 Data Quality Tips

### ✅ **Good Practices:**
- Use **ISO date format** (`YYYY-MM-DD`) for best compatibility
- Include all required fields
- Use consistent data types
- Handle missing values as `null` (JSON) or empty (CSV)

### ⚠️ **Common Issues:**
- Missing required columns
- Invalid date formats
- Text in numeric fields
- Special characters in names

---

## 📁 Example Files

### 📄 CSV Example (`example_data.csv`)
```csv
Cliente,Identificador_Unico,Edad,Ocupacion,NombreEmpleadorCliente,CargoEmpleoCliente,FechaIngresoEmpleo,saldo,monto_letra,fecha_inicio
3642,9-706-693,67,JUBILADO,CAJA DE SEGURO SOCIAL,JUBILADO,2010-05-15,15000.50,450.75,2020-01-10
10547,8-904-143,45,POLICIA,POLICIA NACIONAL,POLICIA,2015-03-20,8500.25,320.00,2018-06-05
```

### 📄 JSON Example (`example_data.json`)
```json
[
  {
    "Cliente": 3642,
    "Identificador_Unico": "9-706-693",
    "Edad": 67,
    "Ocupacion": "JUBILADO",
    "NombreEmpleadorCliente": "CAJA DE SEGURO SOCIAL",
    "CargoEmpleoCliente": "JUBILADO",
    "FechaIngresoEmpleo": "2010-05-15",
    "saldo": 15000.50,
    "monto_letra": 450.75,
    "fecha_inicio": "2020-01-10"
  },
  {
    "Cliente": 10547,
    "Identificador_Unico": "8-904-143",
    "Edad": 45,
    "Ocupacion": "POLICIA",
    "NombreEmpleadorCliente": "POLICIA NACIONAL",
    "CargoEmpleoCliente": "POLICIA",
    "FechaIngresoEmpleo": "2015-03-20",
    "saldo": 8500.25,
    "monto_letra": 320.00,
    "fecha_inicio": "2018-06-05"
  }
]
```

---

## 🚀 Usage Examples

### CSV Input:
```bash
python income_prediction_pipeline.py customer_data.csv
```

### JSON Input:
```bash
python income_prediction_pipeline.py customer_data.json
```

---

## 📊 Output Formats

The pipeline automatically generates:

1. **📺 Screen Output**: Clean prediction results
2. **📄 CSV File**: `predictions_YYYYMMDD_HHMMSS.csv`
3. **📄 JSON File**: `predictions_YYYYMMDD_HHMMSS.json`

---

## 🔧 Troubleshooting

### **"Missing required features"**
- Check all 10 required columns are present
- Verify column names match exactly (case-sensitive)

### **"Date conversion failed"**
- Use ISO format: `YYYY-MM-DD`
- Check for invalid dates

### **"Model prediction failed"**
- Ensure all `.pkl` files are in the same folder
- Check data types are correct

---

## 📞 Quick Reference

**✅ Ready to use?**
1. Prepare your data in CSV or JSON format
2. Include all 10 required fields
3. Run: `python income_prediction_pipeline.py your_data.csv`
4. Get predictions instantly!
