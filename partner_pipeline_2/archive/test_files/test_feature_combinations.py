#!/usr/bin/env python3
# =============================================================================
# SYSTEMATIC FEATURE COMBINATION TESTING
# =============================================================================
#
# OBJECTIVE: Test model behavior with different feature combinations
# 
# APPROACH:
# 1. Test with only 1 feature (others NaN)
# 2. Test with only 2 features (others NaN)
# 3. Test with only 3 features (others NaN)
# ... and so on
#
# This helps understand minimum data requirements and model robustness
# =============================================================================

import pandas as pd
import numpy as np
import itertools
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_base_customer():
    """Create a base customer with all features filled"""
    return {
        'Cliente': 88888,
        'Identificador_Unico': 'COMBO-TEST',
        'Edad': 44,
        'Ocupacion': 'COMERCIANTE',
        'NombreEmpleadorCliente': 'OTROS',
        'CargoEmpleoCliente': 'PROPIETARIO',
        'FechaIngresoEmpleo': '2020-01-15',
        'saldo': 15000.0,
        'monto_letra': 500.0,
        'fecha_inicio': '2020-02-01',
        'fecha_vencimiento': '2025-02-01'
    }

def create_test_scenario(features_to_keep, base_customer):
    """Create a test scenario with only specified features, others as NaN"""
    scenario = {}
    
    # Always keep Cliente and Identificador_Unico for tracking
    scenario['Cliente'] = base_customer['Cliente']
    scenario['Identificador_Unico'] = f"TEST-{len(features_to_keep)}F"
    
    # Set specified features
    for feature in features_to_keep:
        if feature in base_customer:
            scenario[feature] = base_customer[feature]
    
    # Set all other features to NaN
    all_features = [
        'Edad', 'Ocupacion', 'NombreEmpleadorCliente', 'CargoEmpleoCliente',
        'FechaIngresoEmpleo', 'saldo', 'monto_letra', 'fecha_inicio', 'fecha_vencimiento'
    ]
    
    for feature in all_features:
        if feature not in features_to_keep:
            scenario[feature] = np.nan
    
    return scenario

def test_pipeline(scenario, scenario_name):
    """Test the pipeline with a specific scenario"""
    try:
        # Create DataFrame and save to CSV
        df = pd.DataFrame([scenario])
        test_file = f'combo_test_{scenario_name}.csv'
        df.to_csv(test_file, index=False)
        
        # Import and run pipeline
        from income_prediction_pipeline import run_income_prediction_pipeline
        result = run_income_prediction_pipeline(test_file)
        
        if result is not None and len(result) > 0:
            prediction = result.iloc[0]['predicted_income']
            ci_lower = result.iloc[0]['income_lower_90']
            ci_upper = result.iloc[0]['income_upper_90']
            ci_width = ci_upper - ci_lower
            
            return {
                'status': 'SUCCESS',
                'predicted_income': prediction,
                'ci_lower': ci_lower,
                'ci_upper': ci_upper,
                'ci_width': ci_width,
                'error': None
            }
        else:
            return {
                'status': 'FAILED',
                'predicted_income': None,
                'ci_lower': None,
                'ci_upper': None,
                'ci_width': None,
                'error': 'No predictions returned'
            }
            
    except Exception as e:
        return {
            'status': 'ERROR',
            'predicted_income': None,
            'ci_lower': None,
            'ci_upper': None,
            'ci_width': None,
            'error': str(e)
        }

