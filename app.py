import streamlit as st
import pandas as pd
from utils.database import execute_query, create_tables, feed_tables
from utils.analise import csv_cleaning
import frontend.dashboard as ds


st.set_page_config(page_title="ANAC - Análise de Dados", page_icon=":bar_chart:", layout="wide")
df = pd.read_csv("C:\\Users\\Aluno\\Downloads\\projeto_final_anac\\database\\csv_anac_2025.csv", sep=';', encoding='latin1')

st.write(df.columns.tolist())
csv_cleaning()
create_tables()
feed_tables()

st.markdown(
    """
    <h1 style='text-align: center;'>
        ANAC - Análise de Dados
    </h1>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    fig_nacionalidade = ds.nacionalidade()
    if fig_nacionalidade:
        st.pyplot(fig_nacionalidade)

with col2:
    st.write()