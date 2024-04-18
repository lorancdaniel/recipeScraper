import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# Połączenie z bazą danych
engine = create_engine('postgresql://postgres:8513@localhost/recipeDatabase')
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

# Tworzenie tabeli w bazie danych (jeśli nie istnieje)
Base.metadata.create_all(engine)

url = "https://aniagotuje.pl/przepis/chleb-na-zakwasie"
print(url)
try:
    response = requests.get(url)
    response.raise_for_status()  # Sprawdzenie statusu odpowiedzi
except requests.exceptions.RequestException as e:
    print("Błąd podczas pobierania strony:", e)
    exit(1)

try:
    soup = BeautifulSoup(response.content, "html.parser")
    recipe = soup.find("article", {"itemtype": "https://schema.org/Recipe"})

    if recipe:
        title = recipe.find("h1", itemprop="name")
        title = title.text.strip() if title else None

        ingredients = recipe.find("ul", class_="recipe-ing-list")
        ingredient_list = [li.span.text.strip() for li in ingredients.find_all("li")] if ingredients else []

        # Dodatkowe pola do pobrania (dostosuj według struktury strony)
        preparation_time = recipe.find("meta", itemprop="prepTime")
        preparation_time = int(preparation_time["content"].split("T")[0]) if preparation_time else None

        image_url = recipe.find("meta", itemprop="image")
        image_url = image_url["content"] if image_url else None

        description = recipe.find("div", class_="article-intro")
        description = description.text.strip() if description else None

        instructions = recipe.find("div", itemprop="recipeInstructions")
        instructions = instructions.text.strip() if instructions else None

        source_url = url

        # Tworzenie obiektu przepisu
        przepis = Przepis(
            nazwa=title,
            czas_przygotowania=preparation_time,
            zdjecie_url=image_url,
            opis=description,
            instrukcja=instructions,
            skladniki=", ".join(ingredient_list),
            zrodlo_url=source_url
        )

        # Dodawanie przepisu do sesji
        session = Session()
        session.add(przepis)
        session.commit()
        session.close()
    else:
        print("Nie znaleziono przepisu na stronie.")

except (AttributeError, KeyError) as e:
    print("Błąd podczas przetwarzania przepisu:", e)