"""Cálculos compartilhados pelos dashboards de pinguins."""

import pandas as pd


def filtrar_dados(df, especies, ilhas=None, intervalo_massa=None):
    mascara = df["species"].isin(especies)
    if ilhas is not None:
        mascara &= df["island"].isin(ilhas)
    if intervalo_massa is not None:
        mascara &= df["body_mass_g"].between(*intervalo_massa)
    return df.loc[mascara].copy()


def calcular_metricas(df):
    quantidade = len(df)
    if quantidade == 0:
        return {"registros": 0, "massa_media": None, "nadadeira_media": None, "gentoo_pct": None}
    return {
        "registros": quantidade,
        "massa_media": df["body_mass_g"].mean(),
        "nadadeira_media": df["flipper_length_mm"].mean(),
        "gentoo_pct": 100 * df["species"].eq("Gentoo").sum() / quantidade,
    }


def filtrar_grupos(df, coluna, grupos):
    """Sem seleção no gráfico, manter o recorte anterior."""
    return df.loc[df[coluna].isin(grupos)].copy() if grupos else df.copy()


def matriz_correlacao(df, variaveis):
    """Pearson com nomes de colunas originais para quem consome o resultado."""
    return df[variaveis].corr(method="pearson")
