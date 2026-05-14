import streamlit as st
import pandas as pd
import joblib

from datetime import datetime
import os

st.markdown("""
<style>

/* Botón principal */
div.stButton > button:first-child {
    background-color: #00B894;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

/* Hover */
div.stButton > button:first-child:hover {
    background-color: #019875;
    color: white;
    transform: scale(1.02);
}

/* Botón secundario */
div.stButton > button[kind="secondary"] {
    background-color: #0984E3;
    color: white;
}

</style>
""", unsafe_allow_html=True)

def validar_inputs(tan, nh3, no2, no3, po4, sulfuro, alk, ph, temp, salinidad, r_np):
    errores = []

    if tan < 0 or tan > 15:
        errores.append(f"TAN = {tan} fuera de rango (0 - 15)")

    if nh3 < 0 or nh3 > 1:
        errores.append(f"NH3T = {nh3} fuera de rango (0 - 1)")

    if no2 < 0 or no2 > 20:
        errores.append(f"NO2 = {no2} fuera de rango (0 - 20)")

    if no3 < 0 or no3 > 20:
        errores.append(f"NO3 = {no3} fuera de rango (0 - 20)")

    if po4 < 0 or po4 > 20:
        errores.append(f"PO4 = {po4} fuera de rango (0 - 20)")

    if sulfuro < 0 or sulfuro > 5:
        errores.append(f"SULFURO = {sulfuro} fuera de rango (0 - 5)")

    if alk < 0 or alk > 800:
        errores.append(f"ALK = {alk} fuera de rango (0 - 800)")

    if ph < 4 or ph > 11:
        errores.append(f"pH = {ph} fuera de rango (4 - 11)")

    if temp < 5 or temp > 50:
        errores.append(f"TEMP = {temp} fuera de rango (5 - 50 °C)")

    if salinidad < 0 or salinidad > 50:
        errores.append(f"SALINIDAD = {salinidad} fuera de rango (0 - 50)")

    if r_np < 0 or r_np > 40:
        errores.append(f"Relación N:P = {r_np} fuera de rango (0 - 40)")

    return errores

modelo = joblib.load("modelo_rf.pkl")

st.set_page_config(page_title="Asistente Técnico Acuícola IA", layout="wide")

st.title("Asistente Técnico Acuícola basado en IA")
st.markdown(
    "Ingrese los parámetros de calidad de agua para estimar el nivel de riesgo sanitario."
)

col_inputs, col_img = st.columns([2, 1])

with col_inputs:
    col1, col2 = st.columns(2)

    with col1:
        tan = st.number_input("TAN", format="%.3f")
        nh3 = st.number_input("NH3", format="%.3f")
        no2 = st.number_input("NO2", format="%.3f")
        no3 = st.number_input("NO3", format="%.3f")
        po4 = st.number_input("PO4", format="%.3f")
        sulfuro = st.number_input("Sulfuro", format="%.3f")
        alk = st.number_input("Alcalinidad", format="%.2f")

    with col2:
        ph = st.number_input("pH", format="%.2f")
        temp = st.number_input("Temperatura", format="%.2f")
        salinidad = st.number_input("Salinidad", format="%.2f")
        r_np = st.number_input("Relación N:P", format="%.2f")

with col_img:
    st.image("assets/Infografia_camaron.png", use_container_width=True)

st.markdown("")

