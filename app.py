
import streamlit as st
import pandas as pd

from pathlib import Path

from visualizacoes.mapas import criar_mapa_neural

from visualizacoes.graficos import (
    grafico_indicador,
    media_por_neuronio
)


PASTA = Path(__file__).parent

ARQUIVO = PASTA / "dados" / "resultados_som.csv"


st.set_page_config(
    page_title="SOM-BRASIL",
    page_icon="🧠",
    layout="wide"
)


st.title("🧠 SOM-BRASIL")

st.subheader(
    "Mapa socioeconômico dos municípios brasileiros"
)

st.write(
    "Rede neural artificial baseada em "
    "aprendizado não supervisionado."
)


if not ARQUIVO.exists():

    st.warning(
        "Ainda não existem resultados de treinamento. "
        "Execute treinamento.py após completar os indicadores."
    )

    st.stop()


df = pd.read_csv(
    ARQUIVO,
    dtype={"id_municipio": str}
)


# Indicadores disponíveis
indicadores = [
    "pib_per_capita",
    "idhm",
    "renda_per_capita",
    "educacao",
    "saude",
    "populacao"
]

st.sidebar.header("Filtros")

ufs = ["Todos"] + sorted(
    df["uf"].dropna().unique().tolist()
)

uf_selecionada = st.sidebar.selectbox(
    "Selecione o estado",
    ufs
)

if uf_selecionada != "Todos":

    df = df[df["uf"] == uf_selecionada]


indicador = st.sidebar.selectbox(
    "Indicador para visualizar",
    indicadores
)


# Indicadores gerais
col1, col2, col3 = st.columns(3)

col1.metric(
    "Municípios analisados",
    len(df)
)

col2.metric(
    "Neurônios disponíveis",
    100
)

col3.metric(
    "Estados presentes",
    df["uf"].nunique()
)


st.divider()

st.header("Mapa de organização neural")

st.plotly_chart(
    criar_mapa_neural(df),
    use_container_width=True
)


st.header("Distribuição dos indicadores")

st.plotly_chart(
    grafico_indicador(df, indicador),
    use_container_width=True
)


st.header("Médias por neurônio")

st.plotly_chart(
    media_por_neuronio(df, indicador),
    use_container_width=True
)


st.header("Municípios classificados")

st.dataframe(
    df,
    use_container_width=True
)
