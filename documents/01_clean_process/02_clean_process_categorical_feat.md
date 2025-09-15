📊 DETAILED EDA - CATEGORICAL VARIABLES ANALYSIS
================================================================================

🔍 CATEGORICAL VARIABLES ANALYSIS: CLIENTES
============================================================
📋 Categorical columns found: 16
Columns: ['identificador_unico', 'segmento', 'sexo', 'ciudad', 'pais', 'ocupacion', 'estado_civil', 'nombreempleadorcliente', 'cargoempleocliente', 'productos_activos', 'controldate', 'data_source', 'processing_timestamp', 'fechaingresoempleo_original', 'fecha_inicio_original', 'fecha_vencimiento_original']

📊 Analyzing: identificador_unico
----------------------------------------
   Total values: 29,319
   Non-null values: 29,319 (100.0%)
   Null values: 0 (0.0%)
   Unique values: 29,319
   Uniqueness ratio: 1.000
   Top 10 values:
       1. '8-799-2213': 1 (0.0%)
       2. '9-706-693': 1 (0.0%)
       3. '8-904-143': 1 (0.0%)
       4. '8-398-877': 1 (0.0%)
       5. '8-142-410': 1 (0.0%)
       6. '8-372-792': 1 (0.0%)
       7. '8-180-835': 1 (0.0%)
       8. '1-50-568': 1 (0.0%)
       9. '8-918-2129': 1 (0.0%)
      10. '8-955-658': 1 (0.0%)
   ⚠️  Potential issues: High cardinality - might be ID column, Many singleton values (29,319)

📊 Analyzing: segmento
----------------------------------------
   Total values: 29,319
   Non-null values: 29,319 (100.0%)
   Null values: 0 (0.0%)
   Unique values: 435
   Uniqueness ratio: 0.015
   Top 10 values:
       1. 'D01Z': 904 (3.1%)
       2. '    ': 873 (3.0%)
       3. 'D40Z': 486 (1.7%)
       4. 'D44Z': 399 (1.4%)
       5. 'D27Z': 397 (1.4%)
       6. 'D54Z': 385 (1.3%)
       7. 'D26Z': 351 (1.2%)
       8. 'D32Z': 350 (1.2%)
       9. 'B01D': 341 (1.2%)
      10. 'D15Z': 338 (1.2%)
   ✅ No obvious data quality issues

📊 Analyzing: sexo
----------------------------------------
   Total values: 29,319
   Non-null values: 29,319 (100.0%)
   Null values: 0 (0.0%)
   Unique values: 2
   Uniqueness ratio: 0.000
   Top 10 values:
       1. 'Femenino': 22,917 (78.2%)
       2. 'Masculino': 6,402 (21.8%)
   ✅ No obvious data quality issues

📊 Analyzing: ciudad
----------------------------------------
   Total values: 29,319
   Non-null values: 28,821 (98.3%)
   Null values: 498 (1.7%)
   Unique values: 78
   Uniqueness ratio: 0.003
   Top 10 values:
       1. 'PANAMA                                       ': 10,010 (34.7%)
       2. 'ARRAIJAN                                     ': 2,968 (10.3%)
       3. 'SAN MIGUELITO                                ': 2,888 (10.0%)
       4. 'LA CHORRERA                                  ': 2,572 (8.9%)
       5. 'DAVID                                        ': 1,758 (6.1%)
       6. 'COLON                                        ': 1,032 (3.6%)
       7. 'CHITRE                                       ': 904 (3.1%)
       8. 'SANTIAGO                                     ': 898 (3.1%)
       9. 'PENONOME                                     ': 633 (2.2%)
      10. 'BUGABA                                       ': 622 (2.2%)
   ✅ No obvious data quality issues

📊 Analyzing: pais
----------------------------------------
   Total values: 29,319
   Non-null values: 29,319 (100.0%)
   Null values: 0 (0.0%)
   Unique values: 16
   Uniqueness ratio: 0.001
   Top 10 values:
       1. 'PANAMA                                       ': 29,295 (99.9%)
       2. 'COLOMBIA                                     ': 4 (0.0%)
       3. 'NICARAGUA                                    ': 3 (0.0%)
       4. 'EL SALVADOR                                  ': 3 (0.0%)
       5. 'PALESTINA                                    ': 2 (0.0%)
       6. 'PERU                                         ': 2 (0.0%)
       7. 'BELICE                                       ': 1 (0.0%)
       8. 'BRASIL                                       ': 1 (0.0%)
       9. 'NAMIBIA                                      ': 1 (0.0%)
      10. 'MEXICO                                       ': 1 (0.0%)
   ⚠️  Potential issues: Many singleton values (10)

