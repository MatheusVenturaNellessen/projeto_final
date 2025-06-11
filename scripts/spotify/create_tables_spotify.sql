SET search_path to spotify;

CREATE TABLE IF NOT EXISTS artistas(
    id_artista SERIAL PRIMARY KEY,
    nome_artista VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS musicas(
    id_musica SERIAL PRIMARY KEY,
    nome_artistico VARCHAR(255),
    data_lancamento DATE,
    modo VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS musicas_artistas(
    id_musica INT REFERENCES musicas(id_musica),
    id_artista INT REFERENCES Artistas(id_artista),
    PRIMARY KEY (id_musica, id_artista)
);

CREATE TABLE IF NOT EXISTS plataformas (
    id_musica INT PRIMARY KEY REFERENCES musicas(id_musica),
    qtd_playlists_spotify INT,
    qtd_destaques_spotify INT,
    qtd_playlists_apple INT,
    qtd_destaques_apple INT,
    qtd_playlists_deezer INT,
    qtd_destaques_deezer INT,
    qtd_destaques_shazam INT
);

CREATE TABLE IF NOT EXISTS transmissoes (
    id_musica INT PRIMARY KEY REFERENCES musicas(id_musica),
    qtd_transmissoes BIGINT
);

