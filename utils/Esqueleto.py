import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.markdown("""
    <style>
    /* Fundo da página */
    .main {
        background-color: #191414;
        color: white;
    }

    /* Fundo da barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #000000;
        color: white;
    }

    /* Títulos */
    h1, h2, h3, h4 {
        color: #1DB954;
    }

    /* Métricas */
    .stMetric {
        background-color: #121212;
        padding: 10px;
        border-radius: 10px;
    }

    /* Texto padrão */
    .css-18e3th9 {
        color: white;
    }

    /* Barras de rolagem e detalhes */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: #1DB954;
        border-radius: 5px;
    }

    </style>
""", unsafe_allow_html=True)

# Gerar base de dados fictícia
np.random.seed(42)
datas = pd.date_range(start="2024-01-01", periods=180)
categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Brinquedos']
regioes = ['Sul', 'Sudeste', 'Nordeste', 'Norte', 'Centro-Oeste']

dados = pd.DataFrame({
    'Data': np.random.choice(datas, size=500),
    'Categoria': np.random.choice(categorias, size=500),
    'Região': np.random.choice(regioes, size=500),
    'Vendas': np.random.randint(100, 5000, size=500)
})

# Título
st.title("📊 Dashboard de Vendas")

with st.sidebar:
    st.image("logo.png", width=150)

# Filtros na barra lateral
regiao_selecionada = st.sidebar.multiselect(
    "Região:",
    options=dados["Região"].unique(),
    default=dados["Região"].unique()
)

categoria_selecionada = st.sidebar.multiselect(
    "Categoria:",
    options=dados["Categoria"].unique(),
    default=dados["Categoria"].unique()
)

# Aplicar filtros
dados_filtrados = dados[
    (dados["Região"].isin(regiao_selecionada)) &
    (dados["Categoria"].isin(categoria_selecionada))
]   

# Métricas principais
st.subheader("📌 Indicadores")
col1, col2 = st.columns(2)
col1.metric("Total de Vendas", f"R$ {dados_filtrados['Vendas'].sum():,.2f}")
col2.metric("Média por Venda", f"R$ {dados_filtrados['Vendas'].mean():,.2f}")

# Gráfico de vendas por data - CORREÇÃO: especificar a coluna 'Vendas'
st.subheader("📈 Vendas ao Longo do Tempo")
vendas_por_dia = dados_filtrados.groupby('Data')['Vendas'].sum().sort_index()
st.line_chart(vendas_por_dia)

# Gráfico de vendas por categoria - CORREÇÃO: especificar a coluna 'Vendas'
st.subheader("📊 Vendas por Categoria")
vendas_categoria = dados_filtrados.groupby('Categoria')['Vendas'].sum().sort_values(ascending=False)
st.bar_chart(vendas_categoria)

# Mostrar tabela
st.subheader("🗃️ Dados Detalhados")
st.dataframe(dados_filtrados.sort_values(by="Data", ascending=False))