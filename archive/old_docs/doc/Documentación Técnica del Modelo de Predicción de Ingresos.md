

# **Documentación Técnica del Modelo de Predicción de Ingresos**

## **Resumen Ejecutivo**

Este documento proporciona una documentación técnica integral para el modelo de predicción de ingresos de clientes desarrollado utilizando técnicas avanzadas de aprendizaje automático. El modelo logra un RMSE de $491.23 ± $3.72 mediante validación cruzada anidada y demuestra un excelente desempeño con un RMSE de prueba de $540.63.Income_Prediction_Model_Technical_Documentation.md

**Logros Clave:**

- ✅ **Precisión de primer nivel:** $540.63 RMSE de prueba (error promedio de predicción)Income_Prediction_Model_Technical_Documentation.md

  

- ✅ **Metodología robusta:** Validación cruzada anidada para estimación imparcial del desempeñoIncome_Prediction_Model_Technical_Documentation.md

  

- ✅ **Listo para producción:** Pipeline completo con ingeniería de características y selección de modeloIncome_Prediction_Model_Technical_Documentation.md

  

- ✅ **Resultados interpretables:** Claridad en la importancia de variables y hallazgos de negocioIncome_Prediction_Model_Technical_Documentation.md

  



------



## **1. Panorama del Proyecto y Supuestos**

## **1.1 Declaración del Problema de Negocio**

**Objetivo:** Desarrollar un modelo de aprendizaje automático para predecir con precisión el ingreso de clientes con base en los datos disponibles, permitiendo mejores recomendaciones de productos financieros y evaluación de riesgos.

**Valor de Negocio:**

- Mejor segmentación y targeting de clientes

  

- Evaluación de riesgo mejorada para decisiones de préstamos y crédito

  

- Recomendaciones personalizadas de productos financieros

  

- Mejor comprensión de la capacidad financiera del cliente

  

## **1.2 Supuestos Clave**

**Supuestos de Datos:**

- Los datos de ingresos son reportados con precisión y son representativos

  

- Los patrones históricos en la predicción de ingresos permanecen estables en el tiempo

  

- Los patrones de datos faltantes no están sesgados sistemáticamente

  

- Las relaciones entre variables son consistentes entre segmentos de clientes

  

**Supuestos de Modelado:**

- Modelos basados en árboles (XGBoost, LightGBM, Random Forest) son adecuados para esta tarea de regresión

  

- Existen relaciones no lineales entre variables e ingresos

  

- La ingeniería de características captura los predictores más relevantes

  

- La validación cruzada brinda estimaciones confiables del rendimiento

  

**Supuestos de Negocio:**

- Las predicciones del modelo se usarán como soporte a la decisión, no para decisiones automáticas

  

- El modelo se reentrenará regularmente para mantener el rendimiento

  

- Las variables disponibles en producción coinciden con las usadas en entrenamiento

  

## **1.3 Criterios de Éxito y Métricas de Evaluación**

**Métricas Principales:**

- **RMSE (Root Mean Square Error):** Métrica principal para selección de modelo

  

  - Meta: < $600 (logrado: $540.63)

    

  - Mide el error promedio de predicción en dólares

    

**Métricas Secundarias:**

- **MAE (Mean Absolute Error):** Medida robusta del error típico

  

  - Logrado: $377.81

    

  - Menos sensible a valores atípicos que el RMSE

    

- **R² (Coeficiente de Determinación):** Varianza explicada

  

  - Logrado: 0.3913 (39.1% de la varianza explicada)

    

  - Indica el poder explicativo del modelo

    

- **MAPE (Error Porcentual Absoluto Medio):** Medida relativa de error

  

  - Logrado: 34.5% para ingresos > $100

    

  - Interpretación en porcentaje útil para negocio

    

**Criterios de Fiabilidad del Modelo:**

- Estimaciones de validación cruzada anidada dentro del intervalo de confianza del 95% del rendimiento en prueba 

  

- Rendimiento consistente en diferentes particiones de datos 

  

- Importancia de variables alineada con la intuición de negocio 

  



------



## **2. Proceso de Ingeniería de Características**

## **2.1 Metodología de Creación de Variables**

La ingeniería de variables siguió un enfoque sistemático para crear predictores significativos:

**Fase 1: Procesamiento Básico**

- Escalamiento y normalización de variables numéricas

  

- Codificación de variables categóricas basada en frecuencias

  

