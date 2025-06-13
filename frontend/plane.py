import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_folium import st_folium
import folium
from utils.anac.views import (
    select_view_rpk,
    select_view_ask,
    select_view_rtk,
    select_view_atk,
    select_view_loadfactor,
    select_view_eficiencia_carga
)

# ============== CONFIG E DADOS ==============
def plane():
    st.markdown("""
        <style>
            .container {
                background-color: white;
                border-radius: 15px;
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                margin: 10px; padding: 20px;
                text-align: center;
            }
            
            .container:hover {
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                border-left: 5px solid #302681;
                cursor: pointer;
                transition: filter box-shadow 0.5s ease; 
            }

            .title {
                font-size: 1.1em;
                font-weight: 900;
                text-align: left;   
            }
                
            .text {
                color: #29846A;
                font-size: 2.5em;
                font-weight: 600;
            }
                
            .subtext {
                color: #29846A;
                font-size: 2em;
                font-weight: 600;
            }
            
            .info {
                color: #302681;
                font-size: 1em;
                font-weight: 600;
                text-align: center;    
            }
                
            .container-m {
                background-color: white;
                border-radius: 15px;
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                margin: 5px; padding: 10px;
                text-align: center;
            }
            
            .container-m:hover {
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                border-left: 5px solid #302681;
                cursor: pointer;
                transition: filter box-shadow 0.5s ease;  
            }

            .title-m {
                font-size: 1.5em;
                font-weight: 900;  
                text-align: left;    
 
            }
                
            .text-m {
                color: #29846A;
                font-size: 3.5em;
                font-weight: 600;
            }
            
            .info-m {
                color: #302681;
                font-size: 1em;
                font-weight: 600;
                text-align: center;    
            }

            h1 {
                font-size: 3em;
                text-align: center; 
            }
                
            h2 {
                text-align: center;         
            }

            .emoji-after:hover::after {
                content: "👇"
            }
                
            .g-title {
                text-align: center;
            }            
            
            .col1:hover::after {
                content: "Quantidade total de registros.";
            }
                
            .col2:hover::after {
                content: "Voos internacionais que chegam (+) e partem (-) do Brasil."
            }
            
            .col6:hover::after {
                content: "Voos que chegam (+) e partem (-).";    
            }
                
            .col7:hover::after {
                content: "Total de passageiros transportados.";    
            }
                
            .col8:hover::after {
                content: "Total de combustível consumido.";    
            }
                
            .col9:hover::after {
                content: "Total de passageiros vs. pela distância voada.";    
            }
            
            .col10:hover::after {
                content: "Capacidade total de transporte de passageiros.";    
            }
            
            .col11:hover::after {
                content: "Porcentagem de ocupação dos assentos disponíveis.";    
            }
            
            .col12:hover::after {
                content: "Porcentagem da capacidade total de carga utilizada.";    
            }
            
            .info-page {
                text-align: justify;   
            }
        </style>
    """, unsafe_allow_html=True)

    df = pd.read_csv("database\\anac\\anaca_2025_limpo.csv", sep=';', encoding='latin1')

    df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
    df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
    df['data'] = pd.to_datetime(df['ano'].astype(str) + '-' + df['mes'].astype(str) + '-01', errors='coerce')
    df = df.dropna(subset=['data']).reset_index(drop=True)

    df['fator_ocupacao'] = df['rpk'] / df['ask']
    df['fator_carga'] = df['rtk'] / df['atk']
    df['passageiros_por_decolagem'] = (df['passageiros_pagos'] / df['decolagens']).where(df['decolagens'] != 0)
    df['carga_total_kg'] = df['carga_paga_kg'] + df['carga_gratis_kg'] + df['correios_kg']
    df['carga_por_voo'] = (df['carga_total_kg'] / df['decolagens']).where(df['decolagens'] != 0)
    df['combustivel_por_passageiro'] = (df['combustivel_litros'] / df['passageiros_pagos']).where(df['passageiros_pagos'] != 0)
    df['distancia_por_voo'] = (df['distancia_voada_km'] / df['decolagens']).where(df['decolagens'] != 0)
    df['assentos_por_voo'] = (df['assentos'] / df['decolagens']).where(df['decolagens'] != 0)
    df['payload_efficiency'] = (df['payload'] / (df['ask'] + df['atk'])).where((df['ask'] + df['atk']) != 0)

    # ============= SIDEBAR INICIAL =============
    st.sidebar.image("frontend\\image\\plane.png", width=150)

    st.sidebar.markdown('''<h1 class="emoji-after">Navegue por aqui!</h1>''', unsafe_allow_html=True)
    page = st.sidebar.radio("Ir para:", ["Visão Geral", "Métricas", "Análises Gráficas", "Insights", "Informações"])

    # ============= VISÃO GERAL =============
    if page == "Visão Geral":
        st.markdown('''
            <h1>✈️ Visão Geral das Operações Aéreas</h1>
        ''', unsafe_allow_html=True)

        empresas_brasileiras = df[df['empresa_nacionalidade'] == 'BRASILEIRA']['empresa_sigla'].unique()
        empresas_estrangeiras = df[df['empresa_nacionalidade'] == 'ESTRANGEIRA']['empresa_sigla'].unique()
        qtd_brasileiras = len(empresas_brasileiras)
        qtd_estrangeiras = len(empresas_estrangeiras)

        todos_os_aeroportos = pd.concat([df['aeroporto_origem_nome'], df['aeroporto_destino_nome']])
        aeroportos_mais_frequentes = todos_os_aeroportos.value_counts()
        aeroporto_top1_nome = aeroportos_mais_frequentes.index[0]
        aeroporto_top1_qtd = aeroportos_mais_frequentes.iloc[0]

        voos_entrando = df[(df['aeroporto_destino_pais'] == 'BRASIL') & (df['aeroporto_origem_pais'] != 'BRASIL')]
        voos_saindo = df[(df['aeroporto_origem_pais'] == 'BRASIL') & (df['aeroporto_destino_pais'] != 'BRASIL')]
        qtd_entrando = len(voos_entrando)
        qtd_saindo = len(voos_saindo)

        df_gru = df[
            (df["aeroporto_origem_nome"].str.contains("GUARULHOS", case=False, na=False)) |
            (df["aeroporto_destino_nome"].str.contains("GUARULHOS", case=False, na=False))
        ]

        voos_entrando_gru = df_gru[df_gru['aeroporto_destino_nome'].str.contains("GUARULHOS", case=False, na=False)]
        voos_saindo_gru = df_gru[df_gru['aeroporto_origem_nome'].str.contains("GUARULHOS", case=False, na=False)]

        total_passageiros_gru = df_gru['passageiros_pagos'].sum() + df_gru['passageiros_gratis'].sum()

        total_combustivel_gru = df_gru['combustivel_litros'].sum()



        qtd_registros = df.shape[0]

        # qtd_passageiros_total = df['passageiros_pagos'].sum() + df['passageiros_gratis'].sum()

        qtd_combustivel_total = df['combustivel_litros'].sum()
        total_carga_kg = df['carga_paga_kg'].sum()

        # qtd_distancia_voada_total = df['distancia_voada_km'].sum() if 'distancia_voada_km' in df.columns else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'''
                <div class="container">
                    <div class="title">Quantidade total de voos</div>
                    <div class="text">{qtd_registros:,.0f}</div>
                    <div class="info col1">ⓘ </div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
                <div class="container">
                    <div class="title">Voos brasileiros</div>
                    <div class="text">{qtd_entrando:,.0f} + | {qtd_saindo:,.0f} -</div>
                    <div class="info col2">ⓘ </div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
                <div class="container">
                    <div class="title">Total de combustível (L)</div>
                    <div class="text">{qtd_combustivel_total:,.0f}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
                <div class="container">
                    <div class="title">Total de carga (Kg)</div>
                    <div class="text">{total_carga_kg:,.0f}</div>
                </div>
            ''', unsafe_allow_html=True)
            
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.markdown(f'''
                <div class="container">
                    <div class="title">Aeroporto mais frequentado</div>
                    <div class="text">{aeroporto_top1_nome}</div>
                </div>
            ''', unsafe_allow_html=True)

        with col6:
            st.markdown(f'''
                <div class="container">
                    <div class="title">Voos de {aeroporto_top1_nome}</div>
                    <div class="text">{len(voos_entrando_gru):,.0f} + | {len(voos_saindo_gru):,.0f} -</div>
                    <div class="info col6">ⓘ </div>
                </div>
            ''', unsafe_allow_html=True)

        with col7:
            st.markdown(f'''
                <div class="container">
                    <div class="title">Passageiros em {aeroporto_top1_nome}</div>
                    <div class="text">{int(total_passageiros_gru):,.0f}</div>
                    <div class="info col7">ⓘ </div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col8:
            st.markdown(f'''
                <div class="container">
                    <div class="title">Combustível em {aeroporto_top1_nome} (L)</div>
                    <div class="text">{int(total_combustivel_gru):,.0f}</div>
                    <div class="info col8">ⓘ </div>
                </div>
            ''', unsafe_allow_html=True)

        coordenadas_aeroportos = {
            "SBGR": (-23.4356, -46.4731),  # Guarulhos
            "SBGL": (-22.8089, -43.2436),  # Galeão - RJ
            "SBEG": (-3.0386, -60.0497),   # Manaus
            "SKBO": (4.7016, -74.1469),    # Bogotá
            "SYCJ": (6.4986, -58.2541),    # Georgetown
            "KDFW": (32.8998, -97.0403),   # Dallas
        }

        # Filtrar voos de Guarulhos com destinos conhecidos no mapa
        df_guarulhos = df[
            (df["aeroporto_origem_sigla"] == "SBGR") &
            (df["aeroporto_destino_sigla"].isin(coordenadas_aeroportos.keys()))
        ].copy()

        # Criar o mapa
        mapa = folium.Map(location=[-23.4356, -46.4731], zoom_start=4)

        # Lista para tabela de visualização
        dados_voos = []

        for _, row in df_guarulhos.iterrows():
            destino_sigla = row["aeroporto_destino_sigla"]
            destino_nome = row["aeroporto_destino_nome"]
            origem_coords = coordenadas_aeroportos["SBGR"]
            destino_coords = coordenadas_aeroportos[destino_sigla]

            # Adiciona marcador e linha no mapa
            folium.Marker(
                location=destino_coords,
                popup=f"{destino_nome} ({destino_sigla})",
                icon=folium.Icon(color='red', icon='plane-arrival', prefix='fa')
            ).add_to(mapa)

            folium.PolyLine([origem_coords, destino_coords], color='blue', weight=2).add_to(mapa)

            # Adiciona descrição à lista de voos mostrados
            dados_voos.append({
                "Origem": "Guarulhos (SBGR)",
                "Destino": f"{destino_nome} ({destino_sigla})",
                "Descrição": f"Voo de Guarulhos (SBGR) para {destino_nome} ({destino_sigla})"
            })

        # Adicionar marcador de origem
        folium.Marker(
            location=coordenadas_aeroportos["SBGR"],
            popup="Guarulhos (SBGR)",
            icon=folium.Icon(color='green', icon='plane-departure', prefix='fa')
        ).add_to(mapa)


        st.markdown('''<hr><h2>Voos com origem em Guarulhos (SBGR)''', unsafe_allow_html=True)
        
        st_folium(mapa, use_container_width=True, height=500)

        st.markdown("""
        <div style="border: 2px solid #302681; border-radius: 12px; padding: 20px; background-color: #f9f9f9;">
        <h3 style="color:#302681; text-align: center;">ℹ️ Informações dos voos</h3>
        <ul style="font-size:16px; line-height:1.6;">
            <li><strong>Guarulhos (SBGR) → Galeão - RJ (SBGL)</strong><br>Voo doméstico, conectando São Paulo ao Rio de Janeiro.</li>
            <li><strong>Guarulhos (SBGR) → Manaus (SBEG)</strong><br>Rota nacional, do sudeste ao norte do Brasil.</li>
            <li><strong>Guarulhos (SBGR) → Bogotá - Colômbia (SKBO)</strong><br>Voo internacional para a capital colombiana.</li>
            <li><strong>Guarulhos (SBGR) → Georgetown - Guiana (SYCJ)</strong><br>Voo internacional para a capital da Guiana.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)


    # ============= MÉTRICAS =============
    if page == "Métricas":
        st.markdown('''<h1>🏆 Top 5 Empresas</h1>''', unsafe_allow_html=True)

        agg = (df.groupby("data")[["rpk", "ask", "atk", "rtk"]]
            .sum()
            .assign(load_factor=lambda x: 100 * x.rpk / x.ask.replace(0, np.nan),
                    eficiencia_carga=lambda x: 100 * x.rtk / x.atk.replace(0, np.nan))
            .fillna(0)
            .reset_index())

        # Cards customizados
        col9, col10, col11, col12 = st.columns(4)
        with col9:
            st.markdown(f'''
                <div class="container-m">
                    <div class="title-m">RPK</div>
                    <div class="text-m">{(agg.rpk.iloc[-1] / 1e9):.2f}</div>
                    <div class="info-m col9">ⓘ </div>
                </div>
            ''', unsafe_allow_html=True)
        with col10:
            st.markdown(f'''
                <div class="container-m">
                    <div class="title-m">ASK</div>
                    <div class="text-m">{(agg.ask.iloc[-1] / 1e9):.2f}</div>
                    <div class="info-m col10">ⓘ </div>
                </div>
            ''', unsafe_allow_html=True)
        with col11:
            st.markdown(f'''
                <div class="container-m">
                    <div class="title-m">Load Factor (%)</div>
                    <div class="text-m">{(agg.load_factor.iloc[-1]):.2f}</div>
                    <div class="info-m col11">ⓘ </div>
                </div>
            ''', unsafe_allow_html=True)
        with col12:
            st.markdown(f'''
                <div class="container-m">
                    <div class="title-m">Eficiência Carga (%)</div>
                    <div class="text-m">{(agg.eficiencia_carga.iloc[-1]):.2f}</div>
                    <div class="info-m col12">ⓘ </div>
                </div>
            ''', unsafe_allow_html=True)
            
    metric_functions = {
        "rpk": select_view_rpk,
        "ask": select_view_ask,
        "rtk": select_view_rtk,
        "atk": select_view_atk,
        "load_factor": select_view_loadfactor,
        "eficiencia_carga": select_view_eficiencia_carga,
    }

    # Lista de opções para o selectbox
    opcoes = list(metric_functions.keys())

    # Sidebar
    st.sidebar.markdown('''<h2 class="emoji-after">Personalize as Métricas!</h2>''', unsafe_allow_html=True)
    metrica_rank = st.sidebar.selectbox("Escolha a métrica:", options=opcoes, index=0)

    # Executa a função correspondente
    top5 = metric_functions[metrica_rank]()

    # Histograma
    st.markdown('''<hr>''', unsafe_allow_html=True)
    st.markdown('''<h2>Histograma: Métricas por Empresa</h2>''', unsafe_allow_html=True)
    st.bar_chart(top5.set_index("empresa_sigla")[metrica_rank], use_container_width=True, x_label='Top 5 Empresas', y_label='Valor da Métrica')

    # Mostra a query (aparece no terminal pelo print das funções)
    # Opcional: mostrar no app também
    def get_query_text(metric):
        query_map = {
            "rpk": """
                SELECT empresa_sigla, rpk
                FROM vw_metricas_agregadas_ultimo_mes
                ORDER BY rpk DESC
                LIMIT 5;
            """,
            "ask": """
                SELECT empresa_sigla, ask
                FROM vw_metricas_agregadas_ultimo_mes
                ORDER BY ask DESC
                LIMIT 5;
            """,
            "rtk": """
                SELECT empresa_sigla, rtk
                FROM vw_metricas_agregadas_ultimo_mes
                ORDER BY rtk DESC
                LIMIT 5;
            """,
            "atk": """
                SELECT empresa_sigla, atk
                FROM vw_metricas_agregadas_ultimo_mes
                ORDER BY atk DESC
                LIMIT 5;
            """,
            "load_factor": """
                SELECT empresa_sigla, load_factor
                FROM vw_metricas_agregadas_ultimo_mes
                ORDER BY load_factor DESC
                LIMIT 5;
            """,
            "eficiencia_carga": """
                SELECT empresa_sigla, eficiencia_carga
                FROM vw_metricas_agregadas_ultimo_mes
                ORDER BY eficiencia_carga DESC
                LIMIT 5;
            """
        }
        return query_map.get(metric, "-- SQL não encontrada --").strip()

    # SQL View
    st.markdown('''<hr>''', unsafe_allow_html=True)
    st.markdown('''<h2>SQL View: Métricas por Empresa</h2>''', unsafe_allow_html=True)
    st.code(get_query_text(metrica_rank), language="sql")
    st.dataframe(top5, use_container_width=True)

#----------------------------------------------------------------------------------------------------------
    # ============= ANÁLISES GRÁFICAS =============
    if page == "Análises Gráficas":
        # Adiciona empresas únicas
        empresas_unique = sorted(df['empresa_sigla'].unique()) # acho que essa linha é desnecessária, ACHO
        empresas_especificas = sorted(['AZU', 'LAN', 'GLO', 'AAL', 'UAE'])
        empresas_default = empresas_especificas

        st.sidebar.markdown('''
            <h2 class="emoji-after">Personalize os Gráficos!</h2>
        ''', unsafe_allow_html=True)

        if 'empresas_selecionadas' not in st.session_state:
            st.session_state['empresas_selecionadas'] = empresas_default

        if st.sidebar.button("Resetar Filtro"): # adiciona botão de resetar filtros
            st.session_state['empresas_selecionadas'] = empresas_default

        # Adiciona multiselect com as empresas únicas
        empresas_selecionadas = st.sidebar.multiselect(
            "Selecione as empresas (por sigla):",
            options=empresas_unique,
            default=st.session_state['empresas_selecionadas'],
            key='empresas_selecionadas'
        )

        df_filtrado = df[df['empresa_sigla'].isin(st.session_state['empresas_selecionadas'])]

        # ============= 1º Gráfico =============
        st.markdown('''<h3 class="g-title">Fator de Ocupação (RPK / ASK)</h3>''', unsafe_allow_html=True)
        df_f_ocupacao = df_filtrado.groupby(['data', 'empresa_sigla'])['fator_ocupacao'].mean().reset_index()
        df_pivot_f_ocupacao = df_f_ocupacao.pivot(index='data', columns='empresa_sigla', values='fator_ocupacao').fillna(0)
        st.line_chart(df_pivot_f_ocupacao, x_label='Período', y_label='Coeficiente F.O.')

        st.markdown('''<p><b>Análise</b>: Quanto mais próximo de 1.0 (100%), melhor o uso dos assentos disponíveis.</p>''', unsafe_allow_html=True)
        st.markdown('''<hr>''', unsafe_allow_html=True)

        # ============= 2º Gráfico =============
        st.markdown('''<h3 class="g-title">Fator de Carga (RTK / ATK)</h3>''', unsafe_allow_html=True)

        df_f_carga = df_filtrado.groupby(['data', 'empresa_sigla'])['fator_carga'].mean().reset_index()
        df_pivot_f_carga = df_f_carga.pivot(index='data', columns='empresa_sigla', values='fator_carga').fillna(0)
        st.line_chart(df_pivot_f_carga, x_label='Período', y_label='Coeficiente F.C.')

        st.markdown('''<p><b>Análise</b>: Valores mais baixos representam muita capacidade ociosa.</p>''', unsafe_allow_html=True)
        st.markdown('''<hr>''', unsafe_allow_html=True)

        # ============= 3º Gráfico =============
        st.markdown('''<h3 class="g-title">Média de Passageiros por Voo</h3>''', unsafe_allow_html=True)

        df_passageiros_decolagem = df_filtrado.groupby(['data', 'empresa_sigla'])['passageiros_por_decolagem'].mean().reset_index()
        df_pivot_passageiros_decolagem = df_passageiros_decolagem.pivot(index='data', columns='empresa_sigla', values='passageiros_por_decolagem').fillna(0)
        st.line_chart(df_pivot_passageiros_decolagem, x_label='Período', y_label='Média de Passageiros')

        st.markdown('''<hr>''', unsafe_allow_html=True)

        # ============= 4º Gráfico =============
        st.markdown('''<h3 class="g-title">Carga Total Média por Voo (em quilogramas)</h3>''', unsafe_allow_html=True)

        df_carga_voo = df_filtrado.groupby(['data', 'empresa_sigla'])['carga_por_voo'].mean().reset_index()
        df_pivot_carga_voo = df_carga_voo.pivot(index='data', columns='empresa_sigla', values='carga_por_voo').fillna(0)
        st.line_chart(df_pivot_carga_voo, x_label='Período', y_label='Média de Carga Total (Kg)')
    
        st.markdown('''<hr>''', unsafe_allow_html=True)

        # ============= 5º Gráfico =============
        st.markdown('''<h3 class="g-title">Distância Média por Voo (em quilômetros)</h3>''', unsafe_allow_html=True)
        df_distancia_voo = df_filtrado.groupby(['data', 'empresa_sigla'])['distancia_por_voo'].mean().reset_index()
        df_pivot_distancia_voo = df_distancia_voo.pivot(index='data', columns='empresa_sigla', values='distancia_por_voo').fillna(0)
        st.line_chart(df_pivot_distancia_voo, x_label='Período', y_label='Distância Média Percorrida (Km)')

        st.markdown('''<hr>''', unsafe_allow_html=True)

        # ============= 6º Gráfico =============
        st.markdown('''<h3 class="g-title">Combustível Médio por Passageiro (em litros)</h3>''', unsafe_allow_html=True)

        df_combustivel_passageiro = df_filtrado.groupby(['data', 'empresa_sigla'])['combustivel_por_passageiro'].mean().reset_index()
        df_pivot_combustivel_passageiro = df_combustivel_passageiro.pivot(index='data', columns='empresa_sigla', values='combustivel_por_passageiro').fillna(0)
        st.line_chart(df_pivot_combustivel_passageiro, x_label='Período', y_label='Combustível Médio (L)')

        st.markdown('''<hr>''', unsafe_allow_html=True)

        # ============= 7º Gráfico =============
        st.markdown('''<h3 class="g-title">Quantidade Média de Assentos por Voo</h3>''', unsafe_allow_html=True)

        df_assentos_voo = df_filtrado.groupby(['data', 'empresa_sigla'])['assentos_por_voo'].mean().reset_index()
        df_pivot_assentos_voo = df_assentos_voo.pivot(index='data', columns='empresa_sigla', values='assentos_por_voo').fillna(0)
        st.line_chart(df_pivot_assentos_voo, x_label='Período', y_label='Qtd. Média de Assentos')

        st.markdown('''<hr>''', unsafe_allow_html=True)

        # ============= 8º Gráfico =============
        st.markdown('''<h3 class="g-title">Eficiência da Carga Útil (Payload Efficiency)</h3>''', unsafe_allow_html=True)

        df_payload_efficiency = df_filtrado.groupby(['data', 'empresa_sigla'])['payload_efficiency'].mean().reset_index()
        df_payload_efficiency = df_payload_efficiency.pivot(index='data', columns='empresa_sigla', values='payload_efficiency').fillna(0)
        st.line_chart(df_payload_efficiency, x_label='Período', y_label='Payload Efficiency')

        st.markdown('''<p><b>Análise</b>: Quanto maior o coeficiente, maior a capacidade total utilizada.</p>''', unsafe_allow_html=True)

    # ============= INSIGHTS =============
    if page == "Insights":
        st.markdown('''

        <h1>🔍 Análise Estratégica das Operações Aéreas no Brasil</h1>
        <p align="center"><strong>(Foco no Aeroporto de Guarulhos)</strong></p>

        <h2>Visão Geral das Operações</h2>
        <ul>
            <li>Voos totais registrados: <strong>13.329</strong></li>
            <li>Aeroporto com maior movimentação: <strong>Guarulhos (2.678 voos)</strong></li>
        </ul>

        <h3> Distribuição Nacional:</h3>
        <ul>
            <li>Voos com origem no Brasil: <strong>1.884</strong></li>
            <li>Voos com destino ao Brasil: <strong>1.887</strong></li>
        </ul>
        <p align="center"><em>Indicador de equilíbrio na conectividade internacional e doméstica.</em></p>

        <h2>Carga & Combustível</h2>
        <h3>Dados gerais:</h3>
        <ul>
            <li>Combustível total consumido: <strong>1,71 bilhões de litros</strong></li>
            <li>Carga total transportada: <strong>458,8 milhões de Kg</strong></li>
        </ul>

        <h4>Dados de Guarulhos:</h4>
        <ul>
            <li>Combustível total consumido: <strong>730,6 milhões de litros (42,6% do total nacional)</strong></li>
            <li>Movimentação total de passageiros: <strong>14,6 milhões</strong></li>
        </ul>
        <p align="center">Guarulhos concentra uma parte significativa dos recursos logísticos e operacionais, sendo um ponto de atenção para políticas de eficiência e sustentabilidade.</p>

        <h2>Análise de Mercado – Potencial Estratégico de Guarulhos</h2>
        <p align="center">Com quase 43% de todo o combustível consumido no setor aéreo nacional, o aeroporto de Guarulhos assume o papel de ponto central da aviação brasileira, tanto em mobilidade de passageiros quanto em transporte de cargas. Este volume expressivo de movimentação não apenas posiciona Guarulhos como hub logístico dominante, mas também o torna altamente sensível a oscilações nos custos de combustível e políticas regulatórias.</p>

        <h3>Demanda Concentrada</h3>
        <p align="center">A movimentação de 14,6 milhões de passageiros revela a importância de Guarulhos como porta de entrada e saída do país, com impacto direto na receita das companhias aéreas, no turismo, no comércio internacional e no fluxo corporativo. Com a crescente urbanização e centralização econômica na região Sudeste, espera-se que essa demanda continue elevada nos próximos anos, exigindo respostas estruturais do setor.</p>

        <h3>Carga como Oportunidade de Expansão</h3>
        <p align="center">Embora o relatório não detalhe a fatia de carga operada especificamente por Guarulhos, a infraestrutura e localização do aeroporto o tornam altamente competitivo no mercado de frete aéreo. Isso representa uma oportunidade clara de:</p>
        <ul>
            <li>Expandir terminais de carga com tecnologia de automação;</li>
            <li>Atrair operadores logísticos globais;</li>
            <li>Promover rotas exclusivas de carga (<i>freighters</i>) com maior valor agregado.</li>
        </ul>

        <h3>⚠️ Pressões e Riscos de Mercado:</h3>
        <ul>
            <li><strong>Custo do combustível:</strong> O querosene de aviação representa o principal custo variável do setor. Com alta concentração de consumo em Guarulhos, oscilações no preço internacional do petróleo afetam diretamente a lucratividade das operações que passam pelo aeroporto.</li>
            <li><strong>Conflitos geopolíticos e mudanças climáticas</strong> podem comprometer a regularidade do abastecimento e aumentar o custo de operação.</li>
            <li><strong>Regulações ambientais futuras</strong> (ex: taxas de carbono, metas de descarbonização) terão impacto direto sobre aeroportos com maior pegada de carbono — caso de Guarulhos.</li>
        </ul>

        <h3>Perspectivas e Recomendação de Mercado</h3>
        <p>Guarulhos já opera como hub dominante, mas sua posição também representa uma exposição crítica a riscos operacionais e ambientais. Para manter competitividade e atender às exigências futuras do mercado, é essencial que os players do setor (companhias aéreas, operadoras logísticas e governo) adotem estratégias como:</p>
        <ul>
            <li>Investimentos em eficiência energética e SAF (combustível sustentável de aviação) para reduzir a dependência do querosene fóssil.</li>
            <li>Ampliação da capacidade de carga aérea, com foco em e-commerce internacional, produtos farmacêuticos e eletrônicos — segmentos de alta rentabilidade.</li>
            <li>Parcerias estratégicas com plataformas de logística digital para otimização do uso do porão das aeronaves.</li>
            <li>Política de incentivos fiscais e tarifários para operações sustentáveis que utilizem Guarulhos como base.</li>
        </ul>

        <h2>Desempenho das Empresas Aéreas</h2>
        <ul>
            <li><strong>RPK</strong> (Receita por Passageiro-Km): 20,98</li>
            <li><strong>ASK</strong> (Assentos disponíveis-Km): 25,06</li>
            <li><strong>Fator de Ocupação (Load Factor):</strong> 83,74%</li>
            <li><strong>Eficiência de Carga:</strong> 63,88%</li>
        </ul>

        <h3>Interpretação</h4>
        <ul>
            <li>Alta ocupação média dos voos (83,74%) indica bom aproveitamento comercial.</li>
            <li>Eficiência de carga (63,88%) revela oportunidades de otimização logística.</li>
            <li>RPK vs. ASK aponta uso eficaz da capacidade disponível.</li>
        </ul>
        ''', unsafe_allow_html=True)

    # ============= INFO =============
    if page == "Informações":
        st.markdown('''
        <h3 style="text-align: center">INFO ℹ️</h3>

        <p style="text-align: justify">Essa aplicação foi desenvolvida para facilitar a análise de um grande conjunto de dados sobre voos, reunindo informações de quase 100 companhias aéreas entre <b>janeiro e abril de 2025</b>.</p>
                    
        <p style="text-align: justify">As funcionalidades incluem filtros dinâmicos, além de visualizações gráficas interativas para apoiar a interpretação dos dados.</p>
        
        <p style="text-align: justify">O objetivo é atender profissionais do setor aéreo, analistas de dados e qualquer pessoa interessada em compreender o panorama da aviação comercial no período analisado.</p>
        
        <p style="text-align: justify">⚠️ Em caso de dúvidas ou sugestões, entre em contato pelo e-mail <a href="mailto:exemplo@email.com">exemplo@email.com</a>.</p>

        <hr>''', unsafe_allow_html=True)

        with st.expander('Clique aqui para visualizar ruídos.'):
            colunas_numericas = ['passageiros_pagos', 'passageiros_gratis', 'carga_paga_kg', 'carga_gratis_kg', 'correios_kg', 'ask', 'rpk', 'atk', 'rtk', 'combustivel_litros', 'distancia_voada_km', 'decolagens', 'carga_paga_km', 'carga_gratis_km', 'correio_km', 'assentos', 'payload', 'HORAS_VOADAS', 'bagagem_kg']

            st.sidebar.markdown('''
                <h2 class="emoji-after">Personalize as Análises!</h2>
            ''', unsafe_allow_html=True)
            empresas = sorted(df['empresa_sigla'].unique())
            default = sorted(['AZU', 'LAN', 'GLO', 'AAL', 'UAE'])

            if 'empresas_selecionadas' not in st.session_state:
                st.session_state.empresas_selecionadas = list(default)

            if st.sidebar.button('Resetar Filtro'):
                st.session_state.empresas_selecionadas = list(default)

            empresas_selecionadas = st.sidebar.multiselect(
                "Selecione as empresas", 
                empresas, 
                default=st.session_state.empresas_selecionadas,
                key='empresas_selecionadas'
            )

            x_col = st.sidebar.selectbox("Coluna do eixo X (horizontal):", colunas_numericas, index=0, help='O gráfico de dispersão mostra a relação entre dois atributos selecionados. Pontos alinhados indicam correlação entre as variáveis, enquanto pontos espalhados mostram pouca relação. As cores representam diferentes empresas e pontos isolados podem indicar erros ou situações fora do padrão.')
            y_col = st.sidebar.selectbox("Coluna do eixo Y (vertical):", colunas_numericas, index=1)

            df_filtrado = df[df['empresa_sigla'].isin(empresas_selecionadas)]

            # Boxplot com Plotly
            fig = px.scatter(
                df_filtrado,
                x=x_col,
                y=y_col,
                color="empresa_sigla",
                hover_data=["empresa_nome", "ano", "mes", "aeroporto_origem_sigla", "aeroporto_destino_sigla"],  # infos extras ao passar mouse
                title=f"Dispersão de {y_col} vs. {x_col} por Empresa",
                labels={x_col: x_col, y_col: y_col, "empresa_sigla": "Empresa"},
            )
            st.plotly_chart(fig, use_container_width=True)

            # Coeficiente de Variação (opcional: para cada eixo)
            cv_x = df_filtrado.groupby("empresa_sigla")[x_col].std() / df_filtrado.groupby("empresa_sigla")[x_col].mean()
            cv_y = df_filtrado.groupby("empresa_sigla")[y_col].std() / df_filtrado.groupby("empresa_sigla")[y_col].mean()

            st.markdown('''<h2>Coeficiente de Variação (por empresa)</h2>''', unsafe_allow_html=True)

            st.dataframe(pd.DataFrame({f"C.V. ({x_col})": cv_x.round(3), f"C.V. ({y_col})": cv_y.round(3)}))

            st.markdown('''
                <div class="info info-page">ℹ️ O <i>Coeficiente de Variação</i> (C.V.) mede o quanto os valores de uma variável são dispersos em relação à sua média. Quanto maior a porcentagem, mais instável ou inconsistente é aquela variável</div>
            ''', unsafe_allow_html=True)

            # Quantidade de outliers usando IQR para ambos eixos
            def conta_outliers(s):
                q1 = s.quantile(0.25)
                q3 = s.quantile(0.75)
                iqr = q3 - q1
                return ((s < (q1 - 1.5 * iqr)) | (s > (q3 + 1.5 * iqr))).sum()
            outliers_x = df_filtrado.groupby("empresa_sigla")[x_col].apply(conta_outliers)
            outliers_y = df_filtrado.groupby("empresa_sigla")[y_col].apply(conta_outliers)

            st.markdown('''<h2>Quantidade de Outliers (por empresa)</h2>''', unsafe_allow_html=True)

            st.dataframe(pd.DataFrame({f"Qtd de Outliers ({x_col})": outliers_x, f"Qtd de Outliers ({y_col})": outliers_y}))

            st.markdown('''
                <div class="info info-page">ℹ️ <i>Outlier</i> é um valor que se destaca dos demais em um conjunto de dados, sendo muito diferente do padrão ou da maioria dos outros valores.</div>
            ''', unsafe_allow_html=True)

        st.markdown('''
            <hr>
            
            <p style="text-align: justify">Esta aplicação foi desenvolvida por <a href="https://www.linkedin.com/in/dev-matheusvn/" target="_blank">Matheus V. Nellessen</a>, <a href="https://www.linkedin.com/in/andr%C3%A9-ciccozzi-71360b1b2/" target="_blank">André Ciccozzi</a>, <a href="" target="_blank">Heitor</a> e <a href="" target="_blank">Leonardo</a> como projeto final da capacitação em <i>Analytics</i>.</p>
                    
            <p style="text-align: justify">Agradecimentos especiais a instrutora <b>Daniella Torelli</b>, profissional repleta de habilidades para ensinar, responsável pela nossa capacitação técnica nesta nova área.</p>                
        ''', unsafe_allow_html=True)