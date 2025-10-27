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
        """Analyserar observationen och returnerar nästa steg (typ av action)."""

        # 1. Dubbletter
        action = self._handle_duplicates(observation)
        if action:
            return action

        # 2. Ofullständiga tasks
        action = self._handle_incomplete_tasks(observation)
        if action:
            return action

        # 3. Nya uppgifter
        action = self._handle_task_creation(observation)
        if action:
            return action

        # 4. Inget kvar att göra
        return Action(type="none", info="All tasks already completed.")
    
    # ---------------- Hjälpfunktioner ------------------
       
    # Hitta dubletter
    def _find_duplicates(self, observation: Observation) -> int | None:
        """Returnerar index för första duplicerade task, eller None om inga finns."""
        titles_seen = set() # Skapar en lista som inte kan innehålla dubletter
        for i, t in enumerate(observation.tasks):
            title = t.title.strip().lower()
            if title in titles_seen:
                return i
            titles_seen.add(title)
        return None
    
    # Ta bort dubletter
    def _handle_duplicates(self, observation: Observation) -> Action | None:
        index = self._find_duplicates(observation)
        if index is not None:
            return Action(type="delete", index=index, info="Removed duplicate task")
        return None
    
    def _handle_incomplete_tasks(self, observation: Observation) -> Action | None:
        incomplete = [t for t in observation.tasks if not t.description]
        if not incomplete:
            return None

        target = max(incomplete, key=lambda t: t.priority)
        index = observation.tasks.index(target)
        enriched = self._enrich_task(target.title)
        return Action(type="update", index=index, task=enriched, info = f"Enriched task: {enriched.title}")

    def _handle_task_creation(self, observation: Observation) -> Action | None:
        if len(observation.tasks) <= 20:
            new_task = self._create_task()
            return Action(type="add", task=new_task, info = f"Created new task: {new_task.title}")
        return None

    # LLM skapar en ny gårdsrelaterad uppgift
    def _create_task(self) -> Task:
        prompt = """
        Skapa EN ny gårdsrelaterad uppgift i JSON-format.
        Fält: title, priority, description, preparations, practical_desc, grants
        Skriv **endast JSON**, fyll ALLA fält. Om du inte vet något, skriv "Ej specificerat".
        Håll varje texts längd under 100 tecken.
        
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

    # Uppdaterar de tasks där info saknas
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

            # Kolla om ticks fortf finns
            # print("LLM raw response:", repr(raw))

            # Ta bort Markdown-kodblock om de finns
            if raw.startswith("```"):
                lines = raw.split("\n")
                # ta bort första raden (```json eller ```) och sista raden (```)
                raw = "\n".join(line for line in lines[1:-1] if not line.strip().startswith("```"))
            
            data = json.loads(raw)

        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print("LLM gav ogiltig JSON eller tomt svar:", e)
            data = {}

        # defaultvärden
        return Task(
            title=title,
            priority=1,
            description=data.get("description", "Ej specificerat"),
            preparations=data.get("preparations", "Ej specificerat"),
            practical_desc=data.get("practical_desc", "Ej specificerat"),
            grants=data.get("grants", "Ej specificerat")
        )

    # publik metod för att llm ska skapa task
    def create_a_proper_task(self) -> Task:
        return self._create_task()