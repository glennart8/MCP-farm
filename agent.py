from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()

class Agent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def decide(self, observation):
        notes = observation["notes"]
        prompt = f"""
                Du är en AI-agent som styr en lista med anteckningar.
                Nuvarande anteckningar: {json.dumps(notes, ensure_ascii=False)}

                Du kan göra en av tre åtgärder:
                1. Lägg till en ny anteckning: {{"type": "add", "content": "Ny idé"}}
                2. Uppdatera en befintlig anteckning: {{"type": "update", "index": 0, "content": "Förbättrad anteckning"}}
                3. Ta bort en anteckning: {{"type": "remove", "content": "Onödig anteckning"}}

                Välj EN åtgärd som verkar vettig. Returnera **endast JSON**.
                Det ska helst inte finnas fler än 20 st antecknignar.
                        """

        response = self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        raw = response.choices[0].message.content.strip()

        # Ta bort ev. ```json ... ```-taggar
        if raw.startswith("```json"):
            raw = raw[len("```json"):].strip()
        if raw.endswith("```"):
            raw = raw[:-3].strip()

        try:
            action = json.loads(raw)
        except json.JSONDecodeError:
            print("⚠️ Kunde inte tolka svaret som JSON:", raw)
            action = {"type": "add", "content": "Fel i JSON-parsning"}

        return action
