import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Dane do połączenia z bazą danych
username = "postgres"
password = "8513"
host = "localhost"
default_db = "postgres"
db_name = "recipeDatabase"

# Połączenie z domyślną bazą danych, aby sprawdzić istnienie docelowej bazy danych
conn = psycopg2.connect(dbname=default_db, user=username, password=password, host=host)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Utworzenie kursora
cur = conn.cursor()

# Sprawdzenie, czy baza danych już istnieje
cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
exists = cur.fetchone()

if not exists:
    # Tworzenie nowej bazy danych
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    print(f"Baza danych '{db_name}' została utworzona.")
else:
    print(f"Baza danych '{db_name}' już istnieje.")

# Zamknięcie połączenia z domyślną bazą danych
cur.close()
conn.close()

# Połączenie z nowo utworzoną bazą danych
conn = psycopg2.connect(dbname=db_name, user=username, password=password, host=host)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Definicja tabeli przepisy
create_table_query = """
CREATE TABLE IF NOT EXISTS przepisy (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(255) NOT NULL,
    czas_przygotowania INTEGER,
    zdjecie_url VARCHAR(255),
    opis TEXT,
    instrukcja TEXT,
    skladniki TEXT,
    zrodlo_url VARCHAR(255)
);
"""

# Tworzenie tabeli przepisy
cur.execute(create_table_query)
print("Tabele zostały utworzone.")

# Zamknięcie połączenia z bazą danych
cur.close()
conn.close()
