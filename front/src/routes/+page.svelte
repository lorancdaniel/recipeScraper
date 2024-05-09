<script>
  import { onMount } from "svelte";
  import SearchRecipes from "./SearchRecipe.svelte";
  import Recipes from "./Recipes.svelte";
  import AddRecipe from "./AddRecipe.svelte";
  let currentView = "SearchRecipes";
  function changeView(view) {
    currentView = view;
  }
  const views = [
    {
      name: "SearchRecipes",
      component: SearchRecipes,
      label: "Wyszukaj przepisy",
    },
    { name: "Recipes", component: Recipes, label: "Przepisy" },
    { name: "AddRecipe", component: AddRecipe, label: "Dodaj przepis" },
  ];
</script>

<main class="container mx-auto px-4 min-h-screen flex flex-col">
  <nav
    class="bg-gradient-to-r from-red-500 to-pink-500 text-white shadow-lg rounded-lg fixed top-2 left-20 right-20 z-10"
  >
    <ul class="flex justify-center space-x-8 py-6">
      {#each views as view}
        <li>
          <a
            href="#"
            class="text-lg font-semibold hover:text-white transition duration-300 ease-in-out rounded-lg px-4 py-2 hover:bg-red-600"
            on:click|preventDefault={() => changeView(view.name)}
          >
            {view.label}
          </a>
        </li>
      {/each}
    </ul>
  </nav>
  <div class="flex-grow overflow-y-auto">
    <div class="mt-32">
      {#key currentView}
        <div
          class="bg-white rounded-lg shadow-md p-8 hover:shadow-lg transition duration-300 ease-in-out"
        >
          {#each views as view}
            {#if currentView === view.name}
              <svelte:component this={view.component} />
            {/if}
          {/each}
        </div>
      {/key}
    </div>
  </div>
</main>
