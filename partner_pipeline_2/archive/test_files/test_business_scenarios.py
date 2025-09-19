#!/usr/bin/env python3
# =============================================================================
# BUSINESS SCENARIO TESTING - REAL-WORLD USE CASES
# =============================================================================
#
# OBJECTIVE: Test model predictions for realistic business scenarios
# 
# TEST SCENARIOS:
# 1. Different income segments (low, middle, high earners)
# 2. Various professions and industries
# 3. Different life stages (young professionals, mid-career, retirees)
# 4. Geographic variations
# 5. Employment stability patterns
# 6. Financial behavior patterns
#
# USAGE: python test_business_scenarios.py
# =============================================================================

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def create_business_scenarios():
   """
   Create realistic business test scenarios
   """
   
   print("*** CREATING BUSINESS SCENARIO TESTS ***")
   print("=" * 60)
   
   test_scenarios = []
   
   # =================================================================
   # SCENARIO 1: YOUNG PROFESSIONALS
   # =================================================================
   print("Scenario 1: Young professionals")
   young_professionals = [
   {
   'Cliente': 77001,
   'Identificador_Unico': 'BIZ-001',
   'Edad': 25,
   'Ocupacion': 'INGENIERO',
   'NombreEmpleadorCliente': 'EMPRESA TECNOLOGIA',
   'CargoEmpleoCliente': 'INGENIERO JUNIOR',
   'FechaIngresoEmpleo': '2023-01-15',  # Recent graduate
   'saldo': 5000.0,  # Starting to save
   'monto_letra': 200.0,  # Low payments
   'fecha_inicio': '2023-02-01'
   },
   {
   'Cliente': 77002,
   'Identificador_Unico': 'BIZ-002',
   'Edad': 27,
   'Ocupacion': 'CONTADOR',
   'NombreEmpleadorCliente': 'FIRMA CONTABLE',
   'CargoEmpleoCliente': 'CONTADOR PUBLICO',
   'FechaIngresoEmpleo': '2021-06-01',  # 2+ years experience
   'saldo': 8500.0,
   'monto_letra': 350.0,
   'fecha_inicio': '2021-07-01'
   },
   {
   'Cliente': 77003,
   'Identificador_Unico': 'BIZ-003',
   'Edad': 29,
   'Ocupacion': 'MEDICO',
   'NombreEmpleadorCliente': 'HOSPITAL NACIONAL',
   'CargoEmpleoCliente': 'MEDICO RESIDENTE',
   'FechaIngresoEmpleo': '2022-03-01',  # Medical resident
   'saldo': 12000.0,
   'monto_letra': 450.0,
   'fecha_inicio': '2022-04-01'
   }
   ]
   test_scenarios.append(("young_professionals", young_professionals))
   
   # =================================================================
   # SCENARIO 2: MID-CAREER PROFESSIONALS
   # =================================================================
   print("Scenario 2: Mid-career professionals")
   mid_career = [
   {
   'Cliente': 77004,
   'Identificador_Unico': 'BIZ-004',
   'Edad': 40,
   'Ocupacion': 'GERENTE',
   'NombreEmpleadorCliente': 'BANCO NACIONAL',
   'CargoEmpleoCliente': 'GERENTE SUCURSAL',
   'FechaIngresoEmpleo': '2010-01-01',  # 14 years experience
   'saldo': 35000.0,  # Established savings
   'monto_letra': 800.0,  # Higher payments
   'fecha_inicio': '2012-01-01'
   },
   {
   'Cliente': 77005,
   'Identificador_Unico': 'BIZ-005',
   'Edad': 45,
   'Ocupacion': 'ABOGADO',
   'NombreEmpleadorCliente': 'BUFETE JURIDICO',
   'CargoEmpleoCliente': 'SOCIO',
   'FechaIngresoEmpleo': '2005-01-01',  # Senior professional
   'saldo': 50000.0,
   'monto_letra': 1200.0,
   'fecha_inicio': '2008-01-01'
   },
   {
   'Cliente': 77006,
   'Identificador_Unico': 'BIZ-006',
   'Edad': 38,
   'Ocupacion': 'ARQUITECTO',
   'NombreEmpleadorCliente': 'ESTUDIO ARQUITECTURA',
   'CargoEmpleoCliente': 'ARQUITECTO SENIOR',
   'FechaIngresoEmpleo': '2015-01-01',  # 9 years experience
   'saldo': 28000.0,
   'monto_letra': 650.0,
   'fecha_inicio': '2016-01-01'
   }
   ]
   test_scenarios.append(("mid_career", mid_career))
   
   # =================================================================
   # SCENARIO 3: GOVERNMENT EMPLOYEES
   # =================================================================
   print("Scenario 3: Government employees")
   government_employees = [
   {
   'Cliente': 77007,
   'Identificador_Unico': 'BIZ-007',
   'Edad': 35,
   'Ocupacion': 'DOCENTE',
   'NombreEmpleadorCliente': 'MINISTERIO DE EDUCACION',
   'CargoEmpleoCliente': 'PROFESOR',
   'FechaIngresoEmpleo': '2012-02-01',  # Stable government job
   'saldo': 18000.0,
   'monto_letra': 500.0,
   'fecha_inicio': '2013-01-01'
   },
   {
   'Cliente': 77008,
   'Identificador_Unico': 'BIZ-008',
   'Edad': 42,
   'Ocupacion': 'FUNCIONARIO',
   'NombreEmpleadorCliente': 'MINISTERIO DE SALUD',
   'CargoEmpleoCliente': 'DIRECTOR REGIONAL',
   'FechaIngresoEmpleo': '2008-01-01',  # Long tenure
   'saldo': 25000.0,
   'monto_letra': 700.0,
   'fecha_inicio': '2010-01-01'
   },
   {
   'Cliente': 77009,
   'Identificador_Unico': 'BIZ-009',
   'Edad': 50,
   'Ocupacion': 'POLICIA',
   'NombreEmpleadorCliente': 'POLICIA NACIONAL',
   'CargoEmpleoCliente': 'INSPECTOR',
   'FechaIngresoEmpleo': '2000-01-01',  # 24 years service
   'saldo': 30000.0,
   'monto_letra': 600.0,
   'fecha_inicio': '2005-01-01'
   }
   ]
   test_scenarios.append(("government_employees", government_employees))
   
   # =================================================================
   # SCENARIO 4: RETIREES
   # =================================================================
   print("Scenario 4: Retirees")
   retirees = [
   {
   'Cliente': 77010,
   'Identificador_Unico': 'BIZ-010',
   'Edad': 65,
   'Ocupacion': 'JUBILADO',
   'NombreEmpleadorCliente': 'CAJA DE SEGURO SOCIAL',
   'CargoEmpleoCliente': 'JUBILADO',
   'FechaIngresoEmpleo': '1980-01-01',  # Long career
   'saldo': 45000.0,  # Retirement savings
   'monto_letra': 400.0,  # Lower payments
   'fecha_inicio': '1985-01-01'
   },
   {
   'Cliente': 77011,
   'Identificador_Unico': 'BIZ-011',
   'Edad': 70,
   'Ocupacion': 'JUBILADO',
   'NombreEmpleadorCliente': 'NO APLICA',
   'CargoEmpleoCliente': 'JUBILADO',
   'FechaIngresoEmpleo': '1975-01-01',  # Very long career
   'saldo': 60000.0,
   'monto_letra': 300.0,
   'fecha_inicio': '1980-01-01'
   }
   ]
   test_scenarios.append(("retirees", retirees))
   
   # =================================================================
   # SCENARIO 5: ENTREPRENEURS & SELF-EMPLOYED
   # =================================================================
   print("Scenario 5: Entrepreneurs & self-employed")
   entrepreneurs = [
   {
   'Cliente': 77012,
   'Identificador_Unico': 'BIZ-012',
   'Edad': 33,
   'Ocupacion': 'COMERCIANTE',
   'NombreEmpleadorCliente': 'INDEPENDIENTE',
   'CargoEmpleoCliente': 'PROPIETARIO',
   'FechaIngresoEmpleo': '2018-01-01',  # Started business
   'saldo': 22000.0,  # Variable income
   'monto_letra': 550.0,
   'fecha_inicio': '2019-01-01'
   },
   {
   'Cliente': 77013,
   'Identificador_Unico': 'BIZ-013',
   'Edad': 41,
   'Ocupacion': 'CONSULTOR',
   'NombreEmpleadorCliente': 'FREELANCE',
   'CargoEmpleoCliente': 'CONSULTOR SENIOR',
   'FechaIngresoEmpleo': '2015-01-01',  # Independent consultant
   'saldo': 18000.0,
   'monto_letra': 480.0,
   'fecha_inicio': '2016-01-01'
   }
   ]
   test_scenarios.append(("entrepreneurs", entrepreneurs))
   
   # =================================================================
   # SCENARIO 6: HIGH-INCOME PROFESSIONALS
   # =================================================================
   print("Scenario 6: High-income professionals")
   high_income = [
   {
   'Cliente': 77014,
   'Identificador_Unico': 'BIZ-014',
   'Edad': 48,
   'Ocupacion': 'MEDICO',
   'NombreEmpleadorCliente': 'CLINICA PRIVADA',
   'CargoEmpleoCliente': 'ESPECIALISTA',
   'FechaIngresoEmpleo': '2000-01-01',  # Established specialist
   'saldo': 80000.0,  # High savings
   'monto_letra': 1500.0,  # High payments
   'fecha_inicio': '2005-01-01'
   },
   {
   'Cliente': 77015,
   'Identificador_Unico': 'BIZ-015',
   'Edad': 52,
   'Ocupacion': 'EJECUTIVO',
   'NombreEmpleadorCliente': 'MULTINACIONAL',
   'CargoEmpleoCliente': 'DIRECTOR GENERAL',
   'FechaIngresoEmpleo': '1995-01-01',  # Executive level
   'saldo': 120000.0,
   'monto_letra': 2000.0,
   'fecha_inicio': '2000-01-01'
   }
   ]
   test_scenarios.append(("high_income", high_income))
   
   return test_scenarios

