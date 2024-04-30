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

<main>
  <h1>Dodaj nowy przepis</h1>

  <form on:submit|preventDefault={addRecipe}>
    <label>
      Nazwa:
      <input type="text" bind:value={newRecipe.nazwa} required />
    </label>

    <label>
      Czas przygotowania (minuty):
      <input type="number" bind:value={newRecipe.czas_przygotowania} />
    </label>

    <label>
      URL zdjęcia:
      <input type="text" bind:value={newRecipe.zdjecie_url} />
    </label>

    <label>
      Opis:
      <textarea bind:value={newRecipe.opis}></textarea>
    </label>

    <label>
      Instrukcja:
      <textarea bind:value={newRecipe.instrukcja}></textarea>
    </label>

    <label>
      Składniki:
      <textarea bind:value={newRecipe.skladniki}></textarea>
    </label>

    <label>
      URL źródła:
      <input type="text" bind:value={newRecipe.zrodlo_url} />
    </label>

    <button type="submit">Dodaj przepis</button>
  </form>
</main>

<style>
  :root {
    --primary-color: #ff6b6b;
    --secondary-color: #4ecdc4;
    --text-color: #333;
    --background-color: #f7fff7;
  }

  main {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }

  h1 {
    color: var(--primary-color);
    text-align: center;
  }

  form {
    display: grid;
    gap: 10px;
  }

  label {
    display: block;
    font-weight: bold;
  }

  input,
  textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #ff4f4f;
  }
</style>
