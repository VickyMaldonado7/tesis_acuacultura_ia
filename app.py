import streamlit as st
import pandas as pd
import joblib

from datetime import datetime
import os

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

#def generar_recomendacion(row):

#    desviaciones = {}

#    if row["TAN"] > 1:
#        desviaciones["TAN"] = row["TAN"] / 1

#    if row["NH3T"] > 0.1:
#        desviaciones["NH3T"] = row["NH3T"] / 0.1

#    if row["NO2"] > 0.66:
#        desviaciones["NO2"] = row["NO2"] / 0.66

#    if row["NO3"] > 3.1:
#        desviaciones["NO3"] = row["NO3"] / 3.1

#    if row["PO4"] > 0.3:
#        desviaciones["PO4"] = row["PO4"] / 0.3

#    if row["SULFURO"] > 0.1:
#        desviaciones["SULFURO"] = row["SULFURO"] / 0.1

#    if row["ALK"] < 200:
#        desviaciones["ALK"] = 200 / max(row["ALK"], 1)

#    if row["PH"] < 7.8 or row["PH"] > 8.2:
#        desviaciones["PH"] = abs(row["PH"] - 8)

#    if row["TEMP"] < 28 or row["TEMP"] > 32:
#        desviaciones["TEMP"] = abs(row["TEMP"] - 30)

#    if row["R_NP"] != 20:
#        desviaciones["R_NP"] = abs(row["R_NP"] - 20)

#    if len(desviaciones) == 0:
#        return "Todos los parámetros dentro de rangos óptimos."

#    peor = max(desviaciones, key=desviaciones.get)

#    recomendaciones = {
#        "TAN": "Reducir carga orgánica, aplicar biorremediación y evaluar alimentación.",
#        "NH3T": "Aumentar recambio de agua y mejorar aireación.",
#        "NO2": "Aplicar bacterias nitrificantes.",
#        "NO3": "Controlar acumulación de nutrientes.",
#        "PO4": "Reducir fosfatos mediante manejo de alimentación.",
#        "SULFURO": "Mejorar oxigenación del fondo.",
#        "ALK": "Aplicar carbonatos para estabilizar alcalinidad.",
#        "PH": "Ajustar pH gradualmente.",
#        "TEMP": "Monitorear temperatura.",
#        "R_NP": "Corregir balance nutricional N:P."
#    }

#    return recomendaciones.get(peor, "Revisar condiciones generales.")

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

    # TAN
    if tan >= 1:
        alertas.append({
            "parametro": "TAN",
            "severidad": 5,
            "mensaje": "Por encima del rango aceptable",
            "recomendacion": "Reducir carga orgánica, aplicar biorremediación al suelo y evaluar alimentación.",
            "direccion": "↑"
        })

    # NH3T
    if nh3 >= 0.1:
        alertas.append({
            "parametro": "NH3T",
            "severidad": 5,
            "mensaje": "Por encima del rango aceptable",
            "recomendacion": "Aumentar recambio de agua y mejorar aireación.",
            "direccion": "↑"
        })

    # NO2
    if no2 >= 0.66:
        alertas.append({
            "parametro": "NO2",
            "severidad": 4,
            "mensaje": "Por encima del rango aceptable",
            "recomendacion": "Aplicar bacterias nitrificantes al agua.",
            "direccion": "↑"
        })

    # NO3
    if no3 >= 3.1:
        alertas.append({
            "parametro": "NO3",
            "severidad": 3,
            "mensaje": "Por encima del rango aceptable",
            "recomendacion": "Aplicar biorrmediacion al agua para controlar acumulación de nutrientes.",
            "direccion": "↑"
        })

    # PO4
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
            background-color:{color};
            padding:18px;
            border-radius:10px;
            color:black;
            font-size:20px;
            font-weight:bold;
            margin-top:20px;
            margin-bottom:20px;">
            {icono} Nivel de riesgo: {pred} ({confianza:.1f}%)
        </div>
        """,
        unsafe_allow_html=True
    )

#    if pred == "ALTO":
#        st.error(f"🔴 Nivel de riesgo: {pred} ({confianza:.1f}%)")
#    elif pred == "MEDIO":
#        st.warning(f"🟡 Nivel de riesgo: {pred} ({confianza:.1f}%)")
#    else:
#        st.success(f"🟢 Nivel de riesgo: {pred} ({confianza:.1f}%)")

#    st.subheader("Variables críticas")

#    if variables_criticas:
#        st.write(", ".join(variables_criticas))
#    else:
#        st.success("No se detectaron variables críticas relevantes.")

#    clases = modelo.classes_

#    st.subheader("Confianza del modelo")

#    for clase, prob in zip(clases, probabilidades):
#        st.write(f"{clase}: {prob*100:.1f}%")

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

