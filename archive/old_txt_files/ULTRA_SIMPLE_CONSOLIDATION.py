# =============================================================================
# ULTRA-SIMPLE CATEGORICAL CONSOLIDATION (COPY-PASTE READY)
# =============================================================================
# 
# OBJECTIVE: Create ultra-simple categorical features (4-5 categories max)
# STRATEGY: Keep only top 3-4 categories, consolidate everything else to 'Others'
# BASED ON: Your actual data analysis results
#
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

print("🎯 ULTRA-SIMPLE CATEGORICAL CONSOLIDATION")
print("="*80)
print("📋 Objective: Ultra-simple categories (4-5 max) for production stability")
print("🎯 Strategy: Keep only top 3-4 categories, rest → 'Others'")
print("📊 Target: 60-80% coverage with main categories")

# =============================================================================
# ULTRA-AGGRESSIVE CONSOLIDATION FUNCTION
# =============================================================================

def ultra_simple_consolidate(df, column_name, max_categories=4):
    """
    Ultra-aggressive consolidation: Keep only top N categories, rest → 'Others'
    
    Parameters:
    - df: DataFrame (your df_clientes)
    - column_name: Column to consolidate
    - max_categories: Maximum number of categories to keep (excluding 'Others')
    
    Returns:
    - Series with consolidated categories
    """
    print(f"\n🔥 ULTRA-CONSOLIDATION: {column_name}")
    print("="*60)
    
    if column_name not in df.columns:
        print(f"❌ Column '{column_name}' not found!")
        return df[column_name].copy() if column_name in df.columns else None
    
    # Get value counts and percentages
    value_counts = df[column_name].value_counts()
    total_non_null = df[column_name].notna().sum()
    
    print(f"📊 Original state:")
    print(f"   Total non-null values: {total_non_null:,}")
    print(f"   Unique categories: {len(value_counts):,}")
    print(f"   Missing values: {df[column_name].isnull().sum():,}")
    
    # Keep only top N categories
    keep_categories = list(value_counts.head(max_categories).index)
    consolidate_categories = list(value_counts.iloc[max_categories:].index)
    
    # Calculate statistics
    keep_count = sum(value_counts[cat] for cat in keep_categories)
    consolidate_count = sum(value_counts[cat] for cat in consolidate_categories)
    final_coverage = (keep_count / total_non_null) * 100
    
    print(f"\n🎯 Ultra-consolidation result:")
    print(f"   Keep: {len(keep_categories)} categories ({keep_count:,} records, {final_coverage:.1f}%)")
    print(f"   → 'Others': {len(consolidate_categories)} categories ({consolidate_count:,} records, {(100-final_coverage):.1f}%)")
    print(f"   Final categories: {len(keep_categories) + (1 if consolidate_categories else 0)}")
    
    # Show kept categories
    print(f"\n🏆 Categories to KEEP:")
    for i, cat in enumerate(keep_categories, 1):
        count = value_counts[cat]
        pct = (count / total_non_null) * 100
        print(f"   {i}. '{cat}': {count:,} ({pct:.1f}%)")
    
    # Create consolidated column
    consolidated_column = df[column_name].copy()
    
    # Handle categorical dtype
    if pd.api.types.is_categorical_dtype(consolidated_column):
        consolidated_column = consolidated_column.astype(str)
    
    # Handle NaN values
    consolidated_column = consolidated_column.fillna('__MISSING__')
    
    # Create mask for values to replace
    mask = ~consolidated_column.isin(keep_categories)
    mask = mask & (consolidated_column != '__MISSING__')
    
    # Apply consolidation
    consolidated_column.loc[mask] = 'Others'
    
    # Convert missing values back to NaN
    consolidated_column = consolidated_column.replace('__MISSING__', np.nan)
    
    print(f"   ✅ Created ultra-consolidated column")
    
    return consolidated_column

# =============================================================================
# APPLY ULTRA-CONSOLIDATION TO YOUR df_clientes
# =============================================================================

print(f"\n🚀 APPLYING ULTRA-CONSOLIDATION TO df_clientes")
print("="*60)

# Create a copy to work with
df_clientes_ultra = df_clientes.copy()

# =============================================================================
# ANALYZE TOP CATEGORIES TO MAKE INFORMED DECISIONS
# =============================================================================

