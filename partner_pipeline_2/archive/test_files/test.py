# Simple test to verify the pipeline works
import os
import sys

def test_pipeline():
    print("🧪 Testing Income Prediction Pipeline")
    print("=" * 40)
    
    # Check required files
    required_files = [
        "income_prediction_pipeline.py",
        "production_part1_data_cleaning.py", 
        "production_part2_model_inference.py",
        "production_model_catboost_all_data.pkl",
        "production_frequency_mappings_catboost.pkl",
        "test_data.csv"
    ]
    
    print("📋 Checking files...")
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {missing}")
        return False
    
    print("\n🚀 Running tests...")

    # Test 1: CSV format
    print("📋 Test 1: CSV format...")
    result1 = os.system("python income_prediction_pipeline.py test_data.csv")

    # Test 2: JSON format
    print("📋 Test 2: JSON format...")
    result2 = os.system("python income_prediction_pipeline.py example_data.json")

    if result1 == 0 and result2 == 0:
        print("\n✅ All tests successful!")
        print("🎯 Both CSV and JSON formats work!")
        return True
    else:
        print("\n❌ Some tests failed!")
        if result1 != 0:
            print("   ❌ CSV test failed")
        if result2 != 0:
            print("   ❌ JSON test failed")
        return False

if __name__ == "__main__":
    success = test_pipeline()
    if not success:
        sys.exit(1)
