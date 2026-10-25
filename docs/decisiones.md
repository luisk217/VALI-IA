# Decisiones de la versión 1.0

DEMOSTRACIÓN ACADÉMICA — DATOS TOTALMENTE FICTICIOS

1. **Escenario inventado desde cero.** No se consultaron archivos privados. Todos los nombres, códigos, actividades y cifras se generaron para este ejercicio. No son datos anonimizados de una entidad real.
2. **Una fila representa una actividad.** El registro de un mismo animal en varias filas es legítimo si las actividades tienen IDs distintos. No se modela un historial clínico ni se infiere estado de salud.
3. **Periodo fijo.** Fechas de enero a marzo de 2026, corte incluido. No se usa la fecha actual para resolver validaciones históricas.
4. **Formato explícito.** Aviso en fila 1, contexto en fila 2, cabeceras en fila 3. Se mantienen cuatro hojas obligatorias. Los totales reportados son valores independientes, no fórmulas enlazadas: pueden diferir del recuento y así se puede evaluar R07.
5. **Catálogo cerrado.** La hoja Catalogos debe coincidir con la especificación 1.0. Se comprueba antes de usarla. No se aceptan nuevas categorías simplemente por añadirlas al archivo.
6. **Recuento transparente.** Todas las filas agrupables entran al recuento provisional, incluidos los duplicados y registros con errores en campos que no determinan el grupo. Las filas no agrupables se enumeran aparte. No se borra, corrige ni elige información.
7. **Confiabilidad conservadora.** Cualquier error en Registros hace provisionales todas las comparaciones. Una combinación inválida del resumen impide esa comparación. Las otras combinaciones pueden compararse, pero el libro sigue requiriendo revisión si queda cualquier error o advertencia.
8. **Ausencias y pendientes.** Los vacíos obligatorios generan R01, evitando redundancia R03–R05. Un seguimiento pendiente es información. Sin fecha de actividad interpretable, no se puede comprobar el orden con un seguimiento informado: advertencia R06.
9. **Identidad de hallazgos.** Se usa ubicación física además del ID, porque este último puede estar ausente o duplicado. H001, etc. identifica un hallazgo dentro de un reporte, no entre diferentes ejecuciones. El SHA-256 vincula el reporte a los bytes exactos del archivo de entrada.
10. **Prueba independiente.** Los errores esperados se describen al introducir mutaciones; no se obtienen ejecutando el validador. El contraste usa coincidencia exacta, con multiplicidades, y mide errores y advertencias. Los informativos tienen pruebas independientes.
11. **Protección de la interpretación.** Las celdas no se ejecutan como código ni como instrucciones de IA. Las fórmulas se rechazan en entradas. Los reportes escriben textos que empiezan por = como texto literal.
12. **Reproducibilidad.** Una semilla fija reproduce valores y hallazgos; los bytes del archivo ZIP interno de Excel pueden variar por metadatos, y los tiempos de ejecución siempre varían. No se promete igualdad binaria entre archivos regenerados.
13. **Interfaz local.** Streamlit sobre Python, sin publicación, autenticación ni conectores. La mención de Sites se consideró para la vista previa, que no es compatible aquí con Python; se entrega una aplicación local completa.
14. **IA manual.** El paquete JSON y el prompt permiten que un asistente redacte el borrador. La aplicación no invoca modelos ni cobra una API. La integración directa queda para una fase posterior.

Fuera de alcance: verificar hechos reales, detectar todos los errores semánticos, resolver duplicados, validar prefijos de identificadores, conciliar historias clínicas, inferir causas, medir incumplimiento de plazos no definidos, escritura a sistemas institucionales o evaluación en producción.
