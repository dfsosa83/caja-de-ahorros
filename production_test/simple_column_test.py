#!/usr/bin/env python3
"""
Simple Column Analysis Test - No Dependencies Required
This script analyzes the datasets without requiring pandas or other ML libraries
"""

import os
import csv
import glob
from datetime import datetime

# Required columns for successful feature engineering
REQUIRED_COLUMNS = [
    'Cliente',                    # ID column
    'Identificador_Unico',        # Unique ID
    'Edad',                       # → edad (direct)
    'Ocupacion',                  # → ocupacion_consolidated_freq
    'NombreEmpleadorCliente',     # → nombreempleadorcliente_consolidated_freq
    'CargoEmpleoCliente',         # → cargoempleocliente_consolidated_freq
    'FechaIngresoEmpleo',         # → fechaingresoempleo_days, employment_years
    'saldo',                      # → saldo (direct), balance_to_payment_ratio
    'monto_letra',                # → balance_to_payment_ratio, professional_stability_score
    'fecha_inicio'                # → fecha_inicio_days
]

# Optional columns (not required for model)
OPTIONAL_COLUMNS = [
    'ingresos_reportados',        # TARGET - not needed for prediction
    'Segmento',                   # Not used in model
    'Sexo',                       # Not used in final model
    'Ciudad',                     # Not used in final model  
    'Pais',                       # Not used in final model
    'Estado_Civil',               # Not used in final model
    'productos_activos',          # Not used in model
    'letras_mensuales',           # Not used in model
    'fecha_vencimiento',          # Not used in model
    'ControlDate',                # Metadata
    'monto_prestamo',             # Not used in model
    'tasa_prestamo',              # Not used in model
    'data_source',                # Metadata
    'processing_timestamp'        # Metadata
]

def analyze_csv_file(file_path):
    """Analyze a CSV file for column structure and null values"""
    print(f"\n🔍 ANALYZING: {os.path.basename(file_path)}")
    print("="*60)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read header
            reader = csv.reader(f)
            header = next(reader)
            
            # Count rows and analyze nulls
            rows = list(reader)
            total_rows = len(rows)
            
        print(f"📊 Total rows: {total_rows}")
        print(f"📊 Total columns: {len(header)}")
        
        # Column validation
        actual_columns = set(header)
        required_columns = set(REQUIRED_COLUMNS)
        optional_columns = set(OPTIONAL_COLUMNS)
        
        # Check missing required columns
        missing_required = required_columns - actual_columns
        
        # Check extra columns
        known_columns = required_columns | optional_columns
        extra_columns = actual_columns - known_columns
        
        # Check present optional columns
        present_optional = optional_columns & actual_columns
        
        print(f"\n✅ Required columns present: {len(required_columns & actual_columns)}/{len(REQUIRED_COLUMNS)}")
        
        if missing_required:
            print(f"❌ Missing REQUIRED columns: {list(missing_required)}")
        else:
            print("✅ All required columns present!")
        
        if present_optional:
            print(f"📋 Optional columns present: {list(present_optional)}")
        
        if extra_columns:
            print(f"⚠️  Extra/Unknown columns: {list(extra_columns)}")
        
        # Null analysis for required columns
        print(f"\n🔍 NULL VALUE ANALYSIS:")
        print("-"*40)
        
        for col in REQUIRED_COLUMNS:
            if col in header:
                col_index = header.index(col)
                null_count = sum(1 for row in rows if not row[col_index] or row[col_index].strip() == '')
                null_percentage = (null_count / total_rows) * 100 if total_rows > 0 else 0
                
                if null_count > 0:
                    print(f"⚠️  {col}: {null_count}/{total_rows} ({null_percentage:.1f}%) NULL/empty values")
                else:
                    print(f"✅ {col}: No NULL values")
        
        # Sample data preview
        print(f"\n📋 SAMPLE DATA (first row):")
        print("-"*40)
        if rows:
            for i, col_name in enumerate(header[:10]):  # Show first 10 columns
                value = rows[0][i] if i < len(rows[0]) else "N/A"
                print(f"   {col_name}: {value}")
            if len(header) > 10:
                print(f"   ... and {len(header) - 10} more columns")
        
        return {
            'file_name': os.path.basename(file_path),
            'total_rows': total_rows,
            'total_columns': len(header),
            'missing_required': list(missing_required),
            'extra_columns': list(extra_columns),
            'validation_passed': len(missing_required) == 0
        }
        
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")
        return None

def main():
    print("🧪 SIMPLE COLUMN ANALYSIS TEST")
    print("="*80)
    print("🎯 OBJECTIVE: Analyze dataset columns without requiring ML libraries")
    print("📋 FEATURES: Column validation, null analysis, data preview")
    print("="*80)
    
    # Find all CSV files in data/external
    external_data_path = "../data/external"
    if not os.path.exists(external_data_path):
        print(f"❌ External data folder not found: {external_data_path}")
        return
    
    csv_files = glob.glob(os.path.join(external_data_path, "*.csv"))
    
    if not csv_files:
        print(f"❌ No CSV files found in: {external_data_path}")
        return
    
    print(f"📂 Found {len(csv_files)} datasets to analyze:")
    for i, file_path in enumerate(csv_files, 1):
        print(f"   {i}. {os.path.basename(file_path)}")
    
    # Analyze each dataset
    results = []
    for dataset_path in csv_files:
        result = analyze_csv_file(dataset_path)
        if result:
            results.append(result)
    
    # Summary
    print(f"\n{'='*80}")
    print("🎯 ANALYSIS SUMMARY")
    print(f"{'='*80}")
    
    successful_validations = sum(1 for r in results if r['validation_passed'])
    failed_validations = len(results) - successful_validations
    
    print(f"📊 Total datasets analyzed: {len(results)}")
    print(f"✅ Datasets with all required columns: {successful_validations}")
    print(f"❌ Datasets missing required columns: {failed_validations}")
    
    if failed_validations > 0:
        print(f"\n🚨 DATASETS WITH ISSUES:")
        for result in results:
            if not result['validation_passed']:
                print(f"   ❌ {result['file_name']}: Missing {result['missing_required']}")
    
    print(f"\n📋 NEXT STEPS:")
    print(f"   1. Fix any missing required columns")
    print(f"   2. Run full pipeline test with: python production_pipeline_complete_test.py test_all")
    print(f"   3. Check model prediction accuracy")

if __name__ == "__main__":
    main()
