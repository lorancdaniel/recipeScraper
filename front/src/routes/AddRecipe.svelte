<script>
  import axios from "axios";
  const initialRecipe = {
    nazwa: "",
    czas_przygotowania: null,
    zdjecie_url: "",
    opis: "",
    instrukcja: "",
    skladniki: "",
    zrodlo_url: "",
  };
  let newRecipe = { ...initialRecipe };
  let isValid = {
    nazwa: true,
    czas_przygotowania: true,
    zdjecie_url: true,
    opis: true,
    instrukcja: true,
    skladniki: true,
    zrodlo_url: true,
  };
  const textFieldPattern = "[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9\\s,.!?:;()-]+";
  const skladnikiPattern = "[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9\\s,]+";
  async function addRecipe() {
    if (validateForm()) {
      try {
        const recipeData = { ...newRecipe };
        recipeData.skladniki = formatIngredients(recipeData.skladniki);
        const response = await axios.post(
          "http://83.150.236.193:8000/recipes",
          recipeData
        );
        if (response.status === 200) {
          newRecipe = { ...initialRecipe };
          alert("Przepis został dodany!");
        }
      } catch (error) {
        console.error("Błąd podczas dodawania przepisu:", error);
        alert("Wystąpił błąd podczas dodawania przepisu.");
      }
    }
  }
  function formatIngredients(ingredients) {
    return JSON.stringify(
      ingredients.split(",").map((ingredient) => ingredient.trim())
    );
  }
  function validateForm() {
    isValid.nazwa = new RegExp(`^${textFieldPattern}$`).test(
      newRecipe.nazwa.trim()
    );
    isValid.czas_przygotowania =
      /^\d+$/.test(newRecipe.czas_przygotowania) &&
      newRecipe.czas_przygotowania > 0;
    isValid.zdjecie_url = isValidURL(newRecipe.zdjecie_url);
    isValid.opis = new RegExp(`^${textFieldPattern}$`).test(
      newRecipe.opis.trim()
    );
    isValid.instrukcja = new RegExp(`^${textFieldPattern}$`).test(
      newRecipe.instrukcja.trim()
    );
    isValid.skladniki = new RegExp(`^${skladnikiPattern}$`).test(
      newRecipe.skladniki.trim()
    );
    isValid.zrodlo_url = isValidURL(newRecipe.zrodlo_url);
    return Object.values(isValid).every((value) => value);
  }
  function isValidURL(url) {
    const urlPattern =
      /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    return urlPattern.test(url);
  }
</script>

<main class="container mx-auto p-4 py-8 overflow-y-auto">
  <h1 class="text-4xl font-bold mb-8 text-center text-pink-600">
    Dodaj nowy przepis
  </h1>
  <form
    class="max-w-2xl mx-auto space-y-6"
    on:submit|preventDefault={addRecipe}
  >
    {#each Object.entries(newRecipe) as [field, value], index (field)}
      <div class="input-field">
        <label class="block text-lg font-medium mb-2 text-gray-700">
          {field === "czas_przygotowania"
            ? "Czas przygotowania (minuty)"
            : field.charAt(0).toUpperCase() + field.slice(1)}: {#if field === "opis" || field === "instrukcja" || field === "skladniki"}
            <textarea
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400 transition duration-300"
              bind:value={newRecipe[field]}
              required
              pattern={field === "skladniki"
                ? skladnikiPattern
                : textFieldPattern}
              rows="4"
            ></textarea>
          {:else}
            <input
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400 transition duration-300"
              inputmode={field === "czas_przygotowania" ? "number" : "text"}
              bind:value={newRecipe[field]}
              required={index !== 2 && index !== 6}
              min={field === "czas_przygotowania" ? 1 : undefined}
              pattern={field === "czas_przygotowania"
                ? "\\d+"
                : field !== "zdjecie_url" && field !== "zrodlo_url"
                  ? textFieldPattern
                  : undefined}
            />
          {/if}
          {#if !isValid[field]}
            <p class="text-red-500 text-sm mt-1">
              {field === "czas_przygotowania"
                ? "Czas przygotowania musi być liczbą większą od zera."
                : field === "zdjecie_url" || field === "zrodlo_url"
                  ? "Nieprawidłowy format URL."
                  : `${field.charAt(0).toUpperCase() + field.slice(1)} może zawierać litery alfabetu (w tym polskie znaki), spacje, numery oraz znaki interpunkcyjne.`}
            </p>
          {/if}
        </label>
      </div>
    {/each}
    <p class="text-sm text-gray-500 mb-4">
      Składniki muszą być oddzielone przecinkami.
    </p>
    <div class="text-center">
      <button
        class="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-6 py-3 rounded-md hover:bg-pink-700 transition duration-300"
        type="submit"
      >
        Dodaj przepis
      </button>
    </div>
  </form>
</main>
