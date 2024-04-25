import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from gpt_formatting import recipeGenerator
import asyncio
import json

username = "recipe"
password = "8513"
host = "83.150.236.193"
default_db = "postgres"
db_name = "recipeDatabase"

# Połączenie z bazą danych
engine = create_engine(f'postgresql://{username}:{password}@{host}/{db_name}')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Definicja modelu tabeli przepisy
class Przepis(Base):
    __tablename__ = 'przepisy'
    id = Column(Integer, primary_key=True)
    nazwa = Column(String(255), nullable=False)
    czas_przygotowania = Column(Integer)
    zdjecie_url = Column(String(255))
    opis = Column(Text)
    instrukcja = Column(Text)
    skladniki = Column(Text)
    zrodlo_url = Column(String(255))

#scrapowanie body
url = "https://www.kwestiasmaku.com/kuchnia_polska/nalesniki/nalesniki.html"
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")
body = soup.find("body")
body_content = body.get_text()
formattedRecipe = asyncio.run(recipeGenerator(body_content))
print(formattedRecipe)
formattedRecipe = json.loads(formattedRecipe)
print(formattedRecipe)
new_recipe = Przepis(
    nazwa=formattedRecipe['nazwa'],
    czas_przygotowania=formattedRecipe['czas_przygotowania'],
    zdjecie_url=formattedRecipe['zdjecie_url'],
    opis=formattedRecipe['opis'],
    instrukcja=formattedRecipe['instrukcja'],
    skladniki=formattedRecipe['skladniki'],
    zrodlo_url=url
)

# Dodawanie przepisu do bazy danych
session = Session()
session.add(new_recipe)
session.commit()
print("Przepis został dodany do bazy danych.")