def save_business_scenarios(test_scenarios):
   """
   Save each business scenario as a separate CSV file
   """
   print("\n*** SAVING BUSINESS SCENARIO FILES ***")
   print("=" * 40)
   
   for scenario_name, scenario_data in test_scenarios:
   # Create DataFrame
   df = pd.DataFrame(scenario_data)
   
   # Save to CSV
   filename = f"test_business_{scenario_name}.csv"
   df.to_csv(filename, index=False)
   print(f"SUCCESS: Saved: {filename} ({len(scenario_data)} customers)")
   
   # Show sample data
   print(f"   Sample customers:")
   for i, customer in enumerate(scenario_data[:2]):
   age = customer['Edad']
   occupation = customer['Ocupacion']
   employer = customer['NombreEmpleadorCliente']
   balance = customer['saldo']
   print(f"   {i+1}. Age {age}, {occupation} at {employer}, Balance: ${balance:,.0f}")
   if len(scenario_data) > 2:
   print(f"   ... and {len(scenario_data)-2} more customers")
   print()

def run_business_tests():
   """
   Run the pipeline on each business scenario and analyze predictions
   """
   print("\n*** RUNNING BUSINESS SCENARIO TESTS ***")
   print("=" * 40)
   
   # Import the main pipeline
   try:
   from income_prediction_pipeline import run_income_prediction_pipeline
   pipeline_available = True
   except ImportError:
   print("FAILED: Could not import pipeline - make sure income_prediction_pipeline.py is available")
   return []
   
   # Get all business test files
   test_files = [f for f in os.listdir('.') if f.startswith('test_business_') and f.endswith('.csv')]
   
   all_results = []
   scenario_summaries = []
   
   for test_file in test_files:
   scenario_name = test_file.replace('test_business_', '').replace('.csv', '')
   print(f"\n Testing: {scenario_name}")
   print("-" * 30)
   
   try:
   # Run pipeline
   result_df = run_income_prediction_pipeline(test_file)
   
   if result_df is not None and len(result_df) > 0:
   print(f"SUCCESS: SUCCESS - {len(result_df)} predictions generated")
   
   # Calculate statistics
   avg_income = result_df['predicted_income'].mean()
   min_income = result_df['predicted_income'].min()
   max_income = result_df['predicted_income'].max()
   avg_ci_width = (result_df['income_upper_90'] - result_df['income_lower_90']).mean()
   
   print(f"   Average predicted income: ${avg_income:.2f}")
   print(f"   Income range: ${min_income:.2f} - ${max_income:.2f}")
   print(f"   Average CI width: ${avg_ci_width:.2f}")
   
   # Add scenario info to results
   result_df['scenario'] = scenario_name
   all_results.append(result_df)
   
   scenario_summaries.append({
   'scenario': scenario_name,
   'status': 'SUCCESS',
   'customers': len(result_df),
   'avg_income': avg_income,
   'min_income': min_income,
   'max_income': max_income,
   'income_range': max_income - min_income,
   'avg_ci_width': avg_ci_width
   })
   
   else:
   print(f"FAILED: FAILED - No predictions returned")
   scenario_summaries.append({
   'scenario': scenario_name,
   'status': 'FAILED',
   'customers': 0,
   'avg_income': None,
   'min_income': None,
   'max_income': None,
   'income_range': None,
   'avg_ci_width': None
   })
   
   except Exception as e:
   print(f"FAILED: ERROR: {str(e)}")
   scenario_summaries.append({
   'scenario': scenario_name,
   'status': 'ERROR',
   'customers': 0,
   'avg_income': None,
   'min_income': None,
   'max_income': None,
   'income_range': None,
   'avg_ci_width': None,
   'error': str(e)
   })
   
   return all_results, scenario_summaries

