<script>
  import { onMount } from "svelte";
  import axios from "axios";
  let keyword = "";
  let isValid = true;
  let apiResponse = "";
  let isLoading = false;
  async function scrapeRecipe() {
    isLoading = true;
    try {
      const response = await axios.post(
        "http://83.150.236.193:8000/scrape",
        keyword,
        { headers: { "Content-Type": "application/json" } }
      );
      apiResponse =
        response.status === 200 ? "Przepis został dodany do bazy danych." : "";
    } catch (error) {
      console.error("Błąd podczas scrapowania przepisu:", error);
      const errorResponse = error.request.response.toString();
      const errorObject = JSON.parse(errorResponse);
      apiResponse = errorObject.detail;
    } finally {
      isLoading = false;
    }
  }
  function validateInput() {
    isValid = /^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s]+$/.test(keyword);
  }
</script>

<main class="container px-4 relative overflow-y-auto">
  {#if isLoading}
    <div
      class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50"
    >
      <div class="bg-white p-8 rounded-lg shadow-lg">
        <div class="flex items-center justify-center">
          <svg
            class="animate-spin -ml-1 mr-3 h-10 w-10 text-crimson-500"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <!-- ... -->
          </svg>
          <span class="text-2xl font-bold">Oczekiwanie...</span>
        </div>
      </div>
    </div>
  {/if}
  <h1 class="text-4xl font-bold mb-8 text-center">
    Scrapowanie przepisów z Google
  </h1>
  <form
    class="max-w-md mx-auto transition duration-300 ease-in-out transform hover:scale-102"
  >
    <div class="mb-4">
      <label for="keyword" class="block text-gray-700 font-bold mb-2"
        >Wpisz słowo kluczowe:</label
      >
      <input
        type="text"
        id="keyword"
        bind:value={keyword}
        on:input={validateInput}
        class="w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-crimson-500 focus:shadow-crimson"
        placeholder="np. sernik"
        required
        disabled={isLoading}
      />
      {#if !isValid}
        <p class="text-red-500 text-sm mt-1">
          Proszę wpisać tylko litery alfabetu i spacje.
        </p>
      {/if}
    </div>
    <button
      on:click|preventDefault={scrapeRecipe}
      class="w-full px-4 py-2 font-bold text-white bg-gradient-to-r from-red-500 to-pink-500 rounded-full hover:bg-crimson-600 focus:outline-none focus:shadow-outline active:scale-98 transition duration-300 ease"
      disabled={!isValid || isLoading}
    >
      {isLoading ? "Oczekiwanie..." : "Scrapuj przepis"}
    </button>
  </form>
  {#if apiResponse}
    <div class="max-w-md mx-auto mt-8">
      <p class="text-lg text-center">{apiResponse}</p>
    </div>
  {/if}
</main>

<style>
  .focus\:shadow-crimson:focus {
    box-shadow: 0 0 5px rgba(220, 20, 60, 0.5);
  }
</style>
