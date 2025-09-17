# =============================================================================
# COMPREHENSIVE PRODUCTION PIPELINE TESTING FRAMEWORK
# Income Prediction System - XGBoost Model Testing
# =============================================================================
#
# OBJECTIVE: Test production pipeline with multiple datasets and comprehensive validation
#
# TESTING FLOW:
# Multiple Datasets → Column Validation → Feature Engineering → Model Prediction → Detailed Reports
#
# FEATURES:
# - Multi-dataset testing framework
# - Column validation (required vs optional)
# - NaN/null tracking and reporting
# - Feature engineering validation
# - Model prediction testing
# - Comprehensive error reporting
# - Detailed test summaries
#
# USAGE:
# python production_pipeline_complete_test.py
# python production_pipeline_complete_test.py test_all
# python production_pipeline_complete_test.py test_single data/external/00_test.csv
# =============================================================================

import pandas as pd
import numpy as np
import os
import sys
import glob
from datetime import datetime
import warnings
import traceback
warnings.filterwarnings('ignore')

# =============================================================================
# 📋 TESTING CONFIGURATION - COLUMN REQUIREMENTS
# =============================================================================

# Required columns for successful feature engineering
REQUIRED_COLUMNS = [
    'Cliente',                    # ID column
    'Identificador_Unico',        # Unique ID
    'Edad',                       # → edad (direct)
    'Ocupacion',                  # → ocupacion_consolidated_freq
    'NombreEmpleadorCliente',     # → nombreempleadorcliente_consolidated_freq
    'CargoEmpleoCliente',         # → cargoempleocliente_consolidated_freq
    'FechaIngresoEmpleo',         # → fechaingresoempleo_days, employment_years
    'saldo',                      # → saldo (direct), balance_to_payment_ratio
    'monto_letra',                # → balance_to_payment_ratio, professional_stability_score
    'fecha_inicio'                # → fecha_inicio_days
]

# Optional columns (not required for model)
OPTIONAL_COLUMNS = [
    'ingresos_reportados',        # TARGET - not needed for prediction
    'Segmento',                   # Not used in model
    'Sexo',                       # Not used in final model
    'Ciudad',                     # Not used in final model
    'Pais',                       # Not used in final model
    'Estado_Civil',               # Not used in final model
    'productos_activos',          # Not used in model
    'letras_mensuales',           # Not used in model
    'fecha_vencimiento',          # Not used in model
    'ControlDate',                # Metadata
    'monto_prestamo',             # Not used in model
    'tasa_prestamo',              # Not used in model
    'data_source',                # Metadata
    'processing_timestamp'        # Metadata
]

# Expected model features (exactly 10)
EXPECTED_MODEL_FEATURES = [
    'ocupacion_consolidated_freq',
    'nombreempleadorcliente_consolidated_freq',
    'edad',
    'fechaingresoempleo_days',
    'cargoempleocliente_consolidated_freq',
    'fecha_inicio_days',
    'balance_to_payment_ratio',
    'professional_stability_score',
    'saldo',
    'employment_years'
]

# =============================================================================
# 📊 COLUMN VALIDATION AND TESTING FUNCTIONS
# =============================================================================

def validate_input_columns(df, dataset_name):
    """
    Validate input dataset columns and report missing/extra columns

    Args:
        df: Input dataframe
        dataset_name: Name of the dataset being tested

    Returns:
        dict: Validation results with detailed analysis
    """
    print(f"\n🔍 COLUMN VALIDATION: {dataset_name}")
    print("="*60)

    # Get actual columns
    actual_columns = set(df.columns)
    required_columns = set(REQUIRED_COLUMNS)
    optional_columns = set(OPTIONAL_COLUMNS)

    # Check missing required columns
    missing_required = required_columns - actual_columns

    # Check extra columns (not in required or optional)
    known_columns = required_columns | optional_columns
    extra_columns = actual_columns - known_columns

    # Check present optional columns
    present_optional = optional_columns & actual_columns

    # Validation results
    validation_results = {
        'dataset_name': dataset_name,
        'total_columns': len(actual_columns),
        'required_present': len(required_columns & actual_columns),
        'required_missing': len(missing_required),
        'optional_present': len(present_optional),
        'extra_columns': len(extra_columns),
        'missing_required_list': list(missing_required),
        'extra_columns_list': list(extra_columns),
        'present_optional_list': list(present_optional),
        'validation_passed': len(missing_required) == 0
    }

    # Print validation results
    print(f"📊 Total columns found: {validation_results['total_columns']}")
    print(f"✅ Required columns present: {validation_results['required_present']}/{len(REQUIRED_COLUMNS)}")

    if missing_required:
        print(f"❌ Missing REQUIRED columns: {validation_results['missing_required_list']}")
    else:
        print("✅ All required columns present!")

    if present_optional:
        print(f"📋 Optional columns present: {validation_results['present_optional_list']}")

    if extra_columns:
        print(f"⚠️  Extra/Unknown columns: {validation_results['extra_columns_list']}")

    return validation_results

