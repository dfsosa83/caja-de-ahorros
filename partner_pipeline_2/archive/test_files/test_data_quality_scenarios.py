#!/usr/bin/env python3
# =============================================================================
# DATA QUALITY TESTING - VALIDATION & ERROR HANDLING
# =============================================================================
#
# OBJECTIVE: Test pipeline robustness with data quality issues
# 
# TEST SCENARIOS:
# 1. Invalid date formats
# 2. Text in numeric fields
# 3. Special characters and encoding issues
# 4. Missing required columns
# 5. Empty datasets
# 6. Duplicate records
# 7. Inconsistent data types
#
# USAGE: python test_data_quality_scenarios.py
# =============================================================================

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_data_quality_tests():
   """
   Create various data quality test scenarios
   """
   
   print("*** CREATING DATA QUALITY TEST SCENARIOS ***")
   print("=" * 60)
   
   test_scenarios = []
   
   # =================================================================
   # SCENARIO 1: INVALID DATE FORMATS
   # =================================================================
   print("Scenario 1: Invalid date formats")
   scenario_1_data = [
   {
   'Cliente': 88001,
   'Identificador_Unico': 'DQ-001',
   'Edad': 35,
   'Ocupacion': 'CONTADOR',
   'NombreEmpleadorCliente': 'EMPRESA ABC',
   'CargoEmpleoCliente': 'CONTADOR',
   'FechaIngresoEmpleo': '32/13/2020',  # Invalid date
   'saldo': 10000.0,
   'monto_letra': 300.0,
   'fecha_inicio': 'not-a-date'  # Invalid date
   },
   {
   'Cliente': 88002,
   'Identificador_Unico': 'DQ-002',
   'Edad': 40,
   'Ocupacion': 'MEDICO',
   'NombreEmpleadorCliente': 'HOSPITAL',
   'CargoEmpleoCliente': 'DOCTOR',
   'FechaIngresoEmpleo': '2020/15/01',  # Invalid month
   'saldo': 25000.0,
   'monto_letra': 600.0,
   'fecha_inicio': '01-15-2020'  # Different format
   }
   ]
   test_scenarios.append(("invalid_dates", scenario_1_data))
   
   # =================================================================
   # SCENARIO 2: TEXT IN NUMERIC FIELDS
   # =================================================================
   print("Scenario 2: Text in numeric fields")
   scenario_2_data = [
   {
   'Cliente': 88003,
   'Identificador_Unico': 'DQ-003',
   'Edad': 'thirty-five',  # Text instead of number
   'Ocupacion': 'INGENIERO',
   'NombreEmpleadorCliente': 'TECH COMPANY',
   'CargoEmpleoCliente': 'DEVELOPER',
   'FechaIngresoEmpleo': '2019-06-01',
   'saldo': 'fifteen thousand',  # Text instead of number
   'monto_letra': 'N/A',  # Text instead of number
   'fecha_inicio': '2020-01-01'
   },
   {
   'Cliente': 'CUSTOMER_004',  # Text instead of number
   'Identificador_Unico': 'DQ-004',
   'Edad': 45,
   'Ocupacion': 'ABOGADO',
   'NombreEmpleadorCliente': 'BUFETE LEGAL',
   'CargoEmpleoCliente': 'SOCIO',
   'FechaIngresoEmpleo': '2015-03-01',
   'saldo': '$20,000.50',  # Currency symbol and comma
   'monto_letra': '500.00 USD',  # Text with number
   'fecha_inicio': '2018-01-01'
   }
   ]
   test_scenarios.append(("text_in_numeric", scenario_2_data))
   
   # =================================================================
   # SCENARIO 3: SPECIAL CHARACTERS AND ENCODING
   # =================================================================
   print("Scenario 3: Special characters and encoding")
   scenario_3_data = [
   {
   'Cliente': 88005,
   'Identificador_Unico': 'DQ-005',
   'Edad': 50,
   'Ocupacion': 'MÉDICO',  # Accented character
   'NombreEmpleadorCliente': 'CLÍNICA SAN JOSÉ',  # Special characters
   'CargoEmpleoCliente': 'ESPECIALISTA EN CARDIOLOGÍA',  # Long text with accents
   'FechaIngresoEmpleo': '2010-01-01',
   'saldo': 30000.0,
   'monto_letra': 750.0,
   'fecha_inicio': '2015-01-01'
   },
   {
   'Cliente': 88006,
   'Identificador_Unico': 'DQ-006-ñ',  # Special character in ID
   'Edad': 33,
   'Ocupacion': 'DISEÑADOR',  # Ñ character
   'NombreEmpleadorCliente': 'AGENCIA & PUBLICIDAD',  # Ampersand
   'CargoEmpleoCliente': 'DISEÑADOR GRÁFICO',
   'FechaIngresoEmpleo': '2018-05-15',
   'saldo': 12000.0,
   'monto_letra': 400.0,
   'fecha_inicio': '2019-01-01'
   }
   ]
   test_scenarios.append(("special_characters", scenario_3_data))
   
   # =================================================================
   # SCENARIO 4: MISSING REQUIRED COLUMNS
   # =================================================================
   print("Scenario 4: Missing required columns")
   scenario_4_data = [
   {
   'Cliente': 88007,
   'Identificador_Unico': 'DQ-007',
   'Edad': 42,
   # 'Ocupacion': Missing entirely
   'NombreEmpleadorCliente': 'EMPRESA XYZ',
   'CargoEmpleoCliente': 'GERENTE',
   'FechaIngresoEmpleo': '2017-01-01',
   'saldo': 18000.0,
   # 'monto_letra': Missing entirely
   'fecha_inicio': '2018-01-01'
   }
   ]
   test_scenarios.append(("missing_columns", scenario_4_data))
   
   # =================================================================
   # SCENARIO 5: EMPTY DATASET
   # =================================================================
   print("Scenario 5: Empty dataset")
   scenario_5_data = []  # Empty list
   test_scenarios.append(("empty_dataset", scenario_5_data))
   
   # =================================================================
   # SCENARIO 6: DUPLICATE RECORDS
   # =================================================================
   print("Scenario 6: Duplicate records")
   duplicate_record = {
   'Cliente': 88008,
   'Identificador_Unico': 'DQ-008',
   'Edad': 38,
   'Ocupacion': 'ARQUITECTO',
   'NombreEmpleadorCliente': 'ESTUDIO ARQUITECTURA',
   'CargoEmpleoCliente': 'ARQUITECTO SENIOR',
   'FechaIngresoEmpleo': '2016-01-01',
   'saldo': 22000.0,
   'monto_letra': 550.0,
   'fecha_inicio': '2017-01-01'
   }
   scenario_6_data = [duplicate_record, duplicate_record, duplicate_record]  # Same record 3 times
   test_scenarios.append(("duplicate_records", scenario_6_data))
   
   # =================================================================
   # SCENARIO 7: MIXED DATA TYPES
   # =================================================================
   print("Scenario 7: Mixed data types in same column")
   scenario_7_data = [
   {
   'Cliente': 88009,
   'Identificador_Unico': 'DQ-009',
   'Edad': 29,
   'Ocupacion': 'PROGRAMADOR',
   'NombreEmpleadorCliente': 'STARTUP TECH',
   'CargoEmpleoCliente': 'FULL STACK DEVELOPER',
   'FechaIngresoEmpleo': '2021-01-01',
   'saldo': 15000,  # Integer
   'monto_letra': 450.50,  # Float
   'fecha_inicio': '2021-02-01'
   },
   {
   'Cliente': 88010,
   'Identificador_Unico': 'DQ-010',
   'Edad': 31.5,  # Float instead of int
   'Ocupacion': 'ANALISTA',
   'NombreEmpleadorCliente': 'CONSULTORA',
   'CargoEmpleoCliente': 'BUSINESS ANALYST',
   'FechaIngresoEmpleo': '2019-01-01',
   'saldo': '18000.75',  # String number
   'monto_letra': 500,  # Integer
   'fecha_inicio': '2020-01-01'
   }
   ]
   test_scenarios.append(("mixed_data_types", scenario_7_data))
   
   return test_scenarios

