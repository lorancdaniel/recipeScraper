from fastapi import FastAPI, HTTPException, Body
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pydantic import BaseModel, validator
import uvicorn
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from gpt_formatting import recipeGenerator, is_recipe
import json
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

app = FastAPI()

# Konfiguracja CORS
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dane do połączenia z bazą danych
username = "recipe"
password = "8513"
host = "83.150.236.193"
db_name = "recipeDatabase"

# Model danych dla przepisu
class Recipe(BaseModel):
    nazwa: str
    czas_przygotowania: int | None = None
    zdjecie_url: str | None = None
    opis: str | None = None
    instrukcja: str | None = None
    skladniki: str | None = None
    zrodlo_url: str | None = None

    @validator('nazwa', 'instrukcja', 'opis', 'skladniki')
    def validate_not_empty(cls, value):
        if not value:
            raise ValueError('Pole nie może być puste')
        return value

# Funkcja pomocnicza do nawiązywania połączenia z bazą danych
def get_db_connection():
    print("🛸 lacze z baza")
    try:
        conn = psycopg2.connect(dbname=db_name, user=username, password=password, host=host)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

#endpoint do dodawania przepisów z formularza na stronie
@app.post("/recipes")
def add_recipe(recipe: Recipe):
    print("🛸 dodaje nowy przepis")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = sql.SQL("INSERT INTO przepisy (nazwa, czas_przygotowania, zdjecie_url, opis, instrukcja, skladniki, zrodlo_url) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        values = (recipe.nazwa, recipe.czas_przygotowania, recipe.zdjecie_url, recipe.opis, recipe.instrukcja, recipe.skladniki, recipe.zrodlo_url)
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Przepis został dodany"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint do pobierania wszystkich przepisów
@app.get("/recipes")
def get_recipes():
    print("🛸 pobieram przepisy")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM przepisy")
        recipes = cur.fetchall()
        cur.close()
        conn.close()
        return recipes
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint do pobierania pojedynczego przepisu
@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
    print(f"🛸 pobieram przepis: {recipe_id}")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM przepisy WHERE id = %s", (recipe_id,))
        recipe = cur.fetchone()
        cur.close()
        conn.close()
        if recipe:
            return recipe
        else:
            raise HTTPException(status_code=404, detail="Przepis nie został znaleziony")
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape")
async def scrape_recipe(keyword: str = Body(...)):
    print(f" Rozpoczynam scrapowanie przepisu: {keyword}")
    try:
        # Wyszukiwanie wyników w Google na podstawie słowa kluczowego
        query = keyword.replace(" ", "+")
        url = f"https://www.google.pl/search?q={query}&num=10"

        # Konfiguracja opcji Chrome
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")

        # Inicjalizacja przeglądarki Chrome
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        search_results = driver.find_elements(By.CSS_SELECTOR, ".yuRUbf a")

        if not search_results:
            driver.quit()
            raise HTTPException(status_code=404, detail="Nie znaleziono wyników wyszukiwania dla podanego słowa kluczowego")

        result_url = None
        for result in search_results:
            result_url = result.get_attribute("href")
            if all(x not in result_url for x in ["facebook.com", "instagram.com", "youtube.com", "x.com"]):
                # Scrapowanie treści strony
                response = requests.get(result_url)
                soup = BeautifulSoup(response.content, "html.parser")
                body_content = soup.find("body").get_text()

                # Sprawdzenie, czy tekst jest przepisem kulinarnym
                if not await is_recipe(keyword):
                    raise HTTPException(status_code=400, detail="Podany tekst nie jest przepisem kulinarnym. Proszę zmienić tekst lub jego format.")

                # Formatowanie przepisu
                formattedRecipe = await recipeGenerator(body_content)
                formattedRecipe = json.loads(formattedRecipe)

                # Dodanie zrodlo_url do formattedRecipe
                formattedRecipe['zrodlo_url'] = result_url

                # Sprawdzenie, czy wymagane pola nie są puste
                if not all(formattedRecipe.get(field) for field in ['nazwa', 'czas_przygotowania', 'opis', 'skladniki', 'instrukcja']):
                    continue

                break

        if result_url is None:
            driver.quit()
            raise HTTPException(status_code=404, detail="Nie znaleziono przepisu dla podanego słowa kluczowego")

        driver.quit()

        # Połączenie z bazą danych
        engine = create_engine(f'postgresql://{username}:{password}@{host}/{db_name}')
        Session = sessionmaker(bind=engine)
        Base = declarative_base()

        # Define the Przepis model with the correct column types
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

        # Dodawanie nowego przepisu do bazy danych
        session = Session()
        try:
            new_recipe = Przepis(**formattedRecipe)
            session.add(new_recipe)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Błąd podczas dodawania przepisu: {e}")
            raise HTTPException(status_code=500, detail="Błąd podczas dodawania przepisu do bazy danych")
        finally:
            session.close()

        return {"message": "Przepis został dodany do bazy danych."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    print(f"🛸 usuwam przepis: {recipe_id}")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM przepisy WHERE id = %s", (recipe_id,))
        deleted_rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        if deleted_rows > 0:
            return {"message": "Przepis został usunięty"}
        else:
            raise HTTPException(status_code=404, detail="Przepis nie został znaleziony")
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)