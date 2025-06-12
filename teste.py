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
            background-color: white;
            filter: opacity(0.9);
            min-height: 150px;
            border-radius: 15px;
            box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            margin: 10px; padding: 20px;
            text-align: center;
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
            color: #302681;
            font-size: 1em;
            font-weight: 600;
            text-align: left;    
        }

        h1 {
            font-size: 3em;
            text-align: center; 
        }
            
        h2 {
            text-align: center;         
        }

        .emoji-after:hover::after {
            content: "👆"
        }
            
        .g-title {
            text-align: center;
        }            
        
    </style>
""", unsafe_allow_html=True)

df = pd.read_csv("C:/Users/mathe/Documentos/Development/projeto_final/database/anac/anac_2025_sem_tratar_outliers.csv", sep=';', encoding='latin1')

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
st.sidebar.image("C:/Users/mathe/Documentos/Development/projeto_final/frontend/arq/plane.png", width=150)

# st.sidebar.markdown(
#     """
#     <div style="display: flex; justify-content: center;">
#         <img src="C:\\Users\\mathe\\Documentos\\Development\\projeto_final\\frontend\\arq\\plane.png">
#     </div>
#     """,
#     unsafe_allow_html=True
# )

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

# ============= MÉTRICAS =============
if page == "Métricas":
    st.markdown('''<h3>Olá mundo!</h3>''', unsafe_allow_html=True)

# ============= ANÁLISES GRÁFICAS =============
if page == "Análises Gráficas":
    # st.markdown('''<h1>📈 Métricas e Gráficos de Desempenho</h1>''', unsafe_allow_html=True)

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
    st.markdown('''<h3 class="g-title">Fator de Ocupação (RPK / ASK) por Empresa</h3>''', unsafe_allow_html=True)
    df_f_ocupacao = df_filtrado.groupby(['data', 'empresa_sigla'])['fator_ocupacao'].mean().reset_index()
    df_pivot_f_ocupacao = df_f_ocupacao.pivot(index='data', columns='empresa_sigla', values='fator_ocupacao').fillna(0)
    st.line_chart(df_pivot_f_ocupacao)

    st.markdown('''<p><b>Análise</b>: Quanto mais próximo de 1.0 (100%), melhor o uso dos assentos disponíveis.</p>''', unsafe_allow_html=True)
    st.markdown('''<hr>''', unsafe_allow_html=True)

    # ============= 2º Gráfico =============
    st.markdown('''<h3 class="g-title">Fator de Carga (RTK / ATK) por Empresa</h3>''', unsafe_allow_html=True)

    df_f_carga = df_filtrado.groupby(['data', 'empresa_sigla'])['fator_carga'].mean().reset_index()
    df_pivot_f_carga = df_f_carga.pivot(index='data', columns='empresa_sigla', values='fator_carga').fillna(0)
    st.line_chart(df_pivot_f_carga)

    st.markdown('''<p><b>Análise</b>: Valores mais baixos representam muita capacidade ociosa.</p>''', unsafe_allow_html=True)
    st.markdown('''<hr>''', unsafe_allow_html=True)

    # ============= 3º Gráfico =============
    st.markdown('''<h3 class="g-title">Média de Passageiros por Decolagem</h3>''', unsafe_allow_html=True)

    df_passageiros_decolagem = df_filtrado.groupby(['data', 'empresa_sigla'])['passageiros_por_decolagem'].mean().reset_index()
    df_pivot_passageiros_decolagem = df_passageiros_decolagem.pivot(index='data', columns='empresa_sigla', values='passageiros_por_decolagem').fillna(0)
    st.line_chart(df_pivot_passageiros_decolagem)

    st.markdown('''<hr>''', unsafe_allow_html=True)

    # ============= 4º Gráfico =============
    st.markdown('''<h3 class="g-title">Média de Carga Total por Voo (em Kg)</h3>''', unsafe_allow_html=True)

    df_carga_voo = df_filtrado.groupby(['data', 'empresa_sigla'])['carga_por_voo'].mean().reset_index()
    df_pivot_carga_voo = df_carga_voo.pivot(index='data', columns='empresa_sigla', values='carga_por_voo').fillna(0)
    st.line_chart(df_pivot_carga_voo)
  
    st.markdown('''<hr>''', unsafe_allow_html=True)

    # ============= 5º Gráfico =============
    st.markdown('''<h3 class="g-title">Distância Média por Voo (em Km)</h3>''', unsafe_allow_html=True)
    df_distancia_voo = df_filtrado.groupby(['data', 'empresa_sigla'])['distancia_por_voo'].mean().reset_index()
    df_pivot_distancia_voo = df_distancia_voo.pivot(index='data', columns='empresa_sigla', values='distancia_por_voo').fillna(0)
    st.line_chart(df_pivot_distancia_voo)

    st.markdown('''<hr>''', unsafe_allow_html=True)

    # ============= 6º Gráfico =============
    st.markdown('''<h3 class="g-title">Combustível por Passageiro (em litros)</h3>''', unsafe_allow_html=True)

    df_combustivel_passageiro = df_filtrado.groupby(['data', 'empresa_sigla'])['combustivel_por_passageiro'].mean().reset_index()
    df_pivot_combustivel_passageiro = df_combustivel_passageiro.pivot(index='data', columns='empresa_sigla', values='combustivel_por_passageiro').fillna(0)
    st.line_chart(df_pivot_combustivel_passageiro)

    st.markdown('''<hr>''', unsafe_allow_html=True)

    # ============= 7º Gráfico =============
    st.markdown('''<h3 class="g-title">Assentos por Voo</h3>''', unsafe_allow_html=True)

    df_assentos_voo = df_filtrado.groupby(['data', 'empresa_sigla'])['assentos_por_voo'].mean().reset_index()
    df_pivot_assentos_voo = df_assentos_voo.pivot(index='data', columns='empresa_sigla', values='assentos_por_voo').fillna(0)
    st.line_chart(df_pivot_assentos_voo)

    st.markdown('''<hr>''', unsafe_allow_html=True)

    # ============= 8º Gráfico =============
    st.markdown('''<h3 class="g-title">Eficiência da Carga Útil (Payload Efficiency)</h3>''', unsafe_allow_html=True)

    df_payload_efficiency = df_filtrado.groupby(['data', 'empresa_sigla'])['payload_efficiency'].mean().reset_index()
    df_payload_efficiency = df_payload_efficiency.pivot(index='data', columns='empresa_sigla', values='payload_efficiency').fillna(0)
    st.line_chart(df_payload_efficiency)

    st.markdown('''<p><b>Análise</b>: Quanto maior o coeficiente, maior a capacidade total utilizada.</p>''', unsafe_allow_html=True)

