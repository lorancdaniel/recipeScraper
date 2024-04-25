from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pydantic import BaseModel
import uvicorn

app = FastAPI()

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

# Funkcja pomocnicza do nawiązywania połączenia z bazą danych
def get_db_connection():
    conn = psycopg2.connect(dbname=db_name, user=username, password=password, host=host)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

# Endpoint do pobierania wszystkich przepisów
@app.get("/recipes")
def get_recipes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM przepisy")
    recipes = cur.fetchall()
    cur.close()
    conn.close()
    return recipes

# Endpoint do pobierania pojedynczego przepisu
@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
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

# Endpoint do dodawania nowego przepisu
@app.post("/recipes")
def create_recipe(recipe: Recipe):
    conn = get_db_connection()
    cur = conn.cursor()
    query = sql.SQL("INSERT INTO przepisy (nazwa, czas_przygotowania, zdjecie_url, opis, instrukcja, skladniki, zrodlo_url) VALUES (%s, %s, %s, %s, %s, %s, %s)").format(
        sql.Literal(recipe.nazwa),
        sql.Literal(recipe.czas_przygotowania),
        sql.Literal(recipe.zdjecie_url),
        sql.Literal(recipe.opis),
        sql.Literal(recipe.instrukcja),
        sql.Literal(recipe.skladniki),
        sql.Literal(recipe.zrodlo_url)
    )
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Przepis został dodany"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)