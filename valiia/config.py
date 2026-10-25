from datetime import date
from itertools import product

AVISO = "DEMOSTRACIÓN ACADÉMICA — DATOS TOTALMENTE FICTICIOS"
INICIO, CORTE = date(2026, 1, 1), date(2026, 3, 31)
SEMILLA = 20260331
PERIODOS = ["2026-01", "2026-02", "2026-03"]
CATALOGOS = {
    "especie": ["Canino", "Felino"],
    "tipo_actividad": ["Valoración", "Orientación", "Seguimiento"],
    "zona": ["Zona A", "Zona B", "Zona C"],
    "responsable_id": ["RESP-001", "RESP-002", "RESP-003", "RESP-004"],
    "seguimiento_requerido": ["Sí", "No"],
}
COLUMNAS = ["id_registro", "id_animal", "fecha_actividad", "especie", "tipo_actividad", "zona", "responsable_id", "edad_meses", "seguimiento_requerido", "fecha_seguimiento", "observaciones"]
OBLIGATORIOS = COLUMNAS[:9]
RESUMEN = ["periodo", "especie", "tipo_actividad", "total_reportado"]
ESQUEMA = {"Registros": COLUMNAS, "Resumen_mensual": RESUMEN,
           "Catalogos": ["campo", "valor_permitido"],
           "Diccionario": ["hoja", "campo", "tipo", "obligatorio", "valores_permitidos", "puede_estar_vacio"]}
COMBINACIONES = list(product(PERIODOS, CATALOGOS["especie"], CATALOGOS["tipo_actividad"]))
HALLAZGOS = ["hallazgo_id", "regla", "codigo", "gravedad", "archivo", "hoja", "fila_excel", "combinacion", "id_registro", "campo", "valor_observado", "explicacion", "accion_sugerida"]
REGLAS = [
 ("R01", "Campos obligatorios", "Error", "Un hallazgo por campo ausente. No se duplica como R03, R04 o R05."),
 ("R02", "ID de actividad duplicado", "Error", "Se señalan todas las filas del ID repetido. id_animal puede repetirse."),
 ("R03", "Categorías permitidas", "Error", "Coincidencia exacta con Catalogos, verificados contra la versión 1.0."),
 ("R04", "Fecha de actividad", "Error", "Fecha válida entre 2026-01-01 y 2026-03-31, inclusive."),
 ("R05", "Edad en meses", "Error", "Entero entre 0 y 300. Se aceptan números escritos como texto, sin redondearlos."),
 ("R06", "Seguimiento", "Error / Información / Advertencia", "Pendiente sin fecha es información. Fecha informada debe ser coherente; orden no evaluable genera advertencia."),
 ("R07", "Conciliación de actividades", "Error / Advertencia", "Diferencia es error con registros fiables; advertencia si hay errores en Registros. No se compara una combinación de resumen inválida."),
 ("R08", "Estructura del resumen", "Error", "18 combinaciones únicas, válidas y completas. Total entero no negativo."),
]
