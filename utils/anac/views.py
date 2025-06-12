import os
import psycopg2
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pandas as pd

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
    