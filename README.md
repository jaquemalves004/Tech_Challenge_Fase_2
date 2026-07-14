# Tech Challenge - Fase 2

## Pipeline de Dados para Análise da Alfabetização no Brasil

### FIAP - Pós-Graduação em Data Analytics

---

## Objetivo

Este projeto tem como objetivo construir uma pipeline de dados completa utilizando uma arquitetura em camadas (Bronze, Silver e Gold) para análise dos indicadores de alfabetização no Brasil.

A solução foi desenvolvida utilizando PySpark e Google Cloud Platform (BigQuery), aplicando conceitos de Engenharia de Dados, Data Lakehouse, Data Quality, FinOps e Analytics.

---

## Problema de Negócio

A alfabetização é um dos principais indicadores da qualidade da educação básica brasileira.

O projeto busca responder perguntas como:

- Qual o nível de alfabetização por município?
- Quais estados apresentam melhor desempenho?
- Quais localidades atingem as metas nacionais?
- Como está a distribuição dos níveis de proficiência?
- Qual o perfil dos alunos avaliados?
- Como evoluem os indicadores educacionais ao longo do tempo?

---

## Arquitetura da Solução

```text
Base dos Dados (BigQuery)
           │
           ▼
      Bronze Layer
           │
           ▼
      Silver Layer
           │
           ▼
       Gold Layer
           │
           ▼
     Dashboard Analytics
```

---

## Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| Python | Desenvolvimento |
| PySpark | Processamento distribuído |
| Google Colab | Ambiente de execução |
| Google Drive | Armazenamento |
| BigQuery | Fonte de dados em nuvem |
| Parquet | Armazenamento otimizado |
| Plotly | Dashboard e visualizações |
| Pandas | Apoio às análises |

---

## Fonte de Dados

Os dados utilizados são provenientes da plataforma Base dos Dados.

Dataset:

https://basedosdados.org/dataset/073a39d4-89cf-4068-b1e8-34ed0d9c0b72

Consulta realizada via BigQuery.

---

# Estrutura do Projeto

```text
TechChallenge_Fase2/

│
├── README.md
│
├── docs/
│   └── Documentacao_Tecnica.md
│
├── notebooks/
│   ├── 01_Bronze.ipynb
│   ├── 02_Silver.ipynb
│   ├── 03_Gold.ipynb
│   └── 06_Dashboard_Analytics.ipynb
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── outputs/
│   ├── dashboard/
│   └── kpis_executivos/
│
└── images/
```

---

# Camada Bronze

Responsável pela ingestão dos dados provenientes do BigQuery.

Principais atividades:

- Leitura das tabelas de origem
- Inclusão de metadados
- Padronização inicial
- Armazenamento em formato Parquet

Tabelas carregadas:

- municipio
- uf
- meta_municipio
- meta_uf
- meta_brasil
- alunos

---

# Camada Silver

Responsável pela padronização e qualidade dos dados.

Transformações realizadas:

- Tratamento de valores nulos
- Conversão de tipos
- Remoção de duplicidades
- Padronização de colunas
- Data Quality
- Agregação da tabela alunos

Validações implementadas:

- Schema validation
- Null validation
- Duplicate validation
- Consistência de dados

---

# Camada Gold

Responsável pela criação dos Data Marts analíticos.

## Data Mart - Desempenho Município

Indicadores:

- Taxa de alfabetização
- Média de português
- Índice geral
- Faixa de desempenho

---

## Data Mart - Desempenho UF

Indicadores agregados por estado.

---

## Data Mart - Meta Município

Análise de cumprimento das metas por município.

---

## Data Mart - Meta UF

Análise de cumprimento das metas estaduais.

---

## Data Mart - Meta Brasil

Indicadores nacionais.

---

## Data Mart - Perfil dos Alunos

Indicadores agregados:

- Presença
- Alfabetização
- Preenchimento do caderno
- Proficiência média

---

## Data Mart - KPIs Executivos

Indicadores consolidados para visualização executiva.

---

# Dashboard Analytics

O dashboard apresenta:

- Indicadores gerais
- Ranking de estados
- Cumprimento de metas
- Distribuição de desempenho
- Indicadores dos alunos
- Evolução dos resultados

Visualizações desenvolvidas com Plotly.

---

# Implementação em Cloud

A solução utiliza a Google Cloud Platform através do BigQuery.

Fluxo:

```text
BigQuery
   ↓
PySpark
   ↓
Bronze
   ↓
Silver
   ↓
Gold
   ↓
Dashboard
```

O BigQuery foi utilizado como camada de consulta e extração dos dados da Base dos Dados.

---

# Estratégias de FinOps

Foram aplicadas práticas de otimização de custo e processamento:

- Utilização de Parquet para armazenamento eficiente
- Processamento distribuído com Spark
- Particionamento por ano
- Leitura apenas das colunas necessárias
- Agregação antecipada da base de alunos
- Conversão para Pandas apenas após agregações
- Reutilização dos dados processados nas camadas intermediárias

Essas estratégias reduzem consumo de memória, processamento e custos computacionais.

---

# Como Executar

## 1. Clonar o repositório

```bash
git clone <repositorio>
```

## 2. Abrir no Google Colab

Executar os notebooks na seguinte ordem:

```text
01_Bronze.ipynb

↓

02_Silver.ipynb

↓

03_Gold.ipynb

↓

06_Dashboard_Analytics.ipynb
```

---

# Principais Resultados

O projeto possibilita:

- Análise nacional da alfabetização
- Comparação entre estados
- Monitoramento de metas educacionais
- Avaliação do perfil dos alunos
- Produção de indicadores executivos para tomada de decisão

---

# Melhorias Futuras

- Integração direta com BigQuery como Data Warehouse
- Orquestração com Airflow
- Deploy em ambiente GCP produtivo
- Dashboard em Looker Studio
- Monitoramento contínuo da qualidade dos dados

---

# Autora

Jaqueline Medeiros

Projeto desenvolvido para o Tech Challenge – FIAP Pós-Graduação em Data Analytics.
