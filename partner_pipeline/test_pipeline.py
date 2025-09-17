# =============================================================================
# SIMPLE PIPELINE TEST
# =============================================================================
#
# Run this after activating your environment:
# 1. mamba activate income-prediction
# 2. python test_pipeline.py
#
# =============================================================================

import sys
import os

def test_pipeline():
    """
    Simple test of the income prediction pipeline
    """
    
    print("🧪 TESTING INCOME PREDICTION PIPELINE")
    print("=" * 50)
    
    try:
        # Test 1: Import check
        print("📋 Test 1: Checking imports...")
        import pandas as pd
        import numpy as np
        print("✅ pandas and numpy imported successfully")
        
        # Test 2: Check if files exist
        print("\n📋 Test 2: Checking required files...")
        required_files = [
            "income_prediction_pipeline.py",
            "production_part1_data_cleaning.py", 
            "production_part2_model_inference.py",
            "production_model_catboost_all_data.pkl",
            "production_frequency_mappings_catboost.pkl",
            "test_data.csv"
        ]
        
        missing_files = []
        for file in required_files:
            if os.path.exists(file):
                print(f"✅ {file}")
            else:
                print(f"❌ {file} - NOT FOUND")
                missing_files.append(file)
        
        if missing_files:
            print(f"\n❌ Missing files: {missing_files}")
            return False
        
        # Test 3: Load test data
        print("\n📋 Test 3: Loading test data...")
        df = pd.read_csv("test_data.csv")
        print(f"✅ Test data loaded: {len(df)} rows, {len(df.columns)} columns")
        
        # Test 4: Run the pipeline
        print("\n📋 Test 4: Running pipeline...")
        from income_prediction_pipeline import run_income_prediction_pipeline
        
        results = run_income_prediction_pipeline("test_data.csv")
        
        if results is not None:
            print("\n🎉 PIPELINE TEST SUCCESSFUL!")
            print(f"✅ Generated predictions for {len(results)} customers")
            print("\n📊 Sample results:")
            print(results.head(3).to_string(index=False))
            return True
        else:
            print("\n❌ PIPELINE TEST FAILED!")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_pipeline()
    if success:
        print("\n✅ ALL TESTS PASSED - Pipeline is ready!")
    else:
        print("\n❌ TESTS FAILED - Check the errors above")
        sys.exit(1)
