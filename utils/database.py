import os
import psycopg2
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pandas as pd

# Load DataFrame outside the function if it's used globally
df = pd.read_csv("C:\\Users\\Aluno\\Downloads\\projeto_final_anac\\database\\anac_2025_sem_tratar_outliers.csv" , sep=';', encoding='latin1')

def get_connection():
    try:
        if os.environ.get('POSTGRES_HOST'):
            conn = psycopg2.connect(
                host=os.environ['POSTGRES_HOST'],
                port=os.environ.get('POSTGRES_PORT', '5432'),
                dbname=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD']
            )
        else:
            conn = psycopg2.connect(
                host=st.secrets.postgres.host,
                port=st.secrets.postgres.port,
                dbname=st.secrets.postgres.dbname,
                user=st.secrets.postgres.user,
                password=st.secrets.postgres.password
            )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {str(e)}")
        return None



def execute_query(query, params=None, return_df=False):
    conn = get_connection()
    if not conn:
        return None
        
    try:
        with conn.cursor() as cur: # Cursor is created here
            cur.execute(query, params)
            
            if query.strip().lower().startswith(('select', 'with')):
                if return_df:
                    if cur.description is not None:
                        columns = [desc[0] for desc in cur.description]
                        data = cur.fetchall()
                        return pd.DataFrame(data, columns=columns)
                    else:
                        return pd.DataFrame()
                else:
                    return cur.fetchall()
            else:
                conn.commit()
                return cur.rowcount
    except Exception as e:
        st.error(f"Erro na execução da query: {str(e)}")
        conn.rollback()
        return None
    finally:
        conn.close()

def create_tables():
    sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'create_tables.sql')
    with open(sql_path, 'r') as f:
        content = f.read()
        execute_query(content.strip())

