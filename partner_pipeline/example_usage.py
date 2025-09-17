# =============================================================================
# EXAMPLE USAGE - Income Prediction Pipeline
# =============================================================================
#
# This script shows how to use the pipeline programmatically
#
# =============================================================================

from income_prediction_pipeline import run_income_prediction_pipeline
import pandas as pd

def example_usage():
    """
    Example of how to use the pipeline programmatically
    """
    
    # Example 1: Run pipeline on a CSV file
    input_file_path = r'C:\Users\david\OneDrive\Documents\augment-projects\caja-de-ahorros\data\external\00_test.csv'
    input_file = input_file_path
    
    print("🧪 EXAMPLE: Running Income Prediction Pipeline")
    print("=" * 50)
    
    # Run the pipeline
    results = run_income_prediction_pipeline(input_file)
    
    if results is not None:
        print("\n✅ Pipeline completed successfully!")
        print(f"📊 Processed {len(results)} customers")
        
        # You can now work with the results DataFrame
        print("\n📋 First 3 predictions:")
        print(results.head(3).to_string(index=False))
        
        # Calculate additional statistics
        avg_income = results['predicted_income'].mean()
        high_income_customers = len(results[results['predicted_income'] > 1500])
        
        print(f"\n📈 Additional Analysis:")
        print(f"   💰 Average predicted income: ${avg_income:,.2f}")
        print(f"   🎯 High income customers (>$1500): {high_income_customers}")
        
        # Save with custom filename
        output_file = "my_custom_predictions.csv"
        results.to_csv(output_file, index=False)
        print(f"   💾 Saved to: {output_file}")
        
    else:
        print("❌ Pipeline failed")

if __name__ == "__main__":
    example_usage()