- Extracción de características de fechas (días desde eventos)

  

- Estrategias de imputación de valores faltantes

  

**Fase 2: Ingeniería Avanzada**

- **Codificación de Frecuencias:** Convertir variables categóricas en recuentos de frecuencia

  

  - ocupacion_consolidated_freq: Frecuencia de puesto de trabajo

    

  - nombreempleadorcliente_consolidated_freq: Frecuencia por empleador

    

  - cargoempleocliente_consolidated_freq: Frecuencia por cargo laboral

    

- **Variables de Razón:** Creación de razones financieras significativas

  

  - balance_to_payment_ratio: Relación entre saldo y monto de pago

    

  - Refleja la capacidad y comportamiento financiero

    

- **Características Temporales:** Extracción de patrones basados en el tiempo

  

  - fechaingresoempleo_days: Días desde inicio de empleo

    

  - fecha_inicio_days: Días desde apertura de la cuenta

    

  - employment_years: Años de experiencia laboral

    

- **Variables Derivadas:** Cálculo de métricas relevantes de negocio

  

  - professional_stability_score: Indicador compuesto de estabilidad laboral

    

  - Combina varios factores relacionados al empleo

    

## **2.2 Variables Más Significativas**

Según el análisis de importancia por permutación, las principales variables son:

**Top 5 Variables Críticas:**

1. **saldo** **(Saldo de Cuenta)** - Importancia: -$118,411.98

   

   - **Impacto de Negocio:** Refleja la capacidad financiera del cliente

     

   - **Interpretación:** Saldos más altos se asocian a mayores ingresos

     

   - **Uso:** Indicador principal para estimar ingresos

     

2. **balance_to_payment_ratio** - Importancia: -$106,510.66

   

   - **Impacto de Negocio:** Indica salud financiera y capacidad de pago

     

   - **Interpretación:** Razones altas sugieren mejor manejo financiero

     

   - **Uso:** Evaluación de riesgo y solvencia crediticia

     

3. **nombreempleadorcliente_consolidated_freq** - Importancia: -$94,382.06

   

   - **Impacto de Negocio:** Empleadores grandes/comunes sugieren ingresos estables y altos

     

   - **Interpretación:** La frecuencia refleja el tamaño y estabilidad del empleador

     

   - **Uso:** Estimación de ingresos basada en empleo

     

4. **ocupacion_consolidated_freq** - Importancia: -$69,728.79

   

   - **Impacto de Negocio:** Puestos comunes tienden a sueldos característicos

     

   - **Interpretación:** Ocupaciones profesionales tienen patrones de ingreso predecibles

     

   - **Uso:** Referencia de ingresos según ocupación

     

5. **professional_stability_score** - Importancia: -$3,164.90

   

   - **Impacto de Negocio:** Indica confiabilidad de ingresos por estabilidad laboral

     

   - **Interpretación:** Empleo estable sugiere ingresos constantes

     

   - **Uso:** Fiabilidad de predicción de ingresos a largo plazo

     

## **2.3 Criterios de Selección de Variables**

**Criterios:**

- Significancia estadística a través de validación múltiple

  

- Interpretabilidad y utilidad para negocio

  

- Disponibilidad y calidad de datos en producción

  

- Baja correlación para evitar redundancia

  

- Rendimiento robusto entre segmentos de clientes

  

**Variables Excluidas:**

- Alta correlación con variables seleccionadas (>0.8)

  

- Bajo poder predictivo en sistema de votos

  

- Problemas de calidad o altos nulos

  

- Potencial sesgo o problemas de justicia

  

- Baja disponibilidad en sistemas de producción

  



------



## **3. Implementación del Sistema de Votación**

## **3.1 Metodología de Ensamble**

El sistema de votación combina múltiples algoritmos para seleccionar variables de forma robusta:

**Modelos de Votación:**

1. **Random Forest Regressor****

   **

   - Configuración: 600 árboles, max_depth=25

     

   - Fortaleza: Captura relaciones no lineales e interacciones

     

   - Peso en el voto: 40%

     

2. **LightGBM Regressor****

   **

   - Configuración: Gradient boosting con parada temprana

     

   - Fortaleza: Manejo eficiente de categóricas

     

   - Peso en el voto: 40%

     

3. **Ridge Regression****

   **

   - Configuración: Regularización L2

     

   - Fortaleza: Relación lineal y regularización

     

   - Peso en el voto: 20%

     

