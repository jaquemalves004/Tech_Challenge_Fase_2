
# Documentação Técnica

## Tech Challenge – Fase 2

### Pipeline de Dados para Análise da Alfabetização no Brasil

---

# 1. Visão Geral

Este projeto implementa uma pipeline de dados em arquitetura Lakehouse para análise dos indicadores de alfabetização no Brasil.

A solução utiliza PySpark para processamento distribuído e BigQuery como fonte de dados em nuvem.

O pipeline foi estruturado seguindo o padrão Medallion Architecture:

- Bronze
- Silver
- Gold

permitindo rastreabilidade, qualidade e reutilização dos dados.

---

# 2. Objetivos

O projeto tem como finalidade:

- Consolidar indicadores de alfabetização;
- Avaliar cumprimento de metas educacionais;
- Produzir Data Marts analíticos;
- Disponibilizar indicadores executivos;
- Aplicar conceitos de Engenharia de Dados e FinOps.

---

# 3. Arquitetura da Solução

## Arquitetura Geral

```text
Base dos Dados (BigQuery)
            │
            ▼
     Camada Bronze
            │
            ▼
     Camada Silver
            │
            ▼
      Camada Gold
            │
            ▼
 Dashboard Analytics
```

---

# 4. Fonte de Dados

## Plataforma

Base dos Dados

## Dataset

Avaliação da Alfabetização

## Acesso

Google BigQuery

## Tabelas Utilizadas

| Tabela | Descrição |
|----------|-------------|
| municipio | Indicadores por município |
| uf | Indicadores por estado |
| meta_municipio | Metas municipais |
| meta_uf | Metas estaduais |
| meta_brasil | Metas nacionais |
| alunos | Dados individuais dos alunos |

---

# 5. Ambiente Tecnológico

## Linguagem

Python 3

## Framework

PySpark

## Armazenamento

Parquet

## Cloud

Google Cloud Platform

## Fonte de Dados

BigQuery

## Visualização

Plotly

## Ambiente de Execução

Google Colab

---

# 6. Camada Bronze

## Objetivo

Realizar a ingestão dos dados provenientes do BigQuery.

## Transformações

- Leitura das tabelas de origem;
- Inclusão de metadados;
- Registro da origem dos dados;
- Persistência em formato Parquet.

## Metadados Adicionados

| Campo | Descrição |
|---------|-------------|
| data_ingestao | Data da carga |
| origem | Fonte dos dados |
| modo_ingestao | Tipo de ingestão |
| projeto_execucao | Identificação do projeto |

## Saída

```text
data/bronze/
```

---

# 7. Camada Silver

## Objetivo

Realizar limpeza, padronização e validação dos dados.

## Principais Transformações

### Padronização

- Conversão de tipos;
- Normalização de colunas;
- Padronização de valores categóricos.

### Qualidade

- Remoção de duplicidades;
- Tratamento de valores nulos;
- Verificação de consistência.

### Tabela Alunos

Devido ao volume elevado de registros, foi criada uma agregação para reduzir o volume de processamento na camada Gold.

Indicadores gerados:

- Total de alunos;
- Total de presentes;
- Total de alfabetizados;
- Total de cadernos preenchidos;
- Proficiência média.

## Saída

```text
data/silver/
```

---

# 8. Data Quality

Foram implementadas validações automáticas.

## Validações Executadas

### Estrutura

- Schema validation

### Integridade

- Null validation
- Duplicate validation

### Negócio

- Consistência de taxas
- Verificação de chaves
- Faixas válidas de indicadores

---

# 9. Camada Gold

## Objetivo

Disponibilizar estruturas analíticas prontas para consumo.

---

## 9.1 Data Mart Desempenho Município

### Granularidade

Município + Série + Rede + Ano

### Indicadores

- Taxa de alfabetização
- Média de português
- Índice geral
- Faixa de desempenho

---

## 9.2 Data Mart Desempenho UF

### Granularidade

UF + Série + Rede + Ano

### Indicadores

- Taxa de alfabetização
- Média de português
- Índice geral
- Ranking

---

## 9.3 Data Mart Meta Município

### Indicadores

- Diferença para meta
- Percentual de cumprimento
- Status da meta

---

## 9.4 Data Mart Meta UF

### Indicadores

- Cumprimento da meta
- Evolução esperada
- Ranking estadual

---

## 9.5 Data Mart Meta Brasil

### Indicadores

- Meta nacional
- Cumprimento nacional
- Evolução projetada

---

## 9.6 Data Mart Perfil dos Alunos

### Indicadores

- Taxa de presença
- Taxa de alfabetização
- Taxa de preenchimento
- Proficiência média
- Situação da proficiência

---

## 9.7 Data Mart KPIs Executivos

Consolidação dos principais indicadores do projeto.

Grupos:

- Cobertura
- Desempenho Municipal
- Desempenho UF
- Metas
- Brasil
- Perfil dos Alunos
- Rankings

---

# 10. Estratégias de Modelagem

## Particionamento

Os Data Marts foram particionados por:

```text
ano
```

Objetivos:

- Reduzir leitura;
- Melhorar performance;
- Reduzir custos.

---

## Formato de Armazenamento

Parquet

Benefícios:

- Compressão;
- Leitura colunar;
- Menor consumo de armazenamento.

---

# 11. Estratégias de FinOps

O projeto adota práticas para otimização de custos computacionais.

## Medidas Implementadas

### Uso de Parquet

Redução do volume armazenado e processado.

### Agregação Antecipada

A tabela alunos foi agregada na camada Silver para reduzir processamento.

### Particionamento

Leitura apenas dos anos necessários.

### Conversão Controlada para Pandas

A conversão ocorre somente após agregações.

### BigQuery como Fonte

Consulta sob demanda sem necessidade de replicação completa dos dados.

---

# 12. Segurança e Privacidade

Os Data Marts analíticos não armazenam informações individuais dos alunos.

Os identificadores pessoais foram removidos das estruturas destinadas à análise.

O Data Mart Perfil dos Alunos trabalha exclusivamente com dados agregados.

---

# 13. Dashboard Analytics

O dashboard foi desenvolvido utilizando Plotly.

## Indicadores Apresentados

### Cobertura

- Municípios
- UFs
- Escolas

### Desempenho

- Ranking estadual
- Distribuição municipal

### Metas

- Cumprimento das metas
- Comparação entre metas e resultados

### Perfil dos Alunos

- Presença
- Alfabetização
- Proficiência

---

# 14. Limitações

- Dependência da disponibilidade da Base dos Dados;
- Atualização conforme publicação oficial dos dados;
- Ambiente de execução baseado em Google Colab.

---

# 15. Possíveis Evoluções

## Engenharia

- Airflow
- Terraform
- CI/CD

## Cloud

- Data Lake em GCS
- BigQuery como Data Warehouse final

## Analytics

- Looker Studio
- Power BI

## Governança

- Catálogo de dados
- Data Lineage

---

# 16. Conclusão

A solução implementa uma pipeline completa de Engenharia de Dados em ambiente cloud, utilizando boas práticas de ingestão, transformação, qualidade, modelagem analítica e otimização de custos.

O resultado é uma arquitetura escalável capaz de suportar análises educacionais em diferentes níveis geográficos, fornecendo indicadores estratégicos para apoio à tomada de decisão.
