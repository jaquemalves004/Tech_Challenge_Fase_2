# Dashboard Analytics

## Objetivo

Apresentar os principais indicadores da pipeline em uma camada visual e executiva.

## Fonte

O dashboard consome exclusivamente os Data Marts da camada Gold.

Não são realizadas leituras diretas da Bronze ou Silver.

## Ano de referência

O ano mais recente disponível é identificado automaticamente a partir do Data Mart de desempenho municipal.

## Indicadores gerais

- Total de municípios;
- Total de UFs;
- Total de escolas;
- Média da taxa de alfabetização;
- Média de Português;
- Percentual de desempenho excelente.

## Indicadores do perfil de alunos

- Total de registros representados;
- Taxa ponderada de presença;
- Taxa ponderada de alfabetização;
- Proficiência média ponderada;
- Percentual de grupos acima do ponto de corte de 743.

## Visualizações

### Distribuição municipal

Apresenta a distribuição dos registros entre:

- Excelente;
- Bom;
- Regular;
- Crítico.

### Ranking das UFs

Exibe as UFs com maior índice geral no ano de referência.

A categoria Total é priorizada. Quando a cobertura não é suficiente, é utilizado o melhor registro disponível por UF.

### Comparação entre resultado e meta

Compara a taxa observada de alfabetização com a meta de 2024 por UF.

### Evolução dos alunos

Exibe a evolução ponderada de:

- presença;
- alfabetização;
- preenchimento do caderno.

### Proficiência

Compara a proficiência média ponderada com o ponto de corte de 743 pontos.

### Indicadores por rede

Compara presença e alfabetização entre as redes disponíveis.

## Tecnologia

As visualizações foram desenvolvidas com Plotly.

Os cálculos pesados são realizados em Spark. A conversão para Pandas ocorre somente depois da agregação dos dados.

## Exportação

Os gráficos são exportados em HTML interativo e as tabelas auxiliares em CSV.

Esses arquivos são gerados durante a execução e não são versionados no GitHub.
