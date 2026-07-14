# Contratos da Camada Silver

## Objetivo

A camada Silver contém dados limpos, tipados, deduplicados e preparados para consumo analítico.

## Entidades

### municipio

Chave lógica:

- ano
- id_municipio
- serie
- rede

Regras:

- taxa_alfabetizacao entre 0 e 100;
- rede preservada como código numérico;
- categoria_rede adicionada como descrição;
- id_municipio armazenado como texto.

### uf

Chave lógica:

- ano
- sigla_uf
- serie
- rede

Regras:

- sigla_uf com duas letras;
- taxa_alfabetizacao entre 0 e 100;
- categoria_rede derivada do código de rede.

### meta_municipio

Chave lógica:

- ano
- id_municipio
- rede

Regras:

- colunas de meta entre 0 e 100;
- valores NaN convertidos para nulo;
- identificador municipal armazenado como texto.

### meta_uf

Chave lógica:

- ano
- sigla_uf
- rede

### meta_brasil

Chave lógica:

- ano
- rede

### alunos_agregados

Granularidade:

- ano
- id_municipio
- id_escola
- serie
- rede

Regras:

- não contém identificador individual de aluno;
- total_registros maior que zero;
- taxas entre 0 e 100;
- agregação realizada previamente no BigQuery.
