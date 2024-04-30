<script>
  import { onMount } from "svelte";
  import axios from "axios";

  let recipes = [];
  let searchTerm = "";

  onMount(async () => {
    try {
      const response = await axios.get("http://83.150.236.193:8000/recipes");
      recipes = response.data;
      console.log(recipes);
    } catch (error) {
      console.error("Błąd podczas pobierania przepisów:", error);
    }
  });

  $: filteredRecipes = recipes.filter((recipe) =>
    recipe[1].toLowerCase().includes(searchTerm.toLowerCase())
  );

  let deleteRecipe = async (recipeId) => {
    try {
      await axios.delete(`http://83.150.236.193:8000/recipes/${recipeId}`);
      // Po usunięciu przepisu, odśwież listę przepisów
      const response = await axios.get("http://83.150.236.193:8000/recipes");
      recipes = response.data;
    } catch (error) {
      console.error("Błąd podczas usuwania przepisu:", error);
    }
  };
</script>

<main>
  <h1>Przepisy</h1>

  <input
    type="text"
    bind:value={searchTerm}
    placeholder="Wyszukaj przepis..."
  />

  <ul>
    {#each filteredRecipes as recipe}
      <li>
        <h3>{recipe[1]}</h3>
        <p>Czas przygotowania: {recipe[2]} minut</p>
        <img src={recipe[3]} alt={recipe[1]} />
        <p>{recipe[4]}</p>
        <p>Instrukcja: {recipe[5]}</p>
        <p>Składniki: {recipe[6]}</p>
        <a href={recipe[7]} target="_blank">Źródło</a>
        <button on:click={() => deleteRecipe(recipe[0])}>Usuń przepis</button>
      </li>
    {/each}
  </ul>
</main>

<style>
  :root {
    --primary-color: #ff6b6b;
    --secondary-color: #4ecdc4;
    --text-color: #333;
    --background-color: #f7fff7;
  }

  main {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }

  h1 {
    color: var(--primary-color);
    text-align: center;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
  }

  li h3 {
    margin-top: 0;
    color: var(--primary-color);
  }

  li img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    margin-bottom: 10px;
  }

  li p {
    margin-bottom: 10px;
  }

  li a {
    color: var(--secondary-color);
    text-decoration: none;
  }
  input {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
</style>
