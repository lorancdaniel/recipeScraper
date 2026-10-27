from sqlalchemy import create_engine, text

from database.models import Base
from database.session import DB_NAME, engine, make_url


def create_database():
    # Połączenie z domyślną bazą danych – CREATE DATABASE nie może działać wewnątrz transakcji
    admin_engine = create_engine(make_url("postgres"), isolation_level="AUTOCOMMIT")
    try:
        with admin_engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_catalog.pg_database WHERE datname = :name"),
                {"name": DB_NAME},
            ).scalar()

            if exists:
                print(f"Baza danych '{DB_NAME}' już istnieje.")
            else:
                # Nazwy bazy nie da się przekazać jako parametru, więc jest bezpiecznie cytowana
                name = admin_engine.dialect.identifier_preparer.quote_identifier(DB_NAME)
                conn.execute(text(f"CREATE DATABASE {name}"))
                print(f"Baza danych '{DB_NAME}' została utworzona.")
    finally:
        admin_engine.dispose()


def create_tables():
    # Tabele tworzone są na podstawie modeli z database/models.py
    Base.metadata.create_all(engine)
    print("Tabele zostały utworzone.")


if __name__ == "__main__":
    create_database()
    create_tables()
