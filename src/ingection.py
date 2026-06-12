import requests
import json
import os
from datetime import datetime

# indicadores selecionados
INDICADORES = {
    'ipca': 433,
    'selic': 11,
    'dolar': 1
}

# periodo selecionado
DATA_INICIO = '01/01/2020'
DATA_FIM = datetime.today().strftime('%d/%m/%Y')

# funcao que chama a API do Bacen e retorna os dados brutos do indicador
def buscar_indicador(nome, codigo):
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados'
    params = {
        'formato': 'json',
        'dataInicial': DATA_INICIO,
        'dataFinal': DATA_FIM
    }
    print(f'Buscando {nome}..')
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# salva os dados brutos em Json na camada Bronze
def salvar_bronze(nome, dados):
    hoje = datetime.today().strftime('%Y%m%d')
    caminho = f'data/bronze/{nome}_{hoje}.json'

    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f'Salvo em {caminho} ({len(dados)} registros)')

def executar():
    for nome, codigo in INDICADORES.items():
        dados = buscar_indicador(nome, codigo)
        salvar_bronze(nome, dados)

    print("\nIngestão concluída!")

if __name__ == '__main__':
    executar()