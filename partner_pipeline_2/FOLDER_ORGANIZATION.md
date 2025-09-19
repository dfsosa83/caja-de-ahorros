# 📁 FOLDER ORGANIZATION

This document explains the organized structure of the `partner_pipeline_2` folder.

## 🎯 **MAIN PRODUCTION FILES** (Root Directory)

### **Core Pipeline Components**
- `income_prediction_pipeline.py` - Main orchestrator script
- `production_part1_data_cleaning.py` - Data preprocessing and feature engineering
- `production_part2_model_inference.py` - Model loading and prediction generation

### **Model Files**
- `production_model_catboost_all_data.pkl` - Trained CatBoost model
- `production_frequency_mappings_catboost.pkl` - Frequency encoding mappings

### **Documentation**
- `README.md` - Main documentation
- `START_HERE.txt` - Quick start guide
- `DATA_FORMATS.md` - Input/output format specifications
- `requirements.txt` - Python dependencies

### **Sample Data**
- `example_data.csv` - Sample CSV input
- `example_data.json` - Sample JSON input
- `single_customer.csv` - Single customer example
- `single_customer.json` - Single customer JSON example
- `minimal_test_data.csv` - Minimal data test case

### **Results**
- `feature_combination_results.csv` - Systematic testing results

## 📦 **ARCHIVE FOLDER** (`archive/`)

### **`archive/test_files/`** - Test Scripts
- `test_edge_cases_minimal_data.py` - Edge case testing
- `test_data_quality_scenarios.py` - Data quality testing
- `test_business_scenarios.py` - Business scenario testing
- `test_feature_combinations.py` - Feature combination testing
- `test_unicode_fix.py` - Unicode encoding fix test
- `test_your_case.py` - Specific case testing
- `run_all_tests.py` - Master test runner
- `simple_test.py` - Simple test script
- `fix_unicode.py` - Unicode fix utility
- `test.py` - General test file

### **`archive/test_data/`** - Test Data Files
- `combo_test_*.csv` - Feature combination test data
- `test_*.csv` - Various test datasets
- `temp_*.csv` - Temporary test files

### **`archive/example_files/`** - Example Result Files
- `business_scenario_detailed_results_EXAMPLE.csv`
- `business_scenario_summary_EXAMPLE.csv`
- `data_quality_test_results_EXAMPLE.csv`
- `edge_case_test_results_EXAMPLE.csv`
- `master_test_analysis_EXAMPLE.txt`

### **`archive/old_predictions/`** - Historical Predictions
- `predictions_20250916_*.csv` - Old prediction files
- `predictions_20250916_*.json` - Old prediction JSON files

## 🚀 **QUICK START**

### **For Production Use:**
1. Use files in the **root directory**
2. Run: `python income_prediction_pipeline.py your_data.csv`

### **For Testing/Development:**
1. Check `archive/test_files/` for test scripts
2. Use `archive/test_data/` for sample test cases
3. Reference `archive/example_files/` for expected outputs

### **For Understanding:**
1. Read `README.md` for comprehensive documentation
2. Check `START_HERE.txt` for quick overview
3. Review `DATA_FORMATS.md` for input specifications

## 🧹 **MAINTENANCE**

### **What to Keep in Root:**
- ✅ Production pipeline files
- ✅ Model files (.pkl)
- ✅ Documentation
- ✅ Current sample data
- ✅ Latest results

### **What Goes to Archive:**
- 📦 Test scripts and utilities
- 📦 Test data files
- 📦 Example/template files
- 📦 Old prediction outputs
- 📦 Temporary files

## 📊 **KEY INSIGHTS FROM TESTING**

The systematic testing revealed:
- **100% success rate** across all feature combinations
- **Minimum requirement**: Just 1 feature (even age alone works!)
- **Your case (Age 44 + 'OTROS')**: Predicts $1,815.80
- **Most robust combination**: Age + Payment amount
- **Pipeline handles missing data gracefully**

---

*Last organized: 2025-09-19*
*Archive contains comprehensive test suite demonstrating pipeline robustness*
