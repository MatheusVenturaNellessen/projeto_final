import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

def esqueleto():
    st.sidebar.image("frontend\\image\\music.png", width=150)

    st.sidebar.markdown('''
        <h1 class="emoji-after">Navegue por aqui!</h1>
        <style>
            h1 {
                font-size: 3em;
                text-align: center; 
            }
            
            .emoji-after:hover::after {
                content: "👇"
            }
        </style>
    ''', unsafe_allow_html=True)

    page = st.sidebar.radio("Ir para:", ["Visão Geral", "Comparativo Entre Artistas"])

    if page == "Visão Geral":

        st.title("🎵 Visão Geral do Spotify 2023")
        st.markdown("Análise completa das músicas mais populares do Spotify em 2023")

        # Carregar dados
        @st.cache_data
        def load_data():
            df = pd.read_csv('database/spotify/spotify_2023_tratado.csv', sep=',', encoding='latin1')
            df['nome_artista'] = df['nome_artista'].str.strip()
            df['primeiro_artista'] = df['nome_artista'].str.split(',').str[0].str.strip()
            return df

        df = load_data()

        # Métricas gerais
        st.header("📊 Métricas Globais")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total de Músicas", len(df))

        with col2:
            st.metric("Artistas Únicos", df['primeiro_artista'].nunique())

        with col3:
            st.metric("BPM Médio", round(df['batidas_por_minuto'].mean(), 2))

        # Aplica o estilo azulzinho
        style_metric_cards()

        # Segunda linha de métricas
        col1, col2, col3 = st.columns(3)

        with col1:
            # Música mais popular (com mais transmissões)
            musica_popular = df.loc[df['qtd_transmissoes'].idxmax(), 'nome_artista']
            nome_musica_popular = df.loc[df['qtd_transmissoes'].idxmax(), 'nome_artistico']
            st.metric("Música Mais Popular", nome_musica_popular)

        with col2:
            # Artista mais popular (com maior número total de transmissões)
            artista_popular = df.groupby('primeiro_artista')['qtd_transmissoes'].sum().idxmax()
            st.metric("Artista Mais Popular", artista_popular)

        with col3:
            total_transmissoes = int(df['qtd_transmissoes'].sum())
            st.metric("Total de Transmissões", f"{total_transmissoes:,}".replace(",", "."))

        # Aplica estilo novamente se quiser aplicar à nova linha também
        style_metric_cards()

        # Top artistas
        st.header("🎤 Top Artistas (Número de músicas)")
        top_artistas = df['primeiro_artista'].value_counts().head(10)
        
        fig = px.bar(top_artistas, 
                        x=top_artistas.index, 
                        y=top_artistas.values,
                        labels={'x':'Artista', 'y':'Número de Músicas'},
                        color=top_artistas.values,
                        color_continuous_scale='Magma')
        st.plotly_chart(fig, use_container_width=True)

        tab1, tab2 = st.tabs(["📆 Popularidade por Década", "📱 Presença nas Plataformas"])

        with tab1:
            # 🎵 Popularidade por Década
            # Garante que a coluna data_lancamento é datetime
            df['data_lancamento'] = pd.to_datetime(df['data_lancamento'], errors='coerce')

            # Cria a coluna da década (ex: 1980, 1990, 2000...)
            df['decada'] = (df['data_lancamento'].dt.year // 10) * 10

            # Agrupa por década e soma as transmissões
            popularidade_decada = df.groupby('decada')['qtd_transmissoes'].sum().reset_index()

            # Converte década para string para exibição no eixo x
            popularidade_decada['decada'] = popularidade_decada['decada'].astype('Int64').astype(str) + 's'

            # Gráfico de barras com Plotly
            fig_decada = px.bar(
                popularidade_decada,
                x='decada',
                y='qtd_transmissoes',
                labels={'qtd_transmissoes': 'Transmissões', 'decada': 'Década'},
                title='Popularidade por Década',
                color='decada',
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            st.plotly_chart(fig_decada, use_container_width=True)

        with tab2:
            # 📱 Presença nas Plataformas
            st.header("")

            # Criando DataFrame com dados agregados por plataforma
            plataformas = pd.DataFrame({
                'Plataforma': ['Spotify', 'Apple', 'Deezer', 'Shazam'],
                'Playlists': [
                    df['qtd_playlists_spotify'].sum(),
                    df['qtd_playlists_apple'].sum(),
                    df['qtd_playlists_deezer'].sum(),
                    0  # Shazam não tem dados de playlists
                ],
                'Destaques': [
                    df['qtd_destaques_spotify'].sum(),
                    df['qtd_destaques_apple'].sum(),
                    df['qtd_destques_deezer'].sum(),
                    df['qtd_destaues_shazam'].sum()
                ]
            })
            col1, col2 = st.columns(2)
            with col1:
                # Gráfico de pizza - Distribuição de Playlists
                fig_playlists = px.pie(
                    plataformas,
                    names='Plataforma',
                    values='Playlists',
                    title='Distribuição de Playlists por Plataforma'
                )
                st.plotly_chart(fig_playlists, use_container_width=True)

            with col2:
                # Gráfico de pizza - Distribuição de Destaques
                fig_destaques = px.pie(
                    plataformas,
                    names='Plataforma',
                    values='Destaques',
                    title='Distribuição de Destaques por Plataforma'
                )
                st.plotly_chart(fig_destaques, use_container_width=True)


# =================================================================================================================================================================================== #


    if page == "Comparativo Entre Artistas":
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