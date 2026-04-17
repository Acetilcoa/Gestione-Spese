import psycopg2
from psycopg2 import sql
from datetime import datetime


# =========================
# CONFIG CONNESSIONE DB
# =========================
DB_NAME = "gestione_spese"
DB_USER = "postgres"
DB_PASSWORD = "Sbagliata_12"   
DB_HOST = "localhost"
DB_PORT = "5432"


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


# =========================
# FUNZIONI DI UTILITÀ
# =========================
def pausa():
    input("\nPremi INVIO per continuare...")


def valida_data(data_str):
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def valida_mese(mese_str):
    try:
        datetime.strptime(mese_str, "%Y-%m")
        return True
    except ValueError:
        return False


def categoria_esiste(conn, nome_categoria):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id_categoria FROM categorie WHERE LOWER(nome) = LOWER(%s);",
            (nome_categoria,)
        )
        return cur.fetchone()


# =========================
# MODULO 1 - GESTIONE CATEGORIE
# =========================
def gestione_categorie(conn):
    print("\n--- GESTIONE CATEGORIE ---")
    nome = input("Inserisci il nome della categoria: ").strip()

    if not nome:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_categoria FROM categorie WHERE LOWER(nome) = LOWER(%s);",
                (nome,)
            )
            if cur.fetchone():
                print("La categoria esiste già.")
                return

            cur.execute(
                "INSERT INTO categorie (nome) VALUES (%s);",
                (nome,)
            )
            conn.commit()
            print("Categoria inserita correttamente.")
    except Exception as e:
        conn.rollback()
        print(f"Errore durante l'inserimento della categoria: {e}")


# =========================
# MODULO 2 - INSERIMENTO SPESA
# =========================
def inserisci_spesa(conn):
    print("\n--- INSERISCI SPESA ---")

    data_spesa = input("Data (YYYY-MM-DD): ").strip()
    if not valida_data(data_spesa):
        print("Errore: formato data non valido.")
        return

    try:
        importo = float(input("Importo: ").strip())
        if importo <= 0:
            print("Errore: l'importo deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: inserisci un importo numerico valido.")
        return

    nome_categoria = input("Nome categoria: ").strip()
    descrizione = input("Descrizione (facoltativa): ").strip()

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_categoria FROM categorie WHERE LOWER(nome) = LOWER(%s);",
                (nome_categoria,)
            )
            risultato = cur.fetchone()

            if not risultato:
                print("Errore: la categoria non esiste.")
                return

            id_categoria = risultato[0]

            cur.execute("""
                INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
                VALUES (%s, %s, %s, %s);
            """, (data_spesa, importo, id_categoria, descrizione if descrizione else None))

            conn.commit()
            print("Spesa inserita correttamente.")
    except Exception as e:
        conn.rollback()
        print(f"Errore durante l'inserimento della spesa: {e}")


# =========================
# MODULO 3 - BUDGET MENSILE
# =========================
def definisci_budget(conn):
    print("\n--- DEFINISCI BUDGET MENSILE ---")

    mese = input("Mese (YYYY-MM): ").strip()
    if not valida_mese(mese):
        print("Errore: formato mese non valido.")
        return

    nome_categoria = input("Nome categoria: ").strip()

    try:
        importo_budget = float(input("Importo budget: ").strip())
        if importo_budget <= 0:
            print("Errore: il budget deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: inserisci un importo valido.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_categoria FROM categorie WHERE LOWER(nome) = LOWER(%s);",
                (nome_categoria,)
            )
            risultato = cur.fetchone()

            if not risultato:
                print("Errore: la categoria non esiste.")
                return

            id_categoria = risultato[0]

            cur.execute("""
                INSERT INTO budget_mensili (mese, id_categoria, importo_budget)
                VALUES (%s, %s, %s)
                ON CONFLICT (mese, id_categoria)
                DO UPDATE SET importo_budget = EXCLUDED.importo_budget;
            """, (mese, id_categoria, importo_budget))

            conn.commit()
            print("Budget mensile salvato correttamente.")
    except Exception as e:
        conn.rollback()
        print(f"Errore durante il salvataggio del budget: {e}")


