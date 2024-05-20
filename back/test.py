import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Dane do połączenia z bazą danych
username = "recipe"
password = "8513"
host = "83.150.236.193"
db_name = "recipeDatabase"

# Funkcja pomocnicza do nawiązywania połączenia z bazą danych
def get_db_connection():
    print("🛸 lacze z baza")
    try:
        conn = psycopg2.connect(dbname=db_name, user=username, password=password, host=host)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
