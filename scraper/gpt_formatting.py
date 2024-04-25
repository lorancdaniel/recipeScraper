import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("API"))

async def recipeGenerator(recipe):
    print(f"formatowanie przepisu {recipe}")
    try:
        messages = [
            {
                "role": "user",
                "content": f"Oto propozycja promptu, który powinien zwrócić przepis w formacie JSON na podstawie dowolnego podanego tekstu: Na podstawie poniższego tekstu dotyczącego przepisu, proszę przygotować dane w formacie JSON zgodnie z poniższą strukturą:```json {{ \"nazwa\": \"\", \"czas_przygotowania\": 0, \"zdjecie_url\": \"\", \"opis\": \"\", \"instrukcja\": \"\", \"skladniki\": \"\", \"zrodlo_url\": \"\"}} Instrukcje:\n1. Wyodrębnij nazwę przepisu z tekstu i wpisz ją w polu \"nazwa\". 2. Jeśli czas przygotowania jest podany w tekście, wpisz go w minutach w polu \"czas_przygotowania\". W przeciwnym razie pozostaw 0. 3. Jeśli w tekście znajduje się adres URL zdjęcia przepisu, wpisz go w polu \"zdjecie_url\". W przeciwnym razie pozostaw puste pole. 4. Wyodrębnij opis przepisu z tekstu i wpisz go w polu \"opis\". 5. Wyodrębnij instrukcję przygotowania z tekstu i wpisz ją w polu \"instrukcja\". Jeśli instrukcja jest podzielona na kroki, połącz je w jeden ciągły tekst. 6. Wyodrębnij listę składników z tekstu i wpisz je w polu \"skladniki\" jako tablicę. 7. Jeśli w tekście znajduje się adres URL źródła przepisu, wpisz go w polu \"zrodlo_url\". W przeciwnym razie pozostaw puste pole. Tekst przepisu: {recipe} Proszę zwrócić dane w formacie JSON zgodnie z powyższą strukturą. Ten prompt powinien pomóc w wyodrębnieniu wszystkich niezbędnych informacji z dowolnego tekstu zawierającego przepis i zwrócić je w ustrukturyzowanym formacie JSON, gotowym do zaimportowania do bazy danych. Pamiętaj aby wszystkie wartości typu string były w podwójnym cudzysłowiu"
            }
        ]

        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0)

        response_message = response.choices[0].message.content
        return response_message
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return []