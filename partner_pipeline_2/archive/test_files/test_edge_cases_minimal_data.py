#!/usr/bin/env python3
# =============================================================================
# EDGE CASE TESTING - MINIMAL DATA SCENARIOS
# =============================================================================
#
# OBJECTIVE: Test model behavior with minimal/incomplete customer data
# 
# TEST SCENARIOS:
# 1. Minimal data (only age + employer)
# 2. Missing critical financial data
# 3. Missing date information
# 4. Unknown/new categorical values
# 5. Extreme values (very old/young, very high/low balances)
#
# USAGE: python test_edge_cases_minimal_data.py
# =============================================================================

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_test_scenarios():
   """
   Create various edge case scenarios for testing
   """

   print("*** CREATING EDGE CASE TEST SCENARIOS ***")
   print("=" * 60)
   
   # Base template with required columns
   base_columns = [
   'Cliente', 'Identificador_Unico', 'Edad', 'Ocupacion', 
   'NombreEmpleadorCliente', 'CargoEmpleoCliente', 'FechaIngresoEmpleo',
   'saldo', 'monto_letra', 'fecha_inicio'
   ]
   
   test_scenarios = []
   
   # =================================================================
   # SCENARIO 1: MINIMAL DATA (Your specific case)
   # =================================================================
   print("Scenario 1: Minimal data (age + employer only)")
   scenario_1 = {
   'Cliente': 99001,
   'Identificador_Unico': 'TEST-001',
   'Edad': 44,
   'Ocupacion': None,  # Missing
   'NombreEmpleadorCliente': 'OTROS',
   'CargoEmpleoCliente': None,  # Missing
   'FechaIngresoEmpleo': None,  # Missing
   'saldo': None,  # Missing
   'monto_letra': None,  # Missing
   'fecha_inicio': None  # Missing
   }
   test_scenarios.append(("minimal_data", scenario_1))
   
   # =================================================================
   # SCENARIO 2: MISSING FINANCIAL DATA
   # =================================================================
   print("Scenario 2: Missing financial data")
   scenario_2 = {
   'Cliente': 99002,
   'Identificador_Unico': 'TEST-002',
   'Edad': 35,
   'Ocupacion': 'INGENIERO',
   'NombreEmpleadorCliente': 'EMPRESA PRIVADA',
   'CargoEmpleoCliente': 'INGENIERO SENIOR',
   'FechaIngresoEmpleo': '2018-06-15',
   'saldo': None,  # Missing - critical for ratios
   'monto_letra': None,  # Missing - critical for ratios
   'fecha_inicio': '2020-01-15'
   }
   test_scenarios.append(("missing_financial", scenario_2))
   
   # =================================================================
   # SCENARIO 3: MISSING DATE INFORMATION
   # =================================================================
   print("Scenario 3: Missing date information")
   scenario_3 = {
   'Cliente': 99003,
   'Identificador_Unico': 'TEST-003',
   'Edad': 52,
   'Ocupacion': 'DOCENTE',
   'NombreEmpleadorCliente': 'MINISTERIO DE EDUCACION',
   'CargoEmpleoCliente': 'PROFESOR',
   'FechaIngresoEmpleo': None,  # Missing - affects tenure
   'saldo': 15000.0,
   'monto_letra': 450.0,
   'fecha_inicio': None  # Missing - affects account age
   }
   test_scenarios.append(("missing_dates", scenario_3))
   
   # =================================================================
   # SCENARIO 4: UNKNOWN CATEGORICAL VALUES
   # =================================================================
   print("Scenario 4: Unknown categorical values")
   scenario_4 = {
   'Cliente': 99004,
   'Identificador_Unico': 'TEST-004',
   'Edad': 28,
   'Ocupacion': 'DATA_SCIENTIST',  # New occupation not in training
   'NombreEmpleadorCliente': 'GOOGLE_PANAMA',  # New employer not in training
   'CargoEmpleoCliente': 'ML_ENGINEER',  # New position not in training
   'FechaIngresoEmpleo': '2023-01-01',
   'saldo': 25000.0,
   'monto_letra': 800.0,
   'fecha_inicio': '2023-02-01'
   }
   test_scenarios.append(("unknown_categories", scenario_4))
   
   # =================================================================
   # SCENARIO 5: EXTREME VALUES - VERY YOUNG
   # =================================================================
   print("Scenario 5: Extreme values - Very young customer")
   scenario_5 = {
   'Cliente': 99005,
   'Identificador_Unico': 'TEST-005',
   'Edad': 18,  # Very young
   'Ocupacion': 'ESTUDIANTE',
   'NombreEmpleadorCliente': 'UNIVERSIDAD',
   'CargoEmpleoCliente': 'ESTUDIANTE',
   'FechaIngresoEmpleo': '2024-01-01',  # Very recent
   'saldo': 500.0,  # Very low balance
   'monto_letra': 50.0,  # Very low payment
   'fecha_inicio': '2024-01-15'
   }
   test_scenarios.append(("extreme_young", scenario_5))
   
   # =================================================================
   # SCENARIO 6: EXTREME VALUES - VERY OLD
   # =================================================================
   print("Scenario 6: Extreme values - Very old customer")
   scenario_6 = {
   'Cliente': 99006,
   'Identificador_Unico': 'TEST-006',
   'Edad': 85,  # Very old
   'Ocupacion': 'JUBILADO',
   'NombreEmpleadorCliente': 'NO APLICA',
   'CargoEmpleoCliente': 'JUBILADO',
   'FechaIngresoEmpleo': '1980-01-01',  # Very old employment
   'saldo': 100000.0,  # Very high balance
   'monto_letra': 2000.0,  # Very high payment
   'fecha_inicio': '1990-01-01'  # Very old account
   }
   test_scenarios.append(("extreme_old", scenario_6))
   
   # =================================================================
   # SCENARIO 7: ZERO/NEGATIVE VALUES
   # =================================================================
   print("Scenario 7: Zero and edge financial values")
   scenario_7 = {
   'Cliente': 99007,
   'Identificador_Unico': 'TEST-007',
   'Edad': 40,
   'Ocupacion': 'COMERCIANTE',
   'NombreEmpleadorCliente': 'INDEPENDIENTE',
   'CargoEmpleoCliente': 'PROPIETARIO',
   'FechaIngresoEmpleo': '2015-06-01',
   'saldo': 0.0,  # Zero balance
   'monto_letra': 0.0,  # Zero payment
   'fecha_inicio': '2020-01-01'  # Exactly on reference date
   }
   test_scenarios.append(("zero_values", scenario_7))
   
   return test_scenarios

