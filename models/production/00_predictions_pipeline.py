# =============================================================================
# PRODUCTION PIPELINE PART 1 - DATA CLEANING & FEATURE ENGINEERING
# =============================================================================
#
# OBJECTIVE: Create df_clientes_clean_final.csv for production inference
#
# FINAL MODEL FEATURES REQUIRED:
# ['ocupacion_consolidated_freq', 'nombreempleadorcliente_consolidated_freq',
#  'edad', 'fechaingresoempleo_days', 'cargoempleocliente_consolidated_freq',
#  'fecha_inicio_days', 'balance_to_payment_ratio', 'professional_stability_score',
#  'saldo', 'employment_years']
#
# ORIGINAL DATASET FEATURES AVAILABLE (PRODUCTION):
# ['Cliente', 'Identificador_Unico', 'Segmento', 'Edad', 'Sexo', 'Ciudad', 'Pais',
#  'Ocupacion', 'Estado_Civil', 'FechaIngresoEmpleo', 'NombreEmpleadorCliente',
#  'CargoEmpleoCliente', 'productos_activos', 'letras_mensuales', 'monto_letra',
#  'saldo', 'fecha_inicio', 'fecha_vencimiento', 'ControlDate', 'monto_prestamo',
#  'tasa_prestamo', 'data_source', 'processing_timestamp']
#
# NOTE: 'ingresos_reportados' is NOT available in production (that's what we predict!)
# =============================================================================

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import pickle
import os
warnings.filterwarnings('ignore')

# Try to import required ML libraries
try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False
    print("⚠️ Warning: joblib not available, will use pickle only")

try:
    import xgboost
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️ Warning: XGBoost not available - model loading may fail")

try:
    import sklearn
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️ Warning: scikit-learn not available - model loading may fail")

# Set display options
pd.set_option('display.max_columns', None)

def load_and_prepare_production_data(file_path):
    """
    Load and prepare data for production inference with only required features
    """
    print("🚀 PRODUCTION PIPELINE - LOADING DATA")
    print("="*60)
    
    # Load the dataset
    print("📂 Loading dataset...")
    df = pd.read_csv(file_path, encoding='latin-1', sep=',', on_bad_lines='skip', engine='python')
    print(f"✅ Dataset loaded: {df.shape}")
    
    return df

def standardize_column_names_production(df):
    """
    Standardize column names for production (simplified version)
    """
    print("🔧 Standardizing column names...")
    
    # Simple column name mapping for production
    column_mapping = {
        'Cliente': 'cliente',
        'Identificador_Unico': 'identificador_unico', 
        'Edad': 'edad',
        'Ocupacion': 'ocupacion',
        'FechaIngresoEmpleo': 'fechaingresoempleo',
        'NombreEmpleadorCliente': 'nombreempleadorcliente',
        'CargoEmpleoCliente': 'cargoempleocliente',
        'monto_letra': 'monto_letra',
        'saldo': 'saldo',
        'fecha_inicio': 'fecha_inicio'
        # NOTE: 'ingresos_reportados' NOT available in production - that's what we predict!
    }
    
    # Apply mapping
    df = df.rename(columns=column_mapping)
    
    # Clean any remaining column names
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '', regex=True)
    
    print(f"✅ Column names standardized")
    return df

def convert_date_columns_production(df):
    """
    Convert only required date columns for production
    """
    print("📅 Converting date columns...")
    
    # Required date columns for our features
    date_columns = ['fechaingresoempleo', 'fecha_inicio']
    
    for col in date_columns:
        if col in df.columns:
            print(f"   Converting {col}...")
            try:
                # Try DD/MM/YYYY format first (most common)
                df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')
                success_rate = df[col].notna().sum() / len(df)
                print(f"   ✅ {col} converted (success rate: {success_rate:.1%})")
            except:
                print(f"   ⚠️ {col} conversion failed")
        else:
            print(f"   ⚠️ {col} not found in dataset")
    
    return df

def create_frequency_features_production(df):
    """
    Create frequency encoding features for categorical variables
    """
    print("🔢 Creating frequency encoding features...")
    
    # Frequency encoding for categorical features
    categorical_freq_features = {
        'ocupacion': 'ocupacion_consolidated_freq',
        'nombreempleadorcliente': 'nombreempleadorcliente_consolidated_freq', 
        'cargoempleocliente': 'cargoempleocliente_consolidated_freq'
    }
    
    for original_col, freq_col in categorical_freq_features.items():
        if original_col in df.columns:
            print(f"   Creating {freq_col}...")
            
            # Clean and consolidate categorical values
            df[original_col] = df[original_col].astype(str).str.strip().str.upper()
            
            # Create frequency encoding
            freq_map = df[original_col].value_counts().to_dict()
            df[freq_col] = df[original_col].map(freq_map).fillna(0)
            
            print(f"   ✅ {freq_col} created (unique values: {df[freq_col].nunique()})")
        else:
            print(f"   ⚠️ {original_col} not found - setting {freq_col} to 0")
            df[freq_col] = 0
    
    return df

