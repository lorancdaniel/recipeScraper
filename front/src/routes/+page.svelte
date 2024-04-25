<style>
  :root {
    --primary-color: #ff6b6b;
    --secondary-color: #4ecdc4;
    --text-color: #333;
    --background-color: #f7fff7;
  }

  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--background-color);
    color: var(--text-color);
    margin: 0;
    padding: 0;
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

  h2 {
    color: var(--secondary-color);
    margin-top: 40px;
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

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
  }

  li h3 {
    margin-top: 0;
    color: var(--primary-color);
  }

  li img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    margin-bottom: 10px;
  }

  li p {
    margin-bottom: 10px;
  }

  li a {
    color: var(--secondary-color);
    text-decoration: none;
  }
</style>

<script>
  import { onMount } from 'svelte';
  import axios from 'axios';

  let recipes = [];
  let newRecipe = {
    nazwa: '',
    czas_przygotowania: null,
    zdjecie_url: '',
    opis: '',
    instrukcja: '',
    skladniki: '',
    zrodlo_url: ''
  };

  onMount(async () => {
    try {
      const response = await axios.get('http://83.150.236.193:8000/recipes');
      recipes = response.data;
      console.log(recipes);
    } catch (error) {
      console.error('Błąd podczas pobierania przepisów:', error);
    }
  });

  async function addRecipe() {
    try {
      const response = await axios.post('http://83.150.236.193:8000/recipes', newRecipe);
      if (response.status === 200) {
        recipes = [...recipes, newRecipe];
        newRecipe = {
          nazwa: '',
          czas_przygotowania: null,
          zdjecie_url: '',
          opis: '',
          instrukcja: '',
          skladniki: '',
          zrodlo_url: ''
        };
      }
    } catch (error) {
      console.error('Błąd podczas dodawania przepisu:', error);
    }
  }
</script>

<main>
  <h1>Przepisy</h1>

  <h2>Dodaj nowy przepis</h2>
  <form on:submit|preventDefault={addRecipe}>
    <label>
      Nazwa:
      <input type="text" bind:value={newRecipe.nazwa} required>
    </label>
    <label>
      Czas przygotowania (minuty):
      <input type="number" bind:value={newRecipe.czas_przygotowania}>
    </label>
    <label>
      URL zdjęcia:
      <input type="text" bind:value={newRecipe.zdjecie_url}>
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
      <input type="text" bind:value={newRecipe.zrodlo_url}>
    </label>
    <button type="submit">Dodaj przepis</button>
  </form>

  <h2>Lista przepisów</h2>
  <ul>
    {#each recipes as recipe}
      <li>
        <h3>{recipe[1]}</h3>
        <p>Czas przygotowania: {recipe[2]} minut</p>
        <img src={recipe[3]} alt={recipe[1]}>
        <p>{recipe[4]}</p>
        <p>Instrukcja: {recipe[5]}</p>
        <p>Składniki: {recipe[6]}</p>
        <a href={recipe[7]} target="_blank">Źródło</a>
      </li>
    {/each}
  </ul>
</main>