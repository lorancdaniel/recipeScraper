<script>
  import { onMount } from "svelte";
  import SearchRecipes from "./SearchRecipe.svelte";
  import Recipes from "./Recipes.svelte";
  import AddRecipe from "./AddRecipe.svelte";

  let currentView = "SearchRecipes";

  function changeView(view) {
    currentView = view;
  }
</script>

<main class="container mx-auto px-4">
  <nav
    class="bg-gradient-to-r from-red-500 to-pink-500 text-white shadow-lg rounded-lg"
  >
    <ul class="flex justify-center space-x-8 py-6">
      <li>
        <a
          href="#"
          class="text-lg font-semibold hover:text-white transition duration-300 ease-in-out rounded-lg px-4 py-2 hover:bg-red-600"
          on:click|preventDefault={() => changeView("SearchRecipes")}
        >
          Search Recipes
        </a>
      </li>
      <li>
        <a
          href="#"
          class="text-lg font-semibold hover:text-white transition duration-300 ease-in-out rounded-lg px-4 py-2 hover:bg-red-600"
          on:click|preventDefault={() => changeView("Recipes")}
        >
          Recipes
        </a>
      </li>
      <li>
        <a
          href="#"
          class="text-lg font-semibold hover:text-white transition duration-300 ease-in-out rounded-lg px-4 py-2 hover:bg-red-600"
          on:click|preventDefault={() => changeView("AddRecipe")}
        >
          Add Recipe
        </a>
      </li>
    </ul>
  </nav>

  <div class="mt-12">
    {#key currentView}
      {#if currentView === "SearchRecipes"}
        <div
          class="bg-white rounded-lg shadow-md p-8 hover:shadow-lg transition duration-300 ease-in-out"
        >
          <SearchRecipes />
        </div>
      {:else if currentView === "Recipes"}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Recipes />
        </div>
      {:else if currentView === "AddRecipe"}
        <div
          class="bg-white rounded-lg shadow-md p-8 hover:shadow-lg transition duration-300 ease-in-out"
        >
          <AddRecipe />
        </div>
      {/if}
    {/key}
  </div>
</main>
