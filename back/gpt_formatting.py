import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("API"))

async def recipeGenerator(recipe):
    print("👽 wysylam przepis do sformatowania przez gpt")
    try:
        messages = [
            {
                "role": "user",
                "content": f"Na podstawie poniższego tekstu dotyczącego przepisu, proszę przygotować dane i zwrócić tylko i wyłącznie w formacie JSON tylko i wyłącznie z poniższą strukturą:\n\n```json\n{{\n  \"nazwa\": \"\",\n  \"czas_przygotowania\": 0,\n  \"zdjecie_url\": \"\",\n  \"opis\": \"\",\n  \"instrukcja\": \"\",\n  \"skladniki\": [],\n  \"zrodlo_url\":\"\n}}\n```\n\nInstrukcje:\n\n1. Wyodrębnij nazwę przepisu z tekstu i wpisz ją w polu \"nazwa\". Jeśli nazwa nie jest podana, pozostaw to pole puste.\n\n2. Jeśli czas przygotowania jest podany w tekście, wpisz go w minutach w polu \"czas_przygotowania\". W przeciwnym razie pozostaw 0.\n\n3. Jeśli w tekście znajduje się adres URL zdjęcia przepisu, wpisz go w polu \"zdjecie_url\". W przeciwnym razie pozostaw puste pole.\n\n4. Wyodrębnij opis przepisu z tekstu i wpisz go w polu \"opis\". Jeśli opis nie jest podany, pozostaw to pole puste.\n\n5. Wyodrębnij instrukcję przygotowania z tekstu i wpisz ją w polu \"instrukcja\". Jeśli instrukcja jest podzielona na kroki, połącz je w jeden ciągły tekst. Jeśli instrukcja nie jest podana, pozostaw to pole puste.\n\n6. Wyodrębnij listę składników z tekstu i wpisz je w polu \"skladniki\" jako tablicę. Jeśli składniki nie są podane, pozostaw pustą tablicę []. Składniki mają być podane w tablicy odzielone przecinkami np. [250g makaronu, 300g wody, 450g śmietanki]\n\n7. \nTekst przepisu:\n{recipe}\n\n Proszę zwrócić dane w formacie JSON zgodnie z powyższą strukturą, nie zmieniaj nazw wartości!!!. Wszystkie wartości typu string muszą być w  jednakowym podwójnym cudzysłowiu, a tablica składników musi być poprawnie sformatowana.\n\nTen prompt powinien pomóc w wyodrębnieniu wszystkich niezbędnych informacji z dowolnego tekstu zawierającego przepis i zwrócić je w ustrukturyzowanym formacie JSON, gotowym do zaimportowania do bazy danych. Pomiń ```json na początku i ``` na końcu. Nie dawaj podwójnych cudzysłowi koło siebie. Pamiętaj aby nie zmieniać podanych wartości i strukury JSONa. Tekst w kluczach ma być dobrze sfromatowany, poprawny stylistycznie i ortograficznie"
            }
        ]

        response = client.chat.completions.create(model="gpt-3.5-turbo-16k",
        messages=messages,
        temperature=0.4,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0)
        response_message = response.choices[0].message.content
        print(response_message)
        return response_message
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return []