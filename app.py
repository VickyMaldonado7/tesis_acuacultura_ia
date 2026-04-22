import streamlit as st
import pandas as pd
import joblib

modelo = joblib.load("modelo_rf.pkl")

st.title("Asistente Acuícola IA")

st.write("Ingrese parámetros:")

tan = st.number_input("TAN")
nh3 = st.number_input("NH3")
no2 = st.number_input("NO2")
no3 = st.number_input("NO3")
po4 = st.number_input("PO4")
sulfuro = st.number_input("Sulfuro")
alk = st.number_input("Alcalinidad")
ph = st.number_input("pH")
temp = st.number_input("Temperatura")
salinidad = st.number_input("Salinidad")
r_np = st.number_input("Relación N:P")

if st.button("Predecir"):
    data = pd.DataFrame([[tan, nh3, no2, no3, po4, sulfuro, alk, ph, temp, salinidad, r_np]],
                        columns=["TAN","NH3T","NO2","NO3","PO4","SULFURO","ALK","PH","TEMP","SALINIDAD","R_NP"])

    pred = modelo.predict(data)[0]

    st.success(f"Nivel de riesgo: {pred}")