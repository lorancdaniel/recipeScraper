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

<main class="container mx-auto p-4 min-h-screen flex flex-col">
  <nav
    class="bg-gradient-to-r from-red-500 to-pink-500 text-white shadow-lg rounded-lg fixed top-2 left-4 right-4 z-10 sm:left-8 sm:right-8 md:left-12 md:right-12 lg:left-20 lg:right-20 xl:left-40 xl:right-40"
  >
    <ul
      class="flex flex-wrap justify-center space-x-2 sm:space-x-4 py-2 sm:py-4"
    >
      {#each views as view}
        <li class="mb-2 sm:mb-0">
          <a
            href="#"
            class="text-sm sm:text-base md:text-lg lg:text-xl xl:text-2xl font-semibold hover:text-white transition duration-300 ease-in-out rounded-lg px-2 sm:px-4 py-1 sm:py-2 hover:bg-red-600"
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
          class="bg-white rounded-lg shadow-md p-8 hover:shadow-lg transition duration-300 ease-in-out
                 lg:p-12 xl:p-16"
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
