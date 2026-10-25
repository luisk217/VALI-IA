"""Generación reproducible; el oráculo se construye de las mutaciones, nunca del validador."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path
import json
import random
from valiia.config import *
from valiia.excel import workbook_bytes

ROOT = Path(__file__).resolve().parent

def dictionary():
    descriptions = {
        "id_registro": ("Texto", "Identificador artificial de actividad, único"),
        "id_animal": ("Texto", "Código ANI-0001, etc. Puede repetirse en actividades distintas"),
        "fecha_actividad": ("Fecha", "Fecha Excel o texto AAAA-MM-DD / DD/MM/AAAA. 2026-01-01 a 2026-03-31"),
        "edad_meses": ("Entero", "0 a 300; se admite texto numérico exacto, sin redondeo"),
        "fecha_seguimiento": ("Fecha", "Fecha válida, igual o posterior a actividad y hasta 2026-03-31"),
        "observaciones": ("Texto", "Nota sintética opcional; no se interpreta como instrucciones"),
        "periodo": ("Texto", "2026-01, 2026-02, 2026-03"),
        "total_reportado": ("Entero", "Número de actividades registradas, entero no negativo. Nunca animales únicos"),
    }
    rows = []
    for sheet, cols in [("Registros", COLUMNAS), ("Resumen_mensual", RESUMEN)]:
        for field in cols:
            kind, allowed = descriptions.get(field, ("Texto", ", ".join(CATALOGOS.get(field, []))))
            optional = sheet == "Registros" and field in ("fecha_seguimiento", "observaciones")
            empty = "No"
            if field == "fecha_seguimiento":
                empty = "Sí: No = no aplica; Sí = pendiente informativo, sin plazo de incumplimiento definido"
            elif field == "observaciones":
                empty = "Sí: nota opcional"
            rows.append([sheet, field, kind, "No" if optional else "Sí", allowed, empty])
    return rows

def build_data():
    rng = random.Random(SEMILLA)
    records=[]
    for i in range(200):
        # Consistent species per artificial animal. Repeated animals are intentional.
        animal=i % 80 + 1
        dt=datetime(2026,1,1)+timedelta(days=rng.randrange(90))
        species="Canino" if animal % 2 else "Felino"
        activity=CATALOGOS["tipo_actividad"][rng.randrange(3)]
        # A genuine zero combination is kept in the monthly summary.
        if dt.month==3 and species=="Felino" and activity=="Seguimiento":
            activity="Orientación"
        required="Sí" if i % 3==0 else "No"
        follow=min(dt+timedelta(days=3),datetime(2026,3,31)) if required=="Sí" else None
        records.append(dict(zip(COLUMNAS,[f"ACT-{i+1:04}",f"ANI-{animal:04}",dt,species,activity,
                         rng.choice(CATALOGOS["zona"]),rng.choice(CATALOGOS["responsable_id"]),
                         12+animal*2,required,follow,"Actividad ficticia para práctica académica."])))
    totals=Counter((r["fecha_actividad"].strftime("%Y-%m"),r["especie"],r["tipo_actividad"]) for r in records)
    summary=[dict(zip(RESUMEN,[*k,totals[k]])) for k in COMBINACIONES]
    catalog=[[k,v] for k,values in CATALOGOS.items() for v in values]
    def sheets(reg, summ):
        return {"Registros":(COLUMNAS,[[r[c] for c in COLUMNAS] for r in reg]),
                "Resumen_mensual":(RESUMEN,[[r[c] for c in RESUMEN] for r in summ]),
                "Catalogos":(ESQUEMA["Catalogos"],catalog),"Diccionario":(ESQUEMA["Diccionario"],dictionary())}
    correct=sheets(records,summary)
    bad, badsum=deepcopy(records),deepcopy(summary)
    oracle=[]
    def expect(rule,code,row,field,explanation,severity="error",sheet="Registros",key=""):
        oracle.append({"regla":rule,"codigo":code,"gravedad":severity,"hoja":sheet,"fila_excel":row,
                       "campo":field,"combinacion":key,"explicacion":explanation})
    def change(index, field, value, rule, code, explanation):
        bad[index][field]=value
        expect(rule,code,index+4,field,explanation)
    change(0,"responsable_id",None,"R01","obligatorio","Responsable obligatorio eliminado.")
    change(1,"id_registro",bad[2]["id_registro"],"R02","duplicado","ID de fila 6 copiado en fila 5.")
    expect("R02","duplicado",6,"id_registro","Segunda fila del ID repetido.")
    change(3,"zona","Zona Z","R03","categoria","Zona ajena al catálogo.")
    # Remove follow-ups as a separate valid pending where a malformed activity is seeded.
    for i in [4,5,6]:
        bad[i]["seguimiento_requerido"]="No"
        bad[i]["fecha_seguimiento"]=None
    change(4,"fecha_actividad","2026-02-30","R04","fecha_actividad","Fecha imposible.")
    change(5,"fecha_actividad",datetime(2026,4,1),"R04","fecha_actividad","Actividad posterior al periodo.")
    change(6,"edad_meses",-1,"R05","edad","Edad negativa.")
    change(7,"edad_meses",2.5,"R05","edad","Edad decimal.")
    change(8,"edad_meses",301,"R05","edad","Edad sobre 300.")
    change(9,"edad_meses","desconocida","R05","edad","Edad no numérica.")
    bad[10]["seguimiento_requerido"]="Sí"
    change(10,"fecha_seguimiento",bad[10]["fecha_actividad"]-timedelta(days=1),"R06","anterior_actividad","Seguimiento antes de la actividad.")
    bad[11]["seguimiento_requerido"]="Sí"
    change(11,"fecha_seguimiento",datetime(2026,4,2),"R06","posterior_corte","Seguimiento posterior al corte.")
    bad[12]["seguimiento_requerido"]="No"
    change(12,"fecha_seguimiento",bad[12]["fecha_actividad"],"R06","contradiccion","Fecha informada junto a No.")
    bad[13]["seguimiento_requerido"]="Sí"
    change(13,"fecha_seguimiento","sin fecha","R06","fecha_no_valida","Fecha no interpretable.")
    change(14,"especie","Ave","R03","categoria","Especie no permitida.")
    change(15,"id_animal",None,"R01","obligatorio","Código del animal eliminado.")
    change(16,"seguimiento_requerido","Tal vez","R03","categoria","Categoría de seguimiento inválida.")
    change(17,"tipo_actividad","Vacunación","R03","categoria","Actividad no permitida.")
    # Valid pending entry in the error fixture, checked separately from error precision.
    bad[18]["seguimiento_requerido"]="Sí"
    bad[18]["fecha_seguimiento"]=None
    # Summary mutations, with exact expected physical rows.
    badsum[0]["total_reportado"]+=4
    badsum[1]["total_reportado"]=-2
    ktext=lambda k:" / ".join(k)
    expect("R08","total_invalido",5,"total_reportado","Total negativo.",sheet="Resumen_mensual",key=ktext(COMBINACIONES[1]))
    badsum[2]["periodo"]="2026-04"
    expect("R08","clave_invalida",6,"periodo","Periodo no permitido.",sheet="Resumen_mensual",key=ktext(("2026-04",*COMBINACIONES[2][1:])))
    expect("R08","combinacion_ausente",None,"combinacion","Combinación perdida al cambiar el periodo.",sheet="Resumen_mensual",key=ktext(COMBINACIONES[2]))
    badsum.pop(3)
    expect("R08","combinacion_ausente",None,"combinacion","Combinación eliminada deliberadamente.",sheet="Resumen_mensual",key=ktext(COMBINACIONES[3]))
    badsum.append(deepcopy(summary[4]))
    for row in [7,21]:
        expect("R08","combinacion_duplicada",row,"combinacion","Combinación repetida.",sheet="Resumen_mensual",key=ktext(COMBINACIONES[4]))
    # Independent ledger: only these four mutations remove rows from groupable counts.
    delta=Counter()
    for i in [4,5,14,17]:
        old=records[i]
        delta[(old["fecha_actividad"].strftime("%Y-%m"),old["especie"],old["tipo_actividad"])]+=1
    delta[COMBINACIONES[0]]+=4
    invalid_keys=set(COMBINACIONES[1:5])
    for key, diff in delta.items():
        if diff and key not in invalid_keys:
            idx=COMBINACIONES.index(key)
            row=idx+4-(1 if idx>3 else 0)
            expect("R07","diferencia",row,"total_reportado",f"Diferencia provisional esperada de {diff} por el registro de mutaciones.","advertencia","Resumen_mensual",ktext(key))
    exceptions=deepcopy(records)
    for i in [0,1,2]:
        exceptions[i]["seguimiento_requerido"]="Sí"
        exceptions[i]["fecha_seguimiento"]=None
    exceptions[3]["edad_meses"]=0
    exceptions[4]["edad_meses"]=300
    exceptions[5]["observaciones"]=None
    exceptions[6]["fecha_seguimiento"]=exceptions[6]["fecha_actividad"]
    return {"base_correcta.xlsx": correct, "base_con_errores.xlsx": sheets(bad,badsum),
            "base_excepciones_validas.xlsx":sheets(exceptions,summary)}, oracle

def main():
    (ROOT/"datos").mkdir(exist_ok=True)
    books, oracle=build_data()
    for name, content in books.items():
        (ROOT/"datos"/name).write_bytes(workbook_bytes(content))
    manifest={"aviso":AVISO,"semilla":SEMILLA,"base":"base_con_errores.xlsx",
              "criterio":"Coincidencia exacta de regla, codigo, gravedad, hoja, fila_excel, campo y combinacion. Información se evalúa aparte.",
              "hallazgos_esperados":oracle,"informativos_esperados":1}
    (ROOT/"datos"/"errores_esperados.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    cols=list(oracle[0])
    (ROOT/"datos"/"errores_esperados.xlsx").write_bytes(workbook_bytes({"Esperados":(cols,[[r[c] for c in cols] for r in oracle])}))
    (ROOT/"docs"/"diccionario_y_reglas.xlsx").write_bytes(workbook_bytes({"Diccionario":(ESQUEMA["Diccionario"],dictionary()),"Reglas":(["regla","nombre","gravedad","criterio"],REGLAS)}))
    print(f"Generadas tres bases de 200 registros. Oráculo independiente: {len(oracle)} hallazgos de error/advertencia.")

if __name__=="__main__":
    main()
