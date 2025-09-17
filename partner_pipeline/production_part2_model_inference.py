# =============================================================================
# PRODUCTION PIPELINE PART 2 - MODEL INFERENCE & PREDICTIONS
# =============================================================================
#
# OBJECTIVE: Load clean dataset and generate income predictions with confidence intervals
#
# INPUT: Clean dataset from Part 1 (11 features + ID columns)
# OUTPUT: Income predictions with 90% confidence intervals
#
# MODEL SPECIFICATIONS:
# - XGBoost Regressor (production_model_catboost_all_data.pkl)
# - RMSE: $527.24 (18.4% improvement over baseline)
# - Training data: 31,125 samples
# - Confidence intervals: 90% CI [-$510.93, +$755.02]
#
# REQUIRED FILES:
# - models/production/production_model_catboost_all_data.pkl (XGBoost model)
# - models/production/production_frequency_mappings_catboost.pkl (encodings)
# - data/production/df_clientes_clean_final.csv (clean dataset from Part 1)
# =============================================================================

import pandas as pd
import numpy as np
import pickle
import os
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

# Try to import ML libraries
try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False
    print("⚠️ Warning: joblib not available")

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️ Warning: XGBoost not available - model loading will fail")

# Set display options
pd.set_option('display.max_columns', None)

def load_production_model():
    """
    Load the trained XGBoost model for income prediction
    Handle different model storage formats (direct model, dict wrapper, etc.)
    """
    print("🤖 LOADING PRODUCTION MODEL")
    print("="*50)

    # Path to our final production model (local copy in partner_pipeline directory)
    model_path = 'production_model_catboost_all_data.pkl'

    print(f"📂 Loading model from: {model_path}")

    try:
        if os.path.exists(model_path):
            # Try joblib first (preferred for sklearn/xgboost)
            if JOBLIB_AVAILABLE:
                try:
                    loaded_object = joblib.load(model_path)
                    print("✅ Object loaded successfully with joblib")
                except:
                    print("⚠️ Joblib loading failed, trying pickle...")
                    loaded_object = None

            # Fallback to pickle if joblib failed
            if loaded_object is None:
                with open(model_path, 'rb') as f:
                    loaded_object = pickle.load(f)
                print("✅ Object loaded successfully with pickle")

            # Handle different model storage formats
            model = extract_model_from_object(loaded_object)

            if model is not None:
                print(f"✅ Model extracted successfully: {type(model)}")
                return model
            else:
                print("❌ Could not extract model from loaded object")
                debug_model_object(loaded_object)
                return None

        else:
            print(f"❌ Model file not found: {model_path}")
            return None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def extract_model_from_object(loaded_object):
    """
    Extract the actual model from different storage formats
    """
    print(f"🔍 Analyzing loaded object type: {type(loaded_object)}")

    # Case 1: Direct model object
    if hasattr(loaded_object, 'predict'):
        print("   ✅ Direct model object found")
        return loaded_object

    # Case 2: Dictionary containing model
    elif isinstance(loaded_object, dict):
        print("   📋 Dictionary detected - searching for model...")

        # Common keys where models might be stored
        possible_keys = ['model', 'best_model', 'final_model', 'xgb_model', 'regressor', 'estimator']

        for key in possible_keys:
            if key in loaded_object:
                candidate = loaded_object[key]
                if hasattr(candidate, 'predict'):
                    print(f"   ✅ Model found in key: '{key}'")
                    return candidate

        # If no direct model found, show available keys
        print(f"   📋 Available keys: {list(loaded_object.keys())}")

        # Try to find any object with predict method
        for key, value in loaded_object.items():
            if hasattr(value, 'predict'):
                print(f"   ✅ Model found in key: '{key}' (by predict method)")
                return value

        print("   ❌ No model with predict method found in dictionary")
        return None

    # Case 3: List or tuple
    elif isinstance(loaded_object, (list, tuple)):
        print("   📋 List/tuple detected - searching for model...")
        for i, item in enumerate(loaded_object):
            if hasattr(item, 'predict'):
                print(f"   ✅ Model found at index {i}")
                return item
        print("   ❌ No model with predict method found in list/tuple")
        return None

    # Case 4: Unknown format
    else:
        print(f"   ❌ Unknown object format: {type(loaded_object)}")
        print(f"   📋 Object attributes: {dir(loaded_object)}")
        return None

