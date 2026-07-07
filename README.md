# Pipeline de Indicadores Econômicos Brasileiros

Pipeline ETL que coleta dados econômicos do Banco Central do Brasil, transforma e carrega em um data warehouse local com dashboard analítico.

## Arquitetura
API BACEN → Bronze (JSON) → Silver (CSV) → Gold (PostgreSQL) → Metabase

## Indicadores coletados

| Indicador | Fonte | Período |
|-----------|-------|---------|
| IPCA | Banco Central do Brasil | 2020–hoje |
| Taxa Selic | Banco Central do Brasil | 2020–hoje |
| Dólar Comercial | Banco Central do Brasil | 2020–hoje |

## Stack

- **Python** — ingestão e transformação
- **Pandas** — limpeza e padronização dos dados
- **PostgreSQL** — data warehouse com star schema
- **SQLAlchemy** — conexão Python → banco
- **Metabase** — dashboard analítico

## Modelagem

Star schema com duas dimensões e uma tabela fato:

- `dim_tempo` — calendário com ano, mês e trimestre
- `dim_indicador` — metadados dos indicadores
- `fato_indicadores` — valores históricos

## Como executar

```bash
# Clone o repositório
git clone https://github.com/01GSilva/pipeline-indicadores-br

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com suas credenciais

# Execute o pipeline completo
python3 src/ingestao.py
python3 src/carga.py
```

## Estrutura do projeto

```bash
├── data/
│   ├── bronze/    # dados brutos da API
│   └── silver/    # dados limpos
├── src/
│   ├── ingestao.py      # coleta da API
│   ├── transformacao.py # limpeza com Pandas
│   └── carga.py         # carga no PostgreSQL
└── requirements.txt
```
