from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from task_model import Task  # Pydantic Task

load_dotenv()

class Agent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def decide(self, observation):
        tasks = observation["tasks"]

        for i, t in enumerate(tasks):
            if not t["description"]:
                task_update = self.enrich_task_info(t["title"])
                # Returnera kwargs som Environment kan använda
                return {"type": "update", "index": i, "kwargs": task_update.dict()}

        return {"type": "none"}

    def enrich_task_info(self, title):
        prompt = f"""
            Skapa en JSON för uppgiften '{title}' med fälten description, preparations, practical_desc och grants.
            Skriv **endast JSON**, utan ``` eller andra Markdown-ticks.
            Exempel på korrekt format:
            {{
                "description": "...",
                "preparations": "...",
                "practical_desc": "...",
                "grants": "..."
            }}
            """

        response = self.client.chat.completions.create(
            model="gemini-2.5-flash",  # byt till korrekt modell
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        raw = response.choices[0].message.content.strip()
        # print("LLM raw output:", raw)  # <--- se vad som faktiskt kommer tillbaka
 
        
        data = json.loads(raw)

        try:
            data = json.loads(raw)
            # Validera mot Task-modellen, title och priority fyller jag i själv
            task_update = Task(title=title, priority=1, **data)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print("Fel i LLM-output, använder tomma standardvärden:", e)
            task_update = Task(title=title, priority=1)

        return task_update  # returnerar ett Task-objekt
