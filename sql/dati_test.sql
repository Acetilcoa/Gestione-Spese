-- =========================
-- DATI DI TEST
-- =========================

INSERT INTO categorie (nome) VALUES
('Alimentari'),
('Trasporti'),
('Bollette'),
('Svago')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
SELECT '2026-01-10', 45.50, id_categoria, 'Spesa supermercato'
FROM categorie WHERE nome = 'Alimentari'
ON CONFLICT DO NOTHING;

INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
SELECT '2026-01-12', 20.00, id_categoria, 'Benzina'
FROM categorie WHERE nome = 'Trasporti'
ON CONFLICT DO NOTHING;

INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
SELECT '2026-01-15', 80.00, id_categoria, 'Luce'
FROM categorie WHERE nome = 'Bollette'
ON CONFLICT DO NOTHING;

INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
SELECT '2026-01-20', 30.00, id_categoria, 'Cinema'
FROM categorie WHERE nome = 'Svago'
ON CONFLICT DO NOTHING;

INSERT INTO budget_mensili (mese, id_categoria, importo_budget)
SELECT '2026-01', id_categoria, 200.00
FROM categorie WHERE nome = 'Alimentari'
ON CONFLICT (mese, id_categoria) DO NOTHING;

INSERT INTO budget_mensili (mese, id_categoria, importo_budget)
SELECT '2026-01', id_categoria, 100.00
FROM categorie WHERE nome = 'Trasporti'
ON CONFLICT (mese, id_categoria) DO NOTHING;

INSERT INTO budget_mensili (mese, id_categoria, importo_budget)
SELECT '2026-01', id_categoria, 150.00
FROM categorie WHERE nome = 'Bollette'
ON CONFLICT (mese, id_categoria) DO NOTHING;