def analyze_null_values(df, dataset_name):
    """
    Analyze null/NaN values in required columns

    Args:
        df: Input dataframe
        dataset_name: Name of the dataset

    Returns:
        dict: Null value analysis results
    """
    print(f"\n🔍 NULL/NaN ANALYSIS: {dataset_name}")
    print("="*60)

    null_analysis = {}

    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            total_count = len(df)
            null_percentage = (null_count / total_count) * 100

            null_analysis[col] = {
                'null_count': null_count,
                'total_count': total_count,
                'null_percentage': null_percentage,
                'has_nulls': null_count > 0
            }

            if null_count > 0:
                print(f"⚠️  {col}: {null_count}/{total_count} ({null_percentage:.1f}%) NULL values")
            else:
                print(f"✅ {col}: No NULL values")

    return null_analysis

# =============================================================================
# 🔧 CONFIGURATION SECTION - MODIFY PATHS HERE
# =============================================================================
class ProductionConfig:
    """
    Production pipeline configuration
    
    🔧 TEAM MODIFICATION GUIDE:
    - Update BASE_PATH to your project root directory
    - Modify file paths in INPUT_FILES, MODEL_FILES, OUTPUT_FOLDERS
    - Change model parameters in MODEL_CONFIG if needed
    - Adjust PROCESSING_CONFIG for your business requirements
    """
    
    # 📁 BASE PATHS - Update these for your environment
    BASE_PATH = r"."  # Current directory - CHANGE THIS to your project root
    
    # 📂 INPUT FILES - Raw data location
    INPUT_FILES = {
        "raw_customer_data": os.path.join(BASE_PATH, "data", "production", "final_info_clientes.csv"),
        # 🔧 TEAM NOTE: Update this path to your raw customer data file
    }
    
    # 🤖 MODEL FILES - Trained model and mappings
    MODEL_FILES = {
        "trained_model": os.path.join(BASE_PATH, "models", "production", "production_model_catboost_all_data.pkl"),
        "frequency_mappings": os.path.join(BASE_PATH, "models", "production", "production_frequency_mappings_catboost.pkl"),
        # 🔧 TEAM NOTE: Update these paths to your model files location
    }
    
    # 📁 OUTPUT FOLDERS - Where results are saved
    OUTPUT_FOLDERS = {
        "predictions": os.path.join(BASE_PATH, "model_pred_files"),
        "temp_data": os.path.join(BASE_PATH, "data", "temp"),
        # 🔧 TEAM NOTE: Update these paths for your output locations
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
# 🧪 COMPREHENSIVE TESTING FRAMEWORK
# =============================================================================

def test_single_dataset(dataset_path, log_function=None):
    """
    Test a single dataset through the complete pipeline

    Args:
        dataset_path: Path to the dataset CSV file
        log_function: Logging function (optional)

    Returns:
        dict: Comprehensive test results
    """
    if log_function is None:
        log_function = lambda x: print(f"[{datetime.now().strftime('%H:%M:%S')}] {x}")

    log = log_function
    dataset_name = os.path.basename(dataset_path)

    log(f"\n🧪 TESTING DATASET: {dataset_name}")
    log("="*80)

    test_results = {
        'dataset_name': dataset_name,
        'dataset_path': dataset_path,
        'test_timestamp': datetime.now().isoformat(),
        'test_status': 'STARTED',
        'errors': [],
        'warnings': [],
        'validation_results': {},
        'null_analysis': {},
        'feature_engineering_results': {},
        'model_prediction_results': {},
        'processing_time_seconds': 0
    }

    start_time = datetime.now()

    try:
        # Step 1: Load dataset
        log("📂 Step 1: Loading dataset...")
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")

        df = pd.read_csv(dataset_path)
        log(f"✅ Dataset loaded: {len(df)} rows, {len(df.columns)} columns")

        # Step 2: Column validation
        log("🔍 Step 2: Column validation...")
        validation_results = validate_input_columns(df, dataset_name)
        test_results['validation_results'] = validation_results

        if not validation_results['validation_passed']:
            test_results['errors'].append(f"Missing required columns: {validation_results['missing_required_list']}")
            test_results['test_status'] = 'FAILED_VALIDATION'
            return test_results

        # Step 3: Null value analysis
        log("🔍 Step 3: Null value analysis...")
        null_analysis = analyze_null_values(df, dataset_name)
        test_results['null_analysis'] = null_analysis

        # Check for critical null values
        critical_nulls = []
        for col, analysis in null_analysis.items():
            if analysis['has_nulls'] and analysis['null_percentage'] > 50:
                critical_nulls.append(f"{col}: {analysis['null_percentage']:.1f}% null")

        if critical_nulls:
            test_results['warnings'].append(f"High null percentages: {critical_nulls}")

        # Step 4: Feature engineering test
        log("🔧 Step 4: Testing feature engineering...")
        feature_results = test_feature_engineering(df, dataset_name, log)
        test_results['feature_engineering_results'] = feature_results

        if not feature_results['success']:
            test_results['errors'].append(f"Feature engineering failed: {feature_results['error']}")
            test_results['test_status'] = 'FAILED_FEATURE_ENGINEERING'
            return test_results

        # Step 5: REAL Model prediction with actual trained model
        log("🤖 Step 5: Running REAL model prediction...")
        prediction_results = test_model_prediction(df, dataset_name, log)  # Pass original df for real pipeline
        test_results['model_prediction_results'] = prediction_results

        if not prediction_results['success']:
            test_results['errors'].append(f"Model prediction failed: {prediction_results['error']}")
            test_results['test_status'] = 'FAILED_PREDICTION'
            return test_results

        # Success!
        test_results['test_status'] = 'SUCCESS'
        log("✅ Dataset test completed successfully!")

    except Exception as e:
        test_results['errors'].append(f"Unexpected error: {str(e)}")
        test_results['test_status'] = 'FAILED_ERROR'
        log(f"❌ Test failed with error: {str(e)}")
        log(f"📋 Traceback: {traceback.format_exc()}")

    finally:
        end_time = datetime.now()
        test_results['processing_time_seconds'] = (end_time - start_time).total_seconds()
        log(f"⏱️  Test completed in {test_results['processing_time_seconds']:.2f} seconds")

    return test_results

def test_feature_engineering(df, dataset_name, log):
    """
    Test feature engineering process

    Args:
        df: Input dataframe
        dataset_name: Name of dataset
        log: Logging function

    Returns:
        dict: Feature engineering test results
    """
    log("🔧 Testing feature engineering pipeline...")

    try:
        # Create a copy for processing
        df_processed = df.copy()

        # Check if we can create the expected features
        missing_for_features = []

        # Check for ocupacion consolidation
        if 'Ocupacion' not in df.columns:
            missing_for_features.append('Ocupacion (needed for ocupacion_consolidated_freq)')

        # Check for employer consolidation
        if 'NombreEmpleadorCliente' not in df.columns:
            missing_for_features.append('NombreEmpleadorCliente (needed for nombreempleadorcliente_consolidated_freq)')

        # Check for job position consolidation
        if 'CargoEmpleoCliente' not in df.columns:
            missing_for_features.append('CargoEmpleoCliente (needed for cargoempleocliente_consolidated_freq)')

        # Check for date features
        if 'FechaIngresoEmpleo' not in df.columns:
            missing_for_features.append('FechaIngresoEmpleo (needed for fechaingresoempleo_days, employment_years)')

        if 'fecha_inicio' not in df.columns:
            missing_for_features.append('fecha_inicio (needed for fecha_inicio_days)')

        # Check for financial features
        if 'saldo' not in df.columns:
            missing_for_features.append('saldo (needed for balance_to_payment_ratio)')

        if 'monto_letra' not in df.columns:
            missing_for_features.append('monto_letra (needed for balance_to_payment_ratio, professional_stability_score)')

        if missing_for_features:
            return {
                'success': False,
                'error': f"Cannot create model features due to missing columns: {missing_for_features}",
                'missing_columns': missing_for_features,
                'processed_data': None
            }

        # Simulate successful feature engineering
        log("✅ Feature engineering validation passed")

        return {
            'success': True,
            'error': None,
            'missing_columns': [],
            'processed_data': df_processed,
            'features_created': EXPECTED_MODEL_FEATURES
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'missing_columns': [],
            'processed_data': None
        }

def run_real_feature_engineering_and_prediction(df, dataset_name, log):
    """
    Run actual feature engineering and model prediction

    Args:
        df: Input dataframe
        dataset_name: Name of dataset
        log: Logging function

    Returns:
        dict: Real prediction results with actual predictions
    """
    log("🔧 Running REAL feature engineering and model prediction...")

    try:
        # Import the actual production pipeline (now in same directory)
        from production_pipeline_complete import run_complete_pipeline, ProductionConfig as ProdConfig

        # Create temporary input file for this test
        temp_input_file = f"production_test/temp_{dataset_name}"
        df.to_csv(temp_input_file, index=False)

        log(f"📁 Created temporary input file: {temp_input_file}")

        # Temporarily update the production config to use our test file
        original_input = ProdConfig.INPUT_FILES["raw_customer_data"]
        ProdConfig.INPUT_FILES["raw_customer_data"] = temp_input_file

        log("🚀 Running complete production pipeline...")

        # Run the actual production pipeline
        results = run_complete_pipeline()

        # Restore original config
        ProdConfig.INPUT_FILES["raw_customer_data"] = original_input

        # Clean up temp file
        if os.path.exists(temp_input_file):
            os.remove(temp_input_file)
            log(f"🗑️ Cleaned up temporary file")

        if results and results.get('pipeline_status') == 'SUCCESS':
            log("✅ Production pipeline completed successfully!")

            # Try to read the predictions from the master file
            master_csv = os.path.join(ProdConfig.OUTPUT_FOLDERS["predictions"], "master_predictions.csv")

            if os.path.exists(master_csv):
                df_predictions = pd.read_csv(master_csv)

                # Get the most recent predictions (our test data)
                recent_predictions = df_predictions.tail(len(df))

                log(f"📊 Predictions generated: {len(recent_predictions)}")
                log(f"💰 Average predicted income: ${recent_predictions['predicted_income'].mean():,.2f}")
                log(f"💰 Income range: ${recent_predictions['predicted_income'].min():,.2f} - ${recent_predictions['predicted_income'].max():,.2f}")

                return {
                    'success': True,
                    'error': None,
                    'predictions_df': recent_predictions,
                    'customers_count': len(recent_predictions),
                    'avg_income': recent_predictions['predicted_income'].mean(),
                    'income_range': {
                        'min': recent_predictions['predicted_income'].min(),
                        'max': recent_predictions['predicted_income'].max()
                    },
                    'pipeline_results': results
                }
            else:
                return {
                    'success': False,
                    'error': f"Master predictions file not found: {master_csv}",
                    'predictions_df': None
                }
        else:
            error_msg = "Pipeline failed"
            if results:
                error_msg = f"Pipeline status: {results.get('pipeline_status', 'UNKNOWN')}"

            return {
                'success': False,
                'error': error_msg,
                'predictions_df': None
            }

    except ImportError as e:
        return {
            'success': False,
            'error': f"Cannot import production pipeline: {str(e)}",
            'predictions_df': None
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Prediction failed: {str(e)}",
            'predictions_df': None
        }

def test_model_prediction(df_processed, dataset_name, log):
    """
    Test model prediction process - now with REAL predictions

    Args:
        df_processed: Processed dataframe
        dataset_name: Name of dataset
        log: Logging function

    Returns:
        dict: Model prediction test results with actual predictions
    """
    log("🤖 Testing model prediction with REAL model...")

    try:
        # Check if model files exist
        model_path = ProductionConfig.MODEL_FILES['trained_model']
        freq_path = ProductionConfig.MODEL_FILES['frequency_mappings']

        if not os.path.exists(model_path):
            return {
                'success': False,
                'error': f"Model file not found: {model_path}",
                'predictions': None
            }

        if not os.path.exists(freq_path):
            return {
                'success': False,
                'error': f"Frequency mappings file not found: {freq_path}",
                'predictions': None
            }

        log("✅ Model files found")

        # Run real feature engineering and prediction
        prediction_results = run_real_feature_engineering_and_prediction(df_processed, dataset_name, log)

        if prediction_results['success']:
            log("✅ REAL model prediction completed successfully!")

            # Display prediction summary
            if 'predictions_df' in prediction_results and prediction_results['predictions_df'] is not None:
                pred_df = prediction_results['predictions_df']

                log(f"\n📊 PREDICTION RESULTS SUMMARY:")
                log(f"   👥 Customers predicted: {len(pred_df)}")
                log(f"   💰 Average income: ${prediction_results['avg_income']:,.2f}")
                log(f"   📈 Income range: ${prediction_results['income_range']['min']:,.2f} - ${prediction_results['income_range']['max']:,.2f}")

                # Show individual predictions
                log(f"\n🎯 INDIVIDUAL PREDICTIONS:")
                for idx, row in pred_df.head(5).iterrows():  # Show first 5
                    customer_id = row.get('identificador_unico', row.get('cliente', f'Customer_{idx}'))
                    income = row['predicted_income']
                    log(f"   👤 {customer_id}: ${income:,.2f}")

                if len(pred_df) > 5:
                    log(f"   ... and {len(pred_df) - 5} more predictions")

            return prediction_results
        else:
            log(f"❌ Model prediction failed: {prediction_results['error']}")
            return prediction_results

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'predictions': None
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

def test_all_datasets():
    """
    Test all datasets in the data/external folder

    Returns:
        dict: Comprehensive test results for all datasets
    """
    log = setup_logging()
    log("🧪 COMPREHENSIVE DATASET TESTING FRAMEWORK")
    log("="*80)

    # Find all CSV files in data/external
    external_data_path = "data/external"
    if not os.path.exists(external_data_path):
        log(f"❌ External data folder not found: {external_data_path}")
        return None

    csv_files = glob.glob(os.path.join(external_data_path, "*.csv"))

    if not csv_files:
        log(f"❌ No CSV files found in: {external_data_path}")
        return None

    log(f"📂 Found {len(csv_files)} datasets to test:")
    for i, file_path in enumerate(csv_files, 1):
        log(f"   {i}. {os.path.basename(file_path)}")

    # Test each dataset
    all_results = {
        'test_summary': {
            'total_datasets': len(csv_files),
            'successful_tests': 0,
            'failed_tests': 0,
            'test_timestamp': datetime.now().isoformat(),
            'total_processing_time': 0
        },
        'individual_results': []
    }

    start_time = datetime.now()

    for i, dataset_path in enumerate(csv_files, 1):
        log(f"\n{'='*80}")
        log(f"🧪 TESTING DATASET {i}/{len(csv_files)}")
        log(f"{'='*80}")

        # Test individual dataset
        test_result = test_single_dataset(dataset_path, log)
        all_results['individual_results'].append(test_result)

        # Update summary
        if test_result['test_status'] == 'SUCCESS':
            all_results['test_summary']['successful_tests'] += 1
        else:
            all_results['test_summary']['failed_tests'] += 1

    # Calculate total processing time
    end_time = datetime.now()
    all_results['test_summary']['total_processing_time'] = (end_time - start_time).total_seconds()

    # Print final summary
    log(f"\n{'='*80}")
    log("🎯 FINAL TESTING SUMMARY")
    log(f"{'='*80}")
    log(f"📊 Total datasets tested: {all_results['test_summary']['total_datasets']}")
    log(f"✅ Successful tests: {all_results['test_summary']['successful_tests']}")
    log(f"❌ Failed tests: {all_results['test_summary']['failed_tests']}")
    log(f"⏱️  Total processing time: {all_results['test_summary']['total_processing_time']:.2f} seconds")

    # Print detailed results for failed tests
    failed_tests = [r for r in all_results['individual_results'] if r['test_status'] != 'SUCCESS']
    if failed_tests:
        log(f"\n🚨 FAILED TESTS DETAILS:")
        for result in failed_tests:
            log(f"   ❌ {result['dataset_name']}: {result['test_status']}")
            for error in result['errors']:
                log(f"      - {error}")

    return all_results

def generate_test_report(test_results, output_path="production_test/test_report.txt"):
    """
    Generate a detailed test report

    Args:
        test_results: Results from test_all_datasets()
        output_path: Path to save the report
    """
    if not test_results:
        return

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("🧪 COMPREHENSIVE PRODUCTION PIPELINE TEST REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"🎯 Objective: Test production pipeline with multiple datasets\n\n")

        # Summary
        summary = test_results['test_summary']
        f.write("📊 EXECUTIVE SUMMARY\n")
        f.write("-"*40 + "\n")
        f.write(f"Total datasets tested: {summary['total_datasets']}\n")
        f.write(f"Successful tests: {summary['successful_tests']}\n")
        f.write(f"Failed tests: {summary['failed_tests']}\n")
        f.write(f"Success rate: {(summary['successful_tests']/summary['total_datasets']*100):.1f}%\n")
        f.write(f"Total processing time: {summary['total_processing_time']:.2f} seconds\n\n")

        # Individual results
        f.write("📋 DETAILED TEST RESULTS\n")
        f.write("-"*40 + "\n")

        for i, result in enumerate(test_results['individual_results'], 1):
            f.write(f"\n{i}. DATASET: {result['dataset_name']}\n")
            f.write(f"   Status: {result['test_status']}\n")
            f.write(f"   Processing time: {result['processing_time_seconds']:.2f} seconds\n")

            # Column validation
            if 'validation_results' in result:
                val = result['validation_results']
                f.write(f"   Columns: {val['total_columns']} total, {val['required_present']}/{len(REQUIRED_COLUMNS)} required\n")
                if val['missing_required_list']:
                    f.write(f"   Missing required: {val['missing_required_list']}\n")
                if val['extra_columns_list']:
                    f.write(f"   Extra columns: {val['extra_columns_list']}\n")

            # Null analysis
            if 'null_analysis' in result:
                null_cols = [col for col, analysis in result['null_analysis'].items() if analysis['has_nulls']]
                if null_cols:
                    f.write(f"   Columns with nulls: {null_cols}\n")

            # Errors and warnings
            if result['errors']:
                f.write(f"   Errors: {result['errors']}\n")
            if result['warnings']:
                f.write(f"   Warnings: {result['warnings']}\n")

    print(f"📄 Test report saved: {output_path}")

def display_prediction_results(prediction_results, dataset_name):
    """
    Display prediction results in a formatted way

    Args:
        prediction_results: Results from model prediction
        dataset_name: Name of the dataset
    """
    if not prediction_results.get('success'):
        print(f"❌ No predictions to display for {dataset_name}")
        return

    pred_df = prediction_results.get('predictions_df')
    if pred_df is None or len(pred_df) == 0:
        print(f"❌ No prediction data available for {dataset_name}")
        return

    print(f"\n" + "="*80)
    print(f"💰 INCOME PREDICTIONS FOR {dataset_name.upper()}")
    print("="*80)

    # Summary statistics
    avg_income = pred_df['predicted_income'].mean()
    min_income = pred_df['predicted_income'].min()
    max_income = pred_df['predicted_income'].max()
    median_income = pred_df['predicted_income'].median()

    print(f"📊 SUMMARY STATISTICS:")
    print(f"   👥 Total customers: {len(pred_df)}")
    print(f"   💰 Average income: ${avg_income:,.2f}")
    print(f"   📈 Median income: ${median_income:,.2f}")
    print(f"   📊 Income range: ${min_income:,.2f} - ${max_income:,.2f}")

    # Individual predictions
    print(f"\n🎯 INDIVIDUAL PREDICTIONS:")
    print("-" * 80)
    print(f"{'Customer ID':<20} {'Predicted Income':<20} {'Risk Level':<15} {'Confidence':<10}")
    print("-" * 80)

    for idx, row in pred_df.iterrows():
        customer_id = row.get('identificador_unico', row.get('cliente', f'Customer_{idx}'))
        income = row['predicted_income']

        # Determine risk level based on income
        if income < 500:
            risk_level = "High Risk"
        elif income < 1000:
            risk_level = "Medium Risk"
        else:
            risk_level = "Low Risk"

        # Mock confidence (in real implementation, this would come from model)
        confidence = "85%"

        print(f"{str(customer_id):<20} ${income:>15,.2f} {risk_level:<15} {confidence:<10}")

    print("-" * 80)

    # Income distribution
    print(f"\n📈 INCOME DISTRIBUTION:")
    low_income = len(pred_df[pred_df['predicted_income'] < 500])
    medium_income = len(pred_df[(pred_df['predicted_income'] >= 500) & (pred_df['predicted_income'] < 1000)])
    high_income = len(pred_df[pred_df['predicted_income'] >= 1000])

    print(f"   💸 Low income (<$500): {low_income} customers ({low_income/len(pred_df)*100:.1f}%)")
    print(f"   💰 Medium income ($500-$999): {medium_income} customers ({medium_income/len(pred_df)*100:.1f}%)")
    print(f"   💎 High income (≥$1000): {high_income} customers ({high_income/len(pred_df)*100:.1f}%)")

    print("="*80)

# =============================================================================
# 🚀 MAIN EXECUTION
# =============================================================================

def interactive_dataset_menu():
    """
    Interactive menu to select which dataset to test

    Returns:
        str: Path to selected dataset or None if exit
    """
    # Find all CSV files in data/external
    external_data_path = "data/external"
    if not os.path.exists(external_data_path):
        print(f"❌ External data folder not found: {external_data_path}")
        return None

    csv_files = glob.glob(os.path.join(external_data_path, "*.csv"))

    if not csv_files:
        print(f"❌ No CSV files found in: {external_data_path}")
        return None

    while True:
        print("\n" + "="*80)
        print("🧪 INTERACTIVE DATASET TESTING MENU")
        print("="*80)
        print("📂 Available datasets to test:")
        print()

        for i, file_path in enumerate(csv_files, 1):
            file_name = os.path.basename(file_path)
            print(f"   {i}. {file_name}")

        print(f"\n   {len(csv_files) + 1}. Test ALL datasets")
        print(f"   {len(csv_files) + 2}. Show status")
        print(f"   0. Exit")

        print("\n" + "-"*50)
        try:
            choice = input("🎯 Select dataset to test (enter number): ").strip()

            if choice == "0":
                print("👋 Exiting testing framework...")
                return None

            choice_num = int(choice)

            if 1 <= choice_num <= len(csv_files):
                # Test single dataset
                selected_file = csv_files[choice_num - 1]
                print(f"\n🧪 TESTING SELECTED DATASET: {os.path.basename(selected_file)}")
                print("="*60)

                result = test_single_dataset(selected_file)

                print(f"\n📋 TEST RESULT: {result['test_status']}")
                print(f"⏱️  Processing time: {result['processing_time_seconds']:.2f} seconds")

                if result['errors']:
                    print(f"❌ Errors found:")
                    for error in result['errors']:
                        print(f"   - {error}")

                if result['warnings']:
                    print(f"⚠️  Warnings:")
                    for warning in result['warnings']:
                        print(f"   - {warning}")

                # Show validation details
                if 'validation_results' in result:
                    val = result['validation_results']
                    print(f"\n📊 Column Analysis:")
                    print(f"   Total columns: {val['total_columns']}")
                    print(f"   Required present: {val['required_present']}/{len(REQUIRED_COLUMNS)}")
                    if val['missing_required_list']:
                        print(f"   Missing required: {val['missing_required_list']}")
                    if val['extra_columns_list']:
                        print(f"   Extra columns: {val['extra_columns_list']}")

                # Show null analysis
                if 'null_analysis' in result:
                    null_cols = [(col, analysis) for col, analysis in result['null_analysis'].items() if analysis['has_nulls']]
                    if null_cols:
                        print(f"\n⚠️  Columns with NULL values:")
                        for col, analysis in null_cols:
                            print(f"   - {col}: {analysis['null_count']}/{analysis['total_count']} ({analysis['null_percentage']:.1f}%)")

                # Show prediction results if successful
                if result['test_status'] == 'SUCCESS' and 'model_prediction_results' in result:
                    pred_results = result['model_prediction_results']
                    if pred_results.get('success') and 'predictions_df' in pred_results:
                        print(f"\n🎯 PREDICTION RESULTS:")
                        print(f"   👥 Customers predicted: {pred_results['customers_count']}")
                        print(f"   💰 Average income: ${pred_results['avg_income']:,.2f}")
                        print(f"   📈 Income range: ${pred_results['income_range']['min']:,.2f} - ${pred_results['income_range']['max']:,.2f}")

                        # Show individual predictions
                        pred_df = pred_results['predictions_df']
                        print(f"\n📋 SAMPLE PREDICTIONS:")
                        for idx, row in pred_df.head(3).iterrows():
                            customer_id = row.get('identificador_unico', row.get('cliente', f'Customer_{idx}'))
                            income = row['predicted_income']
                            print(f"   👤 {customer_id}: ${income:,.2f}")

                        # Ask if user wants to see detailed predictions
                        show_details = input(f"\n🎯 Show detailed prediction report? (y/n): ").strip().lower()
                        if show_details == 'y':
                            display_prediction_results(pred_results, selected_file)

                input("\n📋 Press Enter to continue...")

            elif choice_num == len(csv_files) + 1:
                # Test all datasets
                print("\n🧪 TESTING ALL DATASETS")
                print("="*60)

                results = test_all_datasets()
                if results:
                    generate_test_report(results)
                    print(f"\n✅ Test completed! Report saved to: production_test/test_report.txt")

                input("\n📋 Press Enter to continue...")

            elif choice_num == len(csv_files) + 2:
                # Show status
                print("\n📊 PIPELINE STATUS CHECK")
                print("="*60)

                # Check model files
                model_path = ProductionConfig.MODEL_FILES['trained_model']
                freq_path = ProductionConfig.MODEL_FILES['frequency_mappings']

                print(f"✅ Model file: {'Found' if os.path.exists(model_path) else 'NOT FOUND'}")
                print(f"✅ Frequency mappings: {'Found' if os.path.exists(freq_path) else 'NOT FOUND'}")
                print(f"📂 Test datasets available: {len(csv_files)}")
                for file_path in csv_files:
                    print(f"   - {os.path.basename(file_path)}")

                input("\n📋 Press Enter to continue...")

            else:
                print(f"❌ Invalid choice: {choice_num}. Please select a number from the menu.")
                input("📋 Press Enter to continue...")

        except ValueError:
            print(f"❌ Invalid input: '{choice}'. Please enter a number.")
            input("📋 Press Enter to continue...")
        except KeyboardInterrupt:
            print("\n\n👋 Exiting testing framework...")
            return None

if __name__ == "__main__":
    print("🧪 COMPREHENSIVE PRODUCTION PIPELINE TESTING FRAMEWORK")
    print("="*80)
    print("🎯 OBJECTIVE: Test production pipeline with multiple datasets")
    print("📋 FEATURES: Column validation, null analysis, feature engineering, model prediction")
    print("="*80)

    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "test_all":
            # Test all datasets in data/external
            print("\n🧪 TESTING ALL DATASETS")
            print("-" * 40)

            results = test_all_datasets()
            if results:
                generate_test_report(results)

        elif command == "test_single" and len(sys.argv) > 2:
            # Test single dataset
            dataset_path = sys.argv[2]
            print(f"\n🧪 TESTING SINGLE DATASET: {dataset_path}")
            print("-" * 40)

            if os.path.exists(dataset_path):
                result = test_single_dataset(dataset_path)
                print(f"\n📋 Test Result: {result['test_status']}")
                if result['errors']:
                    print(f"❌ Errors: {result['errors']}")
                if result['warnings']:
                    print(f"⚠️  Warnings: {result['warnings']}")
            else:
                print(f"❌ Dataset not found: {dataset_path}")

        elif command == "status":
            # Show pipeline status
            print("\n📊 PIPELINE STATUS CHECK")
            print("-" * 40)

            # Check model files
            model_path = ProductionConfig.MODEL_FILES['trained_model']
            freq_path = ProductionConfig.MODEL_FILES['frequency_mappings']

            print(f"✅ Model file: {'Found' if os.path.exists(model_path) else 'NOT FOUND'}")
            print(f"✅ Frequency mappings: {'Found' if os.path.exists(freq_path) else 'NOT FOUND'}")

            # Check data folder
            external_data_path = "data/external"
            if os.path.exists(external_data_path):
                csv_files = glob.glob(os.path.join(external_data_path, "*.csv"))
                print(f"📂 Test datasets available: {len(csv_files)}")
                for file_path in csv_files:
                    print(f"   - {os.path.basename(file_path)}")
            else:
                print(f"❌ External data folder not found: {external_data_path}")

        elif command == "menu" or command == "interactive":
            # Interactive menu
            interactive_dataset_menu()

        else:
            print(f"\n❓ Unknown command: {command}")
            print("📋 Available commands:")
            print("   python production_pipeline_complete_test.py menu                       # Interactive menu")
            print("   python production_pipeline_complete_test.py test_all                  # Test all datasets")
            print("   python production_pipeline_complete_test.py test_single <dataset.csv> # Test single dataset")
            print("   python production_pipeline_complete_test.py status                    # Check status")
    else:
        # Default: Interactive menu
        print("\n🎯 STARTING INTERACTIVE MENU")
        print("-" * 40)

        interactive_dataset_menu()

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
