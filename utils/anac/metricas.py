import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_csv("C:\\Users\\mathe\\Documentos\\Development\\projeto_final_anac\\database\\anac\\anac_2025_sem_tratar_outliers.csv", sep=';', encoding='latin1')

df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
df['mes'] = pd.to_numeric(df['mes'], errors='coerce')

df['data'] = pd.to_datetime(
    df['ano'].astype(str) + '-' + df['mes'].astype(str) + '-01',
    errors='coerce'
)
df = df.dropna(subset=['data']).reset_index(drop=True)

# ===================================================
#                     BIG NUMBERS                        
# ===================================================

empresas_brasileiras = df[df['empresa_nacionalidade'] == 'BRASILEIRA']['empresa_sigla'].unique()
empresas_estrangeiras = df[df['empresa_nacionalidade'] == 'ESTRANGEIRA']['empresa_sigla'].unique()

qtd_brasileiras = len(empresas_brasileiras)
qtd_estrangeiras = len(empresas_estrangeiras)

# ========== TOP 1 AEROPORTO ==========

todos_os_aeroportos = pd.concat([
    df['aeroporto_origem_nome'],
    df['aeroporto_destino_nome']
])

aeroportos_mais_frequentes = todos_os_aeroportos.value_counts()

aeroporto_top1 = aeroportos_mais_frequentes.head(1)
aeroporto_top1_nome = aeroporto_top1.index[0]
aeroporto_top1_qtd = aeroporto_top1.iloc[0]

# ========== VOOS NACIONAIS / ESTRANGEIROS ==========

voos_entrando = df[
    (df['aeroporto_destino_pais'] == 'BRASIL') &
    (df['aeroporto_origem_pais'] != 'BRASIL')
]

voos_saindo = df[
    (df['aeroporto_origem_pais'] == 'BRASIL') &
    (df['aeroporto_destino_pais'] != 'BRASIL')
]

qtd_entrando = len(voos_entrando)
qtd_saindo = len(voos_saindo)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Aeroporto mais Frequente:', value=aeroporto_top1_nome)
    st.caption(f'{aeroporto_top1_qtd} voos')

with col2:
    st.metric("Voos internacionais que entram no Brasil", value=qtd_entrando)

with col3:
    st.metric("Voos internacionais que saem do Brasil", value=qtd_saindo)

# ================================================
#                     GRÁFICOS                    
# ================================================

df['fator_ocupacao'] = df['rpk'] / df['ask']
df['fator_carga'] = df['rtk'] / df['atk']

st.sidebar.title('Filtro por Empresa')

empresas_unique = sorted(df['empresa_sigla'].unique())
empresas_default = empresas_unique[:5] 

if 'empresas_selecionadas' not in st.session_state:
    st.session_state['empresas_selecionadas'] = empresas_default


if st.sidebar.button("Resetar Filtro"):
    st.session_state['empresas_selecionadas'] = empresas_default

empresas_selecionadas = st.sidebar.multiselect(
    "Selecione as empresas (por sigla):",
    options=empresas_unique,
    default=st.session_state['empresas_selecionadas'],
    key='empresas_selecionadas'
)

df_filtrado = df[df['empresa_sigla'].isin(st.session_state['empresas_selecionadas'])]

# ========== Gráfico de fator de ocupação ==========
st.subheader("Fator de Ocupação (RPK / ASK) por Empresa")

df_f_ocupacao = df_filtrado.groupby(['data', 'empresa_sigla'])['fator_ocupacao'].mean().reset_index()

df_pivot_f_ocupacao = df_f_ocupacao.pivot(index='data', columns='empresa_sigla', values='fator_ocupacao')

df_pivot_f_ocupacao = df_pivot_f_ocupacao.fillna(0)

st.line_chart(df_pivot_f_ocupacao)
st.markdown('''
O Fator de Ocupação mede o quanto da capacidade de assentos oferecida foi efetivamente utilizada por passageiros pagantes.
        
- RPK (Revenue Passenger Kilometers): total de quilômetros percorridos por passageiros pagantes.
        
- ASK (Available Seat Kilometers): total de quilômetros oferecidos (assentos disponíveis x distância voada).

Fórmula:
            
            Fator de Ocupação = RPK / ASK

Como interpretar:            

- Um fator de ocupação próximo de 1.0 (ou 100%) indica que a companhia aérea está utilizando muito bem sua capacidade.

- Valores abaixo de 0.7 (70%) podem indicar ociosidade, ou seja, muitos assentos estão vazios.

- Valores altos demais (acima de 90%) podem indicar demanda reprimida, com risco de overbooking ou perda de receita por falta de oferta.
''', unsafe_allow_html=True)

# ========== Gráfico de fator de carga ==========
st.subheader("Fator de Carga (RTK / ATK) por Empresa")

df_f_carga = df_filtrado.groupby(['data', 'empresa_sigla'])['fator_carga'].mean().reset_index()

df_pivot_f_carga = df_f_carga.pivot(index='data', columns='empresa_sigla', values='fator_carga')

df_pivot_f_carga = df_pivot_f_carga.fillna(0)

st.line_chart(df_pivot_f_carga)
st.markdown('''
O fator de carga avalia o aproveitamento da capacidade de carga das aeronaves.

- RTK (Revenue Ton Kilometers): toneladas de carga efetivamente transportadas multiplicadas pela distância.

- ATK (Available Ton Kilometers): capacidade total (em toneladas) multiplicada pela distância.

Fórmula:
            
            Fator de Carga = RTK / ATK
 
Como interpretar:

- Valores próximos de 1.0 representam ótimo aproveitamento da capacidade de carga.

- Fatores baixos (ex: < 0.5) sugerem ineficiência logística, voos com espaço de carga ocioso.

- Esse fator é muito relevante para empresas que operam voos cargueiros ou mistas (passageiros + carga).
''', unsafe_allow_html=True)