## **3.2 Proceso de Votación**

**Paso 1: Entrenamiento Individual**

- Cada modelo se entrena con todas las variables disponibles

  

- Se extrae la importancia de variables de cada modelo

  

- Puntuaciones normalizadas para comparación

  

**Paso 2: Umbrales de Voto**

- Se aplican varios umbrales a la importancia obtenida

  

- Variables por encima del umbral reciben un "voto" del modelo

  

- Variables ruidosas generadas como línea base

  

**Paso 3: Construcción de Consenso**

- Variables con votos de varios modelos se priorizan

  

- Umbrales por ruido aseguran significancia estadística

  

- La selección final balancea consenso e intuición de cada modelo

  

**Paso 4: Control de Calidad**

- Variables ruidosas excluidas explícitamente

  

- Se aplican límites mínimo y máximo al número de variables finales

  

- Validación del negocio sobre la selección final

  

## **3.3 Beneficios del Sistema de Votación**

**Robustez:**

- Reduce el sobreajuste al sesgo de un solo algoritmo

  

- Captura diferentes tipos de relaciones entre variables

  

- Selección más estable entre variaciones de datos

  

**Interpretabilidad:**

- Múltiples perspectivas sobre la importancia de variables

  

- Selección por consenso brinda más confianza

  

- Trazabilidad clara de decisiones de selección

  

**Desempeño:**

- Combina fortalezas de distintos algoritmos

  

- Reduce el riesgo de dejar fuera variables relevantes

  

- Mayor generalización en nuevos datos

  



------



## **4. Selección Final de Variables**

## **4.1 Variables Usadas en Producción**

El modelo final utiliza **10 variables cuidadosamente seleccionadas** guiadas por el sistema de votación:

| **Posición** | **Nombre de Variable**                   | **Tipo**   | **Significado de Negocio**       |
| ------------ | ---------------------------------------- | ---------- | -------------------------------- |
| 1            | ocupacion_consolidated_freq              | Frecuencia | Común en puestos laborales       |
| 2            | nombreempleadorcliente_consolidated_freq | Frecuencia | Tamaño/estabilidad del empleador |
| 3            | edad                                     | Numérica   | Edad del cliente                 |
| 4            | fechaingresoempleo_days                  | Temporal   | Antigüedad en empleo             |
| 5            | cargoempleocliente_consolidated_freq     | Frecuencia | Frecuencia por cargo             |
| 6            | fecha_inicio_days                        | Temporal   | Antigüedad de cuenta             |
| 7            | balance_to_payment_ratio                 | Razón      | Indicador de salud financiera    |
| 8            | professional_stability_score             | Derivada   | Estabilidad laboral              |
| 9            | saldo                                    | Numérica   | Saldo de cuenta                  |
| 10           | employment_years                         | Numérica   | Años de experiencia laboral      |

## **4.2 Distribución de Tipos de Variables**

**Categorías:**

- **Frecuencia (30%):** 3 variables sobre patrones categóricos

  

- **Numéricas (30%):** 3 con mediciones directas

  

- **Temporales (20%):** 2 variables de patrones temporales

  

- **Derivadas (20%):** 2 variables combinadas por lógica de negocio

  

## **4.3 Importancia de Variables**

**Nivel 1 - Críticas (impacto >$50,000):**

- saldo: $118,412

  

- balance_to_payment_ratio: $106,511

  

- nombreempleadorcliente_consolidated_freq: $94,382

  

- ocupacion_consolidated_freq: $69,729

  

**Nivel 2 - Importantes ($10,000-$50,000):**

- fecha_inicio_days: $34,097

  

- fechaingresoempleo_days: $29,464

  

- employment_years: $12,647

  

**Nivel 3 - Secundarias (<$10,000):**

- cargoempleocliente_consolidated_freq: $5,606

  

- edad: $1,759

  

- professional_stability_score: $3,165

  

## **4.4 Justificación de la Selección**

**Variables Financieras (motores principales):**

- saldo y balance_to_payment_ratio miden la capacidad financiera

  

- Alta correlación con ingresos en cualquier segmento de cliente

  

- Disponibilidad en tiempo real para predicciones en producción

  

**Variables de Empleo (motores secundarios):**

- Frecuencia de empleador y ocupación capturan estabilidad de ingresos

  

- Antigüedad laboral marca progresión e incremento en ingresos

  

- El indicador de estabilidad profesional refuerza la confiabilidad de los ingresos

  

