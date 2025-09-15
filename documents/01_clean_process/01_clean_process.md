============================================================
FINAL CLEANING SUMMARY: CLIENTES
============================================================
📊 Dataset shape: (29319, 27) → (29319, 27)
💾 Memory usage: 7.93 MB
🗂️  Total columns: 27

📋 Data types:
  datetime64[ns]: 3 columns
  float32: 3 columns
  float64: 2 columns
  int8: 2 columns
  int32: 1 columns
  category: 1 columns
  category: 1 columns
  object: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns
  category: 1 columns

📅 Date columns converted: ['fechaingresoempleo', 'fecha_inicio', 'fecha_vencimiento']
📅 Expected date columns: ['fechaingresoempleo', 'fecha_inicio', 'fecha_vencimiento']
✅ All expected date columns converted successfully!

🎯 Target column 'ingresos_reportados':
   Type: float64
   Non-null values: 29,319
   Range: 0.00 to 999999999.00
   Mean: 70272.85

🆔 Identifier column 'identificador_unico':
   Unique values: 29,319
   Uniqueness ratio: 100.00%

❓ Missing values: 123,873 (15.65% of total data)

🔍 Sample of cleaned data:
   cliente identificador_unico segmento  edad       sexo  \
0     3642           9-706-693     D34Z    47  Masculino   
1    10547           8-904-143     D02Z    29   Femenino   
2    13095           8-398-877     C66Q    74  Masculino   

                                          ciudad  \
0  ANTON                                           
1  ARRAIJAN                                        
2  PANAMA                                          

                                            pais  \
0  PANAMA                                          
1  PANAMA                                          
2  PANAMA                                          

                                       ocupacion estado_civil  \
0  JARDINERO                                          Soltero   
1  ASISTENTE                                           Casado   
2  JUBILADO                                            Casado   

  fechaingresoempleo             nombreempleadorcliente cargoempleocliente  \
0         2014-09-16  UNIVERSIDAD TECNOLOGICA DE PANAMA          JARDINERO   
1         2020-10-01     TRANSPORTE MASIVO DE PANAMA SA          ASISTENTE   
2         2013-04-14                          NO APLICA           JUBILADO   

  productos_activos  letras_mensuales  monto_letra     saldo fecha_inicio  \
0              PR15                 1   216.820007  12297.69   2018-05-08   
1              PR10                 1   202.279999  52145.67   2023-12-12   
2              PR10                 1   625.679993  39299.44   2017-03-28   

  fecha_vencimiento  ingresos_reportados controldate  monto_prestamo  \
0        2033-05-08                920.0         NaN             NaN   
1        2058-12-26                800.0         NaN             NaN   
2        2032-03-28               1148.3         NaN             NaN   

   tasa_prestamo       data_source processing_timestamp  \
0            NaN  Info_Cliente.csv  2025-09-06 20:35:16   
1            NaN  Info_Cliente.csv  2025-09-06 20:35:16   
2            NaN  Info_Cliente.csv  2025-09-06 20:35:16   

  fechaingresoempleo_original fecha_inicio_original fecha_vencimiento_original  
0                  16/09/2014            08/05/2018                 08/05/2033  
1                  01/10/2020            12/12/2023                 26/12/2058  
2                  14/04/2013            28/03/2017                 28/03/2032  

🎉 DATA CLEANING COMPLETE!
✅ Both datasets are now ready for exploratory data analysis
📝 Next steps: Detailed EDA, feature engineering, and modeling