import re
import sys

import requests
from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.models import Base, Przepis
from database.session import Session, engine

DEFAULT_URL = "https://aniagotuje.pl/przepis/chleb-na-zakwasie"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; recipeScraper/1.0)"}
TIMEOUT = 15  # sekundy

# Czas w formacie ISO 8601, np. "PT45M", "PT1H30M", "P1DT2H"
DURATION_RE = re.compile(
    r"P(?:(?P<days>\d+)D)?"
    r"(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+(?:\.\d+)?)S)?)?"
)


def parse_duration(value):
    """Zamienia czas ISO 8601 (np. "PT1H30M") albo samą liczbę minut na liczbę minut."""
    value = (value or "").strip().upper()
    if value.isdigit():
        return int(value)

    match = DURATION_RE.fullmatch(value)
    if not match or value in ("P", "PT"):
        return None

    parts = {k: float(v) for k, v in match.groupdict(default="0").items()}
    return int(parts["days"] * 24 * 60 + parts["hours"] * 60 + parts["minutes"] + parts["seconds"] / 60)


def text_of(element, separator=" "):
    return element.get_text(separator, strip=True) if element else None


def fetch_page(url):
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()  # Sprawdzenie statusu odpowiedzi
    return response.content


def parse_recipe(html, source_url):
    """Wyciąga dane przepisu z mikrodanych schema.org. Zwraca słownik albo None."""
    soup = BeautifulSoup(html, "html.parser")
    recipe = soup.find(attrs={"itemtype": re.compile(r"schema\.org/Recipe$")})
    if recipe is None:
        return None

    ingredients = recipe.find("ul", class_="recipe-ing-list")
    ingredient_list = []
    if ingredients:
        for li in ingredients.find_all("li"):
            item = text_of(li.span or li)
            if item:
                ingredient_list.append(item)

    prep_time = recipe.find("meta", itemprop="prepTime")
    image = recipe.find("meta", itemprop="image") or recipe.find("img", itemprop="image")

    return {
        "nazwa": text_of(recipe.find("h1", itemprop="name")),
        "czas_przygotowania": parse_duration(prep_time.get("content")) if prep_time else None,
        "zdjecie_url": (image.get("content") or image.get("src")) if image else None,
        "opis": text_of(recipe.find("div", class_="article-intro"), "\n"),
        "instrukcja": text_of(recipe.find("div", itemprop="recipeInstructions"), "\n"),
        "skladniki": ", ".join(ingredient_list),
        "zrodlo_url": source_url,
    }


def save_recipe(data):
    """Zapisuje przepis. Jeśli przepis z tego adresu już jest w bazie, aktualizuje go.

    Zwraca True, gdy dodano nowy przepis, i False przy aktualizacji.
    """
    with Session() as session, session.begin():
        przepis = session.scalars(
            select(Przepis).filter_by(zrodlo_url=data["zrodlo_url"])
        ).first()
        created = przepis is None
        if created:
            przepis = Przepis()
            session.add(przepis)
        for field, value in data.items():
            setattr(przepis, field, value)
    return created


def main(url=DEFAULT_URL):
    print(url)
    try:
        html = fetch_page(url)
    except requests.exceptions.RequestException as e:
        print("Błąd podczas pobierania strony:", e)
        return 1

    data = parse_recipe(html, url)
    if data is None:
        print("Nie znaleziono przepisu na stronie.")
        return 1
    if not data["nazwa"]:
        print("Nie znaleziono nazwy przepisu – pomijam zapis.")
        return 1

    try:
        # Tworzenie tabeli w bazie danych (jeśli nie istnieje)
        Base.metadata.create_all(engine)
        created = save_recipe(data)
    except SQLAlchemyError as e:
        print("Błąd podczas zapisu do bazy danych:", e)
        return 1

    print(f"Przepis '{data['nazwa']}' został {'dodany' if created else 'zaktualizowany'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
