# Data Quality Requirements for Categorical Features

## 🎯 Purpose

This document defines the **mandatory data quality standards** for categorical features in the income prediction system. Following these requirements ensures consistent model performance and prevents production issues.

## 📋 Critical Data Entry Standards

### 🏢 Occupation (`ocupacion`)

#### ✅ Approved Categories (Top 6)
```
1. "JUBILADO"                    # Retired persons
2. "DOCENTE"                     # Teachers/Educators  
3. "POLICIA"                     # Police officers
4. "OFICINISTAS"                 # Office workers
5. "SUPERVISOR"                  # Supervisors
6. "ASISTENTE"                   # Assistants
```

#### 📝 Entry Rules
- **Format**: ALL UPPERCASE
- **Spaces**: No leading/trailing spaces
- **Consistency**: Use exact spelling above
- **Fallback**: Any other occupation → "Others" in model

#### 🔄 What to Enter for Non-Approved Occupations
**IMPORTANT**: If the occupation is NOT in the approved list above, enter:
```
"OTROS"
```

#### 📝 Examples of Non-Approved → "OTROS"
```
"INGENIERO" → "OTROS"
"MEDICO" → "OTROS"
"ABOGADO" → "OTROS"
"VENDEDOR" → "OTROS"
"CONTADOR" → "OTROS"
"MECANICO" → "OTROS"
```

#### ❌ Common Mistakes to Avoid
```
❌ "jubilado" → ✅ "JUBILADO"
❌ "PROFESOR" → ✅ "DOCENTE"
❌ "POLICÍA" → ✅ "POLICIA"
❌ "OFICINISTA" → ✅ "OFICINISTAS"
❌ "JUBILADO   " → ✅ "JUBILADO"
❌ "INGENIERO" → ✅ "OTROS"
❌ "Others" → ✅ "OTROS"
❌ "other" → ✅ "OTROS"
```

### 🏛️ Employer (`nombreempleadorcliente`)

#### ✅ Approved Categories (Top 6)
```
1. "NO APLICA"                           # Not applicable/unemployed
2. "MINISTERIO DE EDUCACION"             # Ministry of Education
3. "MINISTERIO DE SEGURIDAD PUBLICA"     # Ministry of Public Security
4. "CAJA DE SEGURO SOCIAL"               # Social Security Fund
5. "CAJA DE AHORROS"                     # Savings Bank
6. "MINISTERIO DE SALUD"                 # Ministry of Health
```

#### 📝 Entry Rules
- **Format**: ALL UPPERCASE
- **Names**: Use complete official names
- **Abbreviations**: Avoid unless standardized
- **Consistency**: Exact spelling required

#### 🔄 What to Enter for Non-Approved Employers
**IMPORTANT**: If the employer is NOT in the approved list above, enter:
```
"OTROS"
```

#### 📝 Examples of Non-Approved → "OTROS"
```
"BANISTMO" → "OTROS"
"CABLE AND WIRELESS" → "OTROS"
"EMPRESA PRIVADA PEQUEÑA" → "OTROS"
"SUPERMERCADOS REY" → "OTROS"
"CONSTRUCTORA ABC" → "OTROS"
```

#### ❌ Common Mistakes to Avoid
```
❌ "MIN EDUCACION" → ✅ "MINISTERIO DE EDUCACION"
❌ "CSS" → ✅ "CAJA DE SEGURO SOCIAL"
❌ "MINISTERIO EDUCACION" → ✅ "MINISTERIO DE EDUCACION"
❌ "CAJA SEGURO SOCIAL" → ✅ "CAJA DE SEGURO SOCIAL"
❌ "BANISTMO" → ✅ "OTROS"
❌ "Others" → ✅ "OTROS"
```

### 💼 Job Position (`cargoempleocliente`)

#### ✅ Approved Categories (Top 6)
```
1. "JUBILADO"                    # Retired
2. "POLICIA"                     # Police officer
3. "DOCENTE"                     # Teacher
4. "SUPERVISOR"                  # Supervisor
5. "SECRETARIA"                  # Secretary
6. "OFICINISTA"                  # Office clerk
```

#### 📝 Entry Rules
- **Format**: ALL UPPERCASE
- **Singular**: Use singular form when possible
- **Standard**: Use most common term
- **Gender**: Use neutral or most common form

#### 🔄 What to Enter for Non-Approved Job Positions
**IMPORTANT**: If the job position is NOT in the approved list above, enter:
```
"OTROS"
```

#### 📝 Examples of Non-Approved → "OTROS"
```
"INGENIERO" → "OTROS"
"CONTADOR" → "OTROS"
"VENDEDOR" → "OTROS"
"MECANICO" → "OTROS"
"CAJERO" → "OTROS"
"GUARDIA" → "OTROS"
```

#### ❌ Common Mistakes to Avoid
```
❌ "SECRETARIO" → ✅ "SECRETARIA"
❌ "OFICINISTAS" → ✅ "OFICINISTA"
❌ "PROFESOR" → ✅ "DOCENTE"
❌ "MAESTRO" → ✅ "DOCENTE"
❌ "INGENIERO" → ✅ "OTROS"
❌ "Others" → ✅ "OTROS"
```

