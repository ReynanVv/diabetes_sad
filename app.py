import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

paises_disponiveis = [
    "Algeria", "Argentina", "Australia", "Bangladesh", "Brazil", "Canada", "Chile", "China", "Colombia",
    "Costa_Rica", "Ecuador", "Egypt", "El_Salvador", "Eswatini", "Ethiopia", "European_Union", "Guatemala",
    "India", "Indonesia", "Iran", "Iraq", "Japan", "Kazakhstan", "Korea_South", "Malaysia", "Mauritius",
    "Mexico", "Morocco", "Nicaragua", "Nigeria", "Other", "Pakistan", "Peru", "Philippines", "Russia",
    "Saudi_Arabia", "Somalia", "South_Africa", "Sudan", "Thailand", "Turkey", "Ukraine", "United_Arab_Emirates",
    "United_Kingdom", "United_States", "Vietnam", "Yemen", "Zimbabwe"
]

st.markdown("""
    <style>
        .main, .stApp {
            background-color: #f0f4f7;
            color: #ffffff;
        }

        h1, h2, h3, h4, h5, h6, label, div {
            color: #2c3e50 !important;
        }

        /* Selectbox - campo */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #3d9970 !important;
            border-radius: 8px;
        }

        .stSelectbox div[data-baseweb="select"]:hover {
            background-color: #368a65 !important;
        }

        /* Selectbox - opções do dropdown */
        div[data-baseweb="menu"] > div > div {
            color: white !important;
            background-color: #3d9970 !important;
        }

        div[data-baseweb="menu"] > div > div:hover {
            background-color: #368a65 !important;
        }

        .stButton>button {
            background-color: #3d9970;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            border-color: #3d9970;
            padding: 0.6em 1.2em;
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #368a65;
        }

        .block-container {
            padding: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("🩺 SAD - Sistema de Apoio à Decisão para Previsão de Diabetes")

st.markdown("---")
st.subheader("📋 Insira os dados do paciente")

# Inputs organizados em colunas
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("Nº Gravidez", min_value=0)
    blood_pressure = st.number_input("Pressão Sanguínea", min_value=0)
    insulin = st.number_input("Insulina", min_value=0)
    dpf = st.number_input("Função de histórico familiar (DPF)", min_value=0.0)
    pais = st.selectbox("País", sorted(paises_disponiveis))

with col2:
    glucose = st.number_input("Glicose", min_value=0)
    skin_thickness = st.number_input("Espessura da Pele", min_value=0)
    bmi = st.number_input("IMC", min_value=0.0)
    age = st.number_input("Idade", min_value=0)

st.markdown("---")

# Carrega o modelo
with open('models/diabetes_model.pkl', 'rb') as f:
    model = pickle.load(f)

if st.button("🔍 Prever"):
    # Verificação de campos obrigatórios (exceto gravidez)
    if any([
        glucose == 0,
        blood_pressure == 0,
        skin_thickness == 0,
        insulin == 0,
        bmi == 0.0,
        dpf == 0.0,
        age == 0
    ]):
        st.warning("⚠️ Por favor, preencha todos os campos com valores maiores que zero (exceto Nº Gravidez).")
    else:
        input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                                insulin, bmi, dpf, age]])
        
        prediction = model.predict(input_data)[0]
        proba = model.predict_proba(input_data)[0][1]  # probabilidade de ter diabetes

        resultado = "TEM diabetes" if prediction == 1 else "NÃO tem diabetes"
        confianca = proba if prediction == 1 else (1 - proba)

        if prediction == 1:
            st.error(f"🚨 O paciente provavelmente TEM diabetes.\n\n📊 Confiança da previsão: **{confianca * 100:.2f}%**")
        else:
            st.success(f"✅ O paciente provavelmente NÃO tem diabetes.\n\n📊 Confiança da previsão: **{confianca * 100:.2f}%**")

        # Salvar no arquivo predicoes.csv
        nova_pred = pd.DataFrame([{
            "Gravidezes": pregnancies,
            "Glicose": glucose,
            "Pressão": blood_pressure,
            "Pele": skin_thickness,
            "Insulina": insulin,
            "IMC": bmi,
            "DPF": dpf,
            "Idade": age,
            "Resultado": resultado,
            "Confiança (%)": round(confianca * 100, 2),
        }])

        if os.path.exists("data/predicoes.csv"):
            nova_pred.to_csv("data/predicoes.csv", mode='a', header=False, index=False)
        else:
            nova_pred.to_csv("data/predicoes.csv", index=False)

        # Salvar no arquivo diabetes.csv com Outcome
        nova_linha_diabetes = pd.DataFrame([{
            "Pregnancies": pregnancies,
            "Glucose": glucose,
            "BloodPressure": blood_pressure,
            "SkinThickness": skin_thickness,
            "Insulin": insulin,
            "BMI": bmi,
            "DiabetesPedigreeFunction": dpf,
            "Age": age,
            "Outcome": int(prediction),
            "Country": pais
        }])

        if os.path.exists("data/diabetes.csv"):
            nova_linha_diabetes.to_csv("data/diabetes.csv", mode='a', header=False, index=False)
        else:
            nova_linha_diabetes.to_csv("data/diabetes.csv", index=False)

        st.info("📁 Dados salvos com sucesso.")
