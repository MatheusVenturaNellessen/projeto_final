SET search_path TO aero;

CREATE TABLE IF NOT EXISTS empresas(
    id_empresas SERIAL PRIMARY KEY,
    empresa_nome VARCHAR(100) NOT NULL,
    empresa_sigla VARCHAR(10) NOT NULL,
    empresa_nacionalidade VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS aeroportos_origem (
    id_aeroporto_origem SERIAL PRIMARY KEY,
    aeroporto_origem_sigla VARCHAR(10) NOT NULL UNIQUE,
    aeroporto_origem_nome VARCHAR(100),
    aeroporto_origem_uf VARCHAR(10) NOT NULL,
    aeroporto_origem_regiao VARCHAR(50) NOT NULL,
    aeroporto_origem_pais VARCHAR(50) NOT NULL,
    aeroporto_origem_continente VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS aeroportos_destino (
    id_aeroporto_destino SERIAL PRIMARY KEY,
    aeroporto_destino_sigla VARCHAR(10) NOT NULL UNIQUE,
    aeroporto_destino_nome VARCHAR(100),
    aeroporto_destino_uf VARCHAR(10) NOT NULL,
    aeroporto_destino_regiao VARCHAR(50) NOT NULL,
    aeroporto_destino_pais VARCHAR(50) NOT NULL,
    aeroporto_destino_continente VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS voos (
    id_voos INTEGER PRIMARY KEY,
    empresa_id INTEGER NOT NULL,
    aeroporto_origem_id INTEGER NOT NULL,
    aeroporto_destino_id INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    natureza VARCHAR(50) NOT NULL,
    grupo_voo VARCHAR(50) NOT NULL,
    passageiros_pagos INTEGER NOT NULL,
    passageiros_gratis INTEGER NOT NULL,
    carga_paga_kg INTEGER NOT NULL,
    carga_gratis_kg INTEGER NOT NULL,
    correios_kg INTEGER NOT NULL,
    ask INTEGER NOT NULL,
    rpk INTEGER NOT NULL,
    atk INTEGER NOT NULL,
    rtk INTEGER NOT NULL,
    combustivel_litros INTEGER NOT NULL,
    distancia_voada_km INTEGER NOT NULL,
    decolagens INTEGER NOT NULL,
    assentos INTEGER NOT NULL,
    payload INTEGER NOT NULL,
    HORAS_VOADAS REAL NOT NULL,
    bagagem_kg INTEGER NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id_empresas),
    FOREIGN KEY (aeroporto_origem_id) REFERENCES aeroportos_origem(id_aeroporto_origem),
    FOREIGN KEY (aeroporto_destino_id) REFERENCES aeroportos_destino(id_aeroporto_destino)
);

