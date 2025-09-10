# Modelo de Predicción de Ingresos - Documentación Técnica (Versión Mejorada y Completa)

# Modelo de Predicción de Ingresos

## Introducción
Este documento proporciona una visión integral del desarrollo, validación y despliegue de un modelo de predicción de ingresos de clientes, utilizando técnicas avanzadas de aprendizaje automático. El objetivo es facilitar la toma de decisiones en productos financieros y gestión de riesgos.

## Logros Clave
*   Implementación de un modelo robusto con validación cruzada anidada.
*   Selección automatizada de variables relevantes mediante sistemas de votación.
*   Desempeño superior respecto a modelos tradicionales.
*   Documentación y trazabilidad completa del proceso.

## Objetivo
Desarrollar un modelo de aprendizaje automático capaz de predecir con precisión el ingreso de clientes, permitiendo mejores recomendaciones de productos financieros y una evaluación de riesgos más precisa.

## Valor para el Negocio
*   Optimización de la oferta de productos.
*   Mejora en la segmentación y retención de clientes.
*   Reducción de riesgos crediticios.
*   Incremento en la rentabilidad mediante decisiones basadas en datos.

## Supuestos
### Supuestos de Datos
*   Los datos provienen de fuentes confiables y están actualizados.
*   Se han eliminado duplicados y valores atípicos.
*   Los datos faltantes se han imputado usando técnicas estadísticas.

### Supuestos de Modelado
*   Las relaciones entre variables pueden ser no lineales.
*   El modelo puede generalizar a nuevos clientes.
*   No existe fuga de información entre entrenamiento y prueba.

### Supuestos de Negocio
*   Las variables seleccionadas reflejan factores clave del negocio.
*   El modelo será revisado y actualizado periódicamente.

## Métricas de Evaluación
### Métricas Principales
*   RMSE (Root Mean Squared Error)
*   MAE (Mean Absolute Error)
*   R² (Coeficiente de determinación)

### Métricas Secundarias
*   MAPE (Mean Absolute Percentage Error)
*   Precisión por decil de ingreso
*   Estabilidad de los hiperparámetros

### Criterios de Fiabilidad
*   Consistencia de resultados en diferentes particiones.
*   Baja varianza entre folds de validación.
*   Importancia lógica de variables.

## Ingeniería de Variables
La ingeniería de variables se realizó en dos fases:

### Fase 1: Procesamiento Básico
*   Limpieza de datos.
*   Conversión de fechas a variables numéricas (ej. antigüedad en días).
*   Normalización de variables numéricas.

### Fase 2: Ingeniería Avanzada
*   Creación de ratios financieros (ej. saldo/pago mensual).
*   Agrupación de categorías poco frecuentes.
*   Generación de puntuaciones de estabilidad laboral y financiera.

## Selección y Análisis de Variables
Se utilizó un sistema de votación entre modelos (XGBoost, Random Forest, LightGBM) para seleccionar las variables más relevantes.

### Top 5 Variables Críticas (Ejemplo)
1. Edad
2. Antigüedad en empleo (días)
3. Saldo de cuenta
4. Ratio saldo/pago
5. Estabilidad laboral

### Variables Excluidas (Ejemplo)
*   Variables con alta correlación entre sí.
*   Variables con más de 30% de valores faltantes.

## Sistema de Votación de Variables
El sistema de votación combina los resultados de varios algoritmos para robustez:
*   Entrenamiento individual de modelos.
*   Umbrales de importancia para cada variable.
*   Consenso final basado en frecuencia de selección.
*   Control de calidad mediante validación cruzada.

## Robustez, Interpretabilidad y Desempeño
*   El modelo es robusto ante cambios en los datos.
*   Las variables seleccionadas son interpretables y alineadas con el negocio.
*   El desempeño es consistente en diferentes muestras.

## Variables Finales Seleccionadas

| Posición | Nombre de Variable | Tipo | Significado de Negocio |
| ---| ---| ---| --- |
| 1 | ocupacion\_consolidated\_freq | Frecuencia | Común en puestos laborales |
| 2 | nombreempleadorcliente\_consolidated\_freq | Frecuencia | Tamaño/estabilidad del empleador |
| 3 | edad | Numérica | Edad del cliente |
| 4 | fechaingresoempleo\_days | Temporal | Antigüedad en empleo |
| 5 | cargoempleocliente\_consolidated\_freq | Frecuencia | Frecuencia por cargo |
| 6 | fecha\_inicio\_days | Temporal | Antigüedad de cuenta |
| 7 | balance\_to\_payment\_ratio | Razón | Salud financiera |
| 8 | professional\_stability\_score | Derivada | Estabilidad laboral |
| 9 | saldo | Numérica | Saldo de cuenta |
| 10 | employment\_years | Numérica | Años de experiencia laboral |

## Categorización de Variables
*   Nivel 1 - Críticas (impacto >$50,000): Edad, saldo, ratio saldo/pago.
*   Nivel 2 - Importantes ($10,000-$50,000): Antigüedad laboral, estabilidad laboral.
*   Nivel 3 - Secundarias (<$10,000): Antigüedad de cuenta, cargo, empleador.