📊 Analyzing: ocupacion
----------------------------------------
   Total values: 29,319
   Non-null values: 29,312 (100.0%)
   Null values: 7 (0.0%)
   Unique values: 245
   Uniqueness ratio: 0.008
   Top 10 values:
       1. 'JUBILADO                                     ': 4,862 (16.6%)
       2. 'DOCENTE                                      ': 2,080 (7.1%)
       3. 'POLICIA                                      ': 1,578 (5.4%)
       4. 'OFICINISTAS                                  ': 1,070 (3.7%)
       5. 'SUPERVISOR                                   ': 1,049 (3.6%)
       6. 'ASISTENTE                                    ': 894 (3.0%)
       7. 'SECRETARIAS                                  ': 829 (2.8%)
       8. 'ADMINISTRADOR                                ': 828 (2.8%)
       9. 'VENDEDOR                                     ': 823 (2.8%)
      10. 'TECNICO                                      ': 681 (2.3%)
   ✅ No obvious data quality issues

📊 Analyzing: estado_civil
----------------------------------------
   Total values: 29,319
   Non-null values: 29,319 (100.0%)
   Null values: 0 (0.0%)
   Unique values: 4
   Uniqueness ratio: 0.000
   Top 10 values:
       1. 'Soltero': 16,705 (57.0%)
       2. 'Casado': 12,590 (42.9%)
       3. 'Otros': 21 (0.1%)
       4. 'Divorciado': 3 (0.0%)
   ✅ No obvious data quality issues

📊 Analyzing: nombreempleadorcliente
----------------------------------------
   Total values: 29,319
   Non-null values: 27,863 (95.0%)
   Null values: 1,456 (5.0%)
   Unique values: 7,698
   Uniqueness ratio: 0.276
   Top 10 values:
       1. 'NO APLICA': 4,212 (15.1%)
       2. 'MINISTERIO DE EDUCACION': 2,299 (8.3%)
       3. 'MINISTERIO DE SEGURIDAD PUBLICA': 1,468 (5.3%)
       4. 'CAJA DE SEGURO SOCIAL': 1,352 (4.9%)
       5. 'CAJA DE AHORROS': 1,027 (3.7%)
       6. 'MINISTERIO DE SALUD': 786 (2.8%)
       7. 'INDEPENDIENTE': 395 (1.4%)
       8. 'ORGANO JUDICIAL': 331 (1.2%)
       9. 'PROCURADURIA GENERAL DE LA NACION': 266 (1.0%)
      10. 'UNIVERSIDAD DE PANAMA': 261 (0.9%)
   ⚠️  Potential issues: Many singleton values (6,389)

📊 Analyzing: cargoempleocliente
----------------------------------------
   Total values: 29,319
   Non-null values: 21,836 (74.5%)
   Null values: 7,483 (25.5%)
   Unique values: 2,178
   Uniqueness ratio: 0.100
   Top 10 values:
       1. 'JUBILADO': 2,861 (13.1%)
       2. 'POLICIA': 1,094 (5.0%)
       3. 'DOCENTE': 988 (4.5%)
       4. 'SECRETARIA': 641 (2.9%)
       5. 'SUPERVISOR': 641 (2.9%)
       6. 'OFICINISTA': 619 (2.8%)
       7. 'ASISTENTE': 610 (2.8%)
       8. 'VENDEDOR': 476 (2.2%)
       9. 'EDUCADOR': 390 (1.8%)
      10. 'EDUCADORA': 365 (1.7%)
   ⚠️  Potential issues: Many singleton values (1,567)

📊 Analyzing: productos_activos
----------------------------------------
   Total values: 29,319
   Non-null values: 29,319 (100.0%)
   Null values: 0 (0.0%)
   Unique values: 16
   Uniqueness ratio: 0.001
   Top 10 values:
       1. 'CA  ': 11,888 (40.5%)
       2. 'PR10': 8,590 (29.3%)
       3. 'PR15': 4,702 (16.0%)
       4. 'TC  ': 2,639 (9.0%)
       5. 'SIMP': 404 (1.4%)
       6. '20AH': 330 (1.1%)
       7. 'PR12': 323 (1.1%)
       8. '20PF': 322 (1.1%)
       9. 'CC  ': 49 (0.2%)
      10. 'PR16': 23 (0.1%)
   ✅ No obvious data quality issues

