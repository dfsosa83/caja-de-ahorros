# =============================================================================
# COMPLETE END-TO-END PRODUCTION PIPELINE
# Income Prediction System - XGBoost Model
# =============================================================================
#
# OBJECTIVE: Complete pipeline from raw data to incremental prediction storage
#
# PIPELINE FLOW:
# Raw Data → Part 1 (Cleaning) → Part 2 (Predictions) → Part 3 (Incremental Storage)
#
# FEATURES:
# - Configurable file paths for easy team modifications
# - Complete error handling and logging
# - Incremental prediction storage (single master dataset)
# - Business-ready output with risk classifications
# - Production-ready with comprehensive documentation
#
# USAGE:
# python production_pipeline_complete.py
# 
# OR programmatically:
# from production_pipeline_complete import run_complete_pipeline
# results = run_complete_pipeline()
# =============================================================================

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 🔧 CONFIGURATION SECTION - MODIFY PATHS HERE
# =============================================================================
# 
# ⚠️  TEAM NOTE: Update these paths for your environment
# All file paths are configured here for easy modification
#
class ProductionConfig:
    """
    Production pipeline configuration
    
    🔧 TEAM MODIFICATION GUIDE:
    - Update BASE_PATH to your project root directory
    - Modify file paths in INPUT_FILES, MODEL_FILES, OUTPUT_FOLDERS
    - Change model parameters in MODEL_CONFIG if needed
    - Adjust PROCESSING_CONFIG for your business requirements
    """
    
    # 📁 BASE PATHS - Updated for production_test directory
    BASE_PATH = r"C:\Users\david\OneDrive\Documents\augment-projects\caja-de-ahorros"  # Absolute path to project root

    # 📂 INPUT FILES - Raw data location
    INPUT_FILES = {
        "raw_customer_data": os.path.join(BASE_PATH, "data", "production", "final_info_clientes.csv"),
        # 🔧 TEAM NOTE: This will be overridden by test framework
    }

    # 🤖 MODEL FILES - Trained model and mappings (from main models/production directory)
    MODEL_FILES = {
        "trained_model": os.path.join(BASE_PATH, "models", "production", "production_model_catboost_all_data.pkl"),
        "frequency_mappings": os.path.join(BASE_PATH, "models", "production", "production_frequency_mappings_catboost.pkl"),
        # 🔧 TEAM NOTE: Using model files from main models/production directory
    }

    # 📁 OUTPUT FOLDERS - Where results are saved
    OUTPUT_FOLDERS = {
        "predictions": os.path.join(BASE_PATH, "model_pred_files"),
        "temp_data": os.path.join(BASE_PATH, "data", "temp"),
        # 🔧 TEAM NOTE: Output to main project directories
    }
    
    # ⚙️ MODEL CONFIGURATION
    MODEL_CONFIG = {
        "confidence_level": 0.90,
        "ci_lower_offset": -510.93,  # From final model analysis
        "ci_upper_offset": 755.02,   # From final model analysis
        "model_version": "XGBoost_v1.0_Final",
        # 🔧 TEAM NOTE: Update these values if you retrain the model
    }
    
    # 📊 PROCESSING CONFIGURATION
    PROCESSING_CONFIG = {
        "archive_days": 90,  # Days to keep in master dataset
        "batch_size": 10000,  # Maximum records to process at once
        "enable_logging": True,
        # 🔧 TEAM NOTE: Adjust these settings for your business needs
    }

# =============================================================================
# 📝 LOGGING SETUP
# =============================================================================

def setup_logging():
    """Setup simple logging for production pipeline"""
    if ProductionConfig.PROCESSING_CONFIG["enable_logging"]:
        log_folder = ProductionConfig.OUTPUT_FOLDERS["predictions"]
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        
        log_file = os.path.join(log_folder, f"pipeline_log_{datetime.now().strftime('%Y%m%d')}.txt")
        
        def log_message(message):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"[{timestamp}] {message}"
            print(log_entry)
            try:
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(log_entry + '\n')
            except:
                pass  # Continue if logging fails
        
        return log_message
    else:
        return print

