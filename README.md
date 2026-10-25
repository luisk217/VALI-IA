# Vali-IA: verificador de indicadores y registros

**DEMOSTRACIÓN ACADÉMICA — DATOS TOTALMENTE FICTICIOS**

Prototipo local del Centro Demostrativo Huellas para el proyecto del curso sinergIA. Revisa 200 actividades ficticias de enero a marzo de 2026, con corte fijo del 31 de marzo. No utiliza datos, archivos ni procesos de una organización real.

## Inicio rápido en Windows

1. Descarga el ZIP y usa **Extraer todo**. Conserva juntas las carpetas y los archivos. Puedes usar `C:\Vali-IA`; evita ejecutarlo desde dentro del ZIP.
2. Instala Python 3.12 desde [python.org](https://www.python.org/downloads/windows/), si no lo tienes. En el instalador habilita **Add python.exe to PATH**.
3. Abre la carpeta que contiene `app.py`. Haz clic en la barra de direcciones del Explorador, escribe `cmd` y pulsa Enter. Se abrirá una terminal en esa carpeta.
4. Ejecuta estos comandos, uno por uno:

```bat
py -3.12 --version
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

El primer comando comprueba Python; el segundo crea un entorno aislado; el tercero instala las tres bibliotecas requeridas y sus dependencias; el cuarto abre la aplicación. La instalación inicial necesita internet. Después la validación local no necesita una API ni conexión a una organización.

Si no se reconoce `py` pero sí `python`, comprueba `python --version` y usa `python -m venv .venv` con Python 3.12. Los otros comandos no cambian. No necesitas activar el entorno ni cambiar políticas de PowerShell.

5. Abre [http://localhost:8501](http://localhost:8501) si el navegador no se abre solo. Mantén la terminal abierta mientras uses Vali-IA. Para cerrar la aplicación, vuelve a la terminal y pulsa **Ctrl+C**.
6. La próxima vez basta ejecutar `iniciar_windows.bat` o repetir el último comando en la misma carpeta.

**Qué debería pasar:** selecciona **Con errores conocidos** y pulsa **Validar información**. Debes ver 200 registros, 18 con error, 91 % sin errores, 24 alertas de error, 3 advertencias y 1 informativa.

## Usar la aplicación

- **Bases de demostración:** elige una de las tres bases. Puedes descargarla para abrirla en Excel.
- **Cargar Excel:** utiliza un archivo ficticio con las cuatro hojas y las cabeceras de la plantilla. Cabeceras en fila 3 y primer registro en fila 4. No cambies esos renglones.
- **Hallazgos:** filtra por regla y gravedad. Selecciona un hallazgo para leer su explicación completa. Las descargas siempre incluyen todo, aunque haya filtros activos.
- **Conciliación de indicadores:** revisa actividades por mes, especie y tipo. Diferencia = total reportado menos recuento de filas agrupables.
- **Informe e IA:** descarga el paquete, extráelo, adjunta el JSON a tu asistente de IA y pega el prompt. Revisa las cifras antes de usar el borrador.
- **Descargar reporte completo en Excel:** obtiene métricas, hallazgos, conciliación y filas no agrupables. No modifica el Excel original.

Al cambiar de archivo se limpian los resultados anteriores. Pulsa de nuevo **Validar información**.

## Las tres bases

| Archivo | Resultado esperado |
|---|---|
| `datos/base_correcta.xlsx` | 200 registros; sin alertas; 18 combinaciones conciliadas, incluida una con cero actividades. |
| `datos/base_con_errores.xlsx` | 18 registros afectados; 24 alertas de error, 3 advertencias y 1 pendiente informativo. |
| `datos/base_excepciones_validas.xlsx` | Sin errores ni advertencias; 3 seguimientos pendientes informativos. |

Las tres contienen actividades repetidas de un mismo animal con identificadores de actividad distintos. Eso es válido. La semilla de generación es `20260331`.

## Qué significa cada resultado

**Número de alertas:** total de hallazgos individuales. Incluye los problemas del resumen. **Registros con error:** número de filas distintas de la hoja Registros con al menos un error. No incluye filas del resumen ni pendientes informativos. **Porcentaje sin errores:** `(registros revisados − registros con error) / registros revisados × 100`. No es una probabilidad de veracidad ni una calificación de todo el libro.

Las 24 alertas de error de la base alterada se distribuyen en 18 alertas de Registros y 6 del resumen. Hay 3 diferencias provisionales de totales y 1 pendiente informativo, para un total de 28 hallazgos. Los 27 hallazgos de error/advertencia se comparan con el archivo independiente de resultados esperados. El informativo se comprueba por separado.

**Conciliación:** se cuentan todas las filas con fecha, especie y actividad válidas. Los duplicados se incluyen en el recuento provisional: no se elimina ni escoge una fila automáticamente. Las filas agrupables con otros errores también se cuentan. Las no agrupables aparecen en una tabla independiente, con su ubicación. En la base alterada: 196 agrupables + 4 no agrupables = 200 revisadas.

Si cualquier registro tiene un error R01–R06, todos los recuentos se consideran provisionales. Una diferencia R07 pasa a advertencia, porque aún no puede concluirse que el total reportado esté equivocado. Si Registros no tiene errores, una diferencia es error. Una combinación ausente, duplicada o con total inválido en el resumen se muestra como **No comparable**, aunque exista un recuento de filas. No se convierte un vacío en cero.

## Reglas y decisiones de alcance

Consulta `docs/diccionario_y_reglas.xlsx` y `docs/decisiones.md`. E00 identifica bloqueos técnicos de estructura antes de R01–R08. No es una novena regla de negocio.

- Categorías exactas y catálogos cerrados para la versión 1.0. Editar el catálogo no permite aprobar nuevas categorías accidentalmente.
- Fechas Excel o texto `AAAA-MM-DD` / `DD/MM/AAAA`. No se interpreta un número cualquiera como fecha.
- Edad entera de 0 a 300; se acepta texto numérico sin decimales reales. Los vacíos obligatorios producen R01, evitando errores repetidos R03–R05 por el mismo vacío.
- Seguimiento `Sí` sin fecha: información. No existe plazo ficticio que permita declararlo atrasado.
- Solo entradas con valores, sin fórmulas. Los archivos protegidos o dañados se rechazan con mensaje. Máximo 5 MB, 10.000 filas y 50 columnas por hoja.
- Una base sin filas no obtiene 100 %: el porcentaje se indica como no evaluable.

## Inteligencia artificial: transferencia manual

La aplicación valida con Python; sus cálculos son deterministas. El **resumen automático por reglas** usa una plantilla y se etiqueta como tal.

Para demostrar la parte generativa:

1. Descarga `paquete_para_IA.zip` desde la aplicación.
2. Extrae el ZIP. Adjunta `resultados_validacion.json` en un asistente de IA al que tengas acceso.
3. Copia el texto completo de `prompt_para_IA.txt` como instrucción.
4. Comprueba que el borrador conserva las cifras, identifica los totales provisionales y cita las referencias H001, H002, etc.
5. Revisa y aprueba tú el texto. No autorices cambios automáticos en los registros.

Se incluye `docs/ejemplo_borrador_IA.md`: ejemplo redactado por el asistente de IA durante la construcción del proyecto, a partir del JSON exportado. No demuestra una llamada automática desde la aplicación. Ese archivo de ejemplo queda fijo; si cambias la base, genera otro borrador.

## Pruebas y reproducibilidad

```bat
.venv\Scripts\python.exe generar_datos.py
.venv\Scripts\python.exe ejecutar_pruebas.py
```

El primer comando **recrea** los archivos de demostración y sus respuestas esperadas. Conserva cualquier copia que hayas editado con otro nombre antes de ejecutarlo. El segundo prueba el sistema y **actualiza** las evidencias de ejecución. No ejecuta una IA ni modifica entradas.

Las pruebas realmente ejecutadas están en `evidencias/pruebas_ejecutadas.txt` y `evidencias/resultados_pruebas.json`. Se comparan hallazgos por regla, subtipo, gravedad, hoja, fila, campo y combinación. El validador nunca lee el archivo de errores esperados; el generador construye ese archivo a partir de mutaciones controladas y un registro independiente de diferencias.

Se probaron 19 casos, incluyendo el flujo de la interfaz mediante AppTest, filtros, cambio de base, lectura, validación y exportaciones. Los resultados son específicos del conjunto de prueba, no una garantía universal. Se probó en Linux con Python 3.12.14, pandas 2.2.3, openpyxl 3.1.5 y Streamlit 1.50.0. **No se ejecutó en Windows ni se completó una prueba visual del navegador o una carga manual desde su selector**. La vista previa de Sites disponible no ejecuta este entorno Python. Sigue pendiente esa comprobación en tu equipo.

## Medir si ahorra trabajo

Abre `docs/medicion_piloto.xlsx`. Mide la revisión manual y, en una ejecución comparable, preparación + procesamiento + revisión humana + uso de IA. Anota todo en minutos; convierte segundos dividiendo por 60. No uses solo los segundos del motor como tiempo asistido total.

`Tiempo asistido total = preparación + procesamiento + revisión humana + IA`. `Diferencia = manual − asistido`. `Ahorro % = diferencia / manual × 100`, solo si el tiempo manual es positivo. No hay tiempos manuales ni ahorros inventados. Para reducir el efecto de conocer las respuestas, usa un segundo revisor o alterna el orden y documenta esa limitación.

## Entregables

| Ubicación | Contenido |
|---|---|
| `app.py`, `valiia/` | Interfaz, reglas y exportación, separadas por responsabilidad. |
| `requirements.txt`, `iniciar_windows.bat` | Dependencias y acceso local. |
| `generar_datos.py`, `datos/` | Bases reproducibles, catálogo, diccionario y oráculo independiente. |
| `tests/`, `ejecutar_pruebas.py` | Pruebas ejecutables y comparación con lo esperado. |
| `evidencias/` | Pruebas reales, reporte Excel, JSON, paquete para IA y resumen por reglas. |
| `docs/` | Reglas, decisiones, prompt, ejemplo de IA, guion de cinco minutos, avance y medición. |

## Problemas frecuentes

**No encuentra `app.py`:** la terminal debe estar en la carpeta extraída que contiene ese archivo. **No instala dependencias:** revisa internet y permisos de instalación; no se requieren permisos institucionales en la aplicación. **El puerto está ocupado:** cierra tu otra sesión o ejecuta `... -m streamlit run app.py --server.port 8502` y abre el puerto indicado. **El archivo no tiene las columnas esperadas:** usa la plantilla y conserva cabeceras en la fila 3. **Cambiaste un dato y no cambia el reporte:** guarda el Excel, cárgalo nuevamente y pulsa Validar. **El catálogo modificado se rechaza:** la versión 1.0 tiene catálogos fijos; su ampliación requiere modificar y probar las reglas.

## Documentación técnica pública consultada

- [Lectura de Excel con pandas](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)
- [Descargas en Streamlit](https://docs.streamlit.io/develop/api-reference/widgets/st.download_button)
- [AppTest de Streamlit](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest)

El prototipo fija versiones para reproducir la demostración. No afirma usar las versiones más recientes.