📊 Analyzing: controldate
----------------------------------------
   Total values: 29,319
   Non-null values: 15,000 (51.2%)
   Null values: 14,319 (48.8%)
   Unique values: 1
   Uniqueness ratio: 0.000
   Top 10 values:
       1. '9/4/2025': 15,000 (100.0%)
   ✅ No obvious data quality issues

📊 Analyzing: data_source
----------------------------------------
   Total values: 29,319
   Non-null values: 29,319 (100.0%)
   Null values: 0 (0.0%)
   Unique values: 2
   Uniqueness ratio: 0.000
   Top 10 values:
       1. 'Info_Clientes_2.csv': 15,000 (51.2%)
       2. 'Info_Cliente.csv': 14,319 (48.8%)
   ✅ No obvious data quality issues

📊 Analyzing: processing_timestamp
----------------------------------------
   Total values: 29,319
   Non-null values: 29,319 (100.0%)
   Null values: 0 (0.0%)
   Unique values: 1
   Uniqueness ratio: 0.000
   Top 10 values:
       1. '2025-09-06 20:35:16': 29,319 (100.0%)
   ✅ No obvious data quality issues

📊 Analyzing: fechaingresoempleo_original
----------------------------------------
   Total values: 29,319
   Non-null values: 27,001 (92.1%)
   Null values: 2,318 (7.9%)
   Unique values: 11,243
   Uniqueness ratio: 0.416
   Top 10 values:
       1. '1/2/2024': 86 (0.3%)
       2. '01/01/2000': 79 (0.3%)
       3. '1/1/2024': 62 (0.2%)
       4. '02/01/2024': 59 (0.2%)
       5. '01/01/2001': 49 (0.2%)
       6. '18/02/2014': 46 (0.2%)
       7. '01/03/1997': 45 (0.2%)
       8. '11/1/2015': 45 (0.2%)
       9. '1/3/2017': 40 (0.1%)
      10. '01/08/1996': 37 (0.1%)
   ⚠️  Potential issues: Many singleton values (6,344)

📊 Analyzing: fecha_inicio_original
----------------------------------------
   Total values: 29,319
   Non-null values: 29,319 (100.0%)
   Null values: 0 (0.0%)
   Unique values: 11,029
   Uniqueness ratio: 0.376
   Top 10 values:
       1. '9/27/2022': 79 (0.3%)
       2. '07/01/2025': 29 (0.1%)
       3. '3/17/2025': 25 (0.1%)
       4. '1/31/2025': 24 (0.1%)
       5. '7/15/2025': 22 (0.1%)
       6. '1/7/2025': 22 (0.1%)
       7. '1/10/2025': 21 (0.1%)
       8. '3/14/2025': 21 (0.1%)
       9. '5/20/2025': 20 (0.1%)
      10. '3/18/2025': 19 (0.1%)
   ✅ No obvious data quality issues

📊 Analyzing: fecha_vencimiento_original
----------------------------------------
   Total values: 29,319
   Non-null values: 14,339 (48.9%)
   Null values: 14,980 (51.1%)
   Unique values: 8,635
   Uniqueness ratio: 0.602
   Top 10 values:
       1. '28/07/2041': 10 (0.1%)
       2. '28/08/2033': 10 (0.1%)
       3. '24/06/2032': 9 (0.1%)
       4. '27/02/2033': 9 (0.1%)
       5. '28/06/2041': 8 (0.1%)
       6. '28/02/2033': 8 (0.1%)
       7. '28/06/2042': 8 (0.1%)
       8. '28/04/2045': 8 (0.1%)
       9. '28/02/2030': 7 (0.0%)
      10. '28/07/2043': 7 (0.0%)
   ⚠️  Potential issues: Many singleton values (5,146)

🔬 DEEP DIVE CATEGORICAL ANALYSIS
============================================================

📊 DEEP DIVE: sexo
==================================================
Non-null values: 29,319
Unique values: 2

Value distribution:
    1. 'Femenino': 22,917 (78.2%)
    2. 'Masculino': 6,402 (21.8%)

🔍 Checking for potential name variations:

📈 Statistical summary:
   Most common: 'Femenino' (22,917 occurrences)
   Least common: 0 values appear only once
   Top 5 values represent: 100.0% of data

📊 DEEP DIVE: ciudad
==================================================
Non-null values: 28,821
Unique values: 78

