import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from models import Task, Observation, Action

load_dotenv()

class Agent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def decide(self, observation: Observation) -> Action:
        """Analyserar observationen och returnerar nästa steg."""
        for i, task in enumerate(observation.tasks):
            if not task.description:
                enriched = self._enrich_task(task.title)
                return Action(type="update", index=i, task=enriched)

        if len(observation.tasks) < 20:
            new_task = self._create_task()
            return Action(type="add", task=new_task)

        return Action(type="none", info="All tasks already complete.")

    # === interna hjälpfunktioner ===
    def _create_task(self) -> Task:
        prompt = """
        Skapa EN ny gårdsrelaterad uppgift i JSON-format.
        Fält: title, priority, description, preparations, practical_desc, grants
        Skriv **endast JSON**, fyll ALLA fält. Om du inte vet något, skriv "Ej specificerat".
        
        Exempel:
        {
            "title": "Rengöring hönshus",
            "priority": 2,
            "description": "Tvätta hönshuset...",
            "preparations": "Skaffa rengöringsmedel",
            "practical_desc": "Arbeta i par",
            "grants": "Ej specificerat"
        }
        """
        response = self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        raw = response.choices[0].message.content.strip()

        # Ta bort Markdown-ticks om de finns
        if raw.startswith("```") and raw.endswith("```"):
            raw = "\n".join(raw.split("\n")[1:-1])  # tar bort första och sista raden

        print("Cleaned LLM output:", raw)

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            data = {}


        # har default-värden
        return Task(
            title=data.get("title", "Ny uppgift"),
            priority=data.get("priority", 1),
            description=data.get("description", "Ej specificerat"),
            preparations=data.get("preparations", "Ej specificerat"),
            practical_desc=data.get("practical_desc", "Ej specificerat"),
            grants=data.get("grants", "Ej specificerat")
        )



    def _enrich_task(self, title: str) -> Task:
        prompt = f"""
        Förbättra uppgiften '{title}' med fälten:
        description, preparations, practical_desc, grants
        Skriv **endast JSON**, fyll ALLA fält.
        Om du inte har information, skriv "Ej specificerat".
        """
        try:
            response = self.client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
            )
            raw = response.choices[0].message.content.strip()

            if not raw:
                raise ValueError("Tomt LLM-svar")

            data = json.loads(raw)

        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print("LLM gav ogiltig JSON eller tomt svar:", e)
            data = {}

        # Säkerställ att alla fält får ett defaultvärde
        return Task(
            title=title,
            priority=1,
            description=data.get("description", "Ej specificerat"),
            preparations=data.get("preparations", "Ej specificerat"),
            practical_desc=data.get("practical_desc", "Ej specificerat"),
            grants=data.get("grants", "Ej specificerat")
        )
