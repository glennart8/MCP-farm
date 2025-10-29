import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from .models import Task, Observation, Action

# Agenten ska ta beslutet och skicka själva beslutet till enviroment

load_dotenv()

class Agent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def decide(self, observation: Observation) -> Action:
        """Analyserar observationen och returnerar nästa action."""
        action = self._handle_duplicates(observation)
        if action:
            return action

        action = self._handle_incomplete_tasks(observation)
        if action:
            return action

        action = self._handle_task_creation(observation)
        if action:
            return action

        return Action(type="none", info="All tasks already completed.")
        
    # Dubletter
    def _handle_duplicates(self, observation: Observation) -> Action | None:
        index = self._find_duplicates(observation)
        if index is not None:
            return Action(type="delete", index=index, info="Removed duplicate task")
        return None
    
    # Skapar lista över tasks, loopar observationslistan, lägger titeln i listan, hittas en match, returneras index för den tasken
    def _find_duplicates(self, observation: Observation) -> int | None:
        """Returnerar index för första duplicerade task, eller None om inga finns."""
        titles_seen = set()
        for i, t in enumerate(observation.tasks):
            title = t.title.strip().lower()
            if title in titles_seen:
                return i
            titles_seen.add(title)
        return None
    
    # Ofullständiga tasks
    def _handle_incomplete_tasks(self, observation: Observation) -> Action | None:
        incomplete = [t for t in observation.tasks if not t.description]
        if not incomplete:
            return None

        # Ta den med högst prio
        target = max(incomplete, key=lambda t: t.priority)
        index = observation.tasks.index(target)
        enriched = self._enrich_task(target.title)
        return Action(type="update", index=index, task=enriched)

    # Skapa task    
    def _handle_task_creation(self, observation: Observation) -> Action | None:
        # Skapa ny task BARA om inga ofullständiga finns
        incomplete = [t for t in observation.tasks if not t.description]
        if incomplete:
            return None

        if len(observation.tasks) <= 20:
            new_task = self._create_task()
            return Action(type="add", task=new_task)
        return None


    # === interna hjälpfunktioner ===
    def _normalize_task_data(self, data: dict) -> Task:
        """Säkerställer att all data har rätt typ och priority är int mellan 1–5."""
        
        def ensure_str(value):
            """Gör om allt till sträng på ett säkert sätt."""
            if isinstance(value, str):
                return value
            elif isinstance(value, list):
                return " ".join(map(str, value))
            elif isinstance(value, dict):
                return json.dumps(value, ensure_ascii=False)
            elif value is None:
                return "Ej specificerat"
            else:
                return str(value)

        # Säkerställ att priority är ett heltal mellan 1–5
        try:
            priority = int(data.get("priority", 1))
            if not (1 <= priority <= 5):
                priority = 1
        except (ValueError, TypeError):
            priority = 1

        # Bygg upp Task-objektet med strängsäkring
        return Task(
            title=ensure_str(data.get("title", "Ny uppgift")),
            priority=priority,
            description=ensure_str(data.get("description", "Ej specificerat")),
            preparations=ensure_str(data.get("preparations", "Ej specificerat")),
            practical_desc=ensure_str(data.get("practical_desc", "Ej specificerat")),
            grants=ensure_str(data.get("grants", "Ej specificerat")),
        )

    def _delete_markdown(self, raw: str) -> str:
        if raw.startswith("```") and raw.endswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(line for line in lines[1:-1] if not line.strip().startswith("```"))
        return raw

    def _create_task(self) -> Task:
        prompt = """
        Skapa EN ny gårdsrelaterad uppgift i JSON-format.
        Exempel på områden - odling, djurhållning, skogsbruk, reparation, renovering.
        Fält: title, priority, description, preparations, practical_desc, grants
        Skriv **endast JSON**, fyll ALLA fält. Om du inte vet något, skriv "Ej specificerat".
        Priority ska vara ett heltal mellan 1–5.
        Håll varje texts längd under 100 tecken.
        
        Exempel:
        {
            "title": "Måla om ladans väggar",
            "priority": 3,
            "description": "Förnya färgen på ladans träpanel.",
            "preparations": "Köp färg och penslar. Slipa ytan innan målning.",
            "practical_desc": "Måla två lager med torktid emellan. Börja från toppen.",
            "grants": "Ej specificerat"
        }
        
        Ange hållbara metoder och material när du t.ex. skapar "preparations" och practical_desc".
        """
        
        response = self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        raw = response.choices[0].message.content.strip()

        cleaned_raw = self._delete_markdown(raw)

        print("Cleaned LLM output:", cleaned_raw)

        try:
            data = json.loads(cleaned_raw)
        except json.JSONDecodeError:
            data = {}

        return self._normalize_task_data(data)

    def _enrich_task(self, title: str) -> Task:
        prompt = f"""
        Förbättra uppgiften '{title}' med fälten:
        description, preparations, practical_desc, grants
        Skriv **endast JSON**, fyll ALLA fält.
        Om du inte har information, skriv "Ej specificerat".
        VIKTIGT: Håll dig kortfattad med max 100 tecken per fält!

        
        Exempel:
            {
            "title": "Plantera potatis",
            "priority": 4,
            "description": "Sätta potatisknölar i jorden för skörd.",
            "preparations": "Förbered jorden, skaffa sättpotatis, hämta redskap.",
            "practical_desc": "Gräv fåror, placera potatis, täck med jord. Vattna vid behov.",
            "grants": "För visst jordbruk finns bidrag att söka, enligt jordbruksverket...."
            },
        """
        try:
            response = self.client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
            )
            raw = response.choices[0].message.content.strip()

            cleaned_raw = self._delete_markdown(raw)
            data = json.loads(cleaned_raw)

        except (json.JSONDecodeError, TypeError, ValueError):
            data = {}

        return self._normalize_task_data({**data, "title": title})

