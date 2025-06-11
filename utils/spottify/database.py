import os
import psycopg2
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
from utils.anac.database import execute_query, get_connection
import numpy as np

df = pd.read_csv("C:\\Users\\leona\\projeto_final\\database\\spotify\\spotify_2023_tratado.csv", sep=',', encoding='latin1')

def create_tables_spotify():
    sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'C:\\Users\\leona\\projeto_final\\scripts\\spotify', 'create_tables_spotify.sql')
    with open(sql_path, 'r') as f:
        content = f.read()
        execute_query(content.strip())
        
def feed_tables_spotify():
    conn = get_connection()
    if not conn:
        return None
    
    with conn.cursor() as cur:
     
    # Verifica se a tabela já contém dados
        check_query = "SELECT COUNT(*) FROM spotify.artistas"
        cur.execute(check_query)
        count_artistas = cur.fetchone()[0]

        if count_artistas == 0:
            print("Tabela 'spotify.artistas' está vazia. Populando agora...")

            artistas = df['nome_artista'].str.split(',')
            artistas = artistas.explode().str.strip() 

            for a in artistas:
                query = """
                INSERT INTO spotify.artistas (nome_artista)
                VALUES (%s)
                """
                execute_query(query, (a,))

            conn.commit()
            print("Tabela 'spotify.artistas' populada com sucesso.")
        else:
            print(f"Tabela 'spotify.artistas' já contém {count_artistas} registros. Pulando inserção.")
            
            
    with conn.cursor() as cur:
        check_query = "SELECT COUNT(*) FROM spotify.musicas"
        cur.execute(check_query)
        count_musicas = cur.fetchone()[0] 
        if count_musicas == 0:
            print("Populando 'spotify.musicas'...")

            musicas = df[['nome_artistico', 'data_lancamento','modo']].drop_duplicates()
            musicas_dict = musicas.to_dict('index')
            
            
            for _, row in musicas_dict.items():
                query = """
                INSERT INTO spotify.musicas (nome_artistico, data_lancamento, modo)
                VALUES (%s, %s, %s)
                RETURNING id_musica;
                """
                execute_query(query, (
                    row['nome_artistico'],
                    row['data_lancamento'],
                    row['modo']
                ))

            conn.commit()
            print("Tabela 'spotify.musicas' populada com sucesso.")
        else:
            print(f"Tabela 'spotify.musicas' já contém {count_musicas} registros. Pulando inserção.")
            

    with conn.cursor() as cur:
        check_query = "SELECT COUNT(*) FROM spotify.musicas_artistas"
        cur.execute(check_query)
        count_musica_artistas = cur.fetchone()[0]

        if count_musica_artistas == 0:
            print("Populando 'spotify.musicas_artistas'...")

            relacoes = df[['nome_artistico', 'nome_artista']].drop_duplicates()
            relacoes['nome_artista'] = relacoes['nome_artista'].str.split(',')
            relacoes = relacoes.explode('nome_artista')
            relacoes['nome_artista'] = relacoes['nome_artista'].str.strip()
            relacoes['nome_artistico'] = relacoes['nome_artistico'].str.strip()

            for _, row in relacoes.iterrows():
                nome_musica = row['nome_artistico'].strip().lower()
                nome_artista = row['nome_artista'].strip().lower()

                # Buscar id da música
                cur.execute("SELECT id_musica FROM spotify.musicas WHERE LOWER(nome_artistico) = %s", (nome_musica,))
                musica_result = cur.fetchone()

                # Buscar id do artista
                cur.execute("SELECT id_artista FROM spotify.artistas WHERE LOWER(nome_artista) = %s", (nome_artista,))
                artista_result = cur.fetchone()

                if musica_result and artista_result:
                    id_musica = musica_result[0]
                    id_artista = artista_result[0]

                    insert_query = """
                    INSERT INTO spotify.musicas_artistas (id_musica, id_artista)
                    VALUES (%s, %s)
                    ON CONFLICT (id_musica, id_artista) DO NOTHING
                    """
                    execute_query(insert_query, (id_musica, id_artista))
                else:
                    print(f"❗ Não encontrado: Música '{row['nome_artistico']}' ou Artista '{row['nome_artista']}'")

            conn.commit()
            print("Tabela 'spotify.musica_artistas' populada com sucesso.")
        else:
            print(f"Tabela 'spotify.musica_artistas' já contém {count_musica_artistas} registros. Pulando inserção.")

    with conn.cursor() as cur:
        check_query = "SELECT COUNT(*) FROM spotify.plataformas"
        cur.execute(check_query)
        count_plataformas = cur.fetchone()[0]

        if count_plataformas == 0:
            print("Populando 'spotify.plataformas'...")

            plataformas = df[[
                'nome_artistico',
                'qtd_playlists_spotify',
                'qtd_destaques_spotify',
                'qtd_playlists_apple',
                'qtd_destaques_apple',
                'qtd_playlists_deezer',
                'qtd_destques_deezer',
                'qtd_destaues_shazam'
            ]].drop_duplicates()

            for _, row in plataformas.iterrows():
                nome_musica = row['nome_artistico'].strip().lower()
                cur.execute(
                    "SELECT id_musica FROM spotify.musicas WHERE LOWER(nome_artistico) = %s",
                    (nome_musica,)
                )
                musica_result = cur.fetchone()

                if musica_result:
                    id_musica = musica_result[0]
                    query = """
                    INSERT INTO spotify.plataformas (
                        id_musica, qtd_playlists_spotify, qtd_destaques_spotify,
                        qtd_playlists_apple, qtd_destaques_apple,
                        qtd_playlists_deezer, qtd_destaques_deezer,
                        qtd_destaques_shazam
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id_musica) DO NOTHING
                    """
                    execute_query(query, (
                        id_musica,
                        row['qtd_playlists_spotify'],
                        row['qtd_destaques_spotify'],
                        row['qtd_playlists_apple'],
                        row['qtd_destaques_apple'],
                        row['qtd_playlists_deezer'],
                        row['qtd_destques_deezer'],
                        row['qtd_destaues_shazam']
                    ))
                else:
                    print(f"❗ Música não encontrada para plataformas: '{row['nome_artistico']}'")

            conn.commit()
            print("Tabela 'spotify.plataformas' populada com sucesso.")
        else:
            print(f"Tabela 'spotify.plataformas' já contém {count_plataformas} registros. Pulando inserção.")

    with conn.cursor() as cur:
        check_query = "SELECT COUNT(*) FROM spotify.transmissoes"
        cur.execute(check_query)
        count_transmissoes = cur.fetchone()[0]

        if count_transmissoes == 0:
            print("Populando 'spotify.transmissoes'...")

            transmissoes = df[['nome_artistico', 'qtd_transmissoes']].drop_duplicates()

            for _, row in transmissoes.iterrows():
                nome_musica = row['nome_artistico'].strip().lower()
                cur.execute(
                    "SELECT id_musica FROM spotify.musicas WHERE LOWER(nome_artistico) = %s",
                    (nome_musica,)
                )
                musica_result = cur.fetchone()

                if musica_result:
                    id_musica = musica_result[0]
                    query = """
                    INSERT INTO spotify.transmissoes (id_musica, qtd_transmissoes)
                    VALUES (%s, %s)
                    """
                    execute_query(query, (id_musica, row['qtd_transmissoes']))
                else:
                    print(f"❗ Música não encontrada para transmissoes: '{row['nome_artistico']}'")

            conn.commit()
            print("Tabela 'spotify.transmissoes' populada com sucesso.")
        else:
            print(f"Tabela 'spotify.transmissoes' já contém {count_transmissoes} registros. Pulando inserção.")
