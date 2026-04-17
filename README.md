# Sistema di Gestione delle Spese Personali e del Budget

## Descrizione

Questo progetto è un'applicazione da terminale sviluppata in Python che consente di gestire le spese personali e il budget mensile.

L'utente può:

* creare categorie di spesa (es. Alimentari, Trasporti, Salute)
* inserire spese giornaliere
* definire un budget mensile per categoria
* visualizzare report riepilogativi

I dati vengono salvati in un database PostgreSQL.

## Requisiti

Per eseguire il progetto è necessario avere installato:

* Python 3.12 (versione consigliata)
* PostgreSQL
* Libreria Python `psycopg2`

## Cos’è psycopg2?

`psycopg2` è una libreria Python che permette al programma di comunicare con il database PostgreSQL.

In pratica:
Python → psycopg2 → PostgreSQL

## Installazione dipendenze

Aprire il terminale e installare la libreria necessaria tramite il comando:

```bash
pip install psycopg2-binary
```

Se si utilizza più versioni di Python:

```bash
py -3.12 -m pip install psycopg2-binary
```

## Configurazione del database

1. Aprire pgAdmin o PostgreSQL

2. Creare un nuovo database chiamato:
gestione_spese

3. Eseguire il file:

```bash
sql/schema.sql
```

4. Eseguire il file:

```bash
sql/dati_test.sql
```

## Configurazione del programma

Aprire il file:

```text
src/app.py
```

e modificare i dati di connessione al database:

```python
DB_NAME = "gestione_spese"            #cambiare questi dati con i dati specifici del
DB_USER = "postgres"                  #proprio database
DB_PASSWORD = "LA_TUA_PASSWORD"
DB_HOST = "localhost"
DB_PORT = "5432"
```

## Avvio del programma

Dal terminale, nella cartella del progetto, eseguire:
python src/app.py
Oppure:
py -3.12 src/app.py

## Funzionamento

All’avvio viene mostrato un menu da cui è possibile:

1. Gestire le categorie
2. Inserire una spesa
3. Definire un budget mensile
4. Visualizzare report

## Report disponibili

* Totale spese per categoria
* Confronto spese vs budget mensile
* Elenco completo delle spese ordinate per data

## Struttura del progetto

```text
gestione_spese/
│
├── src/
│   └── app.py
│
├── sql/
│   ├── schema.sql
│   └── dati_test.sql
│
├── demo/
│   └── demo_video.mp4
│
└── README.md
```

## Demo

Nel repository è presente un video che mostra il funzionamento completo del programma.

## Note
Il progetto è stato sviluppato a scopo didattico per dimostrare:

* utilizzo di Python
* interazione con database SQL
* gestione dei dati e validazione degli input
