import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from home import load_images 

# Configuração da página com ícone de avião
st.set_page_config(
    page_title="Dashboard de Aviação",
    page_icon="✈️",
    layout="wide"
)

# Tema azul de aviação
st.markdown("""
    <style>
    /* Fundo da página */
    .main {
        background-color: #0a1a35;
        color: white;
    }

    /* Fundo da barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #0c2340;
        color: white;
        border-right: 1px solid #1e90ff;
    }

    /* Títulos - Azul claro para contraste */
    h1, h2, h3, h4 {
        color: #1e90ff;
        font-family: 'Arial', sans-serif;
    }

    /* Métricas - Estilo cockpit */
    .stMetric {
        background-color: #0c2340;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #1e90ff;
        box-shadow: 0 4px 8px rgba(30, 144, 255, 0.2);
    }

    /* Texto padrão */
    .css-18e3th9 {
        color: white;
    }

    /* Botões e controles */
    .st-bq {
        border-color: #1e90ff;
    }

    /* Barras de rolagem */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: #1e90ff;
        border-radius: 5px;
    }

    /* Gráficos - fundo transparente */
    .stPlotlyChart {
        background: transparent;
    }

    /* Cards de métricas */
    .css-1fv8s86 {
        background: linear-gradient(135deg, #0c2340 0%, #1e3d6b 100%);
    }

    </style>
""", unsafe_allow_html=True)

# Gerar base de dados fictícia de aviação
np.random.seed(42)
datas = pd.date_range(start="2024-01-01", periods=180)
companhias = ['Latam', 'Gol', 'Azul', 'Delta', 'Emirates']
rotas = ['GRU-JFK', 'GIG-MIA', 'BSB-MCO', 'POA-LAX', 'REC-YYZ']
tipos_voo = ['Comercial', 'Carga', 'Executivo', 'Militar']

dados = pd.DataFrame({
    'Data': np.random.choice(datas, size=500),
    'Companhia': np.random.choice(companhias, size=500),
    'Rota': np.random.choice(rotas, size=500),
    'Tipo Voo': np.random.choice(tipos_voo, size=500),
    'Passageiros': np.random.randint(50, 300, size=500),
    'Receita (US$)': np.random.randint(10000, 500000, size=500),
    'Atraso (min)': np.random.randint(0, 180, size=500)
})

# Logo e título com temática de aviação
st.title("✈️ Dashboard de Operações Aéreas")

with st.sidebar:
    st.image("plane.png", width=150)
    st.markdown("### Filtros de Operação")

# Filtros temáticos
companhia_selecionada = st.sidebar.multiselect(
    "Companhia Aérea:",
    options=dados["Companhia"].unique(),
    default=dados["Companhia"].unique()
)

rota_selecionada = st.sidebar.multiselect(
    "Rota:",
    options=dados["Rota"].unique(),
    default=dados["Rota"].unique()
)

tipo_voo_selecionado = st.sidebar.multiselect(
    "Tipo de Voo:",
    options=dados["Tipo Voo"].unique(),
    default=dados["Tipo Voo"].unique()
)

# Aplicar filtros
dados_filtrados = dados[
    (dados["Companhia"].isin(companhia_selecionada)) &
    (dados["Rota"].isin(rota_selecionada)) &
    (dados["Tipo Voo"].isin(tipo_voo_selecionado))
]

# Métricas (KPI) - Estilo cockpit
st.subheader("📊 Indicadores de Operação")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Voos", len(dados_filtrados), "Voos registrados")
col2.metric("Receita Total", f"US$ {dados_filtrados['Receita (US$)'].sum():,.2f}", "Faturamento")
col3.metric("Média de Atraso", f"{dados_filtrados['Atraso (min)'].mean():.1f} min", "Pontualidade")

# Gráficos com tema azul
st.subheader("📈 Desempenho por Rota")
vendas_por_rota = dados_filtrados.groupby('Rota')['Receita (US$)'].sum().sort_values(ascending=False)
st.bar_chart(vendas_por_rota, color='#1e90ff')

st.subheader("🛫 Passageiros Transportados por Companhia")
passageiros_por_companhia = dados_filtrados.groupby('Companhia')['Passageiros'].sum().sort_values(ascending=False)
st.area_chart(passageiros_por_companhia, color='#1e90ff')

# Dados detalhados
st.subheader("🗂️ Registros de Voos")
st.dataframe(
    dados_filtrados.sort_values(by="Data", ascending=False),
    column_config={
        "Receita (US$)": st.column_config.NumberColumn(format="US$ %.2f"),
        "Atraso (min)": st.column_config.ProgressColumn(min_value=0, max_value=180)
    },
    hide_index=True
)

def plane():
    st.title("Dashboard de Aviação")
    st.write("Monitoramento de voos e operações")
    
    if st.button("← Voltar ao Analytics Hub"):
        st.switch_page("../home.py")

if __name__ == "__main__":
    plane()