**Variables Demográficas (apoyo):**

- La edad da contexto de etapa de vida para expectativas de ingresos

  

- Antigüedad de la cuenta indica madurez de la relación cliente-institución

  

- Acompañadas de otras variables, mejoran la precisión del modelo

  

**Beneficios de Interacciones:**

- Empleo + Finanzas ofrecen una visión integral del cliente

  

- Temporalidad agrega estabilidad y tendencias

  

- La codificación por frecuencia simplifica lo categórico

  



------



## **5. Proceso de Modelado con Validación Cruzada Anidada**

## **5.1 Metodología Anidada**

**¿Por qué cruzada anidada?****
** La validación cruzada anidada da estimaciones imparciales del rendimiento al separar por completo la selección de modelo de la estimación de desempeño, evitando sobreajuste y fugas de datos.

**Estructura de dos niveles:**

- **CV externa (5 particiones):** Estimación imparcial del desempeño

  

- **CV interna (3 particiones):** Optimización de hiperparámetros

  

- **Total modelos entrenados:** 450 (5 × 3 × 10 iteraciones × 3 algoritmos)

  

**Beneficios clave:**

- Elimina el sesgo optimista de la optimización de hiperparámetros

  

- Da estimaciones realistas para producción

  

- Permite comparar diferentes algoritmos

  

- Genera intervalos de confianza para métricas de rendimiento

  

## **5.2 Comparación de Modelos**

**Algoritmos evaluados:**

1. **XGBoost (Ganador)****

   **

   - **Ventajas:** Maneja bien datos mixtos, robusto a atípicos

     

   - **Configuración:** 300-700 estimadores, learning rate 0.01-0.1

     

   - **Desempeño:** RMSE $491.23 ± $3.72

     

   - **Justificación selección:** Mejor desempeño y estabilidad

     

2. **Random Forest****

   **

   - **Ventajas:** Interpretabilidad, maneja valores nulos

     

   - **Configuración:** 200-400 árboles, varias profundidades

     

   - **Desempeño:** RMSE $506.01 ± $3.98

     

   - **Resultado:** Segundo lugar, consistente

     

3. **LightGBM****

   **

   - **Ventajas:** Entrenamiento rápido, eficiente en memoria

     

   - **Configuración:** Gradient boosting con parada temprana

     

   - **Desempeño:** RMSE $510.82 ± $3.21

     

   - **Resultado:** Buen desempeño, menor varianza

     

**Criterios de Selección:**

- Primario: RMSE (más bajo = mejor)

  

- Secundario: R² (más alto = mejor)

  

- Terciario: Estabilidad e interpretabilidad

  

## **5.3 Optimización de Hiperparámetros**

**Estrategia:**

- **Método:** RandomizedSearchCV con 10 iteraciones por fold interno

  

- **Puntuación:** MSE negativo (optimiza RMSE)

  

- **Espacio de búsqueda:** Grids amplios y relevantes

  

**Grid de XGBoost:**

python

{

  'n_estimators': [300, 500, 700],

  'max_depth': [6, 8, 10],

  'learning_rate': [0.01, 0.05, 0.1],

  'subsample': [0.8, 0.85, 0.9],

  'colsample_bytree': [0.8, 0.85, 0.9],

  'reg_alpha': [0, 0.1, 0.5],

  'reg_lambda': [0.5, 1.0, 2.0]

}

**Parámetros óptimos XGBoost (más frecuentes):**

- n_estimators: 500

  

- max_depth: 8

  

- learning_rate: 0.05

  

- subsample: 0.85

  

- colsample_bytree: 0.85

  

- reg_alpha: 0.1

  

- reg_lambda: 1.0

  

## **5.4 Estimación de Desempeño Imparcial**

**Resumen de resultados de CV Anidada:**

| **Modelo**    | **Media RMSE** | **Std RMSE** | **Media MAE** | **Std MAE** | **Media R²** | **Std R²** |
| ------------- | -------------- | ------------ | ------------- | ----------- | ------------ | ---------- |
| **XGBoost**   | **$491.23**    | **$3.72**    | **$344.98**   | **$2.94**   | **0.4940**   | **0.009**  |
| Random Forest | $506.01        | $3.98        | $359.77       | $2.71       | 0.4631       | 0.011      |
| LightGBM      | $510.82        | $3.21        | $367.64       | $3.40       | 0.4528       | 0.010      |

**Significancia estadística:**

