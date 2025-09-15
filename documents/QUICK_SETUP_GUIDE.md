# 🚀 QUICK SETUP GUIDE - Income Prediction Pipeline

## 📋 **5-MINUTE SETUP CHECKLIST**

### **✅ STEP 1: VERIFY FILES ARE IN PLACE**

Make sure you have these files in your project directory:
```
your-project/
├── production_pipeline_complete.py          ✅ Main pipeline
├── production_part1_data_cleaning.py        ✅ Part 1: Data cleaning
├── production_part2_model_inference.py      ✅ Part 2: Model inference  
├── production_part3_business_formatting.py  ✅ Part 3: Business formatting
├── production_incremental_predictions.py    ✅ Incremental storage
├── data/production/final_info_clientes.csv  ✅ Your customer data
└── models/production/
    ├── production_model_catboost_all_data.pkl           ✅ Trained model
    └── production_frequency_mappings_catboost.pkl       ✅ Frequency mappings
```

### **✅ STEP 2: UPDATE CONFIGURATION (2 MINUTES)**

Open `production_pipeline_complete.py` and update **lines 53-73**:

```python
class ProductionConfig:
    # 📁 UPDATE THIS PATH to your project root
    BASE_PATH = r"C:\Users\david\OneDrive\Documents\augment-projects\caja-de-ahorros"  # ← CHANGE THIS
    
    # 📂 INPUT FILES - Update if your data file has different name/location
    INPUT_FILES = {
        "raw_customer_data": os.path.join(BASE_PATH, "data", "production", "final_info_clientes.csv"),
        # ↑ CHANGE if your customer data file has different name
    }
    
    # 🤖 MODEL FILES - Update if your model files are in different location
    MODEL_FILES = {
        "trained_model": os.path.join(BASE_PATH, "models", "production", "production_model_catboost_all_data.pkl"),
        "frequency_mappings": os.path.join(BASE_PATH, "models", "production", "production_frequency_mappings_catboost.pkl"),
        # ↑ CHANGE if your model files are in different location
    }
    
    # 📁 OUTPUT FOLDERS - Update if you want different output location
    OUTPUT_FOLDERS = {
        "predictions": os.path.join(BASE_PATH, "model_pred_files"),  # ← Main output folder
        "temp_data": os.path.join(BASE_PATH, "data", "temp"),        # ← Temporary files
    }
```

### **✅ STEP 3: TEST RUN (1 MINUTE)**

Open command prompt/terminal in your project directory and run:

```bash
# Test the pipeline
python production_pipeline_complete.py
```

**Expected output:**
```
🎯 COMPLETE END-TO-END PRODUCTION PIPELINE
================================================================================
🔧 Income Prediction System - XGBoost Model
📋 Pipeline: Raw Data → Features → Predictions → Master Dataset
================================================================================

[2025-09-14 11:30:00] 🔍 VALIDATING FILE PATHS AND DEPENDENCIES
[2025-09-14 11:30:00] ✅ raw_customer_data: data/production/final_info_clientes.csv
[2025-09-14 11:30:00] ✅ trained_model: models/production/production_model_catboost_all_data.pkl
[2025-09-14 11:30:01] ✅ All file paths validated successfully

[2025-09-14 11:30:01] 🚀 PART 1: DATA CLEANING & FEATURE ENGINEERING
[2025-09-14 11:30:05] ✅ Part 1 completed: (31125, 13)

[2025-09-14 11:30:05] 🚀 PART 2: MODEL INFERENCE & PREDICTIONS
[2025-09-14 11:30:15] ✅ Part 2 completed: (31125, 15)

[2025-09-14 11:30:15] 🚀 PART 3: BUSINESS FORMATTING & INCREMENTAL STORAGE
[2025-09-14 11:30:20] ✅ Part 3 completed: Incremental storage successful

[2025-09-14 11:30:20] 🎉 COMPLETE PIPELINE SUCCESS!
```

### **✅ STEP 4: VERIFY OUTPUT (30 SECONDS)**

Check that these files were created:
```
model_pred_files/
├── master_predictions.csv          ✅ Main dataset (CSV)
├── master_predictions.json         ✅ Main dataset (JSON)
└── pipeline_log_20250914.txt       ✅ Execution log
```

