import streamlit as st
import pandas as pd
from utils.database import execute_query, create_tables
from utils.analise import csv_cleaning


st.set_page_config(page_title="ANAC - Análise de Dados", page_icon=":bar_chart:", layout="wide")
df = pd.read_csv("C:\\Users\\leona\\projeto_final\\database\\csv_limpo_anac_2025.csv", sep=';', encoding='latin1')

st.write(df.columns.tolist())
csv_cleaning()
create_tables()
# feed_tables()

st.title("ANAC - Análise de Dados")