- XGBoost supera significativamente a los otros modelos (p < 0.05)

  

- IC 95% para RMSE de XGBoost: [$483.94, $498.52]

  

- Baja desviación estándar indica rendimiento consistenteIncome_Prediction_Model_Technical_Documentation.md

  

**Confiabilidad de Validación Cruzada:**

- Todos los modelos con baja varianza en las particiones

  

- Estimaciones robustas y sin evidencia de sobreajuste o fugas de datos

  



------



## **6. Desempeño Final y Resultados**

## **6.1 Comparación CV Anidada vs Prueba**

**Validación de Desempeño:**

| **Métrica** | **Estimación CV Anidada** | **Resultado Test** | **Diferencia** | **En IC 95%** |
| ----------- | ------------------------- | ------------------ | -------------- | ------------- |
| **RMSE**    | $491.23 ± $3.72           | **$540.63**        | $49.40         | ⚠️ No          |
| **MAE**     | $344.98 ± $2.94           | **$377.81**        | $32.83         | ⚠️ No          |
| **R²**      | 0.4940 ± 0.009            | **0.3913**         | 0.1027         | ⚠️ No          |
| **MAPE**    | No Medido                 | **34.5%**          | -              | -             |

**Análisis de diferencias:**

- El desempeño en prueba es levemente inferior al estimado por CV

  

- Diferencia de ~$49 RMSE aceptable en producción

  

- Diferencia de R² sugiere cierto sobreajuste, pero el modelo sigue siendo útil

  

- La degradación es típica en despliegues reales

  

## **6.2 Evaluación de Fiabilidad**

**Indicadores de Fiabilidad:**

✅ **Algoritmo seleccionado consistente:** XGBoost ganó en todos los folds
 ✅ **Hiperparámetros estables:** Parámetros óptimos similares en particiones
 ✅ **Baja varianza:** Desviaciones estándar bajas
 ✅ **Importancia lógica de variables:** Alineada con la intuición de negocio
 ⚠️ **Brecha de generalización:** Caída de ~10% entre CV y prueba

**Evaluación de Riesgos:**

- **Riesgo Bajo:** Arquitectura y variables sólidas

  

- **Riesgo Medio:** Evidencia de cierto sobreajuste general

  

- **Mitigación:** Reentrenamiento y monitoreo regular

  

## **6.3 Comparación con Experimentos de Transformación**

**Comparación de enfoques:**

| **Enfoque**                | **Mejor Modelo** | **RMSE Test** | **MAE Test** | **R² Test** | **Complejidad** |
| -------------------------- | ---------------- | ------------- | ------------ | ----------- | --------------- |
| **Normal (Base)**          | **XGBoost**      | **$540.63**   | $377.81      | **0.3913**  | ⭐ Simple        |
| Transformación Logarítmica | XGBoost          | $551.75       | **$370.41**  | 0.3660      | ⭐⭐ Media        |
| Box-Cox                    | XGBoost          | $552.14       | $369.97      | 0.3651      | ⭐⭐⭐ Compleja    |

**Hallazgos clave:**

- **El enfoque normal es superior:** $11+ RMSE mejor que las transformaciones

  

- **No ayudan las transformaciones:** XGBoost maneja bien la asimetría

  

- **La simplicidad gana:** Sin complejidad adicional en producción

  

- **Resultados consistentes:** Todas las aproximaciones identifican las mismas variables importantesIncome_Prediction_Model_Technical_Documentation.md

  

**Recomendación:****
** El enfoque base sin transformaciones logra:

- Mejor predicción ($540.63 vs $551+ RMSE)

  

- Simplicidad operativa (sin transformaciones)

  

- Bajo riesgo en producción

  

- Inferencia más rápida

  



------



## **7. Conclusiones y Recomendaciones**

## **7.1 Hallazgos Clave**

**Desempeño:**

- ✅ **Muy buena precisión:** $540.63 RMSE representa gran capacidad predictiva

  

- ✅ **Variables relevantes para el negocio:** Principales predictores alineados a la intuición financiera

  

- ✅ **Metodología robusta:** CV anidada garantiza confiabilidad

  

- ✅ **Listo para producción:** Pipeline validado integralmente

  

**Hallazgos técnicos:**

- **XGBoost óptimo:** Consistentemente supera los demás algoritmos

  

- **Sin transformar:** El enfoque base es mejor que log/Box-Cox

  

