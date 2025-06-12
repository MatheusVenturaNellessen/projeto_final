import pandas as pd
import numpy as np
import streamlit as st

def spotify_csv_cleaning():
    
    df = pd.read_csv('database\\spotify\\spotify_2023.csv', sep=',', encoding='latin1', parse_dates=[['released_year', 'released_month', 'released_day']])
    df_bkp = df.copy()
    df = df.drop('key', axis=1)

    colunas_para_remover = ['danceability_%', 'valence_%', 'energy_%','liveness_%' , 'speechiness_%']
    df.drop(columns=colunas_para_remover, inplace=True)
    
    df['streams'] = pd.to_numeric(df['streams'], errors='coerce')

    df['in_deezer_playlists'] = df['in_deezer_playlists'].str.replace(',', '.', regex=False)
    df['in_deezer_playlists'] = pd.to_numeric(df['in_deezer_playlists'], errors='coerce')

    df['in_shazam_charts'] = df['in_shazam_charts'].str.replace(',', '.', regex=False)
    df['in_shazam_charts'] = pd.to_numeric(df['in_shazam_charts'], errors='coerce')

    df['in_shazam_charts'] = df['in_shazam_charts'].replace(r'^\s*$', np.nan, regex=True)
    df['in_shazam_charts'] = df['in_shazam_charts'].fillna(0)

    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.strip().str.upper()

    df.rename(columns={
        'released_year_released_month_released_day': 'data_lancamento',
        'track_name': 'nome_artistico',
        'artist(s)_name': 'nome_artista',
        'artist_count': 'qtd_artistas',
        'in_spotify_playlists': 'qtd_playlists_spotify',
        'in_spotify_charts': 'qtd_destaques_spotify',
        'streams': 'qtd_transmissoes',
        'in_apple_playlists': 'qtd_playlists_apple',
        'in_apple_charts': 'qtd_destaques_apple',
        'in_deezer_playlists': 'qtd_playlists_deezer',
        'in_deezer_charts': 'qtd_destques_deezer',
        'in_shazam_charts': 'qtd_destaues_shazam',
        'bpm': 'batidas_por_minuto',
        'mode': 'modo',
        'danceability_%': 'dancabilidade_%',
        'valence_%': 'valencia_%',
        'energy_%': 'energia_%',
        'acousticness_%': 'acustica_%',
        'instrumentalness_%': 'instrumentalidade_%',
        'liveness_%': 'vivacidade_%',
        'speechiness_%': 'oratoria_%'
        },
        inplace=True
    )

    # print(df.info()) # funcionou 

    df.to_csv('database\\spotify\\spotify_2023_tratado.csv', sep=',', encoding='utf-8', index=False)