#!/usr/bin/env python3
# Test your specific case with different data completeness levels

import pandas as pd
import sys
import os

def test_scenario(scenario_name, test_data, description):
    """Test a specific scenario"""
    print(f"\n{scenario_name.upper()}")
    print("=" * 60)
    print(f"Description: {description}")
    print("\nTest data:")
    for key, value in test_data.items():
        print(f"   {key}: {value}")
    
    # Save to CSV
    df = pd.DataFrame([test_data])
    test_file = f'test_{scenario_name.lower().replace(" ", "_")}.csv'
    df.to_csv(test_file, index=False)
    print(f"\nSaved to: {test_file}")
    
    # Try to run the pipeline
    try:
        print("\nRunning pipeline...")
        
        # Import the pipeline
        from income_prediction_pipeline import run_income_prediction_pipeline
        
        # Run prediction
        result = run_income_prediction_pipeline(test_file)
        
        if result is not None and len(result) > 0:
            print("SUCCESS!")
            print(f"   Predicted Income: ${result.iloc[0]['predicted_income']:.2f}")
            print(f"   90% CI: ${result.iloc[0]['income_lower_90']:.2f} - ${result.iloc[0]['income_upper_90']:.2f}")
            ci_width = result.iloc[0]['income_upper_90'] - result.iloc[0]['income_lower_90']
            print(f"   CI Width: ${ci_width:.2f}")
            return True, result.iloc[0]['predicted_income']
        else:
            print("FAILED: No predictions returned")
            return False, None
            
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return False, None

def main():
    """Test different scenarios for your case"""
    print("TESTING YOUR CASE: Age 44 + Employer 'OTROS'")
    print("=" * 80)
    print("Testing different levels of data completeness")
    
    results = []
    
    # SCENARIO 1: Absolute minimal (what you originally asked)
    scenario_1 = {
        'Cliente': 99001,
        'Identificador_Unico': 'TEST-001',
        'Edad': 44,
        'NombreEmpleadorCliente': 'OTROS'
    }
    success_1, pred_1 = test_scenario(
        "Scenario 1 - Absolute Minimal", 
        scenario_1,
        "Only age and employer (your original question)"
    )
    results.append(("Absolute Minimal", success_1, pred_1))
    
    # SCENARIO 2: Add minimal financial data
    scenario_2 = {
        'Cliente': 99002,
        'Identificador_Unico': 'TEST-002',
        'Edad': 44,
        'NombreEmpleadorCliente': 'OTROS',
        'saldo': 10000.0,  # Add balance
        'monto_letra': 400.0  # Add payment
    }
    success_2, pred_2 = test_scenario(
        "Scenario 2 - With Financial Data", 
        scenario_2,
        "Age 44 + OTROS + basic financial data"
    )
    results.append(("With Financial Data", success_2, pred_2))
    
    # SCENARIO 3: Add some dates
    scenario_3 = {
        'Cliente': 99003,
        'Identificador_Unico': 'TEST-003',
        'Edad': 44,
        'NombreEmpleadorCliente': 'OTROS',
        'saldo': 10000.0,
        'monto_letra': 400.0,
        'FechaIngresoEmpleo': '2020-01-01',
        'fecha_inicio': '2020-02-01'
    }
    success_3, pred_3 = test_scenario(
        "Scenario 3 - With Dates", 
        scenario_3,
        "Age 44 + OTROS + financial + employment dates"
    )
    results.append(("With Dates", success_3, pred_3))
    
    # SCENARIO 4: Add occupation
    scenario_4 = {
        'Cliente': 99004,
        'Identificador_Unico': 'TEST-004',
        'Edad': 44,
        'Ocupacion': 'COMERCIANTE',  # Add occupation
        'NombreEmpleadorCliente': 'OTROS',
        'saldo': 10000.0,
        'monto_letra': 400.0,
        'FechaIngresoEmpleo': '2020-01-01',
        'fecha_inicio': '2020-02-01'
    }
    success_4, pred_4 = test_scenario(
        "Scenario 4 - With Occupation", 
        scenario_4,
        "Age 44 + OTROS + financial + dates + occupation"
    )
    results.append(("With Occupation", success_4, pred_4))
    
    # SUMMARY
    print("\n" + "=" * 80)
    print("SUMMARY OF RESULTS")
    print("=" * 80)
    
    successful_scenarios = []
    for scenario_name, success, prediction in results:
        status = "SUCCESS" if success else "FAILED"
        pred_text = f"${prediction:.2f}" if prediction else "N/A"
        print(f"   {scenario_name:20} | {status:7} | {pred_text}")
        if success:
            successful_scenarios.append((scenario_name, prediction))
    
    print(f"\nSuccessful scenarios: {len(successful_scenarios)}/{len(results)}")
    
    if successful_scenarios:
        print("\nKEY INSIGHTS:")
        print("-" * 40)
        
        # Find minimum required data
        min_data_scenario = successful_scenarios[0]
        print(f"   Minimum data needed: {min_data_scenario[0]}")
        print(f"   Prediction with minimal data: ${min_data_scenario[1]:.2f}")
        
        # Compare predictions if multiple scenarios worked
        if len(successful_scenarios) > 1:
            predictions = [pred for _, pred in successful_scenarios]
            print(f"   Prediction range: ${min(predictions):.2f} - ${max(predictions):.2f}")
            print(f"   Difference: ${max(predictions) - min(predictions):.2f}")
            
            print("\n   How predictions change with more data:")
            for scenario_name, prediction in successful_scenarios:
                print(f"      {scenario_name}: ${prediction:.2f}")
    
    else:
        print("\nNO SUCCESSFUL SCENARIOS!")
        print("The pipeline requires more data than provided in all test cases.")
    
    print("\n" + "=" * 80)
    print("CONCLUSION FOR YOUR QUESTION:")
    print("=" * 80)
    
    if results[0][1]:  # If absolute minimal worked
        print(f"✓ YES: Age 44 + 'OTROS' alone works!")
        print(f"  Predicted income: ${results[0][2]:.2f}")
    elif results[1][1]:  # If with financial data worked
        print(f"✓ PARTIAL: Age 44 + 'OTROS' needs financial data")
        print(f"  Predicted income: ${results[1][2]:.2f}")
        print(f"  Required: saldo (balance) and monto_letra (payment)")
    else:
        print("✗ NO: Age 44 + 'OTROS' is not sufficient")
        print("  The pipeline requires additional data fields")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
