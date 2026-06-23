import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def conectar():
    # Cria a conexão com o PostgreSQL usando as variáveis do .env
    url = (
        f'postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}'
        f'@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'
    )
    engine = create_engine(url)
    print('Conexão com o banco estabelecida.')
    return engine

def carregar_dim_indicador(engine, metadados):
    # Popula a tabela dimensão de indicadores
    with engine.begin() as conn:
        for meta in metadados.values():
            conn.execute(text('''
                INSERT INTO dim_indicador (codigo, nome, unidade, fonte)
                VALUES (:codigo, :nome, :unidade, :fonte)
                ON CONFLICT (codigo) DO NOTHING
            '''), meta)
    print('dim_indicador carregada.')

def carregar_dim_tempo(engine, df_total):
    # Popula a tabela dimensão de tempo com todas as datas únicas.
    datas = df_total[['data','ano','mes','trimestre','nome_mes']].drop_duplicates()

    with engine.begin() as conn:
        for _, row in datas.iterrows():
            conn.execute(text('''
                INSERT INTO dim_tempo (data, ano, mes, trimestre, nome_mes)
                VALUES (:data, :ano, :mes, :trimestre, :nome_mes)
                ON CONFLICT (data) DO NOTHING
            '''), {
                'data': row['data'].date(),
                'ano': int(row['ano']),
                'mes': int(row['mes']),
                'trimestre': int(row['trimestre']),
                'nome_mes': row['nome_mes']
            })
    print('dim_tempo carregada.')

def carregar_fato(engine, dfs):
    #Popula a tabela fato cruzando com as dimensões ja carregadas
    with engine.begin() as conn:
        for nome, df in dfs.items():
            for _, row in df.iterrows():
                conn.execute(text('''
                    INSERT INTO fato_indicadores (id_tempo, id_indicador, valor)
                    SELECT t.id_tempo, i.id_indicador, :valor
                    FROM dim_tempo t, dim_indicador i
                    WHERE t.data = :data
                    AND i.codigo = :indicador
                '''), {
                    'valor': float(row['valor']),
                    'data': row['data'].date(),
                    'indicador': nome
                })
            print(f'fato_indicadores: {nome} carregado ({len(df)} registros)')

def executar(dfs, metadados):
    engine = conectar()
    df_total = pd.concat(dfs.values())
    carregar_dim_indicador(engine, metadados)
    carregar_dim_tempo(engine, df_total)
    carregar_fato(engine, dfs)

    print("\nCarga concluída")

if __name__ == "__main__":
    from transformacao import executar as transformar
    dfs, metadados = transformar()
    executar(dfs, metadados)