def save_data_quality_tests(test_scenarios):
   """
   Save each test scenario as a separate CSV file
   """
   print("\n*** SAVING DATA QUALITY TEST FILES ***")
   print("=" * 40)
   
   for scenario_name, scenario_data in test_scenarios:
   filename = f"test_data_quality_{scenario_name}.csv"
   
   try:
   if len(scenario_data) == 0:
   # Create empty CSV with headers
   empty_df = pd.DataFrame(columns=[
   'Cliente', 'Identificador_Unico', 'Edad', 'Ocupacion',
   'NombreEmpleadorCliente', 'CargoEmpleoCliente', 'FechaIngresoEmpleo',
   'saldo', 'monto_letra', 'fecha_inicio'
   ])
   empty_df.to_csv(filename, index=False)
   print(f"SUCCESS: Saved: {filename} (empty dataset)")
   else:
   # Create DataFrame
   df = pd.DataFrame(scenario_data)
   df.to_csv(filename, index=False)
   print(f"SUCCESS: Saved: {filename} ({len(scenario_data)} records)")
   
   # Show sample data
   print(f"   Sample data:")
   for i, record in enumerate(scenario_data[:2]):  # Show first 2 records
   print(f"   Record {i+1}: {record}")
   if len(scenario_data) > 2:
   print(f"   ... and {len(scenario_data)-2} more records")
   
   except Exception as e:
   print(f"FAILED: Error saving {filename}: {str(e)}")
   
   print()