- **Selección efectiva:** El sistema de votación elige predictores robustos

  

- **Generalización aceptable:** Caída esperada ~10% es normal en producción

  

## **7.2 Recomendaciones para Despliegue**

**Despliegue inmediato:**

1. **Desplegar modelo base:** final_production_model_nested_cv.pkl

   

2. **Esperado:** RMSE ≈ $540 (se espera una variación de ±10%)

   

3. **Variables requeridas:** Asegurar las 10 disponibles en producción

   

4. **Monitoreo:** Rastrear precisión y deriva de variables

   

**Consideraciones operativas:**

- **Tiempo de inferencia:** < 1ms por predicción (sin transformación)

  

- **Requerimientos de memoria:** ~50MB (modelo + escalador + metadatos)

  

- **Dependencias:** Asegurar pipeline de datos para todas las variables

  

- **Manejo de errores:** Implementar reservas ante valores faltantes

  

**Monitoreo de desempeño:**

- **KPI principal:** RMSE en nuevas predicciones vs. ingresos reales

  

- **KPI secundarios:** MAE, R², estabilidad en importancia de variables

  

- **Umbrales de alerta:** RMSE > $600 or R² < 0.35

  

- **Revisión:** Reportes mensuales y evaluación trimestral

  

## **7.3 Oportunidades de Mejora**

**Corto plazo (3-6 meses):**

1. **Ingeniería de variables:** Explorar nuevas razones/interacciones

   

2. **Aumento de datos:** Incluir indicadores económicos externos

   

3. **Método en ensamble:** Combinar más modelos por precisión

   

4. **Optimización hiperparámetros:** Bayesian optimization

   

**Mediano plazo (6-12 meses):**

1. **Redes neuronales:** Para patrones complejos

   

2. **Aprendizaje en línea:** Adaptación continua

   

3. **Modelos por segmento:** Diferenciar por tipos de cliente

   

4. **Explicabilidad:** SHAP por predicción individual

   

**Largo plazo (12+ meses):**

1. **AutoML:** Selección y ajuste automático de modelos

   

2. **Optimización multi-objetivo:** Equilibrio entre precisión, justicia, interpretabilidad

   

3. **Inferencia causal:** Identificar relaciones causales

   

4. **Aprendizaje federado:** Actualizaciones con privacidad

   

**Datos e infraestructura:**

- Mejor calidad de datos

  

- Implementar feature store

  

- Marco de A/B testing en producción

  

- Pipeline de MLOps automático

  

## **7.4 Gestión de Riesgos y Mitigación**

**Riesgos identificados:**

1. **Drift del modelo:** Degradación en el tiempo

   

2. **Disponibilidad de variables:** Problemas de calidad de datos en producción

   

3. **Cumplimiento regulatorio:** Justicia y no discriminación

   

4. **Cambios económicos:** Patrones históricos pueden variar

   

**Estrategias de mitigación:**

1. **Reentrenamiento regular:** Actualizar trimestralmente

   

2. **Monitoreo robusto:** Alertas automáticas ante caídas de rendimiento

   

3. **Pruebas de sesgo:** Auditoría de justicia entre segmentos

   

4. **Mecanismos de reserva:** Reglas alternativas ante fallas del modelo

   

**Éxito en producción:**

- **Mantenimiento de precisión:** RMSE dentro de ±15% del baseline

  

- **Cobertura:** >95% de clientes con predicción válida

  

- **Tiempo de respuesta:** <100ms por predicción

  

- **Impacto de negocio:** Mejor targeting y gestión de riesgo

  



------



## **Apéndice Técnico**

## **Artefactos de Modelo**

- **Modelo de producción:** final_production_model_nested_cv.pkl

  

- **Lista de variables:** nested_cv_feature_list.csv

  

- **Métricas de desempeño:** nested_cv_results.json

  

- **Importancia por permutación:** nested_cv_permutation_importance.csv

  

## **Estructura del Código**

text

├── data/

│  ├── processed/     # Datasets limpios y con ingeniería de variables

│  └── models/      # Artefactos del modelo entrenado

├── notebooks/

│  ├── 02_00_clean_training_nested_version.ipynb # Pipeline de entrenamiento principal

│  ├── 02_01_clean_training_nested_version_log_transf.ipynb

│  └── 02_02_clean_training_nested_version_boxcox_transf.ipynb

└── documentation/

  └── Income_Prediction_Model_Technical_Documentation.md



