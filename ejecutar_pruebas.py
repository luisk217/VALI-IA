"""Ejecuta pruebas reales y guarda evidencia; termina con error si hay una falla."""
from collections import Counter
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import platform
import sys
import unittest
import pandas, openpyxl, streamlit
from valiia.config import AVISO
from valiia.validator import validar
from valiia.reporting import export_excel, ai_package, json_bytes, automatic_summary, PROMPT

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"evidencias"
OUT.mkdir(exist_ok=True)
stream=io.StringIO()
suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"))
runner=unittest.TextTestRunner(stream=stream,verbosity=2)
result=runner.run(suite)
log=stream.getvalue()
print(log)
(OUT/"pruebas_ejecutadas.txt").write_text(AVISO+"\n"+log,encoding="utf-8")
keys=["regla","codigo","gravedad","hoja","fila_excel","campo","combinacion"]
make_key=lambda f:tuple(f.get(k) for k in keys)
expected=json.loads((ROOT/"datos"/"errores_esperados.json").read_text(encoding="utf-8"))
cases=[]
for name in ["base_correcta.xlsx","base_con_errores.xlsx","base_excepciones_validas.xlsx"]:
    r=validar((ROOT/"datos"/name).read_bytes(),name)
    cases.append({"archivo":name,**r["metricas"],"segundos_procesamiento":r["segundos_procesamiento"]})
    if name=="base_con_errores.xlsx":
        expected_keys=Counter(make_key(f) for f in expected["hallazgos_esperados"])
        actual_keys=Counter(make_key(f) for f in r["hallazgos"] if f["gravedad"]!="información")
        evaluation={"aciertos":sum((actual_keys&expected_keys).values()),"omitidos":sum((expected_keys-actual_keys).values()),
                    "falsas_alertas":sum((actual_keys-expected_keys).values()),"alcance":"Errores y advertencias; información se prueba aparte.",
                    "errores_esperados":sum(f["gravedad"]=="error" for f in expected["hallazgos_esperados"]),
                    "advertencias_esperadas":sum(f["gravedad"]=="advertencia" for f in expected["hallazgos_esperados"])}
        (OUT/"reporte_validacion.xlsx").write_bytes(export_excel(r))
        (OUT/"paquete_para_IA.zip").write_bytes(ai_package(r))
        (OUT/"resultados_validacion.json").write_bytes(json_bytes(r))
        (OUT/"resumen_por_reglas.txt").write_text(automatic_summary(r),encoding="utf-8")
meta={"aviso":AVISO,"fecha_ejecucion_utc":datetime.now(timezone.utc).isoformat(),
      "entorno":{"sistema":platform.system(),"python":platform.python_version(),"pandas":pandas.__version__,"openpyxl":openpyxl.__version__,"streamlit":streamlit.__version__},
      "pruebas_ejecutadas":result.testsRun,"fallas":len(result.failures),"errores_de_ejecucion":len(result.errors),
      "exitoso":result.wasSuccessful(),"comparacion_oraculo":evaluation,"bases":cases,
      "limites":"Tiempos de una ejecución local, incluyen lectura y validación. Excluyen exportación, revisión humana e IA. No se mide ahorro manual ni rendimiento institucional."}
(OUT/"resultados_pruebas.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
(ROOT/"docs"/"prompt_para_IA.txt").write_text(PROMPT,encoding="utf-8")
print(json.dumps(meta,ensure_ascii=False,indent=2))
sys.exit(0 if result.wasSuccessful() else 1)
