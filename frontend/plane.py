import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px

# ============== CONFIG E DADOS ==============
def plane():
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

    df = pd.read_csv("database\\anac\\anaca_2025_limpo.csv", sep=';', encoding='latin1')

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
    st.sidebar.image("frontend\\image\\plane.png", width=150)

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

        with st.expander('Clique aqui para visualizar ruídos.'):
            colunas_numericas = ['passageiros_pagos', 'passageiros_gratis', 'carga_paga_kg', 'carga_gratis_kg', 'correios_kg', 'ask', 'rpk', 'atk', 'rtk', 'combustivel_litros', 'distancia_voada_km', 'decolagens', 'carga_paga_km', 'carga_gratis_km', 'correio_km', 'assentos', 'payload', 'HORAS_VOADAS', 'bagagem_kg']

            st.sidebar.markdown('''
                <h2 class="emoji-after">Personalize as Métricas!</h2>
            ''', unsafe_allow_html=True)
            empresas = sorted(df['empresa_sigla'].unique())
            default = sorted(['AZU', 'LAN', 'GLO', 'AAL', 'UAE'])
            empresas_selecionadas = st.sidebar.multiselect("Selecione as empresas", empresas, default=list(default))

            # coluna = st.sidebar.selectbox("Selecione um atributo:", colunas_numericas)

            x_col = st.sidebar.selectbox("Coluna do eixo X (horizontal):", colunas_numericas, index=0, help='O gráfico de dispersão mostra a relação entre dois atributos selecionados. Pontos alinhados indicam correlação entre as variáveis, enquanto pontos espalhados mostram pouca relação. As cores representam diferentes empresas e pontos isolados podem indicar erros ou situações fora do padrão.')
            y_col = st.sidebar.selectbox("Coluna do eixo Y (vertical):", colunas_numericas, index=1)

            df_filtrado = df[df['empresa_sigla'].isin(empresas_selecionadas)]

            # Boxplot com Plotly
            fig = px.scatter(
                df_filtrado,
                x=x_col,
                y=y_col,
                color="empresa_sigla",
                hover_data=["empresa_nome", "ano", "mes", "aeroporto_origem_sigla", "aeroporto_destino_sigla"],  # infos extras ao passar mouse
                title=f"Dispersão de {y_col} vs. {x_col} por Empresa",
                labels={x_col: x_col, y_col: y_col, "empresa_sigla": "Empresa"},
            )
            st.plotly_chart(fig, use_container_width=True)

            # Coeficiente de Variação (opcional: para cada eixo)
            st.subheader("Coeficiente de Variação (por empresa)")
            cv_x = df_filtrado.groupby("empresa_sigla")[x_col].std() / df_filtrado.groupby("empresa_sigla")[x_col].mean()
            cv_y = df_filtrado.groupby("empresa_sigla")[y_col].std() / df_filtrado.groupby("empresa_sigla")[y_col].mean()
            st.dataframe(pd.DataFrame({f"CV {x_col}": cv_x.round(3), f"CV {y_col}": cv_y.round(3)}))

            # Quantidade de outliers usando IQR para ambos eixos
            def conta_outliers(s):
                q1 = s.quantile(0.25)
                q3 = s.quantile(0.75)
                iqr = q3 - q1
                return ((s < (q1 - 1.5 * iqr)) | (s > (q3 + 1.5 * iqr))).sum()
            outliers_x = df_filtrado.groupby("empresa_sigla")[x_col].apply(conta_outliers)
            outliers_y = df_filtrado.groupby("empresa_sigla")[y_col].apply(conta_outliers)

            st.markdown('''<h2>Quantidade de Outliers (por empresa)</h2>''', unsafe_allow_html=True)

            st.dataframe(pd.DataFrame({f"Qtd de Outliers ({x_col})": outliers_x, f"Qtd de Outliers ({y_col})": outliers_y}))

            st.markdown('''
    	        <div class="info">Outliers</div>
            ''', unsafe_allow_html=True)

    # ============= MÉTRICAS =============
    if page == "Métricas":
        st.markdown('''<h1>🏆 Top 5 Empresas</h1>''', unsafe_allow_html=True)

        agg = (df.groupby("data")[["rpk", "ask", "atk", "rtk"]]
            .sum()
            .assign(load_factor=lambda x: 100 * x.rpk / x.ask.replace(0, np.nan),
                    eficiencia_carga=lambda x: 100 * x.rtk / x.atk.replace(0, np.nan))
            .fillna(0)
            .reset_index())

        # Cards customizados
        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.markdown(f'''
                <div class="container">
                    <div class="title">RPK</div>
                    <div class="text">{(agg.rpk.iloc[-1] / 1e9):.2f}</div>
                    <div class="info">Ipsum lorem</div>
                </div>
            ''', unsafe_allow_html=True)
        with col5:
            st.markdown(f'''
                <div class="container">
                    <div class="title">ASK</div>
                    <div class="text">{(agg.ask.iloc[-1] / 1e9):.2f}</div>
                    <div class="info">Ipsum lorem</div>
                </div>
            ''', unsafe_allow_html=True)
        with col6:
            st.markdown(f'''
                <div class="container">
                    <div class="title">Load Factor (%)</div>
                    <div class="text">{(agg.load_factor.iloc[-1]):.2f}</div>
                    <div class="info">Ipsum lorem</div>
                </div>
            ''', unsafe_allow_html=True)
        with col7:
            st.markdown(f'''
                <div class="container">
                    <div class="title">Eficiência Carga (%)</div>
                    <div class="text">{(agg.eficiencia_carga.iloc[-1]):.2f}</div>
                    <div class="info">Ipsum lorem</div>
                </div>
            ''', unsafe_allow_html=True)

        opcoes = ["rpk", "ask", "load_factor", "rtk", "atk", "eficiencia_carga"]

        st.sidebar.markdown('''
            <h2 class="emoji-after">Personalize as Métricas!</h2>
        ''', unsafe_allow_html=True)
        metrica_rank = st.sidebar.selectbox("Escolha a métrica:", options=opcoes, index=0)

        ultimo_mes = df["data"].max()
        base = df[df["data"] == ultimo_mes]

        if metrica_rank in ["load_factor", "eficiencia_carga"]:
            tbl = (base.groupby("empresa_sigla")[["rpk", "ask", "rtk", "atk"]].sum())
            tbl["load_factor"] = 100 * tbl["rpk"] / tbl["ask"].replace(0, np.nan)
            tbl["eficiencia_carga"] = 100 * tbl["rtk"] / tbl["atk"].replace(0, np.nan)
            top5 = tbl[metrica_rank].nlargest(5).reset_index()
        else:
            top5 = (base.groupby("empresa_sigla")[metrica_rank].sum().nlargest(5).reset_index())


        st.markdown('''<hr>''', unsafe_allow_html=True)
        st.markdown('''<h2>Histograma: Métricas por Empresa</h2>''', unsafe_allow_html=True)
        st.bar_chart(top5.set_index("empresa_sigla")[metrica_rank], use_container_width=True, x_label='Top 5 Empresas', y_label='Valor da Métrica')

        st.markdown('''<hr>''', unsafe_allow_html=True)
        st.markdown('''<h2>SQL View: Métricas por Empresa</h2>''', unsafe_allow_html=True)
        st.dataframe(top5, use_container_width=True)


    # ============= ANÁLISES GRÁFICAS =============
    if page == "Análises Gráficas":
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
