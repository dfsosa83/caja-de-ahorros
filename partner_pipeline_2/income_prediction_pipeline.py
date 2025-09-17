# =============================================================================
# INCOME PREDICTION PIPELINE - STANDALONE VERSION
# =============================================================================
#
# OBJECTIVE: Simple pipeline for income prediction
# INPUT: CSV file with customer data
# OUTPUT: Predictions with confidence intervals
#
# USAGE:
# python income_prediction_pipeline.py input_data.csv
#
# REQUIREMENTS:
# - input_data.csv: Customer data file
# - production_model_catboost_all_data.pkl: Trained model
# - production_frequency_mappings_catboost.pkl: Frequency mappings
# =============================================================================

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class PipelineConfig:
    """
    Pipeline configuration - Update paths for your environment
    """
    # 📁 MODEL FILES - Update these paths to your model files location
    MODEL_FILES = {
        "trained_model": "production_model_catboost_all_data.pkl",
        "frequency_mappings": "production_frequency_mappings_catboost.pkl",
    }
    
    # ⚙️ MODEL CONFIGURATION
    MODEL_CONFIG = {
        "confidence_level": 0.90,
        "ci_lower_offset": -510.93,  # From model analysis
        "ci_upper_offset": 755.02,   # From model analysis
    }

def run_income_prediction_pipeline(input_file):
    """
    Complete income prediction pipeline
    
    Args:
        input_file (str): Path to input CSV file
        
    Returns:
        pandas.DataFrame: Predictions with confidence intervals
    """
    
    print("🚀 INCOME PREDICTION PIPELINE")
    print("=" * 50)
    print(f"📁 Processing: {input_file}")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # Step 1: Load input data (supports CSV and JSON)
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # Detect file format and load accordingly
        if input_file.lower().endswith('.json'):
            import json
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            df_raw = pd.DataFrame(data)
            print(f"📊 Loaded {len(df_raw)} customers from JSON")
        else:
            df_raw = pd.read_csv(input_file)
            print(f"📊 Loaded {len(df_raw)} customers from CSV")

        # Step 2: Feature engineering
        print("🔧 Processing features...")
        from production_part1_data_cleaning import production_part1_main

        try:
            # Convert JSON to CSV if needed for feature engineering
            if input_file.lower().endswith('.json'):
                temp_input_file = "temp_input_data.csv"
                df_raw.to_csv(temp_input_file, index=False)
                input_for_processing = temp_input_file
            else:
                input_for_processing = input_file

            temp_clean_file = "temp_cleaned_data.csv"
            df_clean = production_part1_main(
                input_file_path=input_for_processing,
                output_file_path=temp_clean_file
            )
        except Exception as e:
            raise Exception(f"Feature engineering error: {str(e)}")

        if df_clean is None:
            raise Exception("Feature engineering returned None")

        # Step 3: Model prediction (suppress verbose output)
        print("🤖 Generating predictions...")
        from production_part2_model_inference import production_part2_main

        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            temp_pred_file = "temp_predictions.csv"
            df_predictions = production_part2_main(
                clean_data_path=temp_clean_file,
                output_path=temp_pred_file
            )
        finally:
            sys.stdout = old_stdout

        if df_predictions is None:
            raise Exception("Model prediction failed")

        # Step 4: Format results
        # Ensure confidence intervals exist
        if 'income_lower_90' not in df_predictions.columns:
            df_predictions['income_lower_90'] = (
                df_predictions['predicted_income'] + PipelineConfig.MODEL_CONFIG['ci_lower_offset']
            ).round(6)

        if 'income_upper_90' not in df_predictions.columns:
            df_predictions['income_upper_90'] = (
                df_predictions['predicted_income'] + PipelineConfig.MODEL_CONFIG['ci_upper_offset']
            ).round(6)
        
        # Select final columns
        final_columns = [
            'identificador_unico', 'cliente', 'predicted_income', 
            'income_lower_90', 'income_upper_90'
        ]
        
        # Ensure all columns exist
        for col in final_columns:
            if col not in df_predictions.columns:
                if col == 'cliente':
                    df_predictions['cliente'] = df_predictions.get('Cliente', 'N/A')
                elif col == 'identificador_unico':
                    df_predictions['identificador_unico'] = df_predictions.get('Identificador_Unico', 'N/A')
        
        df_final = df_predictions[final_columns].copy()
        
        # Clean up temporary files
        for temp_file in [temp_clean_file, temp_pred_file]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

        print("✅ Processing completed!")
        print()
        print("📊 PREDICTION RESULTS:")
        print("=" * 50)
        print(df_final.to_string(index=False))
        print()
        print(f"📈 Summary:")
        print(f"   👥 Total customers: {len(df_final)}")
        print(f"   💰 Average income: ${df_final['predicted_income'].mean():,.2f}")
        print(f"   📊 Income range: ${df_final['predicted_income'].min():,.2f} - ${df_final['predicted_income'].max():,.2f}")

        return df_final

    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        return None

