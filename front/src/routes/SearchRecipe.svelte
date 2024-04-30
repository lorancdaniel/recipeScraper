<script>
  import { onMount } from "svelte";
  import axios from "axios";
  let keyword = "";
  async function scrapeRecipe() {
    try {
      const response = await axios.post(
        "http://83.150.236.193:8000/scrape",
        keyword,
        { headers: { "Content-Type": "application/json" } }
      );
      if (response.status === 200) {
        console.log("Przepis został dodany do bazy danych.");
      }
    } catch (error) {
      console.error("Błąd podczas scrapowania przepisu:", error);
    }
  }
</script>

<main class="container mx-auto px-4">
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
        class="w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-crimson-500 focus:shadow-crimson"
        placeholder="np. sernik"
      />
    </div>
    <button
      on:click|preventDefault={scrapeRecipe}
      class="w-full px-4 py-2 font-bold text-white bg-red-500 rounded-full hover:bg-crimson-600 focus:outline-none focus:shadow-outline active:scale-98 transition duration-300 ease"
    >
      Scrapuj przepis
    </button>
  </form>
</main>

<style>
  .focus\:shadow-crimson:focus {
    box-shadow: 0 0 5px rgba(220, 20, 60, 0.5);
  }
</style>
