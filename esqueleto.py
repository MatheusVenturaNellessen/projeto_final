import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from utils.anac.database import get_connection

def pagina_artistas():
    st.title("🎤 Músicas por Artista")

    conn = get_connection()
    if not conn:
        st.error("Erro ao conectar ao banco de dados.")
        return

    # Obter lista de artistas
    with conn.cursor() as cur:
        cur.execute("SELECT id_artista, nome_artista FROM spotify.artistas ORDER BY nome_artista")
        artistas = cur.fetchall()

    if not artistas:
        st.warning("Nenhum artista encontrado no banco.")
        return

    artistas_dict = {nome: id for id, nome in artistas}
    nome_artista = st.selectbox("Selecione um artista:", list(artistas_dict.keys()))

    if nome_artista:
        id_artista = artistas_dict[nome_artista]

        # Buscar músicas do artista
        query = """
        SELECT m.nome_artistico
        FROM spotify.musicas m
        JOIN spotify.musicas_artistas ma ON m.id_musica = ma.id_musica
        WHERE ma.id_artista = %s
        ORDER BY m.nome_artistico;
        """
        with conn.cursor() as cur:
            cur.execute(query, (id_artista,))
            musicas = cur.fetchall()

        if musicas:
            df_musicas = pd.DataFrame(musicas, columns=["Música"])
            st.write(f"🎶 Músicas de **{nome_artista}**:")
            st.dataframe(df_musicas, use_container_width=True)
        else:
            st.info("Este artista não possui músicas cadastradas.")