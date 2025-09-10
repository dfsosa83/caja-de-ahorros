# Feature Preparation Plan for ML Model

## Dataset Overview
- **Total Records**: 15,000
- **Features to Process**: 19 (excluding ID columns and target)
- **Target Variable**: `ingresos_reportados`

## Feature Categories & Strategies

### 1. **Numerical Features** (Ready for ML)
| Feature | Type | Missing | Strategy |
|---------|------|---------|----------|
| `letras_mensuales` | int64 | 0 | ✅ **Keep as-is** - Already numerical |
| `saldo` | float64 | 0 | ✅ **Keep as-is** - Already numerical |
| `missing_fechaingresoempleo` | int64 | 0 | ✅ **Keep as-is** - Binary indicator |
| `missing_nombreempleadorcliente` | int64 | 0 | ✅ **Keep as-is** - Binary indicator |
| `missing_cargoempleocliente` | int64 | 0 | ✅ **Keep as-is** - Binary indicator |
| `is_retired` | int64 | 0 | ✅ **Keep as-is** - Binary indicator |
| `payment_to_income_ratio` | float64 | 0 | ⚠️ **Review** - Potential data leakage |

### 2. **Numerical Features with Missing Values**
| Feature | Type | Missing | Strategy |
|---------|------|---------|----------|
| `monto_letra` | float64 | 2,536 (16.9%) | 🔧 **Impute** with median + create missing indicator |

### 3. **Date Features** (Need Conversion)
| Feature | Type | Missing | Strategy |
|---------|------|---------|----------|
| `fechaingresoempleo` | object | 769 (5.1%) | 🔧 **Convert** to days since reference + impute |
| `fecha_inicio` | object | 0 | 🔧 **Convert** to days since reference |
| `fecha_vencimiento` | object | 2,530 (16.9%) | 🔧 **Convert** to days since reference + impute |

### 4. **Categorical Features** (Need Encoding)

#### **Low Cardinality** (One-Hot Encoding)
| Feature | Type | Missing | Unique Values | Strategy |
|---------|------|---------|---------------|----------|
| `sexo_consolidated` | object | 0 | ~2 | 🔧 **One-Hot** encode (drop first) |
| `estado_civil_consolidated` | object | 0 | ~4 | 🔧 **One-Hot** encode (drop first) |
| `pais_consolidated` | object | 0 | ~10 | 🔧 **One-Hot** encode (drop first) |
| `age_group` | object | 0 | ~6 | 🔧 **One-Hot** encode (drop first) |

#### **High Cardinality** (Alternative Encoding)
| Feature | Type | Missing | Strategy |
|---------|------|---------|----------|
| `ocupacion_consolidated` | object | 0 | 🔧 **Frequency** encoding or **Target** encoding |
| `ciudad_consolidated` | object | 0 | 🔧 **Frequency** encoding or **Target** encoding |
| `nombreempleadorcliente_consolidated` | object | 0 | 🔧 **Frequency** encoding or **Target** encoding |
| `cargoempleocliente_consolidated` | object | 0 | 🔧 **Frequency** encoding or **Target** encoding |

## Detailed Processing Steps

### **Step 1: Handle Missing Values**
```python
# Numerical missing values
df['monto_letra_missing'] = df['monto_letra'].isnull().astype(int)
df['monto_letra'] = df['monto_letra'].fillna(df['monto_letra'].median())

# Date missing values (after conversion)
df['fecha_vencimiento_missing'] = df['fecha_vencimiento'].isnull().astype(int)
# Handle date imputation after conversion
```

### **Step 2: Convert Date Features**
```python
# Convert to datetime then to numerical
reference_date = pd.Timestamp('2020-01-01')  # Choose appropriate reference

for date_col in ['fechaingresoempleo', 'fecha_inicio', 'fecha_vencimiento']:
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df[f'{date_col}_days'] = (df[date_col] - reference_date).dt.days
    df.drop(columns=[date_col], inplace=True)
```

### **Step 3: Encode Categorical Features**

#### **One-Hot Encoding (Low Cardinality)**
```python
low_cardinality = ['sexo_consolidated', 'estado_civil_consolidated', 
                   'pais_consolidated', 'age_group']

df_encoded = pd.get_dummies(df, columns=low_cardinality, drop_first=True)
```

#### **Frequency/Target Encoding (High Cardinality)**
```python
high_cardinality = ['ocupacion_consolidated', 'ciudad_consolidated',
                    'nombreempleadorcliente_consolidated', 'cargoempleocliente_consolidated']

# Option 1: Frequency Encoding
for col in high_cardinality:
    freq_map = df[col].value_counts().to_dict()
    df[f'{col}_freq'] = df[col].map(freq_map)

# Option 2: Target Encoding (use with cross-validation)
# Implement target encoding with proper validation
```

### **Step 4: Feature Scaling**
```python
# Standardize numerical features
from sklearn.preprocessing import StandardScaler

numerical_features = ['letras_mensuales', 'saldo', 'monto_letra', 
                     'fechaingresoempleo_days', 'fecha_inicio_days', 'fecha_vencimiento_days']

scaler = StandardScaler()
df[numerical_features] = scaler.fit_transform(df[numerical_features])
```

## Special Considerations

### **Data Leakage Review**
- ⚠️ **`payment_to_income_ratio`**: Contains target information - **EXCLUDE** from model
- ✅ All other features appear safe for prediction

### **Feature Engineering Opportunities**
1. **Loan Duration**: `fecha_vencimiento_days - fecha_inicio_days`
2. **Employment Tenure**: `current_date - fechaingresoempleo_days`
3. **Payment Burden**: `monto_letra / saldo` (if meaningful)

### **Validation Strategy**
- Use **time-based split** if temporal patterns exist
- Apply **cross-validation** for target encoding
- **Fit transformations only on training data**

## Final Feature Set (Estimated)
- **Numerical**: ~10 features
- **Binary Indicators**: ~8 features  
- **One-Hot Encoded**: ~15 features
- **Frequency/Target Encoded**: ~4 features
- **Total**: ~37 features (interpretable and ML-ready)

## Next Steps
1. Implement missing value handling
2. Convert date features to numerical
3. Apply appropriate encoding strategies
4. Create feature engineering pipeline
5. Validate no data leakage
6. Prepare final dataset for modeling
