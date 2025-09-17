# =============================================================================
# PRODUCTION PIPELINE PART 3 - BUSINESS FORMATTING & OUTPUT GENERATION
# =============================================================================
#
# OBJECTIVE: Create business-ready prediction files in JSON and CSV formats
#
# INPUT: Predictions dataframe from Part 2 (with customer IDs and predictions)
# OUTPUT: Professional business files with risk classifications and insights
#
# BUSINESS FEATURES:
# - Risk segmentation based on income levels
# - Confidence classifications for decision support
# - Business recommendations for each customer
# - Professional JSON and CSV formats
# - Automated folder management for predictions
#
# OUTPUT FOLDER: model_pred_files/ (created automatically)
# OUTPUT FILES: 
# - income_predictions_YYYYMMDD_HHMMSS.csv
# - income_predictions_YYYYMMDD_HHMMSS.json
# - prediction_summary_YYYYMMDD_HHMMSS.json
# =============================================================================

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)

def create_prediction_folder():
    """
    Create model_pred_files folder if it doesn't exist
    Returns the folder path
    """
    print("📁 CREATING PREDICTION FOLDER")
    print("="*50)
    
    folder_name = "model_pred_files"
    
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"✅ Created new folder: {folder_name}")
        else:
            print(f"✅ Folder already exists: {folder_name}")
        
        # Get absolute path for clarity
        abs_path = os.path.abspath(folder_name)
        print(f"📂 Folder path: {abs_path}")
        
        return folder_name
    except Exception as e:
        print(f"❌ Error creating folder: {e}")
        return None

def classify_income_risk_segments(df):
    """
    Classify customers into business risk segments based on predicted income
    """
    print("\n🎯 CLASSIFYING INCOME RISK SEGMENTS")
    print("="*50)
    
    df = df.copy()
    
    # Income-based risk segmentation
    def get_income_segment(income):
        if income < 500:
            return "LOW_INCOME_HIGH_RISK"
        elif income < 1000:
            return "LOW_INCOME_STABLE"
        elif income < 1500:
            return "MIDDLE_INCOME_STABLE"
        elif income < 2000:
            return "MIDDLE_INCOME_GROWTH"
        elif income < 3000:
            return "HIGH_INCOME_STABLE"
        else:
            return "HIGH_INCOME_PREMIUM"
    
    # Apply income segmentation
    df['income_segment'] = df['predicted_income'].apply(get_income_segment)
    
    # Confidence classification based on prediction range
    def get_confidence_category(predicted_income, ci_width):
        if predicted_income < 1500 and ci_width < 1200:
            return "HIGH_CONFIDENCE"
        elif predicted_income < 2000 and ci_width < 1400:
            return "MEDIUM_CONFIDENCE"
        else:
            return "LOWER_CONFIDENCE"
    
    df['confidence_category'] = df.apply(
        lambda row: get_confidence_category(row['predicted_income'], row['ci_width']), 
        axis=1
    )
    
    # Business priority classification
    def get_business_priority(income_segment, confidence_category):
        if confidence_category == "HIGH_CONFIDENCE":
            if income_segment in ["MIDDLE_INCOME_STABLE", "MIDDLE_INCOME_GROWTH"]:
                return "HIGH_PRIORITY"
            elif income_segment in ["HIGH_INCOME_STABLE", "HIGH_INCOME_PREMIUM"]:
                return "PREMIUM_PRIORITY"
            else:
                return "STANDARD_PRIORITY"
        else:
            return "REVIEW_REQUIRED"
    
    df['business_priority'] = df.apply(
        lambda row: get_business_priority(row['income_segment'], row['confidence_category']),
        axis=1
    )
    
    # Business recommendations
    def get_recommendation(income_segment, confidence_category, business_priority):
        if business_priority == "PREMIUM_PRIORITY":
            return "Offer premium products and personalized services"
        elif business_priority == "HIGH_PRIORITY":
            return "Target for standard loan products and credit increases"
        elif business_priority == "STANDARD_PRIORITY":
            return "Monitor and offer basic financial products"
        else:
            return "Requires manual review before product offers"
    
    df['recommendation'] = df.apply(
        lambda row: get_recommendation(row['income_segment'], row['confidence_category'], row['business_priority']),
        axis=1
    )
    
    # Summary statistics
    segment_counts = df['income_segment'].value_counts()
    confidence_counts = df['confidence_category'].value_counts()
    priority_counts = df['business_priority'].value_counts()
    
    print(f"📊 Income segments:")
    for segment, count in segment_counts.items():
        pct = (count / len(df)) * 100
        print(f"   {segment}: {count:,} ({pct:.1f}%)")
    
    print(f"\n🔒 Confidence levels:")
    for conf, count in confidence_counts.items():
        pct = (count / len(df)) * 100
        print(f"   {conf}: {count:,} ({pct:.1f}%)")
    
    print(f"\n🎯 Business priorities:")
    for priority, count in priority_counts.items():
        pct = (count / len(df)) * 100
        print(f"   {priority}: {count:,} ({pct:.1f}%)")
    
    print("✅ Business classifications completed")
    return df

