# Arquitetura da Solução

## Fluxo Geral

```text
BigQuery (GCP)
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

## Camada Bronze

Responsável pela ingestão dos dados.

## Camada Silver

Responsável por limpeza, padronização e qualidade.

## Camada Gold

Responsável pelos Data Marts analíticos.

## Dashboard

Responsável pela visualização dos indicadores.
