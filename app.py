import streamlit as st
import pandas as pd
import joblib

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

def generar_recomendacion(row):

    desviaciones = {}

    if row["TAN"] > 1:
        desviaciones["TAN"] = row["TAN"] / 1

    if row["NH3T"] > 0.1:
        desviaciones["NH3T"] = row["NH3T"] / 0.1

    if row["NO2"] > 0.66:
        desviaciones["NO2"] = row["NO2"] / 0.66

    if row["NO3"] > 3.1:
        desviaciones["NO3"] = row["NO3"] / 3.1

    if row["PO4"] > 0.3:
        desviaciones["PO4"] = row["PO4"] / 0.3

    if row["SULFURO"] > 0.1:
        desviaciones["SULFURO"] = row["SULFURO"] / 0.1

    if row["ALK"] < 200:
        desviaciones["ALK"] = 200 / max(row["ALK"], 1)

    if row["PH"] < 7.8 or row["PH"] > 8.2:
        desviaciones["PH"] = abs(row["PH"] - 8)

    if row["TEMP"] < 28 or row["TEMP"] > 32:
        desviaciones["TEMP"] = abs(row["TEMP"] - 30)

    if row["R_NP"] != 20:
        desviaciones["R_NP"] = abs(row["R_NP"] - 20)

    if len(desviaciones) == 0:
        return "Todos los parámetros dentro de rangos óptimos."

    peor = max(desviaciones, key=desviaciones.get)

    recomendaciones = {
        "TAN": "Reducir carga orgánica, aplicar biorremediación y evaluar alimentación.",
        "NH3T": "Aumentar recambio de agua y mejorar aireación.",
        "NO2": "Aplicar bacterias nitrificantes.",
        "NO3": "Controlar acumulación de nutrientes.",
        "PO4": "Reducir fosfatos mediante manejo de alimentación.",
        "SULFURO": "Mejorar oxigenación del fondo.",
        "ALK": "Aplicar carbonatos para estabilizar alcalinidad.",
        "PH": "Ajustar pH gradualmente.",
        "TEMP": "Monitorear temperatura.",
        "R_NP": "Corregir balance nutricional N:P."
    }

    return recomendaciones.get(peor, "Revisar condiciones generales.")

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

    with col2:
        alk = st.number_input("Alcalinidad", format="%.2f")
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
            "mensaje": "TAN por encima del rango aceptable",
            "recomendacion": "Revisar acumulación de materia orgánica y reforzar biorremediación de agua y suelo."
        })

    # NH3T
    if nh3 >= 0.1:
        alertas.append({
            "parametro": "NH3T",
            "severidad": 5,
            "mensaje": "NH3T por encima del rango aceptable",
            "recomendacion": "Priorizar reducción de amonio tóxico; validar medición, mejorar oxigenación y evaluar recambio parcial."
        })

    # NO2
    if no2 >= 0.66:
        alertas.append({
            "parametro": "NO2",
            "severidad": 4,
            "mensaje": "NO2 por encima del rango aceptable",
            "recomendacion": "Revisar proceso de nitrificación y reforzar manejo bacteriano del sistema."
        })

    # NO3
    if no3 >= 3.1:
        alertas.append({
            "parametro": "NO3",
            "severidad": 3,
            "mensaje": "NO3 por encima del rango aceptable",
            "recomendacion": "Monitorear acumulación de nitratos y revisar balance del sistema nitrogenado."
        })

    # PO4
    if po4 >= 0.3:
        alertas.append({
            "parametro": "PO4",
            "severidad": 4,
            "mensaje": "PO4 por encima del rango aceptable",
            "recomendacion": "Revisar carga orgánica, fertilización y balance de nutrientes; priorizar reducción de fosfatos."
        })

    # Sulfuro
    if sulfuro >= 0.1:
        alertas.append({
            "parametro": "SULFURO",
            "severidad": 5,
            "mensaje": "Sulfuro por encima del rango aceptable",
            "recomendacion": "Evaluar condición de fondo, acumulación de lodos y necesidad de tratamiento de suelo."
        })

    # Alcalinidad
    if alk <= 200:
        alertas.append({
            "parametro": "ALK",
            "severidad": 3,
            "mensaje": "Alcalinidad por debajo del rango aceptable",
            "recomendacion": "Corregir alcalinidad para mejorar estabilidad del pH y capacidad buffer del sistema."
        })

    # pH
    if ph < 7.8:
        alertas.append({
            "parametro": "pH",
            "severidad": 2,
            "mensaje": "pH por debajo del rango informativo ideal",
            "recomendacion": "Monitorear estabilidad del sistema y revisar alcalinidad."
        })
    elif ph > 8.2:
        alertas.append({
            "parametro": "pH",
            "severidad": 3,
            "mensaje": "pH por encima del rango informativo ideal",
            "recomendacion": "Monitorear riesgo de mayor toxicidad del amonio y revisar manejo de fitoplancton."
        })

    # Temperatura
    if temp < 28:
        alertas.append({
            "parametro": "TEMP",
            "severidad": 2,
            "mensaje": "Temperatura por debajo del rango ideal",
            "recomendacion": "Considerar menor actividad metabólica y ajustar expectativas de consumo y crecimiento."
        })
    elif temp > 32:
        alertas.append({
            "parametro": "TEMP",
            "severidad": 4,
            "mensaje": "Temperatura por encima del rango ideal",
            "recomendacion": "Incrementar monitoreo de oxígeno, estrés del camarón y riesgo sanitario."
        })

    # Salinidad
    # No se asigna alerta directa porque depende del balance iónico.
    if salinidad <= 2:
        alertas.append({
            "parametro": "SALINIDAD",
            "severidad": 2,
            "mensaje": "Salinidad muy baja",
            "recomendacion": "En agua dulce o baja salinidad, revisar balance iónico, especialmente calcio, magnesio y potasio."
        })

    # Relación N:P
    if r_np < 20:
        alertas.append({
            "parametro": "R_NP",
            "severidad": 4,
            "mensaje": "Relación N:P por debajo del ideal",
            "recomendacion": "Revisar exceso relativo de fosfato y priorizar acciones para mejorar el balance nitrógeno:fósforo."
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

    alertas_principales, recomendacion_general = generar_recomendaciones(
        tan, nh3, no2, no3, po4, sulfuro, alk, ph, temp, salinidad, r_np, pred
    )

    if pred == "ALTO":
        st.error(f"⚠️ Nivel de riesgo: {pred}")
    elif pred == "MEDIO":
        st.warning(f"⚠️ Nivel de riesgo: {pred}")
    else:
        st.success(f"✅ Nivel de riesgo: {pred}")

    st.subheader("Recomendación general")
    st.write(recomendacion_general)

    st.subheader("Alertas principales")

    if alertas_principales:
        for alerta in alertas_principales:
            st.warning(f"**{alerta['parametro']}**: {alerta['mensaje']}")
            st.write(f"Recomendación: {alerta['recomendacion']}")
    else:
        st.success("No se detectaron desviaciones relevantes en los parámetros ingresados.")

