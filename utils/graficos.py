import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_csv("database/anac_2025_tratado.csv", sep=';', encoding='latin1')

df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
df['mes'] = pd.to_numeric(df['mes'], errors='coerce')

df['data'] = pd.to_datetime(
    df['ano'].astype(str) + '-' + df['mes'].astype(str) + '-01',
    errors='coerce'
)
df = df.dropna(subset=['data']).reset_index(drop=True)

# ==================================================
#                   BIG NUMBERS                        
# ==================================================

empresas_brasileiras = df[df['empresa_nacionalidade'] == 'BRASILEIRA']['empresa_sigla'].unique()
empresas_estrangeiras = df[df['empresa_nacionalidade'] == 'ESTRANGEIRA']['empresa_sigla'].unique()

qtd_brasileiras = len(empresas_brasileiras)
qtd_estrangeiras = len(empresas_estrangeiras)

print(qtd_brasileiras)
print(qtd_estrangeiras)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Empresas Brasileiras:', value=f'{qtd_brasileiras} companhias')

with col2:
    st.metric('Empresas Estrangeiras:', value=f'{qtd_estrangeiras} companhias')

# # ==================================================
# #                     1º GRÁFICO                        
# # ==================================================
# st.subheader("Evolução de passageiros pagantes por empresa")

# df_data_e_empresa_sigla_by_passageiros_pagos = df.groupby(['data', 'empresa_sigla'])['passageiros_pagos'].sum().reset_index()

# empresas_unique = sorted(df_data_e_empresa_sigla_by_passageiros_pagos['empresa_sigla'].unique())

# empresas_default1 = empresas_unique[:5]

# if 'empresa_selecionada1' not in st.session_state:
#     st.session_state['empresa_selecionada1'] = empresas_default1

# if st.button('Resetar Filtros do 1º Gráfico', key='reset_btn_1'):
#     st.session_state['empresa_selecionada1'] = empresas_default1

# empresa_selecionada1 = st.multiselect(
#     "Selecione as empresas:",
#     options=empresas_unique,
#     default=st.session_state['empresa_selecionada1'],
#     key='empresa_selecionada1'
# )

# df_filtrado1 = df_data_e_empresa_sigla_by_passageiros_pagos[df_data_e_empresa_sigla_by_passageiros_pagos['empresa_sigla'].isin(empresa_selecionada1)]

# df_filtrado_pivot1 = df_filtrado1.pivot(index='data', columns='empresa_sigla', values='passageiros_pagos')

# df_filtrado_pivot1 = df_filtrado_pivot1.fillna(0)

# st.line_chart(df_filtrado_pivot1, x_label='Data (mês dia)', y_label='Qtd de Passageiros Pagantes')

# # ==================================================
# #                     2º GRÁFICO                        
# # ==================================================

# st.subheader("Quantidade de passageiros pagantes por empresa")

# df_empresa_sigla_by_passageiros_pagos = df.groupby('empresa_sigla')['passageiros_pagos'].sum().reset_index()

# empresas_default2 = empresas_unique[:5]

# if 'empresa_selecionada2' not in st.session_state:
#     st.session_state['empresa_selecionada2'] = empresas_default2

# if st.button('Resetar Filtros do 2º Gráfico', key='reset_btn_2'):
#     st.session_state['empresa_selecionada2'] = empresas_default2

# st.multiselect(
#     "Selecione as empresas:",
#     options=empresas_unique,
#     key='empresa_selecionada2'
# )

# empresa_selecionada2 = st.session_state['empresa_selecionada2']

# df_filtrado2 = df_empresa_sigla_by_passageiros_pagos[df_empresa_sigla_by_passageiros_pagos['empresa_sigla'].isin(empresa_selecionada2)]

# df_filtrado_pivot2 = df_filtrado2.pivot(columns='empresa_sigla', values='passageiros_pagos')

# df_filtrado_pivot2 = df_filtrado_pivot2.fillna(0)

# st.bar_chart(df_filtrado_pivot2, x_label='Empresas', y_label='Qtd de Passageiros Pagantes')


# # ==================================================
# #                     3º GRÁFICO                        
# # ==================================================