def create_temporal_features_production(df):
    """
    Create temporal features from date columns
    """
    print("⏰ Creating temporal features...")
    
    # Reference date for calculations (use current date or a fixed reference)
    reference_date = datetime.now()
    
    # Create days-based features
    temporal_features = {
        'fechaingresoempleo': 'fechaingresoempleo_days',
        'fecha_inicio': 'fecha_inicio_days'
    }
    
    for date_col, days_col in temporal_features.items():
        if date_col in df.columns and pd.api.types.is_datetime64_any_dtype(df[date_col]):
            print(f"   Creating {days_col}...")
            df[days_col] = (reference_date - df[date_col]).dt.days
            df[days_col] = df[days_col].fillna(df[days_col].median())  # Fill missing with median
            print(f"   ✅ {days_col} created")
        else:
            print(f"   ⚠️ {date_col} not available - setting {days_col} to median")
            df[days_col] = 1000  # Default value
    
    return df

def create_derived_features_production(df):
    """
    Create derived features required by the model
    """
    print("🔧 Creating derived features...")
    
    # 1. Balance to payment ratio
    print("   Creating balance_to_payment_ratio...")
    if 'saldo' in df.columns and 'monto_letra' in df.columns:
        # Avoid division by zero
        df['balance_to_payment_ratio'] = np.where(
            df['monto_letra'] > 0,
            df['saldo'] / df['monto_letra'],
            0
        )
        # Cap extreme values
        df['balance_to_payment_ratio'] = np.clip(df['balance_to_payment_ratio'], 0, 100)
        print("   ✅ balance_to_payment_ratio created")
    else:
        print("   ⚠️ Required columns missing - setting balance_to_payment_ratio to 0")
        df['balance_to_payment_ratio'] = 0
    
    # 2. Employment years (from fechaingresoempleo)
    print("   Creating employment_years...")
    if 'fechaingresoempleo_days' in df.columns:
        df['employment_years'] = df['fechaingresoempleo_days'] / 365.25
        df['employment_years'] = np.clip(df['employment_years'], 0, 50)  # Cap at 50 years
        print("   ✅ employment_years created")
    else:
        print("   ⚠️ fechaingresoempleo_days missing - setting employment_years to 5")
        df['employment_years'] = 5  # Default value
    
    # 3. Professional stability score (composite feature)
    print("   Creating professional_stability_score...")
    
    # Simple professional stability score based on available features
    stability_components = []
    
    # Employment tenure component (longer = more stable)
    if 'employment_years' in df.columns:
        employment_stability = np.clip(df['employment_years'] / 10, 0, 1)  # Normalize to 0-1
        stability_components.append(employment_stability)
    
    # Employer frequency component (more common employers = more stable)
    if 'nombreempleadorcliente_consolidated_freq' in df.columns:
        employer_stability = np.clip(df['nombreempleadorcliente_consolidated_freq'] / 100, 0, 1)
        stability_components.append(employer_stability)
    
    # Occupation frequency component
    if 'ocupacion_consolidated_freq' in df.columns:
        occupation_stability = np.clip(df['ocupacion_consolidated_freq'] / 100, 0, 1)
        stability_components.append(occupation_stability)
    
    # Calculate composite score
    if stability_components:
        df['professional_stability_score'] = np.mean(stability_components, axis=0)
    else:
        df['professional_stability_score'] = 0.5  # Default neutral score
    
    print("   ✅ professional_stability_score created")
    
    return df

