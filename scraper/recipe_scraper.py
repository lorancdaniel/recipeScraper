import requests
from bs4 import BeautifulSoup
import Session from database

url = "https://www.example.com/recipes"
response = requests.get(url)


soup = BeautifulSoup(response.content, "html.parser")


recipes = soup.find_all("div", class_="recipe")
for recipe in recipes:
    title = recipe.find("h2").text
    print(title)

ingredients = recipe.find("ul", class_="ingredients")
ingredient_list = [li.text for li in ingredients.find_all("li")]
print(ingredient_list)
