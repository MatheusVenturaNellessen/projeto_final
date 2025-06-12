import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

@st.cache_data
def carregar_dados():
    return pd.read_csv(r"C:\Users\andre\Downloads\Trabalho_Final_Atualizado\projeto_final_anac\database\anac\anaca_2025_limpo.csv", encoding="ISO-8859-1", sep=';')
df = carregar_dados()

# Coordenadas conhecidas (adicione mais se necessário)
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


st.title("Voos com origem em Guarulhos (SBGR)")
st_folium(mapa, width=725, height=500)

st.markdown("""
<div style="border: 2px solid #302681; border-radius: 12px; padding: 20px; background-color: #f9f9f9;">
  <h3 style="color:#302681;">✈️ Voos com origem em Guarulhos (SBGR)</h3>
  <ul style="font-size:16px; line-height:1.6;">
    <li><strong>Guarulhos (SBGR) → Galeão - RJ (SBGL)</strong><br>
        Voo doméstico, conectando São Paulo ao Rio de Janeiro.</li>
    <li><strong>Guarulhos (SBGR) → Manaus (SBEG)</strong><br>
        Rota nacional, do sudeste ao norte do Brasil.</li>
    <li><strong>Guarulhos (SBGR) → Bogotá - Colômbia (SKBO)</strong><br>
        Voo internacional para a capital colombiana.</li>
    <li><strong>Guarulhos (SBGR) → Georgetown - Guiana (SYCJ)</strong><br>
        Voo internacional para a capital da Guiana.</li>
  </ul>
</div>
""", unsafe_allow_html=True)