def analyze_business_results(all_results, scenario_summaries):
   """
   Analyze business scenario results and generate insights
   """
   print("\n*** BUSINESS SCENARIO ANALYSIS ***")
   print("=" * 50)
   
   # Save detailed results
   if all_results:
   combined_results = pd.concat(all_results, ignore_index=True)
   combined_results.to_csv('business_scenario_detailed_results.csv', index=False)
   print(" Detailed results saved to: business_scenario_detailed_results.csv")
   
   # Save summary
   summary_df = pd.DataFrame(scenario_summaries)
   summary_df.to_csv('business_scenario_summary.csv', index=False)
   print(" Summary saved to: business_scenario_summary.csv")
   
   # Analysis
   successful_scenarios = summary_df[summary_df['status'] == 'SUCCESS']
   
   if len(successful_scenarios) > 0:
   print(f"\n INCOME PREDICTION INSIGHTS:")
   print(f"   Scenarios tested: {len(successful_scenarios)}")
   print(f"   👥 Total customers: {successful_scenarios['customers'].sum()}")
   
   # Sort by average income
   sorted_scenarios = successful_scenarios.sort_values('avg_income', ascending=False)
   
   print(f"\n INCOME RANKINGS (by average predicted income):")
   for i, row in sorted_scenarios.iterrows():
   print(f"   {row.name+1}. {row['scenario']}: ${row['avg_income']:.2f}")
   print(f"   Range: ${row['min_income']:.2f} - ${row['max_income']:.2f}")
   
   print(f"\n OVERALL STATISTICS:")
   print(f"   Highest average income: {sorted_scenarios.iloc[0]['scenario']} (${sorted_scenarios.iloc[0]['avg_income']:.2f})")
   print(f"   Lowest average income: {sorted_scenarios.iloc[-1]['scenario']} (${sorted_scenarios.iloc[-1]['avg_income']:.2f})")
   print(f"   Most consistent predictions: {sorted_scenarios.loc[sorted_scenarios['avg_ci_width'].idxmin(), 'scenario']}")
   print(f"   Least consistent predictions: {sorted_scenarios.loc[sorted_scenarios['avg_ci_width'].idxmax(), 'scenario']}")
   
   # Show any failures
   failed_scenarios = summary_df[summary_df['status'] != 'SUCCESS']
   if len(failed_scenarios) > 0:
   print(f"\nFAILED: FAILED SCENARIOS:")
   for _, row in failed_scenarios.iterrows():
   print(f"   • {row['scenario']}: {row['status']}")
   if 'error' in row and pd.notna(row['error']):
   print(f"   Error: {row['error']}")

if __name__ == "__main__":
   print("*** BUSINESS SCENARIO TESTING SUITE ***")
   print("=" * 60)
   print("Testing model predictions for realistic business use cases")
   print()

   # Create business scenarios
   test_scenarios = create_business_scenarios()

   # Save test files
   save_business_scenarios(test_scenarios)

   # Run tests
   all_results, scenario_summaries = run_business_tests()

   # Analyze results
   if scenario_summaries:
   analyze_business_results(all_results, scenario_summaries)

   print("\n*** BUSINESS SCENARIO TESTING COMPLETE! ***")
   print("Check the generated CSV files for detailed business insights.")