# ============= INSIGHTS =============
if page == "Insights":
    st.markdown('''<h3>Olá mundo!</h3>''', unsafe_allow_html=True)

# ============= INFO =============
if page == "Informações":
    st.markdown('''
    <h3 style="text-align: center">INFO ℹ️</h3>

    <p style="text-align: justify">Essa aplicação foi desenvolvida para facilitar a análise de um grande conjunto de dados sobre voos, reunindo informações de quase 100 companhias aéreas entre <b>janeiro e abril de 2025</b>.</p>
                
    <p style="text-align: justify">As funcionalidades incluem filtros dinâmicos, além de visualizações gráficas interativas para apoiar a interpretação dos dados.</p>
    
    <p style="text-align: justify">O objetivo é atender profissionais do setor aéreo, analistas de dados e qualquer pessoa interessada em compreender o panorama da aviação comercial no período analisado.</p>
    
    <p style="text-align: justify">⚠️ Em caso de dúvidas ou sugestões, entre em contato pelo e-mail <a href="mailto:exemplo@email.com">exemplo@email.com</a>.</p>

    <hr>

    <p style="text-align: justify">Esta aplicação foi desenvolvida por <a href="https://www.linkedin.com/in/dev-matheusvn/" target="_blank">Matheus Ventura Nellessen</a>, <a href="" target="_blank">André</a>, <a href="" target="_blank">Heitor</a> e <a href="" target="_blank">Leonardo</a> como projeto final da capacitação em <i>Analytics</i>.</p>
                
    <p style="text-align: justify">Agradecimentos especiais a instrutora <a href="https://www.linkedin.com/in/daniella-torelli-3464b81a9/" target="_blank">Daniella Torelli</a>, profissional repleta de habilidades para ensinar, responsável pela nossa capacitação técnica nesta nova área.</p>                
    ''', unsafe_allow_html=True)
