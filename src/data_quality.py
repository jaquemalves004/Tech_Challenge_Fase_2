"""Funções reutilizáveis de qualidade de dados."""

from datetime import datetime
from typing import Any

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, isnan


def contar_nulos(df: DataFrame) -> dict[str, int]:
    """
    Conta valores nulos por coluna.

    Em colunas float e double, também considera NaN.
    """

    tipos = dict(df.dtypes)
    resultado: dict[str, int] = {}

    for nome_coluna in df.columns:
        condicao = col(nome_coluna).isNull()

        if tipos[nome_coluna] in {"double", "float"}:
            condicao = condicao | isnan(col(nome_coluna))

        resultado[nome_coluna] = df.filter(
            condicao
        ).count()

    return resultado


def analisar_tabela(
    nome: str,
    df: DataFrame,
) -> dict[str, Any]:
    """
    Gera métricas gerais de qualidade para uma tabela.
    """

    total_registros = df.count()
    total_distintos = df.dropDuplicates().count()

    nulos_por_coluna = contar_nulos(df)

    return {
        "tabela": nome,
        "registros": total_registros,
        "colunas": len(df.columns),
        "duplicados_completos": (
            total_registros - total_distintos
        ),
        "valores_nulos": sum(
            nulos_por_coluna.values()
        ),
        "colunas_com_nulos": sum(
            1
            for valor in nulos_por_coluna.values()
            if valor > 0
        ),
        "data_execucao": datetime.now(),
    }


def contar_fora_intervalo(
    df: DataFrame,
    nome_coluna: str,
    minimo: float,
    maximo: float,
) -> int:
    """
    Conta valores não nulos fora de um intervalo permitido.
    """

    return df.filter(
        col(nome_coluna).isNotNull()
        & (
            (col(nome_coluna) < minimo)
            | (col(nome_coluna) > maximo)
        )
    ).count()


def contar_chaves_duplicadas(
    df: DataFrame,
    chaves: list[str],
) -> int:
    """
    Conta combinações de chave que aparecem mais de uma vez.
    """

    return (
        df.groupBy(*chaves)
        .count()
        .filter(
            col("count") > 1
        )
        .count()
    )


def criar_resultado_teste(
    tabela: str,
    regra: str,
    registros_invalidos: int,
    criticidade: str = "erro",
) -> dict[str, Any]:
    """
    Cria o registro padronizado de uma regra de qualidade.
    """

    return {
        "tabela": tabela,
        "regra": regra,
        "registros_invalidos": int(
            registros_invalidos
        ),
        "criticidade": criticidade,
        "status": (
            "APROVADO"
            if registros_invalidos == 0
            else "REPROVADO"
        ),
        "data_execucao": datetime.now(),
    }
