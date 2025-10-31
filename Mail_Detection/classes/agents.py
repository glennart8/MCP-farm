import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
load_dotenv()



class BaseAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )


class SupervisorAgent(BaseAgent):
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
            "meeting_time": "YYYY-MM-DDTHH:MM:SS"  # om mailet är ett möte
        }}
        
        Om du väljer "sales", skicka med produkten som kunden vill köpa också.
        
        Om du väljer "meeting":
            Extrahera datum och tid för mötet i ISO-format (YYYY-MM-DDTHH:MM:SS) och returnera ENBART som JSON:
            {{"decision": "meeting", "meeting_time": "2025-11-01T10:00:00"}}
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
            meeting_time = data.get("meeting_time")  # kan vara None
            return decision, product, meeting_time
        except json.JSONDecodeError:
            print("AI-svaret gick inte att tolka:", raw)
            return "other"

class ComplaintAgent(BaseAgent):
    def write_response_to_complaint(self, email):
        prompt = f"""
        Du är en kontorsassistent som besvarar klagomål via mail. Läs {email} och skapa ett anpassat, trevligt och kort svar.
        Innehåll: 
        Bekräftelse på emottagande av mail och vad klagomålet avser.
        En försäkran om att detta ska tas vidare och att vi ber att få återkomma.
        
        Skriv: Detta mail skickades: {now}
        
        Avsluta med att önska en fortsatt trevligt dag/kväll.
        Med vänliga hälsningar,

        [Kontorsassistenten]
        [Det orubbliga företaget]
        """

        response = self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        return raw

class SalesAgent(BaseAgent):
    def write_response_to_order(self, email):
        prompt = f"""
        Du är en vänlig kontorsassistent som skriver ett kvitto/bekräftelse på ett köp. 
        Läs följande kundmail: {email}

        Skapa ett kort, professionellt och trevligt svar som innehåller:
        1. Bekräftelse på att kundens beställning har mottagits.
        2. Specificera vad kunden önskar köpa (om det framgår av mailet).
        3. Tiden då kvittot skickas: {now}
        4. Avsluta med en vänlig hälsning och önska en fortsatt trevlig dag/kväll.

        Skriv svaret på ett sätt som kan skickas direkt till kunden.
        """

        response = self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        return raw