# ========== TRATANDO CSV again ==========r

df['passageiros_por_decolagem'] = (df['passageiros_pagos'] / df['decolagens']).where(df['decolagens'] != 0)
df['carga_total_kg'] = df['carga_paga_kg'] + df['carga_gratis_kg'] + df['correios_kg']
df['carga_por_voo'] = (df['carga_total_kg'] / df['decolagens']).where(df['decolagens'] != 0)
df['combustivel_por_passageiro'] = (df['combustivel_litros'] / df['passageiros_pagos']).where(df['passageiros_pagos'] != 0)
df['distancia_por_voo'] = (df['distancia_voada_km'] / df['decolagens']).where(df['decolagens'] != 0)
df['assentos_por_voo'] = (df['assentos'] / df['decolagens']).where(df['decolagens'] != 0)
df['payload_efficiency'] = (df['payload'] / (df['ask'] + df['atk'])).where((df['ask'] + df['atk']) != 0)

# =================== FILTRO DE EMPRESA ===================

df_filtrado2 = df[
    (df['empresa_sigla'].isin(st.session_state['empresas_selecionadas'])) &
    (df['passageiros_por_decolagem'].notna()) &
    (df['carga_por_voo'].notna()) &
    (df['distancia_por_voo'].notna())
]

# ==================== GRÁFICO PASSAGEIROS POR DECOLAGEM ====================
st.subheader("Média de Passageiros por Decolagem")

df_passageiros_decolagem = df_filtrado2.groupby(['data', 'empresa_sigla'])['passageiros_por_decolagem'].mean().reset_index()

df_pivot_passageiros_decolagem = df_passageiros_decolagem.pivot(index='data', columns='empresa_sigla', values='passageiros_por_decolagem').fillna(0)

st.line_chart(df_pivot_passageiros_decolagem, x_label='Data (mês dia)', y_label='Média de Passageiros')

# ==================== GRÁFICO CARGA TOTAL POR VOO ====================
st.subheader("Média de Carga Total por Voo (em Kg)")

df_carga_voo = df_filtrado2.groupby(['data', 'empresa_sigla'])['carga_por_voo'].mean().reset_index()

df_pivot_carga_voo = df_carga_voo.pivot(index='data', columns='empresa_sigla', values='carga_por_voo').fillna(0)

st.line_chart(df_pivot_carga_voo, x_label='Data (mês dia)', y_label='Carga Total (Kg)')

# ==================== GRÁFICO DISTÂNCIA POR VOO ====================
st.subheader("Distância Média por Voo (em Km)")

df_distancia_voo = df_filtrado2.groupby(['data', 'empresa_sigla'])['distancia_por_voo'].mean().reset_index()

df_pivot_distancia_voo = df_distancia_voo.pivot(index='data', columns='empresa_sigla', values='distancia_por_voo').fillna(0)

st.line_chart(df_pivot_distancia_voo, x_label='Data (mês dia)', y_label='Distância Média por Voo (Km)')

# ========== GRÁFICO 4: Combustível por Passageiro ==========
st.subheader("Combustível por Passageiro (em litros)")

df_combustivel_passageiro = df_filtrado2.groupby(['data', 'empresa_sigla'])['combustivel_por_passageiro'].mean().reset_index()

df_pivot_combustivel_passageiro = df_combustivel_passageiro.pivot(index='data', columns='empresa_sigla', values='combustivel_por_passageiro').fillna(0)

st.line_chart(df_pivot_combustivel_passageiro, x_label='Data (mês dia)', y_label='Combustível Utilizados (L)')

# ========== GRÁFICO 5: Assentos por Voo ==========
st.subheader("Assentos por Voo")

df_assentos_voo = df_filtrado2.groupby(['data', 'empresa_sigla'])['assentos_por_voo'].mean().reset_index()

df_pivot_assentos_voo = df_assentos_voo.pivot(index='data', columns='empresa_sigla', values='assentos_por_voo').fillna(0)

st.line_chart(df_pivot_assentos_voo, x_label='Data (mês dia)', y_label='Qtd. de Assentos')

# ========== GRÁFICO 6: Payload Efficiency ==========

st.subheader("Eficiência da Carga Útil (Payload Efficiency)")

df_payload_efficiency = df_filtrado2.groupby(['data', 'empresa_sigla'])['payload_efficiency'].mean().reset_index()

df_payload_efficiency = df_payload_efficiency.pivot(index='data', columns='empresa_sigla', values='payload_efficiency').fillna(0)

st.line_chart(df_payload_efficiency, x_label='Data (mês dia)', y_label='Coeficiente de Payload')

st.markdown('''
A eficiência de Carga Útil mede o quanto da capacidade total da aeronave foi efetivamente utilizada em uma operação aérea. Ela combina tanto o transporte de passageiros quanto de carga, oferecendo uma visão integrada do uso da capacidade total disponível.

Fórmula: 

            Payload Efficiency = Payload / ASK + ATK
 
- Payload: carga total útil transportada (em toneladas), considerando tanto passageiros quanto carga e correio.

- ASK (Available Seat Kilometers): capacidade de passageiros oferecida.

- ATK (Available Ton Kilometers): capacidade de carga oferecida.

Como interpretar:

- Valores próximos de 1.0 (ou 100%) indicam que a empresa está aproveitando quase toda sua capacidade disponível para transportar carga e passageiros.

- Valores abaixo de 0.6 geralmente indicam ociosidade significativa, com aeronaves voando com capacidade disponível não utilizada.

- Valores muito altos e constantes podem indicar alta eficiência ou até sobrecarga, o que exige atenção operacional.
''', unsafe_allow_html=True)