# =============================================================================
# 🔧 UTILITY FUNCTIONS
# =============================================================================

def validate_file_paths():
    """
    Validate that all required files and folders exist
    """
    log = setup_logging()
    log("🔍 VALIDATING FILE PATHS AND DEPENDENCIES")
    log("="*60)
    
    # Check input files
    missing_files = []
    for file_type, file_path in ProductionConfig.INPUT_FILES.items():
        if os.path.exists(file_path):
            log(f"✅ {file_type}: {file_path}")
        else:
            log(f"❌ {file_type}: {file_path} (NOT FOUND)")
            missing_files.append(f"{file_type}: {file_path}")
    
    # Check model files
    for file_type, file_path in ProductionConfig.MODEL_FILES.items():
        if os.path.exists(file_path):
            log(f"✅ {file_type}: {file_path}")
        else:
            log(f"❌ {file_type}: {file_path} (NOT FOUND)")
            missing_files.append(f"{file_type}: {file_path}")
    
    # Create output folders if they don't exist
    for folder_type, folder_path in ProductionConfig.OUTPUT_FOLDERS.items():
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            log(f"📁 Created {folder_type}: {folder_path}")
        else:
            log(f"✅ {folder_type}: {folder_path}")
    
    if missing_files:
        log("🚨 MISSING FILES DETECTED:")
        for missing in missing_files:
            log(f"   ❌ {missing}")
        log("\n🔧 TEAM ACTION REQUIRED:")
        log("   1. Update paths in ProductionConfig class")
        log("   2. Ensure all model files are in correct locations")
        log("   3. Verify input data file exists")
        return False
    
    log("✅ All file paths validated successfully")
    return True

def create_temp_files():
    """Create temporary file paths for pipeline stages"""
    temp_folder = ProductionConfig.OUTPUT_FOLDERS["temp_data"]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return {
        "clean_data": os.path.join(temp_folder, f"clean_data_{timestamp}.csv"),
        "predictions": os.path.join(temp_folder, f"predictions_{timestamp}.csv")
    }

# =============================================================================
# 🚀 MAIN PIPELINE FUNCTIONS
# =============================================================================

def run_part1_data_cleaning(input_file, output_file):
    """
    Part 1: Data Cleaning & Feature Engineering
    """
    log = setup_logging()
    log("\n🚀 PART 1: DATA CLEANING & FEATURE ENGINEERING")
    log("="*60)
    
    try:
        # Import Part 1 functions
        from production_part1_data_cleaning import production_part1_main
        
        # Run data cleaning
        df_clean = production_part1_main(input_file, output_file)
        
        if df_clean is not None:
            log(f"✅ Part 1 completed: {df_clean.shape}")
            return df_clean, True
        else:
            log("❌ Part 1 failed: Data cleaning returned None")
            return None, False
            
    except ImportError as e:
        log(f"❌ Part 1 failed: Cannot import production_part1_data_cleaning.py")
        log(f"   Error: {e}")
        log("🔧 TEAM ACTION: Ensure production_part1_data_cleaning.py is in the same directory")
        return None, False
    except Exception as e:
        log(f"❌ Part 1 failed: {e}")
        return None, False

def run_part2_model_inference(clean_data_file, output_file):
    """
    Part 2: Model Inference & Predictions
    """
    log = setup_logging()
    log("\n🚀 PART 2: MODEL INFERENCE & PREDICTIONS")
    log("="*60)
    
    try:
        # Import Part 2 functions
        from production_part2_model_inference import production_part2_main
        
        # Run model inference
        df_predictions = production_part2_main(clean_data_file, output_file)
        
        if df_predictions is not None:
            log(f"✅ Part 2 completed: {df_predictions.shape}")
            return df_predictions, True
        else:
            log("❌ Part 2 failed: Model inference returned None")
            return None, False
            
    except ImportError as e:
        log(f"❌ Part 2 failed: Cannot import production_part2_model_inference.py")
        log(f"   Error: {e}")
        log("🔧 TEAM ACTION: Ensure production_part2_model_inference.py is in the same directory")
        return None, False
    except Exception as e:
        log(f"❌ Part 2 failed: {e}")
        return None, False

