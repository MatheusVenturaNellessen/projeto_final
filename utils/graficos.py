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
#                     1º GRÁFICO                        
# ==================================================

df_grouped1 = df.groupby('data')['passageiros_pagos'].sum().reset_index()

st.subheader('Evoluão de Passageiros Pagantes por Data')


st.line_chart(df_grouped1.set_index('data')['passageiros_pagos'], x_label='Datas (MM-DD)', y_label='Qtd. de Passageiros Pagantes')

# ==================================================
#                     2º GRÁFICO                        
# ==================================================

df_grouped2 = df.groupby(['empresa_sigla'])[['passageiros_pagos']].sum().sort_values(by='passageiros_pagos', ascending=False)

st.subheader('Quantidade de Passageiros Pagantes por Companhia Aérea')
st.bar_chart(df_grouped2.head(), x_label='Companhias Aéreas (sigla)', y_label='Qtd. de Passageiros Pagantes')

# ==================================================
#                     3º GRÁFICO                        
# ==================================================

teste