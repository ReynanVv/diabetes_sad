import streamlit as st
import pandas as pd
import os


# Título
st.title("📦 Importação de Dados em Lote para o Dataset de Diabetes")

st.markdown("""
Envie um arquivo `.csv` contendo os dados já prontos, **incluindo a coluna `Outcome`** com valores `0` (não tem diabetes) ou `1` (tem diabetes).
""")

st.markdown("### 📌 Estrutura esperada do CSV:")

colunas_esperadas = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Country", "Outcome"
]

st.markdown("**Colunas obrigatórias:**")
st.code(", ".join(colunas_esperadas), language="csv")

# Exemplo de estrutura
exemplo = pd.DataFrame([{
    "Pregnancies": 2,
    "Glucose": 120,
    "BloodPressure": 70,
    "SkinThickness": 25,
    "Insulin": 100,
    "BMI": 28.5,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 32,
    "Country": "Brazil",
    "Outcome": 1
}])

st.markdown("**Exemplo de linha válida:**")
st.dataframe(exemplo)

st.markdown("---")

# Upload do arquivo
arquivo = st.file_uploader("📁 Enviar arquivo CSV com dados prontos", type=["csv"])

if arquivo is not None:
    try:
        df = pd.read_csv(arquivo)

        if not all(col in df.columns for col in colunas_esperadas):
            st.error("❌ O CSV deve conter as colunas: " + ", ".join(colunas_esperadas))
        else:
            st.success("✅ Arquivo carregado com sucesso!")
            st.dataframe(df.head())

            caminho_dataset = "datasets/diabetes.csv"
            if os.path.exists(caminho_dataset):
                df.to_csv(caminho_dataset, mode="a", header=False, index=False)
            else:
                df.to_csv(caminho_dataset, index=False)

            st.success("🗃️ Dados adicionados ao dataset com sucesso!")

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
