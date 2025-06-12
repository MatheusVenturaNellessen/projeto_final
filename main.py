import streamlit as st
from PIL import Image
import base64
import io
import frontend.plane as pln
import frontend.esqueleto as esq
st.set_page_config(page_title="Dashboard Aviação", page_icon="✈️", layout="wide")

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'plane'

with st.sidebar:
    col1, col2, col3 = st.columns(3)

    with col3:
        st.write('')
    with col2:
        btn_plane = st.button('Plane', key='btn_plane')
    with col1:
        btn_esqueleto = st.button('Spotify', key='btn_esqueleto')
    st.divider()

    # Atualiza o estado quando um botão é clicado
    if btn_plane:
        st.session_state.active_tab = 'plane'
    if btn_esqueleto:
        st.session_state.active_tab = 'esqueleto'

# Exibe o conteúdo com base no estado atual
if st.session_state.active_tab == 'plane':
    pln.plane()  # Conteúdo padrão (carrega inicialmente)
elif st.session_state.active_tab == 'esqueleto':
    esq.esqueleto()