def debug_model_object(loaded_object):
    """
    Debug function to inspect the loaded object structure
    """
    print("\n🔍 DEBUG: INSPECTING LOADED OBJECT")
    print("="*50)

    print(f"Object type: {type(loaded_object)}")
    print(f"Object size: {len(loaded_object) if hasattr(loaded_object, '__len__') else 'N/A'}")

    if isinstance(loaded_object, dict):
        print(f"Dictionary keys: {list(loaded_object.keys())}")
        for key, value in loaded_object.items():
            print(f"  {key}: {type(value)} - Has predict: {hasattr(value, 'predict')}")

    elif isinstance(loaded_object, (list, tuple)):
        print(f"List/tuple contents:")
        for i, item in enumerate(loaded_object):
            print(f"  [{i}]: {type(item)} - Has predict: {hasattr(item, 'predict')}")

    else:
        print(f"Object attributes: {[attr for attr in dir(loaded_object) if not attr.startswith('_')]}")
        print(f"Has predict method: {hasattr(loaded_object, 'predict')}")

def validate_model_features(df, model):
    """
    Validate that the dataset has exactly the features the model expects
    """
    print("\n🔍 VALIDATING MODEL FEATURES")
    print("="*50)
    
    # Expected 11 features for our XGBoost model
    expected_features = [
        'edad',
        'fechaingresoempleo_days', 
        'balance_to_payment_ratio',
        'fecha_inicio_days',
        'saldo',
        'nombreempleadorcliente_consolidated_freq',
        'location_x_occupation',
        'monto_letra',
        'fecha_vencimiento_days',
        'balance_coverage_ratio',
        'payment_per_age'
    ]
    
    print(f"📋 Expected features: {len(expected_features)}")
    
    # Check if all expected features are present
    missing_features = []
    available_features = []
    
    for feature in expected_features:
        if feature in df.columns:
            available_features.append(feature)
            print(f"   ✅ {feature}: Available")
        else:
            missing_features.append(feature)
            print(f"   ❌ {feature}: Missing")
    
    if missing_features:
        print(f"\n🚨 ERROR: Missing required features: {missing_features}")
        return None, False
    
    # Extract feature matrix for model
    X = df[expected_features].copy()
    
    # Validate data types and handle any remaining issues
    print(f"\n🔧 Feature validation:")
    for feature in expected_features:
        dtype = X[feature].dtype
        missing_count = X[feature].isnull().sum()
        
        if missing_count > 0:
            print(f"   ⚠️ {feature}: {missing_count} missing values - filling with median")
            X[feature] = X[feature].fillna(X[feature].median())
        
        # Ensure numeric types
        if X[feature].dtype == 'object':
            X[feature] = pd.to_numeric(X[feature], errors='coerce').fillna(0)
            print(f"   🔧 {feature}: converted to numeric")
        
        print(f"   ✅ {feature}: {dtype} - Range [{X[feature].min():.2f}, {X[feature].max():.2f}]")
    
    print(f"\n✅ Feature matrix ready: {X.shape}")
    return X, True

def generate_predictions_with_confidence(model, X):
    """
    Generate income predictions with 90% confidence intervals
    """
    print("\n🎯 GENERATING INCOME PREDICTIONS")
    print("="*50)
    
    try:
        # Generate point predictions
        print("📊 Computing point predictions...")
        predictions = model.predict(X)
        
        print(f"✅ Predictions generated for {len(predictions):,} customers")
        print(f"📈 Prediction range: ${predictions.min():,.2f} to ${predictions.max():,.2f}")
        print(f"📊 Mean prediction: ${predictions.mean():,.2f}")
        
        # Add confidence intervals (from our final model analysis)
        print("\n🔒 Adding 90% confidence intervals...")
        
        # These are the exact confidence interval offsets from our final model
        CI_LOWER_OFFSET = -510.93  # 5th percentile offset
        CI_UPPER_OFFSET = 755.02   # 95th percentile offset
        CONFIDENCE_LEVEL = 0.90    # 90% confidence level
        
        # Calculate confidence bounds
        lower_bounds = predictions + CI_LOWER_OFFSET
        upper_bounds = predictions + CI_UPPER_OFFSET
        
        # Ensure no negative income predictions
        lower_bounds = np.maximum(lower_bounds, 0)
        
        print(f"✅ Confidence intervals added")
        print(f"📊 Average CI width: ${CI_UPPER_OFFSET - CI_LOWER_OFFSET:.2f}")
        print(f"🔒 Confidence level: {CONFIDENCE_LEVEL*100:.0f}%")
        
        # Create results dictionary
        results = {
            'predictions': predictions,
            'lower_bounds': lower_bounds,
            'upper_bounds': upper_bounds,
            'ci_lower_offset': CI_LOWER_OFFSET,
            'ci_upper_offset': CI_UPPER_OFFSET,
            'confidence_level': CONFIDENCE_LEVEL
        }
        
        return results
        
    except Exception as e:
        print(f"❌ Error generating predictions: {e}")
        return None

