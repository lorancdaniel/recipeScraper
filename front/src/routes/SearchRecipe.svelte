<script>
  import { onMount } from "svelte";
  import axios from "axios";

  let keyword = "";

  async function scrapeRecipe() {
    try {
      const response = await axios.post(
        "http://83.150.236.193:8000/scrape",
        keyword,
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      if (response.status === 200) {
        console.log("Przepis został dodany do bazy danych.");
      }
    } catch (error) {
      console.error("Błąd podczas scrapowania przepisu:", error);
    }
  }
</script>

<main>
  <h1>Scrapowanie przepisów z Google</h1>
  <form>
    <label for="keyword">Wpisz słowo kluczowe:</label>
    <input type="text" id="keyword" bind:value={keyword} />
    <button on:click={scrapeRecipe}>Scrapuj przepis</button>
  </form>
</main>

<style>
  :root {
    --primary-color: #ff6b6b;
    --secondary-color: #4ecdc4;
    --text-color: #333;
    --background-color: #f7fff7;
  }

  body {
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
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

  nav {
    background-color: var(--primary-color);
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  nav a {
    color: white;
    text-decoration: none;
    margin-right: 20px;
  }

  nav a:hover {
    color: #ccc;
  }
</style>
