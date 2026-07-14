# Regras de Data Quality

## Objetivo

Validar a consistência, integridade e confiabilidade dos dados da camada Silver antes da liberação para a Gold.

## Criticidades

- `erro`: falha que bloqueia a pipeline;
- `alerta`: inconsistência que deve ser investigada, mas não necessariamente bloqueia o processamento.

## Regras gerais

- contagem de registros;
- contagem de colunas;
- duplicidade completa;
- valores nulos e NaN;
- verificação de schema.

## Município

Chave lógica:

- ano
- id_municipio
- serie
- rede

Regras:

- chaves obrigatórias preenchidas;
- taxa de alfabetização entre 0 e 100;
- unicidade da chave lógica.

## UF

Chave lógica:

- ano
- sigla_uf
- serie
- rede

Regras:

- chaves obrigatórias preenchidas;
- taxa de alfabetização entre 0 e 100;
- sigla de UF no padrão de duas letras maiúsculas.

## Metas

Regras:

- metas de 2024 a 2030 entre 0 e 100;
- percentual de participação entre 0 e 100;
- tratamento de campos ausentes como nulos, sem exclusão global de registros.

## Alunos agregados

Granularidade:

- ano
- id_municipio
- id_escola
- serie
- rede

Regras:

- total de registros maior que zero;
- totais não negativos;
- presentes não podem exceder o total;
- alfabetizados não podem exceder o total;
- cadernos preenchidos não podem exceder o total;
- taxas entre 0 e 100;
- proficiência média não negativa;
- unicidade da granularidade;
- integridade dos municípios em relação à tabela municipal.

## Liberação para a Gold

A pipeline é considerada aprovada quando não existem regras de criticidade `erro` com status `REPROVADO`.
