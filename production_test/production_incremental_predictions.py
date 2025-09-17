# =============================================================================
# PRODUCTION INCREMENTAL PREDICTIONS MANAGER
# =============================================================================
#
# OBJECTIVE: Maintain one master prediction dataset with incremental updates
#
# STRATEGY:
# - Single master file: master_predictions.csv & master_predictions.json
# - Append new predictions to existing dataset
# - Maintain prediction history with timestamps
# - Automatic deduplication based on customer ID + date
# - Archive old predictions while keeping recent ones
# - Efficient storage and retrieval for production use
#
# BENEFITS:
# - Scalable for thousands of daily predictions
# - Historical tracking of customer income evolution
# - Single source of truth for all predictions
# - Efficient storage management
# - Easy integration with business systems
# =============================================================================

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)

class IncrementalPredictionManager:
    """
    Manages incremental prediction dataset with automatic archiving and deduplication
    """
    
    def __init__(self, base_folder="model_pred_files"):
        self.base_folder = base_folder
        self.master_csv = os.path.join(base_folder, "master_predictions.csv")
        self.master_json = os.path.join(base_folder, "master_predictions.json")
        self.archive_folder = os.path.join(base_folder, "archive")
        
        # Create folders if they don't exist
        self._create_folders()
        
    def _create_folders(self):
        """Create necessary folders"""
        print("📁 SETTING UP INCREMENTAL PREDICTION STRUCTURE")
        print("="*60)
        
        for folder in [self.base_folder, self.archive_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"✅ Created folder: {folder}")
            else:
                print(f"✅ Folder exists: {folder}")
    
    def load_master_dataset(self):
        """
        Load existing master dataset or create empty one
        """
        print("\n📂 LOADING MASTER DATASET")
        print("="*50)
        
        if os.path.exists(self.master_csv):
            try:
                df_master = pd.read_csv(self.master_csv, encoding='utf-8')
                print(f"✅ Master dataset loaded: {df_master.shape}")
                print(f"📊 Date range: {df_master['prediction_date'].min()} to {df_master['prediction_date'].max()}")
                print(f"🆔 Unique customers: {df_master['identificador_unico'].nunique():,}")
                return df_master
            except Exception as e:
                print(f"⚠️ Error loading master dataset: {e}")
                print("🔄 Creating new master dataset...")
                return self._create_empty_master()
        else:
            print("📝 No master dataset found - creating new one")
            return self._create_empty_master()
    
    def _create_empty_master(self):
        """Create empty master dataset with proper structure"""
        columns = [
            # Customer identification
            'identificador_unico', 'cliente',
            
            # Core predictions
            'predicted_income', 'income_lower_90', 'income_upper_90',
            
            # Business classifications
            'income_segment', 'confidence_category', 'business_priority',
            'recommendation',
            
            # Technical details
            'confidence_level', 'ci_width',
            
            # Metadata
            'prediction_date', 'model_version', 'batch_id'
        ]
        
        return pd.DataFrame(columns=columns)
    
    def add_new_predictions(self, df_new_predictions, batch_id=None):
        """
        Add new predictions to master dataset with deduplication
        """
        print("\n➕ ADDING NEW PREDICTIONS TO MASTER DATASET")
        print("="*60)
        
        # Generate batch ID if not provided
        if batch_id is None:
            batch_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Add batch ID to new predictions
        df_new = df_new_predictions.copy()
        df_new['batch_id'] = batch_id
        
        print(f"📊 New predictions: {len(df_new):,}")
        print(f"🏷️ Batch ID: {batch_id}")
        
        # Load existing master dataset
        df_master = self.load_master_dataset()
        
        # Deduplication strategy
        if len(df_master) > 0:
            df_master, df_new = self._deduplicate_predictions(df_master, df_new)
        
        # Combine datasets
        df_combined = pd.concat([df_master, df_new], ignore_index=True)
        
        # Sort by customer ID and prediction date
        df_combined = df_combined.sort_values(['identificador_unico', 'prediction_date'])
        
        print(f"📊 Combined dataset: {len(df_combined):,} total predictions")
        print(f"🆔 Unique customers: {df_combined['identificador_unico'].nunique():,}")
        
        return df_combined, batch_id
    
    def _deduplicate_predictions(self, df_master, df_new):
        """
        Handle duplicate predictions based on customer ID and date
        """
        print("\n🔄 DEDUPLICATION PROCESS")
        print("="*40)
        
        # Convert prediction_date to date only for comparison
        df_master['prediction_date_only'] = pd.to_datetime(df_master['prediction_date']).dt.date
        df_new['prediction_date_only'] = pd.to_datetime(df_new['prediction_date']).dt.date
        
        # Find duplicates (same customer + same date)
        merge_cols = ['identificador_unico', 'prediction_date_only']
        duplicates = df_new.merge(df_master[merge_cols], on=merge_cols, how='inner')
        
        if len(duplicates) > 0:
            print(f"⚠️ Found {len(duplicates):,} duplicate predictions")
            print("🔄 Strategy: Keep newest prediction, archive old ones")
            
            # Remove old predictions for customers with new predictions today
            duplicate_customers_today = duplicates[merge_cols].drop_duplicates()
            
            # Archive old predictions
            df_to_archive = df_master.merge(duplicate_customers_today, on=merge_cols, how='inner')
            if len(df_to_archive) > 0:
                self._archive_predictions(df_to_archive, "duplicate_replacement")
            
            # Remove duplicates from master
            df_master = df_master.merge(duplicate_customers_today, on=merge_cols, how='left', indicator=True)
            df_master = df_master[df_master['_merge'] == 'left_only'].drop('_merge', axis=1)
            
            print(f"✅ Removed {len(df_to_archive):,} old predictions")
        else:
            print("✅ No duplicates found")
        
        # Clean up temporary columns
        df_master = df_master.drop('prediction_date_only', axis=1)
        df_new = df_new.drop('prediction_date_only', axis=1)
        
        return df_master, df_new
    
    def _archive_predictions(self, df_to_archive, reason):
        """
        Archive old predictions to separate file
        """
        archive_filename = f"archived_predictions_{reason}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        archive_path = os.path.join(self.archive_folder, archive_filename)
        
        df_to_archive.to_csv(archive_path, index=False, encoding='utf-8')
        print(f"📦 Archived {len(df_to_archive):,} predictions to: {archive_filename}")
    
    def cleanup_old_predictions(self, days_to_keep=90):
        """
        Archive predictions older than specified days
        """
        print(f"\n🧹 CLEANING UP PREDICTIONS OLDER THAN {days_to_keep} DAYS")
        print("="*60)
        
        df_master = self.load_master_dataset()
        
        if len(df_master) == 0:
            print("📝 No predictions to clean up")
            return df_master
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d')
        
        # Convert prediction_date to datetime
        df_master['prediction_datetime'] = pd.to_datetime(df_master['prediction_date'])
        
        # Separate old and recent predictions
        df_old = df_master[df_master['prediction_datetime'] < cutoff_date]
        df_recent = df_master[df_master['prediction_datetime'] >= cutoff_date]
        
        print(f"📊 Total predictions: {len(df_master):,}")
        print(f"📦 Old predictions (< {cutoff_str}): {len(df_old):,}")
        print(f"✅ Recent predictions (>= {cutoff_str}): {len(df_recent):,}")
        
        # Archive old predictions if any
        if len(df_old) > 0:
            self._archive_predictions(df_old, f"cleanup_{days_to_keep}days")
            print(f"✅ Archived {len(df_old):,} old predictions")
        
        # Clean up temporary column
        df_recent = df_recent.drop('prediction_datetime', axis=1)
        
        return df_recent

    def cleanup_old_predictions_from_dataset(self, df_dataset, days_to_keep=90):
        """
        Archive predictions older than specified days from provided dataset
        """
        print(f"\n🧹 CLEANING UP PREDICTIONS OLDER THAN {days_to_keep} DAYS")
        print("="*60)

        if len(df_dataset) == 0:
            print("📝 No predictions to clean up")
            return df_dataset

        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d')

        # Convert prediction_date to datetime
        df_dataset['prediction_datetime'] = pd.to_datetime(df_dataset['prediction_date'])

        # Separate old and recent predictions
        df_old = df_dataset[df_dataset['prediction_datetime'] < cutoff_date]
        df_recent = df_dataset[df_dataset['prediction_datetime'] >= cutoff_date]

        print(f"📊 Total predictions: {len(df_dataset):,}")
        print(f"📦 Old predictions (< {cutoff_str}): {len(df_old):,}")
        print(f"✅ Recent predictions (>= {cutoff_str}): {len(df_recent):,}")

        # Archive old predictions if any
        if len(df_old) > 0:
            self._archive_predictions(df_old, f"cleanup_{days_to_keep}days")
            print(f"✅ Archived {len(df_old):,} old predictions")

        # Clean up temporary column
        df_recent = df_recent.drop('prediction_datetime', axis=1)

        return df_recent

    def save_master_dataset(self, df_master):
        """
        Save master dataset in both CSV and JSON formats
        """
        print("\n💾 SAVING MASTER DATASET")
        print("="*50)
        
        try:
            # Save CSV
            df_master.to_csv(self.master_csv, index=False, encoding='utf-8')
            csv_size = os.path.getsize(self.master_csv) / 1024  # KB
            print(f"✅ CSV saved: master_predictions.csv ({csv_size:.1f} KB)")
            
            # Save JSON (structured format)
            json_data = self._create_master_json(df_master)
            with open(self.master_json, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            json_size = os.path.getsize(self.master_json) / 1024  # KB
            print(f"✅ JSON saved: master_predictions.json ({json_size:.1f} KB)")
            
            return True
        except Exception as e:
            print(f"❌ Error saving master dataset: {e}")
            return False
    
    def _create_master_json(self, df_master):
        """
        Create structured JSON from master dataset
        """
        # Summary statistics
        summary = {
            "dataset_metadata": {
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "total_predictions": len(df_master),
                "unique_customers": int(df_master['identificador_unico'].nunique()),
                "date_range": {
                    "earliest": df_master['prediction_date'].min(),
                    "latest": df_master['prediction_date'].max()
                } if len(df_master) > 0 else {"earliest": None, "latest": None}
            },
            "business_summary": {
                "income_segments": df_master['income_segment'].value_counts().to_dict() if len(df_master) > 0 else {},
                "business_priorities": df_master['business_priority'].value_counts().to_dict() if len(df_master) > 0 else {},
                "confidence_levels": df_master['confidence_category'].value_counts().to_dict() if len(df_master) > 0 else {}
            }
        }
        
        # Recent predictions (last 30 days)
        if len(df_master) > 0:
            recent_date = datetime.now() - timedelta(days=30)
            df_recent = df_master[pd.to_datetime(df_master['prediction_date']) >= recent_date]
            
            recent_predictions = []
            for _, row in df_recent.iterrows():
                pred = {
                    "identificador_unico": str(row['identificador_unico']),
                    "predicted_income": float(row['predicted_income']),
                    "income_segment": str(row['income_segment']),
                    "business_priority": str(row['business_priority']),
                    "prediction_date": str(row['prediction_date']),
                    "batch_id": str(row['batch_id'])
                }
                recent_predictions.append(pred)
            
            summary["recent_predictions_30days"] = recent_predictions
        
        return summary
    
    def get_customer_history(self, identificador_unico):
        """
        Get prediction history for a specific customer
        """
        df_master = self.load_master_dataset()
        
        if len(df_master) == 0:
            return None
        
        customer_history = df_master[df_master['identificador_unico'] == identificador_unico].copy()
        customer_history = customer_history.sort_values('prediction_date', ascending=False)
        
        return customer_history
    
    def get_latest_predictions(self, days=1):
        """
        Get predictions from the last N days
        """
        df_master = self.load_master_dataset()
        
        if len(df_master) == 0:
            return None
        
        cutoff_date = datetime.now() - timedelta(days=days)
        df_master['prediction_datetime'] = pd.to_datetime(df_master['prediction_date'])
        
        latest = df_master[df_master['prediction_datetime'] >= cutoff_date].copy()
        latest = latest.drop('prediction_datetime', axis=1)
        latest = latest.sort_values('prediction_date', ascending=False)
        
        return latest

def process_new_predictions_incremental(df_new_predictions, cleanup_days=90):
    """
    Main function to process new predictions incrementally

    Args:
        df_new_predictions: DataFrame with new predictions
        cleanup_days: Days to keep in master dataset (older ones archived)

    Returns:
        dict: Processing results and statistics
    """
    print("🚀 INCREMENTAL PREDICTION PROCESSING")
    print("="*80)
    print("🎯 OBJECTIVE: Add new predictions to master dataset")
    print("📋 STRATEGY: Single master file + automatic archiving")
    print("="*80)

    # Initialize manager
    manager = IncrementalPredictionManager()

    # Add new predictions
    df_combined, batch_id = manager.add_new_predictions(df_new_predictions)

    # Cleanup old predictions (use the combined dataset)
    df_final = manager.cleanup_old_predictions_from_dataset(df_combined, days_to_keep=cleanup_days)

    # Save master dataset
    success = manager.save_master_dataset(df_final)

    if not success:
        print("❌ Failed to save master dataset")
        return None

    # Generate processing results
    results = {
        "processing_summary": {
            "batch_id": batch_id,
            "new_predictions_added": len(df_new_predictions),
            "total_predictions_in_master": len(df_final),
            "unique_customers": int(df_final['identificador_unico'].nunique()),
            "processing_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        "file_locations": {
            "master_csv": manager.master_csv,
            "master_json": manager.master_json,
            "archive_folder": manager.archive_folder
        },
        "business_insights": {
            "income_segments": df_final['income_segment'].value_counts().to_dict() if len(df_final) > 0 else {},
            "business_priorities": df_final['business_priority'].value_counts().to_dict() if len(df_final) > 0 else {},
            "average_predicted_income": float(df_final['predicted_income'].mean()) if len(df_final) > 0 else 0
        }
    }

    # Display summary
    print(f"\n🎉 INCREMENTAL PROCESSING COMPLETED!")
    print(f"📊 Batch ID: {batch_id}")
    print(f"➕ New predictions added: {len(df_new_predictions):,}")
    print(f"📋 Total predictions in master: {len(df_final):,}")
    print(f"🆔 Unique customers: {results['processing_summary']['unique_customers']:,}")
    print(f"💰 Average predicted income: ${results['business_insights']['average_predicted_income']:,.2f}")

    print(f"\n📂 FILES UPDATED:")
    print(f"   📄 master_predictions.csv")
    print(f"   📄 master_predictions.json")
    print(f"   📁 archive/ (for old predictions)")

    return results

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def example_single_customer_prediction():
    """
    Example: Add prediction for a single customer
    """
    print("\n📝 EXAMPLE: Single Customer Prediction")
    print("="*50)

    # Simulate single customer prediction
    single_prediction = pd.DataFrame({
        'identificador_unico': ['CUST_12345'],
        'cliente': ['Juan Perez'],
        'predicted_income': [1850.50],
        'income_lower_90': [1339.57],
        'income_upper_90': [2605.52],
        'income_segment': ['MIDDLE_INCOME_GROWTH'],
        'confidence_category': ['MEDIUM_CONFIDENCE'],
        'business_priority': ['HIGH_PRIORITY'],
        'recommendation': ['Target for standard loan products and credit increases'],
        'confidence_level': [0.90],
        'ci_width': [1265.95],
        'prediction_date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'model_version': ['XGBoost_v1.0_Final']
    })

    # Process incrementally
    results = process_new_predictions_incremental(single_prediction)

    if results:
        print("✅ Single customer prediction added to master dataset")

    return results

def example_batch_predictions():
    """
    Example: Add batch of predictions (e.g., 1000 customers)
    """
    print("\n📝 EXAMPLE: Batch Predictions")
    print("="*50)

    # Simulate batch predictions
    n_customers = 100  # Simulate 100 customers

    batch_predictions = pd.DataFrame({
        'identificador_unico': [f'CUST_{i:06d}' for i in range(1, n_customers + 1)],
        'cliente': [f'Customer_{i}' for i in range(1, n_customers + 1)],
        'predicted_income': np.random.normal(1500, 400, n_customers).round(2),
        'income_lower_90': lambda x: x['predicted_income'] - 510.93,
        'income_upper_90': lambda x: x['predicted_income'] + 755.02,
        'confidence_level': [0.90] * n_customers,
        'prediction_date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * n_customers,
        'model_version': ['XGBoost_v1.0_Final'] * n_customers
    })

    # Calculate derived columns
    batch_predictions['income_lower_90'] = batch_predictions['predicted_income'] - 510.93
    batch_predictions['income_upper_90'] = batch_predictions['predicted_income'] + 755.02
    batch_predictions['ci_width'] = batch_predictions['income_upper_90'] - batch_predictions['income_lower_90']

    # Add business classifications (simplified)
    batch_predictions['income_segment'] = batch_predictions['predicted_income'].apply(
        lambda x: 'LOW_INCOME_STABLE' if x < 1000 else
                 'MIDDLE_INCOME_STABLE' if x < 1500 else
                 'MIDDLE_INCOME_GROWTH' if x < 2000 else 'HIGH_INCOME_STABLE'
    )
    batch_predictions['confidence_category'] = 'MEDIUM_CONFIDENCE'
    batch_predictions['business_priority'] = 'HIGH_PRIORITY'
    batch_predictions['recommendation'] = 'Target for standard loan products and credit increases'

    # Process incrementally
    results = process_new_predictions_incremental(batch_predictions)

    if results:
        print(f"✅ Batch of {n_customers} predictions added to master dataset")

    return results

if __name__ == "__main__":
    print("🎯 INCREMENTAL PREDICTION MANAGEMENT EXAMPLES")
    print("="*80)

    # Example 1: Single customer
    print("\n1️⃣ SINGLE CUSTOMER PREDICTION:")
    example_single_customer_prediction()

    # Example 2: Batch predictions
    print("\n2️⃣ BATCH PREDICTIONS:")
    example_batch_predictions()

    # Example 3: Check customer history
    print("\n3️⃣ CUSTOMER HISTORY CHECK:")
    manager = IncrementalPredictionManager()
    history = manager.get_customer_history('CUST_12345')
    if history is not None and len(history) > 0:
        print(f"📊 Customer CUST_12345 has {len(history)} predictions")
        print(history[['prediction_date', 'predicted_income', 'business_priority']].head())
    else:
        print("📝 No history found for customer CUST_12345")

    # Example 4: Get latest predictions
    print("\n4️⃣ LATEST PREDICTIONS (Last 24 hours):")
    latest = manager.get_latest_predictions(days=1)
    if latest is not None and len(latest) > 0:
        print(f"📊 Found {len(latest)} predictions from last 24 hours")
        print(latest[['identificador_unico', 'predicted_income', 'prediction_date']].head())
    else:
        print("📝 No predictions found in last 24 hours")
