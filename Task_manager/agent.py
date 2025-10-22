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
        
    def create_a_proper_task(self):
        prompt = f"""
            Skapa en ny passande uppgift med fälten title, priority, description, preparations, practical_desc och grants.
            Det ska vara en typisk uppgift som tillhör ett gårdsbruk, exempelområden är:
            - djurhållning
            - odling
            - skogsarbete
            - byggnation
            - reparation
            - inköp till gården
            
            Skriv **endast JSON**, utan ``` eller andra Markdown-ticks.
            
            Exempel på korrekt format:
            {{
                "title": "...",
                "priority": 1,
                "description": "...",
                "preparations": "...",
                "practical_desc": "...",
                "grants": "..."
            }}
            """
        
        response = self.client.chat.completions.create(
            model="gemini-2.5-flash", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        raw = response.choices[0].message.content.strip()
 
        try:
            data = json.loads(raw)
            new_task = Task(**data)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print("Fel i LLM-output:", e)

        return new_task  # returnerar ett Task-objekt    
    

    def decide_what_to_do(self, observation):
        tasks = observation["tasks"]

        for i, t in enumerate(tasks):
            if not t["description"]:
                task_update = self.enrich_task_info(t["title"])
                # Returnera kwargs som Environment kan använda
                return {"type": "update", "index": i, "kwargs": task_update.model_dump()}
        if len(tasks) < 30:
            new_task = self.create_a_proper_task()
            return {"type": "add", "title": new_task.title, "priority": new_task.priority, "kwargs": new_task.model_dump()}
        else:                               
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
            model="gemini-2.5-flash", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        # Tar ut själva svaret, inget llm-message osv
        raw = response.choices[0].message.content.strip()
        # print("LLM raw output:", raw)  # <--- se vad som faktiskt kommer tillbaka
 
        try:
            # gör till dict
            data = json.loads(raw)
            # uppdatera
            task_update = Task(title=title, priority=1, **data)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print("Fel i LLM-output:", e)
            # Bevarar som tidigare
            task_update = Task(title=title, priority=1)

        return task_update  # returnerar ett Task-objekt