def run_systematic_tests():
    """Run systematic feature combination tests"""
    print("SYSTEMATIC FEATURE COMBINATION TESTING")
    print("=" * 80)
    print("Testing model behavior with different numbers of features")
    print()
    
    base_customer = create_base_customer()
    
    # Define all testable features (excluding ID fields)
    all_features = [
        'Edad', 'Ocupacion', 'NombreEmpleadorCliente', 'CargoEmpleoCliente',
        'FechaIngresoEmpleo', 'saldo', 'monto_letra', 'fecha_inicio', 'fecha_vencimiento'
    ]
    
    results = []
    
    # Test with 1 feature at a time
    print("TESTING WITH 1 FEATURE AT A TIME")
    print("-" * 50)
    
    for feature in all_features:
        features_to_keep = [feature]
        scenario = create_test_scenario(features_to_keep, base_customer)
        scenario_name = f"1F_{feature}"
        
        print(f"Testing: {feature}")
        result = test_pipeline(scenario, scenario_name)
        
        result_record = {
            'num_features': 1,
            'features': feature,
            'scenario_name': scenario_name,
            **result
        }
        results.append(result_record)
        
        status = result['status']
        if status == 'SUCCESS':
            print(f"   SUCCESS: ${result['predicted_income']:.2f}")
        else:
            print(f"   {status}: {result.get('error', 'Unknown error')}")
    
    # Test with 2 features at a time (key combinations)
    print(f"\nTESTING WITH 2 FEATURES AT A TIME (Key Combinations)")
    print("-" * 50)
    
    key_2feature_combos = [
        ['Edad', 'NombreEmpleadorCliente'],  # Your original question
        ['Edad', 'saldo'],
        ['Edad', 'monto_letra'],
        ['saldo', 'monto_letra'],  # Financial data
        ['Edad', 'Ocupacion'],
        ['NombreEmpleadorCliente', 'saldo'],
        ['FechaIngresoEmpleo', 'Edad'],
        ['fecha_inicio', 'saldo']
    ]
    
    for features_to_keep in key_2feature_combos:
        scenario = create_test_scenario(features_to_keep, base_customer)
        scenario_name = f"2F_{'_'.join(features_to_keep)}"
        
        print(f"Testing: {' + '.join(features_to_keep)}")
        result = test_pipeline(scenario, scenario_name)
        
        result_record = {
            'num_features': 2,
            'features': ' + '.join(features_to_keep),
            'scenario_name': scenario_name,
            **result
        }
        results.append(result_record)
        
        status = result['status']
        if status == 'SUCCESS':
            print(f"   SUCCESS: ${result['predicted_income']:.2f}")
        else:
            print(f"   {status}: {result.get('error', 'Unknown error')}")
    
    # Test with 3 features (essential combinations)
    print(f"\nTESTING WITH 3 FEATURES (Essential Combinations)")
    print("-" * 50)
    
    key_3feature_combos = [
        ['Edad', 'NombreEmpleadorCliente', 'saldo'],
        ['Edad', 'NombreEmpleadorCliente', 'monto_letra'],
        ['Edad', 'saldo', 'monto_letra'],  # Age + financial
        ['Edad', 'Ocupacion', 'NombreEmpleadorCliente'],  # Demographics
        ['saldo', 'monto_letra', 'FechaIngresoEmpleo'],  # Financial + tenure
    ]
    
    for features_to_keep in key_3feature_combos:
        scenario = create_test_scenario(features_to_keep, base_customer)
        scenario_name = f"3F_{'_'.join(features_to_keep)}"
        
        print(f"Testing: {' + '.join(features_to_keep)}")
        result = test_pipeline(scenario, scenario_name)
        
        result_record = {
            'num_features': 3,
            'features': ' + '.join(features_to_keep),
            'scenario_name': scenario_name,
            **result
        }
        results.append(result_record)
        
        status = result['status']
        if status == 'SUCCESS':
            print(f"   SUCCESS: ${result['predicted_income']:.2f}")
        else:
            print(f"   {status}: {result.get('error', 'Unknown error')}")
    
    return results

def analyze_results(results):
    """Analyze the systematic test results"""
    print("\n" + "=" * 80)
    print("ANALYSIS OF FEATURE COMBINATION RESULTS")
    print("=" * 80)
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(results)
    
    # Save detailed results
    df.to_csv('feature_combination_results.csv', index=False)
    print("Detailed results saved to: feature_combination_results.csv")
    
    # Success rate by number of features
    print(f"\nSUCCESS RATE BY NUMBER OF FEATURES:")
    print("-" * 40)
    
    for num_features in sorted(df['num_features'].unique()):
        subset = df[df['num_features'] == num_features]
        successful = len(subset[subset['status'] == 'SUCCESS'])
        total = len(subset)
        success_rate = (successful / total) * 100
        print(f"   {num_features} feature(s): {successful}/{total} ({success_rate:.1f}%)")
    
    # Successful combinations
    successful_df = df[df['status'] == 'SUCCESS']
    if len(successful_df) > 0:
        print(f"\nSUCCESSFUL COMBINATIONS:")
        print("-" * 40)
        
        for _, row in successful_df.iterrows():
            print(f"   {row['num_features']} features: {row['features']}")
            print(f"      Prediction: ${row['predicted_income']:.2f}")
            print(f"      CI: ${row['ci_lower']:.2f} - ${row['ci_upper']:.2f}")
        
        # Find minimum successful combination
        min_features = successful_df['num_features'].min()
        min_combo = successful_df[successful_df['num_features'] == min_features].iloc[0]
        
        print(f"\nMINIMUM SUCCESSFUL COMBINATION:")
        print("-" * 40)
        print(f"   Features needed: {min_features}")
        print(f"   Combination: {min_combo['features']}")
        print(f"   Prediction: ${min_combo['predicted_income']:.2f}")
        
    else:
        print(f"\nNO SUCCESSFUL COMBINATIONS FOUND!")
        print("The pipeline requires more complete data.")
    
    # Failed combinations analysis
    failed_df = df[df['status'] != 'SUCCESS']
    if len(failed_df) > 0:
        print(f"\nCOMMON FAILURE REASONS:")
        print("-" * 40)
        
        error_counts = failed_df['error'].value_counts()
        for error, count in error_counts.items():
            print(f"   {error}: {count} cases")

def main():
    """Main function"""
    print("FEATURE COMBINATION TESTING SUITE")
    print("=" * 80)
    print("Understanding minimum data requirements for income prediction")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run systematic tests
    results = run_systematic_tests()
    
    # Analyze results
    analyze_results(results)
    
    print(f"\n" + "=" * 80)
    print("TESTING COMPLETE!")
    print("Check 'feature_combination_results.csv' for detailed results")

if __name__ == "__main__":
    main()
