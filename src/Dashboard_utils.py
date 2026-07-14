"""Funções auxiliares para o Dashboard Analytics."""

from typing import Optional

import pandas as pd


def obter_kpi(
    kpis: pd.DataFrame,
    grupo: str,
    indicador: str,
    valor_padrao: Optional[float] = None,
) -> Optional[float]:
    """
    Retorna o valor numérico de um KPI identificado
    pela combinação grupo + indicador.
    """

    filtro = kpis.loc[
        (kpis["grupo"] == grupo)
        & (kpis["indicador"] == indicador)
    ]

    if filtro.empty:
        return valor_padrao

    valor = filtro.iloc[0]["valor_numerico"]

    if pd.isna(valor):
        return valor_padrao

    return float(valor)


def formatar_numero(
    valor: Optional[float],
    casas: int = 2,
) -> str:
    """
    Formata números no padrão brasileiro.
    """

    if valor is None:
        return "N/D"

    return (
        f"{valor:,.{casas}f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def validar_colunas(
    dataframe: pd.DataFrame,
    colunas_obrigatorias: list[str],
    nome_dataframe: str,
) -> None:
    """
    Valida a presença de colunas necessárias antes
    da geração das visualizações.
    """

    faltantes = (
        set(colunas_obrigatorias)
        - set(dataframe.columns)
    )

    if faltantes:
        raise ValueError(
            f"{nome_dataframe}: colunas ausentes: "
            f"{sorted(faltantes)}"
        )