def run_part3_incremental_storage(df_predictions):
    """
    Part 3: Business Formatting & Incremental Storage
    """
    log = setup_logging()
    log("\n🚀 PART 3: BUSINESS FORMATTING & INCREMENTAL STORAGE")
    log("="*60)
    
    try:
        # Import Part 3 functions
        from production_part3_business_formatting import classify_income_risk_segments
        from production_incremental_predictions import process_new_predictions_incremental
        
        # Add business classifications
        df_business = classify_income_risk_segments(df_predictions)
        
        # Process incrementally
        results = process_new_predictions_incremental(
            df_business, 
            cleanup_days=ProductionConfig.PROCESSING_CONFIG["archive_days"]
        )
        
        if results is not None:
            log(f"✅ Part 3 completed: Incremental storage successful")
            return results, True
        else:
            log("❌ Part 3 failed: Incremental storage returned None")
            return None, False
            
    except ImportError as e:
        log(f"❌ Part 3 failed: Cannot import required modules")
        log(f"   Error: {e}")
        log("🔧 TEAM ACTION: Ensure all pipeline modules are in the same directory")
        return None, False
    except Exception as e:
        log(f"❌ Part 3 failed: {e}")
        return None, False

def run_complete_pipeline():
    """
    🚀 MAIN FUNCTION: Complete End-to-End Production Pipeline

    Executes all three parts of the pipeline:
    1. Data Cleaning & Feature Engineering
    2. Model Inference & Predictions
    3. Business Formatting & Incremental Storage

    Returns:
        dict: Complete pipeline results and statistics
    """
    log = setup_logging()
    log("🚀 COMPLETE END-TO-END PRODUCTION PIPELINE")
    log("="*80)
    log("🎯 OBJECTIVE: Raw data → Clean features → Predictions → Master dataset")
    log("📋 PIPELINE: Part 1 → Part 2 → Part 3 → Complete")
    log("="*80)

    pipeline_start_time = datetime.now()

    # Step 0: Validate environment
    log("\n📋 STEP 0: ENVIRONMENT VALIDATION")
    if not validate_file_paths():
        log("❌ Pipeline aborted: Environment validation failed")
        return None

    # Create temporary files
    temp_files = create_temp_files()

    try:
        # Step 1: Data Cleaning & Feature Engineering
        log("\n📋 STEP 1: DATA CLEANING & FEATURE ENGINEERING")
        df_clean, part1_success = run_part1_data_cleaning(
            ProductionConfig.INPUT_FILES["raw_customer_data"],
            temp_files["clean_data"]
        )

        if not part1_success:
            log("❌ Pipeline aborted: Part 1 failed")
            return None

        # Step 2: Model Inference & Predictions
        log("\n📋 STEP 2: MODEL INFERENCE & PREDICTIONS")
        df_predictions, part2_success = run_part2_model_inference(
            temp_files["clean_data"],
            temp_files["predictions"]
        )

        if not part2_success:
            log("❌ Pipeline aborted: Part 2 failed")
            return None

        # Step 3: Business Formatting & Incremental Storage
        log("\n📋 STEP 3: BUSINESS FORMATTING & INCREMENTAL STORAGE")
        incremental_results, part3_success = run_part3_incremental_storage(df_predictions)

        if not part3_success:
            log("❌ Pipeline aborted: Part 3 failed")
            return None

        # Pipeline completion
        pipeline_end_time = datetime.now()
        processing_time = (pipeline_end_time - pipeline_start_time).total_seconds()

        # Compile final results
        final_results = {
            "pipeline_status": "SUCCESS",
            "execution_summary": {
                "start_time": pipeline_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": pipeline_end_time.strftime('%Y-%m-%d %H:%M:%S'),
                "processing_time_seconds": round(processing_time, 2),
                "customers_processed": len(df_predictions),
                "pipeline_version": "v1.0_Complete"
            },
            "data_flow": {
                "input_file": ProductionConfig.INPUT_FILES["raw_customer_data"],
                "clean_data_shape": df_clean.shape,
                "predictions_generated": len(df_predictions),
                "master_dataset_location": os.path.join(ProductionConfig.OUTPUT_FOLDERS["predictions"], "master_predictions.csv")
            },
            "business_results": incremental_results["business_insights"],
            "file_locations": {
                "master_csv": os.path.join(ProductionConfig.OUTPUT_FOLDERS["predictions"], "master_predictions.csv"),
                "master_json": os.path.join(ProductionConfig.OUTPUT_FOLDERS["predictions"], "master_predictions.json"),
                "archive_folder": os.path.join(ProductionConfig.OUTPUT_FOLDERS["predictions"], "archive"),
                "log_file": os.path.join(ProductionConfig.OUTPUT_FOLDERS["predictions"], f"pipeline_log_{datetime.now().strftime('%Y%m%d')}.txt")
            }
        }

        # Success summary
        log("\n🎉 COMPLETE PIPELINE SUCCESS!")
        log("="*60)
        log(f"⏱️  Processing time: {processing_time:.2f} seconds")
        log(f"👥 Customers processed: {len(df_predictions):,}")
        log(f"💰 Average predicted income: ${incremental_results['business_insights']['average_predicted_income']:,.2f}")
        log(f"📊 Total predictions in master: {incremental_results['processing_summary']['total_predictions_in_master']:,}")
        log(f"🆔 Unique customers: {incremental_results['processing_summary']['unique_customers']:,}")

        log("\n📂 OUTPUT FILES:")
        log(f"   📄 master_predictions.csv")
        log(f"   📄 master_predictions.json")
        log(f"   📁 archive/ (for old predictions)")
        log(f"   📝 pipeline_log_{datetime.now().strftime('%Y%m%d')}.txt")

        log("\n🎯 PIPELINE COMPLETED SUCCESSFULLY!")
        log("   Ready for business use and system integration")

        return final_results

    except Exception as e:
        log(f"\n❌ PIPELINE FAILED: Unexpected error")
        log(f"   Error: {e}")
        log("🔧 TEAM ACTION: Check error details and configuration")
        return None

    finally:
        # Cleanup temporary files
        log("\n🧹 CLEANING UP TEMPORARY FILES")
        for temp_file in temp_files.values():
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    log(f"🗑️  Removed: {os.path.basename(temp_file)}")
            except:
                pass  # Continue if cleanup fails

