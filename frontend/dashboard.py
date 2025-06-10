import matplotlib.pyplot as plt
import seaborn as sns
from utils.database import execute_query
import streamlit as st
import plotly.express as px

def nacionalidade():
    query = '''
    SELECT empresa_nacionalidade AS nacionalidade, COUNT(*) AS quantidade
    FROM aero.empresas
    GROUP BY empresa_nacionalidade
    ORDER BY quantidade DESC
    '''
    df_nacionalidade = execute_query(query, return_df=True)

    fig = px.bar(
        df_nacionalidade,
        x='nacionalidade',
        y='quantidade',
        text='quantidade',
        color='nacionalidade',
        labels={'nacionalidade': 'Nacionalidade', 'quantidade': 'Quantidade'},
        title='Quantidade de Empresas por Nacionalidade',
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_tickangle=0)

    st.plotly_chart(fig, use_container_width=True)