def save_test_scenarios(test_scenarios):
   """
   Save each test scenario as a separate CSV file
   """
   print("\n*** SAVING TEST SCENARIO FILES ***")
   print("=" * 40)
   
   for scenario_name, scenario_data in test_scenarios:
   # Create DataFrame
   df = pd.DataFrame([scenario_data])
   
   # Save to CSV
   filename = f"test_scenario_{scenario_name}.csv"
   df.to_csv(filename, index=False)
   print(f"SUCCESS: Saved: {filename}")

   # Show what was saved
   print(f"   Data preview:")
   for key, value in scenario_data.items():
   if value is not None:
   print(f"   {key}: {value}")
   else:
   print(f"   {key}: NULL")
   print()

def run_pipeline_tests():
   """
   Run the pipeline on each test scenario and capture results
   """
   print("\n*** RUNNING PIPELINE TESTS ***")
   print("=" * 40)
   
   # Import the main pipeline
   try:
   from income_prediction_pipeline import run_income_prediction_pipeline
   pipeline_available = True
   except ImportError:
   print("FAILED: Could not import pipeline - make sure income_prediction_pipeline.py is available")
   pipeline_available = False
   return
   
   # Get all test scenario files
   test_files = [f for f in os.listdir('.') if f.startswith('test_scenario_') and f.endswith('.csv')]
   
   results_summary = []
   
   for test_file in test_files:
   scenario_name = test_file.replace('test_scenario_', '').replace('.csv', '')
   print(f"\n Testing: {scenario_name}")
   print("-" * 30)
   
   try:
   # Run pipeline
   result_df = run_income_prediction_pipeline(test_file)
   
   if result_df is not None and len(result_df) > 0:
   prediction = result_df.iloc[0]['predicted_income']
   lower_ci = result_df.iloc[0]['income_lower_90']
   upper_ci = result_df.iloc[0]['income_upper_90']
   
   print(f"SUCCESS")
   print(f"   Predicted Income: ${prediction:.2f}")
   print(f"   90% CI: ${lower_ci:.2f} - ${upper_ci:.2f}")
   
   results_summary.append({
   'scenario': scenario_name,
   'status': 'SUCCESS',
   'predicted_income': prediction,
   'ci_lower': lower_ci,
   'ci_upper': upper_ci,
   'ci_width': upper_ci - lower_ci
   })
   else:
   print(f"FAILED - No predictions returned")
   results_summary.append({
   'scenario': scenario_name,
   'status': 'FAILED',
   'predicted_income': None,
   'ci_lower': None,
   'ci_upper': None,
   'ci_width': None
   })
   
   except Exception as e:
   print(f"ERROR: {str(e)}")
   results_summary.append({
   'scenario': scenario_name,
   'status': 'ERROR',
   'predicted_income': None,
   'ci_lower': None,
   'ci_upper': None,
   'ci_width': None,
   'error': str(e)
   })
   
   return results_summary

