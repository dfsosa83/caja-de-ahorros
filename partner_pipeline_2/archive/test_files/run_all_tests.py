#!/usr/bin/env python3
# =============================================================================
# MASTER TEST RUNNER - COMPREHENSIVE PIPELINE TESTING
# =============================================================================
#
# OBJECTIVE: Run all test suites and generate comprehensive analysis
# 
# TEST SUITES:
# 1. Edge Cases & Minimal Data (test_edge_cases_minimal_data.py)
# 2. Data Quality & Validation (test_data_quality_scenarios.py)  
# 3. Business Scenarios (test_business_scenarios.py)
#
# USAGE: python run_all_tests.py
# =============================================================================

import pandas as pd
import numpy as np
import os
import subprocess
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def print_header(title):
   """Print formatted header"""
   print("\n" + "=" * 80)
   print(f"*** {title} ***")
   print("=" * 80)

def print_section(title):
   """Print formatted section"""
   print(f"\n*** {title} ***")
   print("-" * 60)

def run_test_suite(test_script, suite_name):
   """
   Run a test suite and capture results
   """
   print_section(f"Running {suite_name}")
   
   try:
   # Check if test script exists
   if not os.path.exists(test_script):
   print(f"FAILED: Test script not found: {test_script}")
   return False
   
   # Run the test script
   print(f"*** Executing: {test_script} ***")
   result = subprocess.run([sys.executable, test_script],
   capture_output=True, text=True, timeout=300)

   if result.returncode == 0:
   print(f"SUCCESS: {suite_name} completed successfully")
   # Print last few lines of output for summary
   output_lines = result.stdout.split('\n')
   summary_lines = [line for line in output_lines[-10:] if line.strip()]
   if summary_lines:
   print("Summary:")
   for line in summary_lines[-5:]:
   if line.strip():
   print(f"   {line}")
   return True
   else:
   print(f"FAILED: {suite_name} failed with return code: {result.returncode}")
   if result.stderr:
   print(f"Error output: {result.stderr[:500]}")
   return False

   except subprocess.TimeoutExpired:
   print(f"TIMEOUT: {suite_name} timed out after 5 minutes")
   return False
   except Exception as e:
   print(f"ERROR: Error running {suite_name}: {str(e)}")
   return False

def collect_all_results():
   """
   Collect and consolidate results from all test suites
   """
   print_section("Collecting and Consolidating Results")
   
   results_files = {
   'edge_cases': 'edge_case_test_results.csv',
   'data_quality': 'data_quality_test_results.csv', 
   'business_summary': 'business_scenario_summary.csv',
   'business_detailed': 'business_scenario_detailed_results.csv'
   }
   
   consolidated_results = {}
   
   for result_type, filename in results_files.items():
   if os.path.exists(filename):
   try:
   df = pd.read_csv(filename)
   consolidated_results[result_type] = df
   print(f"SUCCESS: Loaded {filename}: {len(df)} records")
   except Exception as e:
   print(f"WARNING: Could not load {filename}: {str(e)}")
   else:
   print(f"WARNING: Results file not found: {filename}")
   
   return consolidated_results

