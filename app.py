from pathlib import Path

import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st

from src.analise_pinguins import calcular_metricas, filtrar_dados, filtrar_grupos, matriz_correlacao

st.set_page_config(page_title="Pinguins Palmer", page_icon="🐧", layout="wide")

MEDIDAS = {
    "bill_length_mm": "Comprimento do bico (mm)",
    "bill_depth_mm": "Profundidade do bico (mm)",
    "flipper_length_mm": "Comprimento da nadadeira (mm)",
    "body_mass_g": "Massa corporal (g)",
}
ESPECIES = {"Adelie": "Adélie", "Chinstrap": "Chinstrap", "Gentoo": "Gentoo"}
CORES_ESPECIES = {"Adélie": "#27717A", "Chinstrap": "#D28245", "Gentoo": "#486B9A"}


@st.cache_data(max_entries=2)
def carregar_dados():
    caminho = Path(__file__).resolve().parent / "data" / "clean" / "penguins.csv"
    return pd.read_csv(caminho)


def numero(valor, casas=1):
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


st.title("Pinguins Palmer")
st.caption("Análise exploratória de medidas físicas · Arquipélago Palmer, 2007–2009")

try:
    df = carregar_dados()
except (FileNotFoundError, pd.errors.EmptyDataError):
    st.error("Não foi possível abrir a base tratada. Execute o notebook da EDA para gerá-la.")
    st.stop()

colunas_obrigatorias = set(MEDIDAS) | {"species", "island"}
if df.empty or not colunas_obrigatorias.issubset(df.columns):
    st.error("A base tratada está vazia ou não contém as colunas esperadas.")
    st.stop()

opcoes_especies = sorted(df["species"].dropna().unique().tolist())
opcoes_ilhas = sorted(df["island"].dropna().unique().tolist())
aba_correlacao, aba_indicadores = st.tabs(["Dashboard 1 · Correlação e distribuição", "Dashboard 2 · Indicadores"])

with aba_correlacao:
    st.header("Medidas e relações")
    st.caption("Os filtros de espécie e massa se aplicam ao mapa de calor e ao histograma.")
    filtro_especie, filtro_medidas, filtro_massa = st.columns([1, 1.3, 1.2])
    with filtro_especie:
        especies = st.multiselect(
            "Espécies", opcoes_especies, default=opcoes_especies,
            format_func=lambda item: ESPECIES.get(item, item), key="d1_especies",
        )
    with filtro_medidas:
        variaveis = st.multiselect(
            "Medidas para correlação", list(MEDIDAS), default=list(MEDIDAS),
            format_func=MEDIDAS.get, key="d1_variaveis",
        )
    with filtro_massa:
        massa_min = int(df["body_mass_g"].min())
        massa_max = int(df["body_mass_g"].max())
        intervalo_massa = st.slider(
            "Intervalo da massa corporal (g)", massa_min, massa_max,
            value=(massa_min, massa_max), step=1, key="d1_massa",
        )

    recorte = filtrar_dados(df, especies, intervalo_massa=intervalo_massa)
    st.caption(f"Exibindo {len(recorte)} de {len(df)} registros após os filtros.")
    if recorte.empty:
        st.warning("Nenhum registro corresponde aos filtros. Selecione espécies ou amplie o intervalo.")

    st.subheader("01 · Quais medidas variam juntas?")
    st.caption("Correlação de Pearson: de −1 a 1. Correlação não indica causalidade.")
    if len(variaveis) < 2:
        st.warning("Selecione pelo menos duas medidas para analisar a correlação.")
    elif len(recorte) < 3 and not recorte.empty:
        st.warning("Amplie os filtros para incluir pelo menos três registros.")
    elif not recorte.empty:
        constantes = [v for v in variaveis if recorte[v].nunique(dropna=True) < 2]
        variaveis_validas = [v for v in variaveis if v not in constantes]
        if constantes:
            nomes = ", ".join(MEDIDAS[v] for v in constantes)
            st.warning(f"Sem variação neste recorte: {nomes}. Essas medidas foram retiradas da correlação.")
        if len(variaveis_validas) < 2:
            st.warning("Escolha pelo menos duas medidas com variação ou amplie os filtros.")
        else:
            corr = matriz_correlacao(recorte, variaveis_validas).rename(index=MEDIDAS, columns=MEDIDAS)
            calor = px.imshow(
                corr, text_auto=".2f", zmin=-1, zmax=1, aspect="auto",
                color_continuous_scale="RdBu_r", labels={"color": "Pearson"},
            )
            calor.update_layout(margin=dict(l=5, r=5, t=15, b=5), coloraxis_colorbar_title="Pearson")
            st.plotly_chart(calor, key="d1_heatmap")

    st.subheader("02 · Como os valores se distribuem?")
    controle_medida, controle_grupos = st.columns([2, 1])
    with controle_medida:
        medida = st.selectbox(
            "Medida para distribuição", list(MEDIDAS),
            index=list(MEDIDAS).index("body_mass_g"), format_func=MEDIDAS.get,
            key="d1_distribuicao",
        )
    with controle_grupos:
        separar = st.toggle("Distinguir por espécie", key="d1_separar")
    if not recorte.empty:
        dados_hist = recorte.assign(especie=recorte["species"].map(ESPECIES).fillna(recorte["species"]))
        hist = px.histogram(
            dados_hist, x=medida, color="especie" if separar else None, nbins=18,
            barmode="overlay" if separar else "relative", opacity=0.75 if separar else 1,
            labels={medida: MEDIDAS[medida], "especie": "Espécie"},
            color_discrete_map=CORES_ESPECIES, color_discrete_sequence=["#27717A"],
        )
        hist.update_layout(yaxis_title="Quantidade de registros", legend_title="Espécie", margin=dict(l=5, r=5, t=15, b=5))
        st.plotly_chart(hist, key="d1_histograma")

