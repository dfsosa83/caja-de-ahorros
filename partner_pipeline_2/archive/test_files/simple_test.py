#!/usr/bin/env python3
# Simple test for your specific case: age 44 + employer 'OTROS'

import pandas as pd
import sys
import os

def test_minimal_data():
    """Test your specific minimal data case"""
    print("TESTING YOUR SPECIFIC CASE: Age 44 + Employer 'OTROS'")
    print("=" * 60)
    
    # Create test data - your exact scenario
    test_data = {
        'Cliente': 99001,
        'Identificador_Unico': 'TEST-MINIMAL',
        'Edad': 44,
        'NombreEmpleadorCliente': 'OTROS'
    }
    
    print("Test data:")
    for key, value in test_data.items():
        print(f"   {key}: {value}")
    
    # Save to CSV
    df = pd.DataFrame([test_data])
    test_file = 'minimal_test_data.csv'
    df.to_csv(test_file, index=False)
    print(f"\nSaved test data to: {test_file}")
    
    # Try to run the pipeline
    try:
        print("\nRunning income prediction pipeline...")
        
        # Import the pipeline
        from income_prediction_pipeline import run_income_prediction_pipeline
        
        # Run prediction
        result = run_income_prediction_pipeline(test_file)
        
        if result is not None and len(result) > 0:
            print("SUCCESS! Pipeline worked!")
            print("\nResults:")
            print(f"   Customer ID: {result.iloc[0]['Cliente']}")
            print(f"   Predicted Income: ${result.iloc[0]['predicted_income']:.2f}")
            print(f"   90% CI Lower: ${result.iloc[0]['income_lower_90']:.2f}")
            print(f"   90% CI Upper: ${result.iloc[0]['income_upper_90']:.2f}")
            
            # Calculate CI width
            ci_width = result.iloc[0]['income_upper_90'] - result.iloc[0]['income_lower_90']
            print(f"   Confidence Interval Width: ${ci_width:.2f}")
            
            return True
        else:
            print("FAILED: No predictions returned")
            return False
            
    except ImportError as e:
        print(f"FAILED: Could not import pipeline: {e}")
        return False
    except Exception as e:
        print(f"FAILED: Pipeline error: {e}")
        return False

def check_required_files():
    """Check if required pipeline files exist"""
    print("\nCHECKING REQUIRED FILES:")
    print("-" * 30)
    
    required_files = [
        'income_prediction_pipeline.py',
        'production_part1_data_cleaning.py',
        'production_part2_model_inference.py',
        'production_model_catboost_all_data.pkl',
        'production_frequency_mappings_catboost.pkl'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   SUCCESS: {file}")
        else:
            print(f"   MISSING: {file}")
            all_exist = False
    
    return all_exist

def main():
    """Main test function"""
    print("SIMPLE PIPELINE TEST")
    print("=" * 60)
    print("Testing your specific case: Age 44 + Employer 'OTROS'")
    print()
    
    # Check required files
    files_ok = check_required_files()
    
    if not files_ok:
        print("\nERROR: Missing required pipeline files!")
        print("Make sure you're in the correct directory with all pipeline files.")
        return 1
    
    # Run the test
    success = test_minimal_data()
    
    print("\n" + "=" * 60)
    if success:
        print("TEST RESULT: SUCCESS!")
        print("Your pipeline can handle minimal data (age 44 + employer 'OTROS')")
    else:
        print("TEST RESULT: FAILED!")
        print("There are issues with the pipeline or data handling")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