def create_business_summary(df):
    """
    Create comprehensive business summary for management reporting
    """
    print("\n📊 CREATING BUSINESS SUMMARY")
    print("="*50)
    
    summary = {
        "prediction_metadata": {
            "generation_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "model_version": "XGBoost_v1.0_Final",
            "total_customers": len(df),
            "model_rmse": 527.24,
            "confidence_level": "90%"
        },
        "income_statistics": {
            "mean_predicted_income": safe_round_float(df['predicted_income'].mean()),
            "median_predicted_income": safe_round_float(df['predicted_income'].median()),
            "min_predicted_income": safe_round_float(df['predicted_income'].min()),
            "max_predicted_income": safe_round_float(df['predicted_income'].max()),
            "std_predicted_income": safe_round_float(df['predicted_income'].std())
        },
        "confidence_analysis": {
            "average_ci_width": safe_round_float(df['ci_width'].mean()),
            "median_ci_width": safe_round_float(df['ci_width'].median()),
            "high_confidence_customers": int(df[df['confidence_category'] == 'HIGH_CONFIDENCE'].shape[0]),
            "review_required_customers": int(df[df['business_priority'] == 'REVIEW_REQUIRED'].shape[0])
        },
        "business_segments": {
            segment: int(count) for segment, count in df['income_segment'].value_counts().items()
        },
        "business_priorities": {
            priority: int(count) for priority, count in df['business_priority'].value_counts().items()
        },
        "confidence_distribution": {
            conf: int(count) for conf, count in df['confidence_category'].value_counts().items()
        }
    }
    
    print("✅ Business summary created")
    return summary

def format_for_csv_export(df):
    """
    Format dataframe for professional CSV export
    """
    print("\n📋 FORMATTING FOR CSV EXPORT")
    print("="*50)
    
    # Select and order columns for business use
    csv_columns = [
        # Customer identification
        'identificador_unico', 'cliente',
        
        # Core predictions
        'predicted_income', 'income_lower_90', 'income_upper_90',
        
        # Business classifications
        'income_segment', 'confidence_category', 'business_priority',
        
        # Business insights
        'recommendation',
        
        # Technical details
        'confidence_level', 'ci_width',
        
        # Metadata
        'prediction_date', 'model_version'
    ]
    
    # Keep only available columns
    available_columns = [col for col in csv_columns if col in df.columns]
    df_csv = df[available_columns].copy()
    
    # Round numeric columns for readability
    numeric_columns = ['predicted_income', 'income_lower_90', 'income_upper_90', 'ci_width']
    for col in numeric_columns:
        if col in df_csv.columns:
            df_csv[col] = df_csv[col].round(2)
    
    print(f"✅ CSV format ready with {len(available_columns)} columns")
    return df_csv

def safe_round_float(value, decimals=2):
    """
    Safely round a value to specified decimals, handling different data types
    """
    try:
        if pd.isna(value):
            return 0.0
        return round(float(value), decimals)
    except (ValueError, TypeError):
        return 0.0

def safe_string(value):
    """
    Safely convert value to string, handling NaN and None
    """
    if pd.isna(value) or value is None:
        return ""
    return str(value)

def format_for_json_export(df):
    """
    Format dataframe for structured JSON export
    """
    print("\n📋 FORMATTING FOR JSON EXPORT")
    print("="*50)

    # Convert dataframe to list of dictionaries
    records = []

    for _, row in df.iterrows():
        try:
            record = {
                "customer_identification": {
                    "identificador_unico": safe_string(row.get('identificador_unico', '')),
                    "cliente": safe_string(row.get('cliente', ''))
                },
                "income_prediction": {
                    "predicted_income": safe_round_float(row['predicted_income']),
                    "confidence_interval": {
                        "lower_bound": safe_round_float(row['income_lower_90']),
                        "upper_bound": safe_round_float(row['income_upper_90']),
                        "confidence_level": safe_round_float(row['confidence_level'], 2),
                        "interval_width": safe_round_float(row['ci_width'])
                    }
                },
                "business_classification": {
                    "income_segment": safe_string(row['income_segment']),
                    "confidence_category": safe_string(row['confidence_category']),
                    "business_priority": safe_string(row['business_priority']),
                    "recommendation": safe_string(row['recommendation'])
                },
                "metadata": {
                    "prediction_date": safe_string(row['prediction_date']),
                    "model_version": safe_string(row['model_version'])
                }
            }
            records.append(record)
        except Exception as e:
            print(f"⚠️ Warning: Error processing row {len(records)}: {e}")
            continue

    json_data = {
        "prediction_summary": {
            "total_customers": len(records),
            "generation_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "model_version": "XGBoost_v1.0_Final"
        },
        "customer_predictions": records
    }

    print(f"✅ JSON format ready with {len(records)} customer records")
    return json_data

