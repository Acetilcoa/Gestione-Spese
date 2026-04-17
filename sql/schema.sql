-- =========================
-- DATABASE: gestione_spese
-- =========================

-- Tabella categorie
CREATE TABLE IF NOT EXISTS categorie (
    id_categoria SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Tabella spese
CREATE TABLE IF NOT EXISTS spese (
    id_spesa SERIAL PRIMARY KEY,
    data_spesa DATE NOT NULL,
    importo NUMERIC(10,2) NOT NULL CHECK (importo > 0),
    id_categoria INTEGER NOT NULL,
    descrizione VARCHAR(255),
    CONSTRAINT fk_spese_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categorie(id_categoria)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Tabella budget mensili
CREATE TABLE IF NOT EXISTS budget_mensili (
    id_budget SERIAL PRIMARY KEY,
    mese CHAR(7) NOT NULL,
    id_categoria INTEGER NOT NULL,
    importo_budget NUMERIC(10,2) NOT NULL CHECK (importo_budget > 0),
    CONSTRAINT uq_budget_mese_categoria UNIQUE (mese, id_categoria),
    CONSTRAINT fk_budget_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categorie(id_categoria)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_formato_mese
        CHECK (mese ~ '^[0-9]{4}-(0[1-9]|1[0-2])$')
);