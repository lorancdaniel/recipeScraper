from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

# Konfiguracja połączenia z bazą danych
url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="8513",
    host="localhost",
    database="recipeDatabase"
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)