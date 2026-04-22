import streamlit as st
import pandas as pd
import joblib

modelo = joblib.load("modelo_rf.pkl")

st.set_page_config(page_title="Asistente Técnico Acuícola IA", layout="wide")

st.title("Asistente Técnico Acuícola basado en IA")
st.markdown(
    "Ingrese los parámetros de calidad de agua para estimar el nivel de riesgo sanitario."
)

col1, col2 = st.columns(2)

with col1:
tan = st.number_input("TAN")
nh3 = st.number_input("NH3")
no2 = st.number_input("NO2")
no3 = st.number_input("NO3")
po4 = st.number_input("PO4")
sulfuro = st.number_input("Sulfuro")

with col2:
alk = st.number_input("Alcalinidad")
ph = st.number_input("pH")
temp = st.number_input("Temperatura")
salinidad = st.number_input("Salinidad")
r_np = st.number_input("Relación N:P")

st.markdown("")

if st.button("Predecir riesgo"):
    data = pd.DataFrame([[tan, nh3, no2, no3, po4, sulfuro, alk, ph, temp, salinidad, r_np]],
                        columns=["TAN","NH3T","NO2","NO3","PO4","SULFURO","ALK","PH","TEMP","SALINIDAD","R_NP"])

    pred = modelo.predict(data)[0]

if pred == "ALTO":
    st.error(f"⚠️ Nivel de riesgo: {pred}")
    st.error("Recomendación: revisar amonio y considerar recambio de agua inmediato.")

elif pred == "MEDIO":
    st.warning(f"⚠️ Nivel de riesgo: {pred}")
    st.warning("Recomendación: monitorear parámetros críticos.")

else:
    st.success(f"✅ Nivel de riesgo: {pred}")
    st.success("Condiciones estables.")
