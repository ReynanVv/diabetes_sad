import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.markdown("""
    <style>
        .main, .stApp {
            background-color: #f0f4f7;
            color: #2c3e50;
        }
        h1, h2, h3, h4, h5, h6, label, div {
            color: #2c3e50 !important;
        }
        .stButton>button {
            background-color: #3d9970;
            color: white;
            font-weight: bold;
            border-radius: 8px;
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

st.title("📊 Dashboard - Previsões Realizadas")

if os.path.exists("data/predicoes.csv"):
    df = pd.read_csv("data/predicoes.csv")

    positivos = df[df["Resultado"] == "TEM diabetes"].shape[0]
    negativos = df[df["Resultado"] == "NÃO tem diabetes"].shape[0]

    st.subheader("Distribuição de Casos")
    labels = ["TEM diabetes", "NÃO tem diabetes"]
    values = [positivos, negativos]

    pie_fig = px.pie(
        names=labels,
        values=values,
        color=labels,
        color_discrete_map={
            "TEM diabetes": "#e74c3c",
            "NÃO tem diabetes": "#2ecc71"
        },
    )
    st.plotly_chart(pie_fig, use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("Casos com risco de diabetes", positivos)
    col2.metric("Casos saudáveis", negativos)

    # Análise cruzada entre açúcar e diabetes
    if os.path.exists("data/diabetes.csv") and os.path.exists("data/sugar.csv"):
        diabetes_df = pd.read_csv("data/diabetes.csv")
        sugar_df = pd.read_csv("data/sugar.csv")

        diabetes_summary = diabetes_df.groupby("Country")["Outcome"].mean().reset_index()
        diabetes_summary.columns = ["Country", "DiabetesRate"]

        sugar_filtered = sugar_df[sugar_df["Action"].isin(["consumption", "production"])]
        sugar_melted = sugar_filtered.melt(id_vars=["Name", "Action"], var_name="Year", value_name="Value")
        sugar_melted["Value"] = sugar_melted["Value"].astype(str).str.replace(",", "").astype(float)
        sugar_avg = sugar_melted.groupby(["Name", "Action"])["Value"].mean().reset_index()
        sugar_pivot = sugar_avg.pivot(index="Name", columns="Action", values="Value").reset_index()
        sugar_pivot.columns.name = None
        sugar_pivot = sugar_pivot.rename(columns={"Name": "Country"})

        merged = pd.merge(diabetes_summary, sugar_pivot, on="Country")

        st.subheader("📊 Correlação entre Diabetes e Açúcar")

        corr_consumo = merged["DiabetesRate"].corr(merged["consumption"]) if "consumption" in merged else None
        corr_producao = merged["DiabetesRate"].corr(merged["production"]) if "production" in merged else None

        col1, col2 = st.columns(2)
        if corr_consumo is not None:
            col1.metric("Correlação (consumo x diabetes)", f"{corr_consumo:.2f}")
        if corr_producao is not None:
            col2.metric("Correlação (produção x diabetes)", f"{corr_producao:.2f}")

        if "consumption" in merged.columns:
            fig1 = px.scatter(
                merged,
                x="consumption",
                y="DiabetesRate",
                text="Country",
                labels={
                    "consumption": "Consumo médio de açúcar (mil toneladas)",
                    "DiabetesRate": "Taxa de Diabetes"
                },
                title="Consumo de Açúcar vs. Taxa de Diabetes",
                trendline="ols"
            )
            fig1.update_traces(textposition='top center')
            st.plotly_chart(fig1, use_container_width=True)

        if "production" in merged.columns:
            fig2 = px.scatter(
                merged,
                x="production",
                y="DiabetesRate",
                text="Country",
                labels={
                    "production": "Produção média de açúcar (mil toneladas)",
                    "DiabetesRate": "Taxa de Diabetes"
                },
                title="Produção de Açúcar vs. Taxa de Diabetes",
                trendline="ols"
            )
            fig2.update_traces(textposition='top center')
            st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("Nenhuma previsão realizada ainda.")