# =============================================================================
# 📋 USAGE EXAMPLES AND DOCUMENTATION
# =============================================================================

def run_single_customer_test():
    """
    🧪 TEST FUNCTION: Run pipeline with single customer

    Tests the complete pipeline with just one customer to verify:
    - Data cleaning works for single record
    - Model inference works for single prediction
    - Incremental storage works for single customer
    - All file outputs are created correctly
    """
    log = setup_logging()
    log("🧪 SINGLE CUSTOMER PIPELINE TEST")
    log("="*80)
    log("🎯 OBJECTIVE: Test pipeline with first customer (9-706-693)")
    log("📋 CUSTOMER: 3642 - JARDINERO - Age 47")
    log("="*80)

    # Create single customer test file
    single_customer_file = os.path.join(ProductionConfig.BASE_PATH, "data", "production", "single_customer_test.csv")

    # Create single customer test data (first customer from main dataset)
    import pandas as pd
    df_full = pd.read_csv(ProductionConfig.INPUT_FILES["raw_customer_data"], encoding='utf-8')
    df_single = df_full.head(1)  # Take first customer
    df_single.to_csv(single_customer_file, index=False, encoding='utf-8')
    log(f"📝 Created single customer test file: {single_customer_file}")

    # Temporarily change input file to single customer
    original_input = ProductionConfig.INPUT_FILES["raw_customer_data"]
    ProductionConfig.INPUT_FILES["raw_customer_data"] = single_customer_file

    try:
        # Run complete pipeline with single customer
        results = run_complete_pipeline()

        if results:
            log("\n🎉 SINGLE CUSTOMER TEST RESULTS:")
            log(f"   ✅ Status: {results['pipeline_status']}")
            log(f"   ✅ Processing time: {results['execution_summary']['processing_time_seconds']} seconds")
            log(f"   ✅ Customers processed: {results['execution_summary']['customers_processed']}")
            log(f"   ✅ Expected: 1 customer")

            if results['execution_summary']['customers_processed'] == 1:
                log("   🎯 SINGLE CUSTOMER TEST: PASSED")
            else:
                log("   ⚠️ SINGLE CUSTOMER TEST: UNEXPECTED COUNT")

        return results

    finally:
        # Restore original input file
        ProductionConfig.INPUT_FILES["raw_customer_data"] = original_input
        log(f"\n🔄 Restored original input file: {original_input}")

        # Clean up single customer test file
        try:
            if os.path.exists(single_customer_file):
                os.remove(single_customer_file)
                log(f"🗑️ Cleaned up test file: {single_customer_file}")
        except:
            pass

