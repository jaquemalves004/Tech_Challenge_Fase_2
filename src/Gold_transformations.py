"""Transformações reutilizáveis da camada Gold."""

from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from pyspark.sql.window import Window


def criar_desempenho_municipio(
    df: DataFrame,
) -> DataFrame:
    """Cria indicadores analíticos de desempenho municipal."""

    return (
        df
        .withColumn(
            "indice_geral",
            F.round(
                (
                    F.col("taxa_alfabetizacao")
                    + (
                        F.col("media_portugues")
                        / 10
                    )
                ) / 2,
                2,
            ),
        )
        .withColumn(
            "nivel_desempenho",
            F.when(
                F.col("taxa_alfabetizacao").isNull(),
                "Não informado",
            )
            .when(
                F.col("taxa_alfabetizacao") >= 80,
                "Excelente",
            )
            .when(
                F.col("taxa_alfabetizacao") >= 70,
                "Bom",
            )
            .when(
                F.col("taxa_alfabetizacao") >= 60,
                "Regular",
            )
            .otherwise("Crítico"),
        )
        .withColumn(
            "faixa_portugues",
            F.when(
                F.col("media_portugues").isNull(),
                "Não informado",
            )
            .when(
                F.col("media_portugues") >= 800,
                "Muito alta",
            )
            .when(
                F.col("media_portugues") >= 700,
                "Alta",
            )
            .when(
                F.col("media_portugues") >= 600,
                "Média",
            )
            .otherwise("Baixa"),
        )
        .withColumn(
            "ano_referencia",
            F.col("ano"),
        )
    )


def criar_desempenho_uf(
    df: DataFrame,
) -> DataFrame:
    """Cria indicadores e ranking da camada estadual."""

    janela = (
        Window
        .partitionBy("ano")
        .orderBy(
            F.col("indice_geral").desc_nulls_last()
        )
    )

    return (
        df
        .withColumn(
            "indice_geral",
            F.round(
                (
                    F.col("taxa_alfabetizacao")
                    + (
                        F.col("media_portugues")
                        / 10
                    )
                ) / 2,
                2,
            ),
        )
        .withColumn(
            "nivel_desempenho",
            F.when(
                F.col("taxa_alfabetizacao").isNull(),
                "Não informado",
            )
            .when(
                F.col("taxa_alfabetizacao") >= 80,
                "Excelente",
            )
            .when(
                F.col("taxa_alfabetizacao") >= 70,
                "Bom",
            )
            .when(
                F.col("taxa_alfabetizacao") >= 60,
                "Regular",
            )
            .otherwise("Crítico"),
        )
        .withColumn(
            "ranking_uf",
            F.dense_rank().over(janela),
        )
        .withColumn(
            "faixa_ranking",
            F.when(
                F.col("ranking_uf") <= 5,
                "Top 5",
            )
            .when(
                F.col("ranking_uf") <= 10,
                "Top 10",
            )
            .when(
                F.col("ranking_uf") <= 20,
                "Top 20",
            )
            .otherwise("Demais"),
        )
    )


def criar_meta_uf(
    df: DataFrame,
) -> DataFrame:
    """Cria indicadores analíticos de metas estaduais."""

    janela = (
        Window
        .partitionBy("ano")
        .orderBy(
            F.col(
                "percentual_cumprimento_meta_2024"
            ).desc_nulls_last()
        )
    )

    return (
        df
        .withColumn(
            "crescimento_meta_2024_2030",
            F.round(
                F.col("meta_alfabetizacao_2030")
                - F.col("meta_alfabetizacao_2024"),
                2,
            ),
        )
        .withColumn(
            "percentual_evolucao_meta",
            F.when(
                F.col(
                    "meta_alfabetizacao_2024"
                ).isNull()
                | (
                    F.col(
                        "meta_alfabetizacao_2024"
                    ) == 0
                ),
                None,
            ).otherwise(
                F.round(
                    (
                        (
                            F.col(
                                "meta_alfabetizacao_2030"
                            )
                            - F.col(
                                "meta_alfabetizacao_2024"
                            )
                        )
                        / F.col(
                            "meta_alfabetizacao_2024"
                        )
                    ) * 100,
                    2,
                )
            ),
        )
        .withColumn(
            "diferenca_meta_2024",
            F.round(
                F.col("taxa_alfabetizacao")
                - F.col("meta_alfabetizacao_2024"),
                2,
            ),
        )
        .withColumn(
            "percentual_cumprimento_meta_2024",
            F.when(
                F.col(
                    "meta_alfabetizacao_2024"
                ).isNull()
                | (
                    F.col(
                        "meta_alfabetizacao_2024"
                    ) == 0
                ),
                None,
            ).otherwise(
                F.round(
                    (
                        F.col("taxa_alfabetizacao")
                        / F.col(
                            "meta_alfabetizacao_2024"
                        )
                    ) * 100,
                    2,
                )
            ),
        )
        .withColumn(
            "status_meta_2024",
            F.when(
                F.col(
                    "meta_alfabetizacao_2024"
                ).isNull(),
                "Sem meta disponível",
            )
            .when(
                F.col("diferenca_meta_2024") >= 0,
                "Meta atingida",
            )
            .when(
                F.col("diferenca_meta_2024") >= -2,
                "Próximo da meta",
            )
            .otherwise("Abaixo da meta"),
        )
        .withColumn(
            "ranking_cumprimento_meta",
            F.dense_rank().over(janela),
        )
    )


def criar_perfil_alunos(
    df: DataFrame,
    ponto_corte: float = 743.0,
) -> DataFrame:
    """Cria indicadores analíticos para grupos agregados de alunos."""

    return (
        df
        .withColumn(
            "situacao_proficiencia",
            F.when(
                F.col("proficiencia_media").isNull(),
                "Não informado",
            )
            .when(
                F.col("proficiencia_media")
                >= F.lit(ponto_corte),
                "Acima do ponto de corte",
            )
            .otherwise(
                "Abaixo do ponto de corte"
            ),
        )
        .withColumn(
            "diferenca_ponto_corte",
            F.round(
                F.col("proficiencia_media")
                - F.lit(ponto_corte),
                2,
            ),
        )
        .withColumn(
            "indice_participacao_aprendizagem",
            F.round(
                (
                    F.col("taxa_presenca")
                    + F.col(
                        "taxa_alfabetizacao_alunos"
                    )
                    + F.col(
                        "taxa_preenchimento_caderno"
                    )
                ) / 3,
                2,
            ),
        )
    )
