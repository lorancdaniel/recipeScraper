<script>
  import axios from "axios";

  let newRecipe = {
    nazwa: "",
    czas_przygotowania: null,
    zdjecie_url: "",
    opis: "",
    instrukcja: "",
    skladniki: "",
    zrodlo_url: "",
  };

  async function addRecipe() {
    try {
      const response = await axios.post(
        "http://83.150.236.193:8000/recipes",
        newRecipe
      );
      if (response.status === 200) {
        newRecipe = {
          nazwa: "",
          czas_przygotowania: null,
          zdjecie_url: "",
          opis: "",
          instrukcja: "",
          skladniki: "",
          zrodlo_url: "",
        };
        alert("Przepis został dodany!");
      }
    } catch (error) {
      console.error("Błąd podczas dodawania przepisu:", error);
      alert("Wystąpił błąd podczas dodawania przepisu.");
    }
  }
</script>

<main class="container mx-auto px-4">
  <h1 class="text-4xl font-bold mb-8 text-center">Dodaj nowy przepis</h1>

  <form class="space-y-6 max-w-md mx-auto" on:submit|preventDefault={addRecipe}>
    <div class="input-field">
      <label class="block text-lg font-medium mb-2">
        Nazwa:
        <input
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          type="text"
          bind:value={newRecipe.nazwa}
          required
        />
      </label>
    </div>

    <div class="input-field">
      <label class="block text-lg font-medium mb-2">
        Czas przygotowania (minuty):
        <input
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          type="number"
          bind:value={newRecipe.czas_przygotowania}
        />
      </label>
    </div>

    <div class="input-field">
      <label class="block text-lg font-medium mb-2">
        URL zdjęcia:
        <input
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          type="text"
          bind:value={newRecipe.zdjecie_url}
        />
      </label>
    </div>

    <div class="input-field">
      <label class="block text-lg font-medium mb-2">
        Opis:
        <textarea
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          bind:value={newRecipe.opis}
        ></textarea>
      </label>
    </div>

    <div class="input-field">
      <label class="block text-lg font-medium mb-2">
        Instrukcja:
        <textarea
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          bind:value={newRecipe.instrukcja}
        ></textarea>
      </label>
    </div>

    <div class="input-field">
      <label class="block text-lg font-medium mb-2">
        Składniki:
        <textarea
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          bind:value={newRecipe.skladniki}
        ></textarea>
      </label>
    </div>

    <div class="input-field">
      <label class="block text-lg font-medium mb-2">
        URL źródła:
        <input
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          type="text"
          bind:value={newRecipe.zrodlo_url}
        />
      </label>
    </div>

    <div class="text-center">
      <button
        class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700"
        type="submit">Dodaj przepis</button
      >
    </div>
  </form>
</main>

<style>
  .input-field {
    max-width: 100%;
  }
</style>
