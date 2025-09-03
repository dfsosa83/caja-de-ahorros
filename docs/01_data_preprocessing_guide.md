# Data Preprocessing Guide

## Overview

This document explains the complete data preprocessing workflow for the Income Estimator ML project. The workflow transforms raw customer data into ML-ready features while handling missing values, encoding categorical variables, and creating new features.

## Dataset Structure

### Original Dataset
- **Size**: 15,000 records × 32 features
- **Data Types**: Mixed (numerical, categorical, dates, text)
- **Missing Values**: Present in several key features
- **Target**: Income estimation (to be defined)

### Key Features Categories
1. **Numerical**: `edad`, `letras_mensuales`, `monto_letra`, `saldo`, `ingresos_reportados`
2. **Categorical**: `segmento`, `sexo`, `ocupacion`, `estado_civil`, `ciudad`, `pais`
3. **Dates**: `fechaingresoempleo`, `fecha_inicio`, `fecha_vencimiento`
4. **Identifiers**: `cliente`, `identificador_unico`
5. **Consolidated Features**: Features ending with `_consolidated`
6. **Missing Indicators**: Features starting with `missing_`

## Preprocessing Workflow

### Step 1: Feature Type Analysis

```python
# Analyze and categorize all features
feature_types = analyze_feature_types(df)
```

**Purpose**: Automatically categorize features into:
- Numerical (continuous/discrete)
- Categorical (nominal/ordinal)
- Binary features
- Date features
- High cardinality features
- ID features (to be dropped)

### Step 2: Missing Value Handling

#### Strategy by Feature Type

| Feature | Strategy | Reason |
|---------|----------|---------|
| `fechaingresoempleo` | Forward fill + missing flag | Temporal data, missing pattern may be informative |
| `monto_letra` | Median imputation + missing flag | Numerical, median robust to outliers |
| `fecha_vencimiento` | Forward fill + business logic | Can derive from `fecha_inicio` + loan duration |

#### Implementation

```python
# Create missing indicators
df['fechaingresoempleo_missing'] = df['fechaingresoempleo'].isnull().astype(int)
df['monto_letra_missing'] = df['monto_letra'].isnull().astype(int)
df['fecha_vencimiento_missing'] = df['fecha_vencimiento'].isnull().astype(int)

# Apply imputation strategies
df['fechaingresoempleo'] = df['fechaingresoempleo'].fillna(method='ffill')
df['monto_letra'] = df['monto_letra'].fillna(df['monto_letra'].median())
df['fecha_vencimiento'] = df['fecha_vencimiento'].fillna(method='ffill')
```

### Step 3: Feature Engineering

#### Ratio Features
- `debt_to_income_ratio = monto_letra / ingresos_reportados`
- `balance_to_income_ratio = saldo / ingresos_reportados`
- `payment_to_income_ratio` (already exists)

#### Date-based Features
- `employment_tenure = today - fechaingresoempleo`
- `loan_duration = fecha_vencimiento - fecha_inicio`
- `days_to_maturity = fecha_vencimiento - today`

#### Categorical Combinations
- `age_marital_status = edad + '_' + estado_civil_consolidated`
- `occupation_gender = ocupacion_consolidated + '_' + sexo_consolidated`

### Step 4: Feature Encoding

#### Encoding Strategy by Cardinality

| Cardinality | Strategy | Example |
|-------------|----------|---------|
| Binary (2 values) | Label Encoding | `sexo`: Male=1, Female=0 |
| Low (≤10 values) | One-Hot Encoding | `segmento`: 3 categories → 2 dummy columns |
| High (>10 values) | Target/Frequency Encoding | `ciudad`: 50+ cities → frequency encoding |

#### Implementation

```python
# Preprocessing pipeline
numerical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
    ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', numerical_transformer, numerical_features),
    ('cat', categorical_transformer, categorical_features)
])
```

### Step 5: Data Cleaning

#### Features to Drop
- **ID Features**: `cliente`, `identificador_unico`
- **Redundant Features**: Original features replaced by consolidated versions
- **High Missing**: Features with >50% missing values (case-by-case evaluation)

#### Consolidated vs Original Features
- Keep consolidated features when they have fewer missing values
- Drop original features that are replaced by better consolidated versions

## Final Datasets

### df_clean
- **Type**: Pandas DataFrame
- **Content**: Original data after dropping unnecessary columns
- **Use**: Exploratory Data Analysis, reference

