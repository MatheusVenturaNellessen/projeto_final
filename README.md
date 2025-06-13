<h1>Projeto Final - Senai</h1>

<p align="justify">O objetivo deste projeto é aplicar, na prática, todas as etapas do processo de análise de dados, desde a compreensão dos dados brutos até a criação de visualizações interativas por meio do <strong>Streamlit</strong>. Este projeto representa a consolidação prática dos conhecimentos adquiridos durante a capacitação, integrando conceitos de <strong>data cleaning</strong>, <strong>bancos de dados relacionais</strong> e <strong>data visualization</strong>.</p>

<hr>

<h2>Tecnologias utilizadas</h2>
<ul>
    <li><strong>Pytohn v3.13.3</strong>: Compatível para analisar, processar, visualizar e interpretar dados com as blibiotecas/<i>frameworks</i> corretos;</li>
    <br>
    <li><strong>Pandas v2.2.3</strong>: Manipulação e análise de dados em tabelas (DataFrames).;</li>
    <br>
    <li><strong>PostegreSQL v17.5</strong>: Banco de dados relacional robusto, open source e muito usado em aplicações profissionais.;</li>
    <br>
    <li><strong>Psycopg2_binary v2.9.10</strong>: Driver para conectar e interagir com bancos de dados PostgreSQL;</li>
    <br>
    <li><strong>Streamlit v1.45.1</strong>:Framework para criar interfaces web interativas voltadas a análise de dados;</li>
    <br>
    <li><strong>Streamlit_extras v0.6.0</strong>: Conjunto de componentes prontos para enriquecer apps Streamlit;</li>
    <br>
    <li><strong>Plotly v6.1.2</strong>: Criação de gráficos interativos e dinâmicos;</li>
    <br>
    <li><strong>Matplotlib v3.10.3</strong>: Geração de gráficos e visualizações estáticas em 2D;</li>
    <br>
    <li><strong>Folium v0.19.7</strong>: Criação de mapas interativos baseados em Leaflet.js;</li>
    <br>
    <li><strong>Streamlit_folium v0.25.0</strong>: Integra mapas do Folium em apps Streamlit;</li>
    <br>
    <li><strong>Numpy v2.2.6</strong>: Cálculos numéricos e manipulação de arrays multidimensionais;</li>
    <br>
    <li><strong>Pillow v11.2.1</strong>: Manipulação e processamento de imagens (abreviação de "PIL").</li>
</ul>

<hr>

<h2>Estrutura do projeto</h2>

<pre>
PROJETO_FINAL_SENAI/
├── database/                                
│   ├── anac/                                   # contém o(s) arquivo(s) CSV origem e destino dos dados de aviação
│   └── spotify/                                # contém o(s) arquivo(s) CSV origem e destino dos dados de músicas  
│
├── frontend/                
│   ├── image/                                  # contém imagens utilizadas na aplicação
│   ├── esqueleto.py                            # script da seção da análise dos dados de músicas
│   └── plane.py                                # script da seção da análise dos dados de aviação
│   
├── scripts/                                    # contém querys SQL
│   ├── anac/
│   │   ├── create_tables.sql
│   │   └── views.sql
│   └── spotify/
│       └── create_tables_spotify.sql
│
├── utils/                                      # contém scripts úteis para funcionamnetos dos demais scritps
│   ├── anac/
│   │   ├── analise.py
│   │   ├── database.py
│   │   ├── metricas.py
│   │   └── views.py
│   └── spotify/
│       ├── analise_spotify.py
│       └── database.py
│
└── main.py                                     # script principal da aplicação
</pre>


<p align="justify">Alguns arquivos e diretórios foram omitidos por não serem essenciais para entendimento da estrutura do projeto.</p>

<hr>

<h2>Funcionalidades</h2>

<h3>[título da funcionalidade]</h3>
<img src="caminho/relativo/do/arquivo.gif" alt="texto alternativo"/>
<ul>
  <li>[descrição da(s) funcionalidade(s)]</li>
