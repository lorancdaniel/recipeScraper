
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("APIPPL"), base_url="https://api.perplexity.ai")

async def is_recipe(text):
    print("👽 Sprawdzam, czy tekst jest przepisem kulinarnym...")
    try:
        messages = [
            {
                "role": "system",
                "content": "Jesteś asystentem AI, który ocenia, czy dany tekst jest przepisem kulinarnym."
            },
            {
                "role": "user",
                "content": f"Przeanalizuj poniższy tekst i sprawdź w polskim internecie, czy jest istnieje taki przepis kulinarny. Odpowiedz słowem 'True', jeśli tekst jest przepisem kularnym, lub słowem 'False', jeśli tekst nie jest przepisem. Nie podawaj żadnych dodatkowych wyjaśnień ani informacji, odpowiedz tylko wartością logiczną True albo False. Sprawdzaj teskt tylko na polskojęzycznych stronach internetowych lub danych.\n\nTekst: {text}"
            }
        ]

        response = client.chat.completions.create(
            model="llama-3-sonar-large-32k-online",
            messages=messages,
            temperature=0.2,
            max_tokens=1,
            top_p=1,
        )
        response_message = response.choices[0].message.content.strip()
        print(response_message)
        return response_message.lower() == 'true'
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return False

async def recipeGenerator(recipe):
    print("👽 wysylam przepis do sformatowania przez gpt")
    try:
        messages = [
            {
                "role": "system",
                "content": "Jesteś ekspertem kulinarnym, który analizuje tekst przepisu i zwraca dane w formacie JSON."
            },
            {
                "role": "user",
                "content": f"Na podstawie poniższego tekstu dotyczącego przepisu, proszę przygotować dane i zwrócić tylko i wyłącznie w formacie JSON z poniższą strukturą:\n\n{{\n  \"nazwa\": \"\",\n  \"czas_przygotowania\": 0,\n  \"zdjecie_url\": \"\",\n  \"opis\": \"\",\n  \"instrukcja\": \"\",\n  \"skladniki\": [],\n  \"zrodlo_url\":\"\n}}\n\nInstrukcje:\n\n1. Wyodrębnij nazwę przepisu z tekstu i wpisz ją w polu \"nazwa\". Jeśli nazwa nie jest podana, pozostaw to pole puste.\n\n2. Jeśli czas przygotowania jest podany w tekście, wpisz go w minutach w polu \"czas_przygotowania\". W przeciwnym razie pozostaw 0.\n\n3. Jeśli w tekście znajduje się adres URL zdjęcia przepisu, wpisz go w polu \"zdjecie_url\". W przeciwnym razie pozostaw puste pole.\n\n4. Wyodrębnij opis przepisu z tekstu i wpisz go w polu \"opis\". Jeśli opis nie jest podany, pozostaw to pole puste.\n\n5. Wyodrębnij instrukcję przygotowania z tekstu i wpisz ją w polu \"instrukcja\". Jeśli instrukcja jest podzielona na kroki, połącz je w jeden ciągły tekst. Jeśli instrukcja nie jest podana, pozostaw to pole puste.\n\n6. Wyodrębnij listę składników z tekstu i wpisz je w polu \"skladniki\" jako tablicę. Jeśli składniki nie są podane, pozostaw pustą tablicę []. Składniki mają być podane w tablicy oddzielone przecinkami, np. [\"250g makaronu\", \"300g wody\", \"450g śmietanki\"]\n\n7. Tekst przepisu:\n{recipe}\n\nPamiętaj, aby zwrócić dane tylko w formacie JSON zgodnie z powyższą strukturą, bez dodatkowych informacji. Nie zmieniaj nazw kluczy. Wszystkie wartości typu string muszą być w podwójnych cudzysłowach, a tablica składników musi być poprawnie sformatowana. Tekst w wartościach ma być dobrze sformatowany, poprawny stylistycznie i ortograficznie."
            }
        ]

        response = client.chat.completions.create(model="llama-3-sonar-large-32k-chat",
        messages=messages,
        temperature=0.2,
        max_tokens=4096,
        top_p=1)
        response_message = response.choices[0].message.content
        print(response_message)
        return response_message
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return {}