def validate_final_features_production(df):
    """
    Validate that all required features are present and handle missing values
    """
    print("✅ Validating final features...")
    
    # Required features for the model
    required_features = [
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
    
    print(f"📋 Checking {len(required_features)} required features...")
    
    missing_features = []
    for feature in required_features:
        if feature not in df.columns:
            missing_features.append(feature)
            print(f"   ❌ Missing: {feature}")
        else:
            missing_count = df[feature].isnull().sum()
            missing_pct = (missing_count / len(df)) * 100
            print(f"   ✅ {feature}: {missing_count} missing ({missing_pct:.1f}%)")
    
    if missing_features:
        print(f"⚠️ Missing features: {missing_features}")
        return False, missing_features
    
    # Handle missing values in existing features
    print("\n🔧 Handling missing values...")
    for feature in required_features:
        if df[feature].isnull().sum() > 0:
            if df[feature].dtype in ['int64', 'float64']:
                # Fill numeric features with median
                median_val = df[feature].median()
                df[feature] = df[feature].fillna(median_val)
                print(f"   📊 {feature}: filled with median ({median_val:.2f})")
            else:
                # Fill categorical features with mode or default
                mode_val = df[feature].mode().iloc[0] if len(df[feature].mode()) > 0 else 0
                df[feature] = df[feature].fillna(mode_val)
                print(f"   📊 {feature}: filled with mode ({mode_val})")
    
    print("✅ All features validated and missing values handled")
    return True, []

def production_pipeline_part1_main(file_path, output_path=None):
    """
    Main production pipeline PART 1 - Data cleaning and feature engineering
    Creates df_clientes_clean_final.csv ready for Part 2 (model inference)
    """
    print("🚀 STARTING PRODUCTION PIPELINE - PART 1")
    print("="*80)
    print("🎯 OBJECTIVE: Create df_clientes_clean_final for model inference")
    print("📋 NOTE: ingresos_reportados NOT available (that's what we predict!)")
    print("="*80)
    
    # Step 1: Load data
    df = load_and_prepare_production_data(file_path)
    
    # Step 2: Standardize column names
    df = standardize_column_names_production(df)
    
    # Step 3: Convert date columns
    df = convert_date_columns_production(df)
    
    # Step 4: Create frequency features
    df = create_frequency_features_production(df)
    
    # Step 5: Create temporal features
    df = create_temporal_features_production(df)
    
    # Step 6: Create derived features
    df = create_derived_features_production(df)
    
    # Step 7: Validate final features
    is_valid, missing_features = validate_final_features_production(df)
    
    if not is_valid:
        print(f"❌ Pipeline failed - missing features: {missing_features}")
        return None
    
    # Step 8: Extract final feature set
    final_features = [
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
    
    # Keep ID columns for reference
    id_columns = ['cliente', 'identificador_unico']
    available_id_cols = [col for col in id_columns if col in df.columns]
    
    # Create final dataset with proper naming
    final_columns = available_id_cols + final_features
    df_clientes_clean_final = df[final_columns].copy()

    # Save to CSV if output path provided
    if output_path:
        print(f"💾 Saving df_clientes_clean_final to: {output_path}")
        df_clientes_clean_final.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ File saved successfully!")

    print(f"\n🎉 PRODUCTION PIPELINE PART 1 COMPLETED!")
    print(f"📊 df_clientes_clean_final shape: {df_clientes_clean_final.shape}")
    print(f"🔧 Features ready for Part 2 (model inference): {len(final_features)}")
    print(f"📋 Next step: Load df_clientes_clean_final in Part 2 for predictions")

    return df_clientes_clean_final

# =============================================================================
# USAGE EXAMPLE - PRODUCTION PIPELINE PART 1
# =============================================================================
if __name__ == "__main__":
    # Input file path (raw production data)
    input_file_path = r'C:\Users\david\OneDrive\Documents\augment-projects\caja-de-ahorros\data\production\final_info_clientes.csv'

    # Output file path (cleaned data for Part 2)
    output_file_path = r'C:\Users\david\OneDrive\Documents\augment-projects\caja-de-ahorros\data\production\df_clientes_clean_final.csv'

    # Run Part 1 pipeline
    df_clientes_clean_final = production_pipeline_part1_main(input_file_path, output_file_path)

    if df_clientes_clean_final is not None:
        print(f"\n📋 df_clientes_clean_final PREVIEW:")
        print(df_clientes_clean_final.head())
        print(f"\n📊 FEATURE SUMMARY:")
        print(df_clientes_clean_final.describe())
        print(f"\n🎯 READY FOR PART 2: Model inference pipeline")
        print(f"📂 Load df_clientes_clean_final.csv in Part 2 for predictions")
        
# =============================================================================
# PRODUCTION PIPELINE PART 2 - FINAL FEATURE PREPARATION FOR MODEL
# =============================================================================

def production_pipeline_part2_main(df_clientes_clean_final_path=None, df_clientes_clean_final=None):
    """
    Production Pipeline PART 2 - Prepare final dataset for model inference
    Creates 'data_to_predict' with exactly the 10 features the model expects

    Parameters:
    - df_clientes_clean_final_path: Path to CSV file from Part 1
    - df_clientes_clean_final: DataFrame from Part 1 (if already loaded)
    """
    print("🚀 STARTING PRODUCTION PIPELINE - PART 2")
    print("="*80)
    print("🎯 OBJECTIVE: Create 'data_to_predict' with final 10 model features")
    print("📋 INPUT: df_clientes_clean_final (from Part 1)")
    print("📋 OUTPUT: data_to_predict (ready for model inference)")
    print("="*80)

    # Load data if path provided
    if df_clientes_clean_final is None:
        if df_clientes_clean_final_path is None:
            print("❌ Error: Must provide either df_clientes_clean_final_path or df_clientes_clean_final")
            return None

        print(f"📂 Loading df_clientes_clean_final from: {df_clientes_clean_final_path}")
        df_clientes_clean_final = pd.read_csv(df_clientes_clean_final_path)
        print(f"✅ Data loaded: {df_clientes_clean_final.shape}")

    # Work with a copy
    df_working = df_clientes_clean_final.copy()
    print(f"📊 Working with dataset: {df_working.shape}")

    # Validate that we have the required features from Part 1
    required_from_part1 = [
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

    print("🔍 Validating features from Part 1...")
    missing_features = []
    for feature in required_from_part1:
        if feature not in df_working.columns:
            missing_features.append(feature)
            print(f"   ❌ Missing: {feature}")
        else:
            print(f"   ✅ Found: {feature}")

    if missing_features:
        print(f"❌ ERROR: Missing required features from Part 1: {missing_features}")
        print("💡 Make sure to run Part 1 pipeline first!")
        return None

    # Extract ID columns (preserve for final output)
    id_columns = []
    for col in ['cliente', 'identificador_unico']:
        if col in df_working.columns:
            id_columns.append(col)
            print(f"   🆔 ID column found: {col}")

    if not id_columns:
        print("⚠️ Warning: No ID columns found - will use row index")
        df_working['row_id'] = df_working.index
        id_columns = ['row_id']

    # Create final feature set for model
    final_model_features = [
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

    print(f"\n🎯 Creating final dataset with {len(final_model_features)} model features...")

    # Create data_to_predict with ID columns + model features
    final_columns = id_columns + final_model_features
    data_to_predict = df_working[final_columns].copy()

    # Final validation and cleanup
    print("🔧 Final validation and cleanup...")

    # Check for missing values in model features
    for feature in final_model_features:
        missing_count = data_to_predict[feature].isnull().sum()
        if missing_count > 0:
            print(f"   ⚠️ {feature}: {missing_count} missing values")

            # Fill missing values appropriately
            if data_to_predict[feature].dtype in ['int64', 'int32', 'float64', 'float32']:
                median_val = data_to_predict[feature].median()
                data_to_predict[feature] = data_to_predict[feature].fillna(median_val)
                print(f"      ✅ Filled with median: {median_val:.2f}")
            else:
                mode_val = data_to_predict[feature].mode().iloc[0] if len(data_to_predict[feature].mode()) > 0 else 0
                data_to_predict[feature] = data_to_predict[feature].fillna(mode_val)
                print(f"      ✅ Filled with mode: {mode_val}")
        else:
            print(f"   ✅ {feature}: No missing values")

    # Ensure proper data types for model
    print("🔧 Optimizing data types for model inference...")
    for feature in final_model_features:
        if data_to_predict[feature].dtype == 'object':
            try:
                data_to_predict[feature] = pd.to_numeric(data_to_predict[feature], errors='coerce')
                data_to_predict[feature] = data_to_predict[feature].fillna(0)
                print(f"   ✅ {feature}: converted to numeric")
            except:
                print(f"   ⚠️ {feature}: could not convert to numeric")

        # Optimize numeric types
        if data_to_predict[feature].dtype in ['int64']:
            data_to_predict[feature] = data_to_predict[feature].astype('int32')
        elif data_to_predict[feature].dtype in ['float64']:
            data_to_predict[feature] = data_to_predict[feature].astype('float32')

    # Final summary
    print(f"\n🎉 PRODUCTION PIPELINE PART 2 COMPLETED!")
    print(f"📊 data_to_predict shape: {data_to_predict.shape}")
    print(f"🆔 ID columns: {id_columns}")
    print(f"🎯 Model features: {len(final_model_features)}")
    print(f"📋 Ready for model inference!")

    # Show feature summary
    print(f"\n📊 FEATURE SUMMARY:")
    for feature in final_model_features:
        dtype = data_to_predict[feature].dtype
        min_val = data_to_predict[feature].min()
        max_val = data_to_predict[feature].max()
        print(f"   {feature}: {dtype} [{min_val:.2f}, {max_val:.2f}]")

    return data_to_predict

def production_pipeline_complete(input_file_path, output_part1_path=None, output_part2_path=None):
    """
    Complete production pipeline - Part 1 + Part 2
    """
    print("🚀 COMPLETE PRODUCTION PIPELINE")
    print("="*80)

    # Part 1: Data cleaning and feature engineering
    print("🔧 RUNNING PART 1...")
    df_clientes_clean_final = production_pipeline_part1_main(input_file_path, output_part1_path)

    if df_clientes_clean_final is None:
        print("❌ Part 1 failed!")
        return None, None

    # Part 2: Final feature preparation
    print("\n🎯 RUNNING PART 2...")
    data_to_predict = production_pipeline_part2_main(df_clientes_clean_final=df_clientes_clean_final)

    if data_to_predict is None:
        print("❌ Part 2 failed!")
        return df_clientes_clean_final, None

    # Save Part 2 output if path provided
    if output_part2_path:
        print(f"💾 Saving data_to_predict to: {output_part2_path}")
        data_to_predict.to_csv(output_part2_path, index=False, encoding='utf-8')
        print(f"✅ File saved successfully!")

    print(f"\n🎉 COMPLETE PIPELINE FINISHED!")
    print(f"📊 df_clientes_clean_final: {df_clientes_clean_final.shape}")
    print(f"🎯 data_to_predict: {data_to_predict.shape}")
    print(f"📋 Ready for model inference!")

    return df_clientes_clean_final, data_to_predict

# =============================================================================
# PRODUCTION PIPELINE PART 3 - MODEL INFERENCE
# =============================================================================

def production_pipeline_part3_inference(data_to_predict_path=None, data_to_predict=None,
                                       model_path=None, output_path=None):
    """
    Production Pipeline PART 3 - Model Inference
    Loads trained model and makes income predictions

    Parameters:
    - data_to_predict_path: Path to CSV file from Part 2
    - data_to_predict: DataFrame from Part 2 (if already loaded)
    - model_path: Path to trained model file (.pkl)
    - output_path: Path to save predictions CSV
    """
    print("🚀 STARTING PRODUCTION PIPELINE - PART 3")
    print("="*80)
    print("🎯 OBJECTIVE: Load model and make income predictions")
    print("📋 INPUT: data_to_predict (from Part 2)")
    print("📋 OUTPUT: predictions with customer IDs")
    print("="*80)

    # Libraries already imported at top of file
    print("✅ Model loading libraries available")

    # Load data if path provided
    if data_to_predict is None:
        if data_to_predict_path is None:
            print("❌ Error: Must provide either data_to_predict_path or data_to_predict")
            return None

        print(f"📂 Loading data_to_predict from: {data_to_predict_path}")
        data_to_predict = pd.read_csv(data_to_predict_path)
        print(f"✅ Data loaded: {data_to_predict.shape}")

    # Set default model path if not provided
    if model_path is None:
        model_path = r'C:\Users\david\OneDrive\Documents\augment-projects\caja-de-ahorros\models\production\final_production_model_nested_cv.pkl'
        print(f"📋 Using default model path: {model_path}")

    # Load the trained model
    print(f"🤖 Loading trained model from: {model_path}")
    try:
        # Try joblib first (recommended for scikit-learn models)
        try:
            loaded_object = joblib.load(model_path)
            print("✅ Model file loaded successfully with joblib")
        except:
            # Fallback to pickle
            with open(model_path, 'rb') as f:
                loaded_object = pickle.load(f)
            print("✅ Model file loaded successfully with pickle")

        # Handle different model storage formats
        print(f"🔍 Analyzing loaded object type: {type(loaded_object)}")

        if hasattr(loaded_object, 'predict'):
            # Direct model object
            model = loaded_object
            print("✅ Direct model object found")
        elif isinstance(loaded_object, dict):
            # Dictionary containing model - try common keys
            print("🔍 Dictionary detected, searching for model...")
            possible_keys = ['model', 'best_model', 'final_model', 'estimator', 'regressor']
            model = None

            for key in possible_keys:
                if key in loaded_object and hasattr(loaded_object[key], 'predict'):
                    model = loaded_object[key]
                    print(f"✅ Model found in dictionary key: '{key}'")
                    break

            if model is None:
                # Print available keys for debugging
                print(f"🔍 Available keys in dictionary: {list(loaded_object.keys())}")
                # Try the first object that has predict method
                for key, value in loaded_object.items():
                    if hasattr(value, 'predict'):
                        model = value
                        print(f"✅ Model found in key: '{key}'")
                        break

                if model is None:
                    print("❌ No model with 'predict' method found in dictionary")
                    return None
        else:
            print(f"❌ Unsupported model format: {type(loaded_object)}")
            return None

    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("💡 Make sure the model file exists and is accessible")
        return None

    # Separate ID columns from features
    id_columns = []
    for col in ['cliente', 'identificador_unico', 'row_id']:
        if col in data_to_predict.columns:
            id_columns.append(col)

    print(f"🆔 ID columns found: {id_columns}")

    # Get model features (exclude ID columns)
    model_features = [col for col in data_to_predict.columns if col not in id_columns]
    print(f"🎯 Model features: {len(model_features)}")

    # Validate we have exactly 10 features
    expected_features = [
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

    print("🔍 Validating model features...")
    missing_features = []
    for feature in expected_features:
        if feature not in model_features:
            missing_features.append(feature)
            print(f"   ❌ Missing: {feature}")
        else:
            print(f"   ✅ Found: {feature}")

    if missing_features:
        print(f"❌ ERROR: Missing model features: {missing_features}")
        return None

    if len(model_features) != 10:
        print(f"⚠️ Warning: Expected 10 features, found {len(model_features)}")
        print(f"   Features: {model_features}")

    # Prepare feature matrix for prediction
    print("🔧 Preparing feature matrix for prediction...")
    X_predict = data_to_predict[expected_features].copy()

    # Final data validation
    print("🔍 Final data validation...")

    # Check for missing values
    missing_summary = X_predict.isnull().sum()
    if missing_summary.sum() > 0:
        print("⚠️ Missing values found:")
        for feature, missing_count in missing_summary.items():
            if missing_count > 0:
                print(f"   {feature}: {missing_count} missing")

        # Fill missing values
        print("🔧 Filling missing values...")
        X_predict = X_predict.fillna(X_predict.median())
        print("✅ Missing values filled with median")

    # Check data types
    print("🔧 Validating data types...")
    for feature in expected_features:
        if X_predict[feature].dtype == 'object':
            print(f"⚠️ Converting {feature} from object to numeric")
            X_predict[feature] = pd.to_numeric(X_predict[feature], errors='coerce').fillna(0)

    print(f"✅ Feature matrix ready: {X_predict.shape}")

    # Make predictions
    print("🎯 Making income predictions...")
    try:
        predictions = model.predict(X_predict)
        print(f"✅ Predictions completed: {len(predictions)} customers")

        # Basic prediction statistics
        print(f"📊 Prediction Statistics:")
        print(f"   Mean predicted income: ${predictions.mean():,.2f}")
        print(f"   Median predicted income: ${np.median(predictions):,.2f}")
        print(f"   Min predicted income: ${predictions.min():,.2f}")
        print(f"   Max predicted income: ${predictions.max():,.2f}")
        print(f"   Std predicted income: ${predictions.std():,.2f}")

    except Exception as e:
        print(f"❌ Error making predictions: {e}")
        return None

    # Create results DataFrame
    print("📋 Creating results DataFrame...")

    # Start with ID columns
    results_df = data_to_predict[id_columns].copy()

    # Add predictions
    results_df['predicted_income'] = predictions

    # Add confidence intervals if available
    if 'confidence_intervals' in loaded_object:
        ci_info = loaded_object['confidence_intervals']
        confidence_level = ci_info['confidence_level']
        ci_lower_offset = ci_info['ci_lower_offset']
        ci_upper_offset = ci_info['ci_upper_offset']

        # Calculate confidence intervals for each prediction
        results_df['income_lower_90'] = predictions + ci_lower_offset
        results_df['income_upper_90'] = predictions + ci_upper_offset
        results_df['confidence_level'] = f"{confidence_level*100:.0f}%"

        print(f"✅ Confidence intervals added:")
        print(f"   📊 Confidence Level: {confidence_level*100:.0f}%")
        print(f"   📉 Average lower bound: ${(predictions + ci_lower_offset).mean():,.2f}")
        print(f"   📈 Average upper bound: ${(predictions + ci_upper_offset).mean():,.2f}")
        print(f"   📊 Average CI width: ${ci_upper_offset - ci_lower_offset:.2f}")
    else:
        print("⚠️ No confidence intervals found in model - predictions without uncertainty estimates")

    # Add prediction metadata
    results_df['prediction_date'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    results_df['model_version'] = 'final_production_model_nested_cv'

    # Round predictions to 2 decimal places
    results_df['predicted_income'] = results_df['predicted_income'].round(2)

    # Round confidence intervals if they exist
    if 'income_lower_90' in results_df.columns:
        results_df['income_lower_90'] = results_df['income_lower_90'].round(2)
        results_df['income_upper_90'] = results_df['income_upper_90'].round(2)

    print(f"✅ Results DataFrame created: {results_df.shape}")

    # Save results if output path provided
    if output_path:
        print(f"💾 Saving predictions to: {output_path}")
        results_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ Predictions saved successfully!")

    # Show sample results
    print(f"\n📋 SAMPLE PREDICTIONS:")
    if 'income_lower_90' in results_df.columns:
        # Show predictions with confidence intervals
        sample_cols = ['cliente', 'identificador_unico', 'predicted_income', 'income_lower_90', 'income_upper_90', 'confidence_level']
        available_cols = [col for col in sample_cols if col in results_df.columns]
        print(results_df[available_cols].head(10))
    else:
        # Show predictions without confidence intervals
        sample_cols = ['cliente', 'identificador_unico', 'predicted_income'] if 'cliente' in results_df.columns else ['predicted_income']
        print(results_df[sample_cols].head(10))

    print(f"\n🎉 PRODUCTION PIPELINE PART 3 COMPLETED!")
    print(f"📊 Predictions made for {len(results_df)} customers")
    print(f"💰 Average predicted income: ${results_df['predicted_income'].mean():,.2f}")

    # Show confidence interval summary if available
    if 'income_lower_90' in results_df.columns:
        avg_lower = results_df['income_lower_90'].mean()
        avg_upper = results_df['income_upper_90'].mean()
        print(f"📊 Average 90% confidence interval: ${avg_lower:,.2f} - ${avg_upper:,.2f}")
        print(f"📈 Average uncertainty range: ±${(avg_upper - avg_lower)/2:,.2f}")

    print(f"📋 Results include customer IDs for easy tracking")

    return results_df

def production_pipeline_complete_with_inference(input_file_path, model_path=None,
                                              output_part1_path=None, output_part2_path=None,
                                              output_predictions_path=None):
    """
    Complete production pipeline - Part 1 + Part 2 + Part 3 (with inference)
    From raw data to final income predictions
    """
    print("🚀 COMPLETE PRODUCTION PIPELINE WITH INFERENCE")
    print("="*80)
    print("🎯 OBJECTIVE: Raw data → Income predictions")
    print("📋 PIPELINE: Part 1 (cleaning) → Part 2 (features) → Part 3 (inference)")
    print("="*80)

    # Part 1: Data cleaning and feature engineering
    print("🔧 RUNNING PART 1 - DATA CLEANING & FEATURE ENGINEERING...")
    df_clientes_clean_final = production_pipeline_part1_main(input_file_path, output_part1_path)

    if df_clientes_clean_final is None:
        print("❌ Part 1 failed!")
        return None, None, None

    # Part 2: Final feature preparation
    print("\n🎯 RUNNING PART 2 - FINAL FEATURE PREPARATION...")
    data_to_predict = production_pipeline_part2_main(df_clientes_clean_final=df_clientes_clean_final)

    if data_to_predict is None:
        print("❌ Part 2 failed!")
        return df_clientes_clean_final, None, None

    # Save Part 2 output if path provided
    if output_part2_path:
        print(f"💾 Saving data_to_predict to: {output_part2_path}")
        data_to_predict.to_csv(output_part2_path, index=False, encoding='utf-8')
        print(f"✅ File saved successfully!")

    # Part 3: Model inference
    print("\n🤖 RUNNING PART 3 - MODEL INFERENCE...")
    predictions_df = production_pipeline_part3_inference(
        data_to_predict=data_to_predict,
        model_path=model_path,
        output_path=output_predictions_path
    )

    if predictions_df is None:
        print("❌ Part 3 failed!")
        return df_clientes_clean_final, data_to_predict, None

    print(f"\n🎉 COMPLETE PIPELINE WITH INFERENCE FINISHED!")
    print(f"📊 Raw data: {df_clientes_clean_final.shape}")
    print(f"🎯 Features: {data_to_predict.shape}")
    print(f"💰 Predictions: {predictions_df.shape}")
    print(f"📋 Average predicted income: ${predictions_df['predicted_income'].mean():,.2f}")

    return df_clientes_clean_final, data_to_predict, predictions_df

# =============================================================================
# MAIN EXECUTION - COMPLETE PRODUCTION PIPELINE
# =============================================================================

def main():
    """
    Main execution function for production pipeline
    """
    print("🎯 INCOME PREDICTION PRODUCTION PIPELINE")
    print("="*80)
    print("🚀 Choose execution mode:")
    print("1. Complete Pipeline with Inference (Recommended)")
    print("2. Part 1 Only (Data cleaning)")
    print("3. Part 2 Only (Feature preparation)")
    print("4. Part 3 Only (Model inference)")
    print("="*80)

    # File paths configuration
    base_path = r'C:\Users\david\OneDrive\Documents\augment-projects\caja-de-ahorros'

    # Input files
    input_file_path = os.path.join(base_path, 'data', 'production', 'final_info_clientes.csv')
    model_path = os.path.join(base_path, 'models', 'production', 'final_production_model_nested_cv.pkl')

    # Output files
    output_part1_path = os.path.join(base_path, 'data', 'production', 'df_clientes_clean_final.csv')
    output_part2_path = os.path.join(base_path, 'data', 'production', 'data_to_predict.csv')
    output_predictions_path = os.path.join(base_path, 'data', 'production', 'income_predictions.csv')

    print(f"📂 Input file: {input_file_path}")
    print(f"🤖 Model file: {model_path}")
    print(f"📊 Output predictions: {output_predictions_path}")
    print("="*80)

    # Check if input file exists
    if not os.path.exists(input_file_path):
        print(f"❌ ERROR: Input file not found: {input_file_path}")
        print("💡 Please ensure the input file exists before running the pipeline")
        return None

    # Check if model file exists
    if not os.path.exists(model_path):
        print(f"❌ ERROR: Model file not found: {model_path}")
        print("💡 Please ensure the trained model file exists")
        return None

    # Execute complete pipeline
    print("🚀 EXECUTING COMPLETE PIPELINE WITH INFERENCE...")
    print("="*80)

    try:
        df_clean, data_predict, predictions = production_pipeline_complete_with_inference(
            input_file_path=input_file_path,
            model_path=model_path,
            output_part1_path=output_part1_path,
            output_part2_path=output_part2_path,
            output_predictions_path=output_predictions_path
        )

        if predictions is not None:
            print("\n" + "="*80)
            print("🎉 PIPELINE EXECUTION SUCCESSFUL!")
            print("="*80)

            print(f"📊 PROCESSING SUMMARY:")
            print(f"   • Customers processed: {len(predictions)}")
            print(f"   • Features engineered: 10 model features")
            print(f"   • Predictions generated: {len(predictions)}")

            print(f"\n💰 PREDICTION RESULTS:")
            print(f"   • Average income: ${predictions['predicted_income'].mean():,.2f}")
            print(f"   • Median income: ${predictions['predicted_income'].median():,.2f}")
            print(f"   • Income range: ${predictions['predicted_income'].min():,.2f} - ${predictions['predicted_income'].max():,.2f}")

            # Show confidence interval summary if available
            if 'income_lower_90' in predictions.columns:
                avg_lower = predictions['income_lower_90'].mean()
                avg_upper = predictions['income_upper_90'].mean()
                print(f"   • Average 90% CI: ${avg_lower:,.2f} - ${avg_upper:,.2f}")
                print(f"   • Average uncertainty: ±${(avg_upper - avg_lower)/2:,.2f}")

            print(f"\n📂 FILES GENERATED:")
            print(f"   ✅ {output_part1_path}")
            print(f"   ✅ {output_part2_path}")
            print(f"   ✅ {output_predictions_path}")

            print(f"\n📋 SAMPLE PREDICTIONS:")
            if 'income_lower_90' in predictions.columns:
                sample_cols = ['cliente', 'identificador_unico', 'predicted_income', 'income_lower_90', 'income_upper_90']
                available_cols = [col for col in sample_cols if col in predictions.columns]
                print(predictions[available_cols].head())
            else:
                sample_cols = ['cliente', 'identificador_unico', 'predicted_income'] if 'cliente' in predictions.columns else ['predicted_income']
                print(predictions[sample_cols].head())

            print(f"\n🎯 NEXT STEPS:")
            print(f"   • Review predictions in: {output_predictions_path}")
            print(f"   • Use customer IDs to link predictions to business processes")
            print(f"   • Monitor model performance over time")

            return predictions
        else:
            print("❌ Pipeline execution failed!")
            return None

    except Exception as e:
        print(f"❌ ERROR during pipeline execution: {e}")
        print("💡 Check input data format and model file compatibility")
        return None

if __name__ == "__main__":
    # Execute main pipeline
    results = main()

    if results is not None:
        print(f"\n🎉 PRODUCTION PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"📊 {len(results)} income predictions generated")
        print(f"💰 Ready for business use!")
    else:
        print(f"\n❌ PRODUCTION PIPELINE FAILED!")
        print(f"💡 Check error messages above for troubleshooting")
