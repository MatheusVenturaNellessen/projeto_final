import pandas as pd

def csv_cleaning():
    
    df_anac = pd.read_csv('database/csv_anac_2025.csv', sep=';', encoding='latin1')

    df_anac['HORAS VOADAS'] = df_anac['HORAS VOADAS'].str.replace(',', '.', regex=False)
    df_anac['HORAS VOADAS'] = pd.to_numeric(df_anac['HORAS VOADAS'], errors='coerce')
    df_anac['ANO'] = pd.to_datetime(df_anac['ANO'], errors='coerce')
    df_anac['MÊS'] = pd.to_datetime(df_anac['MÊS'], errors='coerce')

    df_anac.rename(columns={
        "EMPRESA (SIGLA)": 'empresa_sigla',
        "EMPRESA (NOME)": 'empresa_nome',
        "EMPRESA (NACIONALIDADE)": 'empresa_nacionalidade',
        "AEROPORTO DE ORIGEM (SIGLA)": 'aeroporto_origem_sigla',
        "AEROPORTO DE ORIGEM (NOME)": 'aeroporto_origem_nome',
        "AEROPORTO DE ORIGEM (UF)": 'aeroporto_origem_uf',
        "AEROPORTO DE ORIGEM (REGIÃO)": 'aeroporto_origem_regiao',
        "AEROPORTO DE ORIGEM (PAÍS)": 'aeroporto_origem_pais',
        "AEROPORTO DE ORIGEM (CONTINENTE)": 'aeroporto_origem_continente',
        "AEROPORTO DE DESTINO (SIGLA)": 'aeroporto_destino_sigla',
        "AEROPORTO DE DESTINO (NOME)": 'aeroporto_destino_nome',
        "AEROPORTO DE DESTINO (UF)": 'aeroporto_destino_uf',
        "AEROPORTO DE DESTINO (REGIÃO)": 'aeroporto_destino_regiao',
        "AEROPORTO DE DESTINO (PAÍS)": 'aeroporto_destino_pais',
        "AEROPORTO DE DESTINO (CONTINENTE)": 'aeroporto_destino_continente',
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




    # print('Quantidade de valores nulos em cada Serie/coluna:\n')
    # print(df_anac.isna().sum())
    # print('-------------------------------------------------')

    # print('Percentual de valores nulos por Serie/coluna:\n')
    # print(df_anac.isna().mean() * 100)
    # print('-------------------------------------------------')

    # df_anac = df_anac.dropna()

    # print(df_anac.info())

    df_anac.to_csv('database/csv_limpo_anac_2025.csv', sep=';', encoding='latin1')
    return df_anac