# =========================
# REPORT 1 - TOTALE SPESE PER CATEGORIA
# =========================
def report_totale_per_categoria(conn):
    print("\n--- REPORT: TOTALE SPESE PER CATEGORIA ---")
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.nome, COALESCE(SUM(s.importo), 0) AS totale_speso
                FROM categorie c
                LEFT JOIN spese s ON c.id_categoria = s.id_categoria
                GROUP BY c.nome
                ORDER BY c.nome;
            """)
            risultati = cur.fetchall()

            if not risultati:
                print("Nessun dato disponibile.")
                return

            print(f"{'Categoria':<20}{'Totale Speso':>15}")
            print("-" * 35)
            for nome, totale in risultati:
                print(f"{nome:<20}{float(totale):>15.2f}")

    except Exception as e:
        print(f"Errore nel report: {e}")


# =========================
# REPORT 2 - SPESE MENSILI VS BUDGET
# =========================
def report_spese_vs_budget(conn):
    print("\n--- REPORT: SPESE MENSILI VS BUDGET ---")
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    b.mese,
                    c.nome,
                    b.importo_budget,
                    COALESCE(SUM(s.importo), 0) AS totale_speso
                FROM budget_mensili b
                JOIN categorie c ON b.id_categoria = c.id_categoria
                LEFT JOIN spese s
                    ON s.id_categoria = b.id_categoria
                    AND TO_CHAR(s.data_spesa, 'YYYY-MM') = b.mese
                GROUP BY b.mese, c.nome, b.importo_budget
                ORDER BY b.mese, c.nome;
            """)
            risultati = cur.fetchall()

            if not risultati:
                print("Nessun budget disponibile.")
                return

            for mese, categoria, budget, speso in risultati:
                stato = "SUPERAMENTO BUDGET" if float(speso) > float(budget) else "NEL BUDGET"
                print(f"\nMese: {mese}")
                print(f"Categoria: {categoria}")
                print(f"Budget: {float(budget):.2f}")
                print(f"Speso: {float(speso):.2f}")
                print(f"Stato: {stato}")

    except Exception as e:
        print(f"Errore nel report: {e}")


# =========================
# REPORT 3 - ELENCO COMPLETO SPESE
# =========================
def report_elenco_spese(conn):
    print("\n--- REPORT: ELENCO COMPLETO DELLE SPESE ---")
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    s.data_spesa,
                    c.nome,
                    s.importo,
                    COALESCE(s.descrizione, '')
                FROM spese s
                JOIN categorie c ON s.id_categoria = c.id_categoria
                ORDER BY s.data_spesa ASC, s.id_spesa ASC;
            """)
            risultati = cur.fetchall()

            if not risultati:
                print("Nessuna spesa registrata.")
                return

            print(f"{'Data':<12}{'Categoria':<20}{'Importo':>12}   {'Descrizione'}")
            print("-" * 70)
            for data_spesa, categoria, importo, descrizione in risultati:
                print(f"{str(data_spesa):<12}{categoria:<20}{float(importo):>12.2f}   {descrizione}")

    except Exception as e:
        print(f"Errore nel report: {e}")


# =========================
# SOTTOMENU REPORT
# =========================
def visualizza_report(conn):
    while True:
        print("\n--- MENU REPORT ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")

        scelta = input("Inserisci la tua scelta: ").strip()

        if scelta == "1":
            report_totale_per_categoria(conn)
            pausa()
        elif scelta == "2":
            report_spese_vs_budget(conn)
            pausa()
        elif scelta == "3":
            report_elenco_spese(conn)
            pausa()
        elif scelta == "4":
            break
        else:
            print("Scelta non valida. Riprovare.")


# =========================
# MENU PRINCIPALE
# =========================
def menu_principale(conn):
    while True:
        print("\n-------------------------")
        print("SISTEMA SPESE PERSONALI")
        print("-------------------------")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        print("-------------------------")

        scelta = input("Inserisci la tua scelta: ").strip()

        if scelta == "1":
            gestione_categorie(conn)
            pausa()
        elif scelta == "2":
            inserisci_spesa(conn)
            pausa()
        elif scelta == "3":
            definisci_budget(conn)
            pausa()
        elif scelta == "4":
            visualizza_report(conn)
        elif scelta == "5":
            print("Uscita dal programma. Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprovare.")


# =========================
# MAIN
# =========================
def main():
    try:
        conn = get_connection()
        print("Connessione al database riuscita.")
        print("Benvenuto nel Sistema di Gestione delle Spese Personali e del Budget.")
        menu_principale(conn)
        conn.close()
    except Exception as e:
        print(f"Errore di connessione al database: {e}")


if __name__ == "__main__":
    main()
