<h1>[título do projeto]</h1>

<p align="justify">[descrição do(s) objetivo(s)/proposta(s) do projeto]</p>

<hr>

<h2>Tecnologias utilizadas</h2>
<ul>
    <li><strong>[tecnologia] v[versão utilizado no desenvolvimento do projeto]</strong>: [breve descrição do que a tecnologia faz/fez]</li>
</ul>

<hr>

<h2>Estrutura das pastas</h2>

<pre>
EXEMPLO:
[NOME DO REPOSITÓRIO]/
├── csv/                        # comentário explicativo
│   └── arquivo.csv
├── database/
│   └── banco.db
├── modules/
│   ├── __pycache__/
│   └── mod1.py
└── main_app.py
</pre>

<p align="justify">[se omitir algum arquivo e/ou pasta, justificar aqui]</p>

<hr>

<h2>Funcionalidades</h2>

<h3 id="login-logout">[título da funcionalidade]</h3>
<img src="caminho/relativo/do/arquivo.gif" alt="texto alternativo" />
<ul>
  <li>[descrição da(s) funcionalidade(s)]</li>
</ul>

<hr>

<h2>Como rodar esse projeto em seu ambiente</h2>

<h3>Pré-requisitos:</h3>
<ul>
  <li>Python v3.13.3 ou superior</li>
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
    <pre><code>pip install streamlit pandas numpy plotly folium streamlit-folium pillow streamlit-extras</code></pre>
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

<p align="justify">Os dados utilizados neste projeto são de acesso público, obtidos exclusivamente a partir de fontes abertas como o Kaggle e o portal da Agência Nacional de Aviação Civil (ANAC). Nenhuma informação sigilosa, proprietária ou sensível foi empregada.</p>

<p align="justify">Este projeto tem caráter estritamente educacional, sendo desenvolvido com o objetivo de aprendizado e capacitação técnica na área de análise de dados. Não possui fins comerciais, tampouco representa qualquer tipo de vínculo, parecer oficial ou risco a organizações, empresas ou órgãos públicos mencionados direta ou indiretamente.</p>

<p align="justify">Reforçamos o compromisso com a ética, o uso responsável da informação e o respeito às diretrizes de uso das bases de dados públicas.</p>

<hr>

<h2>Contribuições</h2>
<p align="justify">Este projeto está aberto para contribuições via <i>>issues</i>. Se você encontrou um <i>bug</i>, deseja sugerir uma melhoria ou tem dúvidas sobre o funcionamento, siga as instruções abaixo:</p>
<ol>
    <li>Verifique se já existe uma <i>issue</i> sobre o assunto. Caso sim, adicione um comentário nela.</li>
    <li>Se não houver, abra uma nova <i>issue</i> com uma descrição clara e objetiva.</li>
</ol>

<hr>

<h2>Licença e Autor</h2>
<p align="justify">Este projeto foi desenvolvido por <a href="https://github.com/MatheusVenturaNellessen">Matheus V. Nellessen</a>, <a href="https://github.com/andre-ciccozzi">André Cicozzi</a>, <a href="https://github.com/heitorkino">Heitor Aguiar</a>, <a href="https://github.com/LeoXP890">Leonardo Novi</a>, e está licenciado sob a licença [acho bom licenciar o projeto sob alguma licença, existem várias]. Veja o <a href="./LICENSE">documento</a> para mais detalhes.</p>