### df_final
- **Type**: Pandas DataFrame with processed features
- **Content**: ML-ready numerical features with proper column names
- **Features**: ~40-60 features (depends on one-hot encoding)
- **Use**: Machine Learning training and prediction

### Feature Transformation Summary
- **Original**: 32 features → **Final**: ~50 features
- **Numerical**: Standardized (mean=0, std=1)
- **Categorical**: One-hot encoded or target encoded
- **Missing**: Imputed + missing indicator flags created
- **New**: Engineered features added

## Production Pipeline Integration

### ⚠️ Critical: Pipeline Consistency

**This preprocessing workflow MUST be part of your production prediction pipeline.**

#### Why?
1. **Raw Data Input**: Production will receive raw data similar to training data
2. **Same Transformations**: All preprocessing steps must be identical
3. **Feature Consistency**: Model expects exact same features in same order
4. **Missing Value Handling**: New data will have missing values too

#### Implementation Strategy

```python
# 1. Save the preprocessing pipeline
import joblib
joblib.save(preprocessor, 'models/preprocessing_pipeline.pkl')

# 2. Create preprocessing function
def preprocess_raw_data(raw_df):
    """
    Apply same preprocessing steps to new raw data
    """
    # Step 1: Handle missing values
    df_processed = handle_missing_values(raw_df)
    
    # Step 2: Feature engineering
    df_engineered = create_new_features(df_processed)
    
    # Step 3: Clean and encode
    df_clean = df_engineered.drop(columns=features_to_drop)
    df_final = pd.DataFrame(
        preprocessor.transform(df_clean), 
        columns=feature_names
    )
    
    return df_final

# 3. Use in production
def predict_new_data(raw_data):
    # Preprocess
    processed_data = preprocess_raw_data(raw_data)
    
    # Predict
    predictions = model.predict(processed_data)
    
    return predictions
```

#### Pipeline Components to Save
1. **Preprocessing Pipeline**: `preprocessor` (ColumnTransformer)
2. **Feature Names**: `feature_names` (list)
3. **Features to Drop**: `features_to_drop` (list)
4. **Missing Value Strategies**: Imputation values (medians, modes)
5. **Feature Engineering Logic**: Custom transformation functions

## Quick Start Instructions

### For Training
```python
# 1. Load and analyze data
feature_types = analyze_feature_types(df)
preprocessing_strategies = define_preprocessing_strategies(feature_types, df)

# 2. Handle missing values
df_processed = handle_missing_values(df)

# 3. Create preprocessing pipeline
preprocessor = create_preprocessing_pipeline()

# 4. Transform data
df_clean = df_processed.drop(columns=features_to_drop)
X_processed = preprocessor.fit_transform(df_clean)
df_final = pd.DataFrame(X_processed, columns=feature_names)

# 5. Ready for ML!
X = df_final
y = df['target_variable']  # Define your target
```

### For Production
```python
# 1. Load saved pipeline
preprocessor = joblib.load('models/preprocessing_pipeline.pkl')

# 2. Preprocess new data
df_final = preprocess_raw_data(new_raw_data)

# 3. Make predictions
predictions = model.predict(df_final)
```

## Best Practices

### ✅ Do
- Always create missing indicator flags
- Use robust scaling for numerical features
- Handle unknown categories in encoding
- Save all preprocessing components
- Test pipeline with new data samples
- Document all transformation decisions

### ❌ Don't
- Skip missing value handling
- Use different preprocessing for train/test
- Hardcode category mappings
- Forget to handle new categories in production
- Mix preprocessing steps with model training
- Ignore data leakage in feature engineering

## Troubleshooting

### Common Issues
1. **Feature Mismatch**: Different number of features in train vs production
   - **Solution**: Ensure identical preprocessing pipeline
   
2. **Unknown Categories**: New categories not seen in training
   - **Solution**: Use `handle_unknown='ignore'` in encoders
   
3. **Missing Value Errors**: New missing patterns in production
   - **Solution**: Robust imputation strategies + missing flags
   
4. **Scale Differences**: Features not properly scaled
   - **Solution**: Use fitted scalers from training data

### Validation Checklist
- [ ] Same number of features in train and test
- [ ] No missing values in final dataset
- [ ] All categorical variables properly encoded
- [ ] Numerical features properly scaled
- [ ] Pipeline can handle new unseen data
- [ ] All components saved for production use

---

**Next Steps**: Use `df_final` for model training and evaluation. Remember to save all preprocessing components for production deployment!