Value distribution:
    1. 'PANAMA                                       ': 10,010 (34.7%)
    2. 'ARRAIJAN                                     ': 2,968 (10.3%)
    3. 'SAN MIGUELITO                                ': 2,888 (10.0%)
    4. 'LA CHORRERA                                  ': 2,572 (8.9%)
    5. 'DAVID                                        ': 1,758 (6.1%)
    6. 'COLON                                        ': 1,032 (3.6%)
    7. 'CHITRE                                       ': 904 (3.1%)
    8. 'SANTIAGO                                     ': 898 (3.1%)
    9. 'PENONOME                                     ': 633 (2.2%)
   10. 'BUGABA                                       ': 622 (2.2%)
   11. 'CHANGUINOLA                                  ': 479 (1.7%)
   12. 'AGUADULCE                                    ': 441 (1.5%)
   13. 'DOLEGA                                       ': 440 (1.5%)
   14. 'LAS TABLAS                                   ': 425 (1.5%)
   15. 'BARU                                         ': 230 (0.8%)
   16. 'BOQUETE                                      ': 215 (0.7%)
   17. 'BOQUERON                                     ': 203 (0.7%)
   18. 'LOS SANTOS                                   ': 201 (0.7%)
   19. 'ATALAYA                                      ': 192 (0.7%)
   20. 'ANTON                                        ': 158 (0.5%)
   ... and 58 more unique values

🔍 Checking for potential name variations:

📈 Statistical summary:
   Most common: 'PANAMA                                       ' (10,010 occurrences)
   Least common: 3 values appear only once
   Top 5 values represent: 70.1% of data

📊 DEEP DIVE: pais
==================================================
Non-null values: 29,319
Unique values: 16

Value distribution:
    1. 'PANAMA                                       ': 29,295 (99.9%)
    2. 'COLOMBIA                                     ': 4 (0.0%)
    3. 'NICARAGUA                                    ': 3 (0.0%)
    4. 'EL SALVADOR                                  ': 3 (0.0%)
    5. 'PALESTINA                                    ': 2 (0.0%)
    6. 'PERU                                         ': 2 (0.0%)
    7. 'BELICE                                       ': 1 (0.0%)
    8. 'BRASIL                                       ': 1 (0.0%)
    9. 'NAMIBIA                                      ': 1 (0.0%)
   10. 'MEXICO                                       ': 1 (0.0%)
   11. 'GUATEMALA                                    ': 1 (0.0%)
   12. 'PAISES BAJOS                                 ': 1 (0.0%)
   13. 'PAPUA NUEVA GUINEA                           ': 1 (0.0%)
   14. 'PARAGUAY                                     ': 1 (0.0%)
   15. 'REPUBLICA DOMINICANA                         ': 1 (0.0%)
   16. 'RUSIA                                        ': 1 (0.0%)

🔍 Checking for potential name variations:

📈 Statistical summary:
   Most common: 'PANAMA                                       ' (29,295 occurrences)
   Least common: 10 values appear only once
   Top 5 values represent: 100.0% of data

📊 DEEP DIVE: ocupacion
==================================================
Non-null values: 29,312
Unique values: 245

Value distribution:
    1. 'JUBILADO                                     ': 4,862 (16.6%)
    2. 'DOCENTE                                      ': 2,080 (7.1%)
    3. 'POLICIA                                      ': 1,578 (5.4%)
    4. 'OFICINISTAS                                  ': 1,070 (3.7%)
    5. 'SUPERVISOR                                   ': 1,049 (3.6%)
    6. 'ASISTENTE                                    ': 894 (3.0%)
    7. 'SECRETARIAS                                  ': 829 (2.8%)
    8. 'ADMINISTRADOR                                ': 828 (2.8%)
    9. 'VENDEDOR                                     ': 823 (2.8%)
   10. 'TECNICO                                      ': 681 (2.3%)
   11. 'INGENIERO                                    ': 592 (2.0%)
   12. 'ABOGADOS                                     ': 587 (2.0%)
   13. 'GERENTE                                      ': 557 (1.9%)
   14. 'ENFERMERA                                    ': 534 (1.8%)
   15. 'AYUDANTE GENERAL                             ': 498 (1.7%)
   16. 'CAJEROS                                      ': 484 (1.7%)
   17. 'EDUCADOR                                     ': 476 (1.6%)
   18. 'ANALISTA                                     ': 448 (1.5%)
   19. 'ESTUDIANTE                                   ': 438 (1.5%)
   20. 'TRABAJADOR MANUAL                            ': 436 (1.5%)
   ... and 225 more unique values