def save_prediction_files(df_predictions, folder_path):
    """
    Save predictions in both CSV and JSON formats with timestamp
    """
    print("\n💾 SAVING PREDICTION FILES")
    print("="*50)

    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    try:
        # 1. Save CSV file
        csv_filename = f"income_predictions_{timestamp}.csv"
        csv_path = os.path.join(folder_path, csv_filename)

        df_csv = format_for_csv_export(df_predictions)
        df_csv.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"✅ CSV file saved: {csv_filename}")

        # 2. Save detailed JSON file
        json_filename = f"income_predictions_{timestamp}.json"
        json_path = os.path.join(folder_path, json_filename)

        json_data = format_for_json_export(df_predictions)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON file saved: {json_filename}")

        # 3. Save business summary
        summary_filename = f"prediction_summary_{timestamp}.json"
        summary_path = os.path.join(folder_path, summary_filename)

        business_summary = create_business_summary(df_predictions)
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(business_summary, f, indent=2, ensure_ascii=False)
        print(f"✅ Summary file saved: {summary_filename}")

        # Return file paths for reference
        saved_files = {
            'csv_file': csv_path,
            'json_file': json_path,
            'summary_file': summary_path
        }

        print(f"\n📂 All files saved in: {os.path.abspath(folder_path)}")
        return saved_files

    except Exception as e:
        print(f"❌ Error saving files: {e}")
        return None

def production_part3_main(predictions_input_path, create_folder=True):
    """
    Main function for Production Part 3: Business Formatting & Output Generation

    Input: Predictions CSV from Part 2 or predictions dataframe
    Output: Business-ready CSV and JSON files in model_pred_files folder
    """
    print("🚀 PRODUCTION PART 3 - BUSINESS FORMATTING & OUTPUT GENERATION")
    print("="*80)
    print("🎯 OBJECTIVE: Create business-ready prediction files (CSV + JSON)")
    print("📋 INPUT: Predictions with customer IDs and income estimates")
    print("📋 OUTPUT: Professional business files with risk classifications")
    print("="*80)

    # Step 1: Load predictions data
    if isinstance(predictions_input_path, str):
        print("📂 Loading predictions from file...")
        try:
            df_predictions = pd.read_csv(predictions_input_path, encoding='utf-8')
            print(f"✅ Predictions loaded: {df_predictions.shape}")
        except Exception as e:
            print(f"❌ Error loading predictions: {e}")
            return None
    elif isinstance(predictions_input_path, pd.DataFrame):
        print("📊 Using provided predictions dataframe...")
        df_predictions = predictions_input_path.copy()
        print(f"✅ Predictions dataframe: {df_predictions.shape}")
    else:
        print("❌ Invalid input: Expected file path or DataFrame")
        return None

    # Step 2: Create prediction folder
    if create_folder:
        folder_path = create_prediction_folder()
        if folder_path is None:
            print("❌ Failed to create prediction folder")
            return None
    else:
        folder_path = "."  # Current directory

    # Step 3: Add business classifications
    df_business = classify_income_risk_segments(df_predictions)

    # Step 4: Save all prediction files
    saved_files = save_prediction_files(df_business, folder_path)

    if saved_files is None:
        print("❌ Failed to save prediction files")
        return None

    # Step 5: Display final summary
    print(f"\n🎉 PRODUCTION PART 3 COMPLETED!")
    print(f"📊 Business files generated for {len(df_business):,} customers")
    print(f"📁 Files saved in: model_pred_files/")
    print(f"📋 Files created:")
    for file_type, file_path in saved_files.items():
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / 1024  # KB
        print(f"   📄 {filename} ({file_size:.1f} KB)")

    # Show business insights summary
    print(f"\n💼 BUSINESS INSIGHTS SUMMARY:")
    high_priority = len(df_business[df_business['business_priority'] == 'HIGH_PRIORITY'])
    premium_priority = len(df_business[df_business['business_priority'] == 'PREMIUM_PRIORITY'])
    review_required = len(df_business[df_business['business_priority'] == 'REVIEW_REQUIRED'])

    print(f"   🎯 High Priority Customers: {high_priority:,}")
    print(f"   💎 Premium Priority Customers: {premium_priority:,}")
    print(f"   ⚠️  Review Required: {review_required:,}")

    avg_income = df_business['predicted_income'].mean()
    high_confidence = len(df_business[df_business['confidence_category'] == 'HIGH_CONFIDENCE'])

    print(f"   💰 Average Predicted Income: ${avg_income:,.2f}")
    print(f"   🔒 High Confidence Predictions: {high_confidence:,} ({high_confidence/len(df_business)*100:.1f}%)")

    return df_business, saved_files

