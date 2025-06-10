import os
import psycopg2
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pandas as pd

df = pd.read_csv("C:\\Users\\leona\\projeto_final\\database\\csv_anac_2025.csv" , sep=';', encoding='latin1')

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
        with conn.cursor() as cur:
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
    st.write()