def save_predictions(df_predictions, base_filename="predictions"):
    """
    Save predictions to both CSV and JSON formats

    Args:
        df_predictions: DataFrame with predictions
        base_filename: Base name for output files

    Returns:
        dict: Paths to saved files
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save CSV
    csv_file = f"{base_filename}_{timestamp}.csv"
    df_predictions.to_csv(csv_file, index=False)

    # Save JSON (more structured format)
    json_file = f"{base_filename}_{timestamp}.json"

    # Create structured JSON
    json_data = {
        "metadata": {
            "total_customers": len(df_predictions),
            "average_income": float(df_predictions['predicted_income'].mean()),
            "income_range": {
                "min": float(df_predictions['predicted_income'].min()),
                "max": float(df_predictions['predicted_income'].max())
            },
            "generated_at": datetime.now().isoformat(),
            "confidence_level": "90%"
        },
        "predictions": df_predictions.to_dict('records')
    }

    import json
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    return {
        "csv_file": csv_file,
        "json_file": json_file
    }

def main():
    """
    Main function for command line usage
    """
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python income_prediction_pipeline.py <input_file.csv> [--verbose]")
        print("Example: python income_prediction_pipeline.py customer_data.csv")
        print("         python income_prediction_pipeline.py customer_data.csv --verbose")
        sys.exit(1)

    input_file = sys.argv[1]
    verbose_mode = len(sys.argv) == 3 and sys.argv[2] == "--verbose"
    
    # Validate model files exist
    for file_type, file_path in PipelineConfig.MODEL_FILES.items():
        if not os.path.exists(file_path):
            print(f"❌ {file_type} not found: {file_path}")
            print("Please ensure model files are in the same directory as this script")
            sys.exit(1)
    
    # Run pipeline
    if verbose_mode:
        # Verbose mode with full output
        results = run_income_prediction_pipeline(input_file)

        if results is not None:
            # Save results to both CSV and JSON
            saved_files = save_predictions(results)
            print(f"💾 Results saved to:")
            print(f"   📄 CSV: {saved_files['csv_file']}")
            print(f"   📄 JSON: {saved_files['json_file']}")
            print()
            print("🎯 Quick Access:")
            print(f"   • Open CSV in Excel: {saved_files['csv_file']}")
            print(f"   • Use JSON for APIs: {saved_files['json_file']}")
        else:
            sys.exit(1)
    else:
        # Default: Clean mode with minimal output
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            results = run_income_prediction_pipeline(input_file)
        finally:
            sys.stdout = old_stdout

        if results is not None:
            # Show only the essential results
            print("📊 PREDICTION RESULTS:")
            print("=" * 50)
            print(results.to_string(index=False))
            print()
            print(f"📈 Summary:")
            print(f"   👥 Total customers: {len(results)}")
            print(f"   💰 Average income: ${results['predicted_income'].mean():,.2f}")
            print(f"   📊 Income range: ${results['predicted_income'].min():,.2f} - ${results['predicted_income'].max():,.2f}")

            # Save files quietly
            saved_files = save_predictions(results)
            print(f"💾 Saved: {saved_files['csv_file']}")
        else:
            print("❌ Pipeline failed")
            sys.exit(1)

if __name__ == "__main__":
    main()
