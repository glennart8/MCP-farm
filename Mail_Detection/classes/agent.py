import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class Agent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def decide(self, email):
        prompt = f"""
        Du är en kontorsassistent. Läs följande e-post och bestäm vilken kategori den tillhör.

        E-post:
        Avsändare: {email['from']}
        Ämne: {email['subject']}
        Meddelande: {email['body']}

        Välj EN kategori och svara ENBART med JSON:
        {{
            "decision": "support" | "sales" | "meeting" | "other",
            "reason": "Kort förklaring varför"
            "product": "T.ex. 'banan'"
        }}
        
        Om du väljer "sales", skicka med produkten som kunden vill köpa också.
        """

        response = self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(raw)
            decision = data.get("decision", "other")
            product = data.get("product")  # kan bli None om det inte finns
            return decision, product
        except json.JSONDecodeError:
            print("AI-svaret gick inte att tolka:", raw)
            return "other"