def analyze_top_categories(df, column_name, top_n=10):
    """
    Show top N categories with their coverage to help decide how many to keep
    """
    print(f"\n🔍 TOP CATEGORIES ANALYSIS: {column_name}")
    print("="*50)

    if column_name not in df.columns:
        print(f"❌ Column '{column_name}' not found!")
        return

    value_counts = df[column_name].value_counts()
    total_non_null = df[column_name].notna().sum()

    print(f"📊 Total categories: {len(value_counts):,}")
    print(f"📊 Total records: {total_non_null:,}")

    cumulative_pct = 0
    print(f"\n🏆 Top {top_n} categories:")
    for i, (cat, count) in enumerate(value_counts.head(top_n).items(), 1):
        pct = (count / total_non_null) * 100
        cumulative_pct += pct
        print(f"   {i:2d}. '{cat[:40]}...': {count:,} ({pct:.1f}%) | Cumulative: {cumulative_pct:.1f}%")

    # Show coverage for different cut-offs
    print(f"\n📈 Coverage analysis:")
    for n in [3, 4, 5, 6, 7, 8]:
        if n <= len(value_counts):
            top_n_count = value_counts.head(n).sum()
            coverage = (top_n_count / total_non_null) * 100
            others_count = total_non_null - top_n_count
            others_pct = (others_count / total_non_null) * 100
            print(f"   Keep top {n}: {coverage:.1f}% coverage, {others_count:,} records ({others_pct:.1f}%) → 'Others'")

# Analyze each categorical feature
categorical_features = ['ocupacion', 'ciudad', 'nombreempleadorcliente', 'cargoempleocliente', 'sexo', 'estado_civil', 'pais']

for feature in categorical_features:
    if feature in df_clientes.columns:
        analyze_top_categories(df_clientes, feature, top_n=8)

print(f"\n🎯 RECOMMENDED CONSOLIDATION RULES (ADJUSTABLE)")
print("="*60)
print("📝 Based on the analysis above, here are suggested rules:")
print("   You can modify these numbers based on what you see!")

# Define flexible rules - YOU CAN MODIFY THESE NUMBERS!
ultra_rules = {
    'ocupacion': 6,           # Keep top 6: JUBILADO, DOCENTE, POLICIA, OFICINISTAS, SUPERVISOR, ASISTENTE
    'ciudad': 5,              # Keep top 5: PANAMA, ARRAIJAN, SAN MIGUELITO, LA CHORRERA, DAVID
    'nombreempleadorcliente': 6,  # Keep top 6: NO APLICA, MIN EDUCACION, MIN SEGURIDAD, CSS, CAJA AHORROS, MIN SALUD
    'cargoempleocliente': 6,  # Keep top 6: JUBILADO, POLICIA, DOCENTE, SUPERVISOR, SECRETARIA, OFICINISTA
    'sexo': 2,                # Keep both: Femenino, Masculino
    'estado_civil': 2,        # Keep top 2: Soltero, Casado
    'pais': 1                 # Keep only: PANAMA
}

print(f"\n📋 CURRENT RULES:")
for feature, max_cats in ultra_rules.items():
    print(f"   {feature}: Keep top {max_cats} categories")

# Apply ultra-consolidation
ultra_results = {}

for column, max_cats in ultra_rules.items():
    if column in df_clientes.columns:
        print(f"\n🔥 Processing: {column} (max {max_cats} categories)")
        
        # Apply ultra-consolidation
        df_clientes_ultra[f"{column}_ultra"] = ultra_simple_consolidate(
            df_clientes, column, max_categories=max_cats
        )
        
        # Store results for validation
        final_counts = df_clientes_ultra[f"{column}_ultra"].value_counts()
        ultra_results[column] = {
            'original_unique': df_clientes[column].nunique(),
            'final_unique': len(final_counts),
            'final_distribution': final_counts.to_dict()
        }
        
        print(f"   ✅ Created: {column}_ultra")
    else:
        print(f"   ⚠️ Column '{column}' not found in df_clientes")

# =============================================================================
# VALIDATION AND SUMMARY
# =============================================================================

print(f"\n✅ ULTRA-CONSOLIDATION VALIDATION")
print("="*60)

for column, result in ultra_results.items():
    ultra_column = f"{column}_ultra"
    
    print(f"\n📊 {column} → {ultra_column}:")
    print(f"   Original categories: {result['original_unique']:,}")
    print(f"   Final categories: {result['final_unique']:,}")
    reduction = ((result['original_unique'] - result['final_unique']) / result['original_unique']) * 100
    print(f"   Reduction: {reduction:.1f}%")
    
    print(f"   Final distribution:")
    total_records = sum(result['final_distribution'].values())
    for cat, count in result['final_distribution'].items():
        pct = (count / total_records) * 100
        print(f"     '{cat}': {count:,} ({pct:.1f}%)")

print(f"\n📈 ULTRA-CONSOLIDATION SUMMARY")
print("="*60)

total_original = sum(r['original_unique'] for r in ultra_results.values())
total_final = sum(r['final_unique'] for r in ultra_results.values())
overall_reduction = ((total_original - total_final) / total_original) * 100

print(f"📊 Overall impact:")
print(f"   Total original categories: {total_original:,}")
print(f"   Total final categories: {total_final:,}")
print(f"   Overall reduction: {overall_reduction:.1f}%")

