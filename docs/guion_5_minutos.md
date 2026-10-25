# Demostración de Vali-IA en cinco minutos

DEMOSTRACIÓN ACADÉMICA — DATOS TOTALMENTE FICTICIOS

Preparación: abre Vali-IA, el Excel de errores, un asistente de IA y el prompt. Ten el ejemplo de borrador como respaldo; si lo usas, di que es un ejemplo preparado, no una generación en vivo.

| Tiempo | Acción y mensaje |
|---|---|
| 0:00–0:35 | “En el Centro Demostrativo Huellas se registran actividades en Excel. Antes de informar, alguien debe revisar campos, fechas y totales. Todo lo que mostraré es inventado para el curso”. |
| 0:35–1:00 | Muestra la base con errores. Señala responsable_id vacío en fila 4 y el identificador repetido en filas 5 y 6. Explica que cada fila representa una actividad. |
| 1:00–1:30 | Selecciona Con errores conocidos y pulsa Validar información. Muestra 200 registros, 18 con error y 91 % sin errores. Explica que 24 alertas de error incluye el resumen, por eso no equivale a 24 registros. |
| 1:30–2:15 | Muestra H001 (responsable ausente), H002/H003 (ID duplicado) y H022 (17 reportadas frente a 12 agrupables, diferencia provisional de 5). Lee la acción sugerida y aclara que no se corrige automáticamente. |
| 2:15–2:50 | Cambia a Excepciones válidas y valida. Muestra 100 % sin errores y 3 pendientes informativos. Explica que repetir un animal y tener un seguimiento pendiente no son errores automáticos. |
| 2:50–3:15 | Vuelve a Con errores conocidos y valida. Descarga el reporte Excel. En Conciliación muestra las cuatro filas no agrupables: se enumeran, no desaparecen. |
| 3:15–4:30 | Descarga y extrae el paquete de IA. Adjunta el JSON y pega el prompt en el asistente. Di: “Este paso es manual; Python comprueba los datos y la IA explica los resultados”. Verifica dos cifras y una referencia. Si el asistente tarda, muestra el ejemplo preparado con esa aclaración. |
| 4:30–5:00 | “Se ejecutaron 19 pruebas. Coincidieron 27 hallazgos de error o advertencia con lo esperado, sin falsas alertas en este conjunto. Aún falta medir tiempo manual y probar en Windows. La siguiente mejora sería ampliar casos e integrar la IA de forma autorizada”. |

Preguntas que puedes responder:

- **¿Por qué no pedirle todo directamente a una IA?** Las reglas y cálculos tienen que ser reproducibles; la IA ayuda a explicar el resultado.
- **¿La base está lista si dice 100 %?** Ese porcentaje describe las filas de Registros bajo las reglas implementadas. También debe revisarse el resumen y las limitaciones.
- **¿Cuánto tiempo ahorra?** Todavía no está medido. Los segundos del motor excluyen carga, revisión humana e IA.
- **¿Usa información del trabajo?** No. Es un escenario y una base completamente sintéticos.