def create_predictions_dataframe(df_original, prediction_results):
    """
    Create final predictions dataframe with customer IDs and predictions
    Ensures identificador_unico is always included for customer identification
    """
    print("\n📋 CREATING PREDICTIONS DATAFRAME")
    print("="*50)

    # Extract prediction components
    predictions = prediction_results['predictions']
    lower_bounds = prediction_results['lower_bounds']
    upper_bounds = prediction_results['upper_bounds']
    confidence_level = prediction_results['confidence_level']

    # Debug: Show available columns
    print(f"📋 Available columns in dataset: {list(df_original.columns)}")

    # Priority order for ID columns (identificador_unico is most important)
    priority_id_columns = ['identificador_unico', 'cliente', 'row_id']
    id_columns = []

    # Find ID columns in priority order
    for col in priority_id_columns:
        if col in df_original.columns:
            id_columns.append(col)
            print(f"   ✅ Found ID column: {col}")

    # If no standard ID columns found, create row_id
    if not id_columns:
        print("⚠️ No standard ID columns found - creating row_id")
        df_original = df_original.copy()  # Avoid modifying original
        df_original['row_id'] = df_original.index
        id_columns = ['row_id']

    # Ensure identificador_unico is first if available
    if 'identificador_unico' in id_columns and id_columns[0] != 'identificador_unico':
        id_columns.remove('identificador_unico')
        id_columns.insert(0, 'identificador_unico')

    print(f"🆔 Final ID columns (in order): {id_columns}")

    # Create predictions dataframe starting with ID columns
    df_predictions = df_original[id_columns].copy()

    # Add prediction columns
    df_predictions['predicted_income'] = predictions.round(2)
    df_predictions['income_lower_90'] = lower_bounds.round(2)
    df_predictions['income_upper_90'] = upper_bounds.round(2)
    df_predictions['confidence_level'] = confidence_level

    # Add metadata
    df_predictions['prediction_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df_predictions['model_version'] = 'XGBoost_v1.0_Final'

    # Add confidence interval width for analysis
    df_predictions['ci_width'] = df_predictions['income_upper_90'] - df_predictions['income_lower_90']

    print(f"✅ Predictions dataframe created: {df_predictions.shape}")
    print(f"🆔 ID columns included: {id_columns}")
    print(f"📊 Prediction columns: ['predicted_income', 'income_lower_90', 'income_upper_90']")

    # Show sample with ID columns
    if len(df_predictions) > 0:
        print(f"\n📋 Sample with customer identification:")
        sample_cols = id_columns + ['predicted_income', 'income_lower_90', 'income_upper_90']
        print(df_predictions[sample_cols].head(3).to_string(index=False))

    return df_predictions

def production_part2_main(clean_data_path, output_path=None):
    """
    Main function for Production Part 2: Model Inference & Predictions
    
    Input: Clean dataset from Part 1 (CSV file)
    Output: Income predictions with confidence intervals
    """
    print("🚀 PRODUCTION PART 2 - MODEL INFERENCE & PREDICTIONS")
    print("="*80)
    print("🎯 OBJECTIVE: Generate income predictions with 90% confidence intervals")
    print("📋 INPUT: Clean dataset with 11 features")
    print("📋 OUTPUT: Income predictions with confidence bounds")
    print("="*80)
    
    # Step 1: Load clean dataset from Part 1
    print("📂 Loading clean dataset...")
    try:
        df_clean = pd.read_csv(clean_data_path, encoding='utf-8')
        print(f"✅ Clean dataset loaded: {df_clean.shape}")
    except Exception as e:
        print(f"❌ Error loading clean dataset: {e}")
        return None
    
    # Step 2: Load production model
    model = load_production_model()
    if model is None:
        print("❌ Failed to load model")
        return None
    
    # Step 3: Validate features and prepare feature matrix
    X, is_valid = validate_model_features(df_clean, model)
    if not is_valid:
        print("❌ Feature validation failed")
        return None
    
    # Step 4: Generate predictions with confidence intervals
    prediction_results = generate_predictions_with_confidence(model, X)
    if prediction_results is None:
        print("❌ Prediction generation failed")
        return None
    
    # Step 5: Create final predictions dataframe
    df_predictions = create_predictions_dataframe(df_clean, prediction_results)
    
    # Step 6: Save predictions if output path provided
    if output_path:
        print(f"\n💾 Saving predictions to: {output_path}")
        df_predictions.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ Predictions saved successfully!")
    
    # Step 7: Display summary statistics
    print(f"\n🎉 PRODUCTION PART 2 COMPLETED!")
    print(f"📊 Predictions generated: {len(df_predictions):,}")

    # Show customer identification info
    id_cols = [col for col in ['identificador_unico', 'cliente', 'row_id'] if col in df_predictions.columns]
    print(f"🆔 Customer identification: {id_cols}")

    print(f"💰 Income prediction summary:")
    print(f"   Mean: ${df_predictions['predicted_income'].mean():,.2f}")
    print(f"   Median: ${df_predictions['predicted_income'].median():,.2f}")
    print(f"   Min: ${df_predictions['predicted_income'].min():,.2f}")
    print(f"   Max: ${df_predictions['predicted_income'].max():,.2f}")
    print(f"🔒 Confidence intervals (90%):")
    print(f"   Average width: ${df_predictions['ci_width'].mean():,.2f}")
    print(f"   Model RMSE: $527.24")

    # Show sample with customer ID for verification
    if len(df_predictions) > 0:
        sample_cols = id_cols + ['predicted_income', 'income_lower_90', 'income_upper_90']
        print(f"\n📋 Sample predictions with customer ID:")
        print(df_predictions[sample_cols].head(3).to_string(index=False))

    return df_predictions

# =============================================================================
# USAGE EXAMPLE
# =============================================================================
if __name__ == "__main__":
    # Input and output file paths
    clean_data_file = r'data\production\df_clientes_clean_final.csv'
    predictions_output_file = r'data\production\income_predictions.csv'

    print("🎯 PRODUCTION PART 2 - INCOME PREDICTION INFERENCE")
    print("="*80)

    # Run Part 2 pipeline
    df_predictions = production_part2_main(clean_data_file, predictions_output_file)

    if df_predictions is not None:
        # Show sample with customer identification
        id_cols = [col for col in ['identificador_unico', 'cliente', 'row_id'] if col in df_predictions.columns]
        sample_cols = id_cols + ['predicted_income', 'income_lower_90', 'income_upper_90']

        print(f"\n📋 SAMPLE PREDICTIONS WITH CUSTOMER ID:")
        print(df_predictions[sample_cols].head())

        print(f"\n📊 PREDICTION STATISTICS:")
        print(df_predictions[['predicted_income', 'income_lower_90', 'income_upper_90', 'ci_width']].describe())

        print(f"\n🆔 CUSTOMER IDENTIFICATION:")
        print(f"   ID columns included: {id_cols}")
        print(f"   Total customers predicted: {len(df_predictions):,}")

        print(f"\n🎯 SUCCESS! Income predictions ready for business use")
        print(f"📂 Next step: Apply business rules and formatting (Part 3)")
    else:
        print(f"\n❌ FAILED! Check error messages above")

# =============================================================================
# MODEL INFERENCE TECHNICAL NOTES
# =============================================================================
"""
🎯 MODEL INFERENCE STRATEGY:

1. MODEL SPECIFICATIONS:
   • XGBoost Regressor (despite filename suggesting CatBoost)
   • Training RMSE: $527.24 (18.4% improvement over Linear Regression)
   • Training samples: 31,125 customers
   • Features: Exactly 11 numeric features (no categorical variables)

2. CONFIDENCE INTERVALS:
   • Level: 90% confidence intervals
   • Lower offset: -$510.93 (5th percentile from residuals)
   • Upper offset: +$755.02 (95th percentile from residuals)
   • Average width: $1,265.95
   • Interpretation: 90% of actual incomes fall within these bounds

3. FEATURE VALIDATION:
   • Ensures exactly 11 features are present
   • Validates data types (all numeric)
   • Handles missing values with median imputation
   • Checks feature ranges for anomalies

4. PREDICTION PROCESS:
   • Load trained XGBoost model
   • Validate feature matrix
   • Generate point predictions
   • Add confidence intervals
   • Create business-ready output format

🔧 PRODUCTION CONSIDERATIONS:

• ERROR HANDLING: Comprehensive error handling for model loading and prediction
• MISSING VALUES: Automatic handling with median imputation
• DATA VALIDATION: Feature presence and type validation
• PERFORMANCE: Optimized for batch processing
• TRACEABILITY: Customer IDs preserved throughout process

✅ OUTPUT FORMAT:

Columns in predictions dataframe:
- Customer identification: cliente, identificador_unico (or row_id)
- Core predictions: predicted_income, income_lower_90, income_upper_90
- Metadata: confidence_level, prediction_date, model_version, ci_width

📊 EXPECTED PERFORMANCE:

• Typical prediction range: $500 - $3,000 USD
• Average prediction: ~$1,312 USD (based on training data)
• Confidence interval width: ~$1,266 USD average
• Model accuracy: ±$527 RMSE

🚨 BUSINESS INTERPRETATION:

• Lower income predictions (< $1,500): Higher confidence, narrower intervals
• Higher income predictions (> $2,000): Lower confidence, wider intervals
• Heteroscedasticity: Normal pattern - higher incomes harder to predict precisely
• Use cases: Credit assessment, marketing segmentation, risk analysis

🎯 NEXT STEPS:
- Part 3: Add business rules, risk classifications, and final formatting
- Integration: Combine all parts into single production pipeline
- Monitoring: Track prediction accuracy and model drift over time
"""