def generar_recomendaciones(tan, nh3, no2, no3, po4, sulfuro, alk, ph, temp, salinidad, r_np, pred):
    alertas = []

    # TAN - NITROGENO AMONIACAL TOTAL
    if tan >= 1:
        alertas.append({
            "parametro": "TAN",
            "severidad": 5,
            "mensaje": "Por encima del rango aceptable",
            "recomendacion": "Reducir carga orgánica, aplicar biorremediación al suelo y evaluar alimentación.",
            "direccion": "↑"
        })

    # NH3T - AMONIO TOXICO
    if nh3 >= 0.1:
        alertas.append({
            "parametro": "NH3T",
            "severidad": 5,
            "mensaje": "Por encima del rango aceptable",
            "recomendacion": "Aumentar recambio de agua y mejorar aireación.",
            "direccion": "↑"
        })

    # NO2 - NITRITO
    if no2 >= 0.66:
        alertas.append({
            "parametro": "NO2",
            "severidad": 4,
            "mensaje": "Por encima del rango aceptable",
            "recomendacion": "Aplicar bacterias nitrificantes al agua.",
            "direccion": "↑"
        })

    # NO3 - NITRATO
    if no3 >= 3.1:
        alertas.append({
            "parametro": "NO3",
            "severidad": 3,
            "mensaje": "Por encima del rango aceptable",
            "recomendacion": "Aplicar biorrmediacion al agua para controlar acumulación de nutrientes.",
            "direccion": "↑"
        })

    # PO4 - FOSFATO
    if po4 >= 0.3:
        alertas.append({
            "parametro": "PO4",
            "severidad": 4,
            "mensaje": "Por encima del rango aceptable",
            "recomendacion": "Aplicar bacterias al agua para reducir fosfatos.",
            "direccion": "↑"
        })

    # Sulfuro
    if sulfuro >= 0.1:
        alertas.append({
            "parametro": "SULFURO",
            "severidad": 5,
            "mensaje": "Por encima del rango aceptable",
            "recomendacion": "Mejorar oxigenación del fondo.",
            "direccion": "↑"
        })

    # Alcalinidad
    if alk <= 200:
        alertas.append({
            "parametro": "ALK",
            "severidad": 3,
            "mensaje": "Por debajo del rango aceptable",
            "recomendacion": "Aplicar carbonatos para estabilizar alcalinidad.",
            "direccion": "↓"
        })

    # pH
    if ph < 7.8:
        alertas.append({
            "parametro": "pH",
            "severidad": 2,
            "mensaje": "Por debajo del rango informativo ideal",
            "recomendacion": "Monitorear estabilidad del sistema y revisar alcalinidad.",
            "direccion": "↓"
        })
    elif ph > 8.2:
        alertas.append({
            "parametro": "pH",
            "severidad": 3,
            "mensaje": "Por encima del rango informativo ideal",
            "recomendacion": "Monitorear riesgo de mayor toxicidad del amonio y revisar manejo de fitoplancton.",
            "direccion": "↑"
        })

    # Temperatura
    if temp < 28:
        alertas.append({
            "parametro": "TEMP",
            "severidad": 2,
            "mensaje": "Por debajo del rango ideal",
            "recomendacion": "Considerar menor actividad metabólica y ajustar expectativas de consumo y crecimiento.",
            "direccion": "↓"
        })
    elif temp > 32:
        alertas.append({
            "parametro": "TEMP",
            "severidad": 4,
            "mensaje": "Por encima del rango ideal",
            "recomendacion": "Fertilizar para oscurecer el agua y conservar temperatura baja en el fondo.",
            "direccion": "↑"
        })

    # Salinidad
    if salinidad <= 2:
        alertas.append({
            "parametro": "SALINIDAD",
            "severidad": 2,
            "mensaje": "Muy baja",
            "recomendacion": "En agua dulce o baja salinidad, revisar balance iónico, especialmente calcio, magnesio y potasio.",
            "direccion": "↓"
        })

    # Relación N:P
    if r_np < 20:
        alertas.append({
            "parametro": "R_NP",
            "severidad": 4,
            "mensaje": "Por debajo del ideal",
            "recomendacion": "Revisar exceso relativo de fosfato y priorizar acciones para mejorar el balance nitrógeno:fósforo.",
            "direccion": "↓"
        })

    # Ordenar por severidad
    alertas_ordenadas = sorted(alertas, key=lambda x: x["severidad"], reverse=True)

    # Mostrar máximo 3 alertas principales
    alertas_principales = alertas_ordenadas[:3]

    # Recomendación general según predicción del modelo
    if pred == "ALTO":
        recomendacion_general = "Activar revisión técnica prioritaria, validar mediciones críticas y definir acción correctiva inmediata."
    elif pred == "MEDIO":
        recomendacion_general = "Mantener monitoreo cercano y corregir los parámetros fuera de rango antes de que el riesgo escale."
    else:
        recomendacion_general = "Mantener seguimiento rutinario y registrar evolución de parámetros."

    return alertas_principales, recomendacion_general

