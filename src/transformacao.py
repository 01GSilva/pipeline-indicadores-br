import pandas as pd
import json
import os
from glob import glob
from datetime import datetime

# Mapeamento de metadados de cada indicador
METADADOS = {
    'ipca':{
        'codigo':'ipca',
        'nome': 'IPCA - Indice de Preços ao Consumidor Amplo',
        'unidade': '% ao mes',
        'fonte': 'Banco Central do Brasil'
    },
    'selic':{
        'codigo': 'selic',
        'nome': 'Taxa Selic',
        'unidade': '% ao ano',
        'fonte': 'Banco Central do Brasil'
    },
    'dolar':{
        'codigo': 'dolar',
        'nome': 'Dólar Comercial',
        'unidade': 'R$',
        'fonte': 'Banco Central do Brasil'
    }
}

def ler_bronze(nome):
    # Lê o arquivo json mais recente de um indicador na camada Bronze.
    arquivos = sorted(glob(f'data/bronze/{nome}_*.json'))
    if not arquivos:
        raise FileNotFoundError(f'Nenhum arquivo encontrado para {nome}')

    # Pega sempre o mais recente
    arquivo = arquivos[-1]
    print(f'Lendo {arquivo}...')
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    return dados

def transformar(nome,dados):
    # Limpa e padroniza os dados brutos
    df = pd.DataFrame(dados)

    # converte os tipos
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

    # Remove linhas com valor nulo
    df = df.dropna(subset=['valor'])

    # Adiciona colunas ao calendário
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    df['trimestre'] = df['data'].dt.quarter
    df['nome_mes'] = df['data'].dt.strftime('%B')
    df['indicador'] = nome

    # Ordena por data
    df = df.sort_values('data').reset_index(drop=True)
    
    print(f'{nome}: {len(df)} registros após limpeza')
    return df

def salvar_silver(nome, df):
    # Salva os dados limpos em CSV na camada Silver
    hoje = datetime.today().strftime('%Y%m%d')
    caminho = f'data/silver/{nome}_{hoje}.csv'
    df.to_csv(caminho, index=False)
    print(f'Salvo em {caminho}')

def executar():
    dfs = {}

    for nome in METADADOS.keys():
        dados = ler_bronze(nome)
        df = transformar(nome, dados)
        salvar_silver(nome, df)
        dfs[nome] = df

    print('\nTransformação concluída.')
    return dfs, METADADOS

if __name__ == '__main__':
    executar()