🔍 Checking for potential name variations:

📈 Statistical summary:
   Most common: 'JUBILADO                                     ' (4,862 occurrences)
   Least common: 21 values appear only once
   Top 5 values represent: 36.3% of data

📊 DEEP DIVE: estado_civil
==================================================
Non-null values: 29,319
Unique values: 4

Value distribution:
    1. 'Soltero': 16,705 (57.0%)
    2. 'Casado': 12,590 (42.9%)
    3. 'Otros': 21 (0.1%)
    4. 'Divorciado': 3 (0.0%)

🔍 Checking for potential name variations:

📈 Statistical summary:
   Most common: 'Soltero' (16,705 occurrences)
   Least common: 0 values appear only once
   Top 5 values represent: 100.0% of data

📊 DEEP DIVE: nombreempleadorcliente
==================================================
Non-null values: 27,863
Unique values: 7,698

Value distribution:
    1. 'NO APLICA': 4,212 (15.1%)
    2. 'MINISTERIO DE EDUCACION': 2,299 (8.3%)
    3. 'MINISTERIO DE SEGURIDAD PUBLICA': 1,468 (5.3%)
    4. 'CAJA DE SEGURO SOCIAL': 1,352 (4.9%)
    5. 'CAJA DE AHORROS': 1,027 (3.7%)
    6. 'MINISTERIO DE SALUD': 786 (2.8%)
    7. 'INDEPENDIENTE': 395 (1.4%)
    8. 'ORGANO JUDICIAL': 331 (1.2%)
    9. 'PROCURADURIA GENERAL DE LA NACION': 266 (1.0%)
   10. 'UNIVERSIDAD DE PANAMA': 261 (0.9%)
   11. 'MINISTERIO DE LA PRESIDENCIA': 218 (0.8%)
   12. 'CONTRALORIA GENERAL DE LA REPUBLICA': 205 (0.7%)
   13. 'JUBILADO': 193 (0.7%)
   14. 'ASAMBLEA NACIONAL': 181 (0.6%)
   15. 'MINISTERIO DE ECONOMIA Y FINANZAS': 153 (0.5%)
   16. 'BNP': 150 (0.5%)
   17. 'AUTORIDAD DEL CANAL DE PANAMA': 147 (0.5%)
   18. 'TRIBUNAL ELECTORAL': 144 (0.5%)
   19. 'MINISTERIO DE GOBIERNO': 128 (0.5%)
   20. 'POLICIA NACIONAL': 127 (0.5%)
   ... and 7678 more unique values

🔍 Checking for potential name variations:

📈 Statistical summary:
   Most common: 'NO APLICA' (4,212 occurrences)
   Least common: 6,389 values appear only once
   Top 5 values represent: 37.2% of data

📊 DEEP DIVE: cargoempleocliente
==================================================
Non-null values: 21,836
Unique values: 2,178

Value distribution:
    1. 'JUBILADO': 2,861 (13.1%)
    2. 'POLICIA': 1,094 (5.0%)
    3. 'DOCENTE': 988 (4.5%)
    4. 'SECRETARIA': 641 (2.9%)
    5. 'SUPERVISOR': 641 (2.9%)
    6. 'OFICINISTA': 619 (2.8%)
    7. 'ASISTENTE': 610 (2.8%)
    8. 'VENDEDOR': 476 (2.2%)
    9. 'EDUCADOR': 390 (1.8%)
   10. 'EDUCADORA': 365 (1.7%)
   11. 'TECNICO': 364 (1.7%)
   12. 'ENFERMERA': 362 (1.7%)
   13. 'GERENTE': 351 (1.6%)
   14. 'AYUDANTE GENERA': 323 (1.5%)
   15. 'ANALISTA': 290 (1.3%)
   16. 'CAJERO': 256 (1.2%)
   17. 'ABOGADO': 236 (1.1%)
   18. 'OFICIAL': 223 (1.0%)
   19. 'TRABAJADOR MANU': 223 (1.0%)
   20. 'INGENIERO': 213 (1.0%)
   ... and 2158 more unique values

🔍 Checking for potential name variations:

📈 Statistical summary:
   Most common: 'JUBILADO' (2,861 occurrences)
   Least common: 1,567 values appear only once
   Top 5 values represent: 28.5% of data