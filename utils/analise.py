import pandas as pd
import numpy as np
import streamlit as st

def csv_cleaning():
    df = pd.read_csv('C:\\Users\\leona\\projeto_final\\database\\csv_anac_2025.csv', sep=';', encoding='latin1')

    df_bkp = df.copy()

    df = df.drop(['AEROPORTO DE ORIGEM (UF)', 
                  'AEROPORTO DE ORIGEM (REGIÃO)', 
                  'AEROPORTO DE ORIGEM (CONTINENTE)', 
                  'AEROPORTO DE DESTINO (UF)', 
                  'AEROPORTO DE DESTINO (REGIÃO)', 
                  'AEROPORTO DE DESTINO (CONTINENTE)'], axis=1)
 
    df['HORAS VOADAS'] = df['HORAS VOADAS'].str.replace(',', '.', regex=False)
    df['HORAS VOADAS'] = pd.to_numeric(df['HORAS VOADAS'], errors='coerce')

    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.strip().str.upper()

    df = df.fillna(0) # os valores nulos foram preenchidos por 0
  
    df.rename(columns={
        "EMPRESA (SIGLA)": 'empresa_sigla',
        "EMPRESA (NOME)": 'empresa_nome',
        "EMPRESA (NACIONALIDADE)": 'empresa_nacionalidade',
        "AEROPORTO DE ORIGEM (SIGLA)": 'aeroporto_origem_sigla',
        "AEROPORTO DE ORIGEM (NOME)": 'aeroporto_origem_nome',
        "AEROPORTO DE ORIGEM (PAÍS)": 'aeroporto_origem_pais',
        "AEROPORTO DE DESTINO (SIGLA)": 'aeroporto_destino_sigla',
        "AEROPORTO DE DESTINO (NOME)": 'aeroporto_destino_nome',
        "AEROPORTO DE DESTINO (PAÍS)": 'aeroporto_destino_pais',
        "NATUREZA": 'natureza',
        "GRUPO DE VOO": 'grupo_voo',
        "PASSAGEIROS PAGOS": 'passageiros_pagos',
        "PASSAGEIROS GRÁTIS": 'passageiros_gratis',
        "CARGA PAGA (KG)": 'carga_paga_kg',
        "CARGA GRÁTIS (KG)": 'carga_gratis_kg',
        "CORREIO (KG)": 'correios_kg',
        "ASK": 'ask',
        "RPK": 'rpk',
        "ATK": 'atk',
        "RTK": 'rtk',
        "COMBUSTÍVEL (LITROS)": 'combustivel_litros',
        "DISTÂNCIA VOADA (KM)": 'distancia_voada_km',
        "DECOLAGENS": 'decolagens',
        "CARGA PAGA KM": 'carga_paga_km',
        "CARGA GRATIS KM": 'carga_gratis_km',
        "CORREIO KM": 'correio_km',
        "ASSENTOS": 'assentos',
        "PAYLOAD": 'payload',
        "HORAS VOADAS": 'horas_voadas',
        "BAGAGEM (KG)": 'bagagem_kg',
        'HORAS VOADAS': 'HORAS_VOADAS',
        'ANO': 'ano',
        'MÊS': 'mes'
    }, inplace=True)

    df_not_tratado = df.copy()

    df_not_tratado.to_csv('database/anac_2025_sem_tratar_outliers.csv', sep=';', encoding='latin1', index=False)
    st.write("Arquivo CSV sem tratamento de outliers salvo como 'anac_2025_sem_tratar_outliers.csv'.")
    st.dataframe(df_not_tratado)

