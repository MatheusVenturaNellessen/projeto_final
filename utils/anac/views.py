import os
import psycopg2
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# Load DataFrame outside the function if it's used globally
df = pd.read_csv("database\\anac\\anaca_2025_limpo.csv" , sep=';', encoding='latin1')


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

def views_metricas_empresa():
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    query = """
        CREATE OR REPLACE VIEW vw_metricas_agregadas_ultimo_mes AS
        WITH ultimo_mes AS (
            SELECT 
                ano, mes
            FROM aero.voos
            ORDER BY ano DESC, mes DESC
            LIMIT 1
        ),
        base AS (
            SELECT v.*, e.empresa_sigla
            FROM aero.voos v
            JOIN aero.empresas e ON v.empresa_id = e.id_empresas
            WHERE (v.ano, v.mes) = (SELECT ano, mes FROM ultimo_mes)
        ),
        somas AS (
            SELECT
                empresa_sigla,
                SUM(rpk) AS rpk,
                SUM(ask) AS ask,
                SUM(rtk) AS rtk,
                SUM(atk) AS atk
            FROM base
            GROUP BY empresa_sigla
        )
        SELECT
            empresa_sigla,
            rpk,
            ask,
            rtk,
            atk,
            ROUND(100.0 * rpk / NULLIF(ask, 0), 2) AS load_factor,
            ROUND(100.0 * rtk / NULLIF(atk, 0), 2) AS eficiencia_carga
        FROM somas;
    """

    cursor.execute(query)
    conn.commit()
    
def get_view_dataframe():
    query = "SELECT * FROM vw_metricas_agregadas_ultimo_mes"
    return execute_query(query, return_df=True)
    
def select_view_rpk():
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    query = """
        SELECT empresa_sigla, rpk
        FROM vw_metricas_agregadas_ultimo_mes
        ORDER BY rpk DESC
        LIMIT 5;
    """
    print("Query RPK:\n", query.strip())
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=['empresa_sigla', 'rpk'])

def select_view_ask():
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    query = """
        SELECT empresa_sigla, ask
        FROM vw_metricas_agregadas_ultimo_mes
        ORDER BY ask DESC
        LIMIT 5;
    """
    print("Query ASK:\n", query.strip())
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=['empresa_sigla', 'ask'])

def select_view_rtk():
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    query = """
        SELECT empresa_sigla, rtk
        FROM vw_metricas_agregadas_ultimo_mes
        ORDER BY rtk DESC
        LIMIT 5;
    """
    print("Query RTK:\n", query.strip())
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=['empresa_sigla', 'rtk'])

def select_view_atk():
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    query = """
        SELECT empresa_sigla, atk
        FROM vw_metricas_agregadas_ultimo_mes
        ORDER BY atk DESC
        LIMIT 5;
    """
    print("Query ATK:\n", query.strip())
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=['empresa_sigla', 'atk'])

def select_view_loadfactor():
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    query = """
        SELECT empresa_sigla, rpk, ask
        FROM vw_metricas_agregadas_ultimo_mes
    """
    print("Query Load Factor (calculado no código):\n", query.strip())
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    
    df = pd.DataFrame(data, columns=['empresa_sigla', 'rpk', 'ask'])
    df['load_factor'] = 100 * df['rpk'] / df['ask'].replace(0, np.nan)
    df = df.dropna(subset=['load_factor'])
    return df.sort_values('load_factor', ascending=False).head(5)[['empresa_sigla', 'load_factor']]

def select_view_eficiencia_carga():
    conn = get_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    query = """
        SELECT empresa_sigla, eficiencia_carga
        FROM vw_metricas_agregadas_ultimo_mes
        ORDER BY eficiencia_carga DESC
        LIMIT 5;
    """
    print("Query Eficiência de Carga:\n", query.strip())
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=['empresa_sigla', 'eficiencia_carga'])
    
