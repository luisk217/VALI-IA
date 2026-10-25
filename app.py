from pathlib import Path
import hashlib
import pandas as pd
import streamlit as st
from valiia.config import AVISO, REGLAS
from valiia.validator import validar
from valiia.reporting import export_excel, ai_package, automatic_summary, PROMPT

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title="Vali-IA · Revisión de registros",page_icon="✓",layout="wide")
st.markdown("""<style>
/* Vali-IA · Diseño nocturno. Solo presentación, sin alterar las reglas. */
:root {
  --v-bg: #090f1d;
  --v-panel: #111d30;
  --v-line: #26364e;
  --v-text: #e8eef8;
  --v-muted: #a9b9cf;
  --v-accent: #58dfd1;
}
.stApp {
  background: radial-gradient(ellipse at 90% 0%, rgba(40,92,138,.16), transparent 48%), var(--v-bg);
  color: var(--v-text);
}
.block-container {max-width:1450px;padding-top:2.2rem;padding-bottom:3rem;}
[data-testid='stHeader'] {background:rgba(9,15,29,.94);}
h1,h2,h3 {color:var(--v-text);letter-spacing:-.025em;}
h2 {font-size:1.65rem;}
h3 {font-size:1.15rem;}
[data-testid='stCaptionContainer'] {color:var(--v-muted);font-size:.875rem;line-height:1.55;}
hr {border-color:var(--v-line);}
a {color:#81c6ff;}
.v-heading {display:flex;align-items:center;gap:1rem;margin:.9rem 0 1.5rem;animation:v-enter .45s ease-out both;}
.v-monogram {
  width:60px;height:60px;flex:0 0 60px;display:grid;place-items:center;
  border:1px solid #337d88;border-radius:18px;color:#81f2e5;
  background:linear-gradient(140deg,#173e50,#142541);font-size:1.8rem;font-weight:750;
  box-shadow:0 0 32px rgba(45,212,191,.09);
}
.v-heading h1 {font-size:2.6rem;line-height:1.15;margin:0;padding:0;font-weight:750;}
.v-heading p {color:var(--v-muted);font-size:1rem;margin:.4rem 0 0;}
.v-eyebrow {color:var(--v-accent);font-size:.78rem;font-weight:650;letter-spacing:.12em;margin-bottom:.4rem;}
.v-context {display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 1.5rem;}
.v-context span {font-size:.85rem;color:#bacce1;padding:.4rem .75rem;border:1px solid var(--v-line);border-radius:7px;background:#0e192b;}
.notice {font-size:.75rem;line-height:1.5;letter-spacing:.035em;color:#96aac5;padding-bottom:.8rem;border-bottom:1px solid #243148;}
[data-testid='stSidebar'] {background:#0d1626;border-right:1px solid #233249;}
[data-testid='stSidebar'] h3 {color:#eff4fd;font-size:1.15rem;}
[data-testid='stSidebar'] [data-testid='stSidebarContent'] {background:linear-gradient(180deg,#111e33 0%,#0d1626 55%);}
[data-testid='stWidgetLabel'] p {font-size:.9rem;font-weight:550;color:#dbe5f3;}
[data-baseweb='select'] > div {
  background:#131f33;border-color:#304460;border-radius:10px;
  transition:border-color .18s ease,box-shadow .18s ease;
}
[data-baseweb='select']:focus-within > div {border-color:#57d8cc;box-shadow:0 0 0 2px rgba(87,216,204,.14);}
[data-baseweb='input'],[data-baseweb='textarea'] {border-radius:10px;}
[data-testid='stFileUploaderDropzone'] {background:#111f33;border:1px dashed #466380;border-radius:14px;padding:1.1rem;}
[data-testid='stFileUploaderDropzone']:hover {border-color:#58dfd1;background:#15273d;}
[data-testid='stButton'] button,[data-testid='stDownloadButton'] button,
[data-testid='stFileUploaderDropzone'] button {
  min-height:44px;border-radius:11px;border:1px solid #39516d;
  color:#e8f0fb;background:#15243a;font-weight:600;
  transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease,background .18s ease;
}
[data-testid='stButton'] button:hover:not(:disabled),
[data-testid='stDownloadButton'] button:hover:not(:disabled),
[data-testid='stFileUploaderDropzone'] button:hover:not(:disabled) {
  transform:translateY(-2px);border-color:#58dfd1;background:#1c324b;
  box-shadow:0 6px 20px rgba(0,0,0,.2);
}
[data-testid='stButton'] button:active:not(:disabled),[data-testid='stDownloadButton'] button:active:not(:disabled) {transform:translateY(0);}
[data-testid='stButton'] button[kind='primary'],[data-testid='stDownloadButton'] button[kind='primary'] {
  background:linear-gradient(110deg,#176b86,#2852b3);border:1px solid #388bac;color:#fff;
  box-shadow:0 4px 18px rgba(26,106,158,.17);
}
[data-testid='stButton'] button[kind='primary']:hover:not(:disabled),
[data-testid='stDownloadButton'] button[kind='primary']:hover:not(:disabled) {
  background:linear-gradient(110deg,#197c95,#3061cd);border-color:#7ae3db;
  box-shadow:0 6px 24px rgba(39,142,169,.23);
}
[data-testid='stButton'] button:disabled {opacity:.45;cursor:not-allowed;}
button:focus-visible,[role='tab']:focus-visible,summary:focus-visible {
  outline:2px solid #81f2e5 !important;outline-offset:3px;
}
[data-testid='stMetric'] {
  position:relative;overflow:hidden;min-height:135px;height:100%;
  border:1px solid #2a3e58;border-radius:16px;padding:1.2rem 1.3rem;
  background:linear-gradient(130deg,#16273e,#101b2d);
  box-shadow:0 8px 24px rgba(0,0,0,.13);
  animation:v-enter .45s ease-out both;
  transition:transform .2s ease,border-color .2s ease;
}
[data-testid='stMetric']::before {
  content:'';position:absolute;inset:0 0 auto;height:2px;
  background:linear-gradient(90deg,#52d8ca,rgba(68,136,234,.65),transparent);
}
[data-testid='stMetric']:hover {transform:translateY(-3px);border-color:#4c708e;}
[data-testid='stMetricLabel'] p {color:#b3c4db;font-size:.88rem;white-space:normal;}
[data-testid='stMetricValue'] {color:#f2f7ff;font-size:2.15rem;font-weight:650;letter-spacing:-.035em;}
[data-baseweb='tab-list'] {
  gap:.5rem;background:#101c2e;border:1px solid #26394f;border-radius:13px;
  padding:.4rem;margin:1rem 0 .5rem;
}
[data-baseweb='tab'] {
  min-height:44px;height:auto;border-radius:9px;padding:.65rem 1rem;
  color:#b3c4da;white-space:normal;transition:background .2s ease,color .2s ease;
}
[data-baseweb='tab']:hover {background:#182c43;color:#edf7ff;}
[data-baseweb='tab'][aria-selected='true'] {background:#1c364b;color:#82f0e2;}
[data-baseweb='tab-highlight'],[data-baseweb='tab-border'] {background:transparent;}
[data-testid='stAlert'] {border:1px solid rgba(137,164,194,.2);border-radius:12px;}
[data-testid='stExpander'] {border:1px solid #293e56;border-radius:12px;background:#101d30;}
[data-testid='stExpander'] details {border-color:#293e56;border-radius:12px;}
[data-testid='stDataFrame'] {border:1px solid #293e56;border-radius:12px;overflow:hidden;}
[data-testid='stCode'],[data-testid='stText'] {border:1px solid #273b53;border-radius:12px;background:#0c1727;padding:.8rem;}
.v-empty-grid {display:grid;grid-template-columns:1.35fr 1fr;gap:1rem;margin-top:1rem;}
.v-empty-card {
  border:1px solid #293c55;border-radius:16px;padding:1.4rem 1.5rem;
  background:linear-gradient(145deg,#14243a,#101a2b);animation:v-enter .45s ease-out both;
}
.v-empty-card h3 {font-size:1.08rem;margin:0 0 .7rem;padding:0;}
.v-empty-card p {color:#b5c6dc;font-size:.95rem;line-height:1.7;margin:.5rem 0;}
.v-empty-card strong {color:#e1edf9;font-weight:600;}
.v-empty-card .v-kicker {color:#6eddd3;font-size:.78rem;letter-spacing:.06em;font-weight:600;margin-bottom:.8rem;}
@keyframes v-enter {from {opacity:0;transform:translateY(8px);}to {opacity:1;transform:translateY(0);}}
@media(max-width:760px) {
  .block-container {padding:1.2rem 1rem 2rem;}
  .v-heading h1 {font-size:2.1rem;}
  .v-monogram {width:48px;height:48px;flex-basis:48px;border-radius:14px;}
  .v-empty-grid {grid-template-columns:1fr;}
  [data-baseweb='tab-list'] {gap:0;padding:.2rem;}
  [data-baseweb='tab'] {padding:.5rem;font-size:.85rem;}
  [data-testid='stMetric'] {min-height:110px;padding:1rem;}
}
@media(prefers-reduced-motion:reduce) {
  .v-heading,.v-empty-card,[data-testid='stMetric'] {animation:none;}
  [data-testid='stMetric'],[data-baseweb='tab'],[data-baseweb='select'] > div,
  [data-testid='stButton'] button,[data-testid='stDownloadButton'] button,
  [data-testid='stFileUploaderDropzone'] button {transition:none;}
  [data-testid='stMetric']:hover,[data-testid='stButton'] button:hover,
  [data-testid='stDownloadButton'] button:hover,[data-testid='stFileUploaderDropzone'] button:hover {transform:none;}
}
</style>""",unsafe_allow_html=True)
st.markdown(f'<div class="notice">{AVISO}</div>',unsafe_allow_html=True)
st.markdown('''<div class="v-heading">
<div class="v-monogram" aria-hidden="true">V</div>
<div><div class="v-eyebrow">CALIDAD DE DATOS</div><h1>Vali-IA</h1>
<p>Revisa tus registros antes del informe mensual.</p></div></div>
<div class="v-context"><span>Centro Demostrativo Huellas</span>
<span>Enero — marzo 2026</span><span>Corte: 31 de marzo</span></div>''',unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Archivo de trabajo")
    source=st.radio("Origen",["Bases de demostración","Cargar Excel"])
    data=None
    filename=""
    if source=="Bases de demostración":
        options={"Con errores conocidos":"base_con_errores.xlsx","Base correcta":"base_correcta.xlsx","Excepciones válidas":"base_excepciones_validas.xlsx"}
        selection=st.selectbox("Elige una base",list(options))
        filename=options[selection]
        file=ROOT/"datos"/filename
        if file.exists():
            data=file.read_bytes()
            st.download_button("Descargar base seleccionada",data,file_name=filename,mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.error("Faltan las bases. Ejecuta python generar_datos.py en la carpeta del proyecto.")
    else:
        uploaded=st.file_uploader("Archivo .xlsx ficticio",type=["xlsx"])
        st.caption("Hasta 5 MB. Usa la estructura de las bases, con cabeceras en la fila 3.")
        if uploaded is not None:
            data,filename=uploaded.getvalue(),uploaded.name
    clicked=st.button("Validar información",type="primary",disabled=data is None,width="stretch")
    st.divider()
    st.caption("8 reglas · Revisión reproducible\n\nTus archivos originales no se modifican.")
    with st.expander("Consultar reglas"):
        for code,name,severity,criterion in REGLAS:
            st.markdown(f"**{code} · {name}**\n\n{criterion}")

fingerprint=(filename,hashlib.sha256(data).hexdigest()) if data is not None else None
if st.session_state.get("fingerprint") != fingerprint:
    st.session_state.pop("result",None)
if clicked and data is not None:
    with st.spinner("Revisando estructura, registros y totales…"):
        st.session_state.result=validar(data,filename)
        st.session_state.fingerprint=fingerprint
        st.session_state.excel=export_excel(st.session_state.result)
        st.session_state.ai_zip=ai_package(st.session_state.result)

if "result" not in st.session_state:
    st.info("Selecciona una base o carga un Excel ficticio y pulsa Validar información.")
    st.markdown('''<div class="v-empty-grid">
<section class="v-empty-card"><div class="v-kicker">REVISIÓN DE REGISTROS</div>
<h3>¿Qué se revisa?</h3><p>Campos obligatorios, identificadores duplicados, categorías, fechas, edades, seguimientos y totales mensuales.</p>
<p>Cada alerta explica dónde está el problema y qué debes verificar.</p></section>
<section class="v-empty-card"><div class="v-kicker">BASES DISPONIBLES</div><h3>Tres casos para practicar</h3>
<p><strong>Con errores</strong> · Encontrar inconsistencias<br>
<strong>Correcta</strong> · Conciliar los totales<br>
<strong>Excepciones</strong> · Distinguir pendientes válidos</p></section></div>''',unsafe_allow_html=True)
    st.stop()

r=st.session_state.result
m=r["metricas"]
if not r["estructura_valida"]:
    st.error("No se completó la validación. Revisa los problemas de estructura indicados abajo.")
elif r["listo_para_informe"]:
    st.success("La base cumple las reglas implementadas. Los pendientes informativos, si existen, siguen abiertos.")
else:
    st.warning("Requiere revisión antes del informe. Consulta los hallazgos y los totales provisionales.")
cols=st.columns(4)
for col,label,value in zip(cols,["Registros revisados","Registros con error","Registros sin errores","Alertas de error"],
                          [m["registros_revisados"],m["registros_con_error"],f"{m['porcentaje_sin_errores']}%" if m['porcentaje_sin_errores'] is not None else None,m["alertas_error"]]):
    col.metric(label,"No evaluable" if value is None else value)
st.caption(f"{m['alertas_advertencia']} advertencias · {m['alertas_informacion']} informativas · {r['segundos_procesamiento']:.3f} s de procesamiento. Un registro puede tener varias alertas. El porcentaje solo considera la hoja Registros.")
tabs=st.tabs(["Hallazgos","Conciliación de indicadores","Informe e IA"])
with tabs[0]:
    st.subheader("Lista de revisión")
    findings=pd.DataFrame(r["hallazgos"])
    if findings.empty:
        st.success("No se encontraron hallazgos.")
    else:
        c1,c2=st.columns(2)
        severity=c1.multiselect("Gravedad",["error","advertencia","información"],default=["error","advertencia","información"])
        rules=c2.multiselect("Regla",sorted(findings.regla.unique()),default=sorted(findings.regla.unique()))
        filtered=findings[findings.gravedad.isin(severity)&findings.regla.isin(rules)]
        st.caption(f"Se muestran {len(filtered)} de {len(findings)} alertas. Las descargas conservan todos los hallazgos.")
        st.dataframe(filtered,width="stretch",hide_index=True,height=370)
        if not filtered.empty:
            hid=st.selectbox("Ver un hallazgo completo",filtered.hallazgo_id)
            item=filtered[filtered.hallazgo_id==hid].iloc[0]
            st.markdown(f"**{item['regla']} · {item['gravedad'].capitalize()} · {item['hoja']} · fila {item['fila_excel'] if pd.notna(item['fila_excel']) else 'sin fila; combinación ausente'}**")
            st.write(item["explicacion"])
            st.write("Acción sugerida: "+item["accion_sugerida"])
with tabs[1]:
    st.subheader("Actividades por mes, especie y tipo")
    st.caption("Se cuentan actividades, no animales únicos. Diferencia = reportado − recuento de filas agrupables. Un valor vacío significa no comparable.")
    if r["conciliacion"]:
        st.dataframe(pd.DataFrame(r["conciliacion"]),hide_index=True,width="stretch",height=430)
    else:
        st.info("Sin conciliación: resuelve primero la estructura del archivo.")
    with st.expander("Cómo se interpretan los totales"):
        st.write("Se cuentan todas las filas con fecha, especie y actividad válidas, incluidos duplicados y filas con otros errores. Si hay algún error en Registros, todas las comparaciones se marcan provisionales. No se decide qué fila eliminar. Una combinación de resumen ausente, duplicada o inválida no se compara.")
    if r["no_agrupables"]:
        st.warning(f"{len(r['no_agrupables'])} registros no pueden asignarse a una combinación. No se han descartado silenciosamente.")
        st.dataframe(pd.DataFrame(r["no_agrupables"]),hide_index=True,width="stretch")
with tabs[2]:
    st.subheader("Explicar los resultados con IA")
    st.write("1. Descarga y extrae el paquete para IA. 2. Adjunta el JSON en tu asistente y copia el prompt. 3. Comprueba las cifras y referencias del borrador.")
    st.info("La transferencia es manual. Esta aplicación no llama a una API ni envía archivos a un modelo.")
    st.download_button("Descargar paquete para IA",st.session_state.ai_zip,"paquete_para_IA.zip","application/zip")
    with st.expander("Ver prompt reutilizable"):
        st.code(PROMPT,language=None)
    st.subheader("Resumen automático por reglas")
    st.caption("Este texto usa una plantilla. No es una respuesta generada por IA.")
    st.text(automatic_summary(r))
st.divider()
st.download_button("Descargar reporte completo en Excel",st.session_state.excel,"reporte_validacion.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",type="primary")
st.caption("Las propuestas requieren revisión humana. Cumplir las reglas no comprueba que una actividad haya ocurrido.")