### **✅ STEP 5: CHECK STATUS (30 SECONDS)**

```bash
# Check pipeline status
python production_pipeline_complete.py status
```

**Expected output:**
```
📊 PIPELINE STATUS CHECK
==================================================
✅ Master dataset exists: 31,125 predictions
🆔 Unique customers: 31,125
📅 Date range: 2025-09-14 11:30:20 to 2025-09-14 11:30:20
💾 File size: 2.5 MB
```

---

## 🔧 **TROUBLESHOOTING COMMON ISSUES**

### **❌ "File not found" Error**
```
❌ raw_customer_data: data/production/final_info_clientes.csv (NOT FOUND)
```
**Solution:** Update the file path in `ProductionConfig.INPUT_FILES`

### **❌ "Cannot import" Error**
```
❌ Part 1 failed: Cannot import production_part1_data_cleaning.py
```
**Solution:** Make sure all pipeline files are in the same directory

### **❌ "Model loading failed" Error**
```
❌ Part 2 failed: Model loading failed
```
**Solution:** 
1. Check model file exists
2. Verify XGBoost is installed: `pip install xgboost`
3. Update model path in `ProductionConfig.MODEL_FILES`

### **❌ Permission Error**
```
❌ Error saving files: Permission denied
```
**Solution:** 
1. Run as administrator (Windows) or with sudo (Linux/Mac)
2. Change output folder to a location you have write access

---

## 🎯 **DAILY USAGE**

### **Regular Production Run:**
```bash
# Run daily predictions
python production_pipeline_complete.py
```

### **Check Current Status:**
```bash
# Check master dataset status
python production_pipeline_complete.py status
```

### **Programmatic Usage:**
```python
from production_pipeline_complete import run_complete_pipeline

# Run pipeline
results = run_complete_pipeline()

if results:
    print(f"Processed {results['execution_summary']['customers_processed']} customers")
    print(f"Processing time: {results['execution_summary']['processing_time_seconds']} seconds")
```

---

## 📊 **UNDERSTANDING THE OUTPUT**

### **master_predictions.csv** - Main business file
| identificador_unico | predicted_income | income_segment | business_priority | prediction_date |
|---------------------|------------------|----------------|-------------------|-----------------|
| CUST_12345 | 1850.50 | MIDDLE_INCOME_GROWTH | HIGH_PRIORITY | 2025-09-14 11:30:20 |

### **master_predictions.json** - Structured data for systems
```json
{
  "dataset_metadata": {
    "total_predictions": 31125,
    "unique_customers": 31125,
    "last_updated": "2025-09-14 11:30:20"
  },
  "business_summary": {
    "income_segments": {"MIDDLE_INCOME_STABLE": 12000, "HIGH_INCOME_STABLE": 8000},
    "business_priorities": {"HIGH_PRIORITY": 15000, "PREMIUM_PRIORITY": 5000}
  }
}
```

---

## 🔄 **INCREMENTAL PROCESSING**

The pipeline automatically handles incremental updates:

- **First run:** Creates master dataset with all predictions
- **Subsequent runs:** Adds new predictions to existing dataset
- **Same customer + same date:** Replaces old prediction with new one
- **Old predictions:** Automatically archived after 90 days (configurable)

---

## 📞 **SUPPORT**

### **Configuration Issues:**
1. Check file paths in `ProductionConfig` class
2. Verify all required files exist
3. Review error logs in `model_pred_files/pipeline_log_YYYYMMDD.txt`

### **Performance Issues:**
1. Adjust `batch_size` in `PROCESSING_CONFIG`
2. Increase `archive_days` if dataset grows too large
3. Monitor disk space in output folders

### **Business Questions:**
1. Review business classifications in master dataset
2. Check income segments and priorities
3. Analyze prediction confidence levels

---

## ✅ **SUCCESS CRITERIA**

Your setup is successful when:
- ✅ Pipeline runs without errors
- ✅ `master_predictions.csv` is created with your data
- ✅ Log file shows "COMPLETE PIPELINE SUCCESS!"
- ✅ Status command shows dataset information
- ✅ Business teams can open CSV file in Excel

**🎉 You're ready for production!**