# =============================================================================
# USAGE EXAMPLE
# =============================================================================
if __name__ == "__main__":
    # Input file from Part 2
    predictions_file = r'data\production\income_predictions.csv'

    print("🎯 PRODUCTION PART 3 - BUSINESS FORMATTING")
    print("="*80)

    # Run Part 3 pipeline
    result = production_part3_main(predictions_file)

    if result is not None:
        df_business, saved_files = result
        print(f"\n📋 SAMPLE BUSINESS-FORMATTED PREDICTIONS:")
        display_cols = [
            'identificador_unico', 'predicted_income', 'income_segment',
            'confidence_category', 'business_priority', 'recommendation'
        ]
        available_cols = [col for col in display_cols if col in df_business.columns]
        print(df_business[available_cols].head())

        print(f"\n📊 BUSINESS CLASSIFICATION SUMMARY:")
        print(f"Income Segments:")
        print(df_business['income_segment'].value_counts())
        print(f"\nBusiness Priorities:")
        print(df_business['business_priority'].value_counts())

        print(f"\n🎯 SUCCESS! Business files ready for management review")
        print(f"📂 Check model_pred_files/ folder for all output files")
    else:
        print(f"\n❌ FAILED! Check error messages above")

# =============================================================================
# BUSINESS FORMATTING TECHNICAL NOTES
# =============================================================================
"""
🎯 BUSINESS FORMATTING STRATEGY:

1. RISK SEGMENTATION:
   • LOW_INCOME_HIGH_RISK: < $500 (requires special attention)
   • LOW_INCOME_STABLE: $500-$1,000 (basic products)
   • MIDDLE_INCOME_STABLE: $1,000-$1,500 (standard products)
   • MIDDLE_INCOME_GROWTH: $1,500-$2,000 (growth opportunities)
   • HIGH_INCOME_STABLE: $2,000-$3,000 (premium products)
   • HIGH_INCOME_PREMIUM: > $3,000 (VIP treatment)

2. CONFIDENCE CLASSIFICATION:
   • HIGH_CONFIDENCE: Low income + narrow CI (automated decisions OK)
   • MEDIUM_CONFIDENCE: Medium income + moderate CI (standard review)
   • LOWER_CONFIDENCE: High income + wide CI (manual review required)

3. BUSINESS PRIORITIES:
   • PREMIUM_PRIORITY: High confidence + high income (VIP customers)
   • HIGH_PRIORITY: High confidence + middle income (target customers)
   • STANDARD_PRIORITY: High confidence + low income (basic products)
   • REVIEW_REQUIRED: Lower confidence (manual review needed)

🔧 OUTPUT FILES:

1. CSV FILE (income_predictions_YYYYMMDD_HHMMSS.csv):
   • Business-ready spreadsheet format
   • Customer IDs + predictions + classifications
   • Ready for Excel analysis and reporting

2. JSON FILE (income_predictions_YYYYMMDD_HHMMSS.json):
   • Structured data format for API integration
   • Nested structure with customer details
   • Machine-readable for automated systems

3. SUMMARY FILE (prediction_summary_YYYYMMDD_HHMMSS.json):
   • Executive summary with key metrics
   • Business segment distributions
   • Model performance statistics

📊 BUSINESS USE CASES:

• CREDIT ASSESSMENT: Use business_priority for loan approvals
• MARKETING CAMPAIGNS: Target by income_segment
• PRODUCT RECOMMENDATIONS: Use recommendation field
• RISK MANAGEMENT: Monitor confidence_category
• EXECUTIVE REPORTING: Use summary file for dashboards

✅ FOLDER MANAGEMENT:

• AUTO-CREATION: model_pred_files/ folder created automatically
• TIMESTAMPED FILES: Unique filenames prevent overwrites
• ORGANIZED STORAGE: All prediction files in one location
• AUDIT TRAIL: Complete history of prediction runs

🎯 INTEGRATION READY:

• CSV: Import into Excel, Power BI, Tableau
• JSON: API integration, web applications
• SUMMARY: Executive dashboards, reporting tools
• AUTOMATED: Can be scheduled for regular runs
"""