def run_data_quality_tests():
   """
   Run the pipeline on each data quality test scenario
   """
   print("\n*** RUNNING DATA QUALITY TESTS ***")
   print("=" * 40)
   
   # Import the main pipeline
   try:
   from income_prediction_pipeline import run_income_prediction_pipeline
   pipeline_available = True
   except ImportError:
   print("FAILED: Could not import pipeline - make sure income_prediction_pipeline.py is available")
   return []
   
   # Get all data quality test files
   test_files = [f for f in os.listdir('.') if f.startswith('test_data_quality_') and f.endswith('.csv')]
   
   results_summary = []
   
   for test_file in test_files:
   scenario_name = test_file.replace('test_data_quality_', '').replace('.csv', '')
   print(f"\n Testing: {scenario_name}")
   print("-" * 30)
   
   try:
   # Run pipeline
   result_df = run_income_prediction_pipeline(test_file)
   
   if result_df is not None and len(result_df) > 0:
   print(f"SUCCESS: PIPELINE HANDLED GRACEFULLY")
   print(f"   Predictions generated: {len(result_df)}")
   
   # Show sample predictions
   for i, row in result_df.head(2).iterrows():
   print(f"   Customer {row['cliente']}: ${row['predicted_income']:.2f}")
   
   results_summary.append({
   'scenario': scenario_name,
   'status': 'SUCCESS',
   'records_processed': len(result_df),
   'avg_prediction': result_df['predicted_income'].mean(),
   'notes': 'Pipeline handled data quality issues gracefully'
   })
   else:
   print(f"WARNING: NO PREDICTIONS GENERATED")
   results_summary.append({
   'scenario': scenario_name,
   'status': 'NO_PREDICTIONS',
   'records_processed': 0,
   'avg_prediction': None,
   'notes': 'Pipeline ran but no predictions returned'
   })
   
   except Exception as e:
   print(f"FAILED: PIPELINE ERROR: {str(e)}")
   results_summary.append({
   'scenario': scenario_name,
   'status': 'ERROR',
   'records_processed': 0,
   'avg_prediction': None,
   'notes': f'Error: {str(e)}'
   })
   
   return results_summary

def analyze_data_quality_results(results_summary):
   """
   Analyze data quality test results
   """
   print("\n*** DATA QUALITY TEST ANALYSIS ***")
   print("=" * 50)
   
   # Save results
   results_df = pd.DataFrame(results_summary)
   results_df.to_csv('data_quality_test_results.csv', index=False)
   print(" Results saved to: data_quality_test_results.csv")
   
   # Summary
   successful = len([r for r in results_summary if r['status'] == 'SUCCESS'])
   errors = len([r for r in results_summary if r['status'] == 'ERROR'])
   no_predictions = len([r for r in results_summary if r['status'] == 'NO_PREDICTIONS'])
   
   print(f"\n ROBUSTNESS SUMMARY:")
   print(f"   SUCCESS: Handled gracefully: {successful}/{len(results_summary)}")
   print(f"   WARNING: No predictions: {no_predictions}/{len(results_summary)}")
   print(f"   FAILED: Pipeline errors: {errors}/{len(results_summary)}")
   
   print(f"\n DETAILED RESULTS:")
   for result in results_summary:
   status_icon = "SUCCESS:" if result['status'] == 'SUCCESS' else "WARNING:" if result['status'] == 'NO_PREDICTIONS' else "FAILED:"
   print(f"   {status_icon} {result['scenario']}: {result['status']}")
   if result['notes']:
   print(f"   📝 {result['notes']}")

if __name__ == "__main__":
   print("*** DATA QUALITY TESTING SUITE ***")
   print("=" * 60)
   print("Testing pipeline robustness with data quality issues")
   print()

   # Create test scenarios
   test_scenarios = create_data_quality_tests()

   # Save test files
   save_data_quality_tests(test_scenarios)

   # Run tests
   results = run_data_quality_tests()

   # Analyze results
   if results:
   analyze_data_quality_results(results)

   print("\n*** DATA QUALITY TESTING COMPLETE! ***")
   print("Check the generated CSV files and results for detailed analysis.")