### 🏙️ City (`ciudad`)

#### ✅ Approved Categories (Top 5)
```
1. "PANAMA"                      # Panama City
2. "ARRAIJAN"                    # Arraiján
3. "SAN MIGUELITO"               # San Miguelito
4. "LA CHORRERA"                 # La Chorrera
5. "DAVID"                       # David
```

#### 📝 Entry Rules
- **Format**: ALL UPPERCASE
- **Names**: Use official city names
- **Articles**: Include articles (LA, SAN, etc.)
- **Accents**: Remove accents for consistency

#### 🔄 What to Enter for Non-Approved Cities
**IMPORTANT**: If the city is NOT in the approved list above, enter:
```
"OTROS"
```

#### 📝 Examples of Non-Approved → "OTROS"
```
"PENONOME" → "OTROS"
"BUGABA" → "OTROS"
"CHANGUINOLA" → "OTROS"
"AGUADULCE" → "OTROS"
"BOQUETE" → "OTROS"
"CHITRE" → "OTROS"
```

#### ❌ Common Mistakes to Avoid
```
❌ "CIUDAD DE PANAMA" → ✅ "PANAMA"
❌ "CHORRERA" → ✅ "LA CHORRERA"
❌ "SAN MIGUEL" → ✅ "SAN MIGUELITO"
❌ "ARRAIJÁN" → ✅ "ARRAIJAN"
❌ "PENONOME" → ✅ "OTROS"
❌ "Others" → ✅ "OTROS"
```

### 👤 Gender (`sexo`)

#### ✅ Approved Categories (All 2)
```
1. "Femenino"                    # Female
2. "Masculino"                   # Male
```

#### 📝 Entry Rules
- **Format**: Title Case (First letter uppercase)
- **Complete**: Use full words, not abbreviations
- **Standard**: Use exact spelling above

#### ❌ Common Mistakes to Avoid
```
❌ "F" → ✅ "Femenino"
❌ "M" → ✅ "Masculino"
❌ "FEMENINO" → ✅ "Femenino"
❌ "Mujer" → ✅ "Femenino"
```

### 💒 Marital Status (`estado_civil`)

#### ✅ Approved Categories (Top 2)
```
1. "Soltero"                     # Single
2. "Casado"                      # Married
```

#### 📝 Entry Rules
- **Format**: Title Case
- **Gender**: Use masculine form as standard
- **Simple**: Only main categories, others → "Others"

#### 🔄 What to Enter for Non-Approved Marital Status
**IMPORTANT**: If the marital status is NOT in the approved list above, enter:
```
"Otros"
```

#### 📝 Examples of Non-Approved → "Otros"
```
"Divorciado" → "Otros"
"Viudo" → "Otros"
"Separado" → "Otros"
"Union Libre" → "Otros"
```

#### ❌ Common Mistakes to Avoid
```
❌ "Soltera" → ✅ "Soltero"
❌ "Casada" → ✅ "Casado"
❌ "SOLTERO" → ✅ "Soltero"
❌ "Divorciado" → ✅ "Otros"
❌ "OTROS" → ✅ "Otros"
❌ "Others" → ✅ "Otros"
```

### 🌍 Country (`pais`)

#### ✅ Approved Categories (Top 1)
```
1. "PANAMA"                      # Panama
```

#### 📝 Entry Rules
- **Format**: ALL UPPERCASE
- **Standard**: Use country name in Spanish
- **Simple**: Only Panama, others → "Others"

#### 🔄 What to Enter for Non-Approved Countries
**IMPORTANT**: If the country is NOT "PANAMA", enter:
```
"OTROS"
```

#### 📝 Examples of Non-Approved → "OTROS"
```
"COLOMBIA" → "OTROS"
"COSTA RICA" → "OTROS"
"ESTADOS UNIDOS" → "OTROS"
"VENEZUELA" → "OTROS"
"NICARAGUA" → "OTROS"
```

#### ❌ Common Mistakes to Avoid
```
❌ "PANAMÁ" → ✅ "PANAMA"
❌ "Panama" → ✅ "PANAMA"
❌ "REP. PANAMA" → ✅ "PANAMA"
❌ "COLOMBIA" → ✅ "OTROS"
❌ "Others" → ✅ "OTROS"
```

## 🎯 CRITICAL NAMING CONVENTION SUMMARY

### 📝 **What to Enter for Non-Approved Categories**

**UNIVERSAL RULE**: When a category is NOT in the approved list, use these exact terms:

| Feature | Non-Approved Entry | Format |
|---------|-------------------|---------|
| `ocupacion` | **"OTROS"** | ALL UPPERCASE |
| `nombreempleadorcliente` | **"OTROS"** | ALL UPPERCASE |
| `cargoempleocliente` | **"OTROS"** | ALL UPPERCASE |
| `ciudad` | **"OTROS"** | ALL UPPERCASE |
| `estado_civil` | **"Otros"** | Title Case |
| `pais` | **"OTROS"** | ALL UPPERCASE |
| `sexo` | *(No others - only 2 approved)* | Title Case |