print(f"\n📋 Per-feature summary:")
for column, result in ultra_results.items():
    reduction = ((result['original_unique'] - result['final_unique']) / result['original_unique']) * 100
    print(f"   {column}: {result['original_unique']:,} → {result['final_unique']:,} categories ({reduction:.1f}% reduction)")

# =============================================================================
# VISUALIZATION: BEFORE/AFTER CONSOLIDATION COMPARISON
# =============================================================================

def visualize_ultra_consolidation_impact(df_original, df_consolidated, ultra_results, max_cols=4):
    """
    Create before/after visualizations for ultra-consolidation
    """
    print(f"\n📊 CREATING BEFORE/AFTER CONSOLIDATION VISUALIZATIONS")
    print("="*60)

    # Select columns to visualize (limit to avoid overcrowding)
    columns_to_plot = list(ultra_results.keys())[:max_cols]

    fig, axes = plt.subplots(len(columns_to_plot), 2, figsize=(16, 5*len(columns_to_plot)))
    if len(columns_to_plot) == 1:
        axes = axes.reshape(1, -1)

    for i, column in enumerate(columns_to_plot):
        # Before consolidation (left side)
        ax1 = axes[i, 0]
        value_counts_original = df_original[column].value_counts().head(15)
        bars1 = value_counts_original.plot(kind='bar', ax=ax1, color='lightcoral', alpha=0.8)
        ax1.set_title(f'{column} - Before Consolidation\n({ultra_results[column]["original_unique"]} categories)',
                     fontweight='bold', fontsize=12)
        ax1.set_xlabel('')
        ax1.set_ylabel('Count', fontsize=10)
        ax1.tick_params(axis='x', rotation=45, labelsize=8)
        ax1.grid(True, alpha=0.3)

        # After consolidation (right side)
        ax2 = axes[i, 1]
        consolidated_col = f"{column}_ultra"
        if consolidated_col in df_consolidated.columns:
            value_counts_consolidated = df_consolidated[consolidated_col].value_counts()
            bars2 = value_counts_consolidated.plot(kind='bar', ax=ax2, color='lightblue', alpha=0.8)

            # Highlight Others category in orange
            if 'Others' in value_counts_consolidated.index:
                others_idx = list(value_counts_consolidated.index).index('Others')
                bars2.patches[others_idx].set_color('orange')
                bars2.patches[others_idx].set_alpha(0.9)

        ax2.set_title(f'{column} - After Consolidation\n({ultra_results[column]["final_unique"]} categories)',
                     fontweight='bold', fontsize=12)
        ax2.set_xlabel('')
        ax2.set_ylabel('Count', fontsize=10)
        ax2.tick_params(axis='x', rotation=45, labelsize=8)
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Print reduction summary
    print(f"\n📈 CONSOLIDATION IMPACT SUMMARY:")
    for column in columns_to_plot:
        original = ultra_results[column]["original_unique"]
        final = ultra_results[column]["final_unique"]
        reduction = ((original - final) / original) * 100
        print(f"   {column}: {original} → {final} categories ({reduction:.1f}% reduction)")

# Create the visualization
visualize_ultra_consolidation_impact(df_clientes, df_clientes_ultra, ultra_results)

# =============================================================================
# CREATE df_clientes_consolidated FOR NEXT STEPS
# =============================================================================

print(f"\n🔧 CREATING df_clientes_consolidated FOR NEXT STEPS")
print("="*50)

# Create df_clientes_consolidated with ultra-consolidated columns
df_clientes_consolidated = df_clientes_ultra.copy()

# Rename ultra columns to consolidated for compatibility with your workflow
for column in ultra_rules.keys():
    if f"{column}_ultra" in df_clientes_consolidated.columns:
        df_clientes_consolidated[f"{column}_consolidated"] = df_clientes_consolidated[f"{column}_ultra"]
        # Keep the ultra column for reference but use consolidated for next steps
        print(f"   ✅ Created: {column}_consolidated")

print(f"\n🎯 ULTRA-CONSOLIDATED FEATURES FOR MODELING:")
consolidated_columns = [col for col in df_clientes_consolidated.columns if col.endswith('_consolidated')]
for col in consolidated_columns:
    unique_count = df_clientes_consolidated[col].nunique()
    print(f"   {col}: {unique_count} categories")

print(f"\n💾 DATASET READY:")
print(f"   df_clientes_consolidated: {df_clientes_consolidated.shape}")
print(f"   Ultra-simple categorical features: {len(consolidated_columns)}")

print(f"\n🎉 ULTRA-CONSOLIDATION COMPLETE!")
print("📝 Next steps:")
print("   1. Continue with your notebook workflow")
print("   2. Use the '_consolidated' columns for feature engineering")
print("   3. Apply frequency encoding to these ultra-simple categories")
print("   4. Train your model with production-safe features")
