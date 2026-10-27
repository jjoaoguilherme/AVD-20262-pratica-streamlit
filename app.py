from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Medidas dos pinguins", page_icon="🐧", layout="wide")

MEDIDAS = {
    "bill_length_mm": "Comprimento do bico (mm)",
    "bill_depth_mm": "Profundidade do bico (mm)",
    "flipper_length_mm": "Comprimento da nadadeira (mm)",
    "body_mass_g": "Massa corporal (g)",
}
ESPECIES = {"Adelie": "Adélie", "Chinstrap": "Chinstrap", "Gentoo": "Gentoo"}


@st.cache_data
def carregar_dados():
    caminho = Path(__file__).resolve().parent / "data" / "clean" / "penguins.csv"
    return pd.read_csv(caminho)


st.title("As medidas dos pinguins")
st.caption("Arquipélago Palmer, 2007–2009 · Correlação e distribuição das medidas físicas")

try:
    df = carregar_dados()
except (FileNotFoundError, pd.errors.EmptyDataError):
    st.error("Não foi possível abrir a base tratada. Execute o notebook da EDA para gerá-la.")
    st.stop()

if df.empty or not (set(MEDIDAS) | {"species"}).issubset(df.columns):
    st.error("A base tratada está vazia ou não contém as colunas esperadas.")
    st.stop()

st.subheader("Selecione seu recorte")
st.caption("Os filtros de espécie e massa se aplicam às duas análises.")
filtro_especie, filtro_medidas, filtro_massa = st.columns([1, 1.3, 1.2])

with filtro_especie:
    opcoes_especies = sorted(df["species"].dropna().unique().tolist())
    especies = st.multiselect(
        "Espécies", opcoes_especies, default=opcoes_especies,
        format_func=lambda especie: ESPECIES.get(especie, especie), key="especies",
    )

with filtro_medidas:
    variaveis = st.multiselect(
        "Medidas para correlação", list(MEDIDAS), default=list(MEDIDAS),
        format_func=MEDIDAS.get, key="variaveis",
    )

with filtro_massa:
    massa_min, massa_max = int(df["body_mass_g"].min()), int(df["body_mass_g"].max())
    intervalo_massa = st.slider(
        "Intervalo da massa corporal (g)", min_value=massa_min, max_value=massa_max,
        value=(massa_min, massa_max), step=1, key="intervalo_massa",
    )

df_filtrado = df.loc[
    df["species"].isin(especies) & df["body_mass_g"].between(*intervalo_massa)
]
st.caption(f"Exibindo {len(df_filtrado)} de {len(df)} registros após os filtros.")
if df_filtrado.empty:
    st.warning("Nenhum registro corresponde aos filtros. Selecione espécies ou amplie o intervalo.")

st.divider()
st.header("01 · Quais medidas variam juntas?")
st.caption("Correlação de Pearson entre as medidas selecionadas")
correlacao, contexto = st.columns([2, 1])
with correlacao:
    if len(variaveis) < 2:
        st.warning("Selecione pelo menos duas medidas para analisar a correlação.")
    elif not df_filtrado.empty and len(df_filtrado) < 3:
        st.warning("Amplie os filtros para incluir pelo menos três registros.")
    elif not df_filtrado.empty and (df_filtrado[variaveis].nunique(dropna=True) < 2).any():
        st.warning("Uma das medidas selecionadas não varia nesses registros. Ajuste os filtros.")
    st.info("Espaço reservado para o mapa de calor da correlação.")

with contexto:
    st.subheader("Nadadeira e massa")
    st.write("Na EDA, essas medidas apresentaram uma relação positiva. Compare as espécies usando os filtros.")
    st.caption("A observação se refere à EDA; o gráfico dos dados filtrados será feito na próxima aula.")

st.divider()
st.header("02 · Como os valores se distribuem?")
st.caption("Observe uma medida e compare as espécies.")
controle_medida, controle_grupos = st.columns([2, 1])
with controle_medida:
    medida_distribuicao = st.selectbox(
        "Medida para distribuição", list(MEDIDAS),
        index=list(MEDIDAS).index("body_mass_g"), format_func=MEDIDAS.get,
        key="medida_distribuicao",
    )
with controle_grupos:
    separar_especies = st.toggle("Distinguir por espécie", key="separar_especies")

st.info("Espaço reservado para o histograma da medida selecionada.")

# O mapa de calor e o histograma serão implementados na próxima aula.