### ⚠️ **CRITICAL**: Never Use These Variations
```
❌ "Others" (English)
❌ "Other" (Singular English)
❌ "OTHERS" (English uppercase)
❌ "otros" (lowercase)
❌ "Otro" (Singular Spanish)
❌ "N/A" or "NA"
❌ "No Aplica" (except for employer field)
❌ Leave blank or empty
```

### ✅ **Always Use These Exact Terms**
```
✅ "OTROS" (for uppercase fields)
✅ "Otros" (for title case fields)
```

## 🔧 Implementation Guidelines

### For Data Entry Systems

#### 1. Dropdown Menus
```python
# Example dropdown configuration
OCUPACION_OPTIONS = [
    "JUBILADO",
    "DOCENTE", 
    "POLICIA",
    "OFICINISTAS",
    "SUPERVISOR",
    "ASISTENTE",
    "OTROS"  # For any other occupation
]
```

#### 2. Validation Rules
```python
# Example validation function
def validate_ocupacion(value):
    approved = ["JUBILADO", "DOCENTE", "POLICIA", "OFICINISTAS", "SUPERVISOR", "ASISTENTE"]
    cleaned = str(value).strip().upper()
    
    if cleaned in approved:
        return cleaned
    else:
        return "OTROS"  # Auto-assign to others category
```

#### 3. Data Cleaning Pipeline
```python
# Example cleaning function
def clean_categorical_data(df):
    # Clean ocupacion
    df['ocupacion'] = df['ocupacion'].str.strip().str.upper()
    
    # Clean employer names
    df['nombreempleadorcliente'] = df['nombreempleadorcliente'].str.strip().str.upper()
    
    # Clean cities
    df['ciudad'] = df['ciudad'].str.strip().str.upper()
    
    # Standardize gender
    df['sexo'] = df['sexo'].str.strip().str.title()
    
    return df
```

### For Database Design

#### 1. Reference Tables
Create lookup tables for each categorical feature:

```sql
-- Example: Occupation reference table
CREATE TABLE ref_ocupacion (
    id INT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE,
    descripcion VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE
);

INSERT INTO ref_ocupacion VALUES 
(1, 'JUBILADO', 'Persona jubilada o retirada', TRUE),
(2, 'DOCENTE', 'Profesor o educador', TRUE),
(3, 'POLICIA', 'Oficial de policía', TRUE);
```

#### 2. Foreign Key Constraints
```sql
-- Link main table to reference table
ALTER TABLE clientes 
ADD CONSTRAINT fk_ocupacion 
FOREIGN KEY (ocupacion_id) REFERENCES ref_ocupacion(id);
```

### For API Integration

#### 1. Input Validation
```python
# Example API validation
from pydantic import BaseModel, validator

class ClienteInput(BaseModel):
    ocupacion: str
    ciudad: str
    sexo: str
    
    @validator('ocupacion')
    def validate_ocupacion(cls, v):
        approved = ["JUBILADO", "DOCENTE", "POLICIA", "OFICINISTAS", "SUPERVISOR", "ASISTENTE"]
        cleaned = v.strip().upper()
        return cleaned if cleaned in approved else "OTROS"
```

## 📊 Quality Monitoring

### Daily Checks
- [ ] **New category detection**: Flag any values not in approved lists
- [ ] **Format validation**: Check for case/spacing issues
- [ ] **Completeness**: Monitor missing value rates

### Weekly Reports
- [ ] **Category distribution**: Track changes in category frequencies
- [ ] **Data quality score**: Calculate compliance with standards
- [ ] **Exception analysis**: Review flagged entries

### Monthly Reviews
- [ ] **Standard updates**: Evaluate need for new approved categories
- [ ] **Training needs**: Identify data entry training requirements
- [ ] **System improvements**: Assess validation rule effectiveness

## 🚨 Escalation Procedures

### When to Add New Categories

**Criteria for adding new approved categories:**
1. **Frequency**: New category appears in >2% of monthly data
2. **Business relevance**: Category has distinct business meaning
3. **Stability**: Category appears consistently over 3+ months
4. **Stakeholder approval**: Business team confirms relevance

**Process:**
1. **Document request** with frequency analysis
2. **Business review** with stakeholders
3. **Technical impact** assessment
4. **Model retraining** evaluation
5. **Approval and implementation**

### Emergency Procedures

**For critical data quality issues:**
1. **Immediate**: Stop data ingestion if >20% invalid
2. **Alert**: Notify data science and business teams
3. **Investigate**: Identify root cause
4. **Fix**: Implement temporary solution
5. **Review**: Permanent solution and prevention

---

## 📞 Support Contacts

- **Data Quality Issues**: [Data Team Contact]
- **Business Questions**: [Business Team Contact]
- **Technical Problems**: [IT Support Contact]
- **Emergency Escalation**: [Manager Contact]

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Next Review**: Monthly