def analyze_results(results_summary):
   """
   Analyze and summarize test results
   """
   print("\n*** TEST RESULTS ANALYSIS ***")
   print("=" * 50)
   
   # Save results to CSV
   results_df = pd.DataFrame(results_summary)
   results_df.to_csv('edge_case_test_results.csv', index=False)
   print(" Results saved to: edge_case_test_results.csv")
   
   # Summary statistics
   successful_tests = results_df[results_df['status'] == 'SUCCESS']
   failed_tests = results_df[results_df['status'] != 'SUCCESS']
   
   print(f"\nSUMMARY:")
   print(f"   Successful tests: {len(successful_tests)}/{len(results_df)}")
   print(f"   Failed tests: {len(failed_tests)}/{len(results_df)}")
   
   if len(successful_tests) > 0:
   print(f"\nPREDICTION ANALYSIS:")
   print(f"   Average prediction: ${successful_tests['predicted_income'].mean():.2f}")
   print(f"   Min prediction: ${successful_tests['predicted_income'].min():.2f}")
   print(f"   Max prediction: ${successful_tests['predicted_income'].max():.2f}")
   print(f"   Average CI width: ${successful_tests['ci_width'].mean():.2f}")
   
   if len(failed_tests) > 0:
   print(f"\nFAILED SCENARIOS:")
   for _, row in failed_tests.iterrows():
   print(f"   • {row['scenario']}: {row['status']}")
   if 'error' in row and pd.notna(row['error']):
   print(f"   Error: {row['error']}")

if __name__ == "__main__":
   print("*** EDGE CASE TESTING SUITE ***")
   print("=" * 60)
   print("Testing model behavior with incomplete/edge case data")
   print()

   # Create test scenarios
   test_scenarios = create_test_scenarios()

   # Save test files
   save_test_scenarios(test_scenarios)

   # Run tests
   results = run_pipeline_tests()

   # Analyze results
   if results:
   analyze_results(results)

   print("\n*** TESTING COMPLETE! ***")
   print("Check the generated CSV files for detailed results.")
