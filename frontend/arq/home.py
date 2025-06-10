import streamlit as st
from PIL import Image
import base64
import io

# Configuração da página
st.set_page_config(
    page_title="Analytics Hub",
    page_icon="📊",
    layout="centered"
)

# Função para converter imagem para base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Carrega as imagens diretamente (sem função separada)
try:
    music_img = Image.open("music.png")
    airplane_img = Image.open("aviao.png")
except FileNotFoundError:
    st.error("Arquivos de imagem não encontrados!")
    st.stop()

# Estilos CSS
st.markdown("""
<style>
    .card {
        padding: 2rem;
        border-radius: 10px;
        background: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        text-align: center;
        cursor: pointer;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem;
        color: #1F2937;
    }
    .card-subtitle {
        font-size: 0.9rem;
        color: #6B7280;
        margin-bottom: 1.5rem;
    }
    .access-btn {
        border: none;
        background: none;
        color: #2563EB;
        font-weight: 500;
        cursor: pointer;
        padding: 0;
    }
    .card-image-container {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>ANALYTICS HUB</h1>", unsafe_allow_html=True)

# Layout dos cards
col1, col2 = st.columns(2, gap="large")

# Card 1 - Música
with col1:
    st.markdown(f"""
    <div class="card" onclick="window.location.href='?page=music'">
        <div class="card-image-container">
            <img src="data:image/png;base64,{image_to_base64(music_img)}" width="80">
        </div>
        <div class="card-title">Dashboard Musical</div>
        <div class="card-subtitle">Análise de streaming e catálogo</div>
        <div class="access-btn">ACESSAR</div>
    </div>
    """, unsafe_allow_html=True)

# Card 2 - Aviação
with col2:
    st.markdown(f"""
    <div class="card" onclick="window.location.href='?page=aviation'">
        <div class="card-image-container">
            <img src="data:image/png;base64,{image_to_base64(airplane_img)}" width="80">
        </div>
        <div class="card-title">Dashboard de Aviação</div>
        <div class="card-subtitle">Monitoramento de voos e operações</div>
        <div class="access-btn">ACESSAR</div>
    </div>
    """, unsafe_allow_html=True)