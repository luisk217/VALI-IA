# Borrador de informe generado con IA

**DEMOSTRACIÓN ACADÉMICA — DATOS TOTALMENTE FICTICIOS**

**Pendiente de revisión humana.** Este ejemplo fue redactado por el asistente de IA durante la construcción de Vali-IA, a partir de `evidencias/resultados_validacion.json`. La aplicación no lo generó mediante una API. Es un ejemplo fijo para la demostración.

**Periodo y archivo.** Se revisó `base_con_errores.xlsx`, para el periodo del 1 de enero al 31 de marzo de 2026, con corte del 31 de marzo. [archivo, periodo, corte]

**Resultados principales.** Se revisaron 200 actividades. En 18 filas de Registros se identificó al menos un error, por lo que el 91 % de esas filas no presentó errores bajo las reglas implementadas. Estos resultados no certifican la veracidad de las actividades. [metricas.registros_revisados; metricas.registros_con_error; metricas.porcentaje_sin_errores]

El análisis produjo 24 alertas de error, 3 advertencias y 1 hallazgo informativo. El número de alertas no debe confundirse con las filas afectadas: también se detectaron problemas en el resumen mensual. [metricas.alertas_error; metricas.alertas_advertencia; metricas.alertas_informacion; H020–H028]

**Inconsistencias.** En la fila 4 falta el responsable. Las filas 5 y 6 comparten un identificador de actividad; el análisis no establece cuál debe conservarse. Hay fechas de actividad inválidas o fuera del periodo, edades fuera de las condiciones admitidas y seguimientos con incoherencias de fecha o estado. [H001/R01; H002–H003/R02; H005–H006/R04; H007–H010/R05; H011–H014/R06]

El resumen contiene un total negativo, un periodo no permitido, combinaciones ausentes y una combinación repetida. Estas situaciones impiden comparar de forma válida los grupos afectados. [H020–H021/R08; H023–H026/R08]

**Posible efecto sobre el informe.** Para enero, Canino, Valoración, aparecen 17 actividades reportadas frente a 12 filas agrupables, diferencia de 5. Esa diferencia es provisional: los errores de Registros pueden modificar el recuento y no permiten concluir que 12 sea el total verdadero. [H022/R07; conciliacion: 2026-01 / Canino / Valoración]

Hay cuatro registros que no se pudieron asignar al recuento por mes, especie y actividad. Sus ubicaciones se conservan en la lista de no agrupables. Las otras filas se cuentan como agrupables, incluso si contienen errores en otros campos. El seguimiento pendiente de la fila 22 se considera información; no demuestra un incumplimiento de plazo. [metricas.registros_no_agrupables; no_agrupables; H019/R06]

**Acciones propuestas.** Revisar los campos y fechas señalados, resolver la identidad de las actividades duplicadas mediante una comprobación humana, restaurar las combinaciones del resumen y volver a validar después de guardar una copia revisada. No se propone reemplazar automáticamente los totales ni eliminar filas. [H001–H018; H020–H028; acciones_sugeridas]

**Limitaciones.** El análisis corresponde a información ficticia, un periodo fijo y reglas definidas. No establece causas de los errores, no verifica hechos y no permite calcular ahorro de trabajo humano. Los resultados actuales requieren revisión antes de elaborar el informe. [aviso; periodo; listo_para_informe=false]

**Comprobaciones de la persona revisora:** confirmar los datos faltantes y fechas; resolver los IDs y combinaciones duplicados; ejecutar nuevamente Vali-IA y comprobar que el texto del informe conserva las cifras y la condición de provisionalidad de la última exportación.
