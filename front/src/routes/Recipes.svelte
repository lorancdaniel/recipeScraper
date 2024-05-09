<script>
  import { onMount } from "svelte";
  import axios from "axios";

  let recipes = [];
  let searchTerm = "";

  onMount(fetchRecipes);

  async function fetchRecipes() {
    try {
      const response = await axios.get("http://83.150.236.193:8000/recipes");
      recipes = response.data;
    } catch (error) {
      console.error("Błąd podczas pobierania przepisów:", error);
    }
  }

  async function deleteRecipe(recipeId) {
    try {
      await axios.delete(`http://83.150.236.193:8000/recipes/${recipeId}`);
      await fetchRecipes();
    } catch (error) {
      console.error("Błąd podczas usuwania przepisu:", error);
    }
  }

  $: filteredRecipes = recipes.filter((recipe) =>
    recipe[1].toLowerCase().includes(searchTerm.toLowerCase())
  );

  $: recipesWithIngredients = filteredRecipes.map((recipe) => {
    let ingredients = recipe[6].slice(1, -1).split('","');
    ingredients = ingredients.map((ingredient) => ingredient.replace(/"/g, ""));
    return { ...recipe, ingredients };
  });
</script>

<main class="container mx-auto px-4">
  <h1
    class="text-4xl font-bold text-center text-pink-600 mb-8 max-w-md mx-auto"
  >
    Przepisy
  </h1>

  <input
    type="text"
    bind:value={searchTerm}
    placeholder="Wyszukaj przepis..."
    class="w-full px-4 py-2 mb-8 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400"
  />

  <ul class="space-y-16">
    {#each recipesWithIngredients as recipe}
      <li class="bg-white rounded-lg p-6 mx-auto shadow-3xl">
        <h3 class="text-4xl font-semibold text-pink-600 mb-4 text-center">
          {recipe[1]}
        </h3>
        <p class="text-gray-500 mb-2 text-center">
          Czas przygotowania: {recipe[2]} minut
        </p>
        {#if recipe[3]}
          <img
            src={recipe[3]}
            alt={recipe[1]}
            class="w-full h-auto rounded-md mb-4 mx-auto"
          />
        {/if}
        <p
          class="text-sm text-slate-600 mb-6 text-center max-w-md mx-auto leading-relaxed italic"
        >
          {recipe[4]}
        </p>
        <p class="text-md text-gray-700 mb-4 leading-relaxed">{recipe[5]}</p>
        <p class="text-gray-800 mb-2 text-center">Składniki:</p>
        <ul class="list-disc list-inside text-sm text-gray-700 space-y-1 mb-4">
          {#each recipe.ingredients as ingredient}
            <li>{ingredient}</li>
          {/each}
        </ul>
        <div class="flex items-center justify-center">
          <button
            on:click={() => deleteRecipe(recipe[0])}
            class="px-4 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-md hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-400"
          >
            Usuń przepis
          </button>
        </div>
        {#if recipe[7]}
          <div class="text-xs text-center mt-2 text-gray-400">
            Źródło: <a href={recipe[7]}>{recipe[7]} </a>
          </div>
        {/if}
      </li>
    {/each}
  </ul>
</main>