def generate_master_analysis(consolidated_results):
   """
   Generate comprehensive analysis across all test suites
   """
   print_section("Master Analysis - All Test Suites")
   
   # Initialize counters
   total_tests = 0
   successful_tests = 0
   failed_tests = 0
   
   analysis_summary = {
   'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
   'test_suites_run': [],
   'total_scenarios': 0,
   'successful_scenarios': 0,
   'failed_scenarios': 0,
   'key_insights': []
   }
   
   # Analyze edge cases
   if 'edge_cases' in consolidated_results:
   edge_df = consolidated_results['edge_cases']
   total_tests += len(edge_df)
   successful_edge = len(edge_df[edge_df['status'] == 'SUCCESS'])
   successful_tests += successful_edge
   failed_tests += len(edge_df) - successful_edge
   
   analysis_summary['test_suites_run'].append('Edge Cases')
   analysis_summary['key_insights'].append(f"Edge Cases: {successful_edge}/{len(edge_df)} scenarios handled successfully")
   
   print(f"Edge Cases Analysis:")
   print(f"   SUCCESS: {successful_edge}/{len(edge_df)}")
   print(f"   FAILED: {len(edge_df) - successful_edge}/{len(edge_df)}")

   if successful_edge > 0:
   successful_edge_df = edge_df[edge_df['status'] == 'SUCCESS']
   avg_prediction = successful_edge_df['predicted_income'].mean()
   print(f"   Average prediction: ${avg_prediction:.2f}")
   
   # Analyze data quality
   if 'data_quality' in consolidated_results:
   quality_df = consolidated_results['data_quality']
   total_tests += len(quality_df)
   successful_quality = len(quality_df[quality_df['status'] == 'SUCCESS'])
   successful_tests += successful_quality
   failed_tests += len(quality_df) - successful_quality
   
   analysis_summary['test_suites_run'].append('Data Quality')
   analysis_summary['key_insights'].append(f"Data Quality: {successful_quality}/{len(quality_df)} scenarios handled gracefully")
   
   print(f"\nData Quality Analysis:")
   print(f"   SUCCESS: Handled gracefully: {successful_quality}/{len(quality_df)}")
   print(f"   FAILED: Pipeline errors: {len(quality_df) - successful_quality}/{len(quality_df)}")
   
   # Analyze business scenarios
   if 'business_summary' in consolidated_results:
   business_df = consolidated_results['business_summary']
   total_tests += len(business_df)
   successful_business = len(business_df[business_df['status'] == 'SUCCESS'])
   successful_tests += successful_business
   failed_tests += len(business_df) - successful_business
   
   analysis_summary['test_suites_run'].append('Business Scenarios')
   
   if successful_business > 0:
   successful_biz_df = business_df[business_df['status'] == 'SUCCESS']
   highest_income_scenario = successful_biz_df.loc[successful_biz_df['avg_income'].idxmax()]
   lowest_income_scenario = successful_biz_df.loc[successful_biz_df['avg_income'].idxmin()]
   
   analysis_summary['key_insights'].append(f"Highest income predictions: {highest_income_scenario['scenario']} (${highest_income_scenario['avg_income']:.2f})")
   analysis_summary['key_insights'].append(f"Lowest income predictions: {lowest_income_scenario['scenario']} (${lowest_income_scenario['avg_income']:.2f})")
   
   print(f"\nBusiness Scenarios Analysis:")
   print(f"   SUCCESS: {successful_business}/{len(business_df)}")
   print(f"   Highest avg income: {highest_income_scenario['scenario']} (${highest_income_scenario['avg_income']:.2f})")
   print(f"   Lowest avg income: {lowest_income_scenario['scenario']} (${lowest_income_scenario['avg_income']:.2f})")
   
   # Overall summary
   analysis_summary['total_scenarios'] = total_tests
   analysis_summary['successful_scenarios'] = successful_tests
   analysis_summary['failed_scenarios'] = failed_tests
   
   print(f"\nOVERALL TEST SUMMARY:")
   print(f"   Total test scenarios: {total_tests}")
   print(f"   SUCCESS: {successful_tests} ({successful_tests/total_tests*100:.1f}%)")
   print(f"   FAILED: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
   print(f"   Test suites run: {', '.join(analysis_summary['test_suites_run'])}")
   
   # Save master analysis
   with open('master_test_analysis.txt', 'w') as f:
   f.write("INCOME PREDICTION PIPELINE - MASTER TEST ANALYSIS\n")
   f.write("=" * 60 + "\n\n")
   f.write(f"Test Run Timestamp: {analysis_summary['timestamp']}\n\n")
   
   f.write("SUMMARY STATISTICS:\n")
   f.write(f"Total Scenarios Tested: {analysis_summary['total_scenarios']}\n")
   f.write(f"Successful Scenarios: {analysis_summary['successful_scenarios']}\n")
   f.write(f"Failed Scenarios: {analysis_summary['failed_scenarios']}\n")
   f.write(f"Success Rate: {successful_tests/total_tests*100:.1f}%\n\n")
   
   f.write("TEST SUITES RUN:\n")
   for suite in analysis_summary['test_suites_run']:
   f.write(f"- {suite}\n")
   
   f.write("\nKEY INSIGHTS:\n")
   for insight in analysis_summary['key_insights']:
   f.write(f"- {insight}\n")
   
   print(f"\nMaster analysis saved to: master_test_analysis.txt")
   
   return analysis_summary

def cleanup_test_files():
   """
   Clean up temporary test files (optional)
   """
   print_section("Cleanup (Optional)")
   
   test_files = [f for f in os.listdir('.') if f.startswith('test_scenario_') or f.startswith('test_data_quality_') or f.startswith('test_business_')]
   
   print(f"Found {len(test_files)} temporary test files")
   
   # Don't auto-delete, just list them
   if test_files:
   print("Temporary test files created:")
   for file in sorted(test_files):
   print(f"   {file}")
   print("\nNOTE: These files can be deleted manually if no longer needed")

def main():
   """
   Main test runner function
   """
   print_header("COMPREHENSIVE PIPELINE TESTING SUITE")
   print("Testing income prediction pipeline robustness and accuracy")
   print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
   
   # Test suites to run
   test_suites = [
   ('test_edge_cases_minimal_data.py', 'Edge Cases & Minimal Data'),
   ('test_data_quality_scenarios.py', 'Data Quality & Validation'),
   ('test_business_scenarios.py', 'Business Scenarios')
   ]
   
   # Track results
   suite_results = {}
   
   # Run each test suite
   for test_script, suite_name in test_suites:
   success = run_test_suite(test_script, suite_name)
   suite_results[suite_name] = success
   
   # Collect and analyze all results
   print_header("CONSOLIDATING RESULTS")
   consolidated_results = collect_all_results()
   
   if consolidated_results:
   analysis_summary = generate_master_analysis(consolidated_results)
   else:
   print("WARNING: No results to analyze - check if test suites ran successfully")
   
   # Cleanup information
   cleanup_test_files()
   
   # Final summary
   print_header("TESTING COMPLETE")
   successful_suites = sum(suite_results.values())
   total_suites = len(suite_results)
   
   print(f"Test Suite Results: {successful_suites}/{total_suites} completed successfully")
   for suite_name, success in suite_results.items():
   status = "SUCCESS" if success else "FAILED"
   print(f"   {status}: {suite_name}")

   print(f"\nGenerated Files:")
   result_files = [
   'edge_case_test_results.csv',
   'data_quality_test_results.csv',
   'business_scenario_summary.csv',
   'business_scenario_detailed_results.csv',
   'master_test_analysis.txt'
   ]

   for file in result_files:
   if os.path.exists(file):
   print(f"   {file}")

   print(f"\n*** COMPREHENSIVE TESTING COMPLETE! ***")
   print(f"   Check the generated files for detailed analysis and insights.")

if __name__ == "__main__":
   main()
