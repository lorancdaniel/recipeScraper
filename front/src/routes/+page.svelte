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

<main>
  <nav>
    <ul>
      <li>
        <a href="#" on:click|preventDefault={() => changeView("SearchRecipes")}
          >Search Recipes</a
        >
      </li>
      <li>
        <a href="#" on:click|preventDefault={() => changeView("Recipes")}
          >Recipes</a
        >
      </li>
      <li>
        <a href="#" on:click|preventDefault={() => changeView("AddRecipe")}
          >Add Recipe</a
        >
      </li>
    </ul>
  </nav>

  {#key currentView}
    {#if currentView === "SearchRecipes"}
      <SearchRecipes />
    {:else if currentView === "Recipes"}
      <Recipes />
    {:else if currentView === "AddRecipe"}
      <AddRecipe />
    {/if}
  {/key}
</main>

<style>
  nav {
    background-color: #f2f2f2;
    padding: 10px;
  }

  nav ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
  }

  nav ul li {
    display: inline;
    margin-right: 10px;
  }

  nav ul li a {
    text-decoration: none;
    color: #333;
    padding: 5px;
  }

  nav ul li a:hover {
    background-color: #ddd;
  }
</style>