def run_pipeline_with_custom_config(custom_config=None):
    """
    Run pipeline with custom configuration

    Args:
        custom_config (dict): Custom configuration overrides

    Example:
        custom_config = {
            "INPUT_FILES": {"raw_customer_data": "/path/to/your/data.csv"},
            "MODEL_FILES": {"trained_model": "/path/to/your/model.pkl"}
        }
    """
    log = setup_logging()

    if custom_config:
        log("🔧 APPLYING CUSTOM CONFIGURATION")
        for section, values in custom_config.items():
            if hasattr(ProductionConfig, section):
                current_config = getattr(ProductionConfig, section)
                current_config.update(values)
                log(f"   Updated {section}: {values}")

    return run_complete_pipeline()

def get_pipeline_status():
    """
    Get current pipeline status and master dataset information
    """
    log = setup_logging()
    log("📊 PIPELINE STATUS CHECK")
    log("="*50)

    master_csv = os.path.join(ProductionConfig.OUTPUT_FOLDERS["predictions"], "master_predictions.csv")

    if os.path.exists(master_csv):
        try:
            df_master = pd.read_csv(master_csv, encoding='utf-8')

            status = {
                "master_dataset_exists": True,
                "total_predictions": len(df_master),
                "unique_customers": df_master['identificador_unico'].nunique(),
                "date_range": {
                    "earliest": df_master['prediction_date'].min(),
                    "latest": df_master['prediction_date'].max()
                },
                "file_size_mb": round(os.path.getsize(master_csv) / (1024*1024), 2),
                "last_modified": datetime.fromtimestamp(os.path.getmtime(master_csv)).strftime('%Y-%m-%d %H:%M:%S')
            }

            log(f"✅ Master dataset exists: {len(df_master):,} predictions")
            log(f"🆔 Unique customers: {status['unique_customers']:,}")
            log(f"📅 Date range: {status['date_range']['earliest']} to {status['date_range']['latest']}")
            log(f"💾 File size: {status['file_size_mb']} MB")

            return status

        except Exception as e:
            log(f"⚠️ Error reading master dataset: {e}")
            return {"master_dataset_exists": False, "error": str(e)}
    else:
        log("📝 No master dataset found - run pipeline to create")
        return {"master_dataset_exists": False}

