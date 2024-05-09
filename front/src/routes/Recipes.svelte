<script>
  import { onMount } from "svelte";
  import axios from "axios";

  let recipes = [];
  let searchTerm = "";
  let selectedRecipe = null;
  let selectedLetter = "";
  let showFullImageModal = false;

  onMount(fetchRecipes);

  async function fetchRecipes() {
    try {
      const response = await axios.get("http://83.150.236.193:8000/recipes");
      recipes = response.data;
    } catch (error) {
      console.error("Błąd podczas pobierania przepisów:", error);
    }
  }

  function toggleFullImageModal() {
    showFullImageModal = !showFullImageModal;
  }

  async function deleteRecipe(recipeId) {
    try {
      await axios.delete(`http://83.150.236.193:8000/recipes/${recipeId}`);
      await fetchRecipes();
      selectedRecipe = null;
    } catch (error) {
      console.error("Błąd podczas usuwania przepisu:", error);
    }
  }

  $: filteredRecipes = recipes.filter((recipe) => {
    const recipeName = recipe[1].toLowerCase();
    const searchTermLower = searchTerm.toLowerCase();
    const selectedLetterLower = selectedLetter.toLowerCase();

    return (
      recipeName.includes(searchTermLower) &&
      (selectedLetterLower === "" || recipeName.startsWith(selectedLetterLower))
    );
  });
  $: recipesWithIngredients = filteredRecipes.map((recipe) => {
    let ingredients = recipe[6].slice(1, -1).split('","');
    ingredients = ingredients.map((ingredient) => ingredient.replace(/"/g, ""));
    return { ...recipe, ingredients };
  });

  function openModal(recipe) {
    selectedRecipe = recipe;
  }

  function selectLetter(letter) {
    selectedLetter = letter;
  }
</script>

<main class="container mx-auto px-4 py-8">
  <h1 class="text-4xl font-bold text-center text-pink-600 mb-8">Przepisy</h1>
  <input
    type="text"
    bind:value={searchTerm}
    placeholder="Wyszukaj przepis..."
    class="w-full px-4 py-2 mb-8 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400"
  />
  <div class="flex flex-wrap justify-center mb-8">
    {#each "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("") as letter}
      <button
        class="mx-1 px-1 py-1 bg-pink-200 text-pink-800 rounded-full hover:bg-pink-300 focus:outline-none focus:ring-2 focus:ring-pink-400 transition-colors duration-300 sm:mx-1 sm:px-3 sm:py-2"
        on:click={() => selectLetter(letter)}
      >
        {letter}
      </button>
    {/each}
    <button
      class=" bg-gray-200 text-gray-800 rounded-full hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400 transition-colors duration-300 sm:ml-6 sm:px-3 sm:py-2"
      on:click={() => selectLetter("")}
    >
      Wszystkie
    </button>
  </div>
  <ul
    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8"
  >
    {#each recipesWithIngredients as recipe (recipe[0])}
      <button
        class="bg-white rounded-lg shadow-md overflow-hidden relative hover:shadow-lg hover:scale-105 transition-all duration-300"
        on:click={() => openModal(recipe)}
      >
        <div class="relative">
          {#if recipe[3]}
            <img
              src={recipe[3]}
              alt={recipe[1]}
              class="w-full h-48 object-cover"
            />
          {:else}
            <div
              class="w-full h-48 bg-gray-200 flex items-center justify-center"
            >
              <span class="text-gray-500 text-sm">Brak zdjęcia</span>
            </div>
          {/if}
          <button
            class="absolute top-2 right-2 text-white bg-pink-500 rounded-full p-2 hover:bg-pink-600 focus:outline-none focus:ring-2 focus:ring-pink-400 transition-colors duration-300"
            on:click|stopPropagation={() => openModal(recipe)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M6.672 1.911a1 1 0 10-1.932.518l.259.966a1 1 0 001.932-.518l-.26-.966zM2.429 4.74a1 1 0 10-.517 1.932l.966.259a1 1 0 00.517-1.932l-.966-.26zm8.814-.569a1 1 0 00-1.415-1.414l-.707.707a1 1 0 101.415 1.415l.707-.708zm-7.071 7.072l.707-.707A1 1 0 003.465 9.12l-.708.707a1 1 0 001.415 1.415zm3.2-5.171a1 1 0 00-1.3 1.3l4 10a1 1 0 001.823.075l1.38-2.759 3.018 3.02a1 1 0 001.414-1.415l-3.019-3.02 2.76-1.379a1 1 0 00-.076-1.822l-10-4z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
          <button
            class="absolute top-2 left-2 text-white bg-red-500 rounded-full p-2 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 transition-colors duration-300"
            on:click|stopPropagation={() => deleteRecipe(recipe[0])}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
        <div class="p-4">
          <h3 class="text-lg font-semibold text-pink-600 mb-2">{recipe[1]}</h3>
          <p class="text-gray-500 text-sm mb-2">
            Czas przygotowania: {recipe[2]} minut
          </p>
          <p class="text-gray-700 text-sm line-clamp-3">
            {recipe[4]}
          </p>
        </div>
      </button>
    {/each}
  </ul>
  {#if selectedRecipe}
    <div class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen">
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          on:click={() => (selectedRecipe = null)}
        ></div>
        <div
          class="bg-white rounded-xl p-8 mx-auto shadow-3xl relative max-w-4xl modal-content overflow-y-auto"
          style="max-height: 90vh;"
        >
          <button
            class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 focus:outline-none transition-colors duration-300"
            on:click={() => (selectedRecipe = null)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
          <h3 class="text-2xl font-semibold text-pink-600 mb-4 text-center">
            {selectedRecipe[1]}
          </h3>
          <p class="text-gray-500 mb-2 text-center text-sm">
            Czas przygotowania: {selectedRecipe[2]} minut
          </p>
          {#if selectedRecipe[3]}
            <img
              src={selectedRecipe[3]}
              alt={selectedRecipe[1]}
              class="w-full h-64 object-cover rounded-md mb-4 mx-auto"
              on:click={toggleFullImageModal}
            />
          {/if}
          <p
            class="text-base text-slate-600 mb-6 text-center max-w-md mx-auto leading-relaxed italic"
          >
            {selectedRecipe[4]}
          </p>
          <p class="text-sm text-gray-700 mb-4 leading-relaxed">
            {selectedRecipe[5]}
          </p>
          <p class="text-gray-800 mb-2 text-center font-semibold text-sm">
            Składniki:
          </p>
          <ul
            class="list-disc list-inside text-sm text-gray-700 space-y-2 mb-4 mx-auto max-w-md"
          >
            {#each selectedRecipe.ingredients as ingredient}
              <li>{ingredient}</li>
            {/each}
          </ul>
          <div class="flex items-center justify-center">
            <button
              on:click={() => deleteRecipe(selectedRecipe[0])}
              class="px-4 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-full hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-400 transition-colors duration-300"
            >
              Usuń przepis
            </button>
          </div>
          {#if selectedRecipe[7]}
            <div class="text-xs text-center mt-2 text-gray-400">
              Źródło: <a href={selectedRecipe[7]}>{selectedRecipe[7]}</a>
            </div>
          {/if}
        </div>
      </div>
    </div>
  {/if}
  {#if showFullImageModal}
    <div class="fixed z-20 inset-0 flex items-center justify-center">
      <div
        class="fixed inset-0 bg-black bg-opacity-75 transition-opacity"
        on:click={toggleFullImageModal}
      ></div>
      <div class="relative">
        <img
          src={selectedRecipe[3]}
          alt={selectedRecipe[1]}
          class="max-h-[80vh] max-w-[80vw] object-contain"
        />
        <button
          class="absolute top-2 right-2 text-white hover:text-gray-300 focus:outline-none transition-colors duration-300"
          on:click={toggleFullImageModal}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
  {/if}
</main>

<style>
  .modal-content {
    scrollbar-width: thin; /* Szerokość scrollbara dla przeglądarek innych niż WebKit */
    scrollbar-color: #d1d1d1 #f1f1f1; /* Kolor kciuka i tła scrollbara dla przeglądarek innych niż WebKit */
  }

  .modal-content::-webkit-scrollbar {
    width: 8px; /* Szerokość scrollbara dla przeglądarek WebKit */
  }

  .modal-content::-webkit-scrollbar-track {
    background-color: #f1f1f1; /* Kolor tła paska scrollbara dla przeglądarek WebKit */
  }

  .modal-content::-webkit-scrollbar-thumb {
    background-color: #d1d1d1; /* Kolor kciuka scrollbara dla przeglądarek WebKit */
    border-radius: 4px; /* Zaokrąglenie kciuka scrollbara dla przeglądarek WebKit */
  }

  .modal-content::-webkit-scrollbar-thumb:hover {
    background-color: #a8a8a8; /* Kolor kciuka scrollbara przy najechaniu kursorem dla przeglądarek WebKit */
  }
</style>
