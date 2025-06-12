import streamlit as st
import pandas as pd
from utils.anac.database import execute_query, create_tables, feed_tables
from utils.anac.analise import csv_cleaning
from utils.spottify.analise_spotify import spotify_csv_cleaning
from utils.spottify.database import create_tables_spotify, feed_tables_spotify


st.set_page_config(page_title="ANAC - Análise de Dados", page_icon=":bar_chart:", layout="wide")
df = pd.read_csv("database\\anac\\csv_anac_2025.csv", sep=';', encoding='latin1')


st.title("ANAC - Análise de Dados")
spotify_csv_cleaning()
csv_cleaning()
create_tables()
create_tables_spotify()
feed_tables()
feed_tables_spotify()