# =============================================================================
# 🚀 MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🎯 COMPLETE END-TO-END PRODUCTION PIPELINE")
    print("="*80)
    print("🔧 Income Prediction System - XGBoost Model")
    print("📋 Pipeline: Raw Data → Features → Predictions → Master Dataset")
    print("="*80)

    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            get_pipeline_status()
        elif sys.argv[1] == "test-single":
            # Run single customer test
            print("🧪 RUNNING SINGLE CUSTOMER TEST")
            print("="*50)
            results = run_single_customer_test()
        else:
            print(f"❌ Unknown command: {sys.argv[1]}")
            print("📋 Available commands:")
            print("   python production_pipeline_complete.py          # Run full pipeline")
            print("   python production_pipeline_complete.py status   # Check status")
            print("   python production_pipeline_complete.py test-single # Test with one customer")
    else:
        # Run complete pipeline
        results = run_complete_pipeline()

        if results:
            print(f"\n✅ PIPELINE EXECUTION SUMMARY:")
            print(f"   Status: {results['pipeline_status']}")
            print(f"   Processing time: {results['execution_summary']['processing_time_seconds']} seconds")
            print(f"   Customers processed: {results['execution_summary']['customers_processed']:,}")
            print(f"   Master dataset: {results['file_locations']['master_csv']}")
        else:
            print(f"\n❌ PIPELINE FAILED - Check logs for details")
            print(f"🔧 TEAM ACTIONS:")
            print(f"   1. Verify file paths in ProductionConfig")
            print(f"   2. Check that all required files exist")
            print(f"   3. Review error logs for specific issues")

# =============================================================================
# 📚 TEAM DOCUMENTATION - CONFIGURATION GUIDE
# =============================================================================
"""
🔧 TEAM CONFIGURATION GUIDE

1. 📁 PATH CONFIGURATION:
   Update ProductionConfig class (lines 41-90):

   BASE_PATH = r"/your/project/root"  # Main project directory

   INPUT_FILES = {
       "raw_customer_data": "/path/to/your/customer_data.csv"
   }

   MODEL_FILES = {
       "trained_model": "/path/to/your/model.pkl",
       "frequency_mappings": "/path/to/your/mappings.pkl"
   }

   OUTPUT_FOLDERS = {
       "predictions": "/path/to/output/folder",
       "temp_data": "/path/to/temp/folder"
   }

2. 🤖 MODEL CONFIGURATION:
   Update MODEL_CONFIG if you retrain the model:

   MODEL_CONFIG = {
       "confidence_level": 0.90,
       "ci_lower_offset": -510.93,  # Update from new model analysis
       "ci_upper_offset": 755.02,   # Update from new model analysis
       "model_version": "XGBoost_v2.0_Updated"
   }

3. ⚙️ PROCESSING CONFIGURATION:
   Adjust PROCESSING_CONFIG for your needs:

   PROCESSING_CONFIG = {
       "archive_days": 90,     # Days to keep in master dataset
       "batch_size": 10000,    # Max records per batch
       "enable_logging": True  # Enable/disable logging
   }

4. 🚀 USAGE EXAMPLES:

   # Basic usage
   python production_pipeline_complete.py

   # Check status
   python production_pipeline_complete.py status

   # Programmatic usage
   from production_pipeline_complete import run_complete_pipeline
   results = run_complete_pipeline()

   # Custom configuration
   custom_config = {
       "INPUT_FILES": {"raw_customer_data": "/new/path/data.csv"}
   }
   results = run_pipeline_with_custom_config(custom_config)

5. 📂 OUTPUT FILES:

   model_pred_files/
   ├── master_predictions.csv          # Main dataset (CSV format)
   ├── master_predictions.json         # Main dataset (JSON format)
   ├── archive/                        # Archived old predictions
   └── pipeline_log_YYYYMMDD.txt       # Daily log files

6. 🔧 TROUBLESHOOTING:

   Common issues and solutions:
   - File not found: Update paths in ProductionConfig
   - Import errors: Ensure all pipeline files are in same directory
   - Model loading: Check model file format and XGBoost version
   - Permission errors: Verify write access to output folders

7. 📊 MONITORING:

   Check pipeline status:
   - Master dataset size and date range
   - Processing logs for errors
   - Archive folder for old predictions
   - Business metrics in JSON output

8. 🔄 MAINTENANCE:

   Regular tasks:
   - Monitor master dataset size
   - Review archived predictions
   - Update model when retrained
   - Adjust archive_days as needed
"""