with aba_indicadores:
    st.header("Pinguins em números")
    st.caption("Indicadores da amostra tratada. Filtre e selecione um grupo para explorar.")
    coluna_especies, coluna_ilhas = st.columns(2)
    with coluna_especies:
        especies_kpi = st.multiselect(
            "Espécies para indicadores", opcoes_especies, default=opcoes_especies,
            format_func=lambda item: ESPECIES.get(item, item), key="d2_especies",
        )
    with coluna_ilhas:
        ilhas_kpi = st.multiselect("Ilhas", opcoes_ilhas, default=opcoes_ilhas, key="d2_ilhas")

    base_kpi = filtrar_dados(df, especies_kpi, ilhas=ilhas_kpi)
    agrupamento = st.selectbox("Agrupar contagem por", ["Espécie", "Ilha"], key="d2_agrupamento")
    coluna_grupo = "especie_nome" if agrupamento == "Espécie" else "island"
    base_kpi["especie_nome"] = base_kpi["species"].map(ESPECIES).fillna(base_kpi["species"])
    base_kpi["grupo"] = base_kpi[coluna_grupo]

    bloco_metricas = st.container()
    coluna_barras, coluna_medias = st.columns(2)
    with coluna_barras:
        st.subheader("Registros por grupo")
        st.caption("Clique em uma barra para filtrar os indicadores. Dê clique duplo para limpar.")
        if base_kpi.empty:
            st.warning("Nenhum registro corresponde aos filtros de espécie e ilha.")
            grupos_escolhidos = []
        else:
            contagem = base_kpi.groupby("grupo", as_index=False).size().rename(columns={"size": "registros"})
            selecao = alt.selection_point(name="grupo_selecionado", fields=["grupo"], clear="dblclick")
            barras = (
                alt.Chart(contagem)
                .mark_bar(cornerRadiusEnd=4)
                .encode(
                    x=alt.X("registros:Q", title="Quantidade de registros"),
                    y=alt.Y("grupo:N", sort="-x", title=agrupamento),
                    color=alt.condition(selecao, alt.value("#27717A"), alt.value("#B8C8CD")),
                    tooltip=[alt.Tooltip("grupo:N", title=agrupamento), alt.Tooltip("registros:Q", title="Registros")],
                )
                .add_params(selecao)
                .properties(height=230)
            )
            evento = st.altair_chart(barras, key=f"d2_barras_{agrupamento}", on_select="rerun")
            itens = evento["selection"].get("grupo_selecionado", [])
            grupos_escolhidos = [item["grupo"] for item in itens if "grupo" in item]

    selecionados = filtrar_grupos(base_kpi, "grupo", grupos_escolhidos)
    metricas = calcular_metricas(selecionados)
    with bloco_metricas:
        if grupos_escolhidos:
            st.caption("Seleção no gráfico: " + ", ".join(map(str, grupos_escolhidos)))
        if selecionados.empty and not base_kpi.empty:
            st.warning("A seleção não possui registros no recorte atual. Limpe a seleção do gráfico ou ajuste os filtros.")
        cols = st.columns(4)
        cols[0].metric("Registros", str(metricas["registros"]))
        cols[1].metric("Massa média", f"{numero(metricas['massa_media'])} g" if metricas["massa_media"] is not None else "—")
        cols[2].metric("Nadadeira média", f"{numero(metricas['nadadeira_media'])} mm" if metricas["nadadeira_media"] is not None else "—")
        cols[3].metric("Gentoo no recorte", f"{numero(metricas['gentoo_pct'])}%" if metricas["gentoo_pct"] is not None else "—")

    with coluna_medias:
        st.subheader("Massa média por espécie")
        st.caption("O gráfico reflete os filtros e a seleção da barra.")
        if selecionados.empty:
            st.info("Sem dados para mostrar neste recorte.")
        else:
            medias = selecionados.groupby("especie_nome", as_index=False).agg(
                massa_media=("body_mass_g", "mean"), registros=("body_mass_g", "size")
            )
            grafico_medias = (
                alt.Chart(medias).mark_bar(cornerRadiusEnd=4)
                .encode(
                    x=alt.X("massa_media:Q", title="Massa corporal média (g)"),
                    y=alt.Y("especie_nome:N", sort="-x", title="Espécie"),
                    color=alt.Color("especie_nome:N", title="Espécie",
                                    scale=alt.Scale(domain=list(CORES_ESPECIES), range=list(CORES_ESPECIES.values())),
                                    legend=None),
                    tooltip=[alt.Tooltip("especie_nome:N", title="Espécie"),
                             alt.Tooltip("massa_media:Q", title="Massa média (g)", format=".1f"),
                             alt.Tooltip("registros:Q", title="Registros")],
                ).properties(height=230)
            )
            st.altair_chart(grafico_medias, key="d2_medias")
    st.caption("Amostra de 2007–2009. As espécies não aparecem igualmente em todas as ilhas; não atribua diferenças ao local isoladamente.")
