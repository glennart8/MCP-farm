import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from .products import PRODUCTS

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
load_dotenv()

class BaseAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def run_llm(self, prompt, temperature=0.5):
        response = self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        return raw

    def run_llm_json(self, prompt, temperature=0.3):
        """
        Kör ett prompt som ska returnera JSON.
        Returnerar Python-dict, eller None om parsing misslyckas.
        """
        raw = self.run_llm(prompt, temperature=temperature)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            print("AI-svaret gick inte att tolka:", raw)
            return None

class SupervisorAgent(BaseAgent):
    def decide(self, email):
        prompt = f"""
        Du är en kontorsassistent. Läs följande e-post och bestäm vilken kategori den tillhör.

        "support" - hanterar klagomål
        "sales" - hanterar offerter och köp
        "meeting" - hanterar möten
        "estimate" - hanterar uppsksattning av virkesåtgång för byggprojekt.
        "other" - övriga ärenden som ej kan klassificeras enligt ovan
    
        E-post:
        Avsändare: {email['from']}
        Ämne: {email['subject']}
        Meddelande: {email['body']}

        Välj EN kategori och svara ENBART med JSON:
        {{
            "decision": "support" | "sales" | "meeting" | "estimate" | "other",
            "reason": "Kort förklaring varför"
            "product": "T.ex. 'banan'"
            "meeting_time": "YYYY-MM-DDTHH:MM:SS"  # om mailet är ett möte
        }}
        
        Om du väljer "sales", skicka med produkten som kunden vill köpa också.
        
        Om du väljer "meeting":
            Extrahera datum och tid för mötet i ISO-format (YYYY-MM-DDTHH:MM:SS) och returnera ENBART som JSON:
            {{"decision": "meeting", "meeting_time": "2025-11-01T10:00:00"}}
        """
        
        data = self.run_llm_json(prompt)
        if not data:
            return "other", None, None
        return data.get("decision", "other"), data.get("product"), data.get("meeting_time")
    

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
        
        return self.run_llm(prompt)


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

        return self.run_llm(prompt)
    

    def extract_order_from_email(self, email):
        prompt = f"""
        Du är en byggvaruexpert som hjälper till att tolka kundbeställningar.
        Läs följande kundmail och returnera en JSON med antal per produkt.
        Använd dig av det som finns i sortimentet: {PRODUCTS}
        
        Om något inte finns i sortimentet, inkludera det under 'not_found', 
        och ge ett likvärdigt produktnamn under 'suggestions' kopplat till den saknade produkten.
        
        Mail:
        {email['body']}
        
        Svara ENBART med JSON, t.ex.:
        {{
            "found": {{"plywood": 2, "bräda_22x145": 5}},
            "not_found": {{"isolering_glasull": 1}},
            "suggestions": {{"isolering_glasull": "träfiberisolering"}}
        }}
        """
        
        raw = self.run_llm(prompt)
        try:
            data = json.loads(raw)
            return {
                "found": data.get("found", {}),
                "not_found": data.get("not_found", {}),
                "suggestions": data.get("suggestions", {})
            }
        except json.JSONDecodeError:
            print("Kunde inte tolka LLM-svar:", raw)
            return {"found": {}, "not_found": {}, "suggestions": {}}
        
    #  UPPSKATTA ÅTGÅNG (ESTIMATE)
    # def estimate_materials_text(self, description: str):
    #     prompt = f"""
    #     Du är en byggnadsteknisk assistent. Läs följande beskrivning av ett byggprojekt
    #     och skriv en användarvänlig uppskattning av materialåtgången som kan skickas
    #     direkt som ett mail till kunden.

    #     Beskrivning: {description}

    #     Använd detta produktsortiment: {PRODUCTS}

    #     Antag följande riktlinjer:
    #     - Inga hälsningsfraser
    #     - Ytterväggar består av regel 45x145 cc600, beklädda med 22x145 panel.
    #     - Bärande väggar ca 2,5 m höga, ytterväggslängd ≈ 4 × (yta ** 0.5).
    #     - Plywood används 1 skiva per 1,2 m² väggyta.
    #     - Isolering motsvarar väggytan i m².
    #     - Undertak ≈ byggytan i m², använd råspontlucka.
    #     - Inkludera längd/bredd/kvm i resultaten
    #     - Avsluta inte med artigheter utan sluta när du presenterat antalet av varje produkt.

    #     Skriv resultatet i punktlista med antal per produkt, t.ex.:
    #     Yttervägg
    #     - regel_45x145: 76 st
    #     - bräda_22x145: 146 st
    #     - "spiklåda_70mm": 2 st
    #     Tak
    #     - regel_45x145: 20 st
        
    #     Innervägg
    #     - plywood_12mm: 119 st
    #     - "skruvlåda_trä_4x40": 2 st
    #     """
    #     return self.run_llm(prompt)
    
    def estimate_materials_json(self, description: str):
        prompt = f"""
        Du är en byggnadsteknisk assistent. Läs följande beskrivning av ett byggprojekt
        och uppskatta materialåtgången baserat på standardbyggteknik i Sverige.
        
        Beskrivning: {description}
        
        Använd produktsortimentet: {PRODUCTS}
        Följ dessa riktlinjer:
        - Ytterväggar: regel_45x145 cc600 + bräda_22x145 panel
        - Plywood: 1 skiva per 1.2 m² väggyta
        - Isolering: väggyta per förpackning enligt PRODUCTS
        - Undertak: råspontlucka enligt PRODUCTS
        - Inkludera endast produkter som behövs
        
        **Viktigt:** Returnera endast ett JSON-objekt med format:
        {{
        "regel_45x145": <antal>,
        "bräda_22x145": <antal>,
        "plywood_12mm": <antal>,
        "isolering_mineralull_145mm": <antal>,
        "råspontlucka_21x95": <antal>
        }}
        Inga förklaringar, inga listor, inga kommentarer, inga punktlistor, endast JSON.
        """
        return self.run_llm_json(prompt)