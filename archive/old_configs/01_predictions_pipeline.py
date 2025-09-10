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
warnings.filterwarnings('ignore')

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
