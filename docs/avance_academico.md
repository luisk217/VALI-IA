# Avance académico: Vali-IA

DEMOSTRACIÓN ACADÉMICA — DATOS TOTALMENTE FICTICIOS

**Problema.** Para elaborar informes mensuales es necesario revisar registros dispersos en Excel. Los campos vacíos, identificadores repetidos, fechas incoherentes y diferencias en los totales pueden trasladarse al informe. El proyecto representa esta necesidad en el Centro Demostrativo Huellas, una organización inventada.

**Solución construida.** Se desarrolló una aplicación local en español con Python, pandas, openpyxl y Streamlit. Permite cargar un Excel, ejecutar ocho reglas, consultar métricas, filtrar hallazgos y descargar un reporte. Cada hallazgo identifica la ubicación, explica el problema y propone una revisión. La conciliación distingue resultados provisionales y no comparables. Se generaron tres bases reproducibles de 200 actividades, correspondientes a enero–marzo de 2026.

**Componente de IA.** La validación y los cálculos se realizan con código determinista. La aplicación exporta un JSON y un prompt para que un asistente de IA redacte un borrador fundamentado en las evidencias. La transferencia es manual. Se incluye un ejemplo de texto generado por IA en la sesión de desarrollo y se distingue del resumen automático por plantilla.

**Resultados comprobados.** Pasaron 19 pruebas ejecutadas en Linux, incluidas pruebas del flujo de la interfaz mediante Streamlit AppTest. En la base alterada se detectaron 24 alertas de error y 3 advertencias que coinciden con el archivo independiente de resultados esperados, sin omisiones ni falsas alertas en ese conjunto. Se identificaron 18 filas de Registros con errores; el porcentaje sin errores fue 91 %. La base correcta no produjo alertas. La base de excepciones produjo únicamente 3 pendientes informativos y conservó 100 % de registros sin errores.

**Aprendizajes.** Un mismo animal puede participar en actividades distintas sin constituir un duplicado. Un campo vacío no siempre significa error ni cero. El número de alertas no equivale al número de registros afectados. Cuando la información de base presenta inconsistencias, un total no debe presentarse como definitivo. La utilidad de la IA depende de recibir cifras calculadas y referencias que la persona pueda comprobar.

**Limitaciones.** Los resultados corresponden a datos sintéticos y reglas acotadas. No se valida que las actividades hayan ocurrido ni se interpreta contenido clínico. No se ha medido tiempo manual, ahorro porcentual ni desempeño institucional. Se entregan instrucciones para Windows, pero no se ejecutaron pruebas en ese sistema. El entorno disponible no permitió una vista previa visual de Streamlit en Sites; se verificó su interacción mediante AppTest. Falta comprobar carga y descarga en el navegador del equipo del estudiante.

**Trabajo futuro.** Realizar un piloto cronometrado con revisión humana incluida, probar más casos límite, mejorar la clasificación de diferencias provisionales por grupo y evaluar una integración autorizada con un modelo de IA. Cualquier adaptación a información real requeriría definir el alcance y revisar previamente su manejo de datos.

Evidencias: `evidencias/resultados_pruebas.json`, `evidencias/pruebas_ejecutadas.txt`, `datos/errores_esperados.json` y `evidencias/reporte_validacion.xlsx`.