def feed_tables():
    conn = get_connection()
    if not conn:
        return None

    with conn.cursor() as cur:
        check_query = "SELECT COUNT(*) FROM aero.empresas"
        cur.execute(check_query)
        count_empresas = cur.fetchone()[0]

        if count_empresas == 0:
            print("Table 'aero.empresas' is empty. Populating now...")
            empresas = df[['empresa_sigla', 'empresa_nome', 'empresa_nacionalidade']].drop_duplicates()
            empresas_dict = empresas.to_dict('index')
            for _, row in empresas_dict.items():
                query = """
                INSERT INTO aero.empresas (empresa_sigla, empresa_nome, empresa_nacionalidade)
                VALUES (%s, %s, %s)
                """
                execute_query(query, (row['empresa_sigla'], row['empresa_nome'], row['empresa_nacionalidade']))
            conn.commit()
            print("Table 'aero.empresas' populated successfully.")
        else:
            print(f"Table 'aero.empresas' already contains {count_empresas} rows. Skipping population.")
    
    with conn.cursor() as cur:
        check_query = "SELECT COUNT(*) FROM aero.aeroportos_origem"
        cur.execute(check_query)
        count_origem = cur.fetchone()[0]

        if count_origem == 0:
            print("Table 'aero.aeroportos_origem' is empty. Populating now...")
            aeroportos_origem = df[['aeroporto_origem_sigla', 'aeroporto_origem_nome', 'aeroporto_origem_pais']].drop_duplicates()
            aeroportos_origem_dict = aeroportos_origem.to_dict('index')
            for _, row in aeroportos_origem_dict.items():
                query = """
                INSERT INTO aero.aeroportos_origem (aeroporto_origem_sigla, aeroporto_origem_nome, aeroporto_origem_pais)
                VALUES (%s, %s, %s)
                ON CONFLICT (aeroporto_origem_sigla) DO NOTHING
                """
                execute_query(query, (row['aeroporto_origem_sigla'], row['aeroporto_origem_nome'], row['aeroporto_origem_pais']))
            conn.commit()
            print("Table 'aero.aeroportos_origem' populated successfully.")
        else:
            print(f"Table 'aero.aeroportos_origem' already contains {count_origem} rows. Skipping population.")

    with conn.cursor() as cur: 
        check_query = "SELECT COUNT(*) FROM aero.aeroportos_destino"
        cur.execute(check_query)
        count_destino = cur.fetchone()[0]

        if count_destino == 0:
            print("Table 'aero.aeroportos_destino' is empty. Populating now...")
            aeroportos_destino = df[['aeroporto_destino_sigla', 'aeroporto_destino_nome', 'aeroporto_destino_pais']].drop_duplicates()
            aeroportos_destino_dict = aeroportos_destino.to_dict('index')
            for _, row in aeroportos_destino_dict.items():
                query = """
                INSERT INTO aero.aeroportos_destino (aeroporto_destino_sigla, aeroporto_destino_nome, aeroporto_destino_pais)
                VALUES (%s, %s, %s)
                ON CONFLICT (aeroporto_destino_sigla) DO NOTHING
                """
                execute_query(query, (row['aeroporto_destino_sigla'], row['aeroporto_destino_nome'], row['aeroporto_destino_pais']))
            conn.commit()
            print("Table 'aero.aeroportos_destino' populated successfully.")

    
    with conn.cursor() as cur:
            check_query = "SELECT COUNT(*) FROM aero.voos"
            cur.execute(check_query)
            # Fetchone pode retornar None ou um tupla vazia, então verificamos isso.
            result_voos = cur.fetchone()
            count_voos = result_voos[0] if result_voos and len(result_voos) > 0 else 0

            if count_voos == 0:
                print("Tabela 'aero.voos' está vazia. Populando agora...")
                
                # Seleção de colunas do DataFrame para a tabela 'voos'.
                # As colunas 'carga_paga_km', 'carga_gratis_km', 'correio_km' foram removidas
                # pois não estavam na sua definição CREATE TABLE.
                voos_df = df[['empresa_sigla', 'aeroporto_origem_sigla', 'aeroporto_destino_sigla', 
                              'natureza', 'grupo_voo', 'passageiros_pagos', 'passageiros_gratis', 
                              'carga_paga_kg', 'carga_gratis_kg', 'correios_kg', 'ask', 'rpk', 'atk', 'rtk', 
                              'combustivel_litros', 'distancia_voada_km', 'decolagens',
                              'assentos', 'payload', 'HORAS_VOADAS', 'bagagem_kg', 
                              'ano', 'mes']].drop_duplicates()
                
                # Itera sobre cada linha do DataFrame para inserção
                for _, row in voos_df.iterrows():
                    query = """
                    INSERT INTO aero.voos (
                        empresa_id,             
                        aeroporto_origem_id,    
                        aeroporto_destino_id,   
                        ano, mes,
                        natureza, grupo_voo, passageiros_pagos, passageiros_gratis, carga_paga_kg,
                        carga_gratis_kg, correios_kg, ask, rpk, atk, rtk, combustivel_litros,
                        distancia_voada_km, decolagens, assentos, payload, HORAS_VOADAS, bagagem_kg
                    ) VALUES (
                        (SELECT id_empresas FROM aero.empresas WHERE empresa_sigla = %s), 
                        (SELECT id_aeroporto_origem FROM aero.aeroportos_origem WHERE aeroporto_origem_sigla = %s), 
                        (SELECT id_aeroporto_destino FROM aero.aeroportos_destino WHERE aeroporto_destino_sigla = %s), 
                        %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    );
                    """
                    execute_query(query, (
                        row['empresa_sigla'],        # Parâmetro para SELECT id_empresas
                        row['aeroporto_origem_sigla'], # Parâmetro para SELECT id_aeroporto_origem
                        row['aeroporto_destino_sigla'],# Parâmetro para SELECT id_aeroporto_destino
                        row['ano'],
                        row['mes'],
                        row['natureza'],
                        row['grupo_voo'],
                        row['passageiros_pagos'],
                        row['passageiros_gratis'],
                        row['carga_paga_kg'],
                        row['carga_gratis_kg'],
                        row['correios_kg'],
                        row['ask'],
                        row['rpk'],
                        row['atk'],
                        row['rtk'],
                        row['combustivel_litros'],
                        row['distancia_voada_km'],
                        row['decolagens'],
                        row['assentos'],
                        row['payload'],
                        row['HORAS_VOADAS'],
                        row['bagagem_kg']
                    ))
                conn.commit()
                print("Tabela 'aero.voos' populada com sucesso.")
            else:
                print(f"Tabela 'aero.voos' já contém {count_voos} linhas. Pulando população.")
    
    conn.close()