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
</script>

<main class="max-w-4xl mx-auto p-4">
  <h1 class="text-4xl font-bold text-center text-pink-600 mb-8">Przepisy</h1>

  <input
    type="text"
    bind:value={searchTerm}
    placeholder="Wyszukaj przepis..."
    class="w-full px-4 py-2 mb-8 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400"
  />

  <ul class="space-y-8">
    {#each filteredRecipes as recipe}
      <li class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-2xl font-semibold text-pink-600 mb-4">{recipe[1]}</h3>
        <p class="text-gray-600 mb-2">Czas przygotowania: {recipe[2]} minut</p>
        <img
          src={recipe[3]}
          alt={recipe[1]}
          class="w-full h-auto rounded-md mb-4"
        />
        <p class="text-gray-800 mb-2">{recipe[4]}</p>
        <p class="text-gray-800 mb-2">Instrukcja: {recipe[5]}</p>
        <p class="text-gray-800 mb-2">Składniki: {recipe[6]}</p>
        <a
          href={recipe[7]}
          target="_blank"
          class="text-teal-500 hover:underline">Źródło</a
        >
        <button
          on:click={() => deleteRecipe(recipe[0])}
          class="mt-4 px-4 py-2 bg-pink-600 text-white rounded-md hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-400"
        >
          Usuń przepis
        </button>
      </li>
    {/each}
  </ul>
</main>
