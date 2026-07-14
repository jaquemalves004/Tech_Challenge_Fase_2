SELECT
    ano,
    id_municipio,
    id_escola,
    serie,
    rede,
    COUNT(*) AS total_registros,
    COUNTIF(LOWER(TRIM(presenca)) IN ('1', 'sim', 's', 'true')) AS total_presentes,
    COUNTIF(LOWER(TRIM(alfabetizado)) IN ('1', 'sim', 's', 'true')) AS total_alfabetizados,
    COUNTIF(
        LOWER(TRIM(preenchimento_caderno))
        IN ('1', 'sim', 's', 'true')
    ) AS total_cadernos_preenchidos,
    AVG(proficiencia) AS proficiencia_media,
    AVG(peso_aluno) AS peso_medio
FROM `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
WHERE ano >= 2023
GROUP BY
    ano,
    id_municipio,
    id_escola,
    serie,
    rede;