</ul>

<hr>

<h2>Como rodar esse projeto em seu ambiente</h2>

<h3>Pré-requisitos:</h3>
<ul>
  <li>Python v3.13.3 ou superior</li>
  <li>PostegreSQL v17.5 ou superior</li>
  <li>Git instalado</li>
  <li>Navegador moderno (Chrome, Firefox, etc.)</li>
</ul>

<h3>Passo a passo:</h3>
<ol>

  <li>
    <strong>Instale o Git (caso não possuir)</strong><br>
    Acesse: <a href="https://git-scm.com/downloads" target="_blank">git-scm.com/downloads</a><br>
    Baixe e instale conforme seu sistema operacional.<br>
    Verifique a instalação com:
    <pre><code>git --version</code></pre>
  </li>

  <li>
    <strong>Clone o repositório do projeto</strong>
    <pre><code>git clone https://github.com/MatheusVenturaNellessen/projeto_final_senai.git
cd seu/repositorio</code></pre>
  </li>

  <li>
    <strong>Instale as dependências do projeto</strong><br>
    <pre><code>pip install psycopg2-binary streamlit pandas numpy sqlalchemy matplotlib plotly folium streamlit-folium Pillow streamlit-extras</code></pre>
    Os detalhes das depedências do projeto estão em <a href="./depedencias.txt">depedencias.txt</a>.
  </li>

  <li>
      [falar sobre o PostegreSQL aqui]
  </li>
  
  <li>
    <strong>Execute a aplicação com Streamlit</strong>
    <pre><code>streamlit run main.py</code></pre>
    (Substitua <code>main.py</code> pelo nome do seu arquivo principal <strong>se for diferente</strong>.)
  </li>

  <li>
    <strong>Acesse no navegador</strong><br>
    Streamlit abrirá automaticamente. Caso contrário, acesse:
    <pre><code>http://localhost:8501</code></pre>
  </li>

</ol>

<hr>

<h2>⚠️ Importante</h2>

<p align="justify">Os dados utilizados neste projeto são de acesso público, obtidos exclusivamente a partir de fontes abertas como o <a href="https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023/data">Kaggle</a> e o portal da <a href="https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/dados-estatisticos/dados-estatisticos">Agência Nacional de Aviação Civil (ANAC)</a>. Nenhuma informação sigilosa, proprietária ou sensível foi empregada.</p>

<p align="justify">Este projeto tem caráter estritamente educacional, sendo desenvolvido com o objetivo de aprendizado e capacitação técnica na área de análise de dados. Não possui fins comerciais, tampouco representa qualquer tipo de vínculo, parecer oficial ou risco a organizações, empresas ou órgãos públicos mencionados direta ou indiretamente.</p>

<p align="justify">Reforçamos o compromisso com a ética, o uso responsável da informação e o respeito às diretrizes de uso das bases de dados públicas.</p>

<hr>

<h2>Contribuições</h2>
<p align="justify">Este projeto está aberto para contribuições via <i>issues</i>. Se você encontrou um <i>bug</i>, deseja sugerir uma melhoria ou tem dúvidas sobre o funcionamento, siga as instruções abaixo:</p>
<ol>
    <li>Verifique se já existe uma <i>issue</i> sobre o assunto. Caso sim, adicione um comentário nela.</li>
    <li>Se não houver, abra uma nova <i>issue</i> com uma descrição clara e objetiva.</li>
</ol>

<hr>

<h2>Licença e Autor</h2>
<p align="justify">Este projeto foi desenvolvido por <a href="https://github.com/MatheusVenturaNellessen">Matheus V. Nellessen</a>, <a href="https://github.com/andre-ciccozzi">André Cicozzi</a>, <a href="https://github.com/heitorkino">Heitor Aguiar</a>, <a href="https://github.com/LeoXP890">Leonardo Novi</a>, e está licenciado sob a licença MIT. Veja o <a href="./LICENSE">documento</a> para mais detalhes.</p>
