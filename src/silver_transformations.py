"""Transformação reutilizável da camada Silver."""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, isnan, trim, when


class SilverProcessor:
    """Transformação comum de limpeza e padronização."""

    @staticmethod
    def remover_duplicados(df: DataFrame) -> DataFrame:
        return df.dropDuplicates()

    @staticmethod
    def normalizar_textos(
        df: DataFrame,
        colunas: list[str],
    ) -> DataFrame:
        for nome_coluna in colunas:
            if nome_coluna in df.columns:
                df = df.withColumn(
                    nome_coluna,
                    trim(col(nome_coluna)),
                )

        return df

    @staticmethod
    def converter_tipos(
        df: DataFrame,
        tipos: dict[str, str],
    ) -> DataFrame:
        for nome_coluna, tipo in tipos.items():
            if nome_coluna in df.columns:
                df = df.withColumn(
                    nome_coluna,
                    col(nome_coluna).cast(tipo),
                )

        return df

    @staticmethod
    def transformar_nan_em_null(
        df: DataFrame,
        colunas: list[str],
    ) -> DataFrame:
        for nome_coluna in colunas:
            if nome_coluna in df.columns:
                df = df.withColumn(
                    nome_coluna,
                    when(
                        isnan(col(nome_coluna)),
                        None,
                    ).otherwise(col(nome_coluna)),
                )

        return df


def tratar_desempenho(df: DataFrame) -> DataFrame:
    """Trata tabelas de desempenho municipal e estadual."""

    colunas_double = [
        "taxa_alfabetizacao",
        "media_portugues",
        *[
            f"proporcao_aluno_nivel_{nivel}"
            for nivel in range(9)
        ],
    ]

    df = SilverProcessor.remover_duplicados(df)

    df = SilverProcessor.converter_tipos(
        df,
        {
            "ano": "int",
            "serie": "int",
            "rede": "int",
            **{
                coluna: "double"
                for coluna in colunas_double
            },
        },
    )

    df = SilverProcessor.transformar_nan_em_null(
        df,
        colunas_double,
    )

    return df.withColumn(
        "categoria_rede",
        when(col("rede") == 0, "Total")
        .when(col("rede") == 2, "Estadual")
        .when(col("rede") == 3, "Municipal")
        .when(col("rede") == 5, "Privada")
        .otherwise("Não informado"),
    )


COLUNAS_META = [
    f"meta_alfabetizacao_{ano}"
    for ano in range(2024, 2031)
]


def tratar_meta(df: DataFrame) -> DataFrame:
    """Trata tabelas de metas municipais, estaduais e nacionais."""

    tipos = {
        "ano": "int",
        "rede": "string",
        "taxa_alfabetizacao": "double",
        "percentual_participacao": "double",
        **{
            coluna: "double"
            for coluna in COLUNAS_META
        },
    }

    if "nivel_alfabetizacao" in df.columns:
        tipos["nivel_alfabetizacao"] = "double"

    df = SilverProcessor.remover_duplicados(df)
    df = SilverProcessor.converter_tipos(df, tipos)

    df = SilverProcessor.normalizar_textos(
        df,
        [
            "rede",
            "sigla_uf",
            "id_municipio",
        ],
    )

    numericas = [
        "taxa_alfabetizacao",
        "percentual_participacao",
        *COLUNAS_META,
    ]

    if "nivel_alfabetizacao" in df.columns:
        numericas.append("nivel_alfabetizacao")

    return SilverProcessor.transformar_nan_em_null(
        df,
        numericas,
    )


def tratar_alunos_agregados(df: DataFrame) -> DataFrame:
    """Trata a base agregada e anonimizada de alunos."""

    df = SilverProcessor.remover_duplicados(df)

    df = SilverProcessor.converter_tipos(
        df,
        {
            "ano": "int",
            "id_municipio": "string",
            "id_escola": "string",
            "serie": "string",
            "rede": "string",
            "total_registros": "long",
            "total_presentes": "long",
            "total_alfabetizados": "long",
            "total_cadernos_preenchidos": "long",
            "proficiencia_media": "double",
            "peso_medio": "double",
            "taxa_presenca": "double",
            "taxa_alfabetizacao_alunos": "double",
        },
    )

    df = SilverProcessor.normalizar_textos(
        df,
        [
            "id_municipio",
            "id_escola",
            "serie",
            "rede",
        ],
    )

    df = df.filter(
        col("ano").isNotNull()
        & col("id_municipio").isNotNull()
        & col("total_registros").isNotNull()
        & (col("total_registros") > 0)
    )

    return df.withColumn(
        "taxa_preenchimento_caderno",
        when(
            col("total_registros") > 0,
            (
                col("total_cadernos_preenchidos")
                / col("total_registros")
            ) * 100,
        ),
    )