# Guardar registros nuevos
def guardar_caso(data, pred, confianza, recomendacion_general, alertas_principales):
    archivo = "data/historial_predicciones.csv"

    if os.path.exists(archivo):
        historial = pd.read_csv(archivo)
        numero_caso = len(historial) + 1
    else:
        numero_caso = 1

    registro = data.copy()
    registro["ID_CASO"] = numero_caso
    registro["PREDICCION_NRS"] = pred
    registro["CONFIANZA_MODELO"] = round(confianza, 2)
    registro["RECOMENDACION_GENERAL"] = recomendacion_general
    registro["ALERTAS_PRINCIPALES"] = "; ".join(
        [f"{a['parametro']} {a['direccion']}: {a['mensaje']}" for a in alertas_principales]
    )
    registro["FECHA_REGISTRO"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(archivo):
        registro.to_csv(archivo, mode="a", header=False, index=False)
    else:
        registro.to_csv(archivo, index=False)

    return numero_caso

# Muestra las barras de parametros para una lectura rapida
def mostrar_barra_parametro(nombre, valor, minimo, maximo, limite_ideal, unidad=""):

    porcentaje = max(0, min(1, valor / maximo))
    porcentaje_visual = porcentaje * 100
    limite_visual = (limite_ideal / maximo) * 100

    if valor <= limite_ideal * 0.8:
        color = "#22c55e"
    elif valor <= limite_ideal:
        color = "#f0b429"
    else:
        color = "#ff4b4b"

    html = f"""
<div style="margin-bottom:18px;">
<div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:5px;">
<strong>{nombre}</strong>
<span>{valor:.3f} {unidad}</span>
</div>

<div style="position:relative; background-color:#e5e7eb; border-radius:10px; height:14px; overflow:hidden;">
<div style="width:{porcentaje_visual}%; background-color:{color}; height:14px; border-radius:10px;"></div>
<div style="position:absolute; left:{limite_visual}%; top:0; width:3px; height:14px; background-color:white;"></div>
</div>
</div>
"""

    st.markdown(html, unsafe_allow_html=True)

if st.button("Predecir riesgo"):

    errores = validar_inputs(tan, nh3, no2, no3, po4, sulfuro, alk, ph, temp, salinidad, r_np)

    if errores:
        st.error("⚠️ Se detectaron valores inconsistentes. Verifique el/los siguientes parámetros:")
        for error in errores:
            st.write(f"• {error}")
        st.info("💡 Estos valores son poco probables en condiciones reales o pueden indicar error de medición.")
        st.stop()

    data = pd.DataFrame(
        [[tan, nh3, no2, no3, po4, sulfuro, alk, ph, temp, salinidad, r_np]],
        columns=["TAN", "NH3T", "NO2", "NO3", "PO4", "SULFURO", "ALK", "PH", "TEMP", "SALINIDAD", "R_NP"]
    )

    pred = modelo.predict(data)[0]

    probabilidades = modelo.predict_proba(data)[0]

    confianza = max(probabilidades) * 100

    alertas_principales, recomendacion_general = generar_recomendaciones(
        tan, nh3, no2, no3, po4, sulfuro, alk, ph, temp, salinidad, r_np, pred
    )

    st.session_state["data"] = data
    st.session_state["pred"] = pred
    st.session_state["confianza"] = confianza
    st.session_state["recomendacion_general"] = recomendacion_general
    st.session_state["alertas_principales"] = alertas_principales

    variables_criticas = []

    for alerta in alertas_principales:
        parametro = alerta["parametro"]
        direccion = alerta["direccion"]

        variables_criticas.append(f"{parametro} {direccion}")
    
    if pred == "ALTO":
        color = "#ff4b4b"
        icono = "🔴"
    elif pred == "MEDIO":
        color = "#f5c542"
        icono = "🟡"
    else:
        color = "#2ecc71"
        icono = "🟢"

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color}, #111827);
            padding: 28px;
            border-radius: 18px;
            color: white;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.25);
            margin-top: 25px;
            margin-bottom: 28px;
            font-family: Arial, sans-serif;
        ">
            <span style="font-size: 46px; font-weight: 800;">
                {icono} RIESGO {pred}
            </span>
            <br>
            <span style="font-size: 22px; font-weight: 500;">
                Confianza del modelo: {confianza:.1f}%
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Muestra los parametros en barras
    st.subheader("Lectura rápida de parámetros")

    col_bar1, col_bar2 = st.columns(2)

    with col_bar1:

        mostrar_barra_parametro("TAN", tan, 0, 2, 1, "mg/L")
        mostrar_barra_parametro("NH3", nh3, 0, 0.2, 0.1, "mg/L")
        mostrar_barra_parametro("NO2", no2, 0, 1, 0.5, "mg/L")
        mostrar_barra_parametro("NO3", no3, 0, 5, 3.1, "mg/L")
        mostrar_barra_parametro("PO4", po4, 0, 1.5, 0.3, "mg/L")

    with col_bar2:

        mostrar_barra_parametro("Sulfuro", sulfuro, 0, 0.2, 0.1, "mg/L")
        mostrar_barra_parametro("Alcalinidad", alk, 0, 400, 200, "mg/L")
        mostrar_barra_parametro("pH", ph, 0, 14, 8.5, "")
        mostrar_barra_parametro("Temperatura", temp, 0, 40, 32, "°C")
        mostrar_barra_parametro("Relación N:P", r_np, 0, 20, 10, "")

    st.subheader("Recomendación general")
    st.write(recomendacion_general)

    st.subheader("Alertas principales")

    if alertas_principales:
        for alerta in alertas_principales:
            st.warning(f"**{alerta['parametro']} {alerta['direccion']}**: {alerta['mensaje']}")
            st.write(f"Recomendación: {alerta['recomendacion']}")
    else:
        st.success("No se detectaron desviaciones relevantes en los parámetros ingresados.")

if st.button("Guardar caso"):
    if "data" in st.session_state:
        numero_caso = guardar_caso(
            st.session_state["data"],
            st.session_state["pred"],
            st.session_state["confianza"],
            st.session_state["recomendacion_general"],
            st.session_state["alertas_principales"]
        )
        st.success(f"Caso #{numero_caso:03d} guardado correctamente para futuro reentrenamiento.")
    else:
        st.warning("Primero debe ejecutar una predicción antes de guardar el caso.")

