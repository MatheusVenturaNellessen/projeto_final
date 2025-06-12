import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

def esqueleto():
    # CSS personalizado
    st.markdown("""
    <style>
    /* Estilo das abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        margin-bottom: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        padding: 0 15px;
        background-color: #f0f2f6;
        border-radius: 8px;
        border: none;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4a8cff;
        color: white !important;
    }
    /* Divisão entre colunas */
    [data-testid="column"]:first-child {
        border-right: 1px solid #e0e0e0;
        padding-right: 15px;
    }
    /* Cards de métricas */
    [data-testid="metric-container"] {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 10px;
    }
    /* Container principal */
    .main-container {
        padding: 0 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Carregar dados
    @st.cache_data
    def load_data():
        df = pd.read_csv('database/spotify/spotify_2023_tratado.csv', sep=',', encoding='latin1')
        df['nome_artista'] = df['nome_artista'].str.strip()
        df['primeiro_artista'] = df['nome_artista'].str.split(',').str[0].str.strip()
        return df

    df = load_data()
    artistas_unicos = sorted(df['primeiro_artista'].unique())

    # Layout principal
    st.title("🎵 Comparador de Artistas Spotify")
    st.caption("Selecione dois artistas para comparar suas métricas e desempenho")

    colA, colB = st.columns(2, gap="medium")

    # Coluna A - Artista 1 (Estilo Magenta)
    with colA:
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Seletor de artista
        artista_esquerda = st.selectbox(
            "**Selecione o primeiro artista:**",
            artistas_unicos,
            key="artista1"
        )
        
        st.markdown(f"# 🎤 {artista_esquerda}")
        
        # Filtrar dados
        df_esquerda = df[df['primeiro_artista'] == artista_esquerda]
        
        # Músicas do artista
        with st.expander("🔍 Ver músicas", expanded=True):
            for _, row in df_esquerda.iterrows():
                outros_artistas = [a.strip() for a in row['nome_artista'].split(',') if a.strip() != artista_esquerda]
                feat = f" _(com {', '.join(outros_artistas)})_" if outros_artistas else ""
                st.markdown(f"- **{row['nome_artistico']}**{feat}")
        
        # Sistema de abas para gráficos
        st.markdown("#### 📈 Visualizações")
        tab1, tab2, tab3 = st.tabs(["📊 Metricas", "📌 Destaques", "📊 Desempenho"])

        with tab1:
            # Primeira linha de métricas
            st.markdown('<div class="metric-row">', unsafe_allow_html=True)
            cols = st.columns(3)
            cols[0].metric("BPM Médio", round(df_esquerda['batidas_por_minuto'].mean(), 2))
            cols[1].metric("Acústica", f"{round(df_esquerda['acustica_%'].mean(), 1)}%")
            cols[2].metric("Instrumental", f"{round(df_esquerda['instrumentalidade_%'].mean(), 1)}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Segunda linha de métricas adicionais
            st.markdown('<div class="metric-row">', unsafe_allow_html=True)
            cols2 = st.columns(2)
            total_charts = (df_esquerda['qtd_destaques_spotify'].sum() + 
                          df_esquerda['qtd_destaques_apple'].sum() + 
                          df_esquerda['qtd_destques_deezer'].sum() + 
                          df_esquerda['qtd_destaues_shazam'].sum())
            
            total_playlists = (df_esquerda['qtd_playlists_spotify'].sum() + 
                              df_esquerda['qtd_playlists_apple'].sum() + 
                              df_esquerda['qtd_playlists_deezer'].sum())
            
            cols2[0].metric("Total em Charts", total_charts)
            cols2[1].metric("Total em Playlists", total_playlists)
            st.markdown('</div>', unsafe_allow_html=True)
            
            style_metric_cards(border_left_color="#9c42f5")
        
        with tab2:
            # Gráfico de playlists
            df_playlists = pd.DataFrame({
                'Plataforma': ['Spotify', 'Apple', 'Deezer'],
                'Playlists': [
                    df_esquerda['qtd_playlists_spotify'].sum(),
                    df_esquerda['qtd_playlists_apple'].sum(),
                    df_esquerda['qtd_playlists_deezer'].sum()
                ]
            })
            fig1 = px.bar(
                df_playlists,
                x='Plataforma',
                y='Playlists',
                color='Plataforma',
                color_discrete_sequence=px.colors.sequential.Magenta_r,
                title='Playlists por Plataforma'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with tab3:
            # Gráfico de destaques
            df_destaques = pd.DataFrame({
                'Plataforma': ['Spotify', 'Apple', 'Deezer', 'Shazam'],
                'Destaques': [
                    df_esquerda['qtd_destaques_spotify'].sum(),
                    df_esquerda['qtd_destaques_apple'].sum(),
                    df_esquerda['qtd_destques_deezer'].sum(),
                    df_esquerda['qtd_destaues_shazam'].sum()
                ]
            })
            fig2 = px.bar(
                df_destaques,
                x='Plataforma',
                y='Destaques',
                color='Plataforma',
                color_discrete_sequence=px.colors.sequential.Magenta_r,
                title='Aparições em Charts'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Coluna B - Artista 2 (Estilo Azul)
    with colB:
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Seletor de artista
        artista_direita = st.selectbox(
            "**Selecione o segundo artista:**",
            artistas_unicos,
            key="artista2"
        )
        
        st.markdown(f"# 🎤 {artista_direita}")
        
        # Filtrar dados
        df_direita = df[df['primeiro_artista'] == artista_direita]
        
        # Músicas do artista
        with st.expander("🔍 Ver músicas", expanded=True):
            for _, row in df_direita.iterrows():
                outros_artistas = [a.strip() for a in row['nome_artista'].split(',') if a.strip() != artista_direita]
                feat = f" _(com {', '.join(outros_artistas)})_" if outros_artistas else ""
                st.markdown(f"- **{row['nome_artistico']}**{feat}")

        # Sistema de abas para gráficos
        st.markdown("#### 📈 Visualizações")
        tab1, tab2, tab3 = st.tabs(["📊 Métricas", "📌 Destaques", "📊 Desempenho"])
        
        with tab1:
            # Primeira linha de métricas
            st.markdown('<div class="metric-row">', unsafe_allow_html=True)
            cols = st.columns(3)
            cols[0].metric("BPM Médio", round(df_direita['batidas_por_minuto'].mean(), 2))
            cols[1].metric("Acústica", f"{round(df_direita['acustica_%'].mean(), 1)}%")
            cols[2].metric("Instrumental", f"{round(df_direita['instrumentalidade_%'].mean(), 1)}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Segunda linha de métricas adicionais
            st.markdown('<div class="metric-row">', unsafe_allow_html=True)
            cols2 = st.columns(2)
            total_charts = (df_direita['qtd_destaques_spotify'].sum() + 
                          df_direita['qtd_destaques_apple'].sum() + 
                          df_direita['qtd_destques_deezer'].sum() + 
                          df_direita['qtd_destaues_shazam'].sum())
            
            total_playlists = (df_direita['qtd_playlists_spotify'].sum() + 
                              df_direita['qtd_playlists_apple'].sum() + 
                              df_direita['qtd_playlists_deezer'].sum())
            
            cols2[0].metric("Total em Charts", total_charts)
            cols2[1].metric("Total em Playlists", total_playlists)
            st.markdown('</div>', unsafe_allow_html=True)
            
            style_metric_cards(border_left_color="#4287f5")

        with tab2:
            # Gráfico de playlists
            df_playlists = pd.DataFrame({
                'Plataforma': ['Spotify', 'Apple', 'Deezer'],
                'Playlists': [
                    df_direita['qtd_playlists_spotify'].sum(),
                    df_direita['qtd_playlists_apple'].sum(),
                    df_direita['qtd_playlists_deezer'].sum()
                ]
            })
            fig1 = px.bar(
                df_playlists,
                x='Plataforma',
                y='Playlists',
                color='Plataforma',
                color_discrete_sequence=px.colors.sequential.Blues_r,
                title='Playlists por Plataforma'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with tab3:
            # Gráfico de destaques
            df_destaques = pd.DataFrame({
                'Plataforma': ['Spotify', 'Apple', 'Deezer', 'Shazam'],
                'Destaques': [
                    df_direita['qtd_destaques_spotify'].sum(),
                    df_direita['qtd_destaques_apple'].sum(),
                    df_direita['qtd_destques_deezer'].sum(),
                    df_direita['qtd_destaues_shazam'].sum()
                ]
            })
            fig2 = px.bar(
                df_destaques,
                x='Plataforma',
                y='Destaques',
                color='Plataforma',
                color_discrete_sequence=px.colors.sequential.Blues_r,
                title='Aparições em Charts'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Rodar a aplicação
if __name__ == "__main__":
    esqueleto()