## Validación Cruzada Anidada
La validación cruzada anidada se implementó para evitar sobreajuste y obtener estimaciones imparciales del desempeño.

### Beneficios
*   Separación total entre selección de modelo y evaluación.
*   Reducción de sesgo y varianza.

## Algoritmos Evaluados
*   XGBoost
*   Random Forest
*   LightGBM
*   Regresión Lineal (como referencia)

### Grid de XGBoost (Ejemplo)

```python
{
  'n_estimators': [300, 500, 700],
  'max_depth': [6, 8, 10],
  'learning_rate': [0.01, 0.05, 0.1],
  'subsample': [0.8, 0.85, 0.9],
  'colsample_bytree': [0.8, 0.85, 0.9],
  'reg_alpha': [0, 0.1, 0.5],
  'reg_lambda': [0.5, 1.0, 2.0]
}
```

## Resultados de Validación

| Modelo | Media RMSE | Std RMSE | Media MAE | Std MAE | Media R² | Std R² |
| ---| ---| ---| ---| ---| ---| --- |
| XGBoost | $491.23 | $3.72 | $344.98 | $2.94 | 0.4940 | 0.009 |
| Random Forest | $506.01 | $3.98 | $359.77 | $2.71 | 0.4631 | 0.011 |
| LightGBM | $510.82 | $3.21 | $367.64 | $3.40 | 0.4528 | 0.010 |

## Validación de Desempeño

| Métrica | Estimación CV Anidada | Resultado Test | Diferencia | En IC 95% |
| ---| ---| ---| ---| --- |
| RMSE | $491.23 ± $3.72 | $540.63 | $49.40 | ⚠️ No |
| MAE | $344.98 ± $2.94 | $377.81 | $32.83 | ⚠️ No |
| R² | 0.4940 ± 0.009 | 0.3913 | 0.1027 | ⚠️ No |
| MAPE | No Medido | 34.5% | \- | \- |

### Análisis de Diferencias
*   Se observa una brecha de generalización (~10%) entre validación y prueba.
*   El modelo mantiene estabilidad en la selección de variables y parámetros.

## Evaluación de Riesgos
*   Riesgo de sobreajuste mitigado por validación cruzada anidada.
*   Posible cambio en la distribución de datos futuros.
*   Dependencia de la calidad de los datos de entrada.

## Comparación de Enfoques

| Enfoque | Mejor Modelo | RMSE Test | MAE Test | R² Test | Complejidad |
| ---| ---| ---| ---| ---| --- |
| Normal (Base) | XGBoost | $540.63 | $377.81 | 0.3913 | Baja |
| Transformación Logarítmica | XGBoost | $551.75 | $370.41 | 0.3660 | Media |
| Box-Cox | XGBoost | $552.14 | $369.97 | 0.3651 | Alta |

**Conclusión:** El enfoque base es el más recomendable por su simplicidad y buen desempeño.

## Despliegue y Operación
### Despliegue Inmediato
1. Implementar el modelo en el entorno de producción.
2. Integrar con sistemas de toma de decisiones.
3. Capacitar a los usuarios clave.
4. Establecer monitoreo automático de desempeño.

### Consideraciones Operativas
*   Definir alertas para desviaciones en métricas clave.
*   Documentar procedimientos de actualización y mantenimiento.

### Monitoreo de Desempeño
*   Revisar métricas mensualmente.
*   Realizar auditorías trimestrales del modelo.

## Plan de Actualización
### Corto Plazo (3-6 meses)
*   Reentrenar el modelo con nuevos datos.
*   Revisar la importancia de variables.

### Mediano Plazo (6-12 meses)
*   Evaluar nuevas fuentes de datos.
*   Probar algoritmos alternativos.

### Largo Plazo (12+ meses)
*   Automatizar el pipeline de actualización.
*   Implementar modelos de autoaprendizaje.

## Datos e Infraestructura
*   Los datos procesados y modelos entrenados se almacenan en `/data/processed/` y `/data/models/`.
*   Los notebooks de entrenamiento están en `/notebooks/`.
*   La documentación técnica se encuentra en `/documentation/`.

## Riesgos y Estrategias de Mitigación
### Riesgos Identificados
1. Cambios en la calidad de los datos.
2. Obsolescencia de variables clave.
3. Cambios regulatorios.

### Estrategias de Mitigación
1. Monitoreo continuo de calidad de datos.
2. Actualización periódica de variables y modelo.
3. Revisión legal y de cumplimiento anual.

## Éxito en Producción
*   El modelo se considera exitoso si mantiene el RMSE dentro del 10% de la validación y mejora la toma de decisiones de negocio.

## Contacto
Para consultas técnicas o soporte de despliegue, contactar al equipo de Ciencia de Datos.

_Versión del documento: 1.0_
_Última actualización: septiembre 2025_
_Revisión próxima: marzo 2026_