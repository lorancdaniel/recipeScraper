import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

# Konfiguracja połączenia z bazą danych – wartości można nadpisać zmiennymi środowiskowymi
DB_NAME = os.getenv("DB_NAME", "recipeDatabase")


def make_url(database=DB_NAME):
    return URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=database,
    )


engine = create_engine(make_url())
Session = sessionmaker(bind=engine)
