import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# ============== CONFIG E DADOS ==============
st.set_page_config(page_title="Dashboard Aviação", page_icon="✈️", layout="wide")

st.markdown("""
    <style>
        .container {
            margin: 10px; padding: 20px;
            text-align: center;
            background-color: white;
            box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            border-radius: 15px;
            min-height: 140px;
            filter: opacity(0.8);
        }
            
        .container:hover {
            filter: opacity(1);
            box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); 
        }
            
        .title {
            font-size: 1.25em;
            font-weight: 600;   
        }
            
        .text {
            font-size: 1.25em;
        }
            
        .subtext {
            font-size: 1.25em;
        }
        
        .info {
            font-size: 0.8em;
            text-align: left;    
        }

        h1 {
            font-size: 3em;
            text-align: center; 
        }
            
    </style>
""", unsafe_allow_html=True)

df = pd.read_csv("C:\\Users\\mathe\\Documentos\\Development\\projeto_final_anac\\database\\anac\\anac_2025_sem_tratar_outliers.csv", sep=';', encoding='latin1')

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

# ============= SIDEBAR =============
st.sidebar.image("C:\\Users\\mathe\\Documentos\\Development\\projeto_final_anac\\frontend\\arq\\plane.png", width=150)
st.sidebar.title('Navegue por aqui!')
page = st.sidebar.radio("Ir para:", ["Visão Geral", "Métricas & Gráficos"])

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

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
            <div class="container">
                <div class="title">Aeroporto mais frequentado</div>
                <div class="text">{aeroporto_top1_nome}</div>
                <div class="subtext">{aeroporto_top1_qtd} voos</div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <div class="container">
                <div class="title">Voos Internacionais Brasileiros</div>
                <div class="text">{qtd_entrando} entradas</div>
                <div class="subtext">{qtd_saindo} saídas</div>
                <div class="info">Voos internacionais que chegam e partem do Brasil</div>
            </div>
        ''', unsafe_allow_html=True)

# ============= MÉTRICAS & GRÁFICOS =============
if page == "Métricas & Gráficos":
    st.markdown('''📈 Métricas e Gráficos de Desempenho''', unsafe_allow_html=True)

    # Adiciona empresas únicas
    empresas_unique = sorted(df['empresa_sigla'].unique())
    empresas_default = empresas_unique[:5]

    if 'empresas_selecionadas' not in st.session_state:
        st.session_state['empresas_selecionadas'] = empresas_default

    if st.button("Resetar Filtro"): # adiciona botão de resetar filtros
        st.session_state['empresas_selecionadas'] = empresas_default

    # Adiciona multiselect com as empresas únicas
    empresas_selecionadas = st.multiselect(
        "Selecione as empresas (por sigla):",
        options=empresas_unique,
        default=st.session_state['empresas_selecionadas'],
        key='empresas_selecionadas'
    )

    df_filtrado = df[df['empresa_sigla'].isin(st.session_state['empresas_selecionadas'])]

    # ============= 1º Gráfico =============
    st.subheader("Fator de Ocupação (RPK / ASK) por Empresa")
    df_f_ocupacao = df_filtrado.groupby(['data', 'empresa_sigla'])['fator_ocupacao'].mean().reset_index()
    df_pivot_f_ocupacao = df_f_ocupacao.pivot(index='data', columns='empresa_sigla', values='fator_ocupacao').fillna(0)
    st.line_chart(df_pivot_f_ocupacao)
    st.caption("Quanto mais próximo de 1.0 (100%), melhor o uso dos assentos disponíveis.")

    # ============= 2º Gráfico =============
    st.subheader("Fator de Carga (RTK / ATK) por Empresa")
    df_f_carga = df_filtrado.groupby(['data', 'empresa_sigla'])['fator_carga'].mean().reset_index()
    df_pivot_f_carga = df_f_carga.pivot(index='data', columns='empresa_sigla', values='fator_carga').fillna(0)
    st.line_chart(df_pivot_f_carga)
    st.caption("Foca em carga útil transportada; valores baixos = muita capacidade ociosa.")

    # ============= 3º Gráfico =============
    st.subheader("Média de Passageiros por Decolagem")
    df_passageiros_decolagem = df_filtrado.groupby(['data', 'empresa_sigla'])['passageiros_por_decolagem'].mean().reset_index()
    df_pivot_passageiros_decolagem = df_passageiros_decolagem.pivot(index='data', columns='empresa_sigla', values='passageiros_por_decolagem').fillna(0)
    st.line_chart(df_pivot_passageiros_decolagem)
    st.caption("Mostra eficiência de ocupação por voo.")

    # ============= 4º Gráfico =============
    st.subheader("Média de Carga Total por Voo (em Kg)")
    df_carga_voo = df_filtrado.groupby(['data', 'empresa_sigla'])['carga_por_voo'].mean().reset_index()
    df_pivot_carga_voo = df_carga_voo.pivot(index='data', columns='empresa_sigla', values='carga_por_voo').fillna(0)
    st.line_chart(df_pivot_carga_voo)
    st.caption("Mede carga útil média por decolagem.")

    # ============= 5º Gráfico =============
    st.subheader("Distância Média por Voo (em Km)")
    df_distancia_voo = df_filtrado.groupby(['data', 'empresa_sigla'])['distancia_por_voo'].mean().reset_index()
    df_pivot_distancia_voo = df_distancia_voo.pivot(index='data', columns='empresa_sigla', values='distancia_por_voo').fillna(0)
    st.line_chart(df_pivot_distancia_voo)
    st.caption("Acompanha evolução das rotas médias.")

    # ============= 6º Gráfico =============
    st.subheader("Combustível por Passageiro (em litros)")
    df_combustivel_passageiro = df_filtrado.groupby(['data', 'empresa_sigla'])['combustivel_por_passageiro'].mean().reset_index()
    df_pivot_combustivel_passageiro = df_combustivel_passageiro.pivot(index='data', columns='empresa_sigla', values='combustivel_por_passageiro').fillna(0)
    st.line_chart(df_pivot_combustivel_passageiro)
    st.caption("Mede eficiência de combustível individual.")

    # ============= 7º Gráfico =============
    st.subheader("Assentos por Voo")
    df_assentos_voo = df_filtrado.groupby(['data', 'empresa_sigla'])['assentos_por_voo'].mean().reset_index()
    df_pivot_assentos_voo = df_assentos_voo.pivot(index='data', columns='empresa_sigla', values='assentos_por_voo').fillna(0)
    st.line_chart(df_pivot_assentos_voo)
    st.caption("Mede capacidade ofertada por voo.")

    # ============= 8º Gráfico =============
    st.subheader("Eficiência da Carga Útil (Payload Efficiency)")
    df_payload_efficiency = df_filtrado.groupby(['data', 'empresa_sigla'])['payload_efficiency'].mean().reset_index()
    df_payload_efficiency = df_payload_efficiency.pivot(index='data', columns='empresa_sigla', values='payload_efficiency').fillna(0)
    st.line_chart(df_payload_efficiency)
    st.caption("Integra passageiro+carga: quanto da capacidade total está sendo utilizada.")
