
# PRODUCTION PREDICTION CODE
# ==========================

import joblib
import pandas as pd
import numpy as np
import os

# Define models path (with proper path separator)
models_path = r'C:\Users\david\OneDrive\Documents\augment-projects\caja-de-ahorros\models\production'
# Read initial data
data_path = r'C:\Users\david\OneDrive\Documents\augment-projects\caja-de-ahorros\data\raw'


# CALL TRAINED MODEL
# ==========================
# Check if models directory exists
if not os.path.exists(models_path):
    print(f"❌ Models directory not found: {models_path}")
    print("Please check the path or create the directory")
    exit()

# Define full model file path (add missing slash)
model_file_path = os.path.join(models_path, 'final_production_model_nested_cv.pkl')

# Check if model file exists
if not os.path.exists(model_file_path):
    print(f"❌ Model file not found: {model_file_path}")
    print("Available files in models directory:")
    try:
        files = os.listdir(models_path)
        for file in files:
            if file.endswith('.pkl'):
                print(f"   📁 {file}")
    except:
        print("   No files found or directory doesn't exist")
    exit()

print(f"📁 Loading model from: {model_file_path}")

try:
    # Load production model artifacts
    artifacts = joblib.load(model_file_path)
    
    # Extract components
    model = artifacts['final_production_model']
    scaler = artifacts['final_scaler']
    feature_columns = artifacts['feature_columns']
    
    print("✅ Model artifacts loaded successfully!")
    print(f"   🤖 Model type: {type(model).__name__}")
    print(f"   ⚖️ Scaler type: {type(scaler).__name__}")
    print(f"   🔧 Features: {len(feature_columns)} columns")
    
    # Print model details
    print(f"\n🤖 MODEL DETAILS:")
    print("-" * 40)
    print(model)
    
    # Print feature columns
    print(f"\n📋 FEATURE COLUMNS ({len(feature_columns)}):")
    print("-" * 40)
    for i, feature in enumerate(feature_columns, 1):
        print(f"   {i:2d}. {feature}")
    
    # Print model metadata if available
    if 'training_info' in artifacts:
        training_info = artifacts['training_info']
        print(f"\n📊 TRAINING INFO:")
        print("-" * 40)
        for key, value in training_info.items():
            print(f"   {key}: {value}")
    
    if 'validation_performance' in artifacts:
        performance = artifacts['validation_performance']
        print(f"\n📈 EXPECTED PERFORMANCE:")
        print("-" * 40)
        for key, value in performance.items():
            if isinstance(value, float):
                print(f"   {key}: {value:.4f}")
            else:
                print(f"   {key}: {value}")

except FileNotFoundError:
    print(f"❌ Error: Model file not found at {model_file_path}")
except KeyError as e:
    print(f"❌ Error: Missing key in model artifacts: {e}")
    print("Available keys in artifacts:")
    try:
        for key in artifacts.keys():
            print(f"   📋 {key}")
    except:
        pass
except Exception as e:
    print(f"❌ Error loading model: {e}")

print(f"\n✅ Model validation complete!")

# PREPARE PRODUCTION DATA
# ==========================
# define initial df
df_clientes = pd.read_csv(data_path + '/Info_Cliente.csv', encoding='latin-1', sep=';', on_bad_lines='skip', engine='python')
print(f"Initial data shape: {df_clientes.shape}")

# %%
# 1.INITIAL DATASET VALIDATION
# =============================================================================
print("\n🔍 VALIDATING INITIAL DATASET COLUMNS")
print("-" * 50)

# Define expected initial columns (excluding target for production)
REQUIRED_INITIAL_COLUMNS = [
    'Cliente', 
    'Identificador_Unico', 
    'Segmento', 
    'Edad', 
    'Sexo', 
    'Ciudad', 
    'Pais', 
    'Ocupacion', 
    'Estado_Civil', 
    'FechaIngresoEmpleo', 
    'NombreEmpleadorCliente', 
    'CargoEmpleoCliente', 
    'productos_activos', 
    'letras_mensuales', 
    'monto_letra', 
    'saldo', 
    'fecha_inicio', 
    'fecha_vencimiento'
    # Note: 'ingresos_reportados' excluded - it's the